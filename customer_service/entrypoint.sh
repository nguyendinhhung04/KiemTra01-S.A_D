#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Making migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Seeding database..."
python manage.py seed_db

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
