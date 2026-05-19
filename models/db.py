"""SQLAlchemy 2.0 async ORM models — canonical schema for all 9 tables."""
from datetime import datetime, date
from typing import Optional
import uuid

from sqlalchemy import (
    BigInteger, Boolean, Column, Date, Float, ForeignKey,
    Integer, Numeric, SmallInteger, String, Text, ARRAY,
    func, text,
)

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID

TIMESTAMPTZ = DateTime(timezone=True)

from sqlalchemy.orm import DeclarativeBase, relationship




class Base(DeclarativeBase):
    pass


class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True)                       # SHA-256 of canonical URL
    title = Column(Text, nullable=False)
    summary = Column(Text)
    url = Column(Text, unique=True, nullable=False)
    source_name = Column(Text, nullable=False)
    source_tier = Column(SmallInteger, nullable=False)
    source_feed_id = Column(Text, ForeignKey("source_feeds.id"), nullable=True)
    tickers = Column(ARRAY(Text), nullable=False, server_default="{}")
    topics = Column(ARRAY(Text), nullable=False, server_default="{}")
    published_at = Column(TIMESTAMPTZ, nullable=False)
    fetched_at = Column(TIMESTAMPTZ, nullable=False)
    raw_content = Column(Text)
    significance_score = Column(Float)
    novelty_score = Column(Float)
    is_processed = Column(Boolean, nullable=False, server_default="false")
    is_embedded = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(TIMESTAMPTZ, nullable=False, server_default=func.now())

    ticker_effects = relationship("ArticleTickerEffect", back_populates="article", lazy="select")
    embedding = relationship("Embedding", back_populates="article", lazy="select")


class Price(Base):
    __tablename__ = "prices"

    ticker = Column(Text, primary_key=True, nullable=False)
    date = Column(Date, primary_key=True, nullable=False)
    open = Column(Numeric(12, 4))
    high = Column(Numeric(12, 4))
    low = Column(Numeric(12, 4))
    close = Column(Numeric(12, 4))
    volume = Column(BigInteger)
    source = Column(Text, nullable=False, server_default="'yfinance'")


class MacroData(Base):
    __tablename__ = "macro_data"

    series_id = Column(Text, primary_key=True, nullable=False)
    date = Column(Date, primary_key=True, nullable=False)
    value = Column(Numeric(18, 6), nullable=False)
    series_name = Column(Text)
    frequency = Column(Text)


class ArticleTickerEffect(Base):
    __tablename__ = "article_ticker_effects"

    article_id = Column(Text, ForeignKey("articles.id"), primary_key=True, nullable=False)
    ticker = Column(Text, primary_key=True, nullable=False)
    attribution_method = Column(Text, nullable=False)
    price_at_publish = Column(Numeric(12, 4))
    price_1h_after = Column(Numeric(12, 4))
    price_1d_after = Column(Numeric(12, 4))
    spy_return_1d = Column(Numeric(8, 6))
    abnormal_return_1d = Column(Numeric(8, 6))
    reaction_label = Column(Text)

    article = relationship("Article", back_populates="ticker_effects")


class HistoricalEvent(Base):
    __tablename__ = "historical_events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    gdelt_event_id = Column(BigInteger, unique=True, nullable=False)
    event_date = Column(Date, nullable=False)
    actor1 = Column(Text)
    actor2 = Column(Text)
    event_code = Column(Text)
    event_category = Column(Text)
    goldstein_scale = Column(Numeric(4, 1))
    avg_tone = Column(Numeric(6, 2))
    num_mentions = Column(Integer)
    num_sources = Column(Integer)
    tickers_affected = Column(ARRAY(Text))
    source_url = Column(Text)


class IntelligenceObject(Base):
    __tablename__ = "intelligence_objects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                server_default=text("gen_random_uuid()"))
    created_at = Column(TIMESTAMPTZ, nullable=False, server_default=func.now())
    trigger_type = Column(Text, nullable=False)
    tickers = Column(ARRAY(Text), nullable=False, server_default="{}")
    topics = Column(ARRAY(Text), nullable=False, server_default="{}")
    summary = Column(Text, nullable=False)
    why_it_matters = Column(Text)
    historical_context = Column(Text)
    contradictions = Column(Text)
    risks = Column(Text)
    unknowns = Column(Text)
    confidence_score = Column(Float)
    confidence_explanation = Column(Text)
    significance_level = Column(Text)
    source_article_ids = Column(ARRAY(Text), nullable=False, server_default="{}")
    llm_model = Column(Text)
    llm_input_tokens = Column(Integer)
    llm_output_tokens = Column(Integer)
    delivered_at = Column(TIMESTAMPTZ)


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    article_id = Column(Text, ForeignKey("articles.id"), nullable=False)
    embedding = Column(Text)   # stored as JSON string; pgvector type set via migration DDL
    embedding_model = Column(Text, nullable=False)
    chunk_index = Column(SmallInteger, nullable=False, server_default="0")
    content_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMPTZ, nullable=False, server_default=func.now())

    article = relationship("Article", back_populates="embedding")


class SourceFeed(Base):
    __tablename__ = "source_feeds"

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    feed_type = Column(Text, nullable=False)
    url = Column(Text)
    tier = Column(SmallInteger)
    fetch_interval_minutes = Column(Integer, nullable=False, server_default="15")
    last_fetched_at = Column(TIMESTAMPTZ)
    last_error = Column(Text)
    is_active = Column(Boolean, nullable=False, server_default="true")
    article_count = Column(Integer, nullable=False, server_default="0")


class RegimeSnapshot(Base):
    __tablename__ = "regime_snapshots"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    snapshot_at = Column(TIMESTAMPTZ, nullable=False)
    volatility_regime = Column(Text)
    liquidity_regime = Column(Text)
    macro_regime = Column(Text)
    sentiment_regime = Column(Text)
    vix_value = Column(Numeric(6, 2))
    yield_curve_spread = Column(Numeric(6, 4))
    fed_funds_rate = Column(Numeric(5, 3))
    confidence = Column(Float)
    notes = Column(Text)


class BootstrapState(Base):
    """Tracks resumable bootstrap progress."""
    __tablename__ = "bootstrap_state"

    id = Column(Integer, primary_key=True, autoincrement=True)
    step = Column(Text, nullable=False, unique=True)
    status = Column(Text, nullable=False, server_default="'pending'")
    progress_key = Column(Text)
    completed_at = Column(TIMESTAMPTZ)
    error = Column(Text)
    updated_at = Column(TIMESTAMPTZ, nullable=False, server_default=func.now(),
                        onupdate=func.now())
