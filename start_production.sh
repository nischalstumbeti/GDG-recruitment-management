#!/bin/bash
# Production startup script for GDG Recruitment System
# Make sure to set environment variables before running

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "env" ]; then
    source env/bin/activate
fi

# Load environment variables from .env if it exists
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Initialize default user
python -c "from app import init_default_user; init_default_user()"

# Start Gunicorn
# Option 1: Using config file (recommended)
gunicorn -c gunicorn_config.py app:app

# Option 2: Direct command (uncomment to use)
# gunicorn --bind 0.0.0.0:8080 --workers 4 --timeout 30 --access-logfile - --error-logfile - app:app

# Option 3: With SSL certificates (uncomment and configure paths)
# gunicorn --bind 0.0.0.0:443 --workers 4 --timeout 30 \
#   --keyfile /path/to/private.key \
#   --certfile /path/to/certificate.crt \
#   --access-logfile - --error-logfile - app:app

