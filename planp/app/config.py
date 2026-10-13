import os
import re


#: The historical default. Kept named so it can be REJECTED rather than
#: silently accepted: a fallback that is a public constant is worse than no
#: fallback, because the service starts and looks healthy.
_PLACEHOLDER_SECRET = 'change-me'


def _require_secret_key():
    """The Flask session-signing key — required in production, never guessable.

    This was `os.environ.get('FLASK_SECRET_KEY', 'change-me')`. If the variable
    ever went missing from a deploy, the key became the literal string
    `change-me`: published in this repo, which is PUBLIC, and therefore known
    to anyone. The service would start, pass its health check, and sign session
    cookies with a value a stranger could reproduce. Nothing would look wrong.

    That is the whole argument for failing instead. A missing secret is a
    deployment fault, and a deployment fault should stop the deployment — not
    degrade quietly into a weaker one.

    Production is identified by `AUTH_DISABLED=false`, which is what makes
    sessions carry anything worth signing. Both CI and the test suite set
    AUTH_DISABLED=false AND supply their own key, so they are unaffected.

    In local dev (AUTH_DISABLED defaults true) an unset key yields a RANDOM
    per-process value rather than a shared constant. Sessions then do not
    survive a restart, which is a fair price: it means no guessable key exists
    anywhere, in any environment, ever.
    """
    key = os.environ.get('FLASK_SECRET_KEY', '')
    auth_disabled = os.environ.get(
        'AUTH_DISABLED', 'true').lower() in ('true', '1', 'yes')

    if key and key != _PLACEHOLDER_SECRET:
        return key

    if not auth_disabled:
        raise RuntimeError(
            "FLASK_SECRET_KEY is %s, and AUTH_DISABLED is false.\n"
            "\n"
            "This key signs session cookies. Starting without a real one "
            "would sign them with a value published in this repository, so "
            "the service refuses to start instead.\n"
            "\n"
            "Set it in the service's .env and recreate the container:\n"
            "  FLASK_SECRET_KEY=$(python3 -c "
            "'import secrets; print(secrets.token_hex(32))')\n"
            "  docker-compose up -d --force-recreate\n"
            "(a plain `restart` keeps the old environment — this service "
            "uses env_file)"
            % ("set to the placeholder %r" % _PLACEHOLDER_SECRET
               if key else "not set"))

    import secrets as _secrets
    return _secrets.token_hex(32)


#: The local-dev database. Named, like the placeholder secret above, so the
#: production path can REJECT it instead of inheriting it.
#:
#: DB name "pdhc_gateway" is the legacy name retained for data continuity
#: (rollup #325 / ticket #336). Pre-2026 the service was called "PDHC
#: Gateway"; renaming the volume would risk data loss.
_DEV_DATABASE_URL = (
    'postgresql+psycopg2://pdhc_admin:change-me@localhost:9031/pdhc_gateway')


def _auth_disabled():
    """True in local dev, false in production. The production tell.

    AUTH_DISABLED is what decides whether sessions carry a real identity, so
    it is the same switch both guards in this module key off. Read as a
    function rather than off `Config`, because `Config`'s attributes are
    evaluated while the class body runs and the guards need it before that.
    """
    return os.environ.get(
        'AUTH_DISABLED', 'true').lower() in ('true', '1', 'yes')


def _require_database_url():
    """The database to connect to — required in production, no fallback.

    This was `os.environ.get('DATABASE_URL', <the dev URL above>)`, which is
    the same shape of fault as the secret key: if the variable went missing
    from a deploy, the service would come up pointed at a *different*
    database than intended, with a password published in this PUBLIC repo.

    It fails differently from a bad secret key, and that is the only reason
    this was lower priority rather than harmless. A wrong connection string
    usually fails at connect, loudly. But "usually" is doing real work in that
    sentence: anything actually listening on localhost:9031 that accepts those
    credentials gets connected to and written to, and on a developer Mac
    127.0.0.1:9031 is plan's own db container.

    Two rejected shapes, not one:

    * **missing or the dev URL** — the deploy lost the variable.
    * **a URL with an EMPTY password** — because of how the container is
      configured. `docker-compose.yml` builds DATABASE_URL in its
      `environment:` block from `${POSTGRES_USER}`, `${POSTGRES_PASSWORD}`
      and `${POSTGRES_DB}`. Compose expands an unset variable to the empty
      string without complaint, so a missing POSTGRES_PASSWORD yields
      `postgresql://pdhc_admin:@db:5432/pdhc_gateway` — a URL that contains
      no placeholder and so passes any check looking only for `change-me`.
      That connects successfully whenever the server's pg_hba has a `trust`
      rule for the client address, which §9 of the workspace CLAUDE.md
      documents as the default in these images. So it is checked for by name.

    Dev keeps a working default, because unlike a signing key there is no
    random value that would do: the service has to be told where its data is.
    """
    url = os.environ.get('DATABASE_URL', '').strip()
    bad = None

    if not url:
        bad = "not set"
    elif url == _DEV_DATABASE_URL or _PLACEHOLDER_SECRET in url:
        bad = "set to the local-dev URL, whose password is published in this " \
              "repository"
    # NOTE the scheme class allows digits and '+': the live shape is
    # `postgresql+psycopg2://` (#711 made every PDHC service name its driver
    # explicitly). A `[a-z+]+` scheme class does not match `psycopg2` and so
    # missed every real URL this check exists for.
    elif re.match(r'^[^:/]+://[^/@]*:@', url):
        bad = ("set to a URL with an EMPTY password — most likely "
               "POSTGRES_PASSWORD is missing from the .env, which compose "
               "expands to nothing while building DATABASE_URL")

    if bad is None:
        return url

    if not _auth_disabled():
        raise RuntimeError(
            "DATABASE_URL is %s, and AUTH_DISABLED is false.\n"
            "\n"
            "Rather than start against an unintended database, the service "
            "refuses to start.\n"
            "\n"
            "Set POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_DB (compose "
            "builds DATABASE_URL from them), or DATABASE_URL directly, then:\n"
            "  docker-compose up -d --force-recreate app\n"
            "(a plain `restart` keeps the old environment — this service "
            "uses env_file)" % bad)

    return _DEV_DATABASE_URL


def _session_cookie_secure():
    """Mark the session cookie Secure, so it is never sent over plain HTTP.

    Production is reached only as https://plan.pdhc.se, where nginx terminates
    TLS and proxies plain HTTP to gunicorn. So Flask itself sees an http
    request and cannot infer this; the flag has to be set deliberately. It
    costs nothing in the normal case and removes the case where a request
    arrives over HTTP and the session cookie goes with it.

    Off in local dev, where the service is http://localhost:9030 and a Secure
    cookie would simply never be stored.

    Explicitly overridable, because the flag has one real cost: reaching
    production directly on 127.0.0.1:9030 through an ssh forward is plain
    HTTP, so a logged-in page cannot be debugged that way while this is on.
    `SESSION_COOKIE_SECURE=false` in the environment turns it off for that,
    rather than someone editing this file under time pressure.
    """
    raw = os.environ.get('SESSION_COOKIE_SECURE')
    if raw is not None and raw.strip() != '':
        return raw.strip().lower() in ('true', '1', 'yes')
    return not _auth_disabled()


class Config:
    SQLALCHEMY_DATABASE_URI = _require_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = _require_secret_key()

    # ------------------------------------------------------------------
    # Session cookie hardening
    # ------------------------------------------------------------------
    SESSION_COOKIE_SECURE = _session_cookie_secure()

    # No script should ever read this cookie. Flask already defaults this to
    # True; stated here so a future edit has to argue with a line rather than
    # with an absence.
    SESSION_COOKIE_HTTPONLY = True

    # 'Lax', NOT 'Strict', and that is load-bearing: SSO login finishes with a
    # top-level GET redirect from sso.pdhc.se back to
    # /api/v1/auth/callback (app/api/auth.py). Lax sends the cookie on exactly
    # that — a top-level navigation — while still withholding it from
    # cross-site POSTs and subresource requests. 'Strict' would drop it on the
    # callback and break login with no error anyone could read.
    SESSION_COOKIE_SAMESITE = 'Lax'

    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'

    # When True, all auth checks are bypassed (local dev/debug mode).
    # Production (SSO) will set this to False.
    AUTH_DISABLED = os.environ.get('AUTH_DISABLED', 'true').lower() in ('true', '1', 'yes')

    # SSO integration (used when AUTH_DISABLED=false)
    SSO_BASE_URL = os.environ.get('SSO_BASE_URL', 'http://localhost:9000')
    SSO_CLIENT_ID = os.environ.get('SSO_CLIENT_ID', '')
    SSO_CLIENT_SECRET = os.environ.get('SSO_CLIENT_SECRET', '')
    SSO_CALLBACK_URL = os.environ.get('SSO_CALLBACK_URL', 'http://localhost:9030/api/v1/auth/callback')

    # Forms builder API key (for external service-to-service access)
    API_KEY = os.environ.get('API_KEY', '')

    # Service-key credentials accepted by api/auth.py service-key bypass
    # (sim.pdhc may consult plan.pdhc to resolve concept GUIDs at run time).
    # PLAN_LOADER_SERVICE_KEY was read here until 2026-10-05; nothing reads it
    # now, so the variable is inert wherever it is still set.
    SIM_PDHC_SERVICE_KEY = os.environ.get('SIM_PDHC_SERVICE_KEY', '')

    # Upstream services
    CONTRACT_BASE_URL = os.environ.get('CONTRACT_BASE_URL', 'http://localhost:9021')

    # Rate limiting
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '200 per minute')
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
    RATELIMIT_HEADERS_ENABLED = True

    # ------------------------------------------------------------------
    # Guided PlanDef authoring assistant (epic #516, GA-1..GA-6)
    # ------------------------------------------------------------------
    # Opt-in tool that helps a non-expert author build a correct PlanDef.
    # OFF by default: when disabled the /api/v1/authoring/* endpoints report
    # "service disabled" and NOTHING about existing concept/plandef saving
    # changes. The deterministic validator (Layer 1) is usable independently
    # of the Claude assistant (Layer 2); Layer 2 additionally needs a key.
    AUTHORING_ASSISTANT_ENABLED = os.environ.get(
        'AUTHORING_ASSISTANT_ENABLED', 'false'
    ).lower() in ('true', '1', 'yes')

    # Anthropic Messages API — the assistant (Layer 2) calls Claude with this.
    # NEVER hardcode a key; it is read from the environment only. With no key
    # the assistant degrades to validation-only and never raises.
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
    ANTHROPIC_API_BASE = os.environ.get(
        'ANTHROPIC_API_BASE', 'https://api.anthropic.com'
    )

    # Selectable Claude models (allowlist). The caller picks one per request;
    # a model not in this list is rejected. Comma-separated env override.
    AUTHORING_ASSISTANT_MODELS = [
        m.strip() for m in os.environ.get(
            'AUTHORING_ASSISTANT_MODELS',
            'claude-sonnet-5,claude-opus-4-8,claude-haiku-4-5-20251001',
        ).split(',') if m.strip()
    ]
    AUTHORING_ASSISTANT_DEFAULT_MODEL = os.environ.get(
        'AUTHORING_ASSISTANT_DEFAULT_MODEL', 'claude-sonnet-5'
    )
    # Bound the assistant's output + wall-clock so a slow call can't hang a
    # worker. Kept modest — a concept suggestion is small.
    AUTHORING_ASSISTANT_MAX_TOKENS = int(
        os.environ.get('AUTHORING_ASSISTANT_MAX_TOKENS', '1500')
    )
    AUTHORING_ASSISTANT_TIMEOUT_SECONDS = float(
        os.environ.get('AUTHORING_ASSISTANT_TIMEOUT_SECONDS', '30')
    )

    # openEHR-realisability check (#523): the builder's "Check openEHR export"
    # button proxies to rosetta.pdhc's /api/v1/openehr/realisable. Both unset =
    # the button degrades gracefully ("rosetta_not_configured"). ROSETTA_SERVICE_KEY
    # must match rosetta's own ROSETTA_SERVICE_KEY.
    ROSETTA_BASE_URL = os.environ.get('ROSETTA_BASE_URL', '')
    ROSETTA_SERVICE_KEY = os.environ.get('ROSETTA_SERVICE_KEY', '')

    # #786 — the #530 CDR6_* settings are GONE, deliberately and by name.
    #
    # plan.pdhc is the authoring plane. The Transfer page it fed was a thin
    # proxy over cdr_6's engine, and it reached cdr_6 by presenting
    # `X-Source-Service: sim.pdhc` with cdr_6's sim service key — so the
    # authoring plane held a data-plane credential it had no other use for, and
    # cdr_6's audit attributed those transfers to sim.pdhc rather than to plan
    # or to the operator who clicked. `sim cdr-transfer` already does the same
    # job from the service that legitimately owns that key.
    #
    # They are NOT read back under any name. An operator with a stale
    # CDR6_SERVICE_KEY in their .env must be IGNORED, not quietly honoured:
    # silently re-admitting a borrowed credential is how retired identities
    # come back (#727 monitor.pdhc, #736 loader.pdhc). Pinned by
    # tests/test_transfer_retired.py.

    # #521 GA-5 — fail-closed validation on concept/plandef saves. When True
    # (default), an ERROR-severity validation issue REJECTS the save on both the
    # web and JSON-API paths (warnings pass). An admin/SU may force a save with
    # ?override_validation=1 (audited to the log). Kill-switch: set to false.
    PLANDEF_VALIDATION_ENFORCED = os.environ.get(
        'PLANDEF_VALIDATION_ENFORCED', 'true'
    ).lower() in ('true', '1', 'yes')
