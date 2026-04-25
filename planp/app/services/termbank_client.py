"""Termbank.pdhc HTTP client for plan.pdhc.

Wraps the small subset of termbank's read API that plan.pdhc needs to
display "View in termbank" panels and power the click-to-fill search
widget on Concept / ValueCatalog forms.

Uses an in-process TTL cache (60 s default) so a page that renders five
concepts referencing the same lib doesn't hammer termbank.

The client is **best-effort**: every call returns a result OR ``None``
(for lookups) / a result with an ``"error"`` key (for searches) when
termbank is unreachable, slow, or returns non-2xx. plan.pdhc's UI
degrades gracefully — no banner, no exception, just an "unavailable"
message in the panel.
"""
from __future__ import annotations

import logging
import os
import time
from threading import Lock
from typing import Any

import requests

log = logging.getLogger(__name__)


DEFAULT_BASE_URL = "https://termbank.pdhc.se"
DEFAULT_TIMEOUT_SECONDS = 5.0
DEFAULT_CACHE_TTL_SECONDS = 60.0


class TermbankClient:
    """Small, thread-safe client. One instance per Flask app.

    Attach to ``app.termbank_client`` in :func:`app.create_app` so views
    can do ``current_app.termbank_client.lookup(...)``.
    """

    def __init__(
        self,
        base_url: str | None = None,
        *,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        cache_ttl: float = DEFAULT_CACHE_TTL_SECONDS,
    ) -> None:
        self.base_url = (base_url or os.environ.get(
            "TERMBANK_BASE_URL", DEFAULT_BASE_URL
        )).rstrip("/")
        self.timeout = timeout
        self.cache_ttl = cache_ttl
        self._cache: dict[tuple, tuple[float, Any]] = {}
        self._lock = Lock()

    # ----- public API ----------------------------------------------------
    def lookup(self, system: str, code: str) -> dict | None:
        """Return termbank's ``$lookup`` Parameters body, or ``None`` on miss/error.

        Cached per ``(system, code)`` for ``cache_ttl`` seconds.
        """
        key = ("lookup", system, code)
        cached = self._get_cached(key)
        if cached is not self._MISS:
            return cached  # cached value, possibly None for a known-miss
        url = f"{self.base_url}/CodeSystem/{system}/{code}"
        try:
            resp = requests.get(url, timeout=self.timeout)
        except requests.RequestException as e:
            log.warning("termbank lookup unreachable: %s", e)
            return None
        if resp.status_code == 200:
            data = resp.json()
            self._set_cached(key, data)
            return data
        if resp.status_code == 404:
            # Cache the miss too — avoids re-querying for known-absent codes.
            self._set_cached(key, None)
            return None
        log.warning("termbank lookup returned %s for %s/%s",
                    resp.status_code, system, code)
        return None

    def search(
        self,
        q: str,
        system: str | None = None,
        limit: int = 20,
    ) -> dict:
        """Return termbank's ``/search`` response.

        Always returns a dict — never raises. On failure returns
        ``{"error": <reason>, "results": []}`` so callers can render a
        consistent shape.
        """
        if not q.strip():
            return {"query": "", "system": system, "count": 0, "results": []}
        key = ("search", q, system, int(limit))
        cached = self._get_cached(key)
        if cached is not self._MISS:
            return cached
        params = {"q": q, "limit": int(limit)}
        if system:
            params["system"] = system
        try:
            resp = requests.get(
                f"{self.base_url}/search",
                params=params,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            log.warning("termbank search unreachable: %s", e)
            return {"error": "unreachable", "results": [], "query": q}
        if resp.status_code != 200:
            return {
                "error": f"http_{resp.status_code}",
                "results": [],
                "query": q,
            }
        data = resp.json()
        self._set_cached(key, data)
        return data

    def health(self) -> dict | None:
        """Best-effort health probe — returns termbank's /health body or None."""
        try:
            resp = requests.get(
                f"{self.base_url}/health",
                timeout=self.timeout,
            )
        except requests.RequestException:
            return None
        if resp.status_code in (200, 503):
            try:
                return resp.json()
            except ValueError:
                return None
        return None

    # ----- cache helpers -------------------------------------------------
    # Sentinel distinguishes "no cache entry" from "cached value of None"
    # (i.e. a cached lookup-miss). Without this, 404s would re-hit termbank
    # on every call.
    _MISS = object()

    def _get_cached(self, key: tuple):
        """Return the cached value, or ``self._MISS`` if absent/expired."""
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return self._MISS
            ts, value = entry
            if (time.monotonic() - ts) >= self.cache_ttl:
                self._cache.pop(key, None)
                return self._MISS
            return value

    def _set_cached(self, key: tuple, value) -> None:
        with self._lock:
            self._cache[key] = (time.monotonic(), value)

    def clear_cache(self) -> None:
        with self._lock:
            self._cache.clear()
