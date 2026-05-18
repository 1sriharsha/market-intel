---
type: community
cohesion: 0.16
members: 24
---

# Macro & Regime Analysis

**Cohesion:** 0.16 - loosely connected
**Members:** 24 nodes

## Members
- [[.test_compressed_vix()]] - code - tests/unit/test_unit_misc.py
- [[.test_confidence_drops_with_missing_data()]] - code - tests/unit/test_unit_misc.py
- [[.test_fearful_sentiment_extreme_vix()]] - code - tests/unit/test_unit_misc.py
- [[.test_full_data_high_confidence()]] - code - tests/unit/test_unit_misc.py
- [[.test_panic_vix()]] - code - tests/unit/test_unit_misc.py
- [[.test_recession_risk_inverted_curve()]] - code - tests/unit/test_unit_misc.py
- [[.test_stressed_liquidity_high_spreads()]] - code - tests/unit/test_unit_misc.py
- [[Apply deterministic rules to classify current market regime across all 4 dimensi]] - rationale - intelligence/regime_classifier.py
- [[Confidence based on how many macro series have current data.]] - rationale - intelligence/regime_classifier.py
- [[Deterministic market regime classification from macro data.]] - rationale - intelligence/regime_classifier.py
- [[Full classification pipeline fetch macro → classify → persist.]] - rationale - intelligence/regime_classifier.py
- [[MacroSnapshot]] - code - models/schemas.py
- [[Point-in-time macro data snapshot — no look-ahead bias.]] - rationale - models/schemas.py
- [[Returns a MacroSnapshot for a given datetime — no look-ahead bias.     Uses late]] - rationale - ingestion/macro_fetcher.py
- [[TestRegimeClassifier]] - code - tests/unit/test_unit_misc.py
- [[_classify_liquidity()]] - code - intelligence/regime_classifier.py
- [[_classify_macro()]] - code - intelligence/regime_classifier.py
- [[_classify_sentiment()]] - code - intelligence/regime_classifier.py
- [[_classify_volatility()]] - code - intelligence/regime_classifier.py
- [[_compute_confidence()]] - code - intelligence/regime_classifier.py
- [[classify_regime()]] - code - intelligence/regime_classifier.py
- [[get_macro_snapshot()]] - code - ingestion/macro_fetcher.py
- [[regime_classifier.py]] - code - intelligence/regime_classifier.py
- [[run_regime_classification()]] - code - intelligence/regime_classifier.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Macro_&_Regime_Analysis
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_API Routes & Contradiction Detection]]
- 1 edge to [[_COMMUNITY_External Data Fetching]]
- 1 edge to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 1 edge to [[_COMMUNITY_FastAPI Layer]]
- 1 edge to [[_COMMUNITY_Signal Scoring]]
- 1 edge to [[_COMMUNITY_Intelligence Generation]]
- 1 edge to [[_COMMUNITY_Article Normalization]]

## Top bridge nodes
- [[MacroSnapshot]] - degree 16, connects to 4 communities
- [[regime_classifier.py]] - degree 11, connects to 3 communities
- [[get_macro_snapshot()]] - degree 5, connects to 2 communities
- [[TestRegimeClassifier]] - degree 9, connects to 1 community