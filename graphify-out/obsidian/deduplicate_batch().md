---
source_file: "ingestion/deduplicator.py"
type: "code"
community: "Deduplication Pipeline"
location: "L103"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Deduplication_Pipeline
---

# deduplicate_batch()

## Connections
- [[Run full dedup pipeline on a batch.     URL check first (fast), content check se]] - `rationale_for` [EXTRACTED]
- [[_api_ingestion_async()]] - `calls` [INFERRED]
- [[_edgar_ingestion_async()]] - `calls` [INFERRED]
- [[_rss_ingestion_async()]] - `calls` [INFERRED]
- [[deduplicator.py]] - `contains` [EXTRACTED]
- [[is_duplicate_content()]] - `calls` [EXTRACTED]
- [[is_duplicate_url()]] - `calls` [EXTRACTED]
- [[mark_url_seen()]] - `calls` [EXTRACTED]
- [[test_duplicate_not_written_twice_semantic_dedup()]] - `calls` [INFERRED]
- [[test_duplicate_not_written_twice_url_dedup()]] - `calls` [INFERRED]
- [[test_unique_articles_all_pass_dedup()]] - `calls` [INFERRED]

#graphify/code #graphify/INFERRED #community/Deduplication_Pipeline