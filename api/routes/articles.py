"""Articles endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db
from models.schemas import ArticleRead

router = APIRouter()


@router.get("", response_model=list[ArticleRead])
async def list_articles(
    ticker: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    source_tier: Optional[int] = Query(None),
    unprocessed_only: bool = Query(False),
    min_significance: Optional[float] = Query(None),
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
):
    conditions = []
    params: dict = {"limit": limit}

    if ticker:
        conditions.append(":ticker = ANY(tickers)")
        params["ticker"] = ticker
    if topic:
        conditions.append(":topic = ANY(topics)")
        params["topic"] = topic
    if source_tier is not None:
        conditions.append("source_tier = :source_tier")
        params["source_tier"] = source_tier
    if unprocessed_only:
        conditions.append("is_processed = false")
    if min_significance is not None:
        conditions.append("significance_score >= :min_significance")
        params["min_significance"] = min_significance

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    result = await db.execute(
        text(f"""
            SELECT id, title, summary, url, source_name, source_tier, tickers, topics,
                   published_at, significance_score, novelty_score, is_processed, is_embedded
            FROM articles
            {where}
            ORDER BY published_at DESC
            LIMIT :limit
        """),
        params,
    )
    rows = result.fetchall()
    return [dict(zip(result.keys(), row)) for row in rows]
