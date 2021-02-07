#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Collect static files
echo "Collect static files"
mkdir -p static upload
sed -i -e 's/\# STATIC_ROOT/STATIC_ROOT/g' project/settings.py
python manage.py collectstatic --noinput
sed -i -e 's/STATIC_ROOT/\# STATIC_ROOT/g' project/settings.py

# Start server
echo "Starting server"
python manage.py runserver
