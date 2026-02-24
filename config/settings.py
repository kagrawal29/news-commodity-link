"""
Application constants and configuration for the Commodity News x Price
Correlation Dashboard.

All tuneable knobs live here so the rest of the codebase stays free of
magic numbers.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# On Vercel (read-only filesystem), use /tmp for the SQLite cache.
if os.getenv("VERCEL"):
    CACHE_DB = Path("/tmp/commodity_cache.db")
else:
    CACHE_DB = PROJECT_ROOT / "commodity_cache.db"

# ---------------------------------------------------------------------------
# Cache durations (in seconds)
# ---------------------------------------------------------------------------
CACHE_DURATIONS = {
    "prices": 3600,       # 1 hour
    "news": 1800,         # 30 minutes
}

# ---------------------------------------------------------------------------
# API rate limits
# ---------------------------------------------------------------------------
API_RATE_LIMITS = {
    "gnews_daily": 100,   # max calls per calendar day
}

# ---------------------------------------------------------------------------
# Sentiment analysis thresholds (VADER compound score)
# ---------------------------------------------------------------------------
SENTIMENT_THRESHOLDS = {
    "positive": 0.05,     # compound > 0.05  -> positive
    "negative": -0.05,    # compound < -0.05 -> negative
    # anything in between is considered neutral
}

# ---------------------------------------------------------------------------
# Default timeframe options
# Maps a human-readable label to the yfinance period string and the
# appropriate interval granularity.
# ---------------------------------------------------------------------------
TIMEFRAME_OPTIONS = {
    "1d": {
        "label": "1 Day",
        "period": "1d",
        "interval": "5m",
    },
    "7d": {
        "label": "7 Days",
        "period": "5d",       # yfinance caps at 5d for intraday
        "interval": "15m",
    },
    "30d": {
        "label": "30 Days",
        "period": "1mo",
        "interval": "1h",
    },
    "90d": {
        "label": "90 Days",
        "period": "3mo",
        "interval": "1d",
    },
    "1y": {
        "label": "1 Year",
        "period": "1y",
        "interval": "1d",
    },
}

# ---------------------------------------------------------------------------
# Confidence score weights (must sum to 1.0)
# ---------------------------------------------------------------------------
CONFIDENCE_WEIGHTS = {
    "sentiment": 0.25,
    "keyword_relevance": 0.20,
    "news_volume": 0.20,
    "recency": 0.15,
    "historical_accuracy": 0.20,
}

# Quick sanity assertion -- keeps us honest if weights are tweaked later.
assert abs(sum(CONFIDENCE_WEIGHTS.values()) - 1.0) < 1e-9, (
    "CONFIDENCE_WEIGHTS must sum to 1.0"
)

# ---------------------------------------------------------------------------
# Dashboard colour scheme
# ---------------------------------------------------------------------------
COLORS = {
    "neon_cyan": "#00FFFF",
    "magenta": "#FF00FF",
    "gold": "#FFD700",
    "neon_green": "#00ff88",
    "electric_blue": "#00d4ff",
    "hot_pink": "#ff006e",
    "amber": "#ffbe0b",
    "purple": "#8338ec",
    "orange": "#FFA500",
    "lime": "#00FF00",

    # Semantic colours
    "positive": "#00ff88",     # neon green
    "negative": "#FF4444",     # red
    "neutral": "#888888",      # grey

    # Background / surface
    "bg_dark": "#0E1117",
    "bg_card": "#1A1A2E",
    "bg_highlight": "#16213E",

    # Text
    "text_primary": "#FFFFFF",
    "text_secondary": "#B0B0B0",
}
