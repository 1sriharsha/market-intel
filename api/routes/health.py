"""Health and status endpoints."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db
from models.schemas import HealthResponse, SystemStatus

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))


@router.get("/status", response_model=SystemStatus)
async def status(db: AsyncSession = Depends(get_db)):
    """Ingestion lag, feed health, embedding backlog, last intelligence run."""

    # Ingestion lag: minutes since last article was fetched
    lag_result = await db.execute(
        text("SELECT EXTRACT(EPOCH FROM (NOW() - MAX(fetched_at)))/60.0 FROM articles")
    )
    lag_minutes = lag_result.scalar()

    # Embedding backlog
    backlog_result = await db.execute(
        text("SELECT COUNT(*) FROM articles WHERE is_embedded = false")
    )
    embedding_backlog = backlog_result.scalar() or 0

    # Last intelligence run
    last_intel_result = await db.execute(
        text("SELECT MAX(created_at) FROM intelligence_objects")
    )
    last_intel = last_intel_result.scalar()

    # Feed health: feeds with last_fetched_at within 2x their interval
    feeds_result = await db.execute(
        text("""
            SELECT
                COUNT(*) FILTER (WHERE is_active = true) as total,
                COUNT(*) FILTER (
                    WHERE is_active = true
                    AND last_fetched_at > NOW() - (fetch_interval_minutes * 2 * INTERVAL '1 minute')
                ) as healthy
            FROM source_feeds
        """)
    )
    feeds_row = feeds_result.fetchone()
    feeds_total = feeds_row[0] if feeds_row else 0
    feeds_healthy = feeds_row[1] if feeds_row else 0

    # Articles last 24h
    articles_result = await db.execute(
        text("SELECT COUNT(*) FROM articles WHERE fetched_at > NOW() - INTERVAL '24 hours'")
    )
    articles_24h = articles_result.scalar() or 0

    # Intelligence objects today
    intel_today_result = await db.execute(
        text("SELECT COUNT(*) FROM intelligence_objects WHERE created_at > NOW() - INTERVAL '24 hours'")
    )
    intel_today = intel_today_result.scalar() or 0

    # Alerts sent today
    from storage.redis_client import get_daily_counter
    alerts_today = await get_daily_counter("telegram_alerts")

    return SystemStatus(
        ingestion_lag_minutes=float(lag_minutes) if lag_minutes else None,
        embedding_backlog=int(embedding_backlog),
        last_intelligence_run=last_intel,
        feeds_healthy=int(feeds_healthy),
        feeds_total=int(feeds_total),
        articles_last_24h=int(articles_24h),
        intelligence_objects_today=int(intel_today),
        alerts_sent_today=int(alerts_today),
    )
