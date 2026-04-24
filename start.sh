#!/bin/bash
echo "🐳 DOCKER ENGINE ENGAGED"

echo "🚀 Phase 0: Erasing Zombie Records..."
rm -rf /app/db.sqlite3

echo "🚀 Phase 1: Building the New Architecture..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput --settings=config.settings || { echo "❌ MIGRATION FAILED!"; exit 1; }

echo "🚀 Phase 2: Activating Social Command Center..."
exec gunicorn --bind 0.0.0.0:$PORT config.wsgi:application --workers 1 --timeout 180 --log-file -
