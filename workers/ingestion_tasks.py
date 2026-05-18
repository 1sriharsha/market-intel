"""Celery tasks wrapping all ingestion operations."""
import asyncio
from datetime import datetime, timezone, timedelta

from config.log import get_logger

from workers.celery_app import app

log = get_logger(__name__)


def _run_async(coro):
    """Run an async coroutine from a sync Celery task."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@app.task(name="workers.ingestion_tasks.run_rss_ingestion", bind=True, max_retries=3)
def run_rss_ingestion(self):
    """Fetch all RSS feeds, deduplicate, write novel articles to DB."""
    try:
        return _run_async(_rss_ingestion_async())
    except Exception as exc:
        log.error("task.rss_ingestion.failed", error=str(exc))
        raise self.retry(exc=exc, countdown=60)


async def _rss_ingestion_async():
    from ingestion.rss_fetcher import fetch_all_feeds
    from ingestion.deduplicator import deduplicate_batch
    from ingestion.normalizer import article_id
    from enrichment.ticker_extractor import extract_tickers
    from intelligence.signal_scorer import compute_novelty_score
    from storage.database import get_session
    from sqlalchemy import text
    from config.watchlist import EQUITY_TICKERS

    async with get_session() as session:
        articles = await fetch_all_feeds()
        if not articles:
            return {"ingested": 0}

        novel = await deduplicate_batch(articles, session)

        written = 0
        embed_ids = []

        for article in novel:
            # Extract tickers
            full_text = f"{article.title} {article.summary or ''}"
            extracted_tickers = extract_tickers(full_text)
            article.tickers = extracted_tickers

            # Compute novelty against recent articles
            result = await session.execute(
                text("""
                    SELECT title, summary, tickers, topics FROM articles
                    WHERE published_at > NOW() - INTERVAL '6 hours'
                    ORDER BY published_at DESC LIMIT 50
                """)
            )
            recent = [{"title": r[0], "summary": r[1], "tickers": r[2], "topics": r[3]}
                      for r in result.fetchall()]
            novelty = compute_novelty_score(
                {"tickers": article.tickers, "topics": article.topics}, recent
            )

            try:
                await session.execute(
                    text("""
                        INSERT INTO articles
                            (id, title, summary, url, source_name, source_tier, source_feed_id,
                             tickers, topics, published_at, fetched_at, raw_content, novelty_score)
                        VALUES
                            (:id, :title, :summary, :url, :source_name, :source_tier, :source_feed_id,
                             :tickers, :topics, :published_at, :fetched_at, :raw_content, :novelty_score)
                        ON CONFLICT (url) DO NOTHING
                    """),
                    {
                        "id": article.id,
                        "title": article.title,
                        "summary": article.summary,
                        "url": article.url,
                        "source_name": article.source_name,
                        "source_tier": article.source_tier,
                        "source_feed_id": article.source_feed_id,
                        "tickers": article.tickers,
                        "topics": article.topics,
                        "published_at": article.published_at,
                        "fetched_at": article.fetched_at,
                        "raw_content": article.raw_content,
                        "novelty_score": novelty,
                    },
                )
                written += 1
                embed_ids.append(article.id)

                # Update feed article count
                if article.source_feed_id:
                    await session.execute(
                        text("""
                            UPDATE source_feeds
                            SET article_count = article_count + 1, last_fetched_at = NOW()
                            WHERE id = :id
                        """),
                        {"id": article.source_feed_id},
                    )
            except Exception as e:
                log.warning("ingestion.write_failed", article_id=article.id, error=str(e))

        # Trigger enrichment for new articles
        if embed_ids:
            run_enrichment_pipeline.delay(embed_ids)

        log.info("ingestion.rss.complete", written=written, total=len(articles))
        return {"ingested": written}


@app.task(name="workers.ingestion_tasks.run_edgar_ingestion", bind=True, max_retries=3)
def run_edgar_ingestion(self):
    try:
        return _run_async(_edgar_ingestion_async())
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


async def _edgar_ingestion_async():
    from ingestion.edgar_fetcher import poll_edgar_rss
    from ingestion.deduplicator import deduplicate_batch
    from storage.database import get_session
    from sqlalchemy import text

    async with get_session() as session:
        articles = await poll_edgar_rss()
        novel = await deduplicate_batch(articles, session)

        written = 0
        for article in novel:
            try:
                await session.execute(
                    text("""
                        INSERT INTO articles
                            (id, title, summary, url, source_name, source_tier,
                             source_feed_id, tickers, topics, published_at, fetched_at)
                        VALUES
                            (:id, :title, :summary, :url, :source_name, :source_tier,
                             :source_feed_id, :tickers, :topics, :published_at, :fetched_at)
                        ON CONFLICT (url) DO NOTHING
                    """),
                    article.model_dump(),
                )
                written += 1
            except Exception as e:
                log.warning("ingestion.edgar.write_failed", error=str(e))

        log.info("ingestion.edgar.complete", written=written)
        return {"ingested": written}


@app.task(name="workers.ingestion_tasks.run_api_ingestion", bind=True, max_retries=2)
def run_api_ingestion(self):
    try:
        return _run_async(_api_ingestion_async())
    except Exception as exc:
        raise self.retry(exc=exc, countdown=300)


async def _api_ingestion_async():
    from ingestion.api_fetcher import fetch_finnhub_news, fetch_marketaux_news, fetch_alpha_vantage_news
    from ingestion.deduplicator import deduplicate_batch
    from config.watchlist import EQUITY_TICKERS
    from storage.database import get_session
    from sqlalchemy import text

    from_dt = datetime.now(timezone.utc) - timedelta(hours=2)
    async with get_session() as session:
        finnhub = await fetch_finnhub_news(EQUITY_TICKERS[:20], from_dt)
        marketaux = await fetch_marketaux_news(EQUITY_TICKERS[:10])
        av = await fetch_alpha_vantage_news()

        all_articles = finnhub + marketaux + av
        novel = await deduplicate_batch(all_articles, session)

        written = 0
        for article in novel:
            try:
                await session.execute(
                    text("""
                        INSERT INTO articles
                            (id, title, summary, url, source_name, source_tier,
                             source_feed_id, tickers, topics, published_at, fetched_at)
                        VALUES
                            (:id, :title, :summary, :url, :source_name, :source_tier,
                             :source_feed_id, :tickers, :topics, :published_at, :fetched_at)
                        ON CONFLICT (url) DO NOTHING
                    """),
                    article.model_dump(),
                )
                written += 1
            except Exception as e:
                log.warning("ingestion.api.write_failed", error=str(e))

        log.info("ingestion.api.complete", written=written)
        return {"ingested": written}


@app.task(name="workers.ingestion_tasks.run_enrichment_pipeline")
def run_enrichment_pipeline(article_ids: list[str]):
    """Trigger enrichment after ingestion — called internally."""
    from workers.enrichment_tasks import run_article_enrichment
    run_article_enrichment.delay(article_ids)


@app.task(name="workers.ingestion_tasks.run_feed_health_check")
def run_feed_health_check():
    """Check feed health and update source_feeds table."""
    return _run_async(_feed_health_async())


async def _feed_health_async():
    from monitoring.health_checker import check_feed_health
    await check_feed_health()
