---
type: community
cohesion: 0.50
members: 4
---

# Celery Beat Schedule

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[Celery application init + task registry + beat schedule.]] - rationale - workers/celery_app.py
- [[No-op — schedule is registered via app.conf above. Called by main.py to import w]] - rationale - workers/celery_app.py
- [[celery_app.py]] - code - workers/celery_app.py
- [[register_beat_schedule()]] - code - workers/celery_app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Celery_Beat_Schedule
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Core Config & Ingestion Hub]]

## Top bridge nodes
- [[celery_app.py]] - degree 3, connects to 1 community