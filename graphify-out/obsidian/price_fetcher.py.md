---
source_file: "ingestion/price_fetcher.py"
type: "code"
community: "Price Data & Abnormal Returns"
location: "L1"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Price_Data_&_Abnormal_Returns
---

# price_fetcher.py

## Connections
- [[Logger (configlog.py)]] - `imports_from` [EXTRACTED]
- [[Pydantic Schemas (schemas.py)]] - `imports_from` [EXTRACTED]
- [[Settings (configsettings.py)]] - `imports_from` [EXTRACTED]
- [[_fetch_price_series()]] - `contains` [EXTRACTED]
- [[_fetch_yfinance()]] - `contains` [EXTRACTED]
- [[_fetch_yfinance_sync()]] - `contains` [EXTRACTED]
- [[_label_reaction()]] - `contains` [EXTRACTED]
- [[_upsert_prices()]] - `contains` [EXTRACTED]
- [[bootstrap_price_history()]] - `contains` [EXTRACTED]
- [[compute_abnormal_return()]] - `contains` [EXTRACTED]
- [[get_price_at()]] - `contains` [EXTRACTED]
- [[sync_daily_prices()]] - `contains` [EXTRACTED]
- [[yfinance price data — historical bootstrap and daily sync.]] - `rationale_for` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Price_Data_&_Abnormal_Returns