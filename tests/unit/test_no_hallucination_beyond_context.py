"""
CRITICAL TEST: test_no_hallucination_beyond_context
Intelligence quality — Claude output must not contain tickers not present in context.
"""
import json
import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from tests.conftest import NOW


@pytest.mark.anyio
async def test_hallucinated_tickers_stripped(mock_session, fixed_context, monkeypatch):
    """
    If Claude returns tickers not in context_package.tickers, they must be stripped.
    Hallucination event must be logged.
    """
    import intelligence.engine as engine_module

    # Claude output includes TSLA which is NOT in context tickers [SPY, TLT, GLD]
    hallucinated_json = json.dumps({
        "summary": "Fed raised rates. Apple and Tesla impacted.",
        "why_it_matters": "Higher rates hurt growth stocks.",
        "historical_context": "Similar to 2018.",
        "contradictions": "None detected",
        "risks": "Pivot risk",
        "unknowns": "Future rate path",
        "confidence_score": 0.75,
        "confidence_explanation": "Tier 2A confirmed",
        "significance_level": "high",
        "tickers": ["SPY", "TLT", "TSLA", "NVDA"],  # TSLA + NVDA are NOT in context
        "topics": ["monetary_policy"],
    })

    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=hallucinated_json)]
    mock_response.usage = MagicMock(input_tokens=1000, output_tokens=400)

    mock_client = AsyncMock()
    mock_client.messages.create = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(engine_module, "_anthropic_client", mock_client)

    mock_result = MagicMock()
    mock_result.fetchone = MagicMock(return_value=(uuid.uuid4(),))
    mock_session.execute = AsyncMock(return_value=mock_result)

    obj = await engine_module.generate_intelligence(fixed_context, mock_session, trigger="test")

    assert obj is not None
    output_tickers = obj["tickers"]

    # TSLA and NVDA must NOT be in output — not in context
    assert "TSLA" not in output_tickers, "TSLA was hallucinated — must be stripped"
    assert "NVDA" not in output_tickers, "NVDA was hallucinated — must be stripped"

    # SPY and TLT ARE in context — must be preserved
    assert "SPY" in output_tickers or "TLT" in output_tickers, \
        "Valid context tickers must be preserved"


@pytest.mark.anyio
async def test_all_valid_tickers_preserved(mock_session, fixed_context, monkeypatch):
    """
    Tickers that ARE in context must not be stripped.
    """
    import intelligence.engine as engine_module

    valid_json = json.dumps({
        "summary": "Fed raised rates. SPY and TLT reacted.",
        "why_it_matters": "Rate sensitive assets moved.",
        "historical_context": "2018 analogue.",
        "contradictions": "None detected",
        "risks": "Pivot risk",
        "unknowns": "Duration unknown",
        "confidence_score": 0.80,
        "confidence_explanation": "Strong source confirmation",
        "significance_level": "high",
        "tickers": ["SPY", "TLT"],  # Both are in context [SPY, TLT, GLD]
        "topics": ["monetary_policy"],
    })

    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=valid_json)]
    mock_response.usage = MagicMock(input_tokens=1000, output_tokens=400)

    mock_client = AsyncMock()
    mock_client.messages.create = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(engine_module, "_anthropic_client", mock_client)

    mock_result = MagicMock()
    mock_result.fetchone = MagicMock(return_value=(uuid.uuid4(),))
    mock_session.execute = AsyncMock(return_value=mock_result)

    obj = await engine_module.generate_intelligence(fixed_context, mock_session, trigger="test")

    assert obj is not None
    assert "SPY" in obj["tickers"], "SPY is in context and must be preserved"
    assert "TLT" in obj["tickers"], "TLT is in context and must be preserved"


@pytest.mark.anyio
async def test_empty_confidence_explanation_rejected(mock_session, fixed_context, monkeypatch):
    """
    Intelligence object with empty confidence_explanation must be rejected entirely.
    """
    import intelligence.engine as engine_module

    bad_json = json.dumps({
        "summary": "Something happened.",
        "why_it_matters": "It matters.",
        "historical_context": "History.",
        "contradictions": "None detected",
        "risks": "Risk",
        "unknowns": "Unknown",
        "confidence_score": 0.5,
        "confidence_explanation": "",   # EMPTY — must be rejected
        "significance_level": "medium",
        "tickers": ["SPY"],
        "topics": ["markets"],
    })

    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=bad_json)]
    mock_response.usage = MagicMock(input_tokens=500, output_tokens=200)

    mock_client = AsyncMock()
    mock_client.messages.create = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(engine_module, "_anthropic_client", mock_client)

    obj = await engine_module.generate_intelligence(fixed_context, mock_session, trigger="test")

    assert obj is None, "Intelligence with empty confidence_explanation must be rejected"
