---
type: community
cohesion: 0.23
members: 15
---

# ORM Schema Layer

**Cohesion:** 0.23 - loosely connected
**Members:** 15 nodes

## Members
- [[Article]] - code - models/db.py
- [[ArticleTickerEffect]] - code - models/db.py
- [[Base]] - code - models/db.py
- [[BootstrapState]] - code - models/db.py
- [[DeclarativeBase]] - code
- [[Embedding]] - code - models/db.py
- [[HistoricalEvent]] - code - models/db.py
- [[IntelligenceObject]] - code - models/db.py
- [[MacroData]] - code - models/db.py
- [[Price]] - code - models/db.py
- [[RegimeSnapshot]] - code - models/db.py
- [[SQLAlchemy 2.0 async ORM models — canonical schema for all 9 tables.]] - rationale - models/db.py
- [[SourceFeed_1]] - code - models/db.py
- [[Tracks resumable bootstrap progress.]] - rationale - models/db.py
- [[db.py]] - code - models/db.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ORM_Schema_Layer
SORT file.name ASC
```
