"""feedparser-based RSS/Atom ingestion for all tier 1, 2A, 2B, 2C sources."""
import asyncio
from datetime import datetime, timezone
from typing import Optional

import httpx

try:
    import feedparser as feedparser
except ImportError:
    feedparser = None  # type: ignore
from config.log import get_logger

from config.settings import settings
from config.sources import SourceFeed, ALL_RSS_FEEDS, GOOGLE_NEWS_MACRO_QUERIES, build_google_news_url
from config.watchlist import EQUITY_TICKERS
from ingestion.normalizer import normalize_article
from models.schemas import RawArticle

log = get_logger(__name__)

_FETCH_TIMEOUT = 30
_SEMAPHORE_LIMIT = 10


class FeedFetchError(Exception):
    pass


class FeedParseError(Exception):
    pass


def _build_ticker_google_news_feeds() -> list[SourceFeed]:
    """Dynamically build Google News RSS feeds for all watchlist tickers."""
    feeds = []
    for ticker in EQUITY_TICKERS[:50]:   # top 50 tickers to stay within reasonable volume
        feeds.append(SourceFeed(
            id=f"gnews_{ticker.lower()}",
            name=f"Google News — {ticker}",
            feed_type="rss",
            url=build_google_news_url(ticker),
            tier=2,
            fetch_interval_minutes=15,
            topics=["markets"],
        ))
    return feeds


def _build_macro_google_news_feeds() -> list[SourceFeed]:
    feeds = []
    for item in GOOGLE_NEWS_MACRO_QUERIES:
        slug = item["query"][:30].replace(" ", "_").lower()
        feeds.append(SourceFeed(
            id=f"gnews_macro_{slug}",
            name=f"Google News — {item['query'][:40]}",
            feed_type="rss",
            url=build_google_news_url(item["query"]),
            tier=2,
            fetch_interval_minutes=15,
            topics=item["topics"],
        ))
    return feeds


def get_all_rss_feeds() -> list[SourceFeed]:
    return ALL_RSS_FEEDS + _build_macro_google_news_feeds() + _build_ticker_google_news_feeds()


async def fetch_feed(feed: SourceFeed) -> list[RawArticle]:
    """
    Fetch one RSS feed. Returns normalized RawArticle objects.
    Raises FeedFetchError on network failure, FeedParseError on malformed XML.
    Never raises on empty feed.
    """
    now = datetime.now(timezone.utc)

    try:
        async with httpx.AsyncClient(timeout=_FETCH_TIMEOUT, follow_redirects=True) as client:
            resp = await client.get(feed.url, headers={"User-Agent": "MIOS/1.0 (market intelligence)"})
            resp.raise_for_status()
            content = resp.text
    except httpx.HTTPError as e:
        raise FeedFetchError(f"HTTP error fetching {feed.id}: {e}") from e
    except Exception as e:
        raise FeedFetchError(f"Network error fetching {feed.id}: {e}") from e

    try:
        parsed = feedparser.parse(content)
    except Exception as e:
        raise FeedParseError(f"Parse error for {feed.id}: {e}") from e

    if parsed.bozo and not parsed.entries:
        raise FeedParseError(f"Malformed feed {feed.id}: {parsed.bozo_exception}")

    articles: list[RawArticle] = []
    for entry in parsed.entries:
        article = normalize_rss_item(entry, feed, fetched_at=now)
        if article is not None:
            articles.append(article)

    return articles


def normalize_rss_item(
    item,
    feed: SourceFeed,
    fetched_at: datetime | None = None,
) -> RawArticle | None:
    """
    Convert a feedparser entry to a RawArticle.
    Never raises — returns None on invalid items.
    """
    try:
        url = getattr(item, "link", None) or item.get("id")
        title = getattr(item, "title", None) or item.get("title")
        if not url or not title:
            return None

        # Summary: prefer summary field, fall back to content
        summary = item.get("summary") or item.get("description")
        if not summary and item.get("content"):
            try:
                summary = item["content"][0].get("value")
            except (IndexError, KeyError, TypeError):
                pass

        published_raw = (
            item.get("published")
            or item.get("updated")
            or item.get("dc_date")
        )

        return normalize_article(
            title=title,
            url=url,
            summary=summary,
            published_at_raw=published_raw,
            source_name=feed.name,
            source_tier=feed.tier,
            source_feed_id=feed.id,
            topics=list(feed.topics),
            fetched_at=fetched_at,
        )
    except Exception as e:
        log.debug("rss.normalize_failed", feed_id=feed.id, error=str(e))
        return None


async def fetch_all_feeds(feeds: list[SourceFeed] | None = None) -> list[RawArticle]:
    """
    Fetch all active RSS feeds concurrently (semaphore=10).
    Aggregates results. Logs per-feed errors without halting others.
    """
    if feeds is None:
        feeds = get_all_rss_feeds()

    semaphore = asyncio.Semaphore(_SEMAPHORE_LIMIT)
    results: list[RawArticle] = []

    async def _fetch_one(feed: SourceFeed) -> list[RawArticle]:
        async with semaphore:
            try:
                articles = await fetch_feed(feed)
                log.debug("rss.fetched", feed_id=feed.id, count=len(articles))
                return articles
            except (FeedFetchError, FeedParseError) as e:
                log.warning("rss.feed_error", feed_id=feed.id, error=str(e))
                return []
            except Exception as e:
                log.error("rss.unexpected_error", feed_id=feed.id, error=str(e))
                return []

    batches = await asyncio.gather(*[_fetch_one(f) for f in feeds])
    for batch in batches:
        results.extend(batch)

    log.info("rss.fetch_complete", feeds=len(feeds), articles=len(results))
    return results
