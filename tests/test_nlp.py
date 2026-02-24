"""
Tests for the NLP sentiment analysis module (nlp/).

Covers:
- SentimentScorer: VADER scoring, keyword boosting, classification
- SentimentAnalyzer: aggregation, rolling windows, trend detection
"""

import pytest
from datetime import datetime, timezone, timedelta


# ── Import tests ─────────────────────────────────────────────────────


class TestNlpImports:
    def test_import_nlp_package(self):
        from nlp import SentimentScorer, SentimentAnalyzer
        assert callable(SentimentScorer)
        assert callable(SentimentAnalyzer)

    def test_import_sentiment_module(self):
        from nlp.sentiment import SentimentScorer
        assert callable(SentimentScorer)

    def test_import_analyzer_module(self):
        from nlp.analyzer import SentimentAnalyzer
        assert callable(SentimentAnalyzer)


# ── SentimentScorer tests ────────────────────────────────────────────


class TestSentimentScorer:
    @pytest.fixture(autouse=True)
    def setup(self):
        from nlp.sentiment import SentimentScorer
        self.scorer = SentimentScorer()

    def test_instantiation(self):
        assert self.scorer is not None
        assert self.scorer._vader is not None

    def test_score_article_positive(self):
        article = {
            "title": "Gold prices surge to record highs amid strong demand",
            "description": "Investors are celebrating as gold reaches new all-time highs, driven by strong global demand and optimistic market outlook.",
        }
        result = self.scorer.score_article(article)
        assert "sentiment_score" in result
        assert "sentiment_label" in result
        assert result["sentiment_label"] == "positive"
        assert result["sentiment_score"] > 0

    def test_score_article_negative(self):
        article = {
            "title": "Oil prices crash as recession fears mount",
            "description": "Crude oil plummets amid growing fears of a global recession. Markets are in panic as demand collapses.",
        }
        result = self.scorer.score_article(article)
        assert result["sentiment_label"] == "negative"
        assert result["sentiment_score"] < 0

    def test_score_article_preserves_original_fields(self):
        article = {
            "title": "Test article",
            "description": "Test description",
            "url": "http://example.com",
            "source": "TestSource",
        }
        result = self.scorer.score_article(article)
        assert result["url"] == "http://example.com"
        assert result["source"] == "TestSource"
        assert result["title"] == "Test article"

    def test_score_article_does_not_mutate_original(self):
        article = {"title": "Test", "description": "Test"}
        original_keys = set(article.keys())
        self.scorer.score_article(article)
        assert set(article.keys()) == original_keys

    def test_keyword_boosting(self):
        article = {
            "title": "Gold price rises slightly today",
            "description": "Gold futures and XAUUSD are up.",
        }
        keywords = ["gold price", "gold futures", "XAUUSD"]
        result = self.scorer.score_article(article, commodity_keywords=keywords)
        assert result["keyword_hits"] >= 2
        assert result["keyword_relevance"] > 0

    def test_keyword_relevance_range(self):
        article = {
            "title": "Gold silver copper platinum",
            "description": "All metals mentioned here.",
        }
        keywords = ["gold", "silver", "copper", "platinum"]
        result = self.scorer.score_article(article, commodity_keywords=keywords)
        assert 0 <= result["keyword_relevance"] <= 1.0

    def test_score_text_method(self):
        result = self.scorer.score_text("This is absolutely wonderful and amazing!")
        assert "compound" in result
        assert "label" in result
        assert result["label"] == "positive"
        assert result["compound"] > 0

    def test_score_text_negative(self):
        result = self.scorer.score_text("This is terrible, horrible, and awful.")
        assert result["label"] == "negative"
        assert result["compound"] < 0

    def test_classify_thresholds(self):
        from nlp.sentiment import SentimentScorer
        assert SentimentScorer._classify(0.1) == "positive"
        assert SentimentScorer._classify(-0.1) == "negative"
        assert SentimentScorer._classify(0.0) == "neutral"
        assert SentimentScorer._classify(0.04) == "neutral"
        assert SentimentScorer._classify(-0.04) == "neutral"

    def test_empty_article(self):
        article = {"title": "", "description": ""}
        result = self.scorer.score_article(article)
        assert "sentiment_score" in result
        assert "sentiment_label" in result


# ── SentimentAnalyzer tests ──────────────────────────────────────────


class TestSentimentAnalyzer:
    @pytest.fixture(autouse=True)
    def setup(self):
        from nlp.analyzer import SentimentAnalyzer
        self.analyzer = SentimentAnalyzer()

    def test_instantiation(self):
        assert self.analyzer is not None
        assert self.analyzer._scorer is not None

    def test_empty_articles_returns_empty_result(self):
        result = self.analyzer.analyze([])
        assert result["scored_articles"] == []
        assert result["summary"]["article_count"] == 0
        assert result["summary"]["label"] == "neutral"
        assert result["trend"]["direction"] == "stable"

    def test_analyze_single_article(self):
        articles = [{
            "title": "Gold surges to record highs",
            "description": "Gold prices hit all-time highs.",
            "published_date": datetime.now(timezone.utc).isoformat(),
        }]
        result = self.analyzer.analyze(articles, commodity_keywords=["gold"])
        assert result["summary"]["article_count"] == 1
        assert len(result["scored_articles"]) == 1
        assert "sentiment_score" in result["scored_articles"][0]

    def test_analyze_multiple_articles(self):
        now = datetime.now(timezone.utc)
        articles = [
            {
                "title": "Oil prices crash sharply in worst day",
                "description": "Markets panic as oil falls.",
                "published_date": (now - timedelta(hours=1)).isoformat(),
            },
            {
                "title": "Oil prices recover slightly from lows",
                "description": "Some recovery in oil markets today.",
                "published_date": now.isoformat(),
            },
            {
                "title": "OPEC announces production cuts to support prices",
                "description": "Great news for oil bulls as supply tightens.",
                "published_date": (now - timedelta(hours=3)).isoformat(),
            },
        ]
        result = self.analyzer.analyze(articles)

        summary = result["summary"]
        assert summary["article_count"] == 3
        assert summary["positive_count"] + summary["negative_count"] + summary["neutral_count"] == 3
        assert abs(summary["positive_pct"] + summary["negative_pct"] + summary["neutral_pct"] - 100.0) < 0.5

    def test_summary_has_all_required_fields(self):
        articles = [{
            "title": "Test",
            "description": "Test",
            "published_date": datetime.now(timezone.utc).isoformat(),
        }]
        result = self.analyzer.analyze(articles)
        summary = result["summary"]
        required_keys = {
            "weighted_avg", "simple_avg", "label", "confidence",
            "article_count", "positive_count", "negative_count", "neutral_count",
            "positive_pct", "negative_pct", "neutral_pct",
        }
        assert required_keys.issubset(set(summary.keys()))

    def test_confidence_in_range(self):
        articles = [{
            "title": "Gold is great",
            "description": "Gold prices wonderful",
            "published_date": datetime.now(timezone.utc).isoformat(),
        }]
        result = self.analyzer.analyze(articles, commodity_keywords=["gold"])
        assert 0 <= result["summary"]["confidence"] <= 1.0

    def test_rolling_returns_list(self):
        articles = [{
            "title": "Test article",
            "description": "Some text here",
            "published_date": datetime.now(timezone.utc).isoformat(),
        }]
        result = self.analyzer.analyze(articles)
        assert isinstance(result["rolling"], list)

    def test_trend_has_required_fields(self):
        articles = [{
            "title": "Test",
            "description": "Test",
            "published_date": datetime.now(timezone.utc).isoformat(),
        }]
        result = self.analyzer.analyze(articles)
        trend = result["trend"]
        assert "direction" in trend
        assert "slope" in trend
        assert "data_points" in trend
        assert trend["direction"] in ("improving", "declining", "stable")

    def test_compute_trend_stable_with_few_points(self):
        from nlp.analyzer import SentimentAnalyzer
        rolling = [
            {"avg_sentiment": 0.0, "article_count": 0},
            {"avg_sentiment": 0.0, "article_count": 0},
        ]
        trend = SentimentAnalyzer._compute_trend(rolling)
        assert trend["direction"] == "stable"
        assert trend["data_points"] == 0

    def test_compute_trend_improving(self):
        from nlp.analyzer import SentimentAnalyzer
        rolling = [
            {"avg_sentiment": -0.5, "article_count": 3},
            {"avg_sentiment": -0.2, "article_count": 2},
            {"avg_sentiment": 0.1, "article_count": 4},
            {"avg_sentiment": 0.4, "article_count": 3},
        ]
        trend = SentimentAnalyzer._compute_trend(rolling)
        assert trend["direction"] == "improving"
        assert trend["slope"] > 0

    def test_compute_trend_declining(self):
        from nlp.analyzer import SentimentAnalyzer
        rolling = [
            {"avg_sentiment": 0.5, "article_count": 2},
            {"avg_sentiment": 0.2, "article_count": 3},
            {"avg_sentiment": -0.1, "article_count": 2},
            {"avg_sentiment": -0.4, "article_count": 1},
        ]
        trend = SentimentAnalyzer._compute_trend(rolling)
        assert trend["direction"] == "declining"
        assert trend["slope"] < 0
