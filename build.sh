#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, ets.)
pip install -r requirements.txt

# Convert static assert files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
