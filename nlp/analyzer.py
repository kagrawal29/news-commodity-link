"""
Aggregate-level sentiment analysis across multiple scored articles.

Provides:
- Weighted average sentiment (recency-weighted)
- Rolling sentiment over configurable time windows
- Trend direction and magnitude
- Distribution breakdown (% positive / negative / neutral)
- Confidence scoring for the overall signal
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Optional

from config.settings import CONFIDENCE_WEIGHTS
from nlp.sentiment import SentimentScorer


class SentimentAnalyzer:
    """High-level sentiment aggregation over a list of news articles."""

    def __init__(self) -> None:
        self._scorer = SentimentScorer()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze(
        self,
        articles: list[dict],
        commodity_keywords: Optional[list[str]] = None,
    ) -> dict:
        """
        Score every article and return an aggregated summary dict.

        Parameters
        ----------
        articles : list[dict]
            Raw articles from ``NewsFetcher.fetch_news``.
        commodity_keywords : list[str] | None
            Commodity-specific keywords used for per-article boosting.

        Returns
        -------
        dict
            Keys: ``scored_articles``, ``summary``, ``rolling``, ``trend``.
        """
        if not articles:
            return self._empty_result()

        scored = [
            self._scorer.score_article(a, commodity_keywords)
            for a in articles
        ]

        summary = self._compute_summary(scored)
        rolling = self._compute_rolling(scored)
        trend = self._compute_trend(rolling)

        return {
            "scored_articles": scored,
            "summary": summary,
            "rolling": rolling,
            "trend": trend,
        }

    # ------------------------------------------------------------------
    # Summary statistics
    # ------------------------------------------------------------------

    def _compute_summary(self, scored: list[dict]) -> dict:
        """Weighted average, distribution, and confidence."""
        n = len(scored)
        if n == 0:
            return self._empty_summary()

        # --- recency-weighted average -----------------------------------
        now = datetime.now(timezone.utc)
        weights: list[float] = []
        scores: list[float] = []

        for art in scored:
            age_hours = self._article_age_hours(art, now)
            # Exponential decay: half-life = 24 hours.
            w = math.exp(-0.693 * age_hours / 24.0)
            weights.append(w)
            scores.append(art["sentiment_score"])

        total_w = sum(weights) or 1.0
        weighted_avg = sum(s * w for s, w in zip(scores, weights)) / total_w
        simple_avg = sum(scores) / n

        # --- distribution -----------------------------------------------
        pos_count = sum(1 for a in scored if a["sentiment_label"] == "positive")
        neg_count = sum(1 for a in scored if a["sentiment_label"] == "negative")
        neu_count = n - pos_count - neg_count

        # --- confidence --------------------------------------------------
        avg_keyword_rel = (
            sum(a.get("keyword_relevance", 0) for a in scored) / n
        )
        volume_score = min(n / 10, 1.0)  # 10+ articles = max volume score
        recency_score = weights[0] if weights else 0.0  # most-recent article's freshness

        confidence = (
            CONFIDENCE_WEIGHTS["sentiment"] * min(abs(weighted_avg) * 2, 1.0)
            + CONFIDENCE_WEIGHTS["keyword_relevance"] * avg_keyword_rel
            + CONFIDENCE_WEIGHTS["news_volume"] * volume_score
            + CONFIDENCE_WEIGHTS["recency"] * recency_score
            + CONFIDENCE_WEIGHTS["historical_accuracy"] * 0.5  # baseline
        )

        label = SentimentScorer._classify(weighted_avg)

        return {
            "weighted_avg": round(weighted_avg, 4),
            "simple_avg": round(simple_avg, 4),
            "label": label,
            "confidence": round(min(confidence, 1.0), 4),
            "article_count": n,
            "positive_count": pos_count,
            "negative_count": neg_count,
            "neutral_count": neu_count,
            "positive_pct": round(pos_count / n * 100, 1),
            "negative_pct": round(neg_count / n * 100, 1),
            "neutral_pct": round(neu_count / n * 100, 1),
        }

    # ------------------------------------------------------------------
    # Rolling sentiment (time-bucketed)
    # ------------------------------------------------------------------

    def _compute_rolling(
        self,
        scored: list[dict],
        window_hours: int = 6,
        num_windows: int = 8,
    ) -> list[dict]:
        """
        Bucket articles into ``num_windows`` time windows of
        ``window_hours`` hours each (most-recent first) and compute the
        average sentiment per bucket.
        """
        now = datetime.now(timezone.utc)
        buckets: list[dict] = []

        for i in range(num_windows):
            window_end = now - timedelta(hours=i * window_hours)
            window_start = window_end - timedelta(hours=window_hours)

            in_window = [
                a for a in scored
                if window_start <= self._parse_date(a) < window_end
            ]

            if in_window:
                avg = sum(a["sentiment_score"] for a in in_window) / len(in_window)
            else:
                avg = 0.0

            buckets.append({
                "window_start": window_start.isoformat(),
                "window_end": window_end.isoformat(),
                "avg_sentiment": round(avg, 4),
                "article_count": len(in_window),
            })

        # Return oldest-first for charting.
        buckets.reverse()
        return buckets

    # ------------------------------------------------------------------
    # Trend detection
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_trend(rolling: list[dict]) -> dict:
        """
        Simple linear-regression-style trend over the rolling windows.

        Returns direction ("improving", "declining", "stable") and a
        numeric slope.
        """
        # Use only windows with articles for a meaningful trend.
        points = [
            (i, b["avg_sentiment"])
            for i, b in enumerate(rolling)
            if b["article_count"] > 0
        ]

        if len(points) < 2:
            return {"direction": "stable", "slope": 0.0, "data_points": len(points)}

        n = len(points)
        sum_x = sum(p[0] for p in points)
        sum_y = sum(p[1] for p in points)
        sum_xy = sum(p[0] * p[1] for p in points)
        sum_x2 = sum(p[0] ** 2 for p in points)

        denom = n * sum_x2 - sum_x ** 2
        if denom == 0:
            slope = 0.0
        else:
            slope = (n * sum_xy - sum_x * sum_y) / denom

        if slope > 0.01:
            direction = "improving"
        elif slope < -0.01:
            direction = "declining"
        else:
            direction = "stable"

        return {
            "direction": direction,
            "slope": round(slope, 6),
            "data_points": n,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_date(article: dict) -> datetime:
        """Parse the ``published_date`` field to a timezone-aware datetime."""
        raw = article.get("published_date", "")
        if not raw:
            return datetime.now(timezone.utc)
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except (ValueError, TypeError):
            return datetime.now(timezone.utc)

    @staticmethod
    def _article_age_hours(article: dict, now: datetime) -> float:
        """Return the age of an article in hours."""
        dt = SentimentAnalyzer._parse_date(article)
        delta = now - dt
        return max(delta.total_seconds() / 3600.0, 0.0)

    @staticmethod
    def _empty_summary() -> dict:
        return {
            "weighted_avg": 0.0,
            "simple_avg": 0.0,
            "label": "neutral",
            "confidence": 0.0,
            "article_count": 0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "positive_pct": 0.0,
            "negative_pct": 0.0,
            "neutral_pct": 0.0,
        }

    @staticmethod
    def _empty_result() -> dict:
        return {
            "scored_articles": [],
            "summary": SentimentAnalyzer._empty_summary(),
            "rolling": [],
            "trend": {"direction": "stable", "slope": 0.0, "data_points": 0},
        }
