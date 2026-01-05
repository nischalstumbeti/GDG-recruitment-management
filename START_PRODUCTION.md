# Quick Start Commands for Production

## Basic Production (HTTP)

```bash
gunicorn --bind 0.0.0.0:8080 --workers 4 --timeout 30 --access-logfile - --error-logfile - app:app
```

## Using Configuration File (Recommended)

```bash
gunicorn -c gunicorn_config.py app:app
```

## Production with HTTPS (Direct SSL - Gunicorn)

```bash
gunicorn --bind 0.0.0.0:443 \
  --workers 4 \
  --timeout 30 \
  --keyfile /path/to/private.key \
  --certfile /path/to/certificate.crt \
  --access-logfile /var/log/gunicorn/access.log \
  --error-logfile /var/log/gunicorn/error.log \
  --log-level info \
  app:app
```

## Production with HTTPS (Recommended: Nginx + Gunicorn)

### Step 1: Start Gunicorn (HTTP on localhost)

```bash
gunicorn --bind 127.0.0.1:8000 \
  --workers 4 \
  --timeout 30 \
  --access-logfile /var/log/gunicorn/access.log \
  --error-logfile /var/log/gunicorn/error.log \
  --log-level info \
  --daemon \
  --pid /var/run/gunicorn.pid \
  app:app
```

### Step 2: Configure Nginx (see nginx.conf.example)

Nginx handles HTTPS and proxies to Gunicorn on port 8000.

## Using Startup Scripts

### Linux/Mac:
```bash
chmod +x start_production.sh
./start_production.sh
```

### Windows:
```cmd
start_production.bat
```

## Environment Variables

Set these before starting:

```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-anon-key"
export FLASK_SECRET_KEY="your-strong-secret-key-here"
export GUNICORN_WORKERS=4
```

## Systemd Service (Linux)

See `PRODUCTION_DEPLOYMENT.md` for complete systemd service configuration.

