#!/bin/bash

python manage.py migrate --noinput
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 KalaMax_Project.wsgi:application
