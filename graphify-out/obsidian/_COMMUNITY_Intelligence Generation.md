---
type: community
cohesion: 0.07
members: 39
---

# Intelligence Generation

**Cohesion:** 0.07 - loosely connected
**Members:** 39 nodes

## Members
- [[.test_message_contains_significance()]] - code - tests/unit/test_unit_misc.py
- [[.test_message_contains_tickers()]] - code - tests/unit/test_unit_misc.py
- [[.test_message_within_char_limit()]] - code - tests/unit/test_unit_misc.py
- [[.test_very_long_message_truncated()]] - code - tests/unit/test_unit_misc.py
- [[All Claude prompt templates. Edit prompts HERE and nowhere else.]] - rationale - intelligence/prompts.py
- [[Assemble the full intelligence generation prompt from a context package dict.]] - rationale - intelligence/prompts.py
- [[CRITICAL TEST test_intelligence_cites_source_ids Intelligence quality — every g]] - rationale - tests/unit/test_intelligence_cites_source_ids.py
- [[Call Claude with assembled context package.     Post-generation validation stri]] - rationale - intelligence/engine.py
- [[Claude Prompt Templates (intelligenceprompts.py)]] - code - intelligence/prompts.py
- [[Extract and parse JSON from Claude's response.]] - rationale - intelligence/engine.py
- [[Format an IntelligenceObject as a Telegram message.     Max 3800 characters (Tel]] - rationale - delivery/telegram_bot.py
- [[Group articles by dominant topic. Simple priority-based clustering.]] - rationale - intelligence/engine.py
- [[IntelligenceObject generated from a context package must have     non-empty sour]] - rationale - tests/unit/test_intelligence_cites_source_ids.py
- [[Main intelligence loop — retrieves context, calls Claude, writes intelligence ob]] - rationale - intelligence/engine.py
- [[Main intelligence loop.     1. Fetch unprocessed high-significance articles from]] - rationale - intelligence/engine.py
- [[Post-generation validation     - Strip any ticker not present in context_packag]] - rationale - intelligence/engine.py
- [[Send a formatted message to the configured Telegram chat.     Retries 3x on netw]] - rationale - delivery/telegram_bot.py
- [[TestTelegramFormatter]] - code - tests/unit/test_unit_misc.py
- [[The DB INSERT for intelligence objects must include source_article_ids.]] - rationale - tests/unit/test_intelligence_cites_source_ids.py
- [[_cluster_by_topic()]] - code - intelligence/engine.py
- [[_get_client()]] - code - intelligence/engine.py
- [[_parse_claude_output()]] - code - intelligence/engine.py
- [[_validate_and_strip()]] - code - intelligence/engine.py
- [[build_intelligence_prompt()]] - code - intelligence/prompts.py
- [[engine.py]] - code - intelligence/engine.py
- [[format_analogues_block()]] - code - intelligence/prompts.py
- [[format_articles_block()]] - code - intelligence/prompts.py
- [[format_contradictions_block()]] - code - intelligence/prompts.py
- [[format_macro_block()]] - code - intelligence/prompts.py
- [[format_message()]] - code - delivery/telegram_bot.py
- [[format_prices_block()]] - code - intelligence/prompts.py
- [[format_regime_block()]] - code - intelligence/prompts.py
- [[generate_intelligence()]] - code - intelligence/engine.py
- [[prompts.py]] - code - intelligence/prompts.py
- [[push_message()]] - code - delivery/telegram_bot.py
- [[run_intelligence_cycle()]] - code - intelligence/engine.py
- [[test_intelligence_cites_source_ids()]] - code - tests/unit/test_intelligence_cites_source_ids.py
- [[test_intelligence_cites_source_ids.py]] - code - tests/unit/test_intelligence_cites_source_ids.py
- [[test_intelligence_source_ids_written_to_db()]] - code - tests/unit/test_intelligence_cites_source_ids.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Intelligence_Generation
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Core Config & Ingestion Hub]]
- 4 edges to [[_COMMUNITY_API Routes & Contradiction Detection]]
- 3 edges to [[_COMMUNITY_Service Entry & Delivery]]
- 3 edges to [[_COMMUNITY_External Data Fetching]]
- 1 edge to [[_COMMUNITY_FastAPI Layer]]
- 1 edge to [[_COMMUNITY_Signal Scoring]]
- 1 edge to [[_COMMUNITY_Macro & Regime Analysis]]

## Top bridge nodes
- [[engine.py]] - degree 13, connects to 3 communities
- [[run_intelligence_cycle()]] - degree 9, connects to 3 communities
- [[push_message()]] - degree 5, connects to 3 communities
- [[generate_intelligence()]] - degree 11, connects to 2 communities
- [[format_message()]] - degree 8, connects to 2 communities