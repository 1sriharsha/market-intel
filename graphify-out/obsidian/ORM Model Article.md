---
source_file: "models/db.py"
type: "code"
community: "DB Migrations"
location: "19"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/DB_Migrations
---

# ORM Model: Article

## Connections
- [[Backfill Embeddings Script]] - `shares_data_with` [INFERRED]
- [[Initial DB Schema Migration (0001)]] - `implements` [EXTRACTED]
- [[ORM Model ArticleTickerEffect]] - `references` [EXTRACTED]
- [[ORM Model Embedding]] - `references` [EXTRACTED]
- [[ORM Model SourceFeed]] - `references` [EXTRACTED]
- [[ORM Models (db.py)]] - `implements` [EXTRACTED]
- [[Pydantic Schema RawArticle]] - `semantically_similar_to` [INFERRED]

#graphify/code #graphify/EXTRACTED #community/DB_Migrations