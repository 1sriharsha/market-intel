"""Dev entry point — starts API server + scheduler in a single process for local development."""
import asyncio
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def main() -> None:
    from workers.celery_app import register_beat_schedule  # noqa: F401

    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.start()

    config = uvicorn.Config("api.main:app", host="0.0.0.0", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
