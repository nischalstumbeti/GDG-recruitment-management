"""
Gunicorn configuration file for production deployment
"""
import multiprocessing
import os

# Server socket
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8080')
backlog = 2048

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = os.getenv('GUNICORN_ACCESS_LOG', '-')  # '-' means stdout
errorlog = os.getenv('GUNICORN_ERROR_LOG', '-')   # '-' means stdout
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'gdg_recruitment_system'

# Server mechanics
daemon = False
pidfile = os.getenv('GUNICORN_PIDFILE', None)
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL Configuration (if using direct SSL)
# Uncomment and configure if using Gunicorn with SSL directly
# keyfile = '/path/to/your/private.key'
# certfile = '/path/to/your/certificate.crt'

# Preload app for better performance
preload_app = True

# Graceful timeout
graceful_timeout = 30

# Max requests per worker (helps prevent memory leaks)
max_requests = 1000
max_requests_jitter = 50

# Enable stats
statsd_host = None
statsd_prefix = 'gunicorn'

def when_ready(server):
    """Called just after the server is started"""
    server.log.info("Server is ready. Spawning workers")

def on_exit(server):
    """Called just before exiting"""
    server.log.info("Shutting down: Master")

def worker_int(worker):
    """Called when a worker receives INT or QUIT signal"""
    worker.log.info("worker received INT or QUIT signal")

def pre_fork(server, worker):
    """Called just before a worker is forked"""
    pass

def post_fork(server, worker):
    """Called just after a worker has been forked"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    """Called just after a worker has initialized the application"""
    # Initialize default user on startup
    from app import init_default_user
    init_default_user()

