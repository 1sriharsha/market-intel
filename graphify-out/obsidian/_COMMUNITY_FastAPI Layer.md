---
type: community
cohesion: 0.09
members: 33
---

# FastAPI Layer

**Cohesion:** 0.09 - loosely connected
**Members:** 33 nodes

## Members
- [[Articles Endpoints]] - code - api/routes/articles.py
- [[Contradiction Schema]] - code - models/schemas.py
- [[Docker Compose (Production Services)]] - document - docker/docker-compose.yml
- [[Enable or disable a source feed.]] - rationale - api/routes/sources.py
- [[FastAPI Application Entry Point]] - code - api/main.py
- [[FastAPI Dependencies (DB Session Provider)]] - code - api/dependencies.py
- [[Feed Health Checker]] - code - monitoring/health_checker.py
- [[Grafana Service]] - document - docker/docker-compose.yml
- [[Health and Status Endpoints]] - code - api/routes/health.py
- [[Intelligence Endpoints]] - code - api/routes/intelligence.py
- [[Intelligence endpoints.]] - rationale - api/routes/intelligence.py
- [[List intelligence objects with optional filters.]] - rationale - api/routes/intelligence.py
- [[Manually trigger an intelligence cycle.]] - rationale - api/routes/intelligence.py
- [[PostgreSQL + TimescaleDB Service]] - document - docker/docker-compose.yml
- [[Prometheus Metric Definitions]] - code - monitoring/metrics.py
- [[Prometheus Scrape Configuration]] - document - docker/prometheus.yml
- [[Prometheus Service]] - document - docker/docker-compose.yml
- [[Pydantic Schema ContextPackage]] - code - models/schemas.py
- [[Pydantic Schema HistoricalAnalogue]] - code - models/schemas.py
- [[Pydantic Schema IntelligenceObjectCreate]] - code - models/schemas.py
- [[Pydantic Schema MacroSnapshot]] - code - models/schemas.py
- [[Pydantic Schemas (schemas.py)]] - code - models/schemas.py
- [[Redis Service]] - document - docker/docker-compose.yml
- [[Sources Endpoints]] - code - api/routes/sources.py
- [[articles.py]] - code - api/routes/articles.py
- [[get_intelligence()]] - code - api/routes/intelligence.py
- [[intelligence.py]] - code - api/routes/intelligence.py
- [[list_articles()]] - code - api/routes/articles.py
- [[list_intelligence()]] - code - api/routes/intelligence.py
- [[list_sources()]] - code - api/routes/sources.py
- [[sources.py_1]] - code - api/routes/sources.py
- [[trigger_intelligence_cycle()]] - code - api/routes/intelligence.py
- [[update_source()]] - code - api/routes/sources.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FastAPI_Layer
SORT file.name ASC
```

## Connections to other communities
- 16 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 6 edges to [[_COMMUNITY_API Routes & Contradiction Detection]]
- 2 edges to [[_COMMUNITY_Deduplication Pipeline]]
- 1 edge to [[_COMMUNITY_External Data Fetching]]
- 1 edge to [[_COMMUNITY_Source Feed Configuration]]
- 1 edge to [[_COMMUNITY_Price Data & Abnormal Returns]]
- 1 edge to [[_COMMUNITY_Article Normalization]]
- 1 edge to [[_COMMUNITY_Macro & Regime Analysis]]
- 1 edge to [[_COMMUNITY_Intelligence Generation]]
- 1 edge to [[_COMMUNITY_DB Migrations]]

## Top bridge nodes
- [[Pydantic Schemas (schemas.py)]] - degree 28, connects to 9 communities
- [[FastAPI Dependencies (DB Session Provider)]] - degree 9, connects to 2 communities
- [[FastAPI Application Entry Point]] - degree 9, connects to 1 community
- [[Health and Status Endpoints]] - degree 6, connects to 1 community
- [[Pydantic Schema ContextPackage]] - degree 5, connects to 1 community