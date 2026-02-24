"""
NLP module for commodity news sentiment analysis.

Exposes the two main classes:
- ``SentimentScorer`` -- per-article VADER-based scoring with keyword boosting.
- ``SentimentAnalyzer`` -- aggregation across multiple articles (rolling
  sentiment, trends, weighted averages).
"""

from nlp.sentiment import SentimentScorer
from nlp.analyzer import SentimentAnalyzer

__all__ = ["SentimentScorer", "SentimentAnalyzer"]
