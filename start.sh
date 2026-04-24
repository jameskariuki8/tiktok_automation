#!/bin/bash
echo "🚀 Phase 0: Clearing the old gears..."
rm -f db.sqlite3

echo "🚀 Phase 1: Rebuilding the Database Engine..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "🚀 Phase 2: Clearing the launchpad..."
python manage.py collectstatic --noinput

echo "🚀 Phase 3: Activating the AI Social Command Center..."
exec gunicorn --bind 0.0.0.0:$PORT config.wsgi:application --workers 1 --timeout 180 --log-file -
