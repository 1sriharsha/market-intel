"""Intelligence endpoints."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db
from models.schemas import IntelligenceObjectRead

router = APIRouter()


@router.get("", response_model=list[IntelligenceObjectRead])
async def list_intelligence(
    significance_level: Optional[str] = Query(None),
    ticker: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List intelligence objects with optional filters."""
    conditions = []
    params: dict = {"limit": limit}

    if significance_level:
        conditions.append("significance_level = :significance_level")
        params["significance_level"] = significance_level
    if ticker:
        conditions.append(":ticker = ANY(tickers)")
        params["ticker"] = ticker

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    result = await db.execute(
        text(f"""
            SELECT id, created_at, trigger_type, tickers, topics, summary, why_it_matters,
                   historical_context, contradictions, risks, unknowns, confidence_score,
                   confidence_explanation, significance_level, source_article_ids,
                   llm_model, llm_input_tokens, llm_output_tokens, delivered_at
            FROM intelligence_objects
            {where}
            ORDER BY created_at DESC
            LIMIT :limit
        """),
        params,
    )
    rows = result.fetchall()
    return [dict(zip(result.keys(), row)) for row in rows]


@router.get("/{object_id}", response_model=IntelligenceObjectRead)
async def get_intelligence(object_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("SELECT * FROM intelligence_objects WHERE id = :id"),
        {"id": object_id},
    )
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Intelligence object not found")
    return dict(zip(result.keys(), row))


@router.post("/trigger")
async def trigger_intelligence_cycle(db: AsyncSession = Depends(get_db)):
    """Manually trigger an intelligence cycle."""
    from workers.intelligence_tasks import trigger_intelligence_manual
    task = trigger_intelligence_manual.delay()
    return {"task_id": task.id, "status": "queued"}
