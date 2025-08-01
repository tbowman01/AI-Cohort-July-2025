---
layout: default
title: Setup Guide
parent: Development
nav_order: 1
---

# Development Setup Guide
{: .fs-9 }

Complete environment setup for AutoDevHub development
{: .fs-6 .fw-300 }

---

## Prerequisites

### Required Software
- **Python 3.12+**: Backend development
- **Node.js 18+**: Frontend development and build tools
- **Git**: Version control
- **Docker** (optional): Containerized development

### Recommended Tools
- **VS Code**: Primary IDE with extensions
- **Postman**: API testing
- **SQLite Browser**: Database inspection

---

## Quick Start

### 1. Repository Setup

```bash
# Clone the repository
git clone https://github.com/ai-cohort-july-2025/AI-Cohort-July-2025.git
cd AI-Cohort-July-2025

# Create development branch
git checkout -b feature/your-feature-name
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (new terminal)
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local
```

### 4. Environment Configuration

#### Backend Environment (.env)
```bash
# AI Configuration
CLAUDE_API_KEY=your_claude_api_key_here

# Database
DATABASE_URL=sqlite:///./autodevhub.db

# Cache
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=true

# API Configuration
API_V1_STR=/api/v1
CORS_ORIGINS=["http://localhost:3002", "http://127.0.0.1:3002"]
```

#### Frontend Environment (.env.local)
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_VERSION=v1

# Environment
VITE_ENVIRONMENT=development
VITE_DEBUG=true
```

---

## Development Servers

### Backend Server

```bash
# From backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Server will be available at:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Redoc: http://localhost:8000/redoc
```

### Frontend Server

```bash
# From frontend directory
cd frontend

# Run development server
npm run dev

# Server will be available at:
# - App: http://localhost:3002
```

---

## Docker Development

### Full Stack with Docker Compose

```bash
# From project root
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild services
docker-compose up -d --build
```

### Individual Services

```bash
# Backend only
docker-compose up -d backend

# Frontend only
docker-compose up -d frontend

# Database only
docker-compose up -d db
```

---

## Database Setup

### SQLite Database

```bash
# From backend directory
cd backend

# Initialize database
python init_db.py

# Run migrations (if any)
alembic upgrade head
```

### Redis Cache (Optional)

```bash
# Install Redis locally
# macOS:
brew install redis
brew services start redis

# Ubuntu:
sudo apt-get install redis-server
sudo systemctl start redis-server

# Or use Docker:
docker run -d -p 6379:6379 redis:alpine
```

---

## IDE Configuration

### VS Code Extensions

Install these recommended extensions:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.pylint",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-vscode.vscode-typescript-next",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense",
    "ms-vscode.vscode-json"
  ]
}
```

### VS Code Settings

```json
{
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "typescript.preferences.quoteStyle": "single",
  "javascript.preferences.quoteStyle": "single"
}
```

---

## Testing Setup

### Backend Testing

```bash
# From backend directory
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_story_generator.py

# Run with verbose output
pytest -v
```

### Frontend Testing

```bash
# From frontend directory
cd frontend

# Run unit tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

---

## Quality Checks

### Backend Code Quality

```bash
# From backend directory
cd backend

# Format code
black .

# Sort imports
isort .

# Lint code
pylint **/*.py

# Type checking
mypy .

# Security check
bandit -r .
```

### Frontend Code Quality

```bash
# From frontend directory
cd frontend

# Lint JavaScript/TypeScript
npm run lint

# Fix lint issues
npm run lint:fix

# Format code
npm run format

# Type checking
npm run type-check
```

---

## Troubleshooting

### Common Issues

#### Backend Issues

**ImportError: No module named 'uvicorn'**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Database connection errors**
```bash
# Check database file permissions
ls -la autodevhub.db

# Reinitialize database
rm autodevhub.db
python init_db.py
```

**Claude API errors**
```bash
# Verify API key in .env file
echo $CLAUDE_API_KEY

# Test API connection
python -c "import anthropic; client = anthropic.Anthropic(api_key='your_key'); print('Connected')"
```

#### Frontend Issues

**Module not found errors**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**CORS errors**
```bash
# Check backend CORS configuration in .env
# Ensure frontend URL is in CORS_ORIGINS
```

**Build errors**
```bash
# Clear Vite cache
npm run build:clean
npm run build
```

### Debug Mode

#### Backend Debug
```bash
# Enable debug logging
export DEBUG=true
uvicorn main:app --reload --log-level debug
```

#### Frontend Debug
```bash
# Enable debug mode
echo "VITE_DEBUG=true" >> .env.local
npm run dev
```

---

## Performance Optimization

### Backend Performance
- Use async/await for I/O operations
- Implement database connection pooling
- Cache frequently accessed data
- Profile slow endpoints

### Frontend Performance
- Enable React StrictMode
- Use React.memo for expensive components
- Implement code splitting
- Optimize bundle size

---

*For deployment procedures, see [Deployment Guide]({% link development/deployment.md %}). For contribution guidelines, see [Contributing Guidelines]({% link development/contributing.md %}).*