"""loader.pdhc is gone from plan.pdhc's service-key allowlist (2026-10-05).

It named no repo — a bulk-concept loader run from the operator's machine — and
held a live, never-rotated key (created 2026-04-28, the same batch as the
monitor.pdhc key destroyed under #727) that bypassed SSO here. plan.pdhc checks
the service-key path FIRST in requires_role, so a valid key skipped the SSO
gate entirely.

It was found only by tools/build_platform_graph.py, after two hand audits of
exactly this question had already reported the wrong answer.
"""
from __future__ import annotations


def test_loader_is_not_a_known_service():
    from app.api.auth import KNOWN_SERVICES
    assert 'loader.pdhc' not in KNOWN_SERVICES
    assert KNOWN_SERVICES == {'sim.pdhc': 'SIM_PDHC_SERVICE_KEY'}


def test_the_loader_key_is_not_read_into_config(app):
    """An operator who still has PLAN_LOADER_SERVICE_KEY set must be ignored,
    not quietly honoured."""
    assert 'PLAN_LOADER_SERVICE_KEY' not in app.config


def test_the_capability_statement_does_not_advertise_it(client):
    """The CapabilityStatement listed loader.pdhc under known_sources.

    Advertising an identity that can no longer authenticate is worse than not
    advertising it: a caller follows the documentation and gets a 403 that the
    documentation says should not happen.
    """
    from app.api import capability
    import inspect
    src = inspect.getsource(capability)
    assert "'loader.pdhc'" not in src and '"loader.pdhc"' not in src
