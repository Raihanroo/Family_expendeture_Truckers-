#!/bin/bash
# Build script for Vercel

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# API Documentation HTML কে staticfiles এ copy করো
cp API_Documentation.html staticfiles/API_Documentation.html