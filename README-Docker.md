# Docker Configuration for AutoDevHub

This document provides comprehensive information about the Docker setup for AutoDevHub, including containerization strategy, deployment options, and operational procedures.

## 🏗️ Architecture Overview

AutoDevHub uses a microservices architecture with the following containerized components:

### Services
- **Backend**: Python FastAPI application with async SQLAlchemy
- **Frontend**: React with Vite, served via nginx
- **Database**: PostgreSQL 15 with persistent storage
- **Cache**: Redis (optional, for session/cache management)
- **Load Balancer**: Nginx (optional, for production)

### Container Types
1. **Individual Services**: Separate containers for backend and frontend
2. **Full-Stack**: Single container with both backend and frontend
3. **Production**: Complete setup with load balancer and caching

## 📁 File Structure

```
/workspaces/AI-Cohort-July-2025/
├── backend/
│   ├── Dockerfile                    # Python FastAPI container
│   └── .dockerignore                # Backend-specific ignore rules
├── frontend/
│   ├── Dockerfile                   # Node.js build + nginx serve
│   └── .dockerignore               # Frontend-specific ignore rules
├── Dockerfile                      # Full-stack single container
├── docker-compose.yml             # Multi-service orchestration
├── .dockerignore                   # Root-level ignore rules
├── .env.example                    # Environment configuration template
├── docker-start.sh                # Startup script with profiles
├── docker-stop.sh                 # Shutdown script with cleanup
└── README-Docker.md               # This documentation
```

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 2. Start Services
```bash
# Development environment (recommended for development)
./docker-start.sh --profile dev

# Production environment
./docker-start.sh --profile prod

# Full-stack single container
./docker-start.sh --profile fullstack

# With caching (Redis)
./docker-start.sh --profile cache
```

### 3. Access Services
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: postgresql://localhost:5432/autodevhub

## 🐳 Container Details

### Backend Container (`backend/Dockerfile`)
- **Base Image**: python:3.11-slim
- **Multi-stage Build**: Optimized for production
- **Features**:
  - Virtual environment isolation
  - Non-root user execution
  - Health checks
  - Proper dependency caching
  - SQLite support for development
  - PostgreSQL support for production

### Frontend Container (`frontend/Dockerfile`)
- **Base Image**: node:18-alpine (build) + nginx:alpine (serve)
- **Multi-stage Build**: Build assets then serve with nginx
- **Features**:
  - Optimized nginx configuration
  - Client-side routing support
  - API proxy to backend
  - Static asset caching
  - Security headers
  - Gzip compression

### Full-Stack Container (`Dockerfile`)
- **Base Image**: python:3.11-slim + nginx
- **Supervisor**: Manages both backend and nginx processes
- **Features**:
  - Single container deployment
  - Shared networking
  - Combined health checks
  - Simplified orchestration

## 🔧 Configuration Options

### Environment Variables

#### Application Settings
```env
ENVIRONMENT=development          # development, staging, production
DEBUG=true                      # Enable debug mode
NODE_ENV=development            # Node.js environment
```

#### Database Configuration
```env
POSTGRES_DB=autodevhub          # Database name
POSTGRES_USER=autodevhub_user   # Database user
POSTGRES_PASSWORD=secret        # Database password
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
```

#### Service Ports
```env
BACKEND_PORT=8000               # Backend service port
FRONTEND_PORT=3000              # Frontend service port
FULLSTACK_PORT=80               # Full-stack service port
```

#### AI Integration
```env
AI_API_KEY=your-api-key         # OpenAI/AI service API key
AI_MODEL=gpt-3.5-turbo         # AI model to use
```

### Docker Compose Profiles

#### Development Profile (default)
```bash
docker-compose up -d database backend frontend
```
- Separate containers for each service
- Development-optimized configurations
- File watching for hot reload

#### Production Profile
```bash
docker-compose --profile production up -d
```
- Includes nginx load balancer
- Production-optimized settings
- SSL termination support
- Health monitoring

#### Full-Stack Profile
```bash
docker-compose --profile fullstack up -d database fullstack
```
- Single container for backend + frontend
- Simplified deployment
- Reduced resource usage

#### Cache Profile
```bash
docker-compose --profile cache up -d
```
- Includes Redis for caching
- Session management
- Performance optimization

## 🛠️ Operational Commands

### Starting Services
```bash
# Basic start
./docker-start.sh

# With specific profile
./docker-start.sh --profile prod

# Rebuild containers
./docker-start.sh --rebuild

# Start and follow logs
./docker-start.sh --logs
```

### Stopping Services
```bash
# Stop containers only
./docker-stop.sh

# Stop and remove volumes (⚠️ deletes data)
./docker-stop.sh --volumes

# Full cleanup
./docker-stop.sh --cleanup
```

### Management Commands
```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Check service status
docker-compose ps

# Execute commands in containers
docker-compose exec backend bash
docker-compose exec frontend sh

# View resource usage
docker stats
```

## 🔍 Health Monitoring

### Health Check Endpoints
- **Backend**: `GET /health`
- **Frontend**: `GET /health`
- **Full-Stack**: `GET /health`

### Container Health Checks
All containers include built-in health checks that monitor:
- Service availability
- Database connectivity
- API responsiveness
- File system health

### Monitoring Commands
```bash
# Check container health
docker-compose ps

# View detailed health status
docker inspect $(docker-compose ps -q backend) | jq '.[0].State.Health'

# Monitor resource usage
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
```

## 🚀 Deployment Strategies

### Development Deployment
```bash
# Start development environment
./docker-start.sh --profile dev

# Benefits:
# - Hot reload for development
# - Separate service debugging
# - Easy log isolation
```

### Staging Deployment
```bash
# Start with production profile but development data
ENVIRONMENT=staging ./docker-start.sh --profile prod

# Benefits:
# - Production-like environment
# - Full feature testing
# - Performance validation
```

### Production Deployment
```bash
# Start production environment
ENVIRONMENT=production ./docker-start.sh --profile prod

# Benefits:
# - Load balancing with nginx
# - SSL termination
# - Caching with Redis
# - Full monitoring
```

### Single Container Deployment
```bash
# Start full-stack container
./docker-start.sh --profile fullstack

# Benefits:
# - Simplified orchestration
# - Reduced resource overhead
# - Easy horizontal scaling
```

## 🔒 Security Considerations

### Container Security
- Non-root user execution
- Minimal base images
- Security header configuration
- Environment variable isolation

### Network Security
- Custom Docker network isolation
- Internal service communication
- Exposed ports minimization
- Proxy-based external access

### Data Security
- Volume encryption support
- Secret management via environment
- Database connection encryption
- SSL/TLS termination

## 📊 Performance Optimization

### Multi-stage Builds
- Separate build and runtime environments
- Reduced image sizes
- Dependency caching optimization
- Layer reuse maximization

### Resource Management
- Memory limits configuration
- CPU allocation controls
- Disk I/O optimization
- Network bandwidth management

### Caching Strategies
- Docker layer caching
- Application-level caching with Redis
- Static asset caching with nginx
- Database query optimization

## 🐛 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check port usage
netstat -tlnp | grep :8000

# Modify ports in .env
BACKEND_PORT=8001
FRONTEND_PORT=3001
```

#### Permission Issues
```bash
# Fix volume permissions
sudo chown -R $USER:$USER ./data
```

#### Memory Issues
```bash
# Check container resource usage
docker stats

# Increase Docker memory limit in Docker Desktop
```

#### Database Connection Issues
```bash
# Check database container status
docker-compose logs database

# Verify connection string
docker-compose exec backend python -c "from database import engine; print('Connection OK')"
```

### Debugging Commands
```bash
# Enter container shell
docker-compose exec backend bash
docker-compose exec frontend sh

# Check container logs
docker-compose logs --tail 100 backend

# Inspect container configuration
docker inspect autodevhub-backend

# Check network connectivity
docker-compose exec backend ping database
```

## 📈 Scaling and Load Balancing

### Horizontal Scaling
```bash
# Scale backend instances
docker-compose up -d --scale backend=3

# Scale with load balancer
docker-compose --profile production up -d --scale backend=3
```

### Load Balancing Configuration
The nginx service provides:
- Round-robin load balancing
- Health check routing
- SSL termination
- Static asset serving

### Database Scaling
For production scaling:
- PostgreSQL read replicas
- Connection pooling
- Database clustering
- Backup strategies

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: Docker Build and Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and test
        run: |
          cp .env.example .env
          ./docker-start.sh --profile dev
          # Run tests
          docker-compose exec -T backend pytest
      - name: Deploy
        run: |
          ./docker-start.sh --profile prod
```

### Registry Push
```bash
# Tag images
docker tag autodevhub-backend registry.com/autodevhub/backend:latest
docker tag autodevhub-frontend registry.com/autodevhub/frontend:latest

# Push to registry
docker push registry.com/autodevhub/backend:latest
docker push registry.com/autodevhub/frontend:latest
```

## 📝 Best Practices

### Development
- Use development profile for local development
- Mount source code volumes for hot reload
- Use separate databases for testing
- Regular container cleanup

### Production
- Use production profile with monitoring
- Implement proper secret management
- Configure backup strategies
- Monitor resource usage
- Use health checks for orchestration

### Maintenance
- Regular image updates
- Security patch application
- Log rotation configuration
- Performance monitoring
- Capacity planning

## 🔗 Related Documentation

- [Backend API Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)
- [Database Schema](docs/database-schema.md)
- [Deployment Guide](docs/deployment.md)
- [Monitoring Guide](docs/monitoring.md)

For additional help, refer to the main project documentation or create an issue in the project repository.