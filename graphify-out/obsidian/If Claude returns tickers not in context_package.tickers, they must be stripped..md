---
source_file: "tests/unit/test_no_hallucination_beyond_context.py"
type: "rationale"
community: "Hallucination Guard Tests"
location: "L16"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Hallucination_Guard_Tests
---

# If Claude returns tickers not in context_package.tickers, they must be stripped.

## Connections
- [[test_hallucinated_tickers_stripped()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Hallucination_Guard_Tests