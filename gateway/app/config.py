import os
from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://pdhc_admin:REDACTED@localhost:9031/pdhc_gateway'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'change-me')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'change-me')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'

    # When True, all auth checks are bypassed (local dev/debug mode).
    # Production (SSO) will set this to False.
    AUTH_DISABLED = os.environ.get('AUTH_DISABLED', 'true').lower() in ('true', '1', 'yes')

    # Rate limiting
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '200 per minute')
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
    RATELIMIT_HEADERS_ENABLED = True
