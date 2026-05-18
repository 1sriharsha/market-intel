"""Celery tasks wrapping enrichment operations."""
import asyncio

from config.log import get_logger

from workers.celery_app import app

log = get_logger(__name__)


def _run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@app.task(name="workers.enrichment_tasks.run_article_enrichment", bind=True, max_retries=2)
def run_article_enrichment(self, article_ids: list[str]):
    """Embed + score significance + compute price reactions for new articles."""
    try:
        return _run_async(_enrichment_async(article_ids))
    except Exception as exc:
        log.error("task.enrichment.failed", error=str(exc))
        raise self.retry(exc=exc, countdown=120)


async def _enrichment_async(article_ids: list[str]):
    from enrichment.embedder import embed_batch
    from enrichment.price_reactor import compute_and_store_price_reactions
    from intelligence.signal_scorer import score_significance
    from storage.database import get_session
    from sqlalchemy import text

    async with get_session() as session:
        await embed_batch(article_ids, session)

        result = await session.execute(
            text("""
                SELECT id, title, summary, source_name, source_tier, tickers, topics,
                       published_at, novelty_score
                FROM articles WHERE id = ANY(:ids)
            """),
            {"ids": article_ids},
        )
        articles = [dict(zip(result.keys(), row)) for row in result.fetchall()]

        for article in articles:
            sig_score = score_significance([article])
            await session.execute(
                text("UPDATE articles SET significance_score = :score WHERE id = :id"),
                {"score": sig_score, "id": article["id"]},
            )

            tickers = article.get("tickers") or []
            published_at = article.get("published_at")
            if tickers and published_at:
                await compute_and_store_price_reactions(
                    article["id"], tickers, published_at, session
                )

    log.info("enrichment.complete", articles=len(articles))
    return {"enriched": len(articles)}


@app.task(name="workers.enrichment_tasks.run_price_sync")
def run_price_sync():
    """Nightly price sync for all watchlist tickers."""
    return _run_async(_price_sync_async())


async def _price_sync_async():
    from ingestion.price_fetcher import sync_daily_prices
    from config.watchlist import ALL_TICKERS
    from storage.database import get_session

    async with get_session() as session:
        await sync_daily_prices(ALL_TICKERS, session)
    return {"status": "ok"}


@app.task(name="workers.enrichment_tasks.run_macro_sync")
def run_macro_sync():
    """Daily macro data sync from FRED."""
    return _run_async(_macro_sync_async())


async def _macro_sync_async():
    from ingestion.macro_fetcher import sync_macro_updates
    from storage.database import get_session

    async with get_session() as session:
        await sync_macro_updates(session)
    return {"status": "ok"}
