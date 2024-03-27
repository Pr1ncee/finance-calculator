#!/bin/bash

set -euf

echo "Applying migrations..."
python /app/finance_calculator/manage.py migrate
echo "All migrations applied!"

echo "Starting the server..."
python /app/finance_calculator/manage.py runserver 0.0.0.0:8000
