"""
FastAPI backend wrapping the existing Python data pipeline.

Provides REST endpoints for commodity prices, news, and sentiment analysis.
Run with: uvicorn api.main:app --reload --port 8000
"""

from __future__ import annotations

import os
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from config.commodities import COMMODITIES
from config.settings import TIMEFRAME_OPTIONS
from data.cache_manager import CacheManager
from data.news_fetcher import NewsFetcher
from data.price_fetcher import PriceFetcher
from nlp.analyzer import SentimentAnalyzer
from nlp.clusterer import ArticleClusterer
from nlp.explainer import ClusterExplainer

app = FastAPI(
    title="Commodity Pulse API",
    description="Commodity news × price correlation data",
    version="1.0.0",
)

# CORS: allow localhost for development, Vercel URLs for production.
_cors_origins = ["http://localhost:3000"]
_vercel_url = os.getenv("VERCEL_URL")
if _vercel_url:
    _cors_origins.append(f"https://{_vercel_url}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# Shared singletons
# ------------------------------------------------------------------

_cache = CacheManager()
_price_fetcher = PriceFetcher(cache=_cache)
_news_fetcher = NewsFetcher(cache=_cache)
_sentiment_analyzer = SentimentAnalyzer()
_clusterer = ArticleClusterer()
_explainer = ClusterExplainer()


def _get_commodity(commodity: str) -> dict:
    """Look up a commodity by key or raise 404."""
    info = COMMODITIES.get(commodity)
    if info is None:
        raise HTTPException(status_code=404, detail=f"Unknown commodity: {commodity}")
    return info


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------


@app.get("/api/commodities")
def list_commodities():
    """Return all available commodities."""
    return {
        key: {
            "name": info["name"],
            "ticker": info["ticker"],
            "icon": info["icon"],
        }
        for key, info in COMMODITIES.items()
    }


@app.get("/api/prices/{commodity}")
def get_latest_price(commodity: str):
    """Return the latest price snapshot for a commodity."""
    info = _get_commodity(commodity)
    price_data = _price_fetcher.get_latest_price(info["ticker"])
    if price_data is None:
        raise HTTPException(status_code=502, detail="Price data unavailable")
    return {"commodity": commodity, **price_data}


@app.get("/api/prices/{commodity}/history")
def get_price_history(
    commodity: str,
    timeframe: Literal["1d", "7d", "30d", "90d", "1y"] = "30d",
):
    """Return historical OHLCV data for a commodity."""
    info = _get_commodity(commodity)
    df = _price_fetcher.fetch_prices(info["ticker"], timeframe=timeframe)
    if df.empty:
        return {"commodity": commodity, "timeframe": timeframe, "data": []}

    # Convert DataFrame to JSON-serialisable records
    records = df.copy()
    records["Date"] = records["Date"].astype(str)
    return {
        "commodity": commodity,
        "timeframe": timeframe,
        "data": records.to_dict(orient="records"),
    }


@app.get("/api/news/{commodity}")
def get_news(commodity: str):
    """Return news articles with sentiment scores for a commodity."""
    info = _get_commodity(commodity)
    articles = _news_fetcher.fetch_news(
        keywords=info["keywords"],
        rss_feeds=info["rss_feeds"],
        commodity_key=commodity,
    )
    sentiment_result = _sentiment_analyzer.analyze(
        articles, commodity_keywords=info["keywords"]
    )
    return {
        "commodity": commodity,
        "articles": sentiment_result["scored_articles"],
        "count": len(sentiment_result["scored_articles"]),
    }


@app.get("/api/sentiment/{commodity}")
def get_sentiment(commodity: str):
    """Return full sentiment analysis for a commodity."""
    info = _get_commodity(commodity)
    articles = _news_fetcher.fetch_news(
        keywords=info["keywords"],
        rss_feeds=info["rss_feeds"],
        commodity_key=commodity,
    )
    result = _sentiment_analyzer.analyze(
        articles, commodity_keywords=info["keywords"]
    )
    return {
        "commodity": commodity,
        "summary": result["summary"],
        "rolling": result["rolling"],
        "trend": result["trend"],
    }


@app.get("/api/news/{commodity}/clusters")
def get_news_clusters(commodity: str):
    """Return news articles grouped into thematic clusters with price context."""
    info = _get_commodity(commodity)

    # Fetch and score articles
    articles = _news_fetcher.fetch_news(
        keywords=info["keywords"],
        rss_feeds=info["rss_feeds"],
        commodity_key=commodity,
    )
    result = _sentiment_analyzer.analyze(
        articles, commodity_keywords=info["keywords"]
    )
    scored = result["scored_articles"]

    # Fetch recent price data for price delta computation
    df = _price_fetcher.fetch_prices(info["ticker"], timeframe="7d")
    price_data = None
    if not df.empty:
        records = df.copy()
        records["Date"] = records["Date"].astype(str)
        price_data = records.to_dict(orient="records")

    # Cluster articles by theme
    clusters = _clusterer.cluster(scored, commodity, price_data)

    # Add LLM explanations (gracefully skipped if no API key)
    clusters = _explainer.explain_clusters(clusters, info["name"])

    return {
        "commodity": commodity,
        "clusters": clusters,
        "total_articles": len(scored),
        "clustered_articles": sum(c["article_count"] for c in clusters),
    }
