#!/bin/bash

# Run migrations to build the tables in Postgres
python manage.py migrate --noinput

# Create a default superuser if it doesn't exist
# Username: admin
# Password: admin123 (You can change this once logged in)
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')
    print("Superuser 'admin' created successfully.")
else:
    print("Superuser 'admin' already exists.")
END

# Start the application
gunicorn config.wsgi --log-file -
