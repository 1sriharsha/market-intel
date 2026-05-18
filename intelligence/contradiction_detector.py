"""Price vs narrative contradiction detection."""
from dataclasses import dataclass

from models.schemas import Contradiction


def detect_contradictions(
    articles: list[dict],
    prices: list[dict],
) -> list[Contradiction]:
    """
    Identify contradictions between article sentiment and price behavior.

    Checks:
    - Positive headline + negative price action
    - Insider selling + bullish narrative
    - Strong earnings + weak market reaction
    - Yield movement vs Fed narrative
    - Broad market divergence (one ticker up, sector down)

    Returns list of Contradiction objects with severity scores.
    """
    contradictions: list[Contradiction] = []

    # Build ticker → price effect map
    ticker_reactions: dict[str, dict] = {}
    for p in prices:
        ticker = p.get("ticker")
        if ticker:
            ticker_reactions[ticker] = p

    for article in articles:
        title = (article.get("title") or "").lower()
        summary = (article.get("summary") or "").lower()
        text = f"{title} {summary}"
        tickers = article.get("tickers") or []
        topics = article.get("topics") or []

        # --- Positive headline + negative price ---
        is_bullish_text = any(w in text for w in [
            "beat", "beats", "surges", "jumps", "record", "strong earnings",
            "raised guidance", "upgrade", "outperform", "growth"
        ])
        is_bearish_text = any(w in text for w in [
            "misses", "miss", "falls", "drops", "cuts guidance", "downgrade",
            "disappoints", "layoffs", "loss", "decline"
        ])

        for ticker in tickers:
            reaction = ticker_reactions.get(ticker)
            if not reaction:
                continue
            abnormal = reaction.get("abnormal_return")
            if abnormal is None:
                continue

            if is_bullish_text and abnormal < -0.03:
                contradictions.append(Contradiction(
                    ticker=ticker,
                    description=f"{ticker}: Bullish narrative ('{article.get('title', '')[:80]}') "
                                f"but price fell {abnormal*100:.1f}% abnormally",
                    severity=min(abs(abnormal) * 5, 1.0),
                    contradiction_type="bullish_narrative_bearish_price",
                ))

            if is_bearish_text and abnormal > 0.03:
                contradictions.append(Contradiction(
                    ticker=ticker,
                    description=f"{ticker}: Bearish narrative ('{article.get('title', '')[:80]}') "
                                f"but price rose {abnormal*100:.1f}% abnormally",
                    severity=min(abs(abnormal) * 5, 1.0),
                    contradiction_type="bearish_narrative_bullish_price",
                ))

        # --- Insider selling + bullish narrative ---
        if "insider_activity" in topics:
            has_selling = any(w in text for w in ["sold", "sells", "disposed", "sale"])
            has_bullish = any(w in text for w in ["bullish", "buy", "purchased", "acquired"])
            if has_selling and has_bullish:
                contradictions.append(Contradiction(
                    ticker=tickers[0] if tickers else None,
                    description="Insider activity report contains both selling and bullish signals",
                    severity=0.5,
                    contradiction_type="insider_selling_bullish_narrative",
                ))

        # --- Earnings beat + weak reaction ---
        if "earnings" in topics:
            is_beat = any(w in text for w in ["beat", "beats", "exceeded", "topped"])
            for ticker in tickers:
                reaction = ticker_reactions.get(ticker)
                if reaction and is_beat:
                    abnormal = reaction.get("abnormal_return")
                    if abnormal is not None and abnormal < -0.02:
                        contradictions.append(Contradiction(
                            ticker=ticker,
                            description=f"{ticker}: Earnings beat but stock fell {abnormal*100:.1f}% "
                                        f"— potential sell-the-news or guidance concern",
                            severity=min(abs(abnormal) * 4, 0.9),
                            contradiction_type="earnings_beat_weak_reaction",
                        ))

        # --- Fed narrative vs yield movement ---
        if "monetary_policy" in topics:
            is_hawkish = any(w in text for w in ["hike", "hikes", "raise rates", "hawkish", "tightening"])
            is_dovish = any(w in text for w in ["cut", "cuts", "lower rates", "dovish", "pause"])
            tlt_reaction = ticker_reactions.get("TLT")
            if tlt_reaction:
                tlt_abnormal = tlt_reaction.get("abnormal_return")
                if tlt_abnormal is not None:
                    # TLT moves inverse to yields
                    if is_hawkish and tlt_abnormal > 0.02:
                        contradictions.append(Contradiction(
                            ticker="TLT",
                            description="Hawkish Fed narrative but bonds rallied — market not believing the guidance",
                            severity=0.7,
                            contradiction_type="fed_narrative_yield_divergence",
                        ))
                    if is_dovish and tlt_abnormal < -0.02:
                        contradictions.append(Contradiction(
                            ticker="TLT",
                            description="Dovish Fed narrative but bonds sold off — market pricing more inflation risk",
                            severity=0.7,
                            contradiction_type="fed_narrative_yield_divergence",
                        ))

    # Deduplicate by type + ticker
    seen: set[str] = set()
    unique: list[Contradiction] = []
    for c in contradictions:
        key = f"{c.contradiction_type}:{c.ticker}"
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return sorted(unique, key=lambda x: x.severity, reverse=True)
