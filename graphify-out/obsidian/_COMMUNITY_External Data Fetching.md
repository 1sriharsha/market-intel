---
type: community
cohesion: 0.06
members: 58
---

# External Data Fetching

**Cohesion:** 0.06 - loosely connected
**Members:** 58 nodes

## Members
- [[AttributionMethod]] - code - models/enums.py
- [[Celery tasks wrapping all ingestion operations.]] - rationale - workers/ingestion_tasks.py
- [[Check feed health and update source_feeds table.]] - rationale - workers/ingestion_tasks.py
- [[Enumerations used across models and business logic.]] - rationale - models/enums.py
- [[EventCategory]] - code - models/enums.py
- [[FRED, BLS macro data fetcher — bootstraps full history, syncs daily.]] - rationale - ingestion/macro_fetcher.py
- [[FeedType]] - code - models/enums.py
- [[Fetch all RSS feeds, deduplicate, write novel articles to DB.]] - rationale - workers/ingestion_tasks.py
- [[Fetch company news from Finnhub for all watchlist tickers.     Rate limit 60 re]] - rationale - ingestion/api_fetcher.py
- [[Fetch complete history for all configured FRED series.     Writes to macro_data.]] - rationale - ingestion/macro_fetcher.py
- [[Fetch latest values for all configured series since last sync. Runs daily at 5 A]] - rationale - ingestion/macro_fetcher.py
- [[Fetch macro and sector news from Alpha Vantage.     Rate limit 25 reqday.]] - rationale - ingestion/api_fetcher.py
- [[Insert all configured RSS feeds into source_feeds table.]] - rationale - scripts/bootstrap.py
- [[LiquidityRegime]] - code - models/enums.py
- [[MacroRegime]] - code - models/enums.py
- [[Measure how novel an article is compared to recent similar articles.     Simple]] - rationale - intelligence/signal_scorer.py
- [[One-time historical data bootstrap. Resumable via bootstrap_state table. Run py]] - rationale - scripts/bootstrap.py
- [[Poll EDGAR RSS feed for recent filings from watchlist companies.     Maps EDGAR]] - rationale - ingestion/edgar_fetcher.py
- [[Query GDELT via Google BigQuery for structured historical events.     Requires G]] - rationale - ingestion/edgar_fetcher.py
- [[ReactionLabel]] - code - models/enums.py
- [[Run an async coroutine from a sync Celery task.]] - rationale - workers/ingestion_tasks.py
- [[SentimentRegime]] - code - models/enums.py
- [[SignificanceLevel]] - code - models/enums.py
- [[SourceTier]] - code - models/enums.py
- [[Synchronous FRED fetch — run in executor.]] - rationale - ingestion/macro_fetcher.py
- [[Trigger enrichment after ingestion — called internally.]] - rationale - workers/ingestion_tasks.py
- [[TriggerType]] - code - models/enums.py
- [[VolatilityRegime]] - code - models/enums.py
- [[_api_ingestion_async()]] - code - workers/ingestion_tasks.py
- [[_edgar_ingestion_async()]] - code - workers/ingestion_tasks.py
- [[_feed_health_async()]] - code - workers/ingestion_tasks.py
- [[_fetch_fred_series()]] - code - ingestion/macro_fetcher.py
- [[_fetch_fred_series_since()]] - code - ingestion/macro_fetcher.py
- [[_get_fred_client()]] - code - ingestion/macro_fetcher.py
- [[_insert_gdelt_events()]] - code - scripts/bootstrap.py
- [[_rss_ingestion_async()]] - code - workers/ingestion_tasks.py
- [[_run_async()]] - code - workers/ingestion_tasks.py
- [[bootstrap()]] - code - scripts/bootstrap.py
- [[bootstrap.py]] - code - scripts/bootstrap.py
- [[bootstrap_macro_series()]] - code - ingestion/macro_fetcher.py
- [[compute_novelty_score()]] - code - intelligence/signal_scorer.py
- [[enums.py]] - code - models/enums.py
- [[fetch_alpha_vantage_news()]] - code - ingestion/api_fetcher.py
- [[fetch_finnhub_news()]] - code - ingestion/api_fetcher.py
- [[fetch_gdelt_events()]] - code - ingestion/edgar_fetcher.py
- [[get_step_status()]] - code - scripts/bootstrap.py
- [[ingestion_tasks.py]] - code - workers/ingestion_tasks.py
- [[macro_fetcher.py]] - code - ingestion/macro_fetcher.py
- [[mark_step()]] - code - scripts/bootstrap.py
- [[poll_edgar_rss()]] - code - ingestion/edgar_fetcher.py
- [[run_api_ingestion()]] - code - workers/ingestion_tasks.py
- [[run_edgar_ingestion()]] - code - workers/ingestion_tasks.py
- [[run_enrichment_pipeline()]] - code - workers/ingestion_tasks.py
- [[run_feed_health_check()]] - code - workers/ingestion_tasks.py
- [[run_rss_ingestion()]] - code - workers/ingestion_tasks.py
- [[seed_source_feeds()]] - code - scripts/bootstrap.py
- [[str]] - code
- [[sync_macro_updates()]] - code - ingestion/macro_fetcher.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/External_Data_Fetching
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 7 edges to [[_COMMUNITY_Async DB & Celery Workers]]
- 5 edges to [[_COMMUNITY_Service Entry & Delivery]]
- 4 edges to [[_COMMUNITY_Deduplication Pipeline]]
- 4 edges to [[_COMMUNITY_Price Data & Abnormal Returns]]
- 3 edges to [[_COMMUNITY_Article Normalization]]
- 3 edges to [[_COMMUNITY_Intelligence Generation]]
- 2 edges to [[_COMMUNITY_Source Feed Configuration]]
- 2 edges to [[_COMMUNITY_Signal Scoring]]
- 2 edges to [[_COMMUNITY_Ticker Extraction (spaCy+Regex)]]
- 2 edges to [[_COMMUNITY_Embedding (OpenAI)]]
- 2 edges to [[_COMMUNITY_Feed Health Monitoring]]
- 1 edge to [[_COMMUNITY_FastAPI Layer]]
- 1 edge to [[_COMMUNITY_Macro & Regime Analysis]]
- 1 edge to [[_COMMUNITY_API Routes & Contradiction Detection]]

## Top bridge nodes
- [[str]] - degree 40, connects to 11 communities
- [[_rss_ingestion_async()]] - degree 8, connects to 4 communities
- [[macro_fetcher.py]] - degree 11, connects to 3 communities
- [[_api_ingestion_async()]] - degree 8, connects to 3 communities
- [[fetch_alpha_vantage_news()]] - degree 6, connects to 3 communities