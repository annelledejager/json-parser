#!/bin/bash

cmd="$@"

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Create new database migrations
echo "Create new database migrations"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

## Run command from compose file
exec $cmd
