"""Main intelligence loop — retrieves context, calls Claude, writes intelligence objects."""
import json
import re
from datetime import datetime, timezone, timedelta
from typing import Optional

from config.log import get_logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import settings
from intelligence.prompts import SYSTEM_PROMPT, build_intelligence_prompt
from intelligence.signal_scorer import score_significance, significance_level_from_score
from models.schemas import ContextPackage, IntelligenceObjectCreate

log = get_logger(__name__)

_anthropic_client = None


def _get_client():
    global _anthropic_client
    if _anthropic_client is None:
        from anthropic import AsyncAnthropic
        _anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _anthropic_client


# ---------------------------------------------------------------------------
# Intelligence cycle
# ---------------------------------------------------------------------------

async def run_intelligence_cycle(
    session: AsyncSession,
    trigger: str = "scheduled",
) -> list[dict]:
    """
    Main intelligence loop.
    1. Fetch unprocessed high-significance articles from last cycle window
    2. Group by topic cluster
    3. For each cluster: build context → call Claude → validate → write → deliver
    4. Mark articles as processed
    """
    cycle_start = datetime.now(timezone.utc)
    cycle_window = timedelta(minutes=settings.intelligence_cycle_minutes * 2)
    cutoff = cycle_start - cycle_window

    # Fetch unprocessed high-significance articles
    result = await session.execute(
        text("""
            SELECT id, title, summary, source_name, source_tier, tickers, topics,
                   published_at, significance_score
            FROM articles
            WHERE is_processed = false
              AND significance_score >= :threshold
              AND published_at > :cutoff
            ORDER BY significance_score DESC
            LIMIT 100
        """),
        {"threshold": settings.significance_threshold, "cutoff": cutoff},
    )
    articles = [dict(zip(result.keys(), row)) for row in result.fetchall()]

    if not articles:
        log.info("intelligence.cycle.no_articles", trigger=trigger)
        return []

    # Group by topic cluster
    clusters = _cluster_by_topic(articles)
    log.info("intelligence.cycle.start", articles=len(articles), clusters=len(clusters), trigger=trigger)

    generated: list[dict] = []

    for cluster_topics, cluster_articles in clusters.items():
        all_tickers = list({t for a in cluster_articles for t in (a.get("tickers") or [])})

        try:
            from intelligence.retriever import build_context_package
            context = await build_context_package(cluster_articles, all_tickers, session)

            intel_obj = await generate_intelligence(context, session, trigger=trigger)
            if intel_obj:
                generated.append(intel_obj)

                # Evaluate delivery
                from delivery.telegram_bot import evaluate_delivery, format_message, push_message
                if await evaluate_delivery(intel_obj):
                    message = format_message(intel_obj)
                    success = await push_message(message, settings.telegram_chat_id)
                    if success:
                        await session.execute(
                            text("UPDATE intelligence_objects SET delivered_at = NOW() WHERE id = :id"),
                            {"id": intel_obj["id"]},
                        )

        except Exception as e:
            log.error("intelligence.cycle.cluster_failed", topics=cluster_topics, error=str(e))
            continue

    # Mark articles as processed
    article_ids = [a["id"] for a in articles]
    if article_ids:
        await session.execute(
            text("UPDATE articles SET is_processed = true WHERE id = ANY(:ids)"),
            {"ids": article_ids},
        )

    log.info("intelligence.cycle.complete", generated=len(generated), trigger=trigger)
    return generated


def _cluster_by_topic(articles: list[dict]) -> dict[str, list[dict]]:
    """Group articles by dominant topic. Simple priority-based clustering."""
    priority_topics = [
        "monetary_policy", "material_event", "earnings", "inflation",
        "employment", "geopolitical", "financial_stability", "regulation",
        "mergers_acquisitions", "ipo", "macro", "markets",
    ]

    clusters: dict[str, list[dict]] = {}
    for article in articles:
        topics = article.get("topics") or []
        assigned = "markets"
        for pt in priority_topics:
            if pt in topics:
                assigned = pt
                break
        if assigned not in clusters:
            clusters[assigned] = []
        clusters[assigned].append(article)

    return clusters


# ---------------------------------------------------------------------------
# Intelligence generation (single cluster)
# ---------------------------------------------------------------------------

async def generate_intelligence(
    context: ContextPackage,
    session: AsyncSession,
    trigger: str = "scheduled",
) -> dict | None:
    """
    Call Claude with assembled context package.
    Post-generation validation: strip hallucinated tickers, reject empty confidence_explanation.
    Writes IntelligenceObject to DB.
    """
    if not context.articles:
        return None

    prompt = build_intelligence_prompt(context.model_dump())
    client = _get_client()

    try:
        response = await client.messages.create(
            model=settings.llm_model,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        log.error("intelligence.claude_failed", error=str(e))
        return None

    raw_text = response.content[0].text if response.content else ""
    input_tokens = response.usage.input_tokens if response.usage else 0
    output_tokens = response.usage.output_tokens if response.usage else 0

    # Parse JSON output
    parsed = _parse_claude_output(raw_text)
    if not parsed:
        log.error("intelligence.parse_failed", raw=raw_text[:200])
        return None

    # Post-generation validation
    parsed = _validate_and_strip(parsed, context)
    if parsed is None:
        return None

    # Build intelligence object
    obj_data = {
        "trigger_type": trigger,
        "tickers": parsed.get("tickers", []),
        "topics": parsed.get("topics", []),
        "summary": parsed.get("summary", ""),
        "why_it_matters": parsed.get("why_it_matters"),
        "historical_context": parsed.get("historical_context"),
        "contradictions": parsed.get("contradictions"),
        "risks": parsed.get("risks"),
        "unknowns": parsed.get("unknowns"),
        "confidence_score": float(parsed.get("confidence_score", 0.5)),
        "confidence_explanation": parsed.get("confidence_explanation", ""),
        "significance_level": parsed.get("significance_level", "medium"),
        "source_article_ids": [a.get("id") for a in context.articles if a.get("id")],
        "llm_model": settings.llm_model,
        "llm_input_tokens": input_tokens,
        "llm_output_tokens": output_tokens,
    }

    result = await session.execute(
        text("""
            INSERT INTO intelligence_objects
                (trigger_type, tickers, topics, summary, why_it_matters, historical_context,
                 contradictions, risks, unknowns, confidence_score, confidence_explanation,
                 significance_level, source_article_ids, llm_model, llm_input_tokens, llm_output_tokens)
            VALUES
                (:trigger_type, :tickers, :topics, :summary, :why_it_matters, :historical_context,
                 :contradictions, :risks, :unknowns, :confidence_score, :confidence_explanation,
                 :significance_level, :source_article_ids, :llm_model, :llm_input_tokens, :llm_output_tokens)
            RETURNING id
        """),
        obj_data,
    )
    row = result.fetchone()
    obj_data["id"] = str(row[0]) if row else None

    log.info(
        "intelligence.generated",
        id=obj_data["id"],
        significance=obj_data["significance_level"],
        confidence=obj_data["confidence_score"],
        tickers=obj_data["tickers"],
    )
    return obj_data


def _parse_claude_output(text: str) -> dict | None:
    """Extract and parse JSON from Claude's response."""
    # Strip markdown code fences if present
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON object from surrounding text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return None


def _validate_and_strip(parsed: dict, context: ContextPackage) -> dict | None:
    """
    Post-generation validation:
    - Strip any ticker not present in context_package.tickers
    - Log hallucination event if tickers stripped
    - Reject if confidence_explanation is empty
    """
    context_tickers = set(context.tickers)

    output_tickers = parsed.get("tickers") or []
    valid_tickers = [t for t in output_tickers if t in context_tickers]
    stripped = [t for t in output_tickers if t not in context_tickers]

    if stripped:
        log.warning("intelligence.hallucinated_tickers", stripped=stripped)

    parsed["tickers"] = valid_tickers

    confidence_explanation = parsed.get("confidence_explanation", "").strip()
    if not confidence_explanation:
        log.error("intelligence.empty_confidence_explanation")
        return None

    # Ensure required fields exist
    if not parsed.get("summary"):
        log.error("intelligence.empty_summary")
        return None

    if not parsed.get("source_article_ids") and not context.articles:
        log.error("intelligence.no_source_articles")
        return None

    return parsed


async def score_significance_for_articles(articles: list[dict]) -> float:
    """Wrapper for signal scorer — used by workers."""
    return score_significance(articles)
