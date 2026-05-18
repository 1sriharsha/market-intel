---
type: community
cohesion: 0.07
members: 73
---

# Core Config & Ingestion Hub

**Cohesion:** 0.07 - loosely connected
**Members:** 73 nodes

## Members
- [[API Fetcher (ingestionapi_fetcher.py)]] - code - ingestion/api_fetcher.py
- [[APScheduler Entry Point (scheduler.py)]] - code - scheduler.py
- [[AbnormalReturn Schema]] - code - models/schemas.py
- [[Article Normalizer (ingestionnormalizer.py)]] - code - ingestion/normalizer.py
- [[Async SQLAlchemy Engine + Session Factory]] - code - storage/database.py
- [[Backfill Embeddings Script]] - code - scripts/backfill_embeddings.py
- [[Celery App (workerscelery_app.py)]] - code - workers/celery_app.py
- [[Compute and persist price reactions for ingested articles.]] - rationale - enrichment/price_reactor.py
- [[Context Retriever (intelligenceretriever.py)]] - code - intelligence/retriever.py
- [[ContextPackage Schema]] - code - models/schemas.py
- [[Contradiction Detector (intelligencecontradiction_detector.py)]] - code - intelligence/contradiction_detector.py
- [[Data Integrity Constraint published_at non-null + append-only]] - rationale - ingestion/normalizer.py
- [[Deduplicator (ingestiondeduplicator.py)]] - code - ingestion/deduplicator.py
- [[Dev Entry Point (main.py)]] - code - main.py
- [[EDGAR Fetcher (ingestionedgar_fetcher.py)]] - code - ingestion/edgar_fetcher.py
- [[Embedder (enrichmentembedder.py)]] - code - enrichment/embedder.py
- [[Enrichment Workers (workersenrichment_tasks.py)]] - code - workers/enrichment_tasks.py
- [[Enum SignificanceLevel]] - code - models/enums.py
- [[Enum SourceTier]] - code - models/enums.py
- [[Enum VolatilityRegime]] - code - models/enums.py
- [[Hard Delivery Rules (5-cap, 4h cooldown, significance filter)]] - rationale - delivery/telegram_bot.py
- [[Historical Data Bootstrap Script]] - code - scripts/bootstrap.py
- [[HistoricalAnalogue Schema]] - code - models/schemas.py
- [[Ingestion Workers (workersingestion_tasks.py)]] - code - workers/ingestion_tasks.py
- [[Intelligence Engine (intelligenceengine.py)]] - code - intelligence/engine.py
- [[Intelligence Workers (workersintelligence_tasks.py)]] - code - workers/intelligence_tasks.py
- [[IntelligenceObjectCreate Schema]] - code - models/schemas.py
- [[Logger (configlog.py)]] - code - config/log.py
- [[Macro Fetcher (ingestionmacro_fetcher.py)]] - code - ingestion/macro_fetcher.py
- [[MacroSnapshot Schema]] - code - models/schemas.py
- [[Post-Generation Hallucination Guard]] - rationale - intelligence/engine.py
- [[Price Fetcher (ingestionprice_fetcher.py)]] - code - ingestion/price_fetcher.py
- [[Price Reactor (Abnormal Return Computation)]] - code - enrichment/price_reactor.py
- [[PricePoint Schema]] - code - models/schemas.py
- [[Pydantic Schema RawArticle]] - code - models/schemas.py
- [[Python Dependency Manifest]] - document - requirements.txt
- [[RSS Fetcher (ingestionrss_fetcher.py)]] - code - ingestion/rss_fetcher.py
- [[RawArticle Schema]] - code - models/schemas.py
- [[Redis Client (storageredis_client.py)]] - code - storage/redis_client.py
- [[Regime Classifier (intelligenceregime_classifier.py)]] - code - intelligence/regime_classifier.py
- [[SEC EDGAR RSS + GDELT BigQuery historical event fetcher.]] - rationale - ingestion/edgar_fetcher.py
- [[Settings (configsettings.py)]] - code - config/settings.py
- [[Signal Scorer (intelligencesignal_scorer.py)]] - code - intelligence/signal_scorer.py
- [[Significance Threshold Gate (default 65.0)]] - rationale - intelligence/engine.py
- [[Source Feed Validation Script]] - code - scripts/validate_sources.py
- [[SourceFeed Dataclass]] - code - config/sources.py
- [[Sources Config (configsources.py)]] - code - config/sources.py
- [[Structured API sources Finnhub, Marketaux, Alpha Vantage with rate limiting.]] - rationale - ingestion/api_fetcher.py
- [[Telegram Bot (deliverytelegram_bot.py)]] - code - delivery/telegram_bot.py
- [[Telegram delivery — evaluate, format, push. Hard delivery rules enforced in code]] - rationale - delivery/telegram_bot.py
- [[Test Fixtures (testsconftest.py)]] - code - tests/conftest.py
- [[Test Duplicate Not Written Twice]] - code - tests/unit/test_duplicate_not_written_twice.py
- [[Test Intelligence Cites Source IDs]] - code - tests/unit/test_intelligence_cites_source_ids.py
- [[Test Low Significance Skips Generation]] - code - tests/unit/test_low_significance_skips_generation.py
- [[Test No Hallucination Beyond Context]] - code - tests/unit/test_no_hallucination_beyond_context.py
- [[Test Published At Never Null]] - code - tests/unit/test_published_at_never_null.py
- [[Test Rate Limit Respected]] - code - tests/unit/test_rate_limit_respected.py
- [[Test Unit Misc (Regime, Scorer, Contradictions, Formatter)]] - code - tests/unit/test_unit_misc.py
- [[Ticker Extractor (spaCy + Regex)]] - code - enrichment/ticker_extractor.py
- [[Two-Stage Deduplication Pipeline]] - rationale - ingestion/deduplicator.py
- [[Watchlist Config (configwatchlist.py)]] - code - config/watchlist.py
- [[api_fetcher.py]] - code - ingestion/api_fetcher.py
- [[article_ticker_effects DB Table]] - code - models/db.py
- [[articles DB Table]] - code - models/db.py
- [[edgar_fetcher.py]] - code - ingestion/edgar_fetcher.py
- [[embeddings DB Table]] - code - models/db.py
- [[historical_events DB Table]] - code - models/db.py
- [[intelligence_objects DB Table]] - code - models/db.py
- [[macro_data DB Table]] - code - models/db.py
- [[price_reactor.py]] - code - enrichment/price_reactor.py
- [[prices DB Table]] - code - models/db.py
- [[regime_snapshots DB Table]] - code - models/db.py
- [[telegram_bot.py]] - code - delivery/telegram_bot.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Core_Config_&_Ingestion_Hub
SORT file.name ASC
```

## Connections to other communities
- 16 edges to [[_COMMUNITY_FastAPI Layer]]
- 9 edges to [[_COMMUNITY_External Data Fetching]]
- 7 edges to [[_COMMUNITY_Intelligence Generation]]
- 6 edges to [[_COMMUNITY_DB Migrations]]
- 5 edges to [[_COMMUNITY_Deduplication Pipeline]]
- 5 edges to [[_COMMUNITY_Source Feed Configuration]]
- 5 edges to [[_COMMUNITY_Service Entry & Delivery]]
- 5 edges to [[_COMMUNITY_Async DB & Celery Workers]]
- 3 edges to [[_COMMUNITY_Price Data & Abnormal Returns]]
- 3 edges to [[_COMMUNITY_Signal Scoring]]
- 3 edges to [[_COMMUNITY_API Routes & Contradiction Detection]]
- 2 edges to [[_COMMUNITY_Ticker Extraction (spaCy+Regex)]]
- 2 edges to [[_COMMUNITY_Embedding (OpenAI)]]
- 1 edge to [[_COMMUNITY_Macro & Regime Analysis]]
- 1 edge to [[_COMMUNITY_Article Normalization]]
- 1 edge to [[_COMMUNITY_Hallucination Guard Tests]]
- 1 edge to [[_COMMUNITY_DB Dependency Injection]]
- 1 edge to [[_COMMUNITY_Celery Beat Schedule]]
- 1 edge to [[_COMMUNITY_Feed Health Monitoring]]

## Top bridge nodes
- [[Settings (configsettings.py)]] - degree 34, connects to 12 communities
- [[Logger (configlog.py)]] - degree 25, connects to 11 communities
- [[Test Fixtures (testsconftest.py)]] - degree 13, connects to 5 communities
- [[Article Normalizer (ingestionnormalizer.py)]] - degree 15, connects to 3 communities
- [[api_fetcher.py]] - degree 10, connects to 3 communities