---
layout: default
title: Deployment Guide
parent: Development
nav_order: 2
---

# Deployment Guide
{: .fs-9 }

Production deployment procedures and best practices
{: .fs-6 .fw-300 }

---

## Deployment Overview

AutoDevHub supports multiple deployment strategies, from simple cloud hosting to enterprise Kubernetes deployments.

## Quick Deploy Options

### 1. Docker Compose (Recommended)
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

### 2. Cloud Platform Deployment
- **Heroku**: One-click deployment
- **Railway**: Git-based deployment
- **DigitalOcean App Platform**: Container deployment
- **AWS ECS**: Enterprise container orchestration

---

## Environment Preparation

### Production Environment Variables

#### Backend (.env.prod)
```bash
# AI Configuration
CLAUDE_API_KEY=prod_claude_api_key

# Database
DATABASE_URL=postgresql://user:pass@host:5432/autodevhub
# or SQLite for simple deployment:
# DATABASE_URL=sqlite:///./data/autodevhub.db

# Cache
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=secure_random_key_256_bits
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=production
DEBUG=false

# API Configuration
API_V1_STR=/api/v1
CORS_ORIGINS=["https://yourdomain.com"]

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
LOG_LEVEL=INFO
```

#### Frontend (.env.production)
```bash
# API Configuration
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_API_VERSION=v1

# Environment
VITE_ENVIRONMENT=production
VITE_DEBUG=false

# Analytics (optional)
VITE_GA_TRACKING_ID=GA_TRACKING_ID
```

---

## Docker Deployment

### Production Docker Configuration

#### docker-compose.prod.yml
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - DATABASE_URL=sqlite:///./data/autodevhub.db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./data:/app/data
    ports:
      - "8000:8000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
      - "443:443"
    restart: unless-stopped
    depends_on:
      - backend

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  redis_data:
  ssl_certs:
```

### Production Dockerfiles

#### Backend Dockerfile.prod
```dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile.prod
```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80 443

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

---

## Cloud Platform Deployments

### Heroku Deployment

#### 1. Heroku Setup
```bash
# Install Heroku CLI
npm install -g heroku

# Login to Heroku
heroku login

# Create Heroku app
heroku create autodevhub-prod

# Set environment variables
heroku config:set CLAUDE_API_KEY=your_api_key
heroku config:set SECRET_KEY=your_secret_key
heroku config:set ENVIRONMENT=production

# Deploy
git push heroku main
```

#### 2. Heroku Configuration Files

**Procfile**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**runtime.txt**
```
python-3.12.0
```

### Railway Deployment

#### railway.json
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "numReplicas": 1,
    "sleepApplication": false,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### DigitalOcean App Platform

#### .do/app.yaml
```yaml
name: autodevhub
services:
- name: backend
  source_dir: /backend
  dockerfile_path: Dockerfile
  http_port: 8000
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: CLAUDE_API_KEY
    scope: RUN_TIME
    type: SECRET
  - key: ENVIRONMENT
    value: production
    
- name: frontend
  source_dir: /frontend
  dockerfile_path: Dockerfile
  http_port: 80
  instance_count: 1
  instance_size_slug: basic-xxs
```

---

## Database Deployment

### SQLite Production Setup
```bash
# Create data directory
mkdir -p /app/data

# Set proper permissions
chown -R appuser:appuser /app/data
chmod 755 /app/data

# Initialize production database
cd /app
python init_db.py
```

### PostgreSQL Setup (Scalable)
```bash
# Docker PostgreSQL
docker run -d \
  --name autodevhub-db \
  -e POSTGRES_DB=autodevhub \
  -e POSTGRES_USER=autodevhub \
  -e POSTGRES_PASSWORD=secure_password \
  -v postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15

# Run migrations
DATABASE_URL=postgresql://autodevhub:secure_password@localhost/autodevhub \
python init_db.py
```

---

## SSL/TLS Configuration

### Let's Encrypt with Certbot
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Nginx SSL Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Frontend
    location / {
        proxy_pass http://frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # API
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Monitoring & Logging

### Application Monitoring
```python
# backend/monitoring.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)
```

### Health Checks
```python
# backend/health.py
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }
```

### Log Configuration
```python
# backend/logging_config.py
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/app/logs/app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
```

---

## Performance Optimization

### Backend Optimizations
```python
# Gunicorn configuration
# gunicorn_config.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
keepalive = 5
```

### Frontend Optimizations
```javascript
// vite.config.js production optimizations
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          utils: ['axios', 'date-fns']
        }
      }
    },
    chunkSizeWarningLimit: 1000,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  }
})
```

---

## Backup and Recovery

### Database Backup
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/app/backups"

# SQLite backup
cp /app/data/autodevhub.db "$BACKUP_DIR/autodevhub_$DATE.db"

# Compress backup
gzip "$BACKUP_DIR/autodevhub_$DATE.db"

# Clean old backups (keep 30 days)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
```

### Automated Backups
```bash
# Add to crontab
0 2 * * * /app/scripts/backup.sh
```

---

## Security Checklist

### Pre-Deployment Security
- [ ] Environment variables secured
- [ ] API keys rotated for production
- [ ] HTTPS/SSL certificates configured
- [ ] Database credentials secured
- [ ] CORS origins restricted
- [ ] Rate limiting implemented
- [ ] Input validation enabled
- [ ] Security headers configured

### Post-Deployment Security
- [ ] Security monitoring enabled
- [ ] Log analysis configured
- [ ] Vulnerability scanning scheduled
- [ ] Backup verification tested
- [ ] Incident response plan documented

---

## Troubleshooting Production Issues

### Common Production Issues

#### High Memory Usage
```bash
# Monitor memory usage
docker stats

# Check application logs
docker logs autodevhub-backend

# Restart services if needed
docker-compose restart backend
```

#### Database Connection Issues
```bash
# Check database connectivity
docker exec -it autodevhub-db psql -U username -d database

# Check connection pool
# Review backend logs for connection errors
```

#### SSL Certificate Issues
```bash
# Check certificate expiry
ssl-check yourdomain.com

# Renew certificate
sudo certbot renew

# Restart nginx
sudo systemctl restart nginx
```

---

*For development setup, see [Setup Guide](/docs/development/setup-guide.md). For contribution guidelines, see [Contributing Guidelines](/docs/development/contributing.md).*