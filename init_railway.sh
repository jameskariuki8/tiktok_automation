#!/bin/bash
set -e

echo "📊 --- DATABASE INITIALIZATION START ---"

# 1. Force Migrations
echo "🚀 Running Migrations..."
python manage.py migrate --noinput --fake-initial

# 2. Run Seeder Command
echo "👤 Attempting Admin Seeder..."
python manage.py create_admin_user || echo "⚠️ Management command failed, trying fallback..."

# 3. Direct Python Fallback (The Nuclear Option)
echo "🔒 Running Direct User Sync..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')
    print("✅ SUCCESS: Admin created via Fallback.")
else:
    print("ℹ️ INFO: Admin already exists.")
END

echo "📊 --- DATABASE INITIALIZATION DONE ---"

# Start the application
exec gunicorn config.wsgi --log-file -
