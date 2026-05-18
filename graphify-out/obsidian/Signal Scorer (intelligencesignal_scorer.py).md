---
source_file: "intelligence/signal_scorer.py"
type: "code"
community: "Core Config & Ingestion Hub"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Core_Config_&_Ingestion_Hub
---

# Signal Scorer (intelligence/signal_scorer.py)

## Connections
- [[Contradiction Detector (intelligencecontradiction_detector.py)]] - `semantically_similar_to` [INFERRED]
- [[Enrichment Workers (workersenrichment_tasks.py)]] - `calls` [EXTRACTED]
- [[Enum SourceTier]] - `shares_data_with` [INFERRED]
- [[Ingestion Workers (workersingestion_tasks.py)]] - `calls` [EXTRACTED]
- [[Intelligence Engine (intelligenceengine.py)]] - `calls` [EXTRACTED]
- [[Regime Classifier (intelligenceregime_classifier.py)]] - `conceptually_related_to` [INFERRED]
- [[Settings (configsettings.py)]] - `references` [EXTRACTED]
- [[Significance Threshold Gate (default 65.0)]] - `references` [INFERRED]
- [[Test Low Significance Skips Generation]] - `references` [EXTRACTED]
- [[Test Unit Misc (Regime, Scorer, Contradictions, Formatter)]] - `references` [EXTRACTED]
- [[engine.py]] - `imports_from` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Core_Config_&_Ingestion_Hub