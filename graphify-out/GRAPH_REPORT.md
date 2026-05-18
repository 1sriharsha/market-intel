# Graph Report - .  (2026-05-18)

## Corpus Check
- Corpus is ~20,619 words - fits in a single context window. You may not need a graph.

## Summary
- 587 nodes · 1035 edges · 32 communities detected
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 200 edges (avg confidence: 0.8)
- Token cost: 185,702 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Core Config & Ingestion Hub|Core Config & Ingestion Hub]]
- [[_COMMUNITY_External Data Fetching|External Data Fetching]]
- [[_COMMUNITY_API Routes & Contradiction Detection|API Routes & Contradiction Detection]]
- [[_COMMUNITY_Service Entry & Delivery|Service Entry & Delivery]]
- [[_COMMUNITY_Intelligence Generation|Intelligence Generation]]
- [[_COMMUNITY_FastAPI Layer|FastAPI Layer]]
- [[_COMMUNITY_Signal Scoring|Signal Scoring]]
- [[_COMMUNITY_Article Normalization|Article Normalization]]
- [[_COMMUNITY_Async DB & Celery Workers|Async DB & Celery Workers]]
- [[_COMMUNITY_Macro & Regime Analysis|Macro & Regime Analysis]]
- [[_COMMUNITY_Source Feed Configuration|Source Feed Configuration]]
- [[_COMMUNITY_Deduplication Pipeline|Deduplication Pipeline]]
- [[_COMMUNITY_DB Migrations|DB Migrations]]
- [[_COMMUNITY_Price Data & Abnormal Returns|Price Data & Abnormal Returns]]
- [[_COMMUNITY_ORM Schema Layer|ORM Schema Layer]]
- [[_COMMUNITY_Embedding (OpenAI)|Embedding (OpenAI)]]
- [[_COMMUNITY_Logging Infrastructure|Logging Infrastructure]]
- [[_COMMUNITY_Feed Health Monitoring|Feed Health Monitoring]]
- [[_COMMUNITY_Hallucination Guard Tests|Hallucination Guard Tests]]
- [[_COMMUNITY_Ticker Extraction (spaCy+Regex)|Ticker Extraction (spaCy+Regex)]]
- [[_COMMUNITY_Settings (BaseSettings)|Settings (BaseSettings)]]
- [[_COMMUNITY_Initial Schema Migration|Initial Schema Migration]]
- [[_COMMUNITY_Celery Beat Schedule|Celery Beat Schedule]]
- [[_COMMUNITY_Scheduler Entry Point|Scheduler Entry Point]]
- [[_COMMUNITY_Dev Entry Point|Dev Entry Point]]
- [[_COMMUNITY_Source Validation Script|Source Validation Script]]
- [[_COMMUNITY_DB Dependency Injection|DB Dependency Injection]]
- [[_COMMUNITY_Watchlist Config|Watchlist Config]]
- [[_COMMUNITY_Prometheus Metrics|Prometheus Metrics]]
- [[_COMMUNITY_Enumerations|Enumerations]]
- [[_COMMUNITY_Reaction Label Enum|Reaction Label Enum]]
- [[_COMMUNITY_Docker Test Profile|Docker Test Profile]]

## God Nodes (most connected - your core abstractions)
1. `Settings (config/settings.py)` - 34 edges
2. `Pydantic Schemas (schemas.py)` - 28 edges
3. `Logger (config/log.py)` - 25 edges
4. `normalize_article()` - 19 edges
5. `Intelligence Engine (intelligence/engine.py)` - 17 edges
6. `MacroSnapshot` - 16 edges
7. `Context Retriever (intelligence/retriever.py)` - 16 edges
8. `classify_regime()` - 15 edges
9. `Article Normalizer (ingestion/normalizer.py)` - 15 edges
10. `Ingestion Workers (workers/ingestion_tasks.py)` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Python Dependency Manifest` --references--> `FastAPI Application Entry Point`  [INFERRED]
  requirements.txt → api/main.py
- `Python Dependency Manifest` --references--> `Intelligence Engine (intelligence/engine.py)`  [INFERRED]
  requirements.txt → intelligence/engine.py
- `Python Dependency Manifest` --references--> `Celery App (workers/celery_app.py)`  [INFERRED]
  requirements.txt → workers/celery_app.py
- `Python Dependency Manifest` --references--> `Embedder (enrichment/embedder.py)`  [INFERRED]
  requirements.txt → enrichment/embedder.py
- `Health and Status Endpoints` --semantically_similar_to--> `Feed Health Checker`  [INFERRED] [semantically similar]
  api/routes/health.py → monitoring/health_checker.py

## Hyperedges (group relationships)
- **Ingestion Pipeline: Fetch → Normalize → Deduplicate → Store** — ingestion_rss_fetcher, ingestion_normalizer, ingestion_deduplicator, db_articles_table [EXTRACTED 0.95]
- **Intelligence Cycle: Retrieve Context → Call Claude → Validate → Deliver** — intelligence_retriever, intelligence_engine, intelligence_prompts, delivery_telegram_bot [EXTRACTED 0.95]
- **Context Assembly: Macro + Regime + Contradictions + Price → ContextPackage** — ingestion_macro_fetcher, intelligence_regime_classifier, intelligence_contradiction_detector, schema_contextpackage [INFERRED 0.85]
- **Six Critical Tests Enforcing System Invariants** — test_duplicate_not_written_twice, test_rate_limit_respected, test_intelligence_cites_source_ids, test_published_at_never_null, test_low_significance_skips_generation, test_no_hallucination_beyond_context [EXTRACTED 1.00]
- **ORM Models, Pydantic Schemas, and Migration form canonical schema layer** — models_db, models_schemas, migration_initial_schema [EXTRACTED 1.00]
- **Bootstrap Scripts: price, macro, GDELT seeded in sequence via BootstrapState** — scripts_bootstrap, orm_bootstrap_state, ingestion_price_fetcher [EXTRACTED 0.95]
- **Sequential Article Processing Pipeline (Ingestion -> Enrichment -> Intelligence)** — workers_ingestion_tasks, workers_enrichment_tasks, workers_intelligence_tasks [EXTRACTED 0.95]
- **FastAPI Routes Share DB Session via Dependency Injection** — api_dependencies, api_route_health, api_route_intelligence, api_route_sources, api_route_articles [EXTRACTED 1.00]
- **Observability Stack (Metrics + Prometheus + Grafana)** — monitoring_metrics, service_prometheus, service_grafana [INFERRED 0.85]

## Communities

### Community 0 - "Core Config & Ingestion Hub"
Cohesion: 0.07
Nodes (69): Logger (config/log.py), Settings (config/settings.py), Sources Config (config/sources.py), Watchlist Config (config/watchlist.py), Data Integrity Constraint: published_at non-null + append-only, article_ticker_effects DB Table, articles DB Table, embeddings DB Table (+61 more)

### Community 1 - "External Data Fetching"
Cohesion: 0.06
Nodes (54): fetch_alpha_vantage_news(), fetch_finnhub_news(), Fetch macro and sector news from Alpha Vantage.     Rate limit: 25 req/day., Fetch company news from Finnhub for all watchlist tickers.     Rate limit: 60 re, fetch_gdelt_events(), poll_edgar_rss(), Poll EDGAR RSS feed for recent filings from watchlist companies.     Maps EDGAR, Query GDELT via Google BigQuery for structured historical events.     Requires G (+46 more)

### Community 2 - "API Routes & Contradiction Detection"
Cohesion: 0.06
Nodes (38): BaseModel, detect_contradictions(), Price vs narrative contradiction detection., Identify contradictions between article sentiment and price behavior.      Check, get_latest_regime(), Fetch most recent regime snapshot from DB., build_context_package(), _get_historical_price_reaction() (+30 more)

### Community 3 - "Service Entry & Delivery"
Cohesion: 0.07
Nodes (39): lifespan(), FastAPI application entry point., deliver(), evaluate_delivery(), Returns True if an intelligence object should be pushed to Telegram.      Hard r, Evaluate, format, and push. Updates cooldowns and counters on success.     Retur, fetch_marketaux_news(), Fetch entity-tagged news from Marketaux.     Rate limit: 100 req/day via Redis d (+31 more)

### Community 4 - "Intelligence Generation"
Cohesion: 0.07
Nodes (32): format_message(), push_message(), Send a formatted message to the configured Telegram chat.     Retries 3x on netw, Format an IntelligenceObject as a Telegram message.     Max 3800 characters (Tel, _cluster_by_topic(), generate_intelligence(), _get_client(), _parse_claude_output() (+24 more)

### Community 5 - "FastAPI Layer"
Cohesion: 0.09
Nodes (27): FastAPI Dependencies (DB Session Provider), FastAPI Application Entry Point, Articles Endpoints, Health and Status Endpoints, Intelligence Endpoints, Sources Endpoints, Docker Compose (Production Services), Prometheus Scrape Configuration (+19 more)

### Community 6 - "Signal Scoring"
Cohesion: 0.08
Nodes (24): Wrapper for signal scorer — used by workers., score_significance_for_articles(), Event significance scoring 0–100., Compute a 0–100 significance score for a batch of articles.      Inputs:     - s, Map numeric score to significance level enum value., score_significance(), significance_level_from_score(), _tier_weight() (+16 more)

### Community 7 - "Article Normalization"
Cohesion: 0.1
Nodes (24): article_id(), canonical_url(), normalize_article(), parse_datetime(), Maps all raw ingestion sources to canonical RawArticle schema., Strip query params that don't affect content identity (tracking params etc)., SHA-256 of canonical URL — stable primary key., Parse any reasonable date string to a UTC-aware datetime. Returns fallback if un (+16 more)

### Community 8 - "Async DB & Celery Workers"
Cohesion: 0.13
Nodes (22): get_db(), get_session(), Async SQLAlchemy engine + session factory., _enrichment_async(), _macro_sync_async(), _price_sync_async(), Celery tasks wrapping enrichment operations., Embed + score significance + compute price reactions for new articles. (+14 more)

### Community 9 - "Macro & Regime Analysis"
Cohesion: 0.16
Nodes (16): get_macro_snapshot(), Returns a MacroSnapshot for a given datetime — no look-ahead bias.     Uses late, _classify_liquidity(), _classify_macro(), classify_regime(), _classify_sentiment(), _classify_volatility(), _compute_confidence() (+8 more)

### Community 10 - "Source Feed Configuration"
Cohesion: 0.15
Nodes (18): build_google_news_url(), All RSS feed URLs, API endpoints, and source trust tier assignments., Build a Google News RSS URL for a given search query., SourceFeed, Exception, _build_macro_google_news_feeds(), _build_ticker_google_news_feeds(), FeedFetchError (+10 more)

### Community 11 - "Deduplication Pipeline"
Cohesion: 0.16
Nodes (17): deduplicate_batch(), is_duplicate_content(), is_duplicate_url(), mark_url_seen(), Two-stage deduplication: URL hash (Redis) then semantic (pgvector)., Run full dedup pipeline on a batch.     URL check first (fast), content check se, O(1) Redis lookup — primary dedup gate., Semantic duplicate check via pgvector cosine similarity.     Only runs after URL (+9 more)

### Community 12 - "DB Migrations"
Cohesion: 0.19
Nodes (16): Initial DB Schema Migration (0001), Alembic environment configuration for async SQLAlchemy., run_async_migrations(), run_migrations_online(), ORM Models (db.py), ORM Model: Article, ORM Model: ArticleTickerEffect, ORM Model: BootstrapState (+8 more)

### Community 13 - "Price Data & Abnormal Returns"
Cohesion: 0.17
Nodes (15): compute_and_store_price_reactions(), For each ticker mentioned in an article, compute and persist:     - price at pub, bootstrap_price_history(), compute_abnormal_return(), _fetch_price_series(), _fetch_yfinance(), get_price_at(), _label_reaction() (+7 more)

### Community 14 - "ORM Schema Layer"
Cohesion: 0.23
Nodes (14): DeclarativeBase, Article, ArticleTickerEffect, Base, BootstrapState, Embedding, HistoricalEvent, IntelligenceObject (+6 more)

### Community 15 - "Embedding (OpenAI)"
Cohesion: 0.24
Nodes (11): _build_embed_input(), _content_hash(), embed_article(), embed_batch(), _embed_texts(), _get_client(), OpenAI text-embedding-3-small generation and storage., Batch embedding — minimizes OpenAI API round trips.     Max 2048 inputs per API (+3 more)

### Community 16 - "Logging Infrastructure"
Cohesion: 0.22
Nodes (3): get_logger(), Structlog compatibility shim — falls back to stdlib logging when structlog not i, _StdlibAdapter

### Community 17 - "Feed Health Monitoring"
Cohesion: 0.25
Nodes (8): check_feed_health(), _check_feeds(), detect_ingestion_stall(), get_embedding_backlog(), Feed health monitoring and ingestion lag detection., Check all active feeds for staleness.     A feed is unhealthy if last_fetched_at, Count articles awaiting embedding., Returns True if no articles have been ingested in the last threshold_minutes.

### Community 18 - "Hallucination Guard Tests"
Cohesion: 0.25
Nodes (7): CRITICAL TEST: test_no_hallucination_beyond_context Intelligence quality — Claud, Intelligence object with empty confidence_explanation must be rejected entirely., If Claude returns tickers not in context_package.tickers, they must be stripped., Tickers that ARE in context must not be stripped., test_all_valid_tickers_preserved(), test_empty_confidence_explanation_rejected(), test_hallucinated_tickers_stripped()

### Community 19 - "Ticker Extraction (spaCy+Regex)"
Cohesion: 0.32
Nodes (7): build_company_ticker_map(), extract_tickers(), _get_company_map(), _load_spacy(), spaCy + regex ticker extraction. Three-pass approach., Build and cache a map from company name variants to ticker symbols.     Sources:, Multi-pass ticker extraction:     1. Regex for explicit $TICKER and NYSE:TICKER

### Community 20 - "Settings (BaseSettings)"
Cohesion: 0.5
Nodes (3): BaseSettings, All environment variables, constants, and thresholds. Read from environment — ne, Settings

### Community 21 - "Initial Schema Migration"
Cohesion: 0.5
Nodes (1): Initial schema — all 9 canonical tables + pgvector + TimescaleDB extensions.

### Community 22 - "Celery Beat Schedule"
Cohesion: 0.5
Nodes (3): Celery application init + task registry + beat schedule., No-op — schedule is registered via app.conf above. Called by main.py to import w, register_beat_schedule()

### Community 23 - "Scheduler Entry Point"
Cohesion: 0.67
Nodes (1): APScheduler entry point — runs beat-schedule tasks when Celery beat is not used.

### Community 24 - "Dev Entry Point"
Cohesion: 0.67
Nodes (1): Dev entry point — starts API server + scheduler in a single process for local de

### Community 25 - "Source Validation Script"
Cohesion: 0.67
Nodes (1): Smoke test all configured feeds before deployment. Run: python scripts/validate_

### Community 26 - "DB Dependency Injection"
Cohesion: 0.67
Nodes (1): FastAPI dependencies — DB session, shared clients.

### Community 27 - "Watchlist Config"
Cohesion: 1.0
Nodes (1): Tickers and macro topics being monitored. Add tickers here + run bootstrap.

### Community 28 - "Prometheus Metrics"
Cohesion: 1.0
Nodes (1): Prometheus metric definitions for all MIOS subsystems.

### Community 43 - "Enumerations"
Cohesion: 1.0
Nodes (1): Enumerations (enums.py)

### Community 44 - "Reaction Label Enum"
Cohesion: 1.0
Nodes (1): Enum: ReactionLabel

### Community 45 - "Docker Test Profile"
Cohesion: 1.0
Nodes (1): Docker Compose (Test Profile)

## Knowledge Gaps
- **171 isolated node(s):** `APScheduler entry point — runs beat-schedule tasks when Celery beat is not used.`, `Dev entry point — starts API server + scheduler in a single process for local de`, `Two-stage deduplication: URL hash (Redis) then semantic (pgvector).`, `O(1) Redis lookup — primary dedup gate.`, `Semantic duplicate check via pgvector cosine similarity.     Only runs after URL` (+166 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Initial Schema Migration`** (4 nodes): `0001_initial_schema.py`, `downgrade()`, `Initial schema — all 9 canonical tables + pgvector + TimescaleDB extensions.`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scheduler Entry Point`** (3 nodes): `main()`, `APScheduler entry point — runs beat-schedule tasks when Celery beat is not used.`, `scheduler.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Dev Entry Point`** (3 nodes): `main.py`, `main()`, `Dev entry point — starts API server + scheduler in a single process for local de`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Source Validation Script`** (3 nodes): `validate_sources.py`, `Smoke test all configured feeds before deployment. Run: python scripts/validate_`, `validate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `DB Dependency Injection`** (3 nodes): `get_db()`, `dependencies.py`, `FastAPI dependencies — DB session, shared clients.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Watchlist Config`** (2 nodes): `watchlist.py`, `Tickers and macro topics being monitored. Add tickers here + run bootstrap.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Prometheus Metrics`** (2 nodes): `metrics.py`, `Prometheus metric definitions for all MIOS subsystems.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Enumerations`** (1 nodes): `Enumerations (enums.py)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Reaction Label Enum`** (1 nodes): `Enum: ReactionLabel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Docker Test Profile`** (1 nodes): `Docker Compose (Test Profile)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings (config/settings.py)` connect `Core Config & Ingestion Hub` to `External Data Fetching`, `API Routes & Contradiction Detection`, `Service Entry & Delivery`, `Intelligence Generation`, `Signal Scoring`, `Async DB & Celery Workers`, `Source Feed Configuration`, `Deduplication Pipeline`, `DB Migrations`, `Price Data & Abnormal Returns`, `Embedding (OpenAI)`, `Celery Beat Schedule`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._
- **Why does `Pydantic Schemas (schemas.py)` connect `FastAPI Layer` to `Core Config & Ingestion Hub`, `External Data Fetching`, `API Routes & Contradiction Detection`, `Intelligence Generation`, `Article Normalization`, `Macro & Regime Analysis`, `Source Feed Configuration`, `Deduplication Pipeline`, `Price Data & Abnormal Returns`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._
- **Why does `Logger (config/log.py)` connect `Core Config & Ingestion Hub` to `External Data Fetching`, `API Routes & Contradiction Detection`, `Intelligence Generation`, `Async DB & Celery Workers`, `Macro & Regime Analysis`, `Source Feed Configuration`, `Deduplication Pipeline`, `Price Data & Abnormal Returns`, `Embedding (OpenAI)`, `Feed Health Monitoring`, `Ticker Extraction (spaCy+Regex)`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `str` (e.g. with `is_duplicate_content()` and `bootstrap_macro_series()`) actually correct?**
  _`str` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `normalize_article()` (e.g. with `normalize_rss_item()` and `poll_edgar_rss()`) actually correct?**
  _`normalize_article()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `APScheduler entry point — runs beat-schedule tasks when Celery beat is not used.`, `Dev entry point — starts API server + scheduler in a single process for local de`, `Two-stage deduplication: URL hash (Redis) then semantic (pgvector).` to the rest of the system?**
  _171 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Core Config & Ingestion Hub` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._