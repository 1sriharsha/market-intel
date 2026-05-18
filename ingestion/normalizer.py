"""Maps all raw ingestion sources to canonical RawArticle schema."""
import hashlib
import re
from datetime import datetime, timezone
from typing import Optional

from models.schemas import RawArticle

try:
    from bs4 import BeautifulSoup as _BS4
    _HAS_BS4 = True
except ImportError:
    _HAS_BS4 = False


def canonical_url(url: str) -> str:
    """Strip query params that don't affect content identity (tracking params etc)."""
    import urllib.parse
    parsed = urllib.parse.urlparse(url.strip())
    # Drop common tracking params
    _TRACKING = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
                 "ref", "source", "via"}
    qs = urllib.parse.parse_qs(parsed.query, keep_blank_values=False)
    cleaned = {k: v for k, v in qs.items() if k.lower() not in _TRACKING}
    new_query = urllib.parse.urlencode(cleaned, doseq=True)
    return urllib.parse.urlunparse(parsed._replace(query=new_query, fragment=""))


def article_id(url: str) -> str:
    """SHA-256 of canonical URL — stable primary key."""
    return hashlib.sha256(canonical_url(url).encode()).hexdigest()


def strip_html(text: str | None) -> str | None:
    if not text:
        return None
    if _HAS_BS4:
        try:
            soup = _BS4(text, "lxml")
            return soup.get_text(separator=" ", strip=True)[:2000]
        except Exception:
            pass
    return re.sub(r"<[^>]+>", " ", text).strip()[:2000]


def parse_datetime(value: str | None, fallback: datetime | None = None) -> datetime | None:
    """Parse any reasonable date string to a UTC-aware datetime. Returns fallback if unparseable."""
    if not value:
        return fallback
    from email.utils import parsedate_to_datetime
    from dateutil import parser as dateutil_parser

    # Try RFC 2822 (common in RSS)
    try:
        dt = parsedate_to_datetime(value)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass

    # Try dateutil (handles ISO 8601 and many others)
    try:
        dt = dateutil_parser.parse(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass

    return fallback


def normalize_article(
    *,
    title: str | None,
    url: str | None,
    summary: str | None = None,
    raw_content: str | None = None,
    published_at_raw: str | None = None,
    published_at_dt: datetime | None = None,
    source_name: str,
    source_tier: int,
    source_feed_id: str | None = None,
    topics: list[str] | None = None,
    fetched_at: datetime | None = None,
) -> RawArticle | None:
    """
    Produce a canonical RawArticle from any source's raw fields.
    Returns None if required fields are missing or unparseable.
    """
    if not title or not url:
        return None

    clean_url = canonical_url(url)
    if not clean_url:
        return None

    now = datetime.now(timezone.utc)
    fetch_time = fetched_at or now

    # Resolve published_at — reject article if completely unavailable
    pub_dt = published_at_dt
    if pub_dt is None and published_at_raw:
        pub_dt = parse_datetime(published_at_raw, fallback=None)
    if pub_dt is None:
        # Fall back to fetch time only if that's truly all we have
        pub_dt = fetch_time

    if pub_dt is None:
        return None   # strict: published_at must be set

    # Ensure UTC
    if pub_dt.tzinfo is None:
        pub_dt = pub_dt.replace(tzinfo=timezone.utc)
    pub_dt = pub_dt.astimezone(timezone.utc)

    clean_summary = strip_html(summary) or strip_html(raw_content)
    if clean_summary:
        clean_summary = clean_summary[:500]

    return RawArticle(
        id=article_id(clean_url),
        title=title.strip()[:512],
        summary=clean_summary,
        url=clean_url,
        source_name=source_name,
        source_tier=source_tier,
        source_feed_id=source_feed_id,
        tickers=[],
        topics=topics or [],
        published_at=pub_dt,
        fetched_at=fetch_time,
        raw_content=raw_content[:10000] if raw_content else None,
    )
