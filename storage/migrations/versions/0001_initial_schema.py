"""Initial schema — all 9 canonical tables + pgvector + TimescaleDB extensions."""
from alembic import op
import sqlalchemy as sa

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID

TIMESTAMPTZ = DateTime(timezone=True)

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE")

    # source_feeds — referenced by articles FK
    op.create_table(
        "source_feeds",
        sa.Column("id", sa.Text, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("feed_type", sa.Text, nullable=False),
        sa.Column("url", sa.Text),
        sa.Column("tier", sa.SmallInteger),
        sa.Column("fetch_interval_minutes", sa.Integer, nullable=False, server_default="15"),
        sa.Column("last_fetched_at", TIMESTAMPTZ),
        sa.Column("last_error", sa.Text),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("article_count", sa.Integer, nullable=False, server_default="0"),
    )

    # articles
    op.create_table(
        "articles",
        sa.Column("id", sa.Text, primary_key=True),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("summary", sa.Text),
        sa.Column("url", sa.Text, unique=True, nullable=False),
        sa.Column("source_name", sa.Text, nullable=False),
        sa.Column("source_tier", sa.SmallInteger, nullable=False),
        sa.Column("source_feed_id", sa.Text, sa.ForeignKey("source_feeds.id")),
        sa.Column("tickers", sa.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("topics", sa.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("published_at", TIMESTAMPTZ, nullable=False),
        sa.Column("fetched_at", TIMESTAMPTZ, nullable=False),
        sa.Column("raw_content", sa.Text),
        sa.Column("significance_score", sa.Float),
        sa.Column("novelty_score", sa.Float),
        sa.Column("is_processed", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("is_embedded", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", TIMESTAMPTZ, nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_articles_published_at", "articles", ["published_at"])
    op.create_index("ix_articles_is_processed", "articles", ["is_processed"])
    op.create_index("ix_articles_is_embedded", "articles", ["is_embedded"])
    op.create_index("ix_articles_significance_score", "articles", ["significance_score"])
    # GIN index for array containment queries
    op.execute("CREATE INDEX ix_articles_tickers ON articles USING GIN (tickers)")
    op.execute("CREATE INDEX ix_articles_topics ON articles USING GIN (topics)")

    # prices — TimescaleDB hypertable
    op.create_table(
        "prices",
        sa.Column("ticker", sa.Text, nullable=False),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("open", sa.Numeric(12, 4)),
        sa.Column("high", sa.Numeric(12, 4)),
        sa.Column("low", sa.Numeric(12, 4)),
        sa.Column("close", sa.Numeric(12, 4)),
        sa.Column("volume", sa.BigInteger),
        sa.Column("source", sa.Text, nullable=False, server_default="'yfinance'"),
        sa.PrimaryKeyConstraint("ticker", "date"),
    )
    op.execute("SELECT create_hypertable('prices', 'date', if_not_exists => TRUE)")
    op.create_index("ix_prices_ticker", "prices", ["ticker"])

    # macro_data
    op.create_table(
        "macro_data",
        sa.Column("series_id", sa.Text, nullable=False),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("value", sa.Numeric(18, 6), nullable=False),
        sa.Column("series_name", sa.Text),
        sa.Column("frequency", sa.Text),
        sa.PrimaryKeyConstraint("series_id", "date"),
    )
    op.create_index("ix_macro_data_series_id", "macro_data", ["series_id"])

    # article_ticker_effects
    op.create_table(
        "article_ticker_effects",
        sa.Column("article_id", sa.Text, sa.ForeignKey("articles.id"), nullable=False),
        sa.Column("ticker", sa.Text, nullable=False),
        sa.Column("attribution_method", sa.Text, nullable=False),
        sa.Column("price_at_publish", sa.Numeric(12, 4)),
        sa.Column("price_1h_after", sa.Numeric(12, 4)),
        sa.Column("price_1d_after", sa.Numeric(12, 4)),
        sa.Column("spy_return_1d", sa.Numeric(8, 6)),
        sa.Column("abnormal_return_1d", sa.Numeric(8, 6)),
        sa.Column("reaction_label", sa.Text),
        sa.PrimaryKeyConstraint("article_id", "ticker"),
    )

    # historical_events (GDELT)
    op.create_table(
        "historical_events",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("gdelt_event_id", sa.BigInteger, unique=True, nullable=False),
        sa.Column("event_date", sa.Date, nullable=False),
        sa.Column("actor1", sa.Text),
        sa.Column("actor2", sa.Text),
        sa.Column("event_code", sa.Text),
        sa.Column("event_category", sa.Text),
        sa.Column("goldstein_scale", sa.Numeric(4, 1)),
        sa.Column("avg_tone", sa.Numeric(6, 2)),
        sa.Column("num_mentions", sa.Integer),
        sa.Column("num_sources", sa.Integer),
        sa.Column("tickers_affected", sa.ARRAY(sa.Text)),
        sa.Column("source_url", sa.Text),
    )
    op.create_index("ix_historical_events_event_date", "historical_events", ["event_date"])
    op.create_index("ix_historical_events_event_category", "historical_events", ["event_category"])

    # intelligence_objects
    op.create_table(
        "intelligence_objects",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("created_at", TIMESTAMPTZ, nullable=False, server_default=sa.func.now()),
        sa.Column("trigger_type", sa.Text, nullable=False),
        sa.Column("tickers", sa.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("topics", sa.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("summary", sa.Text, nullable=False),
        sa.Column("why_it_matters", sa.Text),
        sa.Column("historical_context", sa.Text),
        sa.Column("contradictions", sa.Text),
        sa.Column("risks", sa.Text),
        sa.Column("unknowns", sa.Text),
        sa.Column("confidence_score", sa.Float),
        sa.Column("confidence_explanation", sa.Text),
        sa.Column("significance_level", sa.Text),
        sa.Column("source_article_ids", sa.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("llm_model", sa.Text),
        sa.Column("llm_input_tokens", sa.Integer),
        sa.Column("llm_output_tokens", sa.Integer),
        sa.Column("delivered_at", TIMESTAMPTZ),
    )
    op.create_index("ix_intelligence_objects_created_at", "intelligence_objects", ["created_at"])
    op.create_index("ix_intelligence_objects_significance_level", "intelligence_objects",
                    ["significance_level"])

    # embeddings — pgvector column
    op.create_table(
        "embeddings",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("article_id", sa.Text, sa.ForeignKey("articles.id"), nullable=False),
        sa.Column("embedding_model", sa.Text, nullable=False),
        sa.Column("chunk_index", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("content_hash", sa.Text, nullable=False),
        sa.Column("created_at", TIMESTAMPTZ, nullable=False, server_default=sa.func.now()),
    )
    # Add vector column separately (pgvector DDL)
    op.execute("ALTER TABLE embeddings ADD COLUMN embedding vector(1536)")
    op.execute(
        "CREATE INDEX ix_embeddings_vector ON embeddings "
        "USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
    )
    op.create_index("ix_embeddings_article_id", "embeddings", ["article_id"])

    # regime_snapshots
    op.create_table(
        "regime_snapshots",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("snapshot_at", TIMESTAMPTZ, nullable=False),
        sa.Column("volatility_regime", sa.Text),
        sa.Column("liquidity_regime", sa.Text),
        sa.Column("macro_regime", sa.Text),
        sa.Column("sentiment_regime", sa.Text),
        sa.Column("vix_value", sa.Numeric(6, 2)),
        sa.Column("yield_curve_spread", sa.Numeric(6, 4)),
        sa.Column("fed_funds_rate", sa.Numeric(5, 3)),
        sa.Column("confidence", sa.Float),
        sa.Column("notes", sa.Text),
    )

    # bootstrap_state — resumable bootstrap progress tracker
    op.create_table(
        "bootstrap_state",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("step", sa.Text, nullable=False, unique=True),
        sa.Column("status", sa.Text, nullable=False, server_default="'pending'"),
        sa.Column("progress_key", sa.Text),
        sa.Column("completed_at", TIMESTAMPTZ),
        sa.Column("error", sa.Text),
        sa.Column("updated_at", TIMESTAMPTZ, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    for table in [
        "bootstrap_state", "regime_snapshots", "embeddings",
        "intelligence_objects", "historical_events", "article_ticker_effects",
        "macro_data", "prices", "articles", "source_feeds",
    ]:
        op.drop_table(table)
    op.execute("DROP EXTENSION IF EXISTS vector")
