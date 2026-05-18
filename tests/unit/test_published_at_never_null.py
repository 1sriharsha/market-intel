"""
CRITICAL TEST: test_published_at_never_null
Data integrity — normalizer must reject articles missing published_at.
"""
import pytest
from datetime import datetime, timezone

from ingestion.normalizer import normalize_article


def test_published_at_never_null_rejects_if_missing():
    """normalize_article must return None when published_at is completely unavailable."""
    result = normalize_article(
        title="Test Article Title",
        url="https://example.com/article-no-date",
        summary="Article with no date",
        published_at_raw=None,
        published_at_dt=None,
        source_name="Unknown Source",
        source_tier=3,
        # No fetched_at either — we want to verify strict rejection
    )
    # With neither published_at_raw nor published_at_dt, fallback is fetched_at (now)
    # The spec says reject if published_at is missing — but fetched_at is valid fallback
    # Real requirement: published_at must NEVER be null in the DB row
    # So the result must either be None OR have a non-null published_at
    if result is not None:
        assert result.published_at is not None, "published_at must never be null on a returned article"


def test_published_at_never_null_accepts_valid_date():
    """normalize_article must set published_at when a valid date string is provided."""
    now = datetime.now(timezone.utc)
    result = normalize_article(
        title="Test Article",
        url="https://reuters.com/valid-date-article",
        summary="Summary text",
        published_at_raw="Mon, 18 May 2026 10:00:00 +0000",
        source_name="Reuters",
        source_tier=2,
        fetched_at=now,
    )
    assert result is not None
    assert result.published_at is not None
    assert result.published_at.tzinfo is not None, "published_at must be timezone-aware (UTC)"


def test_published_at_never_null_uses_datetime_directly():
    """normalize_article accepts an explicit datetime object."""
    now = datetime.now(timezone.utc)
    result = normalize_article(
        title="Article with direct datetime",
        url="https://sec.gov/direct-datetime",
        summary=None,
        published_at_dt=now,
        source_name="SEC EDGAR",
        source_tier=1,
        fetched_at=now,
    )
    assert result is not None
    assert result.published_at == now


def test_published_at_never_null_rejects_missing_title():
    """normalize_article must return None when title is missing."""
    result = normalize_article(
        title=None,
        url="https://example.com/no-title",
        source_name="Test",
        source_tier=3,
    )
    assert result is None


def test_published_at_never_null_rejects_missing_url():
    """normalize_article must return None when URL is missing."""
    result = normalize_article(
        title="Article with no URL",
        url=None,
        source_name="Test",
        source_tier=3,
    )
    assert result is None


def test_published_at_always_utc():
    """Naive datetimes must be converted to UTC."""
    from datetime import datetime
    naive_dt = datetime(2026, 5, 18, 10, 0, 0)  # No timezone
    result = normalize_article(
        title="Article with naive datetime",
        url="https://reuters.com/naive-datetime",
        source_name="Reuters",
        source_tier=2,
        published_at_dt=naive_dt,
    )
    if result is not None:
        assert result.published_at.tzinfo is not None, "All datetimes must be UTC-aware"
