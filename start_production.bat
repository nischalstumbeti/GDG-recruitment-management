@echo off
REM Production startup script for GDG Recruitment System (Windows)
REM Make sure to set environment variables before running

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist env\Scripts\activate.bat (
    call env\Scripts\activate.bat
)

REM Initialize default user
python -c "from app import init_default_user; init_default_user()"

REM Start Gunicorn
REM Option 1: Using config file (recommended)
gunicorn -c gunicorn_config.py app:app

REM Option 2: Direct command (uncomment to use)
REM gunicorn --bind 0.0.0.0:8080 --workers 4 --timeout 30 --access-logfile - --error-logfile - app:app

REM Option 3: With SSL certificates (uncomment and configure paths)
REM gunicorn --bind 0.0.0.0:443 --workers 4 --timeout 30 --keyfile C:\path\to\private.key --certfile C:\path\to\certificate.crt --access-logfile - --error-logfile - app:app

