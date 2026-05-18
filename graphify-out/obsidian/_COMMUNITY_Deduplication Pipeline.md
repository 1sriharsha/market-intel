---
type: community
cohesion: 0.16
members: 19
---

# Deduplication Pipeline

**Cohesion:** 0.16 - loosely connected
**Members:** 19 nodes

## Members
- [[CRITICAL TEST test_duplicate_not_written_twice Data integrity — the two-stage d]] - rationale - tests/unit/test_duplicate_not_written_twice.py
- [[O(1) Redis lookup — primary dedup gate.]] - rationale - ingestion/deduplicator.py
- [[Run full dedup pipeline on a batch.     URL check first (fast), content check se]] - rationale - ingestion/deduplicator.py
- [[Semantic duplicate check via pgvector cosine similarity.     Only runs after URL]] - rationale - ingestion/deduplicator.py
- [[Stage 1 Same URL submitted twice — second must be suppressed.]] - rationale - tests/unit/test_duplicate_not_written_twice.py
- [[Stage 2 Two articles with different URLs but same semantic content must dedupli]] - rationale - tests/unit/test_duplicate_not_written_twice.py
- [[Three completely different articles must all pass.]] - rationale - tests/unit/test_duplicate_not_written_twice.py
- [[Two-stage deduplication URL hash (Redis) then semantic (pgvector).]] - rationale - ingestion/deduplicator.py
- [[_url_hash()]] - code - ingestion/deduplicator.py
- [[deduplicate_batch()]] - code - ingestion/deduplicator.py
- [[deduplicator.py]] - code - ingestion/deduplicator.py
- [[is_duplicate_content()]] - code - ingestion/deduplicator.py
- [[is_duplicate_url()]] - code - ingestion/deduplicator.py
- [[make_article()]] - code - tests/unit/test_duplicate_not_written_twice.py
- [[mark_url_seen()]] - code - ingestion/deduplicator.py
- [[test_duplicate_not_written_twice.py]] - code - tests/unit/test_duplicate_not_written_twice.py
- [[test_duplicate_not_written_twice_semantic_dedup()]] - code - tests/unit/test_duplicate_not_written_twice.py
- [[test_duplicate_not_written_twice_url_dedup()]] - code - tests/unit/test_duplicate_not_written_twice.py
- [[test_unique_articles_all_pass_dedup()]] - code - tests/unit/test_duplicate_not_written_twice.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Deduplication_Pipeline
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 4 edges to [[_COMMUNITY_External Data Fetching]]
- 2 edges to [[_COMMUNITY_FastAPI Layer]]
- 2 edges to [[_COMMUNITY_Service Entry & Delivery]]
- 1 edge to [[_COMMUNITY_Article Normalization]]
- 1 edge to [[_COMMUNITY_API Routes & Contradiction Detection]]

## Top bridge nodes
- [[deduplicator.py]] - degree 10, connects to 2 communities
- [[test_duplicate_not_written_twice.py]] - degree 8, connects to 2 communities
- [[make_article()]] - degree 6, connects to 2 communities
- [[deduplicate_batch()]] - degree 11, connects to 1 community
- [[is_duplicate_url()]] - degree 5, connects to 1 community