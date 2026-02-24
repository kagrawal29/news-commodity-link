"""
Keyword-based article clustering by commodity-specific themes.

Groups scored articles into thematic clusters using the keyword banks
defined in ``config.themes``.  Each cluster includes aggregate sentiment,
a time window, and a divergence flag when sentiment conflicts with the
price movement over the same window.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from datetime import datetime, timezone
from typing import Optional


from config.themes import COMMODITY_THEMES


class ArticleClusterer:
    """Group scored articles into theme-based clusters."""

    # Maximum clusters to return per request.
    MAX_CLUSTERS = 4

    # Minimum keyword hits for an article to be assigned to a theme.
    MIN_KEYWORD_HITS = 1

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def cluster(
        self,
        scored_articles: list[dict],
        commodity_key: str,
        price_data: Optional[list[dict]] = None,
    ) -> list[dict]:
        """
        Group *scored_articles* into theme clusters for *commodity_key*.

        Parameters
        ----------
        scored_articles : list[dict]
            Articles already enriched by ``SentimentScorer.score_article``.
        commodity_key : str
            Key into ``COMMODITY_THEMES`` (e.g. ``"gold"``).
        price_data : list[dict] | None
            Historical price records (need ``Date`` and ``Close`` fields)
            for computing price deltas per cluster time window.

        Returns
        -------
        list[dict]
            Up to ``MAX_CLUSTERS`` cluster dicts, ranked by relevance.
        """
        themes = COMMODITY_THEMES.get(commodity_key, [])
        if not themes or not scored_articles:
            return []

        # 1. Match each article against every theme's keywords.
        theme_buckets: dict[str, list[dict]] = {t["name"]: [] for t in themes}
        theme_keywords: dict[str, list[str]] = {
            t["name"]: t["keywords"] for t in themes
        }
        # Track keyword hits per theme for the description field.
        theme_keyword_hits: dict[str, Counter] = {
            t["name"]: Counter() for t in themes
        }

        for article in scored_articles:
            text = self._article_text(article)
            best_theme: Optional[str] = None
            best_hits = 0
            best_matched: list[str] = []

            for theme_name, keywords in theme_keywords.items():
                matched = self._matched_keywords(text, keywords)
                if len(matched) >= self.MIN_KEYWORD_HITS and len(matched) > best_hits:
                    best_hits = len(matched)
                    best_theme = theme_name
                    best_matched = matched

            if best_theme is not None:
                theme_buckets[best_theme].append(article)
                for kw in best_matched:
                    theme_keyword_hits[best_theme][kw] += 1

        # 2. Build cluster objects for non-empty buckets.
        clusters: list[dict] = []
        for theme_name, articles in theme_buckets.items():
            if not articles:
                continue

            sentiment_scores = [a["sentiment_score"] for a in articles]
            sentiment_avg = sum(sentiment_scores) / len(sentiment_scores)

            # Classify aggregate
            if sentiment_avg >= 0.05:
                sentiment_label = "positive"
            elif sentiment_avg <= -0.05:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"

            # Time window
            dates = [self._parse_date(a) for a in articles]
            start_time = min(dates)
            end_time = max(dates)

            # Price delta over this cluster's time window
            price_delta = None
            price_delta_pct = None
            if price_data:
                price_delta, price_delta_pct = self._compute_price_delta(
                    price_data, start_time, end_time
                )

            # Divergence detection
            divergence = None
            if price_delta is not None:
                divergence = self._detect_divergence(
                    sentiment_avg, sentiment_label, price_delta
                )

            # Transparency description: explain which keywords matched
            description = self._build_description(
                theme_keyword_hits[theme_name], len(articles)
            )

            clusters.append({
                "theme": theme_name,
                "description": description,
                "article_count": len(articles),
                "sentiment_avg": round(sentiment_avg, 4),
                "sentiment_label": sentiment_label,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "price_delta": round(price_delta, 2) if price_delta is not None else None,
                "price_delta_pct": round(price_delta_pct, 2) if price_delta_pct is not None else None,
                "divergence": divergence,
                "articles": [
                    {
                        "title": a["title"],
                        "source": a.get("source", ""),
                        "url": a.get("url", ""),
                        "published_date": a.get("published_date", ""),
                        "sentiment_score": a["sentiment_score"],
                        "sentiment_label": a["sentiment_label"],
                    }
                    for a in sorted(
                        articles,
                        key=lambda x: abs(x["sentiment_score"]),
                        reverse=True,
                    )
                ],
            })

        # 3. Rank: weight volume more than intensity per Raj's conviction
        #    model (theme convergence > single strong signal).
        clusters.sort(
            key=lambda c: math.pow(c["article_count"], 1.5) * abs(c["sentiment_avg"]),
            reverse=True,
        )
        return clusters[: self.MAX_CLUSTERS]

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _article_text(article: dict) -> str:
        """Get searchable text from an article."""
        title = article.get("title", "") or ""
        description = article.get("description", "") or ""
        return f"{title} {description}".lower()

    @staticmethod
    def _matched_keywords(text: str, keywords: list[str]) -> list[str]:
        """Return the distinct keywords that appear in text."""
        return [
            kw for kw in keywords
            if re.search(re.escape(kw.lower()), text)
        ]

    @staticmethod
    def _build_description(keyword_counts: Counter, article_count: int) -> str:
        """
        Build a human-readable description of why articles matched this theme.

        E.g. "3 articles mention sanctions, 2 mention shipping disruptions"
        """
        if not keyword_counts:
            return f"{article_count} article{'s' if article_count != 1 else ''} matched this theme"

        # Take top 3 keywords by frequency
        top = keyword_counts.most_common(3)
        parts = []
        for kw, count in top:
            if count == 1:
                parts.append(f"1 article mentions {kw}")
            else:
                parts.append(f"{count} articles mention {kw}")

        return ", ".join(parts)

    @staticmethod
    def _parse_date(article: dict) -> datetime:
        """Parse published_date to timezone-aware datetime."""
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
    def _compute_price_delta(
        price_data: list[dict],
        start_time: datetime,
        end_time: datetime,
    ) -> tuple[Optional[float], Optional[float]]:
        """
        Compute the price change over a time window.

        Returns (absolute_delta, percentage_delta) or (None, None).
        """
        if not price_data:
            return None, None

        # Find closest price records to start and end
        start_price = None
        end_price = None

        for record in price_data:
            record_date = record.get("Date", "")
            if not record_date:
                continue
            try:
                if isinstance(record_date, str):
                    rd = datetime.fromisoformat(
                        record_date.replace("Z", "+00:00")
                    )
                else:
                    rd = record_date
                if rd.tzinfo is None:
                    rd = rd.replace(tzinfo=timezone.utc)
            except (ValueError, TypeError):
                continue

            close = record.get("Close")
            if close is None:
                continue

            if start_price is None or rd <= start_time:
                start_price = float(close)
            if rd <= end_time:
                end_price = float(close)

        if start_price is None or end_price is None or start_price == 0:
            # Fallback: use first and last price in dataset
            try:
                start_price = float(price_data[0]["Close"])
                end_price = float(price_data[-1]["Close"])
            except (KeyError, IndexError, TypeError):
                return None, None

        if start_price == 0:
            return None, None

        delta = end_price - start_price
        delta_pct = (delta / start_price) * 100
        return delta, delta_pct

    @staticmethod
    def _detect_divergence(
        sentiment_avg: float,
        sentiment_label: str,
        price_delta: float,
    ) -> Optional[str]:
        """
        Detect when sentiment direction conflicts with price movement.

        Returns a human-readable divergence label or None.
        """
        if sentiment_label == "neutral":
            return None

        # Bullish sentiment but price falling
        if sentiment_avg > 0.1 and price_delta < -0.5:
            return "News: BULLISH / Price: DECLINING"

        # Bearish sentiment but price rising
        if sentiment_avg < -0.1 and price_delta > 0.5:
            return "News: BEARISH / Price: RISING"

        return None
