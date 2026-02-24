"""
News theme definitions for article clustering.

Each commodity maps to a list of theme buckets.  A theme has:
- ``name``      : Domain-vocabulary label shown in the UI.
- ``keywords``  : Words / short phrases used for matching.

Commodities sharing a sector (e.g. all precious metals) reuse the
same base themes, with minor per-commodity tweaks where needed.
"""

from __future__ import annotations

# ------------------------------------------------------------------
# Theme bank per sector
# ------------------------------------------------------------------

_PRECIOUS_METALS_THEMES: list[dict] = [
    {
        "name": "Fed & Rate Policy",
        "keywords": [
            "fed", "federal reserve", "interest rate", "rate cut", "rate hike",
            "fomc", "monetary policy", "inflation", "cpi", "powell", "central bank",
            "dovish", "hawkish", "treasury", "yield", "bond",
        ],
    },
    {
        "name": "Geopolitical Tensions",
        "keywords": [
            "geopolitical", "war", "conflict", "sanctions", "russia", "ukraine",
            "china", "trade war", "tariff", "tension", "military", "missile",
            "iran", "middle east", "safe haven", "haven demand",
        ],
    },
    {
        "name": "Dollar & Currency",
        "keywords": [
            "dollar", "usd", "dxy", "currency", "forex", "exchange rate",
            "euro", "yen", "gbp", "pound", "rupee", "weakening", "strengthening",
        ],
    },
    {
        "name": "Investment & ETF Flows",
        "keywords": [
            "etf", "inflow", "outflow", "demand", "investment", "holdings",
            "reserve", "buying", "spdr", "gld", "slv", "futures", "speculative",
            "hedge fund", "allocation", "portfolio",
        ],
    },
    {
        "name": "Supply & Mining",
        "keywords": [
            "mining", "production", "supply", "output", "mine", "extraction",
            "refinery", "ore", "deposit", "exploration", "shortage",
        ],
    },
]

_ENERGY_THEMES: list[dict] = [
    {
        "name": "OPEC & Production",
        "keywords": [
            "opec", "production cut", "output", "quota", "saudi", "barrel",
            "supply cut", "opec+", "cartel", "compliance", "production increase",
        ],
    },
    {
        "name": "Geopolitical Supply Risk",
        "keywords": [
            "sanctions", "russia", "iran", "shipping", "tanker", "pipeline",
            "disruption", "conflict", "strait", "hormuz", "attack", "military",
            "ukraine", "embargo", "blockade", "reroute",
        ],
    },
    {
        "name": "Demand & Economic Outlook",
        "keywords": [
            "demand", "economic growth", "gdp", "recession", "consumption",
            "refinery", "inventory", "stockpile", "china demand", "india",
            "recovery", "slowdown", "manufacturing",
        ],
    },
    {
        "name": "US Policy & Shale",
        "keywords": [
            "shale", "drilling", "rig count", "strategic reserve", "spr",
            "policy", "permit", "us production", "eia", "api", "cushing",
        ],
    },
    {
        "name": "LNG & Global Trade",
        "keywords": [
            "lng", "export", "import", "trade", "europe", "asia", "henry hub",
            "cargo", "terminal", "liquefaction", "regasification", "spot",
        ],
    },
]

_AGRICULTURE_THEMES: list[dict] = [
    {
        "name": "Weather & Crop Conditions",
        "keywords": [
            "weather", "drought", "flood", "crop", "harvest", "yield",
            "planting", "condition", "frost", "heat", "rainfall", "growing season",
            "la nina", "el nino",
        ],
    },
    {
        "name": "Trade & Export",
        "keywords": [
            "export", "import", "trade", "tariff", "china", "shipment",
            "buyer", "tender", "cargo", "embargo", "trade deal", "shipping",
        ],
    },
    {
        "name": "USDA & Policy",
        "keywords": [
            "usda", "report", "subsidy", "policy", "farm bill", "ethanol",
            "biofuel", "mandate", "forecast", "estimate", "acres", "planted",
        ],
    },
    {
        "name": "Supply & Inventory",
        "keywords": [
            "supply", "inventory", "stockpile", "storage", "carryover",
            "stocks", "surplus", "deficit", "tightening", "balance sheet",
        ],
    },
]

# ------------------------------------------------------------------
# Map commodity keys to theme lists
# ------------------------------------------------------------------

COMMODITY_THEMES: dict[str, list[dict]] = {
    "gold": _PRECIOUS_METALS_THEMES,
    "silver": _PRECIOUS_METALS_THEMES,
    "platinum": _PRECIOUS_METALS_THEMES,
    "copper": [
        {
            "name": "China Demand & Stimulus",
            "keywords": [
                "china", "stimulus", "demand", "construction", "manufacturing",
                "infrastructure", "property", "real estate", "pmi",
                "economic growth", "recovery",
            ],
        },
        _PRECIOUS_METALS_THEMES[0],  # Fed & Rate Policy
        {
            "name": "Supply & Inventory",
            "keywords": [
                "supply", "inventory", "lme", "warehouse", "stockpile",
                "mining", "production", "shortage", "deficit", "surplus",
                "chile", "peru", "congo", "zambia", "smelter",
            ],
        },
        _PRECIOUS_METALS_THEMES[1],  # Geopolitical Tensions
        {
            "name": "Green Energy Transition",
            "keywords": [
                "ev", "electric vehicle", "renewable", "solar", "wind",
                "battery", "grid", "energy transition", "electrification",
                "copper demand", "wiring", "cable",
            ],
        },
    ],
    "crude_oil": _ENERGY_THEMES,
    "natural_gas": _ENERGY_THEMES,
    "wheat": _AGRICULTURE_THEMES,
    "corn": _AGRICULTURE_THEMES,
}
