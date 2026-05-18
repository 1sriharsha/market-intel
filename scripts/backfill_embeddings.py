"""
Embed all bootstrapped articles that haven't been embedded yet.
Run overnight after bootstrap. Resumable — skips already-embedded articles.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import structlog
from sqlalchemy import text

log = structlog.get_logger()


async def backfill():
    from enrichment.embedder import embed_batch
    from storage.database import get_session
    from config.settings import settings

    batch_size = settings.embedding_batch_size

    async with get_session() as session:
        result = await session.execute(
            text("SELECT COUNT(*) FROM articles WHERE is_embedded = false")
        )
        total = result.scalar() or 0
        log.info("backfill.start", total_pending=total)

        processed = 0
        while True:
            result = await session.execute(
                text("""
                    SELECT id FROM articles
                    WHERE is_embedded = false
                    ORDER BY published_at DESC
                    LIMIT :batch_size
                """),
                {"batch_size": batch_size},
            )
            ids = [row[0] for row in result.fetchall()]
            if not ids:
                break

            await embed_batch(ids, session, batch_size=batch_size)
            processed += len(ids)
            log.info("backfill.progress", processed=processed, total=total)

    log.info("backfill.complete", processed=processed)


if __name__ == "__main__":
    asyncio.run(backfill())
