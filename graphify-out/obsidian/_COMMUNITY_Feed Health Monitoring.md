---
type: community
cohesion: 0.25
members: 9
---

# Feed Health Monitoring

**Cohesion:** 0.25 - loosely connected
**Members:** 9 nodes

## Members
- [[Check all active feeds for staleness.     A feed is unhealthy if last_fetched_at]] - rationale - monitoring/health_checker.py
- [[Count articles awaiting embedding.]] - rationale - monitoring/health_checker.py
- [[Feed health monitoring and ingestion lag detection.]] - rationale - monitoring/health_checker.py
- [[Returns True if no articles have been ingested in the last threshold_minutes.]] - rationale - monitoring/health_checker.py
- [[_check_feeds()]] - code - monitoring/health_checker.py
- [[check_feed_health()]] - code - monitoring/health_checker.py
- [[detect_ingestion_stall()]] - code - monitoring/health_checker.py
- [[get_embedding_backlog()]] - code - monitoring/health_checker.py
- [[health_checker.py]] - code - monitoring/health_checker.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Feed_Health_Monitoring
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_External Data Fetching]]
- 1 edge to [[_COMMUNITY_Async DB & Celery Workers]]
- 1 edge to [[_COMMUNITY_Core Config & Ingestion Hub]]

## Top bridge nodes
- [[check_feed_health()]] - degree 5, connects to 2 communities
- [[health_checker.py]] - degree 6, connects to 1 community
- [[_check_feeds()]] - degree 3, connects to 1 community