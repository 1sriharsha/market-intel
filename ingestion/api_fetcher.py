"""Structured API sources: Finnhub, Marketaux, Alpha Vantage with rate limiting."""
from datetime import datetime, timezone, timedelta
from typing import Optional

import httpx
from config.log import get_logger

from config.settings import settings
from config.watchlist import EQUITY_TICKERS
from ingestion.normalizer import normalize_article
from models.schemas import RawArticle
from storage.redis_client import check_rate_limit, get_rate_limit_count

log = get_logger(__name__)

_TIMEOUT = 30


# ---------------------------------------------------------------------------
# Finnhub
# ---------------------------------------------------------------------------

async def fetch_finnhub_news(
    tickers: list[str],
    from_dt: datetime,
) -> list[RawArticle]:
    """
    Fetch company news from Finnhub for all watchlist tickers.
    Rate limit: 60 req/min via Redis token bucket.
    Falls back to cached/empty response if rate limit is hit.
    """
    articles: list[RawArticle] = []
    from_str = from_dt.strftime("%Y-%m-%d")
    to_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        for ticker in tickers:
            allowed = await check_rate_limit("finnhub_minute", settings.finnhub_rate_limit_per_minute, 60)
            if not allowed:
                log.warning("api.finnhub.rate_limit_hit", ticker=ticker)
                break

            try:
                resp = await client.get(
                    "https://finnhub.io/api/v1/company-news",
                    params={"symbol": ticker, "from": from_str, "to": to_str,
                            "token": settings.finnhub_api_key},
                )
                resp.raise_for_status()
                items = resp.json()
            except Exception as e:
                log.warning("api.finnhub.fetch_error", ticker=ticker, error=str(e))
                continue

            now = datetime.now(timezone.utc)
            for item in items:
                url = item.get("url")
                if not url:
                    continue
                article = normalize_article(
                    title=item.get("headline"),
                    url=url,
                    summary=item.get("summary"),
                    published_at_dt=datetime.fromtimestamp(item["datetime"], tz=timezone.utc)
                    if item.get("datetime") else None,
                    source_name=item.get("source", "Finnhub"),
                    source_tier=3,
                    source_feed_id="finnhub_company_news",
                    topics=["markets"],
                    fetched_at=now,
                )
                if article:
                    article.tickers = [ticker]
                    articles.append(article)

    log.info("api.finnhub.complete", articles=len(articles))
    return articles


# ---------------------------------------------------------------------------
# Marketaux
# ---------------------------------------------------------------------------

async def fetch_marketaux_news(tickers: list[str]) -> list[RawArticle]:
    """
    Fetch entity-tagged news from Marketaux.
    Rate limit: 100 req/day via Redis daily counter.
    Returns empty list (not error) when daily limit reached.
    """
    count = await get_rate_limit_count("marketaux_day")
    if count >= settings.marketaux_rate_limit_per_day:
        log.info("api.marketaux.daily_limit_reached")
        return []

    articles: list[RawArticle] = []
    symbols = ",".join(tickers[:10])   # Marketaux supports comma-separated, cap at 10

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            allowed = await check_rate_limit("marketaux_day", settings.marketaux_rate_limit_per_day, 86400)
            if not allowed:
                return []

            resp = await client.get(
                "https://api.marketaux.com/v1/news/all",
                params={
                    "symbols": symbols,
                    "filter_entities": "true",
                    "language": "en",
                    "api_token": settings.marketaux_api_key,
                },
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        log.warning("api.marketaux.fetch_error", error=str(e))
        return []

    now = datetime.now(timezone.utc)
    for item in data.get("data", []):
        url = item.get("url")
        if not url:
            continue

        # Extract tickers from entities
        item_tickers = [
            e["symbol"] for e in item.get("entities", [])
            if e.get("type") == "equity" and e.get("symbol")
        ]

        article = normalize_article(
            title=item.get("title"),
            url=url,
            summary=item.get("description"),
            published_at_raw=item.get("published_at"),
            source_name=item.get("source", "Marketaux"),
            source_tier=3,
            source_feed_id="marketaux_news",
            topics=["markets"],
            fetched_at=now,
        )
        if article:
            article.tickers = item_tickers
            articles.append(article)

    log.info("api.marketaux.complete", articles=len(articles))
    return articles


# ---------------------------------------------------------------------------
# Alpha Vantage
# ---------------------------------------------------------------------------

async def fetch_alpha_vantage_news(topics: list[str] | None = None) -> list[RawArticle]:
    """
    Fetch macro and sector news from Alpha Vantage.
    Rate limit: 25 req/day.
    Priority topics: earnings, ipo, mergers_and_acquisitions, financial_markets, economy_macro.
    """
    allowed = await check_rate_limit("alpha_vantage_day", settings.alpha_vantage_rate_limit_per_day, 86400)
    if not allowed:
        log.info("api.alpha_vantage.daily_limit_reached")
        return []

    priority_topics = topics or [
        "earnings", "ipo", "mergers_and_acquisitions", "financial_markets", "economy_macro"
    ]
    articles: list[RawArticle] = []
    now = datetime.now(timezone.utc)

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        for topic in priority_topics[:5]:   # 5 calls max per run
            allowed = await check_rate_limit("alpha_vantage_day", settings.alpha_vantage_rate_limit_per_day, 86400)
            if not allowed:
                break

            try:
                resp = await client.get(
                    "https://www.alphavantage.co/query",
                    params={
                        "function": "NEWS_SENTIMENT",
                        "topics": topic,
                        "sort": "LATEST",
                        "limit": "50",
                        "apikey": settings.alpha_vantage_key,
                    },
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                log.warning("api.alpha_vantage.fetch_error", topic=topic, error=str(e))
                continue

            for item in data.get("feed", []):
                url = item.get("url")
                if not url:
                    continue

                item_tickers = [
                    t["ticker"] for t in item.get("ticker_sentiment", [])
                    if t.get("ticker") and not t["ticker"].startswith("CRYPTO:")
                ]

                article = normalize_article(
                    title=item.get("title"),
                    url=url,
                    summary=item.get("summary"),
                    published_at_raw=item.get("time_published"),
                    source_name=item.get("source", "Alpha Vantage"),
                    source_tier=3,
                    source_feed_id="alpha_vantage_news",
                    topics=[topic.replace("_", " ")],
                    fetched_at=now,
                )
                if article:
                    article.tickers = item_tickers
                    articles.append(article)

    log.info("api.alpha_vantage.complete", articles=len(articles))
    return articles
