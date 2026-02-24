"""
Smoke tests for the data layer.

Verifies that all modules import cleanly, classes instantiate without
errors, and basic method calls don't crash.  These tests use a
temporary SQLite database so they never touch the production cache.
"""

import tempfile
import os
from pathlib import Path

import pytest
import pandas as pd


# ── Module import tests ──────────────────────────────────────────────


class TestImports:
    """Every module in config/ and data/ should import without errors."""

    def test_import_settings(self):
        from config import settings
        assert hasattr(settings, "CACHE_DURATIONS")
        assert hasattr(settings, "TIMEFRAME_OPTIONS")
        assert hasattr(settings, "CONFIDENCE_WEIGHTS")
        assert hasattr(settings, "COLORS")

    def test_import_commodities(self):
        from config.commodities import COMMODITIES
        assert isinstance(COMMODITIES, dict)
        assert len(COMMODITIES) > 0

    def test_import_cache_manager(self):
        from data.cache_manager import CacheManager
        assert callable(CacheManager)

    def test_import_price_fetcher(self):
        from data.price_fetcher import PriceFetcher
        assert callable(PriceFetcher)

    def test_import_news_fetcher(self):
        from data.news_fetcher import NewsFetcher
        assert callable(NewsFetcher)


# ── Config validation tests ──────────────────────────────────────────


class TestConfig:
    """Validate config values are well-formed."""

    def test_confidence_weights_sum_to_one(self):
        from config.settings import CONFIDENCE_WEIGHTS
        assert abs(sum(CONFIDENCE_WEIGHTS.values()) - 1.0) < 1e-9

    def test_cache_durations_are_positive(self):
        from config.settings import CACHE_DURATIONS
        for key, val in CACHE_DURATIONS.items():
            assert val > 0, f"CACHE_DURATIONS[{key!r}] must be positive"

    def test_timeframe_options_have_required_keys(self):
        from config.settings import TIMEFRAME_OPTIONS
        for tf_key, tf_val in TIMEFRAME_OPTIONS.items():
            assert "label" in tf_val, f"Missing 'label' in TIMEFRAME_OPTIONS[{tf_key!r}]"
            assert "period" in tf_val, f"Missing 'period' in TIMEFRAME_OPTIONS[{tf_key!r}]"
            assert "interval" in tf_val, f"Missing 'interval' in TIMEFRAME_OPTIONS[{tf_key!r}]"

    def test_commodities_have_required_fields(self):
        from config.commodities import COMMODITIES
        required = {"name", "ticker", "keywords", "rss_feeds", "icon"}
        for key, commodity in COMMODITIES.items():
            missing = required - set(commodity.keys())
            assert not missing, f"Commodity {key!r} missing fields: {missing}"


# ── CacheManager tests ───────────────────────────────────────────────


class TestCacheManager:
    """Smoke tests for CacheManager using a temp database."""

    @pytest.fixture(autouse=True)
    def setup_cache(self, tmp_path):
        from data.cache_manager import CacheManager
        self.db_path = tmp_path / "test_cache.db"
        self.cache = CacheManager(db_path=self.db_path)
        yield
        self.cache.close()

    def test_instantiation(self):
        assert self.cache is not None
        assert Path(self.cache.db_path).exists()

    def test_set_and_get(self):
        self.cache.set_cached("test:key", {"foo": "bar"})
        result = self.cache.get_cached("test:key", max_age=60)
        assert result == {"foo": "bar"}

    def test_cache_miss_returns_none(self):
        result = self.cache.get_cached("nonexistent:key", max_age=60)
        assert result is None

    def test_expired_cache_returns_none(self):
        self.cache.set_cached("old:key", {"old": True})
        # Force expiry by requesting max_age=0
        result = self.cache.get_cached("old:key", max_age=0)
        assert result is None

    def test_api_budget_tracking(self):
        assert self.cache.has_api_budget("gnews") is True
        count = self.cache.get_api_calls_today("gnews")
        assert count == 0

        new_count = self.cache.increment_api_calls("gnews")
        assert new_count == 1
        assert self.cache.get_api_calls_today("gnews") == 1

    def test_clear_all(self):
        self.cache.set_cached("a", [1, 2, 3])
        self.cache.set_cached("b", [4, 5, 6])
        self.cache.clear_all()
        assert self.cache.get_cached("a", max_age=60) is None
        assert self.cache.get_cached("b", max_age=60) is None

    def test_cleanup_expired(self):
        # Just ensure it doesn't crash
        removed = self.cache.cleanup_expired()
        assert isinstance(removed, int)


# ── PriceFetcher tests ───────────────────────────────────────────────


class TestPriceFetcher:
    """Smoke tests for PriceFetcher (no live API calls)."""

    @pytest.fixture(autouse=True)
    def setup_fetcher(self, tmp_path):
        from data.cache_manager import CacheManager
        from data.price_fetcher import PriceFetcher
        cache = CacheManager(db_path=tmp_path / "test_cache.db")
        self.fetcher = PriceFetcher(cache=cache)
        self.cache = cache
        yield
        cache.close()

    def test_instantiation(self):
        assert self.fetcher is not None
        assert self.fetcher.cache is not None

    def test_unknown_timeframe_returns_empty_df(self):
        df = self.fetcher.fetch_prices("GC=F", timeframe="invalid")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_normalize_static_method(self):
        from data.price_fetcher import PriceFetcher
        # Create a minimal DataFrame that mimics yfinance output
        data = {
            "Date": pd.date_range("2024-01-01", periods=5, freq="D"),
            "Open": [100.0, 101.0, 102.0, 103.0, 104.0],
            "High": [101.0, 102.0, 103.0, 104.0, 105.0],
            "Low": [99.0, 100.0, 101.0, 102.0, 103.0],
            "Close": [100.5, 101.5, 102.5, 103.5, 104.5],
            "Volume": [1000, 1100, 1200, 1300, 1400],
        }
        hist = pd.DataFrame(data).set_index("Date")
        result = PriceFetcher._normalize(hist)

        assert "Date" in result.columns
        assert "Change" in result.columns
        assert "Change_Pct" in result.columns
        assert len(result) == 5

    def test_get_latest_price_with_empty_cache(self):
        # Without live API, this will attempt a fetch and likely return None
        # or empty -- either outcome is acceptable for a smoke test.
        result = self.fetcher.get_latest_price("FAKE_TICKER_XYZ")
        # Just ensure it doesn't crash; result may be None or a dict
        assert result is None or isinstance(result, dict)


# ── NewsFetcher tests ────────────────────────────────────────────────


class TestNewsFetcher:
    """Smoke tests for NewsFetcher (no live API calls)."""

    @pytest.fixture(autouse=True)
    def setup_fetcher(self, tmp_path):
        from data.cache_manager import CacheManager
        from data.news_fetcher import NewsFetcher
        cache = CacheManager(db_path=tmp_path / "test_cache.db")
        self.fetcher = NewsFetcher(cache=cache)
        self.cache = cache
        yield
        cache.close()

    def test_instantiation(self):
        assert self.fetcher is not None
        assert self.fetcher.cache is not None

    def test_normalize_title(self):
        from data.news_fetcher import NewsFetcher
        assert NewsFetcher._normalize_title("  Hello, World!  ") == "hello world"
        assert NewsFetcher._normalize_title("Gold price: $2000/oz") == "gold price 2000oz"
        assert NewsFetcher._normalize_title("") == ""

    def test_parse_date_valid(self):
        from data.news_fetcher import NewsFetcher
        result = NewsFetcher._parse_date("2024-01-15T10:30:00Z")
        assert "2024-01-15" in result

    def test_parse_date_empty(self):
        from data.news_fetcher import NewsFetcher
        result = NewsFetcher._parse_date("")
        # Should return current timestamp as fallback
        assert isinstance(result, str)
        assert len(result) > 0

    def test_merge_and_deduplicate(self):
        from data.news_fetcher import NewsFetcher
        articles = [
            {"title": "Gold hits new high", "source_type": "rss", "url": "a"},
            {"title": "Gold hits new high!", "source_type": "gnews", "url": "b"},
            {"title": "Oil prices drop sharply", "source_type": "rss", "url": "c"},
        ]
        merged = NewsFetcher._merge_and_deduplicate(articles)
        assert len(merged) == 2
        # The gnews version should be preferred for the duplicate
        gold_articles = [a for a in merged if "gold" in a["title"].lower()]
        assert len(gold_articles) == 1
        assert gold_articles[0]["source_type"] == "gnews"

    def test_fetch_news_empty_keywords_and_feeds(self):
        # With no keywords and no feeds, should return empty list
        result = self.fetcher.fetch_news(
            keywords=[],
            rss_feeds=[],
            commodity_key="test",
            max_results=5,
        )
        assert isinstance(result, list)
        assert len(result) == 0
