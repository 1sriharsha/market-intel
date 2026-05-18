---
type: community
cohesion: 0.32
members: 8
---

# Ticker Extraction (spaCy+Regex)

**Cohesion:** 0.32 - loosely connected
**Members:** 8 nodes

## Members
- [[Build and cache a map from company name variants to ticker symbols.     Sources]] - rationale - enrichment/ticker_extractor.py
- [[Multi-pass ticker extraction     1. Regex for explicit $TICKER and NYSETICKER]] - rationale - enrichment/ticker_extractor.py
- [[_get_company_map()]] - code - enrichment/ticker_extractor.py
- [[_load_spacy()]] - code - enrichment/ticker_extractor.py
- [[build_company_ticker_map()]] - code - enrichment/ticker_extractor.py
- [[extract_tickers()]] - code - enrichment/ticker_extractor.py
- [[spaCy + regex ticker extraction. Three-pass approach.]] - rationale - enrichment/ticker_extractor.py
- [[ticker_extractor.py]] - code - enrichment/ticker_extractor.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Ticker_Extraction_(spaCy+Regex)
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_External Data Fetching]]
- 2 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]

## Top bridge nodes
- [[ticker_extractor.py]] - degree 7, connects to 1 community
- [[extract_tickers()]] - degree 6, connects to 1 community