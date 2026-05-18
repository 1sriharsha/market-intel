---
type: community
cohesion: 0.06
members: 50
---

# API Routes & Contradiction Detection

**Cohesion:** 0.06 - loosely connected
**Members:** 50 nodes

## Members
- [[.test_bullish_headline_negative_price()]] - code - tests/unit/test_unit_misc.py
- [[.test_no_contradictions_consistent()]] - code - tests/unit/test_unit_misc.py
- [[AbnormalReturn]] - code - models/schemas.py
- [[ArticleRead]] - code - models/schemas.py
- [[Assemble the full context package for intelligence generation.     All data veri]] - rationale - intelligence/retriever.py
- [[BaseModel]] - code
- [[Canonical article representation produced by all normalizers.]] - rationale - models/schemas.py
- [[ContextPackage]] - code - models/schemas.py
- [[Contradiction]] - code - models/schemas.py
- [[Embed query text, search pgvector for semantically similar articles.     Score =]] - rationale - intelligence/retriever.py
- [[Fetch most recent regime snapshot from DB.]] - rationale - intelligence/regime_classifier.py
- [[Find similar past events from historical_events table.     Matches on event cat]] - rationale - intelligence/retriever.py
- [[Health and status endpoints.]] - rationale - api/routes/health.py
- [[HealthResponse]] - code - models/schemas.py
- [[HistoricalAnalogue]] - code - models/schemas.py
- [[Identify contradictions between article sentiment and price behavior.      Check]] - rationale - intelligence/contradiction_detector.py
- [[Ingestion lag, feed health, embedding backlog, last intelligence run.]] - rationale - api/routes/health.py
- [[Intelligence object with empty articles in context must not be generated.]] - rationale - tests/unit/test_intelligence_cites_source_ids.py
- [[IntelligenceObjectCreate]] - code - models/schemas.py
- [[IntelligenceObjectRead]] - code - models/schemas.py
- [[Price vs narrative contradiction detection.]] - rationale - intelligence/contradiction_detector.py
- [[PricePoint]] - code - models/schemas.py
- [[Pydantic schemas for API responses and internal data transfer objects.]] - rationale - models/schemas.py
- [[RawArticle]] - code - models/schemas.py
- [[SourceFeedRead]] - code - models/schemas.py
- [[SystemStatus]] - code - models/schemas.py
- [[Test fixtures mock DB, Redis, Claude stub, fixed IntelligenceObject. All unit t]] - rationale - tests/conftest.py
- [[TestContradictionDetector]] - code - tests/unit/test_unit_misc.py
- [[Unit tests for regime classifier, signal scorer, contradiction detector, Telegra]] - rationale - tests/unit/test_unit_misc.py
- [[_get_historical_price_reaction()]] - code - intelligence/retriever.py
- [[anyio_backend()]] - code - tests/conftest.py
- [[build_context_package()]] - code - intelligence/retriever.py
- [[conftest.py]] - code - tests/conftest.py
- [[contradiction_detector.py]] - code - intelligence/contradiction_detector.py
- [[detect_contradictions()]] - code - intelligence/contradiction_detector.py
- [[fixed_context()]] - code - tests/conftest.py
- [[get_latest_regime()]] - code - intelligence/regime_classifier.py
- [[health()]] - code - api/routes/health.py
- [[health.py]] - code - api/routes/health.py
- [[mock_anthropic()]] - code - tests/conftest.py
- [[mock_redis()]] - code - tests/conftest.py
- [[mock_session()]] - code - tests/conftest.py
- [[pgvector semantic search + context package assembly.]] - rationale - intelligence/retriever.py
- [[retrieve_historical_analogues()]] - code - intelligence/retriever.py
- [[retrieve_similar_articles()]] - code - intelligence/retriever.py
- [[retriever.py]] - code - intelligence/retriever.py
- [[schemas.py]] - code - models/schemas.py
- [[status()]] - code - api/routes/health.py
- [[test_intelligence_object_never_orphaned()]] - code - tests/unit/test_intelligence_cites_source_ids.py
- [[test_unit_misc.py]] - code - tests/unit/test_unit_misc.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/API_Routes_&_Contradiction_Detection
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Macro & Regime Analysis]]
- 6 edges to [[_COMMUNITY_FastAPI Layer]]
- 4 edges to [[_COMMUNITY_Intelligence Generation]]
- 3 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 2 edges to [[_COMMUNITY_Source Feed Configuration]]
- 2 edges to [[_COMMUNITY_Price Data & Abnormal Returns]]
- 2 edges to [[_COMMUNITY_Article Normalization]]
- 2 edges to [[_COMMUNITY_Service Entry & Delivery]]
- 1 edge to [[_COMMUNITY_Embedding (OpenAI)]]
- 1 edge to [[_COMMUNITY_External Data Fetching]]
- 1 edge to [[_COMMUNITY_Deduplication Pipeline]]
- 1 edge to [[_COMMUNITY_Signal Scoring]]

## Top bridge nodes
- [[test_unit_misc.py]] - degree 8, connects to 6 communities
- [[build_context_package()]] - degree 10, connects to 3 communities
- [[RawArticle]] - degree 7, connects to 3 communities
- [[retriever.py]] - degree 8, connects to 2 communities
- [[retrieve_similar_articles()]] - degree 4, connects to 2 communities