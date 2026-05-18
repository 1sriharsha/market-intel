"""Feed health monitoring and ingestion lag detection."""
from datetime import datetime, timezone, timedelta

from config.log import get_logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

log = get_logger(__name__)


async def check_feed_health(session: AsyncSession | None = None) -> dict:
    """
    Check all active feeds for staleness.
    A feed is unhealthy if last_fetched_at is older than 2× its fetch_interval.
    Updates metrics and logs unhealthy feeds.
    """
    from storage.database import get_session
    from monitoring.metrics import feeds_healthy, feeds_total, ingestion_lag_minutes

    if session is None:
        async with get_session() as s:
            return await _check_feeds(s, feeds_healthy, feeds_total, ingestion_lag_minutes)
    return await _check_feeds(session, feeds_healthy, feeds_total, ingestion_lag_minutes)


async def _check_feeds(session, feeds_healthy_gauge, feeds_total_gauge, lag_gauge) -> dict:
    result = await session.execute(
        text("""
            SELECT
                id, name, fetch_interval_minutes, last_fetched_at, last_error, is_active
            FROM source_feeds
            WHERE is_active = true
        """)
    )
    feeds = result.fetchall()

    now = datetime.now(timezone.utc)
    healthy = 0
    unhealthy_feeds = []

    for feed in feeds:
        feed_id, name, interval, last_fetched, last_error, is_active = feed
        threshold = timedelta(minutes=(interval or 15) * 2)

        if last_fetched is None:
            unhealthy_feeds.append({"id": feed_id, "reason": "never_fetched"})
            continue

        # Ensure timezone-aware comparison
        if last_fetched.tzinfo is None:
            last_fetched = last_fetched.replace(tzinfo=timezone.utc)

        if now - last_fetched > threshold:
            unhealthy_feeds.append({
                "id": feed_id,
                "name": name,
                "last_fetched": str(last_fetched),
                "lag_minutes": (now - last_fetched).total_seconds() / 60,
                "last_error": last_error,
            })
        else:
            healthy += 1

    feeds_healthy_gauge.set(healthy)
    feeds_total_gauge.set(len(feeds))

    # Overall ingestion lag
    lag_result = await session.execute(
        text("SELECT EXTRACT(EPOCH FROM (NOW() - MAX(fetched_at)))/60.0 FROM articles")
    )
    lag = lag_result.scalar()
    if lag is not None:
        lag_gauge.set(float(lag))

    if unhealthy_feeds:
        log.warning("health.feeds_unhealthy", count=len(unhealthy_feeds), feeds=unhealthy_feeds[:5])

    return {
        "healthy": healthy,
        "total": len(feeds),
        "unhealthy": unhealthy_feeds,
        "checked_at": now.isoformat(),
    }


async def get_embedding_backlog(session: AsyncSession) -> int:
    """Count articles awaiting embedding."""
    result = await session.execute(
        text("SELECT COUNT(*) FROM articles WHERE is_embedded = false")
    )
    return result.scalar() or 0


async def detect_ingestion_stall(session: AsyncSession, threshold_minutes: int = 60) -> bool:
    """
    Returns True if no articles have been ingested in the last threshold_minutes.
    Used to trigger alerts.
    """
    result = await session.execute(
        text("""
            SELECT EXTRACT(EPOCH FROM (NOW() - MAX(fetched_at)))/60.0
            FROM articles
        """)
    )
    lag = result.scalar()
    if lag is None:
        return True  # No articles at all
    return float(lag) > threshold_minutes
