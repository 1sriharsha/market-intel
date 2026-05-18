"""Pydantic schemas for API responses and internal data transfer objects."""
from datetime import datetime, date
from typing import Optional
import uuid

from pydantic import BaseModel, Field, field_validator, ConfigDict


# ---------------------------------------------------------------------------
# Internal data transfer objects
# ---------------------------------------------------------------------------

class RawArticle(BaseModel):
    """Canonical article representation produced by all normalizers."""
    id: str                          # SHA-256 of canonical URL
    title: str
    summary: str | None = None
    url: str
    source_name: str
    source_tier: int
    source_feed_id: str | None = None
    tickers: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)
    published_at: datetime           # MUST be non-null — reject at normalizer if missing
    fetched_at: datetime
    raw_content: str | None = None


class MacroSnapshot(BaseModel):
    """Point-in-time macro data snapshot — no look-ahead bias."""
    as_of: datetime
    fed_funds_rate: float | None = None
    cpi: float | None = None
    t10y2y_spread: float | None = None
    vix: float | None = None
    dgs10: float | None = None
    unrate: float | None = None
    oil_price: float | None = None
    m2: float | None = None
    hy_spread: float | None = None


class AbnormalReturn(BaseModel):
    ticker: str
    event_date: date
    raw_return: float | None = None
    market_return: float | None = None
    beta: float | None = None
    abnormal_return: float | None = None
    reaction_label: str = "none"


class PricePoint(BaseModel):
    ticker: str
    date: date
    close: float | None = None


class HistoricalAnalogue(BaseModel):
    event_date: date
    event_category: str | None = None
    goldstein_scale: float | None = None
    avg_tone: float | None = None
    tickers_affected: list[str] = Field(default_factory=list)
    similarity_score: float | None = None
    price_reaction_summary: str | None = None


class Contradiction(BaseModel):
    ticker: str | None = None
    description: str
    severity: float = Field(ge=0.0, le=1.0)
    contradiction_type: str


class ContextPackage(BaseModel):
    articles: list[dict]
    tickers: list[str]
    topics: list[str]
    price_movements: list[PricePoint]
    macro_snapshot: MacroSnapshot
    historical_analogues: list[HistoricalAnalogue]
    regime: dict | None = None
    active_contradictions: list[Contradiction] = Field(default_factory=list)
    assembled_at: datetime


# ---------------------------------------------------------------------------
# Intelligence objects
# ---------------------------------------------------------------------------

class IntelligenceObjectCreate(BaseModel):
    trigger_type: str
    tickers: list[str]
    topics: list[str]
    summary: str
    why_it_matters: str | None = None
    historical_context: str | None = None
    contradictions: str | None = None
    risks: str | None = None
    unknowns: str | None = None
    confidence_score: float = Field(ge=0.0, le=1.0)
    confidence_explanation: str
    significance_level: str
    source_article_ids: list[str]
    llm_model: str | None = None
    llm_input_tokens: int | None = None
    llm_output_tokens: int | None = None


class IntelligenceObjectRead(IntelligenceObjectCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    delivered_at: datetime | None = None


# ---------------------------------------------------------------------------
# API response schemas
# ---------------------------------------------------------------------------

class ArticleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    summary: str | None
    url: str
    source_name: str
    source_tier: int
    tickers: list[str]
    topics: list[str]
    published_at: datetime
    significance_score: float | None
    novelty_score: float | None
    is_processed: bool
    is_embedded: bool


class SourceFeedRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    feed_type: str
    url: str | None
    tier: int | None
    fetch_interval_minutes: int
    last_fetched_at: datetime | None
    last_error: str | None
    is_active: bool
    article_count: int


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


class SystemStatus(BaseModel):
    ingestion_lag_minutes: float | None
    embedding_backlog: int
    last_intelligence_run: datetime | None
    feeds_healthy: int
    feeds_total: int
    articles_last_24h: int
    intelligence_objects_today: int
    alerts_sent_today: int
