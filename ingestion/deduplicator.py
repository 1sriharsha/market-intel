"""Two-stage deduplication: URL hash (Redis) then semantic (pgvector)."""
import hashlib
from datetime import datetime, timezone, timedelta
from typing import TYPE_CHECKING

from config.log import get_logger

from config.settings import settings
from models.schemas import RawArticle
from storage.redis_client import is_url_seen, set_url_seen

try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None  # type: ignore

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

log = get_logger(__name__)


def _url_hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()


async def is_duplicate_url(url: str) -> bool:
    """O(1) Redis lookup — primary dedup gate."""
    return await is_url_seen(_url_hash(url))


async def mark_url_seen(url: str) -> None:
    await set_url_seen(_url_hash(url))


async def is_duplicate_content(
    article: RawArticle,
    session: "AsyncSession",
    window_hours: int | None = None,
) -> bool:
    """
    Semantic duplicate check via pgvector cosine similarity.
    Only runs after URL check passes (slower).
    Returns True if a near-duplicate exists.
    """
    from sqlalchemy import text

    if AsyncOpenAI is None:
        log.debug("dedup.openai_unavailable", article_id=article.id)
        return False

    hours = window_hours or settings.semantic_dedup_window_hours
    threshold = settings.semantic_dedup_similarity_threshold

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    input_text = f"{article.title} {article.summary or ''}"[:8192]

    try:
        resp = await client.embeddings.create(
            model=settings.embedding_model,
            input=input_text,
        )
        vec = resp.data[0].embedding
    except Exception as e:
        log.warning("dedup.embed_failed", error=str(e))
        return False

    # Format vector as pgvector literal
    vec_str = "[" + ",".join(f"{v:.6f}" for v in vec) + "]"
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    # Query for cosine similarity above threshold — scope to same tickers if possible
    ticker_filter = ""
    if article.tickers:
        ticker_filter = "AND a.tickers && :tickers"

    sql = text(f"""
        SELECT e.article_id
        FROM embeddings e
        JOIN articles a ON a.id = e.article_id
        WHERE a.published_at > :cutoff
          {ticker_filter}
          AND 1 - (e.embedding <=> :vec::vector) > :threshold
        LIMIT 1
    """)

    params: dict = {"cutoff": cutoff, "vec": vec_str, "threshold": threshold}
    if article.tickers:
        params["tickers"] = article.tickers

    try:
        result = await session.execute(sql, params)
        row = result.fetchone()
        if row:
            log.debug("dedup.semantic_match", article_id=article.id, matched=row[0])
            return True
    except Exception as e:
        log.warning("dedup.semantic_query_failed", error=str(e))

    return False


async def deduplicate_batch(
    articles: list[RawArticle],
    session: "AsyncSession",
) -> list[RawArticle]:
    """
    Run full dedup pipeline on a batch.
    URL check first (fast), content check second (slow, only on URL-unique items).
    Returns only novel articles. Logs suppression counts per feed.
    """
    suppressed_url = 0
    suppressed_semantic = 0
    novel: list[RawArticle] = []
    url_unique: list[RawArticle] = []

    for article in articles:
        if await is_duplicate_url(article.url):
            suppressed_url += 1
        else:
            url_unique.append(article)

    for article in url_unique:
        if await is_duplicate_content(article, session):
            suppressed_semantic += 1
        else:
            novel.append(article)
            await mark_url_seen(article.url)

    if suppressed_url or suppressed_semantic:
        log.info(
            "dedup.batch_result",
            total=len(articles),
            novel=len(novel),
            suppressed_url=suppressed_url,
            suppressed_semantic=suppressed_semantic,
        )

    return novel
