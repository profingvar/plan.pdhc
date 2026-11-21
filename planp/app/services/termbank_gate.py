"""termbank is reachable ONLY from inside plan.pdhc (operator rule, 2026-11-20).

termbank listens on 127.0.0.1 with no vhost, so every outside path to it runs
through plan. Each such path calls `refusal()` first:

  * a logged-in plan session (any role) passes -- plan's own pages (the
    "View in termbank" panel, the search picker) send its cookie;
  * a service key is refused even when valid: no other service reads
    termbank through plan, and a read_only key must not make plan a side door;
  * anything else (anonymous, crawlers) gets the session decorator's 401.

Plan's LOCAL CodeSystem lookups ($lookup with the local system) never reach
termbank and are not gated here.
"""
from __future__ import annotations

from flask import current_app, jsonify, request

MESSAGE = 'termbank is only available inside plan.pdhc'


def refusal():
    """None when this request may reach termbank, else a Flask response."""
    if current_app.config.get('AUTH_DISABLED'):
        return None
    if request.headers.get('X-Service-Key') or request.headers.get('X-Source-Service'):
        return jsonify({'error': MESSAGE}), 403
    from app.api.auth import requires_role
    return requires_role('read_only')(lambda: None)()
