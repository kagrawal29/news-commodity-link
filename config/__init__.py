"""Configuration package for the Commodity News x Price Correlation Dashboard."""

from config.settings import (
    CACHE_DB,
    CACHE_DURATIONS,
    API_RATE_LIMITS,
    SENTIMENT_THRESHOLDS,
    TIMEFRAME_OPTIONS,
    CONFIDENCE_WEIGHTS,
    COLORS,
)
from config.commodities import COMMODITIES

__all__ = [
    "CACHE_DB",
    "CACHE_DURATIONS",
    "API_RATE_LIMITS",
    "SENTIMENT_THRESHOLDS",
    "TIMEFRAME_OPTIONS",
    "CONFIDENCE_WEIGHTS",
    "COLORS",
    "COMMODITIES",
]
