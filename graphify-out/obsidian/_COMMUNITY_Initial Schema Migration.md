---
type: community
cohesion: 0.50
members: 4
---

# Initial Schema Migration

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[0001_initial_schema.py]] - code - storage/migrations/versions/0001_initial_schema.py
- [[Initial schema — all 9 canonical tables + pgvector + TimescaleDB extensions.]] - rationale - storage/migrations/versions/0001_initial_schema.py
- [[downgrade()]] - code - storage/migrations/versions/0001_initial_schema.py
- [[upgrade()]] - code - storage/migrations/versions/0001_initial_schema.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Initial_Schema_Migration
SORT file.name ASC
```
