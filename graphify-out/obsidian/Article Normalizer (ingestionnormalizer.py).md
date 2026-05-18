---
source_file: "ingestion/normalizer.py"
type: "code"
community: "Core Config & Ingestion Hub"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Core_Config_&_Ingestion_Hub
---

# Article Normalizer (ingestion/normalizer.py)

## Connections
- [[API Fetcher (ingestionapi_fetcher.py)]] - `calls` [EXTRACTED]
- [[Data Integrity Constraint published_at non-null + append-only]] - `references` [INFERRED]
- [[Deduplicator (ingestiondeduplicator.py)]] - `conceptually_related_to` [INFERRED]
- [[EDGAR Fetcher (ingestionedgar_fetcher.py)]] - `calls` [EXTRACTED]
- [[Ingestion Workers (workersingestion_tasks.py)]] - `calls` [EXTRACTED]
- [[RSS Fetcher (ingestionrss_fetcher.py)]] - `calls` [EXTRACTED]
- [[RawArticle Schema]] - `references` [EXTRACTED]
- [[Test Duplicate Not Written Twice]] - `references` [EXTRACTED]
- [[Test Published At Never Null]] - `references` [EXTRACTED]
- [[Test Unit Misc (Regime, Scorer, Contradictions, Formatter)]] - `references` [EXTRACTED]
- [[api_fetcher.py]] - `imports_from` [EXTRACTED]
- [[edgar_fetcher.py]] - `imports_from` [EXTRACTED]
- [[rss_fetcher.py]] - `imports_from` [EXTRACTED]
- [[test_duplicate_not_written_twice.py]] - `imports_from` [EXTRACTED]
- [[test_published_at_never_null.py]] - `imports_from` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Core_Config_&_Ingestion_Hub