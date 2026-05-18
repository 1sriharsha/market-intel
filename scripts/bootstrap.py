"""
One-time historical data bootstrap. Resumable via bootstrap_state table.
Run: python scripts/bootstrap.py [--tickers AAPL MSFT] [--reset]
"""
import argparse
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow running from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

import structlog
from sqlalchemy import text

log = structlog.get_logger()

BOOTSTRAP_STEPS = [
    "prices",
    "macro",
    "edgar_feeds_seeded",
    "gdelt",
]


async def get_step_status(step: str, session) -> str:
    result = await session.execute(
        text("SELECT status FROM bootstrap_state WHERE step = :step"),
        {"step": step},
    )
    row = result.fetchone()
    return row[0] if row else "pending"


async def mark_step(step: str, status: str, session, progress_key: str | None = None, error: str | None = None):
    await session.execute(
        text("""
            INSERT INTO bootstrap_state (step, status, progress_key, completed_at, error, updated_at)
            VALUES (:step, :status, :progress_key,
                    CASE WHEN :status = 'completed' THEN NOW() ELSE NULL END,
                    :error, NOW())
            ON CONFLICT (step) DO UPDATE SET
                status = EXCLUDED.status,
                progress_key = EXCLUDED.progress_key,
                completed_at = EXCLUDED.completed_at,
                error = EXCLUDED.error,
                updated_at = EXCLUDED.updated_at
        """),
        {"step": step, "status": status, "progress_key": progress_key, "error": error},
    )


async def bootstrap(tickers: list[str] | None = None, reset: bool = False):
    from storage.database import get_session, engine
    from models.db import Base
    from ingestion.price_fetcher import bootstrap_price_history
    from ingestion.macro_fetcher import bootstrap_macro_series
    from config.watchlist import ALL_TICKERS
    from config.sources import FRED_SERIES

    target_tickers = tickers or ALL_TICKERS

    async with get_session() as session:
        if reset:
            for step in BOOTSTRAP_STEPS:
                await mark_step(step, "pending", session)
            log.info("bootstrap.reset")

        # Step 1: Price history
        step_status = await get_step_status("prices", session)
        if step_status != "completed":
            log.info("bootstrap.step.prices.start", tickers=len(target_tickers))
            await mark_step("prices", "in_progress", session)
            try:
                await bootstrap_price_history(target_tickers, session)
                await mark_step("prices", "completed", session)
                log.info("bootstrap.step.prices.done")
            except Exception as e:
                await mark_step("prices", "failed", session, error=str(e))
                log.error("bootstrap.step.prices.failed", error=str(e))
        else:
            log.info("bootstrap.step.prices.skip")

        # Step 2: Macro history
        step_status = await get_step_status("macro", session)
        if step_status != "completed":
            log.info("bootstrap.step.macro.start")
            await mark_step("macro", "in_progress", session)
            try:
                series_ids = [s["id"] for s in FRED_SERIES]
                await bootstrap_macro_series(series_ids, session)
                await mark_step("macro", "completed", session)
                log.info("bootstrap.step.macro.done")
            except Exception as e:
                await mark_step("macro", "failed", session, error=str(e))
                log.error("bootstrap.step.macro.failed", error=str(e))
        else:
            log.info("bootstrap.step.macro.skip")

        # Step 3: Seed source_feeds table from config
        step_status = await get_step_status("edgar_feeds_seeded", session)
        if step_status != "completed":
            log.info("bootstrap.step.feeds.start")
            await mark_step("edgar_feeds_seeded", "in_progress", session)
            try:
                await seed_source_feeds(session)
                await mark_step("edgar_feeds_seeded", "completed", session)
                log.info("bootstrap.step.feeds.done")
            except Exception as e:
                await mark_step("edgar_feeds_seeded", "failed", session, error=str(e))
                log.error("bootstrap.step.feeds.failed", error=str(e))
        else:
            log.info("bootstrap.step.feeds.skip")

        # Step 4: GDELT (optional, requires GCP)
        step_status = await get_step_status("gdelt", session)
        if step_status != "completed":
            from config.settings import settings
            if settings.google_cloud_project:
                log.info("bootstrap.step.gdelt.start")
                await mark_step("gdelt", "in_progress", session)
                try:
                    from ingestion.edgar_fetcher import fetch_gdelt_events
                    rows = await fetch_gdelt_events(target_tickers, start_year=2010, session=session)
                    if rows:
                        await _insert_gdelt_events(rows, session)
                    await mark_step("gdelt", "completed", session)
                    log.info("bootstrap.step.gdelt.done", rows=len(rows))
                except Exception as e:
                    await mark_step("gdelt", "failed", session, error=str(e))
                    log.error("bootstrap.step.gdelt.failed", error=str(e))
            else:
                log.info("bootstrap.step.gdelt.skip", reason="no GCP project configured")
                await mark_step("gdelt", "completed", session, progress_key="skipped")
        else:
            log.info("bootstrap.step.gdelt.skip")

    log.info("bootstrap.complete")


async def seed_source_feeds(session):
    """Insert all configured RSS feeds into source_feeds table."""
    from config.sources import ALL_RSS_FEEDS, API_SOURCES

    all_feeds = ALL_RSS_FEEDS + API_SOURCES
    for feed in all_feeds:
        await session.execute(
            text("""
                INSERT INTO source_feeds (id, name, feed_type, url, tier, fetch_interval_minutes)
                VALUES (:id, :name, :feed_type, :url, :tier, :interval)
                ON CONFLICT (id) DO NOTHING
            """),
            {
                "id": feed.id,
                "name": feed.name,
                "feed_type": feed.feed_type,
                "url": feed.url,
                "tier": feed.tier,
                "interval": feed.fetch_interval_minutes,
            },
        )


async def _insert_gdelt_events(rows: list[dict], session) -> None:
    from datetime import date as date_type
    for row in rows:
        try:
            event_date_raw = row.get("event_date")
            if isinstance(event_date_raw, str):
                event_date = datetime.strptime(event_date_raw[:8], "%Y%m%d").date()
            else:
                event_date = event_date_raw

            await session.execute(
                text("""
                    INSERT INTO historical_events
                        (gdelt_event_id, event_date, actor1, actor2, event_code,
                         goldstein_scale, avg_tone, num_mentions, num_sources, source_url)
                    VALUES
                        (:gdelt_event_id, :event_date, :actor1, :actor2, :event_code,
                         :goldstein_scale, :avg_tone, :num_mentions, :num_sources, :source_url)
                    ON CONFLICT (gdelt_event_id) DO NOTHING
                """),
                {
                    "gdelt_event_id": row.get("gdelt_event_id"),
                    "event_date": event_date,
                    "actor1": row.get("actor1"),
                    "actor2": row.get("actor2"),
                    "event_code": row.get("event_code"),
                    "goldstein_scale": row.get("goldstein_scale"),
                    "avg_tone": row.get("avg_tone"),
                    "num_mentions": row.get("num_mentions"),
                    "num_sources": row.get("num_sources"),
                    "source_url": row.get("source_url"),
                },
            )
        except Exception as e:
            log.warning("bootstrap.gdelt.insert_failed", error=str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap MIOS historical data")
    parser.add_argument("--tickers", nargs="+", help="Specific tickers to bootstrap")
    parser.add_argument("--reset", action="store_true", help="Reset all steps and restart")
    args = parser.parse_args()
    asyncio.run(bootstrap(tickers=args.tickers, reset=args.reset))
