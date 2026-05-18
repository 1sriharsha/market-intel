---
source_file: "workers/ingestion_tasks.py"
type: "code"
community: "External Data Fetching"
location: "L1"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/External_Data_Fetching
---

# ingestion_tasks.py

## Connections
- [[Celery App (workerscelery_app.py)]] - `imports_from` [EXTRACTED]
- [[Celery tasks wrapping all ingestion operations.]] - `rationale_for` [EXTRACTED]
- [[Logger (configlog.py)]] - `imports_from` [EXTRACTED]
- [[_api_ingestion_async()]] - `contains` [EXTRACTED]
- [[_edgar_ingestion_async()]] - `contains` [EXTRACTED]
- [[_feed_health_async()]] - `contains` [EXTRACTED]
- [[_rss_ingestion_async()]] - `contains` [EXTRACTED]
- [[_run_async()]] - `contains` [EXTRACTED]
- [[run_api_ingestion()]] - `contains` [EXTRACTED]
- [[run_edgar_ingestion()]] - `contains` [EXTRACTED]
- [[run_enrichment_pipeline()]] - `contains` [EXTRACTED]
- [[run_feed_health_check()]] - `contains` [EXTRACTED]
- [[run_rss_ingestion()]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/External_Data_Fetching