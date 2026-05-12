#!/usr/bin/env bash
set -e

python manage.py migrate --noinput

exec gunicorn ticketSystem.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --access-logfile - \
    --error-logfile -
