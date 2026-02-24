"""
Per-article sentiment scoring using VADER with commodity-keyword boosting.

Each article receives:
- ``sentiment_score``  : float in [-1, +1] (VADER compound, optionally boosted)
- ``sentiment_label``  : "positive" | "negative" | "neutral"
- ``keyword_hits``     : int -- how many commodity keywords appear in the text
- ``keyword_relevance``: float in [0, 1] -- ratio of keywords that matched
"""

from __future__ import annotations

import re
from typing import Optional

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from config.settings import SENTIMENT_THRESHOLDS


class SentimentScorer:
    """VADER-based sentiment scorer with commodity-keyword boosting."""

    # How much each keyword hit nudges the compound score toward its sign.
    _KEYWORD_BOOST = 0.05
    # Cap so boosting can never flip the sign by more than +-0.15.
    _MAX_BOOST = 0.15

    def __init__(self) -> None:
        self._vader = SentimentIntensityAnalyzer()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def score_article(
        self,
        article: dict,
        commodity_keywords: Optional[list[str]] = None,
    ) -> dict:
        """
        Return a **new** dict that is *article* enriched with sentiment
        fields.  The original dict is not mutated.

        Parameters
        ----------
        article : dict
            Must contain at least ``title`` and ``description`` strings.
        commodity_keywords : list[str] | None
            Keywords from ``config.commodities.COMMODITIES[key]["keywords"]``.
            When provided, keyword hits boost the raw compound score.
        """
        text = self._article_text(article)
        commodity_keywords = commodity_keywords or []

        # --- base VADER score -------------------------------------------
        scores = self._vader.polarity_scores(text)
        compound = scores["compound"]

        # --- keyword boosting -------------------------------------------
        keyword_hits = self._count_keyword_hits(text, commodity_keywords)
        total_keywords = len(commodity_keywords) if commodity_keywords else 1
        keyword_relevance = min(keyword_hits / total_keywords, 1.0)

        if keyword_hits > 0 and compound != 0.0:
            boost = min(keyword_hits * self._KEYWORD_BOOST, self._MAX_BOOST)
            # Nudge in the direction of the existing sentiment.
            compound += boost if compound > 0 else -boost
            # Clamp to [-1, +1].
            compound = max(-1.0, min(1.0, compound))

        # --- classify ---------------------------------------------------
        label = self._classify(compound)

        return {
            **article,
            "sentiment_score": round(compound, 4),
            "sentiment_label": label,
            "sentiment_pos": round(scores["pos"], 4),
            "sentiment_neg": round(scores["neg"], 4),
            "sentiment_neu": round(scores["neu"], 4),
            "keyword_hits": keyword_hits,
            "keyword_relevance": round(keyword_relevance, 4),
        }

    def score_text(self, text: str) -> dict:
        """Score arbitrary text (no keyword boosting). Returns VADER dict."""
        scores = self._vader.polarity_scores(text)
        return {
            "compound": round(scores["compound"], 4),
            "pos": round(scores["pos"], 4),
            "neg": round(scores["neg"], 4),
            "neu": round(scores["neu"], 4),
            "label": self._classify(scores["compound"]),
        }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _article_text(article: dict) -> str:
        """Concatenate the useful text fields from a news article."""
        title = article.get("title", "") or ""
        description = article.get("description", "") or ""
        # Title carries more weight -- duplicate it so VADER counts it twice.
        return f"{title}. {title}. {description}"

    @staticmethod
    def _count_keyword_hits(text: str, keywords: list[str]) -> int:
        """Case-insensitive count of how many distinct keywords appear."""
        text_lower = text.lower()
        return sum(
            1
            for kw in keywords
            if re.search(re.escape(kw.lower()), text_lower)
        )

    @staticmethod
    def _classify(compound: float) -> str:
        """Map a VADER compound score to a human-readable label."""
        if compound >= SENTIMENT_THRESHOLDS["positive"]:
            return "positive"
        if compound <= SENTIMENT_THRESHOLDS["negative"]:
            return "negative"
        return "neutral"
