"""Deterministic market regime classification from macro data."""
from datetime import datetime, timezone

from config.log import get_logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from models.schemas import MacroSnapshot

log = get_logger(__name__)


def classify_regime(macro: MacroSnapshot) -> dict:
    """
    Apply deterministic rules to classify current market regime across all 4 dimensions.
    Writes to regime_snapshots table via caller.
    Returns RegimeSnapshot dict.
    """
    volatility = _classify_volatility(macro.vix)
    liquidity = _classify_liquidity(macro.fed_funds_rate, macro.m2, macro.hy_spread)
    macro_regime = _classify_macro(macro.t10y2y_spread, macro.cpi, macro.unrate)
    sentiment = _classify_sentiment(macro.vix, macro.t10y2y_spread)
    confidence = _compute_confidence(macro)

    notes_parts = []
    if macro.vix is not None:
        notes_parts.append(f"VIX={macro.vix:.1f}")
    if macro.fed_funds_rate is not None:
        notes_parts.append(f"FEDFUNDS={macro.fed_funds_rate:.2f}%")
    if macro.t10y2y_spread is not None:
        notes_parts.append(f"10Y-2Y={macro.t10y2y_spread:.2f}%")

    return {
        "snapshot_at": datetime.now(timezone.utc),
        "volatility_regime": volatility,
        "liquidity_regime": liquidity,
        "macro_regime": macro_regime,
        "sentiment_regime": sentiment,
        "vix_value": macro.vix,
        "yield_curve_spread": macro.t10y2y_spread,
        "fed_funds_rate": macro.fed_funds_rate,
        "confidence": confidence,
        "notes": " | ".join(notes_parts) if notes_parts else None,
    }


def _classify_volatility(vix: float | None) -> str:
    if vix is None:
        return "normal"
    if vix < 15:
        return "compressed"
    if vix < 25:
        return "normal"
    if vix < 35:
        return "elevated"
    return "panic"


def _classify_liquidity(
    fed_funds: float | None,
    m2: float | None,
    hy_spread: float | None,
) -> str:
    stress_signals = 0
    ease_signals = 0

    if fed_funds is not None:
        if fed_funds > 5.0:
            stress_signals += 1
        elif fed_funds < 1.0:
            ease_signals += 1

    if hy_spread is not None:
        # HY spread in percentage points
        if hy_spread > 6.0:
            stress_signals += 2   # stressed credit = strong stress signal
        elif hy_spread > 4.0:
            stress_signals += 1
        elif hy_spread < 3.0:
            ease_signals += 1

    if stress_signals >= 2:
        return "stressed"
    if stress_signals == 1:
        return "tightening"
    if ease_signals >= 1:
        return "loose"
    return "normal"


def _classify_macro(
    t10y2y: float | None,
    cpi: float | None,
    unrate: float | None,
) -> str:
    # Inverted yield curve + high unemployment = recession risk
    if t10y2y is not None and t10y2y < 0:
        if unrate is not None and unrate > 5.0:
            return "recession_risk"

    # High CPI + slow growth signals = stagflation
    if cpi is not None and cpi > 200:   # CPIAUCSL index level
        if t10y2y is not None and t10y2y < 0.5:
            return "stagflation"

    # Positive yield curve + falling inflation = disinflation / expansion
    if t10y2y is not None and t10y2y > 0.5:
        return "expansion"

    if cpi is not None and t10y2y is not None and t10y2y > 0:
        return "disinflation"

    return "expansion"


def _classify_sentiment(vix: float | None, t10y2y: float | None) -> str:
    if vix is None:
        return "neutral"
    if vix > 40:
        return "fearful"
    if vix > 30:
        return "pessimistic"
    if vix > 20:
        if t10y2y is not None and t10y2y < 0:
            return "pessimistic"
        return "neutral"
    if vix < 13:
        return "euphoric"
    if vix < 17:
        return "optimistic"
    return "neutral"


def _compute_confidence(macro: MacroSnapshot) -> float:
    """Confidence based on how many macro series have current data."""
    fields = [
        macro.fed_funds_rate, macro.cpi, macro.t10y2y_spread,
        macro.vix, macro.dgs10, macro.unrate,
    ]
    available = sum(1 for f in fields if f is not None)
    return round(available / len(fields), 2)


async def get_latest_regime(session: AsyncSession) -> dict | None:
    """Fetch most recent regime snapshot from DB."""
    result = await session.execute(
        text("""
            SELECT volatility_regime, liquidity_regime, macro_regime, sentiment_regime,
                   vix_value, yield_curve_spread, fed_funds_rate, confidence, snapshot_at
            FROM regime_snapshots
            ORDER BY snapshot_at DESC LIMIT 1
        """)
    )
    row = result.fetchone()
    if not row:
        return None
    return {
        "volatility_regime": row[0],
        "liquidity_regime": row[1],
        "macro_regime": row[2],
        "sentiment_regime": row[3],
        "vix_value": float(row[4]) if row[4] is not None else None,
        "yield_curve_spread": float(row[5]) if row[5] is not None else None,
        "fed_funds_rate": float(row[6]) if row[6] is not None else None,
        "confidence": float(row[7]) if row[7] is not None else None,
        "snapshot_at": row[8],
    }


async def run_regime_classification(session: AsyncSession) -> dict:
    """Full classification pipeline: fetch macro → classify → persist."""
    from datetime import datetime, timezone
    from ingestion.macro_fetcher import get_macro_snapshot

    now = datetime.now(timezone.utc)
    macro = await get_macro_snapshot(now, session)
    regime = classify_regime(macro)

    await session.execute(
        text("""
            INSERT INTO regime_snapshots
                (snapshot_at, volatility_regime, liquidity_regime, macro_regime,
                 sentiment_regime, vix_value, yield_curve_spread, fed_funds_rate,
                 confidence, notes)
            VALUES
                (:snapshot_at, :volatility_regime, :liquidity_regime, :macro_regime,
                 :sentiment_regime, :vix_value, :yield_curve_spread, :fed_funds_rate,
                 :confidence, :notes)
        """),
        regime,
    )

    log.info(
        "regime.classified",
        volatility=regime["volatility_regime"],
        liquidity=regime["liquidity_regime"],
        macro=regime["macro_regime"],
        sentiment=regime["sentiment_regime"],
    )
    return regime
