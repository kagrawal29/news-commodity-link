"""
Commodity registry.

Each entry maps a short key to a dict containing everything the dashboard
needs to fetch prices and news for that commodity.

Fields
------
name : str
    Human-readable display name.
ticker : str
    yfinance futures ticker symbol.
keywords : list[str]
    Search terms used when querying GNews and filtering RSS items.
rss_feeds : list[str]
    Public RSS/Atom feed URLs relevant to the commodity.  These are
    always available (no API key required) and act as the primary
    fallback when the GNews budget is exhausted.
icon : str
    Emoji shown next to the commodity in the UI.
"""

# Google News RSS search — reliable, always fresh, commodity-specific.
_GNEWS_RSS = "https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q="

COMMODITIES: dict[str, dict] = {
    "gold": {
        "name": "Gold",
        "ticker": "GC=F",
        "keywords": [
            "gold price",
            "gold market",
            "gold futures",
            "gold trading",
            "XAUUSD",
        ],
        "rss_feeds": [
            f"{_GNEWS_RSS}gold+price+futures",                                  # Google News — Gold
            "https://www.mining.com/feed/",                                      # Mining.com — metals & mining

            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=GC=F",          # Yahoo Finance — Gold futures
        ],
        "icon": "\U0001f947",  # gold medal
    },
    "silver": {
        "name": "Silver",
        "ticker": "SI=F",
        "keywords": [
            "silver price",
            "silver market",
            "silver futures",
            "silver trading",
            "XAGUSD",
        ],
        "rss_feeds": [
            f"{_GNEWS_RSS}silver+price+market",                                  # Google News — Silver
            "https://www.mining.com/feed/",                                      # Mining.com — metals & mining

            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=SI=F",          # Yahoo Finance — Silver futures
        ],
        "icon": "\U0001f948",  # silver medal
    },
    "crude_oil": {
        "name": "Crude Oil",
        "ticker": "CL=F",
        "keywords": [
            "crude oil price",
            "oil market",
            "WTI crude",
            "oil futures",
            "Brent crude",
            "OPEC",
        ],
        "rss_feeds": [
            "https://oilprice.com/rss/main",                                    # OilPrice.com — energy
            f"{_GNEWS_RSS}crude+oil+price+WTI",                                 # Google News — Crude Oil

            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=CL=F",          # Yahoo Finance — Oil futures
        ],
        "icon": "\U0001f6e2\ufe0f",  # oil drum
    },
    "natural_gas": {
        "name": "Natural Gas",
        "ticker": "NG=F",
        "keywords": [
            "natural gas price",
            "natural gas market",
            "natural gas futures",
            "LNG",
            "Henry Hub",
        ],
        "rss_feeds": [
            "https://oilprice.com/rss/main",                                    # OilPrice.com — energy
            f"{_GNEWS_RSS}natural+gas+price+LNG",                               # Google News — Natural Gas

            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=NG=F",          # Yahoo Finance — NatGas futures
        ],
        "icon": "\U0001f525",  # fire
    },
    "copper": {
        "name": "Copper",
        "ticker": "HG=F",
        "keywords": [
            "copper price",
            "copper market",
            "copper futures",
            "copper trading",
        ],
        "rss_feeds": [
            f"{_GNEWS_RSS}copper+price+market",                                 # Google News — Copper
            "https://www.mining.com/feed/",                                      # Mining.com — metals & mining

            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=HG=F",          # Yahoo Finance — Copper futures
        ],
        "icon": "\U0001fa99",  # coin (copper)
    },
    "platinum": {
        "name": "Platinum",
        "ticker": "PL=F",
        "keywords": [
            "platinum price",
            "platinum market",
            "platinum futures",
            "platinum trading",
        ],
        "rss_feeds": [
            f"{_GNEWS_RSS}platinum+price+futures",                               # Google News — Platinum
            "https://www.mining.com/feed/",                                      # Mining.com — metals & mining

            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=PL=F",          # Yahoo Finance — Platinum futures
        ],
        "icon": "\u2728",  # sparkles
    },
    "wheat": {
        "name": "Wheat",
        "ticker": "ZW=F",
        "keywords": [
            "wheat price",
            "wheat market",
            "wheat futures",
            "grain market",
            "wheat trading",
        ],
        "rss_feeds": [
            f"{_GNEWS_RSS}wheat+price+futures+grain",                            # Google News — Wheat
            "https://www.feedstuffs.com/rss.xml",                                # Feedstuffs — agriculture

            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=ZW=F",          # Yahoo Finance — Wheat futures
        ],
        "icon": "\U0001f33e",  # sheaf of rice
    },
    "corn": {
        "name": "Corn",
        "ticker": "ZC=F",
        "keywords": [
            "corn price",
            "corn market",
            "corn futures",
            "grain market",
            "corn trading",
        ],
        "rss_feeds": [
            f"{_GNEWS_RSS}corn+price+futures+CBOT",                             # Google News — Corn
            "https://www.feedstuffs.com/rss.xml",                                # Feedstuffs — agriculture

            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=ZC=F",          # Yahoo Finance — Corn futures
        ],
        "icon": "\U0001f33d",  # ear of corn
    },
}
