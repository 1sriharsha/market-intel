"""OpenAI text-embedding-3-small generation and storage."""
import asyncio
from datetime import datetime, timezone
import hashlib

from config.log import get_logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings

log = get_logger(__name__)

_client = None


def _get_client():
    global _client
    if _client is None:
        from openai import AsyncOpenAI
        _client = AsyncOpenAI(api_key=settings.openai_api_key)
    return _client


def _content_hash(text_input: str) -> str:
    return hashlib.sha256(text_input.encode()).hexdigest()


def _build_embed_input(title: str, summary: str | None) -> str:
    parts = [title]
    if summary:
        parts.append(summary)
    combined = " ".join(parts)
    # Truncate to roughly max token budget (4 chars ≈ 1 token)
    max_chars = settings.embedding_max_tokens * 4
    return combined[:max_chars]


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def _embed_texts(texts: list[str]) -> list[list[float]]:
    client = _get_client()
    resp = await client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )
    return [item.embedding for item in resp.data]


async def embed_article(article_id: str, session: AsyncSession) -> None:
    """
    Fetch article from DB, embed title+summary, write to embeddings table.
    Updates articles.is_embedded = true. Retries 3x on API failure.
    """
    result = await session.execute(
        text("SELECT title, summary FROM articles WHERE id = :id"),
        {"id": article_id},
    )
    row = result.fetchone()
    if not row:
        log.warning("embedder.article_not_found", article_id=article_id)
        return

    title, summary = row
    input_text = _build_embed_input(title, summary)
    content_hash = _content_hash(input_text)

    # Skip if already embedded with same content
    existing = await session.execute(
        text("SELECT id FROM embeddings WHERE article_id = :id AND content_hash = :h"),
        {"id": article_id, "h": content_hash},
    )
    if existing.fetchone():
        return

    try:
        vectors = await _embed_texts([input_text])
        vec = vectors[0]
    except Exception as e:
        log.error("embedder.api_failed", article_id=article_id, error=str(e))
        return

    vec_str = "[" + ",".join(f"{v:.8f}" for v in vec) + "]"

    await session.execute(
        text("""
            INSERT INTO embeddings (article_id, embedding, embedding_model, chunk_index, content_hash)
            VALUES (:article_id, :embedding::vector, :model, 0, :content_hash)
            ON CONFLICT DO NOTHING
        """),
        {
            "article_id": article_id,
            "embedding": vec_str,
            "model": settings.embedding_model,
            "content_hash": content_hash,
        },
    )

    await session.execute(
        text("UPDATE articles SET is_embedded = true WHERE id = :id"),
        {"id": article_id},
    )


async def embed_batch(
    article_ids: list[str],
    session: AsyncSession,
    batch_size: int | None = None,
) -> None:
    """
    Batch embedding — minimizes OpenAI API round trips.
    Max 2048 inputs per API call. Handles partial failures without halting batch.
    """
    bs = batch_size or settings.embedding_batch_size
    max_per_call = settings.embedding_max_inputs_per_call

    # Fetch all articles needing embedding
    result = await session.execute(
        text("""
            SELECT a.id, a.title, a.summary
            FROM articles a
            WHERE a.id = ANY(:ids) AND a.is_embedded = false
        """),
        {"ids": article_ids},
    )
    rows = result.fetchall()
    if not rows:
        return

    successes = 0
    failures = 0

    for i in range(0, len(rows), min(bs, max_per_call)):
        chunk = rows[i : i + min(bs, max_per_call)]
        texts = [_build_embed_input(r[1], r[2]) for r in chunk]
        hashes = [_content_hash(t) for t in texts]

        try:
            vectors = await _embed_texts(texts)
        except Exception as e:
            log.error("embedder.batch_api_failed", batch_start=i, error=str(e))
            failures += len(chunk)
            continue

        for (article_id, _, _), vec, content_hash in zip(chunk, vectors, hashes):
            vec_str = "[" + ",".join(f"{v:.8f}" for v in vec) + "]"
            try:
                await session.execute(
                    text("""
                        INSERT INTO embeddings (article_id, embedding, embedding_model, chunk_index, content_hash)
                        VALUES (:article_id, :embedding::vector, :model, 0, :content_hash)
                        ON CONFLICT DO NOTHING
                    """),
                    {
                        "article_id": article_id,
                        "embedding": vec_str,
                        "model": settings.embedding_model,
                        "content_hash": content_hash,
                    },
                )
                await session.execute(
                    text("UPDATE articles SET is_embedded = true WHERE id = :id"),
                    {"id": article_id},
                )
                successes += 1
            except Exception as e:
                log.warning("embedder.write_failed", article_id=article_id, error=str(e))
                failures += 1

        await session.commit()

    log.info("embedder.batch_complete", successes=successes, failures=failures)
