---
source_file: "storage/redis_client.py"
type: "code"
community: "Core Config & Ingestion Hub"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Core_Config_&_Ingestion_Hub
---

# Redis Client (storage/redis_client.py)

## Connections
- [[API Fetcher (ingestionapi_fetcher.py)]] - `calls` [EXTRACTED]
- [[Deduplicator (ingestiondeduplicator.py)]] - `calls` [EXTRACTED]
- [[FastAPI Application Entry Point]] - `calls` [EXTRACTED]
- [[Hard Delivery Rules (5-cap, 4h cooldown, significance filter)]] - `references` [INFERRED]
- [[Health and Status Endpoints]] - `calls` [EXTRACTED]
- [[Settings (configsettings.py)]] - `references` [EXTRACTED]
- [[Telegram Bot (deliverytelegram_bot.py)]] - `references` [EXTRACTED]
- [[Test Fixtures (testsconftest.py)]] - `references` [EXTRACTED]
- [[Two-Stage Deduplication Pipeline]] - `references` [INFERRED]
- [[api_fetcher.py]] - `imports_from` [EXTRACTED]
- [[deduplicator.py]] - `imports_from` [EXTRACTED]
- [[telegram_bot.py]] - `imports_from` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Core_Config_&_Ingestion_Hub