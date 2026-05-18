---
source_file: "ingestion/deduplicator.py"
type: "rationale"
community: "Deduplication Pipeline"
location: "L41"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Deduplication_Pipeline
---

# Semantic duplicate check via pgvector cosine similarity.     Only runs after URL

## Connections
- [[is_duplicate_content()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Deduplication_Pipeline