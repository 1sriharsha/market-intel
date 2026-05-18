---
source_file: "workers/ingestion_tasks.py"
type: "code"
community: "Core Config & Ingestion Hub"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Core_Config_&_Ingestion_Hub
---

# Ingestion Workers (workers/ingestion_tasks.py)

## Connections
- [[API Fetcher (ingestionapi_fetcher.py)]] - `calls` [EXTRACTED]
- [[APScheduler Entry Point (scheduler.py)]] - `calls` [EXTRACTED]
- [[Article Normalizer (ingestionnormalizer.py)]] - `calls` [EXTRACTED]
- [[Async SQLAlchemy Engine + Session Factory]] - `calls` [EXTRACTED]
- [[Celery App (workerscelery_app.py)]] - `references` [EXTRACTED]
- [[Deduplicator (ingestiondeduplicator.py)]] - `calls` [EXTRACTED]
- [[EDGAR Fetcher (ingestionedgar_fetcher.py)]] - `calls` [EXTRACTED]
- [[Enrichment Workers (workersenrichment_tasks.py)]] - `calls` [EXTRACTED]
- [[Feed Health Checker]] - `calls` [EXTRACTED]
- [[Intelligence Workers (workersintelligence_tasks.py)]] - `conceptually_related_to` [INFERRED]
- [[RSS Fetcher (ingestionrss_fetcher.py)]] - `calls` [EXTRACTED]
- [[Signal Scorer (intelligencesignal_scorer.py)]] - `calls` [EXTRACTED]
- [[Ticker Extractor (spaCy + Regex)]] - `calls` [EXTRACTED]
- [[Watchlist Config (configwatchlist.py)]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Core_Config_&_Ingestion_Hub