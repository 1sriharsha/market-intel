---
type: community
cohesion: 0.13
members: 25
---

# Async DB & Celery Workers

**Cohesion:** 0.13 - loosely connected
**Members:** 25 nodes

## Members
- [[Async SQLAlchemy engine + session factory.]] - rationale - storage/database.py
- [[Celery tasks wrapping enrichment operations.]] - rationale - workers/enrichment_tasks.py
- [[Celery tasks wrapping intelligence operations.]] - rationale - workers/intelligence_tasks.py
- [[Daily macro data sync from FRED.]] - rationale - workers/enrichment_tasks.py
- [[Embed + score significance + compute price reactions for new articles.]] - rationale - workers/enrichment_tasks.py
- [[Manually triggered intelligence cycle — called from API.]] - rationale - workers/intelligence_tasks.py
- [[Nightly price sync for all watchlist tickers.]] - rationale - workers/enrichment_tasks.py
- [[_enrichment_async()]] - code - workers/enrichment_tasks.py
- [[_intelligence_cycle_async()]] - code - workers/intelligence_tasks.py
- [[_macro_sync_async()]] - code - workers/enrichment_tasks.py
- [[_price_sync_async()]] - code - workers/enrichment_tasks.py
- [[_regime_async()]] - code - workers/intelligence_tasks.py
- [[_run_async()_1]] - code - workers/enrichment_tasks.py
- [[_run_async()_2]] - code - workers/intelligence_tasks.py
- [[database.py]] - code - storage/database.py
- [[enrichment_tasks.py]] - code - workers/enrichment_tasks.py
- [[get_db()]] - code - storage/database.py
- [[get_session()]] - code - storage/database.py
- [[intelligence_tasks.py]] - code - workers/intelligence_tasks.py
- [[run_article_enrichment()]] - code - workers/enrichment_tasks.py
- [[run_intelligence_cycle()_1]] - code - workers/intelligence_tasks.py
- [[run_macro_sync()]] - code - workers/enrichment_tasks.py
- [[run_price_sync()]] - code - workers/enrichment_tasks.py
- [[run_regime_classification()_1]] - code - workers/intelligence_tasks.py
- [[trigger_intelligence_manual()]] - code - workers/intelligence_tasks.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Async_DB_&_Celery_Workers
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_External Data Fetching]]
- 5 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 2 edges to [[_COMMUNITY_Price Data & Abnormal Returns]]
- 2 edges to [[_COMMUNITY_Embedding (OpenAI)]]
- 1 edge to [[_COMMUNITY_Signal Scoring]]
- 1 edge to [[_COMMUNITY_Feed Health Monitoring]]

## Top bridge nodes
- [[get_session()]] - degree 13, connects to 3 communities
- [[_enrichment_async()]] - degree 6, connects to 3 communities
- [[enrichment_tasks.py]] - degree 10, connects to 1 community
- [[intelligence_tasks.py]] - degree 9, connects to 1 community
- [[run_article_enrichment()]] - degree 5, connects to 1 community