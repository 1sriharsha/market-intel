---
source_file: "ingestion/price_fetcher.py"
type: "code"
community: "Price Data & Abnormal Returns"
location: "L54"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Price_Data_&_Abnormal_Returns
---

# sync_daily_prices()

## Connections
- [[Fetch last 5 trading days for all tickers. Upserts into prices table.     Handle]] - `rationale_for` [EXTRACTED]
- [[_fetch_yfinance()]] - `calls` [EXTRACTED]
- [[_price_sync_async()]] - `calls` [INFERRED]
- [[_upsert_prices()]] - `calls` [EXTRACTED]
- [[price_fetcher.py]] - `contains` [EXTRACTED]
- [[str]] - `calls` [INFERRED]

#graphify/code #graphify/EXTRACTED #community/Price_Data_&_Abnormal_Returns