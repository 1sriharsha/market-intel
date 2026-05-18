---
source_file: "ingestion/normalizer.py"
type: "code"
community: "Article Normalization"
location: "L1"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Article_Normalization
---

# normalizer.py

## Connections
- [[Maps all raw ingestion sources to canonical RawArticle schema.]] - `rationale_for` [EXTRACTED]
- [[Pydantic Schemas (schemas.py)]] - `imports_from` [EXTRACTED]
- [[article_id()]] - `contains` [EXTRACTED]
- [[canonical_url()]] - `contains` [EXTRACTED]
- [[normalize_article()]] - `contains` [EXTRACTED]
- [[parse_datetime()]] - `contains` [EXTRACTED]
- [[strip_html()]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Article_Normalization