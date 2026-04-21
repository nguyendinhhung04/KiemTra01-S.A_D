#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Seeding database..."
python manage.py seed_db

echo "Seeding graph database..."
python seed_graph.py

echo "Starting server..."
exec "$@"
