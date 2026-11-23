"""#931 — shadow log of API reads that arrive without a credential.

plan's reads were open because no consumer could authenticate. #931 gives
every consumer a key; this hook records who STILL reads without one, so the
reads can be gated on evidence (the #902 pattern on ips) rather than on a
guess about who calls what. It blocks nothing.

One line per read, logger `plan.read_shadow`, WARNING so gunicorn shows it:

    read_shadow outcome=<none|invalid_key> method=GET path=/api/v1/concepts
                claimed=<X-Source-Service or -> remote=<client addr> ua=<UA>

An SSO session or a VALID service key is not logged. An INVALID key is —
on an open route it is let through today, and it is exactly the line that
says a consumer's key is wrong before the gate makes that an outage.
"""
from __future__ import annotations

import logging

from flask import request, session

log = logging.getLogger('plan.read_shadow')

#: Public by decision, so an unauthenticated read here is not a finding.
#: `$validate-code` stays public by #913 (a yes/no about one code, not an
#: enumeration); health/metadata are what monitors and FHIR clients probe.
PUBLIC_BY_DECISION = (
    '/api/health',
    '/api/v1/metadata',
    '/api/v1/capability-statement',
    '/api/v1/auth/',
    # #1011: the same ENDPOINTS list as capability-statement, flat.
    '/api/v1/endpoints',
    # #1011: the documentation catalogue. Every file it serves is in the
    # PUBLIC plan.pdhc GitHub repo, and the web page /docs serves the same
    # files without a login; gating the API copy would protect nothing.
    '/api/v1/docs',
)

#: #1011: after stage 3 this IS the list of API reads that answer without a
#: credential — tests/test_read_gate_1011.py walks every GET rule and fails if
#: anything outside it answers anonymously, so the shadow exemption and the
#: gate cannot drift apart.


def _is_public(path: str) -> bool:
    if any(path == p or path.startswith(p) for p in PUBLIC_BY_DECISION):
        return True
    return path.endswith('/$validate-code') or path.endswith('/%24validate-code')


def _remote() -> str:
    # nginx sits in front; the socket peer is the docker bridge for everyone.
    fwd = request.headers.get('X-Forwarded-For', '')
    return (fwd.split(',')[0].strip() or request.headers.get('X-Real-IP', '')
            or request.remote_addr or '-')


def classify() -> str | None:
    """None when the read is authenticated or exempt, else the outcome."""
    if request.method not in ('GET', 'HEAD'):
        return None
    path = request.path
    if not path.startswith('/api/') or _is_public(path):
        return None
    if session.get('sso_token'):
        return None
    from app.api.auth import _service_key_outcome
    sk = _service_key_outcome()
    if sk is None:
        return 'none'
    if sk is False:
        return 'invalid_key'
    return None


def init_read_shadow(app):
    @app.before_request
    def _read_shadow():
        if app.config.get('AUTH_DISABLED'):
            return None
        try:
            outcome = classify()
        except Exception:  # a shadow log must never fail a request
            log.exception('read_shadow classify failed')
            return None
        if outcome:
            claimed = request.headers.get('X-Source-Service', '').strip() or '-'
            ua = (request.headers.get('User-Agent', '') or '-')[:80]
            log.warning('read_shadow outcome=%s method=%s path=%s claimed=%s remote=%s ua=%s',
                        outcome, request.method, request.path, claimed[:40], _remote(), ua)
        return None
