# Full-Stack Application Dockerfile
# Multi-stage build combining backend and frontend

# Backend build stage
FROM python:3.11-slim as backend-builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# Frontend build stage
FROM node:18-alpine as frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ .
RUN npm run build

# Production stage
FROM python:3.11-slim as production

# Install nginx and runtime dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    sqlite3 \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy Python virtual environment
COPY --from=backend-builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy backend application
WORKDIR /app/backend
COPY backend/ .

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist /var/www/html

# Create nginx configuration
RUN cat > /etc/nginx/sites-enabled/default << 'EOF'
server {
    listen 80;
    server_name localhost;
    root /var/www/html;
    index index.html;

    # Frontend routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check for full stack
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
    }

    # Static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}
EOF

# Create supervisor configuration
RUN cat > /etc/supervisor/conf.d/app.conf << 'EOF'
[supervisord]
nodaemon=true
user=root

[program:backend]
command=/opt/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
directory=/app/backend
autostart=true
autorestart=true
stderr_logfile=/var/log/backend.err.log
stdout_logfile=/var/log/backend.out.log

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autostart=true
autorestart=true
stderr_logfile=/var/log/nginx.err.log
stdout_logfile=/var/log/nginx.out.log
EOF

# Create app user and set permissions
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    mkdir -p /app/data /app/logs && \
    chown -R appuser:appuser /app && \
    chown -R www-data:www-data /var/www/html

# Health check for full stack
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Expose port
EXPOSE 80

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/app.conf"]