"""
SQLite-based cache manager.

Provides transparent caching for price data and news data so that
repeated requests within the configured TTL window do not trigger
redundant API / network calls.  Also tracks the daily GNews API
budget so we never exceed the free-tier limit.
"""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

from config.settings import CACHE_DB, CACHE_DURATIONS, API_RATE_LIMITS


class CacheManager:
    """Thread-safe SQLite cache with automatic expiry and API budget tracking."""

    _local = threading.local()

    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.db_path = str(db_path or CACHE_DB)
        self._init_db()

    # ------------------------------------------------------------------
    # Connection helpers (one connection per thread)
    # ------------------------------------------------------------------

    def _get_conn(self) -> sqlite3.Connection:
        """Return a per-thread SQLite connection."""
        conn = getattr(self._local, "conn", None)
        if conn is None:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.row_factory = sqlite3.Row
            self._local.conn = conn
        return conn

    def _init_db(self) -> None:
        """Create the schema if it doesn't exist yet."""
        conn = self._get_conn()
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS cache (
                key       TEXT PRIMARY KEY,
                data      TEXT NOT NULL,
                timestamp REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS api_calls (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                api_name  TEXT NOT NULL,
                call_date TEXT NOT NULL,
                call_count INTEGER NOT NULL DEFAULT 0,
                UNIQUE(api_name, call_date)
            );
            """
        )
        conn.commit()

    # ------------------------------------------------------------------
    # Generic cache get / set
    # ------------------------------------------------------------------

    def get_cached(self, key: str, max_age: Optional[int] = None) -> Optional[Any]:
        """
        Return cached data for *key* if it exists and is younger than
        *max_age* seconds.  Returns ``None`` on a cache miss.

        Parameters
        ----------
        key : str
            Unique cache key (e.g. ``"prices:GC=F:1d"``).
        max_age : int | None
            Maximum acceptable age in seconds.  If ``None`` the
            ``CACHE_DURATIONS`` defaults are used based on the key prefix
            (``"prices"`` or ``"news"``).
        """
        if max_age is None:
            prefix = key.split(":")[0] if ":" in key else key
            max_age = CACHE_DURATIONS.get(prefix, CACHE_DURATIONS["prices"])

        conn = self._get_conn()
        row = conn.execute(
            "SELECT data, timestamp FROM cache WHERE key = ?", (key,)
        ).fetchone()

        if row is None:
            return None

        age = time.time() - row["timestamp"]
        if age > max_age:
            # Stale -- clean it up.
            conn.execute("DELETE FROM cache WHERE key = ?", (key,))
            conn.commit()
            return None

        try:
            return json.loads(row["data"])
        except (json.JSONDecodeError, TypeError):
            return None

    def set_cached(self, key: str, data: Any) -> None:
        """Store *data* (must be JSON-serialisable) under *key*."""
        conn = self._get_conn()
        conn.execute(
            """
            INSERT INTO cache (key, data, timestamp)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET data = excluded.data,
                                           timestamp = excluded.timestamp
            """,
            (key, json.dumps(data, default=str), time.time()),
        )
        conn.commit()

    # ------------------------------------------------------------------
    # API budget tracking
    # ------------------------------------------------------------------

    def get_api_calls_today(self, api_name: str = "gnews") -> int:
        """Return the number of API calls made today for *api_name*."""
        today = date.today().isoformat()
        conn = self._get_conn()
        row = conn.execute(
            "SELECT call_count FROM api_calls WHERE api_name = ? AND call_date = ?",
            (api_name, today),
        ).fetchone()
        return row["call_count"] if row else 0

    def increment_api_calls(self, api_name: str = "gnews") -> int:
        """
        Increment the daily call counter for *api_name* and return the
        new total.
        """
        today = date.today().isoformat()
        conn = self._get_conn()
        conn.execute(
            """
            INSERT INTO api_calls (api_name, call_date, call_count)
            VALUES (?, ?, 1)
            ON CONFLICT(api_name, call_date)
            DO UPDATE SET call_count = call_count + 1
            """,
            (api_name, today),
        )
        conn.commit()
        return self.get_api_calls_today(api_name)

    def has_api_budget(self, api_name: str = "gnews") -> bool:
        """Return ``True`` if we have not yet hit today's rate limit."""
        limit = API_RATE_LIMITS.get(f"{api_name}_daily", 100)
        return self.get_api_calls_today(api_name) < limit

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def cleanup_expired(self) -> int:
        """
        Delete all cache rows older than the longest configured TTL.
        Returns the number of rows removed.
        """
        max_ttl = max(CACHE_DURATIONS.values())
        cutoff = time.time() - max_ttl
        conn = self._get_conn()
        cursor = conn.execute(
            "DELETE FROM cache WHERE timestamp < ?", (cutoff,)
        )
        conn.commit()

        # Also prune api_calls older than 7 days.
        week_ago = (
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        )
        from datetime import timedelta
        week_ago_str = (week_ago - timedelta(days=7)).date().isoformat()
        conn.execute(
            "DELETE FROM api_calls WHERE call_date < ?", (week_ago_str,)
        )
        conn.commit()

        return cursor.rowcount

    def clear_all(self) -> None:
        """Wipe the entire cache (useful for testing / manual reset)."""
        conn = self._get_conn()
        conn.execute("DELETE FROM cache")
        conn.execute("DELETE FROM api_calls")
        conn.commit()

    def close(self) -> None:
        """Close the thread-local connection if open."""
        conn = getattr(self._local, "conn", None)
        if conn is not None:
            conn.close()
            self._local.conn = None
