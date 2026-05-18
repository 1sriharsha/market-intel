---
type: community
cohesion: 0.17
members: 17
---

# Price Data & Abnormal Returns

**Cohesion:** 0.17 - loosely connected
**Members:** 17 nodes

## Members
- [[Compute abnormal return relative to SPY for a given ticker and event date.     U]] - rationale - ingestion/price_fetcher.py
- [[Fetch last 5 trading days for all tickers. Upserts into prices table.     Handle]] - rationale - ingestion/price_fetcher.py
- [[For each ticker mentioned in an article, compute and persist     - price at pub]] - rationale - enrichment/price_reactor.py
- [[One-time function. Fetches period='max' for each ticker.     Skips tickers that]] - rationale - ingestion/price_fetcher.py
- [[Returns adjusted close price for a ticker on a given date.     Returns None if n]] - rationale - ingestion/price_fetcher.py
- [[_fetch_price_series()]] - code - ingestion/price_fetcher.py
- [[_fetch_yfinance()]] - code - ingestion/price_fetcher.py
- [[_fetch_yfinance_sync()]] - code - ingestion/price_fetcher.py
- [[_label_reaction()]] - code - ingestion/price_fetcher.py
- [[_upsert_prices()]] - code - ingestion/price_fetcher.py
- [[bootstrap_price_history()]] - code - ingestion/price_fetcher.py
- [[compute_abnormal_return()]] - code - ingestion/price_fetcher.py
- [[compute_and_store_price_reactions()]] - code - enrichment/price_reactor.py
- [[get_price_at()]] - code - ingestion/price_fetcher.py
- [[price_fetcher.py]] - code - ingestion/price_fetcher.py
- [[sync_daily_prices()]] - code - ingestion/price_fetcher.py
- [[yfinance price data — historical bootstrap and daily sync.]] - rationale - ingestion/price_fetcher.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Price_Data_&_Abnormal_Returns
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_External Data Fetching]]
- 3 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 2 edges to [[_COMMUNITY_Async DB & Celery Workers]]
- 2 edges to [[_COMMUNITY_API Routes & Contradiction Detection]]
- 1 edge to [[_COMMUNITY_FastAPI Layer]]
- 1 edge to [[_COMMUNITY_Service Entry & Delivery]]

## Top bridge nodes
- [[compute_and_store_price_reactions()]] - degree 6, connects to 3 communities
- [[price_fetcher.py]] - degree 13, connects to 2 communities
- [[sync_daily_prices()]] - degree 6, connects to 2 communities
- [[bootstrap_price_history()]] - degree 6, connects to 1 community
- [[compute_abnormal_return()]] - degree 6, connects to 1 community