"""APScheduler entry point — runs beat-schedule tasks when Celery beat is not used."""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

import structlog

log = structlog.get_logger()


def main() -> None:
    scheduler = BlockingScheduler(timezone="UTC")

    from workers.ingestion_tasks import run_rss_ingestion, run_api_ingestion, run_edgar_ingestion
    from workers.intelligence_tasks import run_intelligence_cycle, run_regime_classification
    from workers.enrichment_tasks import run_price_sync, run_macro_sync

    scheduler.add_job(run_rss_ingestion, IntervalTrigger(minutes=15), id="rss_ingestion")
    scheduler.add_job(run_edgar_ingestion, IntervalTrigger(minutes=15), id="edgar_ingestion")
    scheduler.add_job(run_api_ingestion, IntervalTrigger(minutes=60), id="api_ingestion")
    scheduler.add_job(run_intelligence_cycle, IntervalTrigger(minutes=60), id="intelligence")
    scheduler.add_job(run_regime_classification, IntervalTrigger(minutes=60), id="regime")
    scheduler.add_job(run_price_sync, CronTrigger(hour=23, minute=30, timezone="UTC"), id="price_sync")
    scheduler.add_job(run_macro_sync, CronTrigger(hour=10, minute=0, timezone="UTC"), id="macro_sync")

    log.info("scheduler.starting")
    scheduler.start()


if __name__ == "__main__":
    main()
