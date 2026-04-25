#!/bin/bash

# Run migrations to build the tables in Postgres
python manage.py migrate --noinput

# Create the default admin user (id=1) if it doesn't exist
python manage.py create_admin_user

# Start the application
gunicorn config.wsgi --log-file -
