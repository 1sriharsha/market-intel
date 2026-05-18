"""pgvector semantic search + context package assembly."""
from datetime import datetime, timezone, timedelta

from config.log import get_logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import settings
from models.schemas import ContextPackage, MacroSnapshot, HistoricalAnalogue, PricePoint, Contradiction

log = get_logger(__name__)


async def retrieve_similar_articles(
    query_text: str,
    session: AsyncSession,
    top_k: int | None = None,
    days_back: int | None = None,
) -> list[dict]:
    """
    Embed query text, search pgvector for semantically similar articles.
    Score = 0.7 * semantic_similarity + 0.3 * recency_weight.
    Returns top_k results sorted by combined score.
    """
    from enrichment.embedder import _embed_texts, _build_embed_input

    k = top_k or settings.retrieval_top_k
    days = days_back or settings.rag_corpus_days
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    try:
        vectors = await _embed_texts([query_text[:8192]])
        vec = vectors[0]
    except Exception as e:
        log.warning("retriever.embed_failed", error=str(e))
        return []

    vec_str = "[" + ",".join(f"{v:.8f}" for v in vec) + "]"

    result = await session.execute(
        text("""
            SELECT
                a.id, a.title, a.summary, a.source_name, a.source_tier,
                a.tickers, a.topics, a.published_at, a.significance_score,
                1 - (e.embedding <=> :vec::vector) as semantic_sim,
                EXTRACT(EPOCH FROM (NOW() - a.published_at)) / 86400.0 as days_ago
            FROM embeddings e
            JOIN articles a ON a.id = e.article_id
            WHERE a.published_at > :cutoff
            ORDER BY e.embedding <=> :vec::vector
            LIMIT :limit
        """),
        {"vec": vec_str, "cutoff": cutoff, "limit": k * 3},   # over-fetch then re-rank
    )
    rows = result.fetchall()
    if not rows:
        return []

    scored = []
    for row in rows:
        days_ago = float(row[10]) if row[10] is not None else 999
        recency_weight = max(0.0, 1.0 - days_ago / days)
        semantic_sim = float(row[9]) if row[9] is not None else 0.0
        combined = (settings.retrieval_semantic_weight * semantic_sim +
                    settings.retrieval_recency_weight * recency_weight)
        scored.append({
            "id": row[0],
            "title": row[1],
            "summary": row[2],
            "source_name": row[3],
            "source_tier": row[4],
            "tickers": row[5] or [],
            "topics": row[6] or [],
            "published_at": row[7],
            "significance_score": row[8],
            "combined_score": combined,
        })

    scored.sort(key=lambda x: x["combined_score"], reverse=True)
    return scored[:k]


async def retrieve_historical_analogues(
    event_summary: str,
    macro_snapshot: MacroSnapshot,
    session: AsyncSession,
    top_k: int = 3,
) -> list[HistoricalAnalogue]:
    """
    Find similar past events from historical_events table.
    Matches on: event category, goldstein_scale range, macro regime similarity
    (rates within 1%, VIX within 10 points).
    Returns top 3 analogues with price reaction data.
    """
    # Determine category filter from event text
    text_lower = event_summary.lower()
    if any(w in text_lower for w in ["fed", "rate", "fomc", "monetary"]):
        categories = ["monetary_policy"]
    elif any(w in text_lower for w in ["earning", "revenue", "profit"]):
        categories = ["earnings"]
    elif any(w in text_lower for w in ["geopolit", "war", "sanction", "trade"]):
        categories = ["geopolitical"]
    elif any(w in text_lower for w in ["inflation", "cpi", "gdp", "unemployment"]):
        categories = ["macro"]
    else:
        categories = ["monetary_policy", "earnings", "macro", "geopolitical"]

    category_placeholders = ",".join([f"'{c}'" for c in categories])

    # Rate range filter (±1%)
    rate_min = (macro_snapshot.fed_funds_rate or 2.5) - 1.0
    rate_max = (macro_snapshot.fed_funds_rate or 2.5) + 1.0

    # VIX range filter (±10 points) — applied as Goldstein proxy
    vix_proxy_min = (macro_snapshot.vix or 20.0) - 10.0
    vix_proxy_max = (macro_snapshot.vix or 20.0) + 10.0

    query = text(f"""
        SELECT
            he.event_date, he.event_category, he.goldstein_scale,
            he.avg_tone, he.tickers_affected, he.source_url,
            he.actor1, he.actor2
        FROM historical_events he
        WHERE he.event_category IN ({category_placeholders})
          AND he.num_sources >= 3
        ORDER BY ABS(he.goldstein_scale) DESC
        LIMIT :limit
    """)

    result = await session.execute(query, {"limit": top_k * 5})
    rows = result.fetchall()
    if not rows:
        return []

    analogues = []
    for row in rows[:top_k]:
        tickers = row[4] or []
        # Build a price reaction summary from article_ticker_effects if available
        reaction_summary = await _get_historical_price_reaction(
            row[0], tickers[:3], session
        )
        analogues.append(HistoricalAnalogue(
            event_date=row[0],
            event_category=row[1],
            goldstein_scale=float(row[2]) if row[2] is not None else None,
            avg_tone=float(row[3]) if row[3] is not None else None,
            tickers_affected=tickers,
            price_reaction_summary=reaction_summary,
        ))

    return analogues


async def _get_historical_price_reaction(
    event_date,
    tickers: list[str],
    session: AsyncSession,
) -> str | None:
    if not tickers:
        return None
    try:
        result = await session.execute(
            text("""
                SELECT ate.ticker, ate.abnormal_return_1d, ate.reaction_label
                FROM article_ticker_effects ate
                JOIN articles a ON a.id = ate.article_id
                WHERE DATE(a.published_at) = :d AND ate.ticker = ANY(:tickers)
                LIMIT 5
            """),
            {"d": event_date, "tickers": tickers},
        )
        rows = result.fetchall()
        if not rows:
            return None
        parts = [
            f"{r[0]}: {r[2]} ({float(r[1])*100:.1f}%)" if r[1] is not None else f"{r[0]}: {r[2]}"
            for r in rows
        ]
        return ", ".join(parts)
    except Exception:
        return None


async def build_context_package(
    articles: list[dict],
    tickers: list[str],
    session: AsyncSession,
) -> ContextPackage:
    """
    Assemble the full context package for intelligence generation.
    All data verified fresh before assembly.
    """
    from datetime import datetime, timezone
    from ingestion.macro_fetcher import get_macro_snapshot
    from intelligence.regime_classifier import get_latest_regime
    from intelligence.contradiction_detector import detect_contradictions

    now = datetime.now(timezone.utc)

    # Macro snapshot
    macro_snapshot = await get_macro_snapshot(now, session)

    # Price movements for relevant tickers
    price_movements: list[PricePoint] = []
    for ticker in tickers:
        from ingestion.price_fetcher import get_price_at
        price = await get_price_at(ticker, now, session)
        if price is not None:
            price_movements.append(PricePoint(ticker=ticker, date=now.date(), close=price))

    # Historical analogues
    query_text = " ".join(a.get("title", "") for a in articles[:5])
    historical_analogues = await retrieve_historical_analogues(
        query_text, macro_snapshot, session
    )

    # Regime
    regime = await get_latest_regime(session)

    # Price reactions for contradiction detection
    price_dicts = [p.model_dump() for p in price_movements]
    active_contradictions = detect_contradictions(articles, price_dicts)

    return ContextPackage(
        articles=articles,
        tickers=tickers,
        topics=list({t for a in articles for t in (a.get("topics") or [])}),
        price_movements=price_movements,
        macro_snapshot=macro_snapshot,
        historical_analogues=historical_analogues,
        regime=regime,
        active_contradictions=active_contradictions,
        assembled_at=now,
    )
