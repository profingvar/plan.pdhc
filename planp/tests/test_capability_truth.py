"""#326 — every endpoint advertised by /capability-statement must resolve.

Pre-#326, the capability statement advertised ghost auth routes
(POST /auth/login, POST /auth/logout, POST /auth/refresh) that were
never wired up. This test walks the response and asserts that for each
advertised endpoint, a matching rule exists in app.url_map for that
method.

Treat a failure here as either: (a) capability advertising a route the
code didn't ship, or (b) a route was renamed/dropped without updating
capability. Either way, fix the divergence before merging.
"""
from __future__ import annotations

import re

import pytest


def _shape(path):
    """Reduce a path to its structural shape — every ``<...>`` block (any
    name, any Flask converter prefix) becomes ``<*>`` so capability paths
    can be compared to url_map rules irrespective of variable-name skew
    (e.g. ``/CodeSystem/<id>`` vs ``/CodeSystem/<id_>``)."""
    return re.sub(r'<[^>]+>', '<*>', path)


def _has_rule(app, method, path):
    target = _shape(path)
    for rule in app.url_map.iter_rules():
        if _shape(rule.rule) == target and method.upper() in rule.methods:
            return True
    return False


class TestCapabilityEndpointsAllResolve:
    def test_every_advertised_endpoint_has_a_route(self, app, client):
        resp = client.get('/api/v1/capability-statement')
        assert resp.status_code == 200
        body = resp.get_json()
        assert 'resources' in body, 'capability response missing resources block'

        missing = []
        for resource_name, endpoints in body['resources'].items():
            for ep in endpoints:
                if not _has_rule(app, ep['method'], ep['path']):
                    missing.append(f"{ep['method']} {ep['path']} (in {resource_name})")
        assert not missing, (
            f'capability advertises {len(missing)} endpoint(s) with no matching '
            f'url_map rule:\n  ' + '\n  '.join(missing)
        )


class TestCapabilityAuthBlockIsTruthful:
    def test_auth_advertises_only_real_routes(self, app, client):
        resp = client.get('/api/v1/capability-statement')
        body = resp.get_json()
        auth_endpoints = [
            ep for ep in body['resources'].get('auth', [])
        ]
        methods_paths = {(e['method'], e['path']) for e in auth_endpoints}

        # Real routes that must be advertised:
        for m, p in [
            ('GET', '/api/v1/auth/login'),
            ('GET', '/api/v1/auth/callback'),
            ('GET', '/api/v1/auth/me'),
        ]:
            assert (m, p) in methods_paths, f'missing real route {m} {p}'

        # Ghost routes that must NOT be advertised:
        for m, p in [
            ('POST', '/api/v1/auth/login'),
            ('POST', '/api/v1/auth/refresh'),
        ]:
            assert (m, p) not in methods_paths, (
                f'capability still advertises ghost route {m} {p}'
            )

    def test_authentication_block_describes_sso(self, client):
        resp = client.get('/api/v1/capability-statement')
        body = resp.get_json()
        auth = body['authentication']
        assert auth['type'].startswith('SSO')
        assert 'service_key_bypass' in auth
        assert set(auth['service_key_bypass']['headers']) == {
            'X-Source-Service', 'X-Service-Key',
        }

    def test_rate_limiting_block_is_truthful(self, client):
        resp = client.get('/api/v1/capability-statement')
        body = resp.get_json()
        rl = body['rate_limiting']
        # No "10 requests/minute" ghost — limit applies uniformly.
        assert '10' not in rl['default'], (
            'capability still advertises the ghost "10/minute on login" limit'
        )
        assert '/api/health' in rl['exempt']
        assert rl['service_key_exempt'] is True
