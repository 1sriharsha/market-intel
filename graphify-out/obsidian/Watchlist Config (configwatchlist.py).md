---
source_file: "config/watchlist.py"
type: "code"
community: "Core Config & Ingestion Hub"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Core_Config_&_Ingestion_Hub
---

# Watchlist Config (config/watchlist.py)

## Connections
- [[API Fetcher (ingestionapi_fetcher.py)]] - `references` [EXTRACTED]
- [[EDGAR Fetcher (ingestionedgar_fetcher.py)]] - `references` [EXTRACTED]
- [[Enrichment Workers (workersenrichment_tasks.py)]] - `calls` [EXTRACTED]
- [[Ingestion Workers (workersingestion_tasks.py)]] - `calls` [EXTRACTED]
- [[RSS Fetcher (ingestionrss_fetcher.py)]] - `references` [EXTRACTED]
- [[Sources Config (configsources.py)]] - `shares_data_with` [INFERRED]
- [[Ticker Extractor (spaCy + Regex)]] - `calls` [EXTRACTED]
- [[api_fetcher.py]] - `imports_from` [EXTRACTED]
- [[edgar_fetcher.py]] - `imports_from` [EXTRACTED]
- [[rss_fetcher.py]] - `imports_from` [EXTRACTED]
- [[ticker_extractor.py]] - `imports_from` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Core_Config_&_Ingestion_Hub