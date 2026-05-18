---
type: community
cohesion: 0.24
members: 13
---

# Embedding (OpenAI)

**Cohesion:** 0.24 - loosely connected
**Members:** 13 nodes

## Members
- [[Batch embedding — minimizes OpenAI API round trips.     Max 2048 inputs per API]] - rationale - enrichment/embedder.py
- [[Embed all bootstrapped articles that haven't been embedded yet. Run overnight af]] - rationale - scripts/backfill_embeddings.py
- [[Fetch article from DB, embed title+summary, write to embeddings table.     Updat]] - rationale - enrichment/embedder.py
- [[OpenAI text-embedding-3-small generation and storage.]] - rationale - enrichment/embedder.py
- [[_build_embed_input()]] - code - enrichment/embedder.py
- [[_content_hash()]] - code - enrichment/embedder.py
- [[_embed_texts()]] - code - enrichment/embedder.py
- [[_get_client()_1]] - code - enrichment/embedder.py
- [[backfill()]] - code - scripts/backfill_embeddings.py
- [[backfill_embeddings.py]] - code - scripts/backfill_embeddings.py
- [[embed_article()]] - code - enrichment/embedder.py
- [[embed_batch()]] - code - enrichment/embedder.py
- [[embedder.py]] - code - enrichment/embedder.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Embedding_(OpenAI)
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_External Data Fetching]]
- 2 edges to [[_COMMUNITY_Async DB & Celery Workers]]
- 2 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 1 edge to [[_COMMUNITY_API Routes & Contradiction Detection]]

## Top bridge nodes
- [[embed_batch()]] - degree 8, connects to 2 communities
- [[embedder.py]] - degree 9, connects to 1 community
- [[embed_article()]] - degree 6, connects to 1 community
- [[_embed_texts()]] - degree 5, connects to 1 community
- [[backfill()]] - degree 3, connects to 1 community