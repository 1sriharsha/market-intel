"""
Test fixtures: mock DB, Redis, Claude stub, fixed IntelligenceObject.
All unit tests use no external dependencies.
"""
import json
import uuid
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from models.schemas import (
    RawArticle, MacroSnapshot, ContextPackage, PricePoint,
    HistoricalAnalogue, IntelligenceObjectCreate,
)


# Restrict anyio async tests to asyncio backend only (trio not installed)
@pytest.fixture
def anyio_backend():
    return "asyncio"


# ---------------------------------------------------------------------------
# Fixed test data
# ---------------------------------------------------------------------------

NOW = datetime(2026, 5, 18, 12, 0, 0, tzinfo=timezone.utc)

FIXED_ARTICLE = {
    "id": "abc123def456" * 4,
    "title": "Federal Reserve Raises Interest Rates by 50 Basis Points",
    "summary": "The Federal Reserve raised interest rates by 50 basis points at today's FOMC meeting.",
    "url": "https://reuters.com/test-article-1",
    "source_name": "Reuters",
    "source_tier": 2,
    "tickers": ["SPY", "TLT", "GLD"],
    "topics": ["monetary_policy", "macro"],
    "published_at": NOW - timedelta(hours=1),
    "significance_score": 85.0,
    "novelty_score": 75.0,
    "is_processed": False,
    "is_embedded": True,
}

FIXED_INTEL_OBJECT = {
    "id": str(uuid.uuid4()),
    "created_at": NOW,
    "trigger_type": "scheduled",
    "tickers": ["SPY", "TLT"],
    "topics": ["monetary_policy"],
    "summary": "Fed raised rates 50bps, signaling continued tightening stance.",
    "why_it_matters": "Higher rates pressure equity valuations and strengthen dollar.",
    "historical_context": "Similar to 2018 tightening cycle when SPY fell 20%.",
    "contradictions": "None detected",
    "risks": "Potential pivot if unemployment rises above 5%",
    "unknowns": "Pace of future hikes unclear",
    "confidence_score": 0.82,
    "confidence_explanation": "Multiple Tier 2A sources confirmed; macro data consistent.",
    "significance_level": "high",
    "source_article_ids": ["abc123def456" * 4],
    "llm_model": "claude-sonnet-4-5",
    "llm_input_tokens": 1200,
    "llm_output_tokens": 450,
    "delivered_at": None,
}

FIXED_MACRO_SNAPSHOT = MacroSnapshot(
    as_of=NOW,
    fed_funds_rate=5.25,
    cpi=311.0,
    t10y2y_spread=-0.5,
    vix=18.5,
    dgs10=4.3,
    unrate=3.9,
    oil_price=78.5,
    m2=21000.0,
    hy_spread=3.8,
)


# ---------------------------------------------------------------------------
# Mock database session
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    return session


# ---------------------------------------------------------------------------
# Mock Redis client
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_redis(monkeypatch):
    redis_mock = AsyncMock()
    redis_mock.exists = AsyncMock(return_value=0)
    redis_mock.setex = AsyncMock(return_value=True)
    redis_mock.get = AsyncMock(return_value=None)
    redis_mock.incr = AsyncMock(return_value=1)
    redis_mock.expire = AsyncMock(return_value=True)
    redis_mock.expireat = AsyncMock(return_value=True)
    redis_mock.pipeline = MagicMock(return_value=AsyncMock(
        execute=AsyncMock(return_value=[1, True]),
        incr=MagicMock(),
        expireat=MagicMock(),
        __aenter__=AsyncMock(return_value=AsyncMock(
            execute=AsyncMock(return_value=[1, True])
        )),
        __aexit__=AsyncMock(return_value=None),
    ))

    import storage.redis_client as rc
    monkeypatch.setattr(rc, "_redis_client", redis_mock)
    return redis_mock


# ---------------------------------------------------------------------------
# Claude stub — returns fixed IntelligenceObject JSON
# ---------------------------------------------------------------------------

FIXED_CLAUDE_JSON = json.dumps({
    "summary": "Fed raised rates 50bps, signaling continued tightening stance.",
    "why_it_matters": "Higher rates pressure equity valuations and strengthen dollar.",
    "historical_context": "Similar to 2018 tightening cycle.",
    "contradictions": "None detected",
    "risks": "Potential pivot if unemployment rises",
    "unknowns": "Pace of future hikes unclear",
    "confidence_score": 0.82,
    "confidence_explanation": "Multiple Tier 2A sources confirmed; macro data consistent.",
    "significance_level": "high",
    "tickers": ["SPY", "TLT"],
    "topics": ["monetary_policy"],
})


@pytest.fixture
def mock_anthropic(monkeypatch):
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=FIXED_CLAUDE_JSON)]
    mock_response.usage = MagicMock(input_tokens=1200, output_tokens=450)

    mock_client = AsyncMock()
    mock_client.messages.create = AsyncMock(return_value=mock_response)

    import intelligence.engine as engine_module
    monkeypatch.setattr(engine_module, "_anthropic_client", mock_client)
    return mock_client


# ---------------------------------------------------------------------------
# Fixed context package
# ---------------------------------------------------------------------------

@pytest.fixture
def fixed_context():
    return ContextPackage(
        articles=[FIXED_ARTICLE],
        tickers=["SPY", "TLT", "GLD"],
        topics=["monetary_policy", "macro"],
        price_movements=[
            PricePoint(ticker="SPY", date=NOW.date(), close=520.0),
            PricePoint(ticker="TLT", date=NOW.date(), close=92.0),
        ],
        macro_snapshot=FIXED_MACRO_SNAPSHOT,
        historical_analogues=[],
        regime=None,
        active_contradictions=[],
        assembled_at=NOW,
    )
