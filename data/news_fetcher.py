"""
News fetcher combining the GNews API and public RSS feeds.

Strategy:
1. If a GNews API key is configured **and** today's budget has not been
   exhausted, query GNews for the commodity's keywords.
2. Always fetch from the commodity's RSS feed list via ``feedparser``.
3. Merge both sources, deduplicate by title similarity, and return a
   unified list of news items sorted newest-first.

Each news item is a dict with the following shape::

    {
        "title": str,
        "description": str,
        "source": str,
        "url": str,
        "published_date": str (ISO-8601),
        "source_type": "gnews" | "rss",
    }
"""

from __future__ import annotations

import logging
import os
import re
from datetime import datetime, timezone
from typing import Optional

import feedparser
import requests
from dotenv import load_dotenv

from config.settings import CACHE_DURATIONS
from data.cache_manager import CacheManager

# Load environment variables from .env if present.
load_dotenv()

logger = logging.getLogger(__name__)

# Maximum articles to request per GNews call.
_GNEWS_MAX_RESULTS = 10


class NewsFetcher:
    """Fetch, merge, and cache commodity news from GNews + RSS feeds."""

    def __init__(self, cache: Optional[CacheManager] = None) -> None:
        self.cache = cache or CacheManager()
        self._gnews_api_key: Optional[str] = os.getenv("GNEWS_API_KEY")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fetch_news(
        self,
        keywords: list[str],
        rss_feeds: list[str],
        commodity_key: str,
        max_results: int = 20,
    ) -> list[dict]:
        """
        Return a deduplicated, newest-first list of news articles related
        to a commodity.

        Parameters
        ----------
        keywords : list[str]
            Search terms for GNews (e.g. ``["gold price", "XAUUSD"]``).
        rss_feeds : list[str]
            RSS/Atom feed URLs to scrape.
        commodity_key : str
            Short commodity identifier used as part of the cache key.
        max_results : int
            Approximate cap on the number of articles returned.

        Returns
        -------
        list[dict]
            Each dict follows the schema described in the module docstring.
        """
        cache_key = f"news:{commodity_key}"

        # --- try cache first ------------------------------------------------
        cached = self.cache.get_cached(cache_key, CACHE_DURATIONS["news"])
        if cached is not None:
            logger.debug("Cache hit for %s", cache_key)
            return cached

        # --- fetch from both sources ----------------------------------------
        gnews_articles = self._fetch_gnews(keywords)
        rss_articles = self._fetch_rss(rss_feeds, keywords)

        merged = self._merge_and_deduplicate(gnews_articles + rss_articles)

        # Sort newest first.
        merged.sort(key=lambda a: a.get("published_date", ""), reverse=True)

        # Cap length.
        merged = merged[:max_results]

        # --- persist to cache -----------------------------------------------
        if merged:
            self.cache.set_cached(cache_key, merged)
            logger.info("Cached %d articles for %s", len(merged), cache_key)

        return merged

    # ------------------------------------------------------------------
    # GNews
    # ------------------------------------------------------------------

    def _fetch_gnews(self, keywords: list[str]) -> list[dict]:
        """Query the GNews REST API.  Returns an empty list on any failure."""
        if not self._gnews_api_key or self._gnews_api_key == "your_gnews_api_key_here":
            logger.debug("GNews API key not configured -- skipping GNews.")
            return []

        if not self.cache.has_api_budget("gnews"):
            logger.warning("GNews daily budget exhausted -- skipping GNews.")
            return []

        articles: list[dict] = []

        # Use the first (most specific) keyword as the query.
        query = keywords[0] if keywords else ""
        if not query:
            return []

        try:
            url = "https://gnews.io/api/v4/search"
            params = {
                "q": query,
                "lang": "en",
                "max": _GNEWS_MAX_RESULTS,
                "apikey": self._gnews_api_key,
            }

            logger.info("Querying GNews API for '%s'", query)
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()

            self.cache.increment_api_calls("gnews")

            data = resp.json()
            for item in data.get("articles", []):
                articles.append(
                    {
                        "title": item.get("title", ""),
                        "description": item.get("description", ""),
                        "source": item.get("source", {}).get("name", "Unknown"),
                        "url": item.get("url", ""),
                        "published_date": self._parse_date(
                            item.get("publishedAt", "")
                        ),
                        "source_type": "gnews",
                    }
                )

        except requests.RequestException as exc:
            logger.warning("GNews request failed: %s", exc)
        except Exception as exc:
            logger.exception("Unexpected error fetching GNews: %s", exc)

        return articles

    # ------------------------------------------------------------------
    # RSS Feeds
    # ------------------------------------------------------------------

    # Google News RSS feeds are pre-filtered by the search query embedded
    # in the URL, so every entry is already relevant.
    _GNEWS_RSS_PREFIX = "https://news.google.com/rss/"

    def _fetch_rss(
        self, feed_urls: list[str], keywords: list[str]
    ) -> list[dict]:
        """
        Parse all *feed_urls* and return articles that are relevant to
        the commodity.

        Relevance rules:
        - **Google News RSS** feeds (query-targeted): accept all entries.
        - **Other feeds**: require at least one full keyword phrase match
          in the title or summary.  Single generic words like "price" or
          "trade" are NOT enough on their own.
        """
        articles: list[dict] = []
        # Build patterns only for full keyword phrases (e.g. "crude oil price",
        # "OPEC", "WTI crude") — not individual words.
        phrase_patterns = [
            re.compile(re.escape(kw), re.IGNORECASE) for kw in keywords
        ]

        for url in feed_urls:
            is_gnews_rss = url.startswith(self._GNEWS_RSS_PREFIX)

            try:
                logger.debug("Parsing RSS feed: %s", url)
                try:
                    resp = requests.get(url, timeout=15)
                    resp.raise_for_status()
                    feed = feedparser.parse(resp.content)
                except requests.RequestException as req_exc:
                    logger.warning("Failed to fetch RSS %s: %s", url, req_exc)
                    continue

                if feed.bozo and not feed.entries:
                    logger.warning(
                        "Feed %s is malformed and has no entries", url
                    )
                    continue

                for entry in feed.entries:
                    title = entry.get("title", "")
                    summary = entry.get("summary", entry.get("description", ""))
                    text_blob = f"{title} {summary}"

                    # Google News RSS: already targeted by search query.
                    # Other feeds: require a full keyword phrase match.
                    if not is_gnews_rss:
                        if not any(pat.search(text_blob) for pat in phrase_patterns):
                            continue

                    pub_date = self._extract_rss_date(entry)
                    source_name = feed.feed.get("title", url)

                    articles.append(
                        {
                            "title": title,
                            "description": summary[:500] if summary else "",
                            "source": source_name,
                            "url": entry.get("link", ""),
                            "published_date": pub_date,
                            "source_type": "rss",
                        }
                    )

            except Exception as exc:
                logger.warning("Failed to parse RSS feed %s: %s", url, exc)

        return articles

    # ------------------------------------------------------------------
    # Deduplication
    # ------------------------------------------------------------------

    @staticmethod
    def _merge_and_deduplicate(articles: list[dict]) -> list[dict]:
        """
        Remove near-duplicate articles based on normalised title.

        When duplicates are found the GNews version is preferred because
        it typically has richer metadata.
        """
        seen: dict[str, dict] = {}

        for article in articles:
            norm_title = NewsFetcher._normalize_title(article.get("title", ""))
            if not norm_title:
                continue

            existing = seen.get(norm_title)
            if existing is None:
                seen[norm_title] = article
            elif (
                article.get("source_type") == "gnews"
                and existing.get("source_type") != "gnews"
            ):
                # Prefer the GNews version.
                seen[norm_title] = article

        return list(seen.values())

    @staticmethod
    def _normalize_title(title: str) -> str:
        """Lowercase, strip punctuation, collapse whitespace."""
        title = title.lower().strip()
        title = re.sub(r"[^\w\s]", "", title)
        title = re.sub(r"\s+", " ", title)
        return title

    # ------------------------------------------------------------------
    # Date helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_date(date_str: str) -> str:
        """Best-effort ISO-8601 parsing for GNews dates."""
        if not date_str:
            return datetime.now(timezone.utc).isoformat()
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.isoformat()
        except (ValueError, TypeError):
            return date_str

    @staticmethod
    def _extract_rss_date(entry: dict) -> str:
        """
        Extract the published date from a feedparser entry and return it
        as an ISO-8601 string.
        """
        for field in ("published_parsed", "updated_parsed"):
            time_struct = entry.get(field)
            if time_struct is not None:
                try:
                    from time import mktime
                    dt = datetime.fromtimestamp(mktime(time_struct), tz=timezone.utc)
                    return dt.isoformat()
                except (TypeError, ValueError, OverflowError):
                    pass

        # Fallback: try the raw string.
        raw = entry.get("published", entry.get("updated", ""))
        if raw:
            return NewsFetcher._parse_date(raw)

        return datetime.now(timezone.utc).isoformat()
