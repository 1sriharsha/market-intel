---
source_file: "workers/enrichment_tasks.py"
type: "code"
community: "Core Config & Ingestion Hub"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Core_Config_&_Ingestion_Hub
---

# Enrichment Workers (workers/enrichment_tasks.py)

## Connections
- [[APScheduler Entry Point (scheduler.py)]] - `calls` [EXTRACTED]
- [[Async SQLAlchemy Engine + Session Factory]] - `calls` [EXTRACTED]
- [[Celery App (workerscelery_app.py)]] - `references` [EXTRACTED]
- [[Embedder (enrichmentembedder.py)]] - `calls` [EXTRACTED]
- [[Ingestion Workers (workersingestion_tasks.py)]] - `calls` [EXTRACTED]
- [[Macro Fetcher (ingestionmacro_fetcher.py)]] - `calls` [EXTRACTED]
- [[Price Fetcher (ingestionprice_fetcher.py)]] - `calls` [EXTRACTED]
- [[Price Reactor (Abnormal Return Computation)]] - `calls` [EXTRACTED]
- [[Signal Scorer (intelligencesignal_scorer.py)]] - `calls` [EXTRACTED]
- [[Watchlist Config (configwatchlist.py)]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Core_Config_&_Ingestion_Hub