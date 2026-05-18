"""Celery tasks wrapping intelligence operations."""
import asyncio

from config.log import get_logger

from workers.celery_app import app

log = get_logger(__name__)


def _run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@app.task(name="workers.intelligence_tasks.run_intelligence_cycle", bind=True, max_retries=1)
def run_intelligence_cycle(self, trigger: str = "scheduled"):
    try:
        return _run_async(_intelligence_cycle_async(trigger))
    except Exception as exc:
        log.error("task.intelligence.failed", error=str(exc))
        raise self.retry(exc=exc, countdown=300)


async def _intelligence_cycle_async(trigger: str):
    from intelligence.engine import run_intelligence_cycle as _run_cycle
    from storage.database import get_session

    async with get_session() as session:
        results = await _run_cycle(session, trigger=trigger)
    return {"generated": len(results)}


@app.task(name="workers.intelligence_tasks.run_regime_classification")
def run_regime_classification():
    return _run_async(_regime_async())


async def _regime_async():
    from intelligence.regime_classifier import run_regime_classification as _classify
    from storage.database import get_session

    async with get_session() as session:
        regime = await _classify(session)
    return {"regime": regime.get("volatility_regime")}


@app.task(name="workers.intelligence_tasks.trigger_intelligence_manual")
def trigger_intelligence_manual():
    """Manually triggered intelligence cycle — called from API."""
    return _run_async(_intelligence_cycle_async("manual"))
