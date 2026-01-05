# Production Deployment Guide

This guide covers deploying the GDG Recruitment System in production using Gunicorn with HTTPS.

## Prerequisites

1. Python 3.8+ installed
2. All dependencies installed: `pip install -r requirements.txt`
3. Supabase configured and database schema created
4. SSL certificates (for HTTPS)

## Quick Start Commands

### Basic Production (HTTP)

```bash
gunicorn --bind 0.0.0.0:8080 --workers 4 --timeout 30 --access-logfile - --error-logfile - app:app
```

### Using Configuration File (Recommended)

```bash
gunicorn -c gunicorn_config.py app:app
```

### Production with HTTPS (Direct SSL)

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

### Production with HTTPS (Recommended: Nginx Reverse Proxy)

**Step 1: Start Gunicorn (HTTP on localhost)**
```bash
gunicorn --bind 127.0.0.1:8000 \
  --workers 4 \
  --timeout 30 \
  --access-logfile /var/log/gunicorn/access.log \
  --error-logfile /var/log/gunicorn/error.log \
  --log-level info \
  app:app
```

**Step 2: Configure Nginx** (see nginx configuration below)

## Gunicorn Configuration Options

### Environment Variables

You can customize Gunicorn using environment variables:

```bash
export GUNICORN_BIND="0.0.0.0:8080"
export GUNICORN_WORKERS=4
export GUNICORN_LOG_LEVEL="info"
export GUNICORN_ACCESS_LOG="/var/log/gunicorn/access.log"
export GUNICORN_ERROR_LOG="/var/log/gunicorn/error.log"
export GUNICORN_PIDFILE="/var/run/gunicorn.pid"

gunicorn -c gunicorn_config.py app:app
```

### Worker Count

Recommended formula: `(2 × CPU cores) + 1`

- 1 CPU core: 3 workers
- 2 CPU cores: 5 workers
- 4 CPU cores: 9 workers
- 8 CPU cores: 17 workers

## Nginx Configuration (Recommended for Production)

### 1. Install Nginx

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install nginx
```

**CentOS/RHEL:**
```bash
sudo yum install nginx
```

### 2. Create Nginx Configuration

Create `/etc/nginx/sites-available/gdg_recruitment`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration
    ssl_certificate /path/to/your/fullchain.pem;
    ssl_certificate_key /path/to/your/privkey.pem;
    
    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Client body size (for file uploads)
    client_max_body_size 16M;

    # Static files
    location /static {
        alias /path/to/your/project/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### 3. Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/gdg_recruitment /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl reload nginx
```

## Systemd Service (Linux)

Create `/etc/systemd/system/gdg-recruitment.service`:

```ini
[Unit]
Description=GDG Recruitment System Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/venv/bin"
Environment="SUPABASE_URL=your_supabase_url"
Environment="SUPABASE_KEY=your_supabase_key"
ExecStart=/path/to/your/venv/bin/gunicorn -c gunicorn_config.py app:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable gdg-recruitment
sudo systemctl start gdg-recruitment
sudo systemctl status gdg-recruitment
```

## SSL Certificates

### Option 1: Let's Encrypt (Free)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Option 2: Commercial SSL Certificate

1. Purchase SSL certificate from a provider
2. Install certificate files
3. Update Nginx configuration with certificate paths

## Security Checklist

- [ ] Change `app.secret_key` in `app.py` to a strong random key
- [ ] Set `debug=False` in production
- [ ] Use environment variables for sensitive data
- [ ] Configure firewall (allow only 80, 443)
- [ ] Set up SSL/TLS certificates
- [ ] Configure proper file permissions
- [ ] Set up log rotation
- [ ] Enable automatic security updates
- [ ] Configure backup strategy

## Environment Variables

Create a `.env` file or set system environment variables:

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# Gunicorn (optional)
GUNICORN_BIND=0.0.0.0:8080
GUNICORN_WORKERS=4
GUNICORN_LOG_LEVEL=info
```

## Monitoring and Logs

### View Gunicorn Logs

```bash
# If using systemd
sudo journalctl -u gdg-recruitment -f

# If using log files
tail -f /var/log/gunicorn/access.log
tail -f /var/log/gunicorn/error.log
```

### Check Application Status

```bash
# Check if Gunicorn is running
ps aux | grep gunicorn

# Check port
netstat -tulpn | grep :8080
```

## Troubleshooting

### Application not starting
- Check Supabase credentials are set
- Verify database schema is created
- Check Gunicorn logs for errors

### 502 Bad Gateway (Nginx)
- Verify Gunicorn is running: `ps aux | grep gunicorn`
- Check Gunicorn is listening on correct port
- Review Nginx error logs: `sudo tail -f /var/log/nginx/error.log`

### SSL Certificate Issues
- Verify certificate paths are correct
- Check certificate expiration: `openssl x509 -in certificate.crt -noout -dates`
- Ensure private key permissions: `chmod 600 private.key`

## Performance Tuning

1. **Adjust workers** based on CPU cores
2. **Enable gzip** in Nginx for static files
3. **Use CDN** for static assets
4. **Enable caching** for static files
5. **Database connection pooling** (handled by Supabase)

## Backup Strategy

- Regular database backups (Supabase handles this)
- Backup uploaded files from `uploads/` directory
- Backup configuration files

