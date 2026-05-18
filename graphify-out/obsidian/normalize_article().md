---
source_file: "ingestion/normalizer.py"
type: "code"
community: "Article Normalization"
location: "L72"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Article_Normalization
---

# normalize_article()

## Connections
- [[.test_html_stripped_from_summary()]] - `calls` [INFERRED]
- [[Produce a canonical RawArticle from any source's raw fields.     Returns None if]] - `rationale_for` [EXTRACTED]
- [[RawArticle]] - `calls` [INFERRED]
- [[article_id()]] - `calls` [EXTRACTED]
- [[canonical_url()]] - `calls` [EXTRACTED]
- [[fetch_alpha_vantage_news()]] - `calls` [INFERRED]
- [[fetch_finnhub_news()]] - `calls` [INFERRED]
- [[fetch_marketaux_news()]] - `calls` [INFERRED]
- [[normalize_rss_item()]] - `calls` [INFERRED]
- [[normalizer.py]] - `contains` [EXTRACTED]
- [[parse_datetime()]] - `calls` [EXTRACTED]
- [[poll_edgar_rss()]] - `calls` [INFERRED]
- [[strip_html()]] - `calls` [EXTRACTED]
- [[test_published_at_always_utc()]] - `calls` [INFERRED]
- [[test_published_at_never_null_accepts_valid_date()]] - `calls` [INFERRED]
- [[test_published_at_never_null_rejects_if_missing()]] - `calls` [INFERRED]
- [[test_published_at_never_null_rejects_missing_title()]] - `calls` [INFERRED]
- [[test_published_at_never_null_rejects_missing_url()]] - `calls` [INFERRED]
- [[test_published_at_never_null_uses_datetime_directly()]] - `calls` [INFERRED]

#graphify/code #graphify/INFERRED #community/Article_Normalization