# AutoDevHub Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL (for production)

### Local Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Production Deployment

#### 1. Build Frontend
```bash
cd frontend
npm run build
# Output in dist/ directory
```

#### 2. Environment Configuration

Create `.env` files:

**Backend `.env`:**
```env
DATABASE_URL=postgresql://user:pass@localhost/autodevhub
ANTHROPIC_API_KEY=your-api-key
ENVIRONMENT=production
```

**Frontend `.env.production`:**
```env
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_API_ENDPOINT=/api/v1/stories/generate-story
```

#### 3. Docker Deployment (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up -d
```

#### 4. Manual Deployment

**Backend:**
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
- Serve `dist/` directory with nginx/apache
- Configure reverse proxy for API

### Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Frontend built for production
- [ ] SSL certificates configured
- [ ] Reverse proxy setup
- [ ] Health checks configured
- [ ] Monitoring enabled
- [ ] Backup strategy implemented

### Monitoring Endpoints

- Health Check: `GET /health`
- API Docs: `GET /docs`
- Metrics: `GET /metrics` (if enabled)

### Troubleshooting

1. **CORS Issues**: Ensure backend allows frontend origin
2. **API Connection**: Verify VITE_API_BASE_URL is correct
3. **Database**: Check DATABASE_URL and migrations
4. **Performance**: Enable caching and CDN for static assets