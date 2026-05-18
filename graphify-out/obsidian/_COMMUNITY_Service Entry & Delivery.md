---
type: community
cohesion: 0.07
members: 42
---

# Service Entry & Delivery

**Cohesion:** 0.07 - loosely connected
**Members:** 42 nodes

## Members
- [[After MAX_DAILY_ALERTS deliveries, further alerts must be suppressed.]] - rationale - tests/unit/test_rate_limit_respected.py
- [[Before the cap is reached, delivery must be allowed.]] - rationale - tests/unit/test_rate_limit_respected.py
- [[CRITICAL TEST test_rate_limit_respected Operational compliance — Telegram daily]] - rationale - tests/unit/test_rate_limit_respected.py
- [[Critical significance objects must pass delivery check (when under cap, no coold]] - rationale - tests/unit/test_rate_limit_respected.py
- [[Daily cap must be exactly 5 — hardcoded in spec, not arbitrary.]] - rationale - tests/unit/test_rate_limit_respected.py
- [[Evaluate, format, and push. Updates cooldowns and counters on success.     Retur]] - rationale - delivery/telegram_bot.py
- [[FastAPI application entry point.]] - rationale - api/main.py
- [[Fetch entity-tagged news from Marketaux.     Rate limit 100 reqday via Redis d]] - rationale - ingestion/api_fetcher.py
- [[Increment a daily counter (resets at midnight UTC). Returns new count.]] - rationale - storage/redis_client.py
- [[Low and medium significance objects must never be delivered.]] - rationale - tests/unit/test_rate_limit_respected.py
- [[Mark a URL hash as seen. Raises nothing on failure — dedup is best-effort.]] - rationale - storage/redis_client.py
- [[Redis connection + helper utilities.]] - rationale - storage/redis_client.py
- [[Returns True if an intelligence object should be pushed to Telegram.      Hard r]] - rationale - delivery/telegram_bot.py
- [[Returns True if request is allowed, False if rate limit exceeded.]] - rationale - storage/redis_client.py
- [[Ticker cooldown must be exactly 4 hours per spec.]] - rationale - tests/unit/test_rate_limit_respected.py
- [[Ticker on 4-hour cooldown must prevent delivery.]] - rationale - tests/unit/test_rate_limit_respected.py
- [[_next_midnight_ts()]] - code - storage/redis_client.py
- [[check_rate_limit()]] - code - storage/redis_client.py
- [[close_redis()]] - code - storage/redis_client.py
- [[deliver()]] - code - delivery/telegram_bot.py
- [[evaluate_delivery()]] - code - delivery/telegram_bot.py
- [[fetch_marketaux_news()]] - code - ingestion/api_fetcher.py
- [[get_daily_counter()]] - code - storage/redis_client.py
- [[get_rate_limit_count()]] - code - storage/redis_client.py
- [[get_redis()]] - code - storage/redis_client.py
- [[increment_daily_counter()]] - code - storage/redis_client.py
- [[int]] - code
- [[is_ticker_on_cooldown()]] - code - storage/redis_client.py
- [[is_url_seen()]] - code - storage/redis_client.py
- [[lifespan()]] - code - api/main.py
- [[main.py_1]] - code - api/main.py
- [[redis_client.py]] - code - storage/redis_client.py
- [[set_ticker_cooldown()]] - code - storage/redis_client.py
- [[set_url_seen()]] - code - storage/redis_client.py
- [[test_cooldown_is_four_hours()]] - code - tests/unit/test_rate_limit_respected.py
- [[test_critical_significance_allowed()]] - code - tests/unit/test_rate_limit_respected.py
- [[test_daily_cap_is_exactly_five()]] - code - tests/unit/test_rate_limit_respected.py
- [[test_low_significance_always_suppressed()]] - code - tests/unit/test_rate_limit_respected.py
- [[test_rate_limit_respected.py]] - code - tests/unit/test_rate_limit_respected.py
- [[test_telegram_daily_cap_allows_before_limit()]] - code - tests/unit/test_rate_limit_respected.py
- [[test_telegram_daily_cap_enforced()]] - code - tests/unit/test_rate_limit_respected.py
- [[test_ticker_cooldown_enforced()]] - code - tests/unit/test_rate_limit_respected.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Service_Entry_&_Delivery
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 5 edges to [[_COMMUNITY_External Data Fetching]]
- 3 edges to [[_COMMUNITY_Intelligence Generation]]
- 2 edges to [[_COMMUNITY_Deduplication Pipeline]]
- 2 edges to [[_COMMUNITY_API Routes & Contradiction Detection]]
- 1 edge to [[_COMMUNITY_Price Data & Abnormal Returns]]
- 1 edge to [[_COMMUNITY_Article Normalization]]

## Top bridge nodes
- [[fetch_marketaux_news()]] - degree 7, connects to 3 communities
- [[int]] - degree 6, connects to 3 communities
- [[evaluate_delivery()]] - degree 11, connects to 2 communities
- [[deliver()]] - degree 7, connects to 2 communities
- [[redis_client.py]] - degree 13, connects to 1 community