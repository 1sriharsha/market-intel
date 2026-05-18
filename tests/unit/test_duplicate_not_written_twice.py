"""
CRITICAL TEST: test_duplicate_not_written_twice
Data integrity — the two-stage dedup pipeline must prevent duplicate writes.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timezone

from ingestion.normalizer import normalize_article, article_id
from ingestion.deduplicator import deduplicate_batch
from models.schemas import RawArticle


def make_article(url: str, title: str = "Test Article") -> RawArticle:
    now = datetime.now(timezone.utc)
    return RawArticle(
        id=article_id(url),
        title=title,
        summary="Test summary about markets",
        url=url,
        source_name="Reuters",
        source_tier=2,
        tickers=["SPY"],
        topics=["markets"],
        published_at=now,
        fetched_at=now,
    )


@pytest.mark.anyio
async def test_duplicate_not_written_twice_url_dedup(mock_redis, mock_session):
    """Stage 1: Same URL submitted twice — second must be suppressed."""
    url = "https://reuters.com/article-dedup-test-1"
    article1 = make_article(url)
    article2 = make_article(url)

    # Simulate: first call = not seen, second call = seen
    mock_redis.exists.side_effect = [0, 1]

    batch = [article1, article2]
    novel = await deduplicate_batch(batch, mock_session)

    assert len(novel) == 1, "Duplicate URL must be suppressed — only 1 novel article expected"
    assert novel[0].url == url


@pytest.mark.anyio
async def test_duplicate_not_written_twice_semantic_dedup(mock_redis, mock_session):
    """Stage 2: Two articles with different URLs but same semantic content must deduplicate."""
    url1 = "https://reuters.com/article-a"
    url2 = "https://ap.com/article-b"  # Same story, different source

    article1 = make_article(url1, title="Fed Raises Rates 50 Basis Points in Historic Move")
    article2 = make_article(url2, title="Federal Reserve Hikes Rates by 50bps at FOMC Meeting")

    # Stage 1: both URLs are new (not in Redis)
    mock_redis.exists.return_value = 0

    # Stage 2: mock embedding + similarity — article2 matches article1
    fixed_vec = [0.1] * 1536

    mock_result = MagicMock()
    mock_result.fetchone = MagicMock(return_value=("existing_id",))

    mock_session.execute = AsyncMock(return_value=mock_result)

    with patch("ingestion.deduplicator.AsyncOpenAI") as mock_openai_cls:
        mock_client = AsyncMock()
        mock_embed_resp = MagicMock()
        mock_embed_resp.data = [MagicMock(embedding=fixed_vec)]
        mock_client.embeddings.create = AsyncMock(return_value=mock_embed_resp)
        mock_openai_cls.return_value = mock_client

        batch = [article1, article2]
        novel = await deduplicate_batch(batch, mock_session)

    # Both should be suppressed if semantic match found for article1 too,
    # OR at minimum the second one. We assert at most 1 makes it through.
    assert len(novel) <= 1, "Semantically duplicate articles must not both pass dedup"


@pytest.mark.anyio
async def test_unique_articles_all_pass_dedup(mock_redis, mock_session):
    """Three completely different articles must all pass."""
    mock_redis.exists.return_value = 0

    mock_result = MagicMock()
    mock_result.fetchone = MagicMock(return_value=None)  # No semantic match
    mock_session.execute = AsyncMock(return_value=mock_result)

    articles = [
        make_article("https://reuters.com/article-x", "Fed Rate Decision"),
        make_article("https://wsj.com/article-y", "Apple Earnings Beat"),
        make_article("https://ft.com/article-z", "Oil Price Spike"),
    ]

    with patch("ingestion.deduplicator.AsyncOpenAI") as mock_openai_cls:
        mock_client = AsyncMock()
        mock_embed_resp = MagicMock()
        mock_embed_resp.data = [MagicMock(embedding=[0.1] * 1536)]
        mock_client.embeddings.create = AsyncMock(return_value=mock_embed_resp)
        mock_openai_cls.return_value = mock_client

        novel = await deduplicate_batch(articles, mock_session)

    assert len(novel) == 3, "All 3 unique articles must pass dedup"
