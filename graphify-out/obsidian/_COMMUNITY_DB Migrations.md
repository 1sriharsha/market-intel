---
type: community
cohesion: 0.19
members: 19
---

# DB Migrations

**Cohesion:** 0.19 - loosely connected
**Members:** 19 nodes

## Members
- [[Alembic Migration Environment]] - code - storage/migrations/env.py
- [[Alembic environment configuration for async SQLAlchemy.]] - rationale - storage/migrations/env.py
- [[Initial DB Schema Migration (0001)]] - code - storage/migrations/versions/0001_initial_schema.py
- [[ORM Model Article]] - code - models/db.py
- [[ORM Model ArticleTickerEffect]] - code - models/db.py
- [[ORM Model BootstrapState]] - code - models/db.py
- [[ORM Model Embedding]] - code - models/db.py
- [[ORM Model HistoricalEvent]] - code - models/db.py
- [[ORM Model IntelligenceObject]] - code - models/db.py
- [[ORM Model MacroData]] - code - models/db.py
- [[ORM Model Price]] - code - models/db.py
- [[ORM Model RegimeSnapshot]] - code - models/db.py
- [[ORM Model SourceFeed]] - code - models/db.py
- [[ORM Models (db.py)]] - code - models/db.py
- [[do_run_migrations()]] - code - storage/migrations/env.py
- [[env.py]] - code - storage/migrations/env.py
- [[run_async_migrations()]] - code - storage/migrations/env.py
- [[run_migrations_offline()]] - code - storage/migrations/env.py
- [[run_migrations_online()]] - code - storage/migrations/env.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/DB_Migrations
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 1 edge to [[_COMMUNITY_FastAPI Layer]]

## Top bridge nodes
- [[ORM Model IntelligenceObject]] - degree 4, connects to 2 communities
- [[ORM Model Article]] - degree 7, connects to 1 community
- [[env.py]] - degree 7, connects to 1 community
- [[ORM Model BootstrapState]] - degree 3, connects to 1 community
- [[Alembic Migration Environment]] - degree 3, connects to 1 community