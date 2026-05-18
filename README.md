# Market Intelligence Operating System (MIOS)

A persistent market intelligence platform that ingests financial news from 100+ free sources, correlates events to price movements, maintains longitudinal market memory, and delivers compressed, high-signal intelligence via Telegram.

**This is not a trading bot. It is not a prediction engine. It is disciplined situational awareness under uncertainty.**

---

## What It Does

1. **Ingests** news every 15 minutes from RSS feeds (Reuters, AP, FT, WSJ, CNBC, SEC EDGAR, Google News), financial APIs (Finnhub, Marketaux, Alpha Vantage), and macro data (FRED, BLS, US Treasury)
2. **Deduplicates** every article in two stages: SHA-256 URL hash (Redis, 7-day TTL) then semantic cosine similarity (pgvector, threshold 0.92)
3. **Enriches** articles with ticker extraction (spaCy + regex), OpenAI embeddings, and abnormal return computation (ticker return − β × SPY return)
4. **Scores** each article 0–100 based on source tier, novelty, cross-asset relevance, and macro regime sensitivity
5. **Generates intelligence** every 60 minutes using Claude — structured analysis with confidence scores, historical analogues, contradiction detection, and explicit unknowns
6. **Delivers** up to 5 Telegram alerts per day (hard cap in code) for `critical` and `high` significance events only

---

## Architecture

```
External Sources
    │
    ▼
Ingestion Layer          RSS · EDGAR · Finnhub · Marketaux · Alpha Vantage · FRED · yfinance
    │
    ▼
Canonical Storage        PostgreSQL 15 + TimescaleDB + pgvector
    │
    ▼
Enrichment Layer         Ticker extraction · OpenAI embeddings · Abnormal returns
    │
    ▼
Intelligence Layer       Signal scoring → Context assembly → Claude → Validation → DB
    │
    ▼
Delivery Layer           Telegram (max 5/day · 4h ticker cooldown · critical/high only)
```

### Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| API | FastAPI (async) |
| Task queue | Celery + Redis |
| Scheduler | APScheduler |
| Database | PostgreSQL 15 + TimescaleDB + pgvector |
| Cache / broker | Redis 7 |
| ORM | SQLAlchemy 2.0 async |
| Migrations | Alembic |
| HTTP client | httpx (async) |
| NLP | spaCy en_core_web_sm |
| Embeddings | OpenAI text-embedding-3-small (1536 dims) |
| LLM | Anthropic Claude (claude-sonnet-4-5) |
| Delivery | python-telegram-bot |
| Containers | Docker + Docker Compose |
| Monitoring | Prometheus + Grafana |
| Logging | structlog |

---

## Project Structure

```
market-intel/
├── config/
│   ├── settings.py          # All env vars and constants
│   ├── sources.py           # Every RSS feed URL, API endpoint, trust tier
│   └── watchlist.py         # Tickers (~75) and macro topics being monitored
├── ingestion/
│   ├── rss_fetcher.py       # feedparser-based RSS ingestion
│   ├── api_fetcher.py       # Finnhub, Marketaux, Alpha Vantage
│   ├── price_fetcher.py     # yfinance — historical + daily sync
│   ├── macro_fetcher.py     # FRED, BLS, Treasury
│   ├── edgar_fetcher.py     # SEC EDGAR RSS + GDELT BigQuery
│   ├── deduplicator.py      # URL hash + semantic dedup
│   └── normalizer.py        # All sources → canonical RawArticle
├── enrichment/
│   ├── embedder.py          # OpenAI text-embedding-3-small → pgvector
│   ├── ticker_extractor.py  # spaCy + regex → ticker list
│   └── price_reactor.py     # Abnormal return computation
├── intelligence/
│   ├── engine.py            # Main intelligence loop + Claude API calls
│   ├── retriever.py         # pgvector semantic search + context assembly
│   ├── regime_classifier.py # Market regime classification
│   ├── contradiction_detector.py
│   ├── signal_scorer.py     # Event significance scoring 0–100
│   └── prompts.py           # All Claude prompt templates — edit here only
├── delivery/
│   └── telegram_bot.py      # Format + push intelligence to Telegram
├── api/
│   ├── main.py              # FastAPI entry point
│   └── routes/              # health, intelligence, articles, sources
├── workers/
│   ├── celery_app.py        # Celery init + beat schedule
│   ├── ingestion_tasks.py
│   ├── enrichment_tasks.py
│   └── intelligence_tasks.py
├── storage/
│   ├── database.py          # Async SQLAlchemy engine + session factory
│   ├── redis_client.py      # Redis helpers (dedup, rate limits, cooldowns)
│   └── migrations/          # Alembic versions
├── monitoring/
│   ├── metrics.py           # Prometheus metric definitions
│   └── health_checker.py    # Feed health, lag detection
├── scripts/
│   ├── bootstrap.py         # One-time historical data load (resumable)
│   ├── backfill_embeddings.py
│   └── validate_sources.py  # Smoke test all feeds before deployment
└── tests/
    └── unit/                # 48 tests, 6 critical invariants
```

---

## Data Sources

### Trust Tiers

| Tier | Sources | Role |
|---|---|---|
| 1 | SEC EDGAR, FRED, BLS, Federal Reserve, US Treasury | Canonical truth — never suppressed |
| 2A | Reuters, AP Business, Bloomberg, FT, WSJ | High-trust corroboration |
| 2B | Google News RSS (per ticker + per macro topic) | Broad coverage |
| 2C | CNBC, MarketWatch, Seeking Alpha, Zacks, Morningstar | Financial press |
| 3 | Finnhub, Marketaux, Alpha Vantage, yfinance | Structured APIs |
| 4 | Reddit, StockTwits | Sentiment signals only — never factual evidence |

### Historical Depth

- **Prices**: yfinance `period='max'` — ~1970 to present
- **Macro**: FRED — 1947–present
- **Filings**: SEC EDGAR — 1993–present
- **Events**: GDELT BigQuery — 1979–present (structured, not full text)
- **RAG corpus**: Rolling 2-year window of full-text articles

---

## Intelligence Pipeline

Every cycle runs these steps in order:

```
1. Fetch unprocessed articles (significance_score > 65.0)
2. Group by topic cluster
3. For each cluster:
   a. Build context package (articles + prices + macro + regime + analogues + contradictions)
   b. Validate context (no stale data, no null prices)
   c. Call Claude with structured prompt
   d. Strip hallucinated tickers (post-generation validation)
   e. Reject if confidence_explanation is empty
   f. Write intelligence_object to PostgreSQL
   g. Evaluate delivery (significance + cooldown + daily cap)
   h. Push to Telegram if criteria met
4. Mark articles as processed
```

### Signal Score Thresholds

| Score | Label | Action |
|---|---|---|
| 90–100 | critical | Pushed to Telegram |
| 70–89 | high | Pushed to Telegram |
| 50–69 | medium | Stored in DB only |
| 30–49 | low | Stored in DB only |
| 0–29 | suppressed | Logged, not stored |

---

## Hard Delivery Rules

These are enforced in code, not config:

- **5 alerts per day maximum** — hard cap
- **4-hour cooldown per ticker** between alerts
- **critical and high only** — medium/low are never pushed
- **3800 character limit** per Telegram message

---

## Setup

### Prerequisites

- Docker + Docker Compose
- Python 3.11+
- API keys (see Step 1 below)

---

### Step 1 — Get your API keys

| Key | Where to get it | Cost |
|---|---|---|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) | Pay-per-use |
| `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) | Pay-per-use |
| `TELEGRAM_BOT_TOKEN` | Message `@BotFather` on Telegram → `/newbot` | Free |
| `TELEGRAM_CHAT_ID` | Message `@userinfobot` on Telegram | Free |
| `FINNHUB_API_KEY` | [finnhub.io/register](https://finnhub.io/register) | Free |
| `MARKETAUX_API_KEY` | [marketaux.com](https://www.marketaux.com) | Free |
| `ALPHA_VANTAGE_KEY` | [alphavantage.co/support](https://www.alphavantage.co/support/#api-key) | Free |

FRED (macro data) requires no key.

---

### Step 2 — Create your `.env` file

In the project root, create a file named `.env`:

```env
# Required
DATABASE_URL=postgresql+asyncpg://mios:changeme@localhost:5432/mios
REDIS_URL=redis://localhost:6379/0
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
FINNHUB_API_KEY=...
MARKETAUX_API_KEY=...
ALPHA_VANTAGE_KEY=...

# Optional
GOOGLE_CLOUD_PROJECT=...        # For GDELT BigQuery bootstrap
SIGNIFICANCE_THRESHOLD=65.0
MAX_DAILY_ALERTS=5
ALERT_COOLDOWN_HOURS=4
RAG_CORPUS_DAYS=730
```

---

### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

### Step 4 — Start infrastructure and run migrations

```bash
# Start PostgreSQL + Redis
docker compose -f docker/docker-compose.yml up -d postgres redis

# Wait ~10 seconds, then run migrations
alembic upgrade head
```

---

### Step 5 — Bootstrap historical data

This runs **once**. It loads price history, macro series, and seeds the analogue database. Takes 30–60 minutes depending on internet speed. It is resumable — safe to interrupt and re-run.

```bash
# Validate all RSS feeds are reachable first
python scripts/validate_sources.py

# Load historical prices + macro data
python scripts/bootstrap.py

# Embed bootstrapped articles (can run overnight for large corpus)
python scripts/backfill_embeddings.py
```

> Do not skip bootstrap. Historical analogues are the foundation of intelligence quality.

---

### Step 6 — Start all services

```bash
docker compose -f docker/docker-compose.yml up -d
```

This starts:

| Service | What it does |
|---|---|
| `api_server` | FastAPI on port 8000 |
| `ingestion_worker` | Fetches RSS + EDGAR every 15 min |
| `enrichment_worker` | Embeds articles, computes abnormal returns |
| `intelligence_worker` | Runs Claude intelligence cycle every 60 min |
| `delivery_worker` | Sends Telegram alerts |
| `celery_beat` | Scheduler that fires all the above |
| `prometheus` | Metrics on port 9090 |
| `grafana` | Dashboard on port 3000 (admin / changeme) |

---

### Step 7 — Verify and trigger first cycle

```bash
# Basic liveness
curl http://localhost:8000/health

# Full system status — ingestion lag, feed health, embedding backlog
curl http://localhost:8000/status

# Trigger first intelligence cycle manually
curl -X POST http://localhost:8000/intelligence/trigger
```

Within a few minutes you should receive a Telegram message if any articles scored above 70.

---

## Day-to-Day Usage

Once running, everything is hands-off:

| Schedule | What happens |
|---|---|
| Every 15 min | Fetches all RSS feeds, EDGAR filings |
| Every 60 min | Runs intelligence cycle, calls Claude |
| When triggered | Sends Telegram alert (max 5/day) |
| Daily 6:30pm ET | Syncs latest stock prices via yfinance |
| Daily 5:00am ET | Syncs FRED macro data |

**To check what's happening at any time:**

```bash
# Articles coming in
curl http://localhost:8000/articles

# Intelligence objects generated today
curl http://localhost:8000/intelligence

# Feed health (last fetch time, errors)
curl http://localhost:8000/sources

# Full logs
docker compose -f docker/docker-compose.yml logs -f intelligence_worker
```

---

## Troubleshooting

| Problem | What to check |
|---|---|
| No articles ingesting | `GET /sources` — look at `last_error` on each feed |
| No Telegram messages | `GET /intelligence` — if objects exist but aren't delivered, check `significance_level` (only `critical`/`high` are sent) |
| DB connection error | `docker compose ps` — confirm postgres is healthy |
| Intelligence not running | `docker compose logs celery_beat` — verify beat schedule is firing |
| Bootstrap interrupted | Re-run `python scripts/bootstrap.py` — it resumes from where it stopped |

**`GET /status` is always the first thing to check** — it shows ingestion lag, embedding backlog, last intelligence run time, and feed health in one response.

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness check |
| GET | `/status` | Ingestion lag, feed health, embedding backlog, last intelligence run |
| GET | `/intelligence` | Recent intelligence objects |
| POST | `/intelligence/trigger` | Trigger manual intelligence cycle |
| GET | `/articles` | Recent articles with scores |
| GET | `/sources` | All registered source feeds with health status |

---

## Job Schedule

| Job | Schedule |
|---|---|
| RSS feeds (all tiers) | Every 15 min |
| EDGAR RSS | Every 15 min |
| Finnhub + Marketaux + Alpha Vantage | Every 60 min |
| Daily price sync (yfinance) | Daily 23:30 UTC (18:30 ET) |
| Macro sync (FRED) | Daily 10:00 UTC (05:00 ET) |
| Embed new articles | Triggered after ingestion |
| Intelligence cycle | Every 60 min |
| Regime classification | Every 60 min |
| Feed health check | Every 30 min |

---

## Testing

```bash
# Unit tests (no external dependencies required)
pytest tests/ -v

# Integration tests (requires Docker test profile)
docker compose -f docker/docker-compose.test.yml up -d
pytest tests/integration/ -v
```

### Critical Tests (must always pass)

| Test | What It Guards |
|---|---|
| `test_duplicate_not_written_twice` | Two-stage dedup correctness |
| `test_published_at_never_null` | Data integrity |
| `test_intelligence_cites_source_ids` | No orphaned intelligence objects |
| `test_no_hallucination_beyond_context` | Claude output validation |
| `test_rate_limit_respected` | Delivery cap enforcement |
| `test_low_significance_skips_generation` | Cost control |

All 48 unit tests run without network access — all DB, Redis, and API calls are mocked.

---

## Operations

### Add a new RSS feed

```bash
# 1. Add entry to config/sources.py
# 2. Add row to source_feeds table
# 3. Validate
python scripts/validate_sources.py
```

### Add a ticker to the watchlist

```bash
# 1. Add to config/watchlist.py
# 2. Backfill price history
python scripts/bootstrap.py --tickers NEW_TICKER
# 3. Rebuild company name map
python -c "from enrichment.ticker_extractor import build_company_ticker_map; build_company_ticker_map()"
```

### Disable a broken feed

```sql
UPDATE source_feeds SET is_active = false WHERE id = 'feed_slug';
```

### Monitoring

- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000` (admin / changeme)
- **Structured logs**: all services emit JSON via structlog

---

## Data Model (key tables)

| Table | Primary Key | Description |
|---|---|---|
| `articles` | `id` (SHA-256 of URL) | Every ingested news item |
| `prices` | `(ticker, date)` | Daily OHLCV, adjusted close |
| `macro_data` | `(series_id, date)` | FRED/BLS economic series |
| `article_ticker_effects` | `(article_id, ticker)` | Abnormal return per article/ticker |
| `intelligence_objects` | `uuid` | All Claude-generated intelligence |
| `embeddings` | `article_id` | pgvector embeddings (1536 dims) |
| `regime_snapshots` | `id` | Point-in-time regime classifications |
| `source_feeds` | `id` (slug) | Feed registry with health state |
| `historical_events` | `id` | GDELT structured events 1979–present |

**PostgreSQL is the canonical source of truth. Redis and pgvector are derived. Events are append-only — historical records are never updated.**

---

## Non-Negotiables

- All timestamps are UTC
- All tasks are idempotent — running any job twice produces the same DB state
- Claude never receives unvalidated retrieval context
- Post-generation validation runs on every LLM output without exception
- The 5-alert daily cap is enforced in code, not environment config
- Tier 4 sources (Reddit, StockTwits) are never used as factual evidence
