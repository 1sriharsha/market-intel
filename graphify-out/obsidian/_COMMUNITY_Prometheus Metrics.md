---
type: community
cohesion: 1.00
members: 2
---

# Prometheus Metrics

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[Prometheus metric definitions for all MIOS subsystems.]] - rationale - monitoring/metrics.py
- [[metrics.py]] - code - monitoring/metrics.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Prometheus_Metrics
SORT file.name ASC
```
