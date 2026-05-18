---
source_file: "delivery/telegram_bot.py"
type: "rationale"
community: "Core Config & Ingestion Hub"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Core_Config_&_Ingestion_Hub
---

# Hard Delivery Rules (5-cap, 4h cooldown, significance filter)

## Connections
- [[Enum SignificanceLevel]] - `shares_data_with` [INFERRED]
- [[Redis Client (storageredis_client.py)]] - `references` [INFERRED]
- [[Telegram Bot (deliverytelegram_bot.py)]] - `implements` [EXTRACTED]
- [[Test Rate Limit Respected]] - `conceptually_related_to` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Core_Config_&_Ingestion_Hub