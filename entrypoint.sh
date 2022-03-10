#!/bin/sh

set -e

python manage.py collectstatic --no-input
python manage.py runserver

# gunicorn --workers=4 root.wsgi:application --bind 0.0.0.0:8000 --timeout 900
