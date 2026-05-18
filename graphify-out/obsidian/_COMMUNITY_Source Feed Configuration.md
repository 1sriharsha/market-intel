---
type: community
cohesion: 0.15
members: 20
---

# Source Feed Configuration

**Cohesion:** 0.15 - loosely connected
**Members:** 20 nodes

## Members
- [[All RSS feed URLs, API endpoints, and source trust tier assignments.]] - rationale - config/sources.py
- [[Build a Google News RSS URL for a given search query.]] - rationale - config/sources.py
- [[Convert a feedparser entry to a RawArticle.     Never raises — returns None on i]] - rationale - ingestion/rss_fetcher.py
- [[Dynamically build Google News RSS feeds for all watchlist tickers.]] - rationale - ingestion/rss_fetcher.py
- [[Exception]] - code
- [[FeedFetchError]] - code - ingestion/rss_fetcher.py
- [[FeedParseError]] - code - ingestion/rss_fetcher.py
- [[Fetch all active RSS feeds concurrently (semaphore=10).     Aggregates results.]] - rationale - ingestion/rss_fetcher.py
- [[Fetch one RSS feed. Returns normalized RawArticle objects.     Raises FeedFetchE]] - rationale - ingestion/rss_fetcher.py
- [[SourceFeed]] - code - config/sources.py
- [[_build_macro_google_news_feeds()]] - code - ingestion/rss_fetcher.py
- [[_build_ticker_google_news_feeds()]] - code - ingestion/rss_fetcher.py
- [[build_google_news_url()]] - code - config/sources.py
- [[feedparser-based RSSAtom ingestion for all tier 1, 2A, 2B, 2C sources.]] - rationale - ingestion/rss_fetcher.py
- [[fetch_all_feeds()]] - code - ingestion/rss_fetcher.py
- [[fetch_feed()]] - code - ingestion/rss_fetcher.py
- [[get_all_rss_feeds()]] - code - ingestion/rss_fetcher.py
- [[normalize_rss_item()]] - code - ingestion/rss_fetcher.py
- [[rss_fetcher.py]] - code - ingestion/rss_fetcher.py
- [[sources.py]] - code - config/sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Source_Feed_Configuration
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 2 edges to [[_COMMUNITY_API Routes & Contradiction Detection]]
- 2 edges to [[_COMMUNITY_External Data Fetching]]
- 1 edge to [[_COMMUNITY_FastAPI Layer]]
- 1 edge to [[_COMMUNITY_Article Normalization]]

## Top bridge nodes
- [[rss_fetcher.py]] - degree 15, connects to 2 communities
- [[normalize_rss_item()]] - degree 5, connects to 2 communities
- [[FeedFetchError]] - degree 5, connects to 1 community
- [[FeedParseError]] - degree 5, connects to 1 community
- [[fetch_all_feeds()]] - degree 4, connects to 1 community