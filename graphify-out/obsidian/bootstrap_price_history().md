---
source_file: "ingestion/price_fetcher.py"
type: "code"
community: "Price Data & Abnormal Returns"
location: "L29"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Price_Data_&_Abnormal_Returns
---

# bootstrap_price_history()

## Connections
- [[One-time function. Fetches period='max' for each ticker.     Skips tickers that]] - `rationale_for` [EXTRACTED]
- [[_fetch_yfinance()]] - `calls` [EXTRACTED]
- [[_upsert_prices()]] - `calls` [EXTRACTED]
- [[bootstrap()]] - `calls` [INFERRED]
- [[price_fetcher.py]] - `contains` [EXTRACTED]
- [[str]] - `calls` [INFERRED]

#graphify/code #graphify/EXTRACTED #community/Price_Data_&_Abnormal_Returns