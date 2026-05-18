"""
CRITICAL TEST: test_intelligence_cites_source_ids
Intelligence quality — every generated intelligence object must cite the articles it was built from.
"""
import json
import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from tests.conftest import FIXED_CLAUDE_JSON, NOW, FIXED_ARTICLE


@pytest.mark.anyio
async def test_intelligence_cites_source_ids(mock_anthropic, mock_session, fixed_context):
    """
    IntelligenceObject generated from a context package must have
    non-empty source_article_ids that match the articles provided.
    """
    from intelligence.engine import generate_intelligence

    # Mock DB write to return a UUID
    mock_result = MagicMock()
    mock_result.fetchone = MagicMock(return_value=(uuid.uuid4(),))
    mock_session.execute = AsyncMock(return_value=mock_result)

    obj = await generate_intelligence(fixed_context, mock_session, trigger="test")

    assert obj is not None, "generate_intelligence must return an object"
    assert "source_article_ids" in obj, "source_article_ids field must be present"
    assert len(obj["source_article_ids"]) > 0, "source_article_ids must not be empty"

    # Verify the IDs come from the provided articles
    context_article_ids = {a["id"] for a in fixed_context.articles}
    for cited_id in obj["source_article_ids"]:
        assert cited_id in context_article_ids, (
            f"source_article_id '{cited_id}' not in context — orphaned intelligence object"
        )


@pytest.mark.anyio
async def test_intelligence_object_never_orphaned(mock_anthropic, mock_session, fixed_context):
    """Intelligence object with empty articles in context must not be generated."""
    from intelligence.engine import generate_intelligence
    from models.schemas import ContextPackage

    empty_context = ContextPackage(
        articles=[],   # No articles
        tickers=[],
        topics=[],
        price_movements=[],
        macro_snapshot=fixed_context.macro_snapshot,
        historical_analogues=[],
        assembled_at=NOW,
    )

    obj = await generate_intelligence(empty_context, mock_session, trigger="test")
    assert obj is None, "Intelligence must not be generated with no source articles"


@pytest.mark.anyio
async def test_intelligence_source_ids_written_to_db(mock_anthropic, mock_session, fixed_context):
    """The DB INSERT for intelligence objects must include source_article_ids."""
    from intelligence.engine import generate_intelligence

    mock_result = MagicMock()
    mock_result.fetchone = MagicMock(return_value=(uuid.uuid4(),))
    execute_calls = []

    async def capture_execute(query, params=None):
        execute_calls.append({"query": str(query), "params": params})
        return mock_result

    mock_session.execute = capture_execute

    obj = await generate_intelligence(fixed_context, mock_session, trigger="test")

    # Find the INSERT call
    insert_calls = [c for c in execute_calls if "INSERT INTO intelligence_objects" in c["query"]]
    assert len(insert_calls) > 0, "Must INSERT to intelligence_objects table"

    insert_params = insert_calls[0]["params"]
    assert insert_params is not None
    assert "source_article_ids" in insert_params
    assert len(insert_params["source_article_ids"]) > 0
