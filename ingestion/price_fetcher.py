"""yfinance price data — historical bootstrap and daily sync."""
from dataclasses import dataclass
from datetime import date, datetime, timezone, timedelta
from typing import Optional

from config.log import get_logger

try:
    import numpy as np
    import pandas as pd
    import yfinance as yf
except ImportError:
    np = None  # type: ignore
    pd = None  # type: ignore
    yf = None  # type: ignore
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import settings
from models.schemas import AbnormalReturn

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

async def bootstrap_price_history(tickers: list[str], session: AsyncSession) -> None:
    """
    One-time function. Fetches period='max' for each ticker.
    Skips tickers that already have data (idempotent).
    """
    for ticker in tickers:
        result = await session.execute(
            text("SELECT COUNT(*) FROM prices WHERE ticker = :t"), {"t": ticker}
        )
        count = result.scalar()
        if count and count > 0:
            log.info("price.bootstrap.skip", ticker=ticker, rows=count)
            continue

        try:
            df = await _fetch_yfinance(ticker, period="max")
            if df is None or df.empty:
                log.warning("price.bootstrap.empty", ticker=ticker)
                continue
            await _upsert_prices(df, ticker, session)
            log.info("price.bootstrap.done", ticker=ticker, rows=len(df))
        except Exception as e:
            log.error("price.bootstrap.error", ticker=ticker, error=str(e))


async def sync_daily_prices(tickers: list[str], session: AsyncSession) -> None:
    """
    Fetch last 5 trading days for all tickers. Upserts into prices table.
    Handles weekends and market holidays gracefully.
    """
    for ticker in tickers:
        try:
            df = await _fetch_yfinance(ticker, period="5d")
            if df is None or df.empty:
                continue
            await _upsert_prices(df, ticker, session)
            log.debug("price.sync.done", ticker=ticker, rows=len(df))
        except Exception as e:
            log.warning("price.sync.error", ticker=ticker, error=str(e))

    log.info("price.sync.complete", tickers=len(tickers))


async def _fetch_yfinance(ticker: str, period: str = "max") -> pd.DataFrame | None:
    import asyncio
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _fetch_yfinance_sync, ticker, period)


def _fetch_yfinance_sync(ticker: str, period: str) -> pd.DataFrame | None:
    try:
        t = yf.Ticker(ticker)
        df = t.history(period=period, auto_adjust=True)
        if df.empty:
            return None
        df = df.reset_index()
        df.columns = [c.lower() for c in df.columns]
        # Normalize date column
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"]).dt.date
        return df[["date", "open", "high", "low", "close", "volume"]]
    except Exception:
        return None


async def _upsert_prices(df: pd.DataFrame, ticker: str, session: AsyncSession) -> None:
    rows = [
        {
            "ticker": ticker,
            "date": row["date"],
            "open": float(row["open"]) if pd.notna(row["open"]) else None,
            "high": float(row["high"]) if pd.notna(row["high"]) else None,
            "low": float(row["low"]) if pd.notna(row["low"]) else None,
            "close": float(row["close"]) if pd.notna(row["close"]) else None,
            "volume": int(row["volume"]) if pd.notna(row["volume"]) else None,
        }
        for _, row in df.iterrows()
    ]
    if not rows:
        return

    await session.execute(
        text("""
            INSERT INTO prices (ticker, date, open, high, low, close, volume)
            VALUES (:ticker, :date, :open, :high, :low, :close, :volume)
            ON CONFLICT (ticker, date) DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume
        """),
        rows,
    )


# ---------------------------------------------------------------------------
# Price lookup
# ---------------------------------------------------------------------------

async def get_price_at(ticker: str, dt: datetime, session: AsyncSession) -> float | None:
    """
    Returns adjusted close price for a ticker on a given date.
    Returns None if no price available (new company, halt, weekend).
    Uses latest available price up to and including the given date.
    """
    target_date = dt.date() if hasattr(dt, "date") else dt
    result = await session.execute(
        text("""
            SELECT close FROM prices
            WHERE ticker = :ticker AND date <= :d
            ORDER BY date DESC LIMIT 1
        """),
        {"ticker": ticker, "d": target_date},
    )
    row = result.fetchone()
    return float(row[0]) if row and row[0] is not None else None


# ---------------------------------------------------------------------------
# Abnormal return computation
# ---------------------------------------------------------------------------

async def compute_abnormal_return(
    ticker: str,
    event_date: date,
    session: AsyncSession,
    window_days: int = 1,
) -> AbnormalReturn:
    """
    Compute abnormal return relative to SPY for a given ticker and event date.
    Uses 60-day rolling beta regression.
    Returns AbnormalReturn with raw_return, market_return, beta, abnormal_return, reaction_label.
    """
    result = AbnormalReturn(ticker=ticker, event_date=event_date)

    # Fetch 70 days of price data (60 for beta + buffer)
    lookback_start = event_date - timedelta(days=90)
    lookback_end = event_date + timedelta(days=window_days + 2)

    ticker_prices = await _fetch_price_series(ticker, lookback_start, lookback_end, session)
    spy_prices = await _fetch_price_series("SPY", lookback_start, lookback_end, session)

    if len(ticker_prices) < 10 or len(spy_prices) < 10:
        return result

    # Align on date
    df = pd.DataFrame({
        "ticker": ticker_prices,
        "spy": spy_prices,
    }).dropna()

    if len(df) < 10:
        return result

    # Compute daily returns
    df["r_ticker"] = df["ticker"].pct_change()
    df["r_spy"] = df["spy"].pct_change()
    df = df.dropna()

    # Beta via OLS on prior 60 days before event
    prior = df[df.index < event_date].tail(settings.beta_regression_days)
    if len(prior) < 10:
        beta = 1.0
    else:
        cov = prior["r_ticker"].cov(prior["r_spy"])
        var = prior["r_spy"].var()
        beta = cov / var if var > 0 else 1.0

    # Event day return
    event_rows = df[df.index == event_date]
    next_rows = df[df.index > event_date].head(window_days)

    if event_rows.empty or next_rows.empty:
        return result

    # 1-day return: close on event_date+1 vs close on event_date
    price_t0 = float(event_rows["ticker"].iloc[-1])
    price_t1 = float(next_rows["ticker"].iloc[-1])
    spy_t0 = float(event_rows["spy"].iloc[-1])
    spy_t1 = float(next_rows["spy"].iloc[-1])

    raw_return = (price_t1 - price_t0) / price_t0
    market_return = (spy_t1 - spy_t0) / spy_t0
    abnormal = raw_return - beta * market_return

    result.raw_return = raw_return
    result.market_return = market_return
    result.beta = beta
    result.abnormal_return = abnormal
    result.reaction_label = _label_reaction(abnormal)

    return result


async def _fetch_price_series(
    ticker: str,
    start: date,
    end: date,
    session: AsyncSession,
) -> pd.Series:
    result = await session.execute(
        text("SELECT date, close FROM prices WHERE ticker = :t AND date BETWEEN :s AND :e ORDER BY date"),
        {"t": ticker, "s": start, "e": end},
    )
    rows = result.fetchall()
    if not rows:
        return pd.Series(dtype=float)
    s = pd.Series(
        {r[0]: float(r[1]) for r in rows if r[1] is not None},
        dtype=float,
    )
    s.index = pd.to_datetime(s.index)
    return s


def _label_reaction(abnormal_return: float) -> str:
    abs_ar = abs(abnormal_return)
    if abs_ar < 0.005:
        return "none"
    if abs_ar < 0.02:
        return "small"
    if abs_ar < 0.05:
        return "moderate"
    return "large"
