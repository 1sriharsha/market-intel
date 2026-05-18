"""FRED, BLS macro data fetcher — bootstraps full history, syncs daily."""
from datetime import datetime, timezone, date
from typing import Optional

from config.log import get_logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import settings
from config.sources import FRED_SERIES
from models.schemas import MacroSnapshot

log = get_logger(__name__)


def _get_fred_client():
    from fredapi import Fred
    return Fred(api_key=None)   # FRED API is free without key — key increases rate limits


async def bootstrap_macro_series(series_ids: list[str], session: AsyncSession) -> None:
    """
    Fetch complete history for all configured FRED series.
    Writes to macro_data. Idempotent — safe to re-run.
    """
    import asyncio
    loop = asyncio.get_event_loop()

    for series_cfg in FRED_SERIES:
        if series_ids and series_cfg["id"] not in series_ids:
            continue

        series_id = series_cfg["id"]
        series_name = series_cfg["name"]
        frequency = series_cfg["frequency"]

        try:
            df = await loop.run_in_executor(None, _fetch_fred_series, series_id)
            if df is None or df.empty:
                log.warning("macro.bootstrap.empty", series_id=series_id)
                continue

            rows = [
                {
                    "series_id": series_id,
                    "date": idx.date() if hasattr(idx, "date") else idx,
                    "value": float(val),
                    "series_name": series_name,
                    "frequency": frequency,
                }
                for idx, val in df.items()
                if val is not None and not (hasattr(val, "__float__") and __import__("math").isnan(float(val)))
            ]

            if rows:
                await session.execute(
                    text("""
                        INSERT INTO macro_data (series_id, date, value, series_name, frequency)
                        VALUES (:series_id, :date, :value, :series_name, :frequency)
                        ON CONFLICT (series_id, date) DO UPDATE SET value = EXCLUDED.value
                    """),
                    rows,
                )
                log.info("macro.bootstrap.done", series_id=series_id, rows=len(rows))
        except Exception as e:
            log.error("macro.bootstrap.error", series_id=series_id, error=str(e))


def _fetch_fred_series(series_id: str):
    """Synchronous FRED fetch — run in executor."""
    fred = _get_fred_client()
    return fred.get_series(series_id)


async def sync_macro_updates(session: AsyncSession) -> None:
    """Fetch latest values for all configured series since last sync. Runs daily at 5 AM ET."""
    import asyncio
    loop = asyncio.get_event_loop()

    for series_cfg in FRED_SERIES:
        series_id = series_cfg["id"]
        try:
            result = await session.execute(
                text("SELECT MAX(date) FROM macro_data WHERE series_id = :s"),
                {"s": series_id},
            )
            last_date = result.scalar()

            df = await loop.run_in_executor(
                None, _fetch_fred_series_since, series_id, last_date
            )
            if df is None or df.empty:
                continue

            rows = [
                {
                    "series_id": series_id,
                    "date": idx.date() if hasattr(idx, "date") else idx,
                    "value": float(val),
                    "series_name": series_cfg["name"],
                    "frequency": series_cfg["frequency"],
                }
                for idx, val in df.items()
                if val is not None
            ]
            if rows:
                await session.execute(
                    text("""
                        INSERT INTO macro_data (series_id, date, value, series_name, frequency)
                        VALUES (:series_id, :date, :value, :series_name, :frequency)
                        ON CONFLICT (series_id, date) DO UPDATE SET value = EXCLUDED.value
                    """),
                    rows,
                )
                log.info("macro.sync.done", series_id=series_id, new_rows=len(rows))
        except Exception as e:
            log.warning("macro.sync.error", series_id=series_id, error=str(e))


def _fetch_fred_series_since(series_id: str, since_date):
    fred = _get_fred_client()
    if since_date:
        return fred.get_series(series_id, observation_start=str(since_date))
    return fred.get_series(series_id)


async def get_macro_snapshot(dt: datetime, session: AsyncSession) -> MacroSnapshot:
    """
    Returns a MacroSnapshot for a given datetime — no look-ahead bias.
    Uses latest available value for each series as-of the given date.
    """
    target_date = dt.date() if hasattr(dt, "date") else dt

    series_map = {
        "FEDFUNDS": "fed_funds_rate",
        "CPIAUCSL": "cpi",
        "T10Y2Y": "t10y2y_spread",
        "VIXCLS": "vix",
        "DGS10": "dgs10",
        "UNRATE": "unrate",
        "DCOILWTICO": "oil_price",
        "M2SL": "m2",
        "BAMLH0A0HYM2": "hy_spread",
    }

    snapshot_data: dict = {"as_of": dt}
    for series_id, field_name in series_map.items():
        result = await session.execute(
            text("""
                SELECT value FROM macro_data
                WHERE series_id = :s AND date <= :d
                ORDER BY date DESC LIMIT 1
            """),
            {"s": series_id, "d": target_date},
        )
        row = result.fetchone()
        snapshot_data[field_name] = float(row[0]) if row else None

    return MacroSnapshot(**snapshot_data)
