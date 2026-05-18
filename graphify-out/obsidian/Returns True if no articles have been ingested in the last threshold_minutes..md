---
source_file: "monitoring/health_checker.py"
type: "rationale"
community: "Feed Health Monitoring"
location: "L95"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Feed_Health_Monitoring
---

# Returns True if no articles have been ingested in the last threshold_minutes.

## Connections
- [[detect_ingestion_stall()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Feed_Health_Monitoring