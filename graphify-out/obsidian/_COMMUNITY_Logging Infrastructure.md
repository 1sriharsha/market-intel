---
type: community
cohesion: 0.22
members: 11
---

# Logging Infrastructure

**Cohesion:** 0.22 - loosely connected
**Members:** 11 nodes

## Members
- [[.__init__()]] - code - config/log.py
- [[.debug()]] - code - config/log.py
- [[.error()]] - code - config/log.py
- [[.exception()]] - code - config/log.py
- [[.info()]] - code - config/log.py
- [[.warn()]] - code - config/log.py
- [[.warning()]] - code - config/log.py
- [[Structlog compatibility shim — falls back to stdlib logging when structlog not i]] - rationale - config/log.py
- [[_StdlibAdapter]] - code - config/log.py
- [[get_logger()]] - code - config/log.py
- [[log.py]] - code - config/log.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Logging_Infrastructure
SORT file.name ASC
```
