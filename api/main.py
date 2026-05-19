"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import make_asgi_app

from api.routes import health, intelligence, articles, sources

log = structlog.get_logger()

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("api.startup")
    yield
    from storage.database import engine
    await engine.dispose()
    from storage.redis_client import close_redis
    await close_redis()
    log.info("api.shutdown")


app = FastAPI(
    title="Market Intelligence Operating System",
    version="1.0.0",
    docs_url="/docs",
    lifespan=lifespan,
)

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Routes
app.include_router(health.router, tags=["health"])
app.include_router(intelligence.router, prefix="/intelligence", tags=["intelligence"])
app.include_router(articles.router, prefix="/articles", tags=["articles"])
app.include_router(sources.router, prefix="/sources", tags=["sources"])

# Serve frontend dashboard
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def dashboard():
    return FileResponse(STATIC_DIR / "index.html")
