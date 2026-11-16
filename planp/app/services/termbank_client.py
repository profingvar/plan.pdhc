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

from app.services.session_headers import outbound_session_headers

log = logging.getLogger(__name__)


# #955: there is NO default base URL. One used to read
# "https://termbank.pdhc.se" -- a name with no vhost (termbank is a loopback
# exception, CLAUDE.md section 7) -- so a lost TERMBANK_BASE_URL silently
# became "the New Concept widget finds no codes" at the next cold start.
# Unset now reads as unset: no call is made, and every answer names the
# cause (#833's rule, which deleted xlate's fabricated default).
NOT_CONFIGURED = "termbank_not_configured"
# 10s, up from the original 5s. The /search ranking join on a 4.7M-row
# concept_designations table can sit just under 1s P50 with pg_trgm
# indexes, but cold-cache or contended queries occasionally cross the
# old 5s ceiling; 10s gives headroom without leaving the UI hanging.
DEFAULT_TIMEOUT_SECONDS = 10.0
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
        raw = base_url or os.environ.get("TERMBANK_BASE_URL") or ""
        self.base_url = raw.strip().rstrip("/") or None
        self.timeout = timeout
        self.cache_ttl = cache_ttl
        self._cache: dict[tuple, tuple[float, Any]] = {}
        self._lock = Lock()

    @property
    def configured(self) -> bool:
        return self.base_url is not None

    # ----- public API ----------------------------------------------------
    def lookup(self, system: str, code: str) -> dict | None:
        """Return termbank's ``$lookup`` Parameters body, or ``None`` on miss/error.

        Cached per ``(system, code)`` for ``cache_ttl`` seconds.
        """
        if not self.configured:
            log.error("termbank lookup refused: TERMBANK_BASE_URL is not configured")
            return None
        key = ("lookup", system, code)
        cached = self._get_cached(key)
        if cached is not self._MISS:
            return cached  # cached value, possibly None for a known-miss
        url = f"{self.base_url}/CodeSystem/{system}/{code}"
        try:
            resp = requests.get(url, headers=outbound_session_headers(), timeout=self.timeout)
        except requests.Timeout as e:
            log.warning("termbank lookup timeout (>%ss) for %s/%s: %s",
                        self.timeout, system, code, e)
            return None
        except requests.ConnectionError as e:
            log.warning("termbank lookup unreachable for %s/%s: %s",
                        system, code, e)
            return None
        except requests.RequestException as e:
            log.warning("termbank lookup request_error for %s/%s: %s",
                        system, code, e)
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
        if not self.configured:
            log.error("termbank search refused: TERMBANK_BASE_URL is not configured")
            return {"error": NOT_CONFIGURED, "results": [], "query": q}
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
                headers=outbound_session_headers(),
                timeout=self.timeout,
            )
        except requests.Timeout as e:
            log.warning(
                "termbank search timeout (>%ss) for q=%r: %s",
                self.timeout, q, e,
            )
            return {"error": "timeout", "results": [], "query": q}
        except requests.ConnectionError as e:
            log.warning("termbank search unreachable for q=%r: %s", q, e)
            return {"error": "unreachable", "results": [], "query": q}
        except requests.RequestException as e:
            log.warning("termbank search request_error for q=%r: %s", q, e)
            return {"error": "request_error", "results": [], "query": q}
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
        if not self.configured:
            return None
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
