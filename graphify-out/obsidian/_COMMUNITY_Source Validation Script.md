---
type: community
cohesion: 0.67
members: 3
---

# Source Validation Script

**Cohesion:** 0.67 - moderately connected
**Members:** 3 nodes

## Members
- [[Smoke test all configured feeds before deployment. Run python scriptsvalidate_]] - rationale - scripts/validate_sources.py
- [[validate()]] - code - scripts/validate_sources.py
- [[validate_sources.py]] - code - scripts/validate_sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Source_Validation_Script
SORT file.name ASC
```
