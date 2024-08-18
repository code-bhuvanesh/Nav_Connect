#!/bin/bash

DRY_RUN=$1

echo "Pulling latest code from repository..."
# Skip actual git pull in dry run
[ "$DRY_RUN" != "true" ] && git pull origin main

echo "Installing dependencies..."
# Skip actual installation in dry run
[ "$DRY_RUN" != "true" ] && pip install -r requirements.txt

echo "Running migrations..."
# Skip actual migrations in dry run
[ "$DRY_RUN" != "true" ] && python manage.py migrate

echo "Restarting the server..."
# Skip actual restart in dry run
[ "$DRY_RUN" != "true" ] && sudo systemctl restart myapp

echo "Deployment complete."