"""Telegram delivery — evaluate, format, push. Hard delivery rules enforced in code."""
from datetime import datetime, timezone

from config.log import get_logger

from config.settings import settings
from storage.redis_client import (
    get_daily_counter, increment_daily_counter,
    is_ticker_on_cooldown, set_ticker_cooldown,
)

log = get_logger(__name__)

# Significance emoji indicators
_SIG_EMOJI: dict[str, str] = {
    "critical": "🚨",
    "high": "⚠️",
    "medium": "ℹ️",
    "low": "📌",
}


async def evaluate_delivery(obj: dict) -> bool:
    """
    Returns True if an intelligence object should be pushed to Telegram.

    Hard rules:
    1. significance_level must be critical or high
    2. No more than 1 delivery per ticker per 4-hour window (cooldown)
    3. No more than MAX_DAILY_ALERTS total per day

    Returns False and logs reason if suppressed.
    """
    significance = obj.get("significance_level", "")
    if significance not in ("critical", "high"):
        log.debug("delivery.suppressed.significance", significance=significance, id=obj.get("id"))
        return False

    # Check global daily cap
    daily_count = await get_daily_counter("telegram_alerts")
    if daily_count >= settings.max_daily_alerts:
        log.info("delivery.suppressed.daily_cap", count=daily_count, id=obj.get("id"))
        return False

    # Check per-ticker cooldown — all tickers in obj must be off cooldown
    tickers = obj.get("tickers") or []
    for ticker in tickers:
        if await is_ticker_on_cooldown(ticker):
            log.info("delivery.suppressed.cooldown", ticker=ticker, id=obj.get("id"))
            return False

    return True


async def deliver(obj: dict) -> bool:
    """
    Evaluate, format, and push. Updates cooldowns and counters on success.
    Returns True if message was sent.
    """
    if not await evaluate_delivery(obj):
        return False

    message = format_message(obj)
    success = await push_message(message, settings.telegram_chat_id)

    if success:
        # Update daily counter
        await increment_daily_counter("telegram_alerts")

        # Set cooldown for all tickers
        for ticker in (obj.get("tickers") or []):
            await set_ticker_cooldown(ticker, settings.alert_cooldown_hours)

        log.info("delivery.sent", id=obj.get("id"), tickers=obj.get("tickers"))

    return success


def format_message(obj: dict) -> str:
    """
    Format an IntelligenceObject as a Telegram message.
    Max 3800 characters (Telegram limit is 4096, buffer for safety).
    Never exposes raw LLM output directly — structured format only.
    """
    significance = obj.get("significance_level", "medium")
    emoji = _SIG_EMOJI.get(significance, "📊")
    tickers = obj.get("tickers") or []
    ticker_str = " ".join(f"${t}" for t in tickers) if tickers else "No specific tickers"
    confidence = obj.get("confidence_score")
    conf_str = f"{confidence:.0%}" if confidence is not None else "N/A"
    created = obj.get("created_at")
    time_str = created.strftime("%Y-%m-%d %H:%M UTC") if isinstance(created, datetime) else "N/A"

    parts = [
        f"{emoji} *{significance.upper()} SIGNAL*",
        f"🕐 {time_str}",
        f"📈 {ticker_str}",
        "",
        f"*SUMMARY*",
        obj.get("summary", ""),
        "",
    ]

    why = obj.get("why_it_matters")
    if why:
        parts += ["*WHY IT MATTERS*", why[:600], ""]

    contradictions = obj.get("contradictions")
    if contradictions and contradictions.lower() != "none detected":
        parts += ["*⚡ CONTRADICTIONS*", contradictions[:300], ""]

    historical = obj.get("historical_context")
    if historical:
        parts += ["*📚 HISTORICAL CONTEXT*", historical[:400], ""]

    unknowns = obj.get("unknowns")
    if unknowns:
        parts += ["*❓ UNKNOWNS*", unknowns[:200], ""]

    parts.append(f"*Confidence:* {conf_str}")

    message = "\n".join(parts)

    # Truncate to hard limit
    if len(message) > settings.telegram_max_message_chars:
        message = message[:settings.telegram_max_message_chars - 20] + "\n\n_(truncated)_"

    return message


async def push_message(message: str, chat_id: str) -> bool:
    """
    Send a formatted message to the configured Telegram chat.
    Retries 3x on network failure.
    Logs delivery confirmation or failure.
    Returns True on success.
    """
    from telegram import Bot
    from telegram.error import TelegramError
    import asyncio

    bot = Bot(token=settings.telegram_bot_token)
    last_error: Exception | None = None

    for attempt in range(3):
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="Markdown",
            )
            log.info("telegram.sent", chat_id=chat_id, attempt=attempt + 1)
            return True
        except TelegramError as e:
            last_error = e
            if attempt < 2:
                await asyncio.sleep(2 ** attempt)
        except Exception as e:
            last_error = e
            if attempt < 2:
                await asyncio.sleep(2 ** attempt)

    log.error("telegram.failed", chat_id=chat_id, error=str(last_error))
    return False
