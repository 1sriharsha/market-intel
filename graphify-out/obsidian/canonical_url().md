---
source_file: "ingestion/normalizer.py"
type: "code"
community: "Article Normalization"
location: "L16"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Article_Normalization
---

# canonical_url()

## Connections
- [[.test_article_id_is_sha256()]] - `calls` [INFERRED]
- [[.test_canonical_url_strips_tracking_params()]] - `calls` [INFERRED]
- [[Strip query params that don't affect content identity (tracking params etc).]] - `rationale_for` [EXTRACTED]
- [[article_id()]] - `calls` [EXTRACTED]
- [[normalize_article()]] - `calls` [EXTRACTED]
- [[normalizer.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Article_Normalization