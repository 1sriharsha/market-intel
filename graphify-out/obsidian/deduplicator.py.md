---
source_file: "ingestion/deduplicator.py"
type: "code"
community: "Deduplication Pipeline"
location: "L1"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Deduplication_Pipeline
---

# deduplicator.py

## Connections
- [[Logger (configlog.py)]] - `imports_from` [EXTRACTED]
- [[Pydantic Schemas (schemas.py)]] - `imports_from` [EXTRACTED]
- [[Redis Client (storageredis_client.py)]] - `imports_from` [EXTRACTED]
- [[Settings (configsettings.py)]] - `imports_from` [EXTRACTED]
- [[Two-stage deduplication URL hash (Redis) then semantic (pgvector).]] - `rationale_for` [EXTRACTED]
- [[_url_hash()]] - `contains` [EXTRACTED]
- [[deduplicate_batch()]] - `contains` [EXTRACTED]
- [[is_duplicate_content()]] - `contains` [EXTRACTED]
- [[is_duplicate_url()]] - `contains` [EXTRACTED]
- [[mark_url_seen()]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Deduplication_Pipeline