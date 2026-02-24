"""
Integration tests — end-to-end flows through multiple modules.

Tests that the data layer, NLP layer, and chart layer can work together
without type mismatches or interface incompatibilities.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta


class TestDataToNlpPipeline:
    """Verify news articles from data/ can flow into nlp/ for analysis."""

    def test_scored_articles_have_expected_shape(self):
        from nlp.sentiment import SentimentScorer
        from config.commodities import COMMODITIES

        scorer = SentimentScorer()
        commodity = COMMODITIES["gold"]

        # Simulate articles as NewsFetcher would return them
        mock_articles = [
            {
                "title": "Gold prices surge to record highs",
                "description": "Investors flock to safe haven assets.",
                "source": "TestSource",
                "url": "http://example.com/1",
                "published_date": datetime.now(timezone.utc).isoformat(),
                "source_type": "rss",
            },
            {
                "title": "Gold drops as dollar strengthens",
                "description": "A strong dollar weighs on gold prices.",
                "source": "TestSource",
                "url": "http://example.com/2",
                "published_date": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat(),
                "source_type": "rss",
            },
        ]

        for article in mock_articles:
            scored = scorer.score_article(article, commodity["keywords"])
            # Original fields preserved
            assert scored["source"] == "TestSource"
            assert scored["source_type"] == "rss"
            # Sentiment fields added
            assert -1 <= scored["sentiment_score"] <= 1
            assert scored["sentiment_label"] in ("positive", "negative", "neutral")
            assert scored["keyword_hits"] >= 0

    def test_analyzer_produces_full_result(self):
        from nlp.analyzer import SentimentAnalyzer
        from config.commodities import COMMODITIES

        analyzer = SentimentAnalyzer()
        commodity = COMMODITIES["crude_oil"]

        mock_articles = [
            {
                "title": "OPEC cuts boost oil outlook",
                "description": "Supply cuts lead to bullish sentiment.",
                "published_date": datetime.now(timezone.utc).isoformat(),
            },
            {
                "title": "Oil demand fears grow",
                "description": "Global slowdown threatens oil consumption.",
                "published_date": (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat(),
            },
        ]

        result = analyzer.analyze(mock_articles, commodity_keywords=commodity["keywords"])

        assert len(result["scored_articles"]) == 2
        assert result["summary"]["article_count"] == 2
        assert isinstance(result["rolling"], list)
        assert result["trend"]["direction"] in ("improving", "declining", "stable")


class TestDataToChartsPipeline:
    """Verify price DataFrames from data/ can flow into dashboard/charts."""

    def test_normalized_df_works_with_price_chart(self):
        from data.price_fetcher import PriceFetcher
        from dashboard.charts import price_chart
        import plotly.graph_objects as go

        # Simulate PriceFetcher._normalize output
        data = {
            "Date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "Open": np.random.uniform(1800, 1900, 20),
            "High": np.random.uniform(1900, 2000, 20),
            "Low": np.random.uniform(1700, 1800, 20),
            "Close": np.random.uniform(1800, 1900, 20),
            "Volume": np.random.randint(1000, 5000, 20),
            "Change": np.random.randn(20) * 10,
            "Change_Pct": np.random.randn(20),
        }
        df = pd.DataFrame(data).set_index("Date")

        fig = price_chart(df, "gold", chart_type="line")
        assert isinstance(fig, go.Figure)

        fig_candle = price_chart(df, "gold", chart_type="candlestick")
        assert isinstance(fig_candle, go.Figure)


class TestNlpToChartsPipeline:
    """Verify NLP output can be fed into chart functions."""

    def test_sentiment_score_works_with_gauge(self):
        from nlp.analyzer import SentimentAnalyzer
        from dashboard.charts import sentiment_gauge
        import plotly.graph_objects as go

        analyzer = SentimentAnalyzer()
        articles = [{
            "title": "Gold hits new highs in amazing rally",
            "description": "Incredible bullish momentum.",
            "published_date": datetime.now(timezone.utc).isoformat(),
        }]

        result = analyzer.analyze(articles, commodity_keywords=["gold"])
        score = result["summary"]["weighted_avg"]
        label = result["summary"]["label"]

        fig = sentiment_gauge(score, label)
        assert isinstance(fig, go.Figure)

    def test_rolling_sentiment_works_with_correlation_timeline(self):
        from nlp.analyzer import SentimentAnalyzer
        from dashboard.charts import correlation_timeline
        import plotly.graph_objects as go

        # Create mock rolling data and convert to DataFrame
        analyzer = SentimentAnalyzer()
        now = datetime.now(timezone.utc)

        articles = [
            {
                "title": f"Article {i}",
                "description": f"Description for article {i}",
                "published_date": (now - timedelta(hours=i * 3)).isoformat(),
            }
            for i in range(10)
        ]

        result = analyzer.analyze(articles)

        # Build sentiment DataFrame from rolling buckets
        rolling = result["rolling"]
        if rolling:
            sent_data = {
                "Date": pd.to_datetime([b["window_end"] for b in rolling]),
                "sentiment": [b["avg_sentiment"] for b in rolling],
            }
            sentiment_df = pd.DataFrame(sent_data).set_index("Date")

            # Build a price DataFrame for the same period
            price_dates = pd.date_range(
                start=now - timedelta(hours=48),
                end=now,
                periods=len(rolling),
            )
            price_df = pd.DataFrame({
                "Close": np.random.uniform(1800, 1900, len(rolling)),
            }, index=price_dates)

            fig = correlation_timeline(price_df, sentiment_df, "gold")
            assert isinstance(fig, go.Figure)


class TestCacheIntegration:
    """Verify CacheManager works correctly with fetcher classes."""

    def test_cache_round_trip_with_json_data(self, tmp_path):
        from data.cache_manager import CacheManager

        cache = CacheManager(db_path=tmp_path / "test.db")

        # Simulate what PriceFetcher stores
        price_data = {
            "Date": ["2024-01-01", "2024-01-02"],
            "Close": [1900.5, 1905.3],
            "Volume": [1234, 5678],
        }
        cache.set_cached("prices:GC=F:30d", price_data)
        retrieved = cache.get_cached("prices:GC=F:30d", max_age=3600)
        assert retrieved == price_data

        # Simulate what NewsFetcher stores
        news_data = [
            {"title": "Test", "source": "RSS", "published_date": "2024-01-01T00:00:00+00:00"},
        ]
        cache.set_cached("news:gold", news_data)
        retrieved = cache.get_cached("news:gold", max_age=1800)
        assert retrieved == news_data

        cache.close()


class TestAllCommoditiesValid:
    """Validate that every commodity in the registry can be processed."""

    def test_all_commodities_can_be_scored(self):
        from config.commodities import COMMODITIES
        from nlp.sentiment import SentimentScorer

        scorer = SentimentScorer()
        for key, commodity in COMMODITIES.items():
            article = {
                "title": f"{commodity['name']} price update",
                "description": f"Latest news about {commodity['name']} market.",
            }
            result = scorer.score_article(article, commodity["keywords"])
            assert "sentiment_score" in result, f"Failed for {key}"

    def test_all_commodities_have_valid_tickers(self):
        from config.commodities import COMMODITIES
        for key, commodity in COMMODITIES.items():
            ticker = commodity["ticker"]
            assert isinstance(ticker, str), f"{key} ticker is not a string"
            assert len(ticker) > 0, f"{key} has empty ticker"
            assert "=" in ticker, f"{key} ticker {ticker!r} doesn't look like a futures ticker"
