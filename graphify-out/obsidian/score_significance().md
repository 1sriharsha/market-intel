---
source_file: "intelligence/signal_scorer.py"
type: "code"
community: "Signal Scoring"
location: "L19"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Signal_Scoring
---

# score_significance()

## Connections
- [[.test_score_capped_at_100()]] - `calls` [INFERRED]
- [[.test_single_tier4_scores_low()]] - `calls` [INFERRED]
- [[.test_tier1_multiple_sources_scores_high()]] - `calls` [INFERRED]
- [[Compute a 0–100 significance score for a batch of articles.      Inputs     - s]] - `rationale_for` [EXTRACTED]
- [[_enrichment_async()]] - `calls` [INFERRED]
- [[_tier_weight()]] - `calls` [EXTRACTED]
- [[score_significance_for_articles()]] - `calls` [INFERRED]
- [[signal_scorer.py]] - `contains` [EXTRACTED]
- [[test_significance_scorer_returns_zero_for_empty()]] - `calls` [INFERRED]
- [[test_significance_scorer_tier1_always_high()]] - `calls` [INFERRED]
- [[test_significance_scorer_tier4_scores_below_threshold()]] - `calls` [INFERRED]

#graphify/code #graphify/INFERRED #community/Signal_Scoring