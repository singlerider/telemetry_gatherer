#!/usr/bin/env sh
python manage.py migrate
python manage.py loaddata telemetry_app_data
python manage.py runserver 0.0.0.0:8000
