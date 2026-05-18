---
type: community
cohesion: 0.10
members: 29
---

# Article Normalization

**Cohesion:** 0.10 - loosely connected
**Members:** 29 nodes

## Members
- [[.test_article_id_is_sha256()]] - code - tests/unit/test_unit_misc.py
- [[.test_canonical_url_strips_tracking_params()]] - code - tests/unit/test_unit_misc.py
- [[.test_html_stripped_from_summary()]] - code - tests/unit/test_unit_misc.py
- [[CRITICAL TEST test_published_at_never_null Data integrity — normalizer must rej]] - rationale - tests/unit/test_published_at_never_null.py
- [[Maps all raw ingestion sources to canonical RawArticle schema.]] - rationale - ingestion/normalizer.py
- [[Naive datetimes must be converted to UTC.]] - rationale - tests/unit/test_published_at_never_null.py
- [[Parse any reasonable date string to a UTC-aware datetime. Returns fallback if un]] - rationale - ingestion/normalizer.py
- [[Produce a canonical RawArticle from any source's raw fields.     Returns None if]] - rationale - ingestion/normalizer.py
- [[SHA-256 of canonical URL — stable primary key.]] - rationale - ingestion/normalizer.py
- [[Strip query params that don't affect content identity (tracking params etc).]] - rationale - ingestion/normalizer.py
- [[TestNormalizer]] - code - tests/unit/test_unit_misc.py
- [[article_id()]] - code - ingestion/normalizer.py
- [[canonical_url()]] - code - ingestion/normalizer.py
- [[normalize_article accepts an explicit datetime object.]] - rationale - tests/unit/test_published_at_never_null.py
- [[normalize_article must return None when URL is missing.]] - rationale - tests/unit/test_published_at_never_null.py
- [[normalize_article must return None when published_at is completely unavailable.]] - rationale - tests/unit/test_published_at_never_null.py
- [[normalize_article must return None when title is missing.]] - rationale - tests/unit/test_published_at_never_null.py
- [[normalize_article must set published_at when a valid date string is provided.]] - rationale - tests/unit/test_published_at_never_null.py
- [[normalize_article()]] - code - ingestion/normalizer.py
- [[normalizer.py]] - code - ingestion/normalizer.py
- [[parse_datetime()]] - code - ingestion/normalizer.py
- [[strip_html()]] - code - ingestion/normalizer.py
- [[test_published_at_always_utc()]] - code - tests/unit/test_published_at_never_null.py
- [[test_published_at_never_null.py]] - code - tests/unit/test_published_at_never_null.py
- [[test_published_at_never_null_accepts_valid_date()]] - code - tests/unit/test_published_at_never_null.py
- [[test_published_at_never_null_rejects_if_missing()]] - code - tests/unit/test_published_at_never_null.py
- [[test_published_at_never_null_rejects_missing_title()]] - code - tests/unit/test_published_at_never_null.py
- [[test_published_at_never_null_rejects_missing_url()]] - code - tests/unit/test_published_at_never_null.py
- [[test_published_at_never_null_uses_datetime_directly()]] - code - tests/unit/test_published_at_never_null.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Article_Normalization
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_External Data Fetching]]
- 2 edges to [[_COMMUNITY_API Routes & Contradiction Detection]]
- 1 edge to [[_COMMUNITY_Source Feed Configuration]]
- 1 edge to [[_COMMUNITY_FastAPI Layer]]
- 1 edge to [[_COMMUNITY_Deduplication Pipeline]]
- 1 edge to [[_COMMUNITY_Service Entry & Delivery]]
- 1 edge to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 1 edge to [[_COMMUNITY_Macro & Regime Analysis]]

## Top bridge nodes
- [[normalize_article()]] - degree 19, connects to 4 communities
- [[TestNormalizer]] - degree 5, connects to 2 communities
- [[test_published_at_never_null.py]] - degree 8, connects to 1 community
- [[normalizer.py]] - degree 7, connects to 1 community
- [[article_id()]] - degree 6, connects to 1 community