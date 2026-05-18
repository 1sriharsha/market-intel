"""
CRITICAL TEST: test_rate_limit_respected
Operational compliance — Telegram daily cap and ticker cooldowns must be enforced.
"""
import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone

from tests.conftest import FIXED_INTEL_OBJECT, NOW


@pytest.mark.anyio
async def test_telegram_daily_cap_enforced(mock_redis):
    """After MAX_DAILY_ALERTS deliveries, further alerts must be suppressed."""
    from delivery.telegram_bot import evaluate_delivery
    from config.settings import settings

    obj = {**FIXED_INTEL_OBJECT, "significance_level": "high", "tickers": ["AAPL"]}

    with patch("delivery.telegram_bot.get_daily_counter",
               new=AsyncMock(return_value=settings.max_daily_alerts)):
        with patch("delivery.telegram_bot.is_ticker_on_cooldown",
                   new=AsyncMock(return_value=False)):
            result = await evaluate_delivery(obj)

    assert result is False, f"Must suppress when daily_count ({settings.max_daily_alerts}) >= max_daily_alerts"


@pytest.mark.anyio
async def test_telegram_daily_cap_allows_before_limit(mock_redis):
    """Before the cap is reached, delivery must be allowed."""
    from delivery.telegram_bot import evaluate_delivery
    from config.settings import settings

    obj = {**FIXED_INTEL_OBJECT, "significance_level": "high", "tickers": ["AAPL"]}

    with patch("delivery.telegram_bot.get_daily_counter",
               new=AsyncMock(return_value=settings.max_daily_alerts - 1)):
        with patch("delivery.telegram_bot.is_ticker_on_cooldown",
                   new=AsyncMock(return_value=False)):
            result = await evaluate_delivery(obj)

    assert result is True, "Must allow delivery when under daily cap"


@pytest.mark.anyio
async def test_ticker_cooldown_enforced(mock_redis):
    """Ticker on 4-hour cooldown must prevent delivery."""
    from delivery.telegram_bot import evaluate_delivery

    obj = {**FIXED_INTEL_OBJECT, "significance_level": "high", "tickers": ["SPY", "TLT"]}

    with patch("delivery.telegram_bot.get_daily_counter", new=AsyncMock(return_value=0)):
        with patch("delivery.telegram_bot.is_ticker_on_cooldown",
                   new=AsyncMock(return_value=True)):
            result = await evaluate_delivery(obj)

    assert result is False, "Must suppress when any ticker is on cooldown"


@pytest.mark.anyio
async def test_low_significance_always_suppressed(mock_redis):
    """Low and medium significance objects must never be delivered."""
    from delivery.telegram_bot import evaluate_delivery

    with patch("delivery.telegram_bot.get_daily_counter", new=AsyncMock(return_value=0)):
        with patch("delivery.telegram_bot.is_ticker_on_cooldown", new=AsyncMock(return_value=False)):
            for level in ("low", "medium", "suppressed"):
                obj = {**FIXED_INTEL_OBJECT, "significance_level": level}
                result = await evaluate_delivery(obj)
                assert result is False, f"significance_level='{level}' must never be delivered"


@pytest.mark.anyio
async def test_critical_significance_allowed():
    """Critical significance objects must pass delivery check (when under cap, no cooldown)."""
    from delivery.telegram_bot import evaluate_delivery

    obj = {**FIXED_INTEL_OBJECT, "significance_level": "critical", "tickers": ["SPY"]}

    with patch("delivery.telegram_bot.get_daily_counter", new=AsyncMock(return_value=0)):
        with patch("delivery.telegram_bot.is_ticker_on_cooldown", new=AsyncMock(return_value=False)):
            result = await evaluate_delivery(obj)

    assert result is True, "Critical significance with capacity available must be allowed"


@pytest.mark.anyio
async def test_daily_cap_is_exactly_five():
    """Daily cap must be exactly 5 — hardcoded in spec, not arbitrary."""
    from config.settings import settings
    assert settings.max_daily_alerts == 5, "Daily alert cap must be exactly 5 per spec"


@pytest.mark.anyio
async def test_cooldown_is_four_hours():
    """Ticker cooldown must be exactly 4 hours per spec."""
    from config.settings import settings
    assert settings.alert_cooldown_hours == 4, "Ticker cooldown must be exactly 4 hours per spec"
