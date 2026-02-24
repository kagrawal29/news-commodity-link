"""
Price data fetcher backed by yfinance.

Fetches historical OHLCV data for commodity futures tickers, caches the
results in SQLite, and returns tidy ``pandas.DataFrame`` objects ready
for charting.
"""

from __future__ import annotations

import logging
from typing import Optional

import pandas as pd
import yfinance as yf

from config.settings import CACHE_DURATIONS, TIMEFRAME_OPTIONS
from data.cache_manager import CacheManager

logger = logging.getLogger(__name__)


class PriceFetcher:
    """Fetch and cache commodity price data from Yahoo Finance."""

    def __init__(self, cache: Optional[CacheManager] = None) -> None:
        self.cache = cache or CacheManager()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fetch_prices(
        self,
        ticker: str,
        timeframe: str = "30d",
    ) -> pd.DataFrame:
        """
        Return a DataFrame of historical prices for *ticker*.

        Parameters
        ----------
        ticker : str
            yfinance ticker symbol (e.g. ``"GC=F"``).
        timeframe : str
            One of the keys in ``TIMEFRAME_OPTIONS`` (``"1d"``, ``"7d"``,
            ``"30d"``, ``"90d"``, ``"1y"``).

        Returns
        -------
        pd.DataFrame
            Columns: Date, Open, High, Low, Close, Volume, Change, Change_Pct.
            Empty DataFrame on failure.
        """
        cache_key = f"prices:{ticker}:{timeframe}"

        # --- try cache first ------------------------------------------------
        cached = self.cache.get_cached(cache_key, CACHE_DURATIONS["prices"])
        if cached is not None:
            try:
                df = pd.DataFrame(cached)
                df["Date"] = pd.to_datetime(df["Date"])
                logger.debug("Cache hit for %s", cache_key)
                return df
            except Exception:
                logger.warning("Corrupt cache entry for %s -- refetching", cache_key)

        # --- fetch from yfinance -------------------------------------------
        tf_config = TIMEFRAME_OPTIONS.get(timeframe)
        if tf_config is None:
            logger.error("Unknown timeframe: %s", timeframe)
            return pd.DataFrame()

        try:
            logger.info(
                "Fetching prices for %s (period=%s, interval=%s)",
                ticker,
                tf_config["period"],
                tf_config["interval"],
            )
            yf_ticker = yf.Ticker(ticker)
            hist: pd.DataFrame = yf_ticker.history(
                period=tf_config["period"],
                interval=tf_config["interval"],
            )

            if hist.empty:
                logger.warning("yfinance returned no data for %s", ticker)
                return pd.DataFrame()

            df = self._normalize(hist)

            # --- persist to cache -------------------------------------------
            self.cache.set_cached(cache_key, df.to_dict(orient="list"))
            logger.info("Cached %d rows for %s", len(df), cache_key)
            return df

        except Exception as exc:
            logger.exception("Failed to fetch prices for %s: %s", ticker, exc)
            return pd.DataFrame()

    def get_latest_price(self, ticker: str) -> Optional[dict]:
        """
        Return a dict with the latest available price snapshot:
        ``{price, change, change_pct, volume, timestamp}``.

        Returns ``None`` on failure.
        """
        df = self.fetch_prices(ticker, timeframe="1d")
        if df.empty:
            return None

        last = df.iloc[-1]
        return {
            "price": float(last["Close"]),
            "change": float(last["Change"]),
            "change_pct": float(last["Change_Pct"]),
            "volume": int(last["Volume"]) if pd.notna(last["Volume"]) else 0,
            "timestamp": str(last["Date"]),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize(hist: pd.DataFrame) -> pd.DataFrame:
        """
        Clean up the raw yfinance DataFrame and add derived columns.
        """
        df = hist.reset_index()

        # yfinance sometimes names the index "Datetime" (intraday) or "Date".
        date_col = "Datetime" if "Datetime" in df.columns else "Date"
        df = df.rename(columns={date_col: "Date"})

        # Keep only the columns we need.
        keep = ["Date", "Open", "High", "Low", "Close", "Volume"]
        for col in keep:
            if col not in df.columns:
                df[col] = 0.0
        df = df[keep].copy()

        # Ensure numeric types.
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

        # Derived columns.
        df["Change"] = df["Close"].diff().fillna(0.0)
        df["Change_Pct"] = (
            df["Close"].pct_change().mul(100).fillna(0.0)
        )

        # Make sure Date is a proper datetime.
        df["Date"] = pd.to_datetime(df["Date"], utc=True, errors="coerce")

        return df
