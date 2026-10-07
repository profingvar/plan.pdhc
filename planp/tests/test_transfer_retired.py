"""The #530 Transfer page and its cdr_6 proxy are retired from plan.pdhc (#786).

Operator decision 2026-10-07 ("Retire transfer"). It replaces
tests/test_transfer.py, whose 12 tests asserted the feature worked.

Three things made it the wrong home, and only the third is about tidiness:

1. **It was already non-functional in production.** `CDR_TRANSFER_TARGETS` was
   unset on `pdhc_app`, and `_validate_to` rejected any destination not in that
   list, so preview and execute both 400'd. The page reported
   `configured: true` -- that flag only checked `CDR6_BASE_URL` -- with
   `targets: []`. It looked wired and could do nothing.

2. **plan held sim's credential and impersonated it.** cdr_6 is sim-only (its
   Rule 2), so plan called it presenting `X-Source-Service: sim.pdhc` with
   cdr_6's SIM service key. The authoring plane therefore held a data-plane
   credential it had no other use for, and cdr_6's audit attributed those
   transfers to sim.pdhc -- not to plan, and not to the operator who clicked.

3. `sim cdr-transfer` already does the job, from the service that legitimately
   owns that key.

What these tests actually guard is the hard part of a retirement: that the
settings are not quietly honoured if someone still has them in a `.env`. Three
identities on this platform came back or lingered that way -- monitor.pdhc
(#727), 2gate.pdhc (#732), loader.pdhc (#736) -- so a retirement that only
deletes code is half done.
"""
from __future__ import annotations


def test_the_api_routes_are_gone(client):
    """404, not 403 or 503: the endpoints do not exist."""
    assert client.get('/api/v1/transfer/targets').status_code == 404
    assert client.post('/api/v1/transfer/preview', json={}).status_code == 404
    assert client.post('/api/v1/transfer/execute', json={}).status_code == 404


def test_the_web_page_is_gone(client):
    assert client.get('/transfer').status_code == 404


def test_neither_blueprint_is_registered(app):
    names = set(app.blueprints)
    assert 'transfer' not in names
    assert 'transfer_web' not in names


def test_no_url_rule_mentions_transfer(app):
    """A route registered under a different blueprint name would still be a
    live transfer endpoint. Check the URL map, not just the blueprint names."""
    rules = [str(r) for r in app.url_map.iter_rules() if 'transfer' in str(r)]
    assert rules == [], rules


def test_the_cdr6_settings_are_not_read_into_config(app):
    """THE one that matters.

    An operator whose `.env` still carries CDR6_SERVICE_KEY must be IGNORED,
    not quietly honoured. If config starts reading it again, the authoring
    plane is holding sim's credential again -- which is the actual reason this
    was retired, and the part no 404 would reveal.
    """
    for key in ('CDR6_BASE_URL', 'CDR6_SERVICE_KEY', 'CDR6_TIMEOUT',
                'CDR_TRANSFER_TARGETS'):
        assert key not in app.config, (
            f'{key} is back in config. plan.pdhc is the authoring plane and '
            f'must not hold a cdr_6 credential; `sim cdr-transfer` owns this.')


def test_a_stale_env_value_is_still_ignored(monkeypatch):
    """Set the variables and build a fresh config: they must not appear.

    Asserting the current app's config proves only that this .env is clean.
    This proves the code no longer reads them at all.
    """
    for key in ('CDR6_BASE_URL', 'CDR6_SERVICE_KEY', 'CDR6_TIMEOUT',
                'CDR_TRANSFER_TARGETS'):
        monkeypatch.setenv(key, 'leftover-value')
    import importlib
    from app import config as config_module
    importlib.reload(config_module)
    try:
        cfg = config_module.Config
        for key in ('CDR6_BASE_URL', 'CDR6_SERVICE_KEY', 'CDR6_TIMEOUT',
                    'CDR_TRANSFER_TARGETS'):
            assert not hasattr(cfg, key), f'{key} is read back from the env'
    finally:
        # Leave the module as the rest of the suite expects to find it.
        for key in ('CDR6_BASE_URL', 'CDR6_SERVICE_KEY', 'CDR6_TIMEOUT',
                    'CDR_TRANSFER_TARGETS'):
            monkeypatch.delenv(key, raising=False)
        importlib.reload(config_module)


def test_the_modules_are_deleted(app):
    """Not merely unregistered. An importable blueprint is one line from live."""
    import importlib
    for mod in ('app.api.transfer', 'app.routes.transfer'):
        try:
            importlib.import_module(mod)
        except ModuleNotFoundError:
            continue
        raise AssertionError(f'{mod} still exists')


def test_the_nav_no_longer_offers_transfer(client):
    """A nav link to a 404 is worse than no link: it reads as an outage."""
    html = client.get('/docs').data.decode()
    assert '>Transfer<' not in html
    assert 'transfer_web' not in html
