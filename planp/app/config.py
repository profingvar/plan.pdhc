import os


class Config:
    # DB name "pdhc_gateway" is the legacy name retained for data continuity
    # (rollup #325 / ticket #336). Pre-2026 the service was called
    # "PDHC Gateway"; renaming the volume would risk data loss.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://pdhc_admin:change-me@localhost:9031/pdhc_gateway'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'change-me')

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
    # (loader.pdhc runs the bulk-concept loader from operator's machine;
    # sim.pdhc may consult plan.pdhc to resolve concept GUIDs at run time).
    PLAN_LOADER_SERVICE_KEY = os.environ.get('PLAN_LOADER_SERVICE_KEY', '')
    SIM_PDHC_SERVICE_KEY = os.environ.get('SIM_PDHC_SERVICE_KEY', '')

    # Upstream services
    CONTRACT_BASE_URL = os.environ.get('CONTRACT_BASE_URL', 'http://localhost:9021')

    # Rate limiting
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '200 per minute')
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
    RATELIMIT_HEADERS_ENABLED = True
