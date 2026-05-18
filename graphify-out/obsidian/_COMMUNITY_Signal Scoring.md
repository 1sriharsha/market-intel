---
type: community
cohesion: 0.08
members: 30
---

# Signal Scoring

**Cohesion:** 0.08 - loosely connected
**Members:** 30 nodes

## Members
- [[.test_score_capped_at_100()]] - code - tests/unit/test_unit_misc.py
- [[.test_single_tier4_scores_low()]] - code - tests/unit/test_unit_misc.py
- [[.test_tier1_multiple_sources_scores_high()]] - code - tests/unit/test_unit_misc.py
- [[Articles below threshold that are skipped by intelligence cycle     must not be]] - rationale - tests/unit/test_low_significance_skips_generation.py
- [[CRITICAL TEST test_low_significance_skips_generation Cost control — articles be]] - rationale - tests/unit/test_low_significance_skips_generation.py
- [[Compute a 0–100 significance score for a batch of articles.      Inputs     - s]] - rationale - intelligence/signal_scorer.py
- [[Default significance threshold must be 65.0 per spec.]] - rationale - tests/unit/test_low_significance_skips_generation.py
- [[Empty article list must score 0.]] - rationale - tests/unit/test_low_significance_skips_generation.py
- [[Event significance scoring 0–100.]] - rationale - intelligence/signal_scorer.py
- [[Intelligence cycle must not process articles below SIGNIFICANCE_THRESHOLD.     A]] - rationale - tests/unit/test_low_significance_skips_generation.py
- [[Map numeric score to significance level enum value.]] - rationale - intelligence/signal_scorer.py
- [[Score-to-level mapping must match spec thresholds.]] - rationale - tests/unit/test_low_significance_skips_generation.py
- [[TestSignalScorer]] - code - tests/unit/test_unit_misc.py
- [[Tier 1 articles must always score well above default threshold.]] - rationale - tests/unit/test_low_significance_skips_generation.py
- [[Tier 4 (sentiment only) articles must score below threshold.]] - rationale - tests/unit/test_low_significance_skips_generation.py
- [[Wrapper for signal scorer — used by workers.]] - rationale - intelligence/engine.py
- [[_tier_weight()]] - code - intelligence/signal_scorer.py
- [[make_low_sig_article()]] - code - tests/unit/test_low_significance_skips_generation.py
- [[score_significance()]] - code - intelligence/signal_scorer.py
- [[score_significance_for_articles()]] - code - intelligence/engine.py
- [[signal_scorer.py]] - code - intelligence/signal_scorer.py
- [[significance_level_from_score()]] - code - intelligence/signal_scorer.py
- [[test_low_significance_articles_skipped_by_cycle()]] - code - tests/unit/test_low_significance_skips_generation.py
- [[test_low_significance_skips_generation.py]] - code - tests/unit/test_low_significance_skips_generation.py
- [[test_significance_level_mapping()]] - code - tests/unit/test_low_significance_skips_generation.py
- [[test_significance_scorer_returns_zero_for_empty()]] - code - tests/unit/test_low_significance_skips_generation.py
- [[test_significance_scorer_tier1_always_high()]] - code - tests/unit/test_low_significance_skips_generation.py
- [[test_significance_scorer_tier4_scores_below_threshold()]] - code - tests/unit/test_low_significance_skips_generation.py
- [[test_significance_threshold_default_is_65()]] - code - tests/unit/test_low_significance_skips_generation.py
- [[test_suppressed_articles_not_marked_processed_without_generation()]] - code - tests/unit/test_low_significance_skips_generation.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Signal_Scoring
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 2 edges to [[_COMMUNITY_External Data Fetching]]
- 1 edge to [[_COMMUNITY_Async DB & Celery Workers]]
- 1 edge to [[_COMMUNITY_Intelligence Generation]]
- 1 edge to [[_COMMUNITY_API Routes & Contradiction Detection]]
- 1 edge to [[_COMMUNITY_Macro & Regime Analysis]]

## Top bridge nodes
- [[signal_scorer.py]] - degree 6, connects to 2 communities
- [[TestSignalScorer]] - degree 5, connects to 2 communities
- [[score_significance()]] - degree 11, connects to 1 community
- [[test_low_significance_skips_generation.py]] - degree 11, connects to 1 community
- [[score_significance_for_articles()]] - degree 3, connects to 1 community