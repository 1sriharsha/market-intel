"""SEC EDGAR RSS + GDELT BigQuery historical event fetcher."""
from datetime import datetime, timezone
from typing import Optional

import httpx
from config.log import get_logger

from config.settings import settings
from config.watchlist import EQUITY_TICKERS
from ingestion.normalizer import normalize_article
from models.schemas import RawArticle

log = get_logger(__name__)

# EDGAR filing type → topic mapping
FILING_TOPIC_MAP: dict[str, str] = {
    "8-K": "material_event",
    "10-Q": "earnings",
    "10-K": "earnings",
    "SC 13G": "insider_activity",
    "SC 13D": "insider_activity",
    "4": "insider_activity",
    "S-1": "ipo",
    "424B4": "ipo",
    "DEF 14A": "corporate_action",
}

EDGAR_RSS_BASE = "https://www.sec.gov/cgi-bin/browse-edgar"


async def poll_edgar_rss(tickers: list[str] | None = None) -> list[RawArticle]:
    """
    Poll EDGAR RSS feed for recent filings from watchlist companies.
    Maps EDGAR filing types to article topics.
    Runs every 15 minutes.
    """
    import feedparser

    filing_types = ["8-K", "10-Q", "10-K", "4", "SC 13G", "SC 13D"]
    articles: list[RawArticle] = []
    now = datetime.now(timezone.utc)

    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        for filing_type in filing_types:
            url = (
                f"{EDGAR_RSS_BASE}?action=getcurrent&type={filing_type}"
                f"&dateb=&owner=include&count=40&output=atom"
            )
            try:
                resp = await client.get(url, headers={"User-Agent": "MIOS/1.0 research@example.com"})
                resp.raise_for_status()
                parsed = feedparser.parse(resp.text)
            except Exception as e:
                log.warning("edgar.rss.fetch_error", filing_type=filing_type, error=str(e))
                continue

            topic = FILING_TOPIC_MAP.get(filing_type, "regulatory")

            for entry in parsed.entries:
                entry_url = getattr(entry, "link", None)
                title = getattr(entry, "title", None)
                if not entry_url or not title:
                    continue

                # Filter by watchlist ticker if specified
                if tickers:
                    title_upper = title.upper()
                    if not any(t in title_upper for t in tickers):
                        continue

                article = normalize_article(
                    title=title,
                    url=entry_url,
                    summary=getattr(entry, "summary", None),
                    published_at_raw=getattr(entry, "updated", None) or getattr(entry, "published", None),
                    source_name="SEC EDGAR",
                    source_tier=1,
                    source_feed_id=f"sec_edgar_{filing_type.lower().replace(' ', '_')}",
                    topics=[topic],
                    fetched_at=now,
                )
                if article:
                    articles.append(article)

    log.info("edgar.rss.complete", articles=len(articles))
    return articles


async def fetch_gdelt_events(
    tickers: list[str],
    start_year: int = 2010,
    session=None,
) -> list[dict]:
    """
    Query GDELT via Google BigQuery for structured historical events.
    Requires GOOGLE_CLOUD_PROJECT env var.
    Runs once during historical bootstrap.
    Writes to historical_events table.
    """
    if not settings.google_cloud_project:
        log.warning("edgar.gdelt.no_gcp_project")
        return []

    from google.cloud import bigquery
    import asyncio

    loop = asyncio.get_event_loop()

    # Build actor filter from tickers and company names
    from config.watchlist import COMPANY_NAME_OVERRIDES
    actor_names = list({
        name for name, ticker in COMPANY_NAME_OVERRIDES.items()
        if ticker in tickers and name is not None
    })

    macro_terms = ["FEDERAL RESERVE", "TREASURY", "CONGRESS", "SEC", "INFLATION",
                   "INTEREST RATE", "RECESSION", "FEDERAL OPEN MARKET"]

    all_terms = actor_names + macro_terms
    if not all_terms:
        return []

    actor_conditions = " OR ".join(
        [f"UPPER(Actor1Name) LIKE '%{name.upper()}%'" for name in all_terms[:20]]
    )

    query = f"""
    SELECT
        CAST(GLOBALID AS INT64) as gdelt_event_id,
        CAST(SQLDATE AS STRING) as event_date,
        Actor1Name as actor1,
        Actor2Name as actor2,
        EventCode as event_code,
        GoldsteinScale as goldstein_scale,
        AvgTone as avg_tone,
        NumMentions as num_mentions,
        NumSources as num_sources,
        SOURCEURL as source_url
    FROM `gdelt-bq.gdeltv2.events`
    WHERE YEAR(CAST(SQLDATE AS DATE FORMAT 'YYYYMMDD')) >= {start_year}
      AND ({actor_conditions})
    LIMIT 50000
    """

    try:
        client = bigquery.Client(project=settings.google_cloud_project)
        results = await loop.run_in_executor(None, lambda: list(client.query(query).result()))
        log.info("gdelt.query.complete", rows=len(results))
        return [dict(r) for r in results]
    except Exception as e:
        log.error("gdelt.query.error", error=str(e))
        return []
