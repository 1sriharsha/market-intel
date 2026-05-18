"""All environment variables, constants, and thresholds. Read from environment — never hardcode."""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # --- Database ---
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/mios"

    # --- Redis ---
    redis_url: str = "redis://localhost:6379/0"

    # --- External API keys ---
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    finnhub_api_key: str = ""
    marketaux_api_key: str = ""
    alpha_vantage_key: str = ""

    # --- Optional ---
    google_cloud_project: str | None = None

    # --- Intelligence tuning ---
    intelligence_cycle_minutes: int = 60
    max_daily_alerts: int = 5
    alert_cooldown_hours: int = 4
    significance_threshold: float = 65.0
    rag_corpus_days: int = 730
    embedding_batch_size: int = 100

    # --- Model identifiers ---
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    llm_model: str = "claude-sonnet-4-5"

    # --- Ingestion constants ---
    rss_fetch_interval_minutes: int = 15
    api_fetch_interval_minutes: int = 60
    price_sync_hour_utc: int = 23       # 18:30 ET ≈ 23:30 UTC
    macro_sync_hour_utc: int = 10       # 05:00 ET ≈ 10:00 UTC
    feed_health_check_interval_minutes: int = 30

    # --- Deduplication ---
    url_dedup_ttl_seconds: int = 7 * 24 * 3600   # 7 days
    semantic_dedup_similarity_threshold: float = 0.92
    semantic_dedup_window_hours: int = 6

    # --- Signal scoring ---
    significance_threshold_systemic: float = 90.0
    significance_threshold_major: float = 70.0
    significance_threshold_meaningful: float = 50.0
    significance_threshold_moderate: float = 30.0

    # --- Retrieval ---
    retrieval_semantic_weight: float = 0.7
    retrieval_recency_weight: float = 0.3
    retrieval_top_k: int = 5

    # --- Telegram ---
    telegram_max_message_chars: int = 3800

    # --- Embedding ---
    embedding_max_tokens: int = 8192
    embedding_max_inputs_per_call: int = 2048

    # --- Price data ---
    beta_regression_days: int = 60

    # --- Rate limits (enforced via Redis counters) ---
    finnhub_rate_limit_per_minute: int = 60
    marketaux_rate_limit_per_day: int = 100
    alpha_vantage_rate_limit_per_day: int = 25


settings = Settings()
