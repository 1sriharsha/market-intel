"""Compute and persist price reactions for ingested articles."""
from datetime import datetime, timezone

from config.log import get_logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ingestion.price_fetcher import compute_abnormal_return, get_price_at

log = get_logger(__name__)


async def compute_and_store_price_reactions(
    article_id: str,
    tickers: list[str],
    published_at: datetime,
    session: AsyncSession,
) -> None:
    """
    For each ticker mentioned in an article, compute and persist:
    - price at publish
    - price 1d after
    - SPY return same day
    - abnormal return (ticker return - beta * SPY return)
    - reaction label
    """
    if not tickers:
        return

    event_date = published_at.date()

    for ticker in tickers:
        # Skip if already computed
        existing = await session.execute(
            text("SELECT 1 FROM article_ticker_effects WHERE article_id = :a AND ticker = :t"),
            {"a": article_id, "t": ticker},
        )
        if existing.fetchone():
            continue

        price_at_pub = await get_price_at(ticker, published_at, session)
        abnormal = await compute_abnormal_return(ticker, event_date, session)

        price_1d = None
        if abnormal.raw_return is not None and price_at_pub is not None:
            price_1d = price_at_pub * (1 + abnormal.raw_return)

        try:
            await session.execute(
                text("""
                    INSERT INTO article_ticker_effects
                        (article_id, ticker, attribution_method, price_at_publish,
                         price_1h_after, price_1d_after, spy_return_1d,
                         abnormal_return_1d, reaction_label)
                    VALUES
                        (:article_id, :ticker, :attribution_method, :price_at_publish,
                         NULL, :price_1d_after, :spy_return_1d,
                         :abnormal_return_1d, :reaction_label)
                    ON CONFLICT (article_id, ticker) DO NOTHING
                """),
                {
                    "article_id": article_id,
                    "ticker": ticker,
                    "attribution_method": "entity_extract",
                    "price_at_publish": price_at_pub,
                    "price_1d_after": price_1d,
                    "spy_return_1d": abnormal.market_return,
                    "abnormal_return_1d": abnormal.abnormal_return,
                    "reaction_label": abnormal.reaction_label,
                },
            )
        except Exception as e:
            log.warning("price_reactor.write_failed", article_id=article_id,
                        ticker=ticker, error=str(e))
