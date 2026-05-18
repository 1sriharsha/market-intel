"""All Claude prompt templates. Edit prompts HERE and nowhere else."""

SYSTEM_PROMPT = """You are a market intelligence analyst. Your sole job is to synthesize factual \
information from a provided context package into compressed, high-signal intelligence.

STRICT RULES:
1. Reason ONLY from facts present in the context package. Do not use prior knowledge.
2. Explicitly state what is UNKNOWN or UNVERIFIED in the unknowns field.
3. Identify contradictions between price behavior and narrative.
4. Express confidence as a float 0.0–1.0 with a written explanation.
5. Never fabricate tickers, numbers, or events not present in the context.
6. If data is insufficient to form a view, say so explicitly.
7. Do not make price predictions or trading recommendations."""


INTELLIGENCE_GENERATION_PROMPT = """Analyze the following market intelligence context and produce a \
structured intelligence object.

=== CONTEXT PACKAGE ===

CURRENT DATE/TIME: {current_dt}

ARTICLES ({article_count} articles, significance threshold passed):
{articles_block}

PRICE MOVEMENTS (relevant tickers, last 5 days):
{prices_block}

MACRO SNAPSHOT (as of {macro_as_of}):
{macro_block}

CURRENT MARKET REGIME:
{regime_block}

HISTORICAL ANALOGUES (top 3 similar past events):
{analogues_block}

ACTIVE CONTRADICTIONS DETECTED:
{contradictions_block}

=== INSTRUCTIONS ===

Produce a JSON object with exactly these fields:
{{
  "summary": "<compressed 2-3 sentence summary of what is happening and why it matters>",
  "why_it_matters": "<1-2 paragraphs: systemic implications, second-order effects, what changes>",
  "historical_context": "<comparison to analogues: what happened then, what was different, what was same>",
  "contradictions": "<any detected contradictions between narrative and price action, or 'None detected'>",
  "risks": "<1-3 scenarios that would invalidate this analysis>",
  "unknowns": "<explicit list of missing data, unverified claims, or open questions>",
  "confidence_score": <float 0.0–1.0>,
  "confidence_explanation": "<why confidence is at this level: what is certain vs uncertain>",
  "significance_level": "<critical|high|medium|low>",
  "tickers": [<list of tickers directly relevant to this intelligence — ONLY from context>],
  "topics": [<list of topics from context>]
}}

significance_level criteria:
- critical: Systemic risk, major Fed action, market structure event
- high: Material earnings, significant macro data, sector-moving event
- medium: Contextually relevant, corroborating signal
- low: Weak signal, insufficient corroboration

Output ONLY valid JSON. No preamble, no explanation outside the JSON."""


def format_articles_block(articles: list[dict]) -> str:
    if not articles:
        return "No articles in context."
    lines = []
    for i, a in enumerate(articles, 1):
        lines.append(
            f"[{i}] SOURCE: {a.get('source_name', 'Unknown')} "
            f"(Tier {a.get('source_tier', '?')}) | "
            f"PUBLISHED: {a.get('published_at', 'Unknown')} | "
            f"SCORE: {a.get('significance_score', 'N/A')}\n"
            f"    TITLE: {a.get('title', '')}\n"
            f"    SUMMARY: {(a.get('summary') or '')[:300]}"
        )
    return "\n\n".join(lines)


def format_prices_block(prices: list[dict]) -> str:
    if not prices:
        return "No price data available."
    lines = []
    for p in prices:
        lines.append(
            f"{p.get('ticker')}: ${p.get('close', 'N/A')} "
            f"(date: {p.get('date', 'N/A')})"
        )
    return "\n".join(lines)


def format_macro_block(macro: dict) -> str:
    if not macro:
        return "No macro data available."
    return (
        f"Fed Funds Rate: {macro.get('fed_funds_rate', 'N/A')}%\n"
        f"CPI (YoY): {macro.get('cpi', 'N/A')}\n"
        f"10Y-2Y Spread: {macro.get('t10y2y_spread', 'N/A')}%\n"
        f"VIX: {macro.get('vix', 'N/A')}\n"
        f"10Y Treasury: {macro.get('dgs10', 'N/A')}%\n"
        f"Unemployment: {macro.get('unrate', 'N/A')}%\n"
        f"WTI Oil: ${macro.get('oil_price', 'N/A')}\n"
        f"HY Credit Spread: {macro.get('hy_spread', 'N/A')} bps"
    )


def format_regime_block(regime: dict | None) -> str:
    if not regime:
        return "No regime classification available."
    return (
        f"Volatility: {regime.get('volatility_regime', 'N/A')} "
        f"(VIX: {regime.get('vix_value', 'N/A')})\n"
        f"Liquidity: {regime.get('liquidity_regime', 'N/A')}\n"
        f"Macro: {regime.get('macro_regime', 'N/A')}\n"
        f"Sentiment: {regime.get('sentiment_regime', 'N/A')}\n"
        f"Confidence: {regime.get('confidence', 'N/A')}"
    )


def format_analogues_block(analogues: list[dict]) -> str:
    if not analogues:
        return "No historical analogues found."
    lines = []
    for i, a in enumerate(analogues, 1):
        lines.append(
            f"[{i}] DATE: {a.get('event_date')} | "
            f"CATEGORY: {a.get('event_category', 'N/A')} | "
            f"GOLDSTEIN: {a.get('goldstein_scale', 'N/A')} | "
            f"TONE: {a.get('avg_tone', 'N/A')}\n"
            f"    TICKERS: {', '.join(a.get('tickers_affected') or []) or 'N/A'}\n"
            f"    PRICE REACTION: {a.get('price_reaction_summary', 'N/A')}"
        )
    return "\n\n".join(lines)


def format_contradictions_block(contradictions: list[dict]) -> str:
    if not contradictions:
        return "None detected."
    lines = []
    for c in contradictions:
        lines.append(
            f"TYPE: {c.get('contradiction_type')} | "
            f"SEVERITY: {c.get('severity', 'N/A')} | "
            f"TICKER: {c.get('ticker', 'N/A')}\n"
            f"  {c.get('description', '')}"
        )
    return "\n".join(lines)


def build_intelligence_prompt(context_package: dict) -> str:
    """Assemble the full intelligence generation prompt from a context package dict."""
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    macro = context_package.get("macro_snapshot", {})
    macro_as_of = macro.get("as_of", "unknown") if macro else "unknown"

    return INTELLIGENCE_GENERATION_PROMPT.format(
        current_dt=now,
        article_count=len(context_package.get("articles", [])),
        articles_block=format_articles_block(context_package.get("articles", [])),
        prices_block=format_prices_block(context_package.get("price_movements", [])),
        macro_block=format_macro_block(macro),
        macro_as_of=macro_as_of,
        regime_block=format_regime_block(context_package.get("regime")),
        analogues_block=format_analogues_block(context_package.get("historical_analogues", [])),
        contradictions_block=format_contradictions_block(
            context_package.get("active_contradictions", [])
        ),
    )
