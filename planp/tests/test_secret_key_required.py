"""The session key must never silently fall back to a published constant.

`SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'change-me')` meant a deploy
that lost the variable would start, pass its health check, and sign session
cookies with a string committed to this repository — which is PUBLIC. Nothing
would look wrong. That is the argument for failing: a missing secret is a
deployment fault, and a deployment fault should stop the deployment rather
than quietly degrade into a weaker one.

Production is identified by `AUTH_DISABLED=false`. CI and this suite both set
AUTH_DISABLED=false *and* supply their own key, so the strict path is the one
they exercise.
"""
from __future__ import annotations

import os

import pytest

# NOT imported at module level, deliberately.
#
# `Config`'s attributes are evaluated when `app.config` is first imported,
# including
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '…:9031…')
# and the session-scoped `app` fixture in conftest sets DATABASE_URL to a
# temporary sqlite file *when it first runs*. A module-level import here made
# pytest import app.config during COLLECTION — before that fixture — so the
# postgres default was frozen into the class and 285 later tests failed with
# "connection to server at localhost port 9031 refused".
#
# Importing inside each test keeps the original ordering.


def _fn():
    from app.config import _require_secret_key, _PLACEHOLDER_SECRET
    return _require_secret_key, _PLACEHOLDER_SECRET


@pytest.fixture
def env(monkeypatch):
    monkeypatch.delenv('FLASK_SECRET_KEY', raising=False)
    monkeypatch.delenv('AUTH_DISABLED', raising=False)
    return monkeypatch


def test_a_real_key_is_used_as_given(env):
    _require_secret_key, _PLACEHOLDER_SECRET = _fn()
    env.setenv('AUTH_DISABLED', 'false')
    env.setenv('FLASK_SECRET_KEY', 'a-real-key')
    assert _require_secret_key() == 'a-real-key'


def test_production_without_a_key_REFUSES_TO_START(env):
    """The whole point. Previously this returned 'change-me' and the service
    came up looking healthy."""
    _require_secret_key, _PLACEHOLDER_SECRET = _fn()
    env.setenv('AUTH_DISABLED', 'false')
    with pytest.raises(RuntimeError) as e:
        _require_secret_key()
    assert 'FLASK_SECRET_KEY' in str(e.value)


def test_production_with_the_PLACEHOLDER_also_refuses(env):
    """Setting it explicitly to the old default is no better than leaving it
    unset — it is the same published string."""
    _require_secret_key, _PLACEHOLDER_SECRET = _fn()
    env.setenv('AUTH_DISABLED', 'false')
    env.setenv('FLASK_SECRET_KEY', _PLACEHOLDER_SECRET)
    with pytest.raises(RuntimeError) as e:
        _require_secret_key()
    assert _PLACEHOLDER_SECRET in str(e.value)


def test_the_error_SAYS_WHAT_TO_DO(env):
    """An error that stops a deploy has to be actionable at 3am, including the
    detail that a plain `restart` will not pick the new value up."""
    _require_secret_key, _PLACEHOLDER_SECRET = _fn()
    env.setenv('AUTH_DISABLED', 'false')
    with pytest.raises(RuntimeError) as e:
        _require_secret_key()
    msg = str(e.value)
    assert 'token_hex' in msg, 'does not say how to generate one'
    assert 'force-recreate' in msg, 'does not say how to apply it'
    assert 'env_file' in msg, 'does not warn that `restart` keeps the old env'


@pytest.mark.parametrize('flag', ['true', 'True', '1', 'yes'])
def test_local_dev_without_a_key_gets_a_RANDOM_one_not_a_constant(env, flag):
    """Dev must keep working, but with a value nobody can guess. Sessions then
    do not survive a restart, which is the fair price for no guessable key
    existing in any environment."""
    _require_secret_key, _PLACEHOLDER_SECRET = _fn()
    env.setenv('AUTH_DISABLED', flag)
    a, b = _require_secret_key(), _require_secret_key()
    assert a != b, 'the dev fallback is a shared constant again'
    assert a != _PLACEHOLDER_SECRET
    assert len(a) >= 32


def test_dev_still_honours_an_explicit_key(env):
    _require_secret_key, _PLACEHOLDER_SECRET = _fn()
    env.setenv('AUTH_DISABLED', 'true')
    env.setenv('FLASK_SECRET_KEY', 'my-dev-key')
    assert _require_secret_key() == 'my-dev-key'


def test_AUTH_DISABLED_defaults_to_dev_so_a_bare_checkout_still_runs(env):
    """With neither variable set — a fresh clone — the service must start."""
    _require_secret_key, _PLACEHOLDER_SECRET = _fn()
    assert len(_require_secret_key()) >= 32


def test_the_published_placeholder_is_never_returned(env):
    """Belt and braces across every combination."""
    _require_secret_key, _PLACEHOLDER_SECRET = _fn()
    for auth in ('true', 'false'):
        for key in (None, '', _PLACEHOLDER_SECRET):
            env.setenv('AUTH_DISABLED', auth)
            if key is None:
                env.delenv('FLASK_SECRET_KEY', raising=False)
            else:
                env.setenv('FLASK_SECRET_KEY', key)
            try:
                assert _require_secret_key() != _PLACEHOLDER_SECRET
            except RuntimeError:
                pass        # refusing is the other acceptable outcome


# ---------------------------------------------------------------------------
# Every test above calls `_require_secret_key()` directly, so they all stay
# green if `Config.SECRET_KEY` goes back to `os.environ.get(..., 'change-me')`
# — which is the entire bug. Verified: reverting the call site left 11 of 11
# passing. These two assert the CALL SITE.
# ---------------------------------------------------------------------------

def test_Config_ACTUALLY_USES_the_checked_accessor():
    """A source check, because `Config`'s attributes evaluate at import time
    and re-importing it mid-suite is what poisoned this file's first version.
    """
    import inspect
    from app import config as cfg

    src = inspect.getsource(cfg)
    assert 'SECRET_KEY = _require_secret_key()' in src, (
        'Config.SECRET_KEY no longer goes through the checked accessor')
    assert "SECRET_KEY = os.environ.get('FLASK_SECRET_KEY'" not in src, (
        'the unchecked fallback is back')


def test_a_production_shaped_process_REFUSES_TO_IMPORT():
    """The real end-to-end proof, in a SUBPROCESS.

    Importing app.config with a doctored environment inside this process would
    either hit the already-imported module or corrupt it for every test that
    follows. A subprocess gets a clean interpreter and tells us what a real
    container would do: refuse to start.
    """
    import os
    import subprocess
    import sys

    env = dict(os.environ)
    env.pop('FLASK_SECRET_KEY', None)
    env['AUTH_DISABLED'] = 'false'
    r = subprocess.run(
        [sys.executable, '-c', 'import app.config'],
        env=env, capture_output=True, text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    assert r.returncode != 0, (
        'a production-shaped process started without a secret key')
    assert 'FLASK_SECRET_KEY' in r.stderr

    # ...and the same process DOES start once the key is supplied.
    env['FLASK_SECRET_KEY'] = 'a-real-key'
    ok = subprocess.run(
        [sys.executable, '-c', 'import app.config'],
        env=env, capture_output=True, text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    assert ok.returncode == 0, ok.stderr
