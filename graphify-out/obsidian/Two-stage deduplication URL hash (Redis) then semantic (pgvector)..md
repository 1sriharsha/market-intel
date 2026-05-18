---
source_file: "ingestion/deduplicator.py"
type: "rationale"
community: "Deduplication Pipeline"
location: "L1"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Deduplication_Pipeline
---

# Two-stage deduplication: URL hash (Redis) then semantic (pgvector).

## Connections
- [[deduplicator.py]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Deduplication_Pipeline