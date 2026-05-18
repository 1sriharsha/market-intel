"""Sources endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db
from models.schemas import SourceFeedRead

router = APIRouter()


@router.get("", response_model=list[SourceFeedRead])
async def list_sources(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT id, name, feed_type, url, tier, fetch_interval_minutes,
                   last_fetched_at, last_error, is_active, article_count
            FROM source_feeds ORDER BY tier, name
        """)
    )
    rows = result.fetchall()
    return [dict(zip(result.keys(), row)) for row in rows]


@router.patch("/{source_id}")
async def update_source(
    source_id: str,
    is_active: bool | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Enable or disable a source feed."""
    result = await db.execute(
        text("SELECT id FROM source_feeds WHERE id = :id"),
        {"id": source_id},
    )
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Source not found")

    if is_active is not None:
        await db.execute(
            text("UPDATE source_feeds SET is_active = :active WHERE id = :id"),
            {"active": is_active, "id": source_id},
        )

    return {"id": source_id, "updated": True}
