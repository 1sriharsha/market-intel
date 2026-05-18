"""Celery application init + task registry + beat schedule."""
from celery import Celery
from celery.schedules import crontab

from config.settings import settings

app = Celery(
    "mios",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "workers.ingestion_tasks",
        "workers.enrichment_tasks",
        "workers.intelligence_tasks",
    ],
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_routes={
        "workers.ingestion_tasks.*": {"queue": "ingestion"},
        "workers.enrichment_tasks.*": {"queue": "enrichment"},
        "workers.intelligence_tasks.*": {"queue": "intelligence"},
    },
    beat_schedule={
        "rss-ingestion-every-15min": {
            "task": "workers.ingestion_tasks.run_rss_ingestion",
            "schedule": 15 * 60,
            "options": {"queue": "ingestion"},
        },
        "edgar-ingestion-every-15min": {
            "task": "workers.ingestion_tasks.run_edgar_ingestion",
            "schedule": 15 * 60,
            "options": {"queue": "ingestion"},
        },
        "api-ingestion-every-60min": {
            "task": "workers.ingestion_tasks.run_api_ingestion",
            "schedule": 60 * 60,
            "options": {"queue": "ingestion"},
        },
        "intelligence-cycle-every-60min": {
            "task": "workers.intelligence_tasks.run_intelligence_cycle",
            "schedule": settings.intelligence_cycle_minutes * 60,
            "options": {"queue": "intelligence"},
        },
        "regime-classification-every-60min": {
            "task": "workers.intelligence_tasks.run_regime_classification",
            "schedule": 60 * 60,
            "options": {"queue": "intelligence"},
        },
        "price-sync-daily": {
            "task": "workers.enrichment_tasks.run_price_sync",
            "schedule": crontab(hour=settings.price_sync_hour_utc, minute=30),
            "options": {"queue": "enrichment"},
        },
        "macro-sync-daily": {
            "task": "workers.enrichment_tasks.run_macro_sync",
            "schedule": crontab(hour=settings.macro_sync_hour_utc, minute=0),
            "options": {"queue": "enrichment"},
        },
        "feed-health-check-every-30min": {
            "task": "workers.ingestion_tasks.run_feed_health_check",
            "schedule": 30 * 60,
            "options": {"queue": "ingestion"},
        },
    },
)


def register_beat_schedule():
    """No-op — schedule is registered via app.conf above. Called by main.py to import workers."""
    pass
