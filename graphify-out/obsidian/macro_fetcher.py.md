---
source_file: "ingestion/macro_fetcher.py"
type: "code"
community: "External Data Fetching"
location: "L1"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/External_Data_Fetching
---

# macro_fetcher.py

## Connections
- [[FRED, BLS macro data fetcher — bootstraps full history, syncs daily.]] - `rationale_for` [EXTRACTED]
- [[Logger (configlog.py)]] - `imports_from` [EXTRACTED]
- [[Pydantic Schemas (schemas.py)]] - `imports_from` [EXTRACTED]
- [[Settings (configsettings.py)]] - `imports_from` [EXTRACTED]
- [[Sources Config (configsources.py)]] - `imports_from` [EXTRACTED]
- [[_fetch_fred_series()]] - `contains` [EXTRACTED]
- [[_fetch_fred_series_since()]] - `contains` [EXTRACTED]
- [[_get_fred_client()]] - `contains` [EXTRACTED]
- [[bootstrap_macro_series()]] - `contains` [EXTRACTED]
- [[get_macro_snapshot()]] - `contains` [EXTRACTED]
- [[sync_macro_updates()]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/External_Data_Fetching