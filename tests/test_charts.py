"""
Tests for the chart module (dashboard/charts.py).

Verifies that each chart function returns a valid Plotly Figure
without crashing on typical inputs.
"""

import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# ── Import tests ─────────────────────────────────────────────────────


class TestChartImports:
    def test_import_charts_module(self):
        from dashboard import charts
        assert hasattr(charts, "price_chart")
        assert hasattr(charts, "sentiment_gauge")
        assert hasattr(charts, "correlation_timeline")
        assert hasattr(charts, "commodity_card_sparkline")
        assert hasattr(charts, "sentiment_heatmap")
        assert hasattr(charts, "multi_commodity_overlay")
        assert hasattr(charts, "news_volume_chart")

    def test_neon_palette_defined(self):
        from dashboard.charts import NEON, NEON_CYCLE
        assert isinstance(NEON, dict)
        assert len(NEON) > 0
        assert isinstance(NEON_CYCLE, list)
        assert len(NEON_CYCLE) > 0


# ── Helper fixtures ──────────────────────────────────────────────────

@pytest.fixture
def sample_price_df():
    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    np.random.seed(42)
    close = 100 + np.cumsum(np.random.randn(30) * 2)
    return pd.DataFrame({
        "Date": dates,
        "Open": close - 1,
        "High": close + 2,
        "Low": close - 2,
        "Close": close,
        "Volume": np.random.randint(1000, 5000, 30),
    }).set_index("Date")


@pytest.fixture
def sample_sentiment_df():
    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    np.random.seed(42)
    return pd.DataFrame({
        "sentiment": np.random.uniform(-1, 1, 30),
    }, index=dates)


# ── Price chart tests ────────────────────────────────────────────────


class TestPriceChart:
    def test_line_chart_returns_figure(self, sample_price_df):
        from dashboard.charts import price_chart
        fig = price_chart(sample_price_df, "gold", chart_type="line")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_candlestick_chart_returns_figure(self, sample_price_df):
        from dashboard.charts import price_chart
        fig = price_chart(sample_price_df, "gold", chart_type="candlestick")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_unknown_commodity_key(self, sample_price_df):
        from dashboard.charts import price_chart
        fig = price_chart(sample_price_df, "unknown_commodity", chart_type="line")
        assert isinstance(fig, go.Figure)


# ── Sentiment gauge tests ────────────────────────────────────────────


class TestSentimentGauge:
    def test_positive_gauge(self):
        from dashboard.charts import sentiment_gauge
        fig = sentiment_gauge(0.75, "Gold Sentiment")
        assert isinstance(fig, go.Figure)

    def test_negative_gauge(self):
        from dashboard.charts import sentiment_gauge
        fig = sentiment_gauge(-0.5, "Oil Sentiment")
        assert isinstance(fig, go.Figure)

    def test_neutral_gauge(self):
        from dashboard.charts import sentiment_gauge
        fig = sentiment_gauge(0.0, "Neutral")
        assert isinstance(fig, go.Figure)

    def test_extreme_values(self):
        from dashboard.charts import sentiment_gauge
        fig_pos = sentiment_gauge(1.0, "Max Positive")
        fig_neg = sentiment_gauge(-1.0, "Max Negative")
        assert isinstance(fig_pos, go.Figure)
        assert isinstance(fig_neg, go.Figure)


# ── Correlation timeline tests ───────────────────────────────────────


class TestCorrelationTimeline:
    def test_returns_figure(self, sample_price_df, sample_sentiment_df):
        from dashboard.charts import correlation_timeline
        fig = correlation_timeline(sample_price_df, sample_sentiment_df, "gold")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_without_commodity_key(self, sample_price_df, sample_sentiment_df):
        from dashboard.charts import correlation_timeline
        fig = correlation_timeline(sample_price_df, sample_sentiment_df)
        assert isinstance(fig, go.Figure)


# ── Sparkline tests ──────────────────────────────────────────────────


class TestSparkline:
    def test_with_series(self):
        from dashboard.charts import commodity_card_sparkline
        prices = pd.Series([100, 101, 102, 103, 104])
        fig = commodity_card_sparkline(prices, "gold")
        assert isinstance(fig, go.Figure)

    def test_with_list(self):
        from dashboard.charts import commodity_card_sparkline
        fig = commodity_card_sparkline([100, 99, 98, 97], "crude_oil", color_idx=2)
        assert isinstance(fig, go.Figure)

    def test_single_value(self):
        from dashboard.charts import commodity_card_sparkline
        fig = commodity_card_sparkline([100], "silver")
        assert isinstance(fig, go.Figure)


# ── Heatmap tests ────────────────────────────────────────────────────


class TestSentimentHeatmap:
    def test_returns_figure(self):
        from dashboard.charts import sentiment_heatmap
        data = {
            "Gold": [0.3, -0.2, 0.1],
            "Oil": [-0.5, 0.4, 0.0],
            "Silver": [0.1, 0.2, -0.3],
        }
        df = pd.DataFrame(data, index=["Day 1", "Day 2", "Day 3"])
        fig = sentiment_heatmap(df)
        assert isinstance(fig, go.Figure)


# ── Multi commodity overlay tests ────────────────────────────────────


class TestMultiCommodityOverlay:
    def test_normalized(self, sample_price_df):
        from dashboard.charts import multi_commodity_overlay
        price_dict = {
            "gold": sample_price_df,
            "silver": sample_price_df * 0.5,
        }
        fig = multi_commodity_overlay(price_dict, normalize=True)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_not_normalized(self, sample_price_df):
        from dashboard.charts import multi_commodity_overlay
        price_dict = {"gold": sample_price_df}
        fig = multi_commodity_overlay(price_dict, normalize=False)
        assert isinstance(fig, go.Figure)


# ── News volume chart tests ──────────────────────────────────────────


class TestNewsVolumeChart:
    def test_returns_figure(self):
        from dashboard.charts import news_volume_chart
        data = {
            "Gold": [5, 3, 8],
            "Oil": [10, 7, 4],
        }
        df = pd.DataFrame(data, index=["Mon", "Tue", "Wed"])
        fig = news_volume_chart(df)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2
