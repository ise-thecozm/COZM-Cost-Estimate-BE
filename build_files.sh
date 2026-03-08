#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Create cache table for DB-based caching
python manage.py createcachetable

# Run migrations
python manage.py migrate --noinput

echo "Build completed successfully!"
