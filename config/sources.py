"""All RSS feed URLs, API endpoints, and source trust tier assignments."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SourceFeed:
    id: str
    name: str
    feed_type: str          # rss | api | official
    url: str
    tier: int               # 1–4
    fetch_interval_minutes: int = 15
    topics: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Tier 1 — Official / Regulatory
# ---------------------------------------------------------------------------
TIER1_FEEDS: list[SourceFeed] = [
    SourceFeed(
        id="sec_edgar_8k",
        name="SEC EDGAR 8-K Filings",
        feed_type="official",
        url="https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&dateb=&owner=include&count=40&output=atom",
        tier=1,
        topics=["material_event"],
    ),
    SourceFeed(
        id="sec_edgar_10q",
        name="SEC EDGAR 10-Q Filings",
        feed_type="official",
        url="https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=10-Q&dateb=&owner=include&count=40&output=atom",
        tier=1,
        fetch_interval_minutes=60,
        topics=["earnings"],
    ),
    SourceFeed(
        id="sec_edgar_10k",
        name="SEC EDGAR 10-K Filings",
        feed_type="official",
        url="https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=10-K&dateb=&owner=include&count=40&output=atom",
        tier=1,
        fetch_interval_minutes=60,
        topics=["earnings"],
    ),
    SourceFeed(
        id="federal_reserve_news",
        name="Federal Reserve Press Releases",
        feed_type="rss",
        url="https://www.federalreserve.gov/feeds/press_all.xml",
        tier=1,
        topics=["monetary_policy", "macro"],
    ),
    SourceFeed(
        id="us_treasury_news",
        name="US Treasury Press Releases",
        feed_type="rss",
        url="https://home.treasury.gov/news/press-releases.xml",
        tier=1,
        topics=["fiscal_policy", "macro"],
    ),
    SourceFeed(
        id="bls_news",
        name="BLS Economic News Releases",
        feed_type="rss",
        url="https://www.bls.gov/feed/bls_latest.rss",
        tier=1,
        topics=["macro", "employment"],
    ),
]

# ---------------------------------------------------------------------------
# Tier 2A — Major Wire Services
# ---------------------------------------------------------------------------
TIER2A_FEEDS: list[SourceFeed] = [
    SourceFeed(
        id="reuters_business",
        name="Reuters Business News",
        feed_type="rss",
        url="https://feeds.reuters.com/reuters/businessNews",
        tier=2,
        topics=["business", "macro"],
    ),
    SourceFeed(
        id="reuters_markets",
        name="Reuters Markets",
        feed_type="rss",
        url="https://feeds.reuters.com/reuters/companyNews",
        tier=2,
        topics=["markets"],
    ),
    SourceFeed(
        id="ap_business",
        name="AP Business News",
        feed_type="rss",
        url="https://feeds.ap.org/rss/business.rss",
        tier=2,
        topics=["business", "macro"],
    ),
    SourceFeed(
        id="ft_markets",
        name="Financial Times Markets",
        feed_type="rss",
        url="https://www.ft.com/rss/home/uk",
        tier=2,
        topics=["markets", "macro"],
    ),
    SourceFeed(
        id="wsj_markets",
        name="Wall Street Journal Markets",
        feed_type="rss",
        url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        tier=2,
        topics=["markets"],
    ),
    SourceFeed(
        id="wsj_economy",
        name="Wall Street Journal Economy",
        feed_type="rss",
        url="https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
        tier=2,
        topics=["macro", "business"],
    ),
]

# ---------------------------------------------------------------------------
# Tier 2C — Financial Press
# ---------------------------------------------------------------------------
TIER2C_FEEDS: list[SourceFeed] = [
    SourceFeed(
        id="cnbc_finance",
        name="CNBC Finance",
        feed_type="rss",
        url="https://www.cnbc.com/id/10000664/device/rss/rss.html",
        tier=3,
        topics=["markets", "finance"],
    ),
    SourceFeed(
        id="cnbc_earnings",
        name="CNBC Earnings",
        feed_type="rss",
        url="https://www.cnbc.com/id/15839135/device/rss/rss.html",
        tier=3,
        topics=["earnings"],
    ),
    SourceFeed(
        id="marketwatch_top",
        name="MarketWatch Top Stories",
        feed_type="rss",
        url="https://feeds.marketwatch.com/marketwatch/topstories/",
        tier=3,
        topics=["markets", "business"],
    ),
    SourceFeed(
        id="marketwatch_realtimeheadlines",
        name="MarketWatch Real-Time Headlines",
        feed_type="rss",
        url="https://feeds.marketwatch.com/marketwatch/realtimeheadlines/",
        tier=3,
        topics=["markets"],
    ),
    SourceFeed(
        id="seeking_alpha_market_news",
        name="Seeking Alpha Market News",
        feed_type="rss",
        url="https://seekingalpha.com/market_currents.xml",
        tier=3,
        topics=["markets"],
    ),
    SourceFeed(
        id="zacks_commentary",
        name="Zacks Commentary",
        feed_type="rss",
        url="https://www.zacks.com/commentary/index.php?output=RSS",
        tier=3,
        topics=["earnings", "analysis"],
    ),
    SourceFeed(
        id="morningstar_news",
        name="Morningstar News",
        feed_type="rss",
        url="https://www.morningstar.com/rss/rss.aspx?section=articles",
        tier=3,
        topics=["analysis", "markets"],
    ),
    SourceFeed(
        id="investopedia_news",
        name="Investopedia News",
        feed_type="rss",
        url="https://www.investopedia.com/feeds/news.aspx",
        tier=3,
        topics=["markets", "education"],
    ),
    SourceFeed(
        id="yahoo_finance_news",
        name="Yahoo Finance News",
        feed_type="rss",
        url="https://finance.yahoo.com/news/rssindex",
        tier=3,
        topics=["markets", "business"],
    ),
    SourceFeed(
        id="benzinga_news",
        name="Benzinga News",
        feed_type="rss",
        url="https://www.benzinga.com/feeds/benzinga-newsfeed.xml",
        tier=3,
        topics=["markets", "earnings"],
    ),
    SourceFeed(
        id="thestreet_news",
        name="TheStreet News",
        feed_type="rss",
        url="https://www.thestreet.com/rss/01_latest_news.xml",
        tier=3,
        topics=["markets", "business"],
    ),
]

# ---------------------------------------------------------------------------
# Tier 2B — Google News RSS (per macro topic — tickers added dynamically from watchlist)
# ---------------------------------------------------------------------------
GOOGLE_NEWS_MACRO_QUERIES: list[dict] = [
    {"query": "Federal Reserve interest rates monetary policy", "topics": ["monetary_policy"]},
    {"query": "inflation CPI consumer prices", "topics": ["inflation", "macro"]},
    {"query": "US jobs report unemployment labor market", "topics": ["employment", "macro"]},
    {"query": "GDP economic growth recession", "topics": ["gdp", "macro"]},
    {"query": "earnings season corporate profits", "topics": ["earnings"]},
    {"query": "stock market crash rally volatility", "topics": ["markets", "volatility"]},
    {"query": "oil crude prices OPEC energy", "topics": ["energy", "macro"]},
    {"query": "US Treasury yields bond market", "topics": ["rates", "macro"]},
    {"query": "China economy trade tariffs", "topics": ["geopolitical", "macro"]},
    {"query": "bank failure credit crisis financial stability", "topics": ["financial_stability"]},
    {"query": "SEC enforcement regulation fintech crypto", "topics": ["regulation"]},
    {"query": "M&A merger acquisition deal", "topics": ["mergers_acquisitions"]},
    {"query": "IPO initial public offering listing", "topics": ["ipo"]},
    {"query": "semiconductor chips AI technology stocks", "topics": ["technology"]},
    {"query": "healthcare pharma drug FDA approval", "topics": ["healthcare"]},
]

# ---------------------------------------------------------------------------
# API Sources (fetched by api_fetcher.py, not RSS)
# ---------------------------------------------------------------------------
API_SOURCES: list[SourceFeed] = [
    SourceFeed(
        id="finnhub_company_news",
        name="Finnhub Company News",
        feed_type="api",
        url="https://finnhub.io/api/v1/company-news",
        tier=3,
        fetch_interval_minutes=60,
    ),
    SourceFeed(
        id="marketaux_news",
        name="Marketaux News",
        feed_type="api",
        url="https://api.marketaux.com/v1/news/all",
        tier=3,
        fetch_interval_minutes=60,
    ),
    SourceFeed(
        id="alpha_vantage_news",
        name="Alpha Vantage News Sentiment",
        feed_type="api",
        url="https://www.alphavantage.co/query",
        tier=3,
        fetch_interval_minutes=60,
    ),
]

# ---------------------------------------------------------------------------
# All feeds combined (RSS only — API sources handled separately)
# ---------------------------------------------------------------------------
ALL_RSS_FEEDS: list[SourceFeed] = TIER1_FEEDS + TIER2A_FEEDS + TIER2C_FEEDS

# FRED series IDs to bootstrap and sync
FRED_SERIES: list[dict] = [
    {"id": "FEDFUNDS",     "name": "Federal Funds Rate",          "frequency": "monthly"},
    {"id": "CPIAUCSL",     "name": "CPI All Urban Consumers",     "frequency": "monthly"},
    {"id": "T10Y2Y",       "name": "10Y-2Y Treasury Spread",      "frequency": "daily"},
    {"id": "VIXCLS",       "name": "CBOE Volatility Index",       "frequency": "daily"},
    {"id": "DGS10",        "name": "10-Year Treasury Yield",      "frequency": "daily"},
    {"id": "UNRATE",       "name": "Unemployment Rate",           "frequency": "monthly"},
    {"id": "DCOILWTICO",   "name": "WTI Crude Oil Price",         "frequency": "daily"},
    {"id": "M2SL",         "name": "M2 Money Supply",             "frequency": "monthly"},
    {"id": "BAMLH0A0HYM2", "name": "High Yield Credit Spread",    "frequency": "daily"},
]


def build_google_news_url(query: str, when: str = "1d") -> str:
    """Build a Google News RSS URL for a given search query."""
    import urllib.parse
    encoded = urllib.parse.quote_plus(query)
    return f"https://news.google.com/rss/search?q={encoded}&when={when}&hl=en-US&gl=US&ceid=US:en"
