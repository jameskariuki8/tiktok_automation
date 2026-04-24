web: (ls -R /app/.cache || echo "Cache Empty") && PLAYWRIGHT_BROWSERS_PATH=/app/.cache playwright install chromium && python manage.py migrate && gunicorn config.wsgi --log-file -
worker: celery -A config worker --loglevel=info -P solo
