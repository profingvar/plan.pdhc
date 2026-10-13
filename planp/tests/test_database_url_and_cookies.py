"""Two remaining `change-me`-shaped holes, closed together.

1. **DATABASE_URL had the same published fallback as the secret key did.**
   `os.environ.get('DATABASE_URL', 'postgresql://pdhc_admin:change-me@…')`
   meant a deploy that lost the variable started against a *different*
   database than intended, with a password committed to this PUBLIC repo.

2. **The session cookie was not marked Secure.** nginx terminates TLS and
   proxies plain HTTP to gunicorn, so Flask sees an http request and cannot
   infer this — it has to be set deliberately.

Imports live INSIDE the tests, for the reason spelled out at length in
`test_secret_key_required.py`: `Config`'s attributes are evaluated at import
time, and importing this module during pytest's COLLECTION phase — before
conftest's session fixture repoints DATABASE_URL at a temporary sqlite file —
froze the postgres default into the class and broke 285 unrelated tests.
"""
from __future__ import annotations

import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _db():
    from app.config import _require_database_url, _DEV_DATABASE_URL
    return _require_database_url, _DEV_DATABASE_URL


def _cookie():
    from app.config import _session_cookie_secure
    return _session_cookie_secure


@pytest.fixture
def env(monkeypatch):
    for v in ('DATABASE_URL', 'AUTH_DISABLED', 'SESSION_COOKIE_SECURE'):
        monkeypatch.delenv(v, raising=False)
    return monkeypatch


# ---------------------------------------------------------------------------
# DATABASE_URL
# ---------------------------------------------------------------------------

def test_a_real_url_is_used_as_given(env):
    _require_database_url, _ = _db()
    env.setenv('AUTH_DISABLED', 'false')
    env.setenv('DATABASE_URL', 'postgresql+psycopg2://u:realpw@db:5432/d')
    assert _require_database_url() == 'postgresql+psycopg2://u:realpw@db:5432/d'


def test_production_without_a_url_REFUSES_TO_START(env):
    _require_database_url, _ = _db()
    env.setenv('AUTH_DISABLED', 'false')
    with pytest.raises(RuntimeError) as e:
        _require_database_url()
    assert 'DATABASE_URL' in str(e.value)


def test_production_with_the_DEV_URL_also_refuses(env):
    """Pointing production at the dev URL explicitly is no better than losing
    the variable — it is the same published password."""
    _require_database_url, _DEV = _db()
    env.setenv('AUTH_DISABLED', 'false')
    env.setenv('DATABASE_URL', _DEV)
    with pytest.raises(RuntimeError):
        _require_database_url()


def test_production_with_ANY_change_me_password_refuses(env):
    """Not just the one literal default — any URL carrying the published
    placeholder password, whatever host or driver it names."""
    _require_database_url, _ = _db()
    env.setenv('AUTH_DISABLED', 'false')
    env.setenv('DATABASE_URL',
               'postgresql+psycopg2://pdhc_admin:change-me@db:5432/pdhc_gateway')
    with pytest.raises(RuntimeError):
        _require_database_url()


@pytest.mark.parametrize('url', [
    'postgresql://pdhc_admin:@db:5432/pdhc_gateway',
    # The live driver shape. A `[a-z+]+` scheme class does not match
    # `psycopg2`, so the first version of this check missed every real URL it
    # existed for — #711 made every PDHC service name its driver explicitly.
    'postgresql+psycopg2://pdhc_admin:@db:5432/pdhc_gateway',
])
def test_production_with_an_EMPTY_PASSWORD_refuses(env, url):
    """The failure this service is actually exposed to.

    `docker-compose.yml` builds DATABASE_URL in its `environment:` block from
    `${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}`. Compose
    expands an unset variable to the empty string silently, so a missing
    POSTGRES_PASSWORD produces a URL containing no placeholder at all — one
    that a check looking only for `change-me` waves straight through. And it
    CONNECTS, wherever pg_hba has a `trust` rule for the client address, which
    §9 of the workspace CLAUDE.md documents as these images' default.
    """
    _require_database_url, _ = _db()
    env.setenv('AUTH_DISABLED', 'false')
    env.setenv('DATABASE_URL', url)
    with pytest.raises(RuntimeError) as e:
        _require_database_url()
    assert 'POSTGRES_PASSWORD' in str(e.value), (
        'the error does not name the variable that is actually missing')


def test_a_url_with_no_password_section_is_NOT_mistaken_for_an_empty_one(env):
    """`user@host` is a deliberate choice (trust/peer/socket auth), not the
    compose-expansion accident above. Different thing, must not be refused."""
    _require_database_url, _ = _db()
    env.setenv('AUTH_DISABLED', 'false')
    env.setenv('DATABASE_URL', 'postgresql+psycopg2://pdhc_admin@db:5432/d')
    assert _require_database_url().endswith('/d')


def test_the_SQLITE_url_this_suite_runs_on_is_accepted(env):
    """Regression guard with teeth: an over-eager empty-password regex would
    match `sqlite:////tmp/x.db` and take the whole suite down with it."""
    _require_database_url, _ = _db()
    env.setenv('AUTH_DISABLED', 'false')
    env.setenv('DATABASE_URL', 'sqlite:////tmp/plan_test.db')
    assert _require_database_url() == 'sqlite:////tmp/plan_test.db'


def test_the_error_SAYS_WHAT_TO_DO(env):
    _require_database_url, _ = _db()
    env.setenv('AUTH_DISABLED', 'false')
    with pytest.raises(RuntimeError) as e:
        _require_database_url()
    msg = str(e.value)
    assert 'POSTGRES_PASSWORD' in msg, 'does not say where the value comes from'
    assert 'force-recreate' in msg, 'does not say how to apply it'
    assert 'env_file' in msg, 'does not warn that `restart` keeps the old env'


def test_local_dev_without_a_url_still_gets_a_working_default(env):
    """Unlike a signing key there is no random value that would do — the
    service has to be told where its data is. So dev keeps its default."""
    _require_database_url, _DEV = _db()
    env.setenv('AUTH_DISABLED', 'true')
    assert _require_database_url() == _DEV


def test_AUTH_DISABLED_defaults_to_dev_so_a_bare_checkout_still_runs(env):
    _require_database_url, _DEV = _db()
    assert _require_database_url() == _DEV


# ---------------------------------------------------------------------------
# Session cookie
# ---------------------------------------------------------------------------

def test_production_marks_the_session_cookie_SECURE(env):
    env.setenv('AUTH_DISABLED', 'false')
    assert _cookie()() is True


def test_local_dev_does_not(env):
    """http://localhost:9030 would simply never store a Secure cookie."""
    env.setenv('AUTH_DISABLED', 'true')
    assert _cookie()() is False


@pytest.mark.parametrize('raw,want', [
    ('false', False), ('0', False), ('no', False),
    ('true', True), ('1', True), ('yes', True), ('True', True),
])
def test_an_explicit_setting_overrides_both_ways(env, raw, want):
    """The escape hatch: production is reachable directly on 127.0.0.1:9030
    through an ssh forward, which is plain HTTP, so a logged-in page cannot be
    debugged there while Secure is on. Overridable by environment rather than
    by editing config.py under time pressure."""
    env.setenv('AUTH_DISABLED', 'false')
    env.setenv('SESSION_COOKIE_SECURE', raw)
    assert _cookie()() is want


def test_an_EMPTY_override_falls_back_to_the_derived_value(env):
    """`SESSION_COOKIE_SECURE=` in a .env is an unset variable, not a False
    one. Reading it as False would silently disable the flag in production."""
    env.setenv('AUTH_DISABLED', 'false')
    env.setenv('SESSION_COOKIE_SECURE', '')
    assert _cookie()() is True


def test_SAMESITE_is_LAX_not_STRICT():
    """Load-bearing, and the reason this is asserted rather than left to
    taste: SSO login finishes with a top-level GET redirect from sso.pdhc.se
    back to /api/v1/auth/callback. Lax sends the cookie on a top-level
    navigation; Strict withholds it and breaks login with no readable error.
    """
    from app.config import Config
    assert Config.SESSION_COOKIE_SAMESITE == 'Lax'
    assert Config.SESSION_COOKIE_HTTPONLY is True


def test_the_SSO_CALLBACK_IS_STILL_A_GET_REDIRECT():
    """The premise of the test above, checked against the route rather than
    assumed. If the callback ever becomes a POST, Lax stops sending the cookie
    and this assertion is the thing that says so.
    """
    import inspect
    from app.api import auth as auth_mod

    src = inspect.getsource(auth_mod)
    assert "@auth_bp.route('/callback', methods=['GET'])" in src, (
        "the SSO callback is no longer a plain GET route — re-check whether "
        "SESSION_COOKIE_SAMESITE='Lax' still lets the session survive login")


# ---------------------------------------------------------------------------
# The call sites. Every test above exercises the accessors directly, so all of
# them stay green if `Config` goes back to `os.environ.get(..., 'change-me')`
# — which is the entire bug. Same hole that let #729 hide for five months.
# ---------------------------------------------------------------------------

def test_Config_ACTUALLY_USES_the_checked_accessors():
    import inspect
    from app import config as cfg

    src = inspect.getsource(cfg)
    assert 'SQLALCHEMY_DATABASE_URI = _require_database_url()' in src, (
        'Config.SQLALCHEMY_DATABASE_URI no longer goes through the check')
    assert "os.environ.get(\n        'DATABASE_URL'," not in src, (
        'the unchecked DATABASE_URL fallback is back')
    assert 'SESSION_COOKIE_SECURE = _session_cookie_secure()' in src, (
        'Config.SESSION_COOKIE_SECURE no longer goes through the accessor')


def test_a_production_shaped_process_REFUSES_TO_IMPORT():
    """The end-to-end proof, in a SUBPROCESS — what a real container does.

    Doctoring the environment and re-importing app.config in THIS process
    would either hit the already-imported module or corrupt it for every test
    that follows.
    """
    base = dict(os.environ)
    base['AUTH_DISABLED'] = 'false'
    base['FLASK_SECRET_KEY'] = 'a-real-key'      # isolate the DB check
    base.pop('DATABASE_URL', None)

    r = subprocess.run([sys.executable, '-c', 'import app.config'],
                       env=base, capture_output=True, text=True, cwd=REPO)
    assert r.returncode != 0, (
        'a production-shaped process started with no DATABASE_URL')
    assert 'DATABASE_URL' in r.stderr

    # ...and the same process starts once it is supplied.
    base['DATABASE_URL'] = 'postgresql+psycopg2://u:realpw@db:5432/d'
    ok = subprocess.run([sys.executable, '-c', 'import app.config'],
                        env=base, capture_output=True, text=True, cwd=REPO)
    assert ok.returncode == 0, ok.stderr


def test_the_production_shaped_process_also_refuses_an_EMPTY_PASSWORD():
    """The compose-expansion case, end to end."""
    base = dict(os.environ)
    base['AUTH_DISABLED'] = 'false'
    base['FLASK_SECRET_KEY'] = 'a-real-key'
    base['DATABASE_URL'] = 'postgresql+psycopg2://pdhc_admin:@db:5432/pdhc_gateway'
    r = subprocess.run([sys.executable, '-c', 'import app.config'],
                       env=base, capture_output=True, text=True, cwd=REPO)
    assert r.returncode != 0, (
        'started against a database reached with an empty password')
    assert 'POSTGRES_PASSWORD' in r.stderr
