"""spaCy + regex ticker extraction. Three-pass approach."""
import re
from functools import lru_cache
from typing import Optional

from config.log import get_logger

from config.watchlist import EQUITY_TICKERS, COMPANY_NAME_OVERRIDES

log = get_logger(__name__)

# Explicit ticker patterns in text: $AAPL, NYSE:AAPL, NASDAQ:AAPL
_EXPLICIT_PATTERN = re.compile(
    r"\$([A-Z]{1,5})\b|(?:NYSE|NASDAQ|AMEX|NYSEARCA):\s*([A-Z]{1,5})\b"
)

# Valid ticker set for validation
_VALID_TICKERS = set(EQUITY_TICKERS)

# Company name → ticker map (loaded lazily)
_COMPANY_MAP: dict[str, str] | None = None


def build_company_ticker_map() -> dict[str, str]:
    """
    Build and cache a map from company name variants to ticker symbols.
    Sources: static COMPANY_NAME_OVERRIDES + yfinance ticker.info for watchlist.
    Refreshed weekly.
    """
    global _COMPANY_MAP
    mapping: dict[str, str] = {}

    # Start with manual overrides (highest priority)
    for name, ticker in COMPANY_NAME_OVERRIDES.items():
        if ticker and name:
            mapping[name.lower()] = ticker
            mapping[name.upper()] = ticker

    # Supplement with yfinance longName (best-effort, fails silently)
    for ticker in EQUITY_TICKERS:
        try:
            import yfinance as yf
            info = yf.Ticker(ticker).info
            long_name = info.get("longName") or info.get("shortName")
            if long_name:
                mapping[long_name.lower()] = ticker
                # Add without Inc/Corp/Ltd suffixes
                clean = re.sub(r"\b(Inc|Corp|Ltd|LLC|Co|Company|Holdings|Group)\.?\b", "", long_name, flags=re.I).strip()
                if clean and len(clean) > 3:
                    mapping[clean.lower()] = ticker
        except Exception:
            pass

    _COMPANY_MAP = mapping
    return mapping


def _get_company_map() -> dict[str, str]:
    global _COMPANY_MAP
    if _COMPANY_MAP is None:
        _COMPANY_MAP = {}
        for name, ticker in COMPANY_NAME_OVERRIDES.items():
            if ticker and name:
                _COMPANY_MAP[name.lower()] = ticker
    return _COMPANY_MAP


@lru_cache(maxsize=1)
def _load_spacy():
    try:
        import spacy
        return spacy.load("en_core_web_sm")
    except Exception:
        return None


def extract_tickers(text: str) -> list[str]:
    """
    Multi-pass ticker extraction:
    1. Regex for explicit $TICKER and NYSE:TICKER patterns
    2. spaCy entity recognition for organization names → company map lookup
    3. Title keyword matching against watchlist company names

    Returns deduplicated, validated ticker list.
    """
    found: set[str] = set()

    # Pass 1 — explicit regex
    for m in _EXPLICIT_PATTERN.finditer(text):
        ticker = m.group(1) or m.group(2)
        if ticker and ticker in _VALID_TICKERS:
            found.add(ticker)

    # Pass 2 — spaCy NER
    nlp = _load_spacy()
    if nlp:
        try:
            doc = nlp(text[:5000])
            company_map = _get_company_map()
            for ent in doc.ents:
                if ent.label_ in ("ORG", "PRODUCT"):
                    candidate = ent.text.strip().lower()
                    ticker = company_map.get(candidate)
                    if ticker and ticker in _VALID_TICKERS:
                        found.add(ticker)
        except Exception as e:
            log.debug("ticker.spacy_failed", error=str(e))

    # Pass 3 — title keyword matching against watchlist company names
    company_map = _get_company_map()
    text_lower = text.lower()
    for name, ticker in company_map.items():
        if not ticker or ticker not in _VALID_TICKERS:
            continue
        if len(name) < 4:
            continue
        if name in text_lower:
            found.add(ticker)

    # Always include tickers explicitly mentioned as uppercase sequences
    for ticker in _VALID_TICKERS:
        if re.search(rf"\b{re.escape(ticker)}\b", text):
            found.add(ticker)

    return sorted(found)
