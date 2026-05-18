---
type: community
cohesion: 0.25
members: 8
---

# Hallucination Guard Tests

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[CRITICAL TEST test_no_hallucination_beyond_context Intelligence quality — Claud]] - rationale - tests/unit/test_no_hallucination_beyond_context.py
- [[If Claude returns tickers not in context_package.tickers, they must be stripped.]] - rationale - tests/unit/test_no_hallucination_beyond_context.py
- [[Intelligence object with empty confidence_explanation must be rejected entirely.]] - rationale - tests/unit/test_no_hallucination_beyond_context.py
- [[Tickers that ARE in context must not be stripped.]] - rationale - tests/unit/test_no_hallucination_beyond_context.py
- [[test_all_valid_tickers_preserved()]] - code - tests/unit/test_no_hallucination_beyond_context.py
- [[test_empty_confidence_explanation_rejected()]] - code - tests/unit/test_no_hallucination_beyond_context.py
- [[test_hallucinated_tickers_stripped()]] - code - tests/unit/test_no_hallucination_beyond_context.py
- [[test_no_hallucination_beyond_context.py]] - code - tests/unit/test_no_hallucination_beyond_context.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Hallucination_Guard_Tests
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Core Config & Ingestion Hub]]

## Top bridge nodes
- [[test_no_hallucination_beyond_context.py]] - degree 5, connects to 1 community