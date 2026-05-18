---
source_file: "delivery/telegram_bot.py"
type: "code"
community: "Core Config & Ingestion Hub"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Core_Config_&_Ingestion_Hub
---

# Telegram Bot (delivery/telegram_bot.py)

## Connections
- [[Hard Delivery Rules (5-cap, 4h cooldown, significance filter)]] - `implements` [EXTRACTED]
- [[Intelligence Engine (intelligenceengine.py)]] - `calls` [EXTRACTED]
- [[ORM Model IntelligenceObject]] - `shares_data_with` [INFERRED]
- [[Redis Client (storageredis_client.py)]] - `references` [EXTRACTED]
- [[Settings (configsettings.py)]] - `references` [EXTRACTED]
- [[Test Rate Limit Respected]] - `references` [EXTRACTED]
- [[Test Unit Misc (Regime, Scorer, Contradictions, Formatter)]] - `references` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Core_Config_&_Ingestion_Hub