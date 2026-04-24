#!/bin/bash
# High-Reliability Start Script for TikTok Bot

echo "🚀 Phase 1: Warming up the Database Engine..."
python manage.py migrate --noinput

echo "🚀 Phase 2: Clearing the launchpad..."
python manage.py collectstatic --noinput

echo "🚀 Phase 3: Activating the AI Social Command Center..."
exec gunicorn --bind 0.0.0.0:$PORT config.wsgi:application --workers 1 --timeout 180 --log-file -
