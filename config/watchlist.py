"""Tickers and macro topics being monitored. Add tickers here + run bootstrap."""

# Core equity watchlist — major indices, sectors, high-signal individual names
EQUITY_TICKERS: list[str] = [
    # Index ETFs
    "SPY", "QQQ", "IWM", "DIA", "VTI",
    # Sector ETFs
    "XLF", "XLK", "XLE", "XLV", "XLI", "XLC", "XLY", "XLP", "XLU", "XLRE", "XLB",
    # Mega-cap tech
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AVGO", "ORCL", "AMD",
    # Financials
    "JPM", "BAC", "GS", "MS", "WFC", "C", "BLK", "SCHW",
    # Healthcare
    "UNH", "JNJ", "LLY", "ABBV", "MRK", "PFE", "TMO",
    # Energy
    "XOM", "CVX", "COP", "EOG", "SLB",
    # Consumer
    "WMT", "HD", "COST", "MCD", "NKE", "SBUX",
    # Industrials / macro-sensitive
    "CAT", "DE", "BA", "GE", "HON",
    # Communication
    "NFLX", "DIS", "CMCSA", "T", "VZ",
    # Market benchmarks (for beta computation)
    "SPY", "TLT", "GLD", "UUP",
]

# Deduplicate while preserving order
_seen: set[str] = set()
EQUITY_TICKERS = [t for t in EQUITY_TICKERS if not (_seen.add(t) or t in _seen)]

# Macro reference assets (price tracked but not in news watchlist)
MACRO_TICKERS: list[str] = [
    "^VIX",    # VIX
    "^TNX",    # 10yr yield
    "^TYX",    # 30yr yield
    "GC=F",    # Gold futures
    "CL=F",    # Crude oil futures
    "DX-Y.NYB", # Dollar index
]

# All tickers for price bootstrap
ALL_TICKERS: list[str] = EQUITY_TICKERS + MACRO_TICKERS

# Topics used for Google News RSS queries and article classification
MACRO_TOPICS: list[str] = [
    "monetary_policy",
    "inflation",
    "employment",
    "gdp",
    "earnings",
    "markets",
    "volatility",
    "energy",
    "rates",
    "geopolitical",
    "financial_stability",
    "regulation",
    "mergers_acquisitions",
    "ipo",
    "technology",
    "healthcare",
    "material_event",
    "insider_activity",
    "macro",
    "fiscal_policy",
    "analysis",
    "business",
    "finance",
]

# Company name → ticker mapping for NLP extraction (supplements yfinance lookup)
COMPANY_NAME_OVERRIDES: dict[str, str] = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Nvidia": "NVDA",
    "Google": "GOOGL",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "Meta": "META",
    "Facebook": "META",
    "Tesla": "TSLA",
    "Broadcom": "AVGO",
    "Oracle": "ORCL",
    "Advanced Micro Devices": "AMD",
    "JPMorgan": "JPM",
    "JPMorgan Chase": "JPM",
    "Bank of America": "BAC",
    "Goldman Sachs": "GS",
    "Morgan Stanley": "MS",
    "Wells Fargo": "WFC",
    "Citigroup": "C",
    "Citi": "C",
    "BlackRock": "BLK",
    "Charles Schwab": "SCHW",
    "UnitedHealth": "UNH",
    "Johnson & Johnson": "JNJ",
    "Eli Lilly": "LLY",
    "AbbVie": "ABBV",
    "Merck": "MRK",
    "Pfizer": "PFE",
    "Thermo Fisher": "TMO",
    "ExxonMobil": "XOM",
    "Chevron": "CVX",
    "ConocoPhillips": "COP",
    "Walmart": "WMT",
    "Home Depot": "HD",
    "Costco": "COST",
    "McDonald's": "MCD",
    "Nike": "NKE",
    "Starbucks": "SBUX",
    "Caterpillar": "CAT",
    "Deere": "DE",
    "John Deere": "DE",
    "Boeing": "BA",
    "General Electric": "GE",
    "Honeywell": "HON",
    "Netflix": "NFLX",
    "Disney": "DIS",
    "Comcast": "CMCSA",
    "AT&T": "T",
    "Verizon": "VZ",
    "Federal Reserve": None,  # not a ticker — suppress
    "Fed": None,
    "Treasury": None,
    "SEC": None,
    "Congress": None,
}
