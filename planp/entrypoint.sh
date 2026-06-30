#!/usr/bin/env bash
set -e

echo "Running database migrations..."
flask db upgrade

echo "Starting application..."
exec gunicorn --bind 0.0.0.0:9030 --workers 2 \
    --access-logfile - \
    --access-logformat '%(t)s %(h)s "%(r)s" %(s)s %(L)ss' \
    "app:create_app()"
