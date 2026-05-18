"""Event significance scoring 0–100."""
from config.settings import settings


# Source tier base weights
_TIER_WEIGHTS: dict[int, float] = {
    1: 40.0,    # Tier 1 canonical — highest weight
    2: 25.0,    # Tier 2A/2B wire services
    3: 15.0,    # Tier 2C financial press
    4: 8.0,     # Tier 3 structured APIs
    5: 2.0,     # Tier 4 sentiment only (near-zero)
}


def _tier_weight(tier: int) -> float:
    return _TIER_WEIGHTS.get(tier, 5.0)


def score_significance(articles: list[dict]) -> float:
    """
    Compute a 0–100 significance score for a batch of articles.

    Inputs:
    - source_tier weights
    - novelty_score (deviation from recent similar articles)
    - ticker_count (cross-asset relevance)
    - historical analogue match quality
    - macro regime sensitivity
    - presence of Tier 1 source confirmation

    Returns float 0–100.
    """
    if not articles:
        return 0.0

    # --- Base score: weighted average of source tiers ---
    tier_scores = [_tier_weight(a.get("source_tier", 4)) for a in articles]
    base_score = sum(tier_scores) / len(tier_scores)

    # --- Novelty boost: average novelty_score across articles ---
    novelty_scores = [
        a.get("novelty_score") for a in articles if a.get("novelty_score") is not None
    ]
    novelty_boost = 0.0
    if novelty_scores:
        avg_novelty = sum(novelty_scores) / len(novelty_scores)
        novelty_boost = avg_novelty * 0.20   # up to +20 points

    # --- Cross-asset relevance: unique ticker count ---
    all_tickers: set[str] = set()
    for a in articles:
        for t in (a.get("tickers") or []):
            all_tickers.add(t)
    ticker_count = len(all_tickers)
    ticker_boost = min(ticker_count * 2.0, 15.0)   # up to +15 points

    # --- Tier 1 confirmation bonus ---
    has_tier1 = any(a.get("source_tier") == 1 for a in articles)
    tier1_bonus = 15.0 if has_tier1 else 0.0

    # --- Article volume signal ---
    volume_bonus = min(len(articles) * 1.5, 10.0)   # up to +10 for corroboration

    raw_score = base_score + novelty_boost + ticker_boost + tier1_bonus + volume_bonus
    return min(round(raw_score, 2), 100.0)


def compute_novelty_score(article: dict, recent_articles: list[dict]) -> float:
    """
    Measure how novel an article is compared to recent similar articles.
    Simple heuristic: penalize if many recent articles share same tickers + topics.
    Returns 0–100.
    """
    if not recent_articles:
        return 100.0

    article_tickers = set(article.get("tickers") or [])
    article_topics = set(article.get("topics") or [])

    overlap_count = 0
    for recent in recent_articles:
        recent_tickers = set(recent.get("tickers") or [])
        recent_topics = set(recent.get("topics") or [])
        ticker_overlap = len(article_tickers & recent_tickers)
        topic_overlap = len(article_topics & recent_topics)
        if ticker_overlap > 0 or topic_overlap > 0:
            overlap_count += 1

    overlap_ratio = overlap_count / len(recent_articles)
    return round((1 - overlap_ratio) * 100.0, 2)


def significance_level_from_score(score: float) -> str:
    """Map numeric score to significance level enum value."""
    if score >= settings.significance_threshold_systemic:
        return "critical"
    if score >= settings.significance_threshold_major:
        return "high"
    if score >= settings.significance_threshold_meaningful:
        return "medium"
    if score >= settings.significance_threshold_moderate:
        return "low"
    return "suppressed"
