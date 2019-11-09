#!/usr/bin/env bash

whoami

echo "Applying database migration"
python3 manage.py migrate

echo "Starting Gunicorn"
gunicorn backend.wsgi --bind 0.0.0.0:8080
