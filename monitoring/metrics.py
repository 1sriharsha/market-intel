"""Prometheus metric definitions for all MIOS subsystems."""
from prometheus_client import Counter, Gauge, Histogram, Summary

# --- Ingestion metrics ---
articles_ingested_total = Counter(
    "mios_articles_ingested_total",
    "Total articles ingested",
    ["source_tier", "feed_id"],
)
articles_deduplicated_total = Counter(
    "mios_articles_deduplicated_total",
    "Total articles suppressed by dedup",
    ["stage"],  # url | semantic
)
feed_fetch_errors_total = Counter(
    "mios_feed_fetch_errors_total",
    "Total feed fetch errors",
    ["feed_id"],
)
ingestion_lag_minutes = Gauge(
    "mios_ingestion_lag_minutes",
    "Minutes since last article was fetched",
)

# --- Enrichment metrics ---
embeddings_generated_total = Counter(
    "mios_embeddings_generated_total",
    "Total embeddings generated",
)
embedding_backlog = Gauge(
    "mios_embedding_backlog",
    "Articles awaiting embedding",
)
embedding_latency_seconds = Histogram(
    "mios_embedding_latency_seconds",
    "OpenAI embedding API latency",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
)

# --- Intelligence metrics ---
intelligence_cycles_total = Counter(
    "mios_intelligence_cycles_total",
    "Total intelligence cycles run",
    ["trigger_type"],
)
intelligence_objects_generated_total = Counter(
    "mios_intelligence_objects_generated_total",
    "Total intelligence objects generated",
    ["significance_level"],
)
claude_api_latency_seconds = Histogram(
    "mios_claude_api_latency_seconds",
    "Claude API call latency",
    buckets=[1.0, 2.0, 5.0, 10.0, 20.0, 30.0],
)
claude_tokens_used_total = Counter(
    "mios_claude_tokens_used_total",
    "Total Claude tokens consumed",
    ["direction"],  # input | output
)
hallucinations_detected_total = Counter(
    "mios_hallucinations_detected_total",
    "Total ticker hallucinations stripped from Claude output",
)

# --- Delivery metrics ---
telegram_alerts_sent_total = Counter(
    "mios_telegram_alerts_sent_total",
    "Total Telegram alerts sent",
    ["significance_level"],
)
telegram_alerts_suppressed_total = Counter(
    "mios_telegram_alerts_suppressed_total",
    "Total Telegram alerts suppressed",
    ["reason"],  # significance | daily_cap | cooldown
)
daily_alerts_remaining = Gauge(
    "mios_daily_alerts_remaining",
    "Remaining Telegram alerts allowed today",
)

# --- System health ---
feeds_healthy = Gauge(
    "mios_feeds_healthy",
    "Number of feeds with recent successful fetches",
)
feeds_total = Gauge(
    "mios_feeds_total",
    "Total active feeds",
)
last_intelligence_run_timestamp = Gauge(
    "mios_last_intelligence_run_timestamp",
    "Unix timestamp of last intelligence cycle",
)
