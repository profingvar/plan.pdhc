"""Rate-limit test (#328 — rollup #325).

Pre-#328, blueprint-level ``limiter.limit("200/minute")(<bp>)`` calls
were silently no-ops — Flask-Limiter's ``.limit`` decorator expects to
wrap a view, not a blueprint. Post-#328 the limit is configured globally
via ``RATELIMIT_DEFAULT='200/minute'`` in ``app/__init__.py``.

This test fires 201 GETs against ``/api/v1/lookup/units`` (a lightweight
read endpoint that exists, is freely callable without auth, and returns
small JSON) and asserts the 201st returns HTTP 429. It also asserts the
exempt endpoints (``/api/v1/capability-statement``, ``/api/health``)
keep returning 200 past the same threshold.

The Flask test client uses a fresh storage backend per request so we
rely on the limiter's in-memory storage (the default for test config).
"""
from __future__ import annotations

import pytest

from app import limiter


@pytest.fixture(autouse=True)
def _reset_limiter_storage(app):
    """Clear the limiter's storage before each test so prior tests don't
    leave half-filled buckets in the in-memory store."""
    storage = limiter.storage
    if hasattr(storage, 'reset'):
        storage.reset()
    elif hasattr(storage, 'storage'):
        storage.storage.clear()
    yield


class TestEnforcedEndpointReturns429:
    def test_201st_request_is_rate_limited(self, client):
        # 200/minute default — fire 200 (should all succeed), then one more
        # should hit 429.
        ok = 0
        for _ in range(200):
            r = client.get('/api/v1/lookup/units')
            if r.status_code == 200:
                ok += 1
            elif r.status_code == 429:
                # Already-hit limit due to a non-isolated prior test.
                pytest.fail(
                    f'Rate limit hit early at request {ok + 1} — '
                    'limiter storage not properly reset between tests.'
                )
        assert ok == 200, f'expected 200/200 to succeed, got {ok}'
        r = client.get('/api/v1/lookup/units')
        assert r.status_code == 429, (
            f'201st request should return 429, got {r.status_code}'
        )


class TestExemptEndpointsAreNotLimited:
    def test_health_is_exempt(self, client):
        # Fire 220 requests at /api/health; none should 429.
        for i in range(220):
            r = client.get('/api/health')
            assert r.status_code in (200, 503), (
                f'/api/health hit {r.status_code} at request {i + 1} '
                '(should never 429)'
            )

    def test_capability_statement_is_exempt(self, client):
        for i in range(220):
            r = client.get('/api/v1/capability-statement')
            assert r.status_code == 200, (
                f'/api/v1/capability-statement hit {r.status_code} '
                f'at request {i + 1} (should never 429)'
            )
