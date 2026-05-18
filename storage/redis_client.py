"""Redis connection + helper utilities."""
from typing import Optional

import redis.asyncio as aioredis

from config.settings import settings

_redis_client: Optional[aioredis.Redis] = None


def get_redis() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            socket_timeout=5,
            socket_connect_timeout=5,
        )
    return _redis_client


async def close_redis() -> None:
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None


# ---------------------------------------------------------------------------
# Deduplication helpers
# ---------------------------------------------------------------------------

async def set_url_seen(url_hash: str, ttl_seconds: int | None = None) -> None:
    """Mark a URL hash as seen. Raises nothing on failure — dedup is best-effort."""
    client = get_redis()
    ttl = ttl_seconds or settings.url_dedup_ttl_seconds
    try:
        await client.setex(f"url:{url_hash}", ttl, "1")
    except Exception:
        pass


async def is_url_seen(url_hash: str) -> bool:
    client = get_redis()
    try:
        return bool(await client.exists(f"url:{url_hash}"))
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Rate limit helpers (token bucket via Redis counter)
# ---------------------------------------------------------------------------

async def check_rate_limit(key: str, limit: int, window_seconds: int) -> bool:
    """Returns True if request is allowed, False if rate limit exceeded."""
    client = get_redis()
    try:
        pipe = client.pipeline()
        pipe.incr(f"rl:{key}")
        pipe.expire(f"rl:{key}", window_seconds)
        results = await pipe.execute()
        count = results[0]
        return count <= limit
    except Exception:
        return True   # fail open — don't block on Redis error


async def get_rate_limit_count(key: str) -> int:
    client = get_redis()
    try:
        val = await client.get(f"rl:{key}")
        return int(val) if val else 0
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Daily counter helpers (for Telegram alert cap)
# ---------------------------------------------------------------------------

async def increment_daily_counter(key: str) -> int:
    """Increment a daily counter (resets at midnight UTC). Returns new count."""
    from datetime import datetime, timezone
    client = get_redis()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    full_key = f"daily:{key}:{today}"
    try:
        pipe = client.pipeline()
        pipe.incr(full_key)
        pipe.expireat(full_key, _next_midnight_ts())
        results = await pipe.execute()
        return results[0]
    except Exception:
        return 0


async def get_daily_counter(key: str) -> int:
    from datetime import datetime, timezone
    client = get_redis()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        val = await client.get(f"daily:{key}:{today}")
        return int(val) if val else 0
    except Exception:
        return 0


def _next_midnight_ts() -> int:
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return int(midnight.timestamp())


# ---------------------------------------------------------------------------
# Ticker cooldown helpers
# ---------------------------------------------------------------------------

async def set_ticker_cooldown(ticker: str, cooldown_hours: int) -> None:
    client = get_redis()
    ttl = cooldown_hours * 3600
    try:
        await client.setex(f"cooldown:{ticker}", ttl, "1")
    except Exception:
        pass


async def is_ticker_on_cooldown(ticker: str) -> bool:
    client = get_redis()
    try:
        return bool(await client.exists(f"cooldown:{ticker}"))
    except Exception:
        return False
