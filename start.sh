#!/bin/bash
echo "🐳 DOCKER ENGINE ENGAGED"

echo "🚀 Phase 1: Database Handshake..."
# Force migrations with full error reporting
python manage.py migrate --noinput --settings=config.settings || { echo "❌ MIGRATION FAILED!"; exit 1; }

echo "🚀 Phase 2: Launching Social Command Center..."
exec gunicorn --bind 0.0.0.0:$PORT config.wsgi:application --workers 1 --timeout 180 --log-file -
