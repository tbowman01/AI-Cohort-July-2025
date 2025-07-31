# AutoDevHub Development Environment Setup

## 🎯 Overview

This document outlines the complete development environment setup for AutoDevHub, an AI-Powered DevOps Tracker. The environment supports both Python (FastAPI backend) and JavaScript (React frontend) development.

## 📋 Prerequisites

- **Python 3.11+** (Currently detected: 3.12.1)
- **Node.js 18+** (Currently detected: v22.17.0)
- **Git** (for version control)
- **GitHub Codespaces** (recommended) or local development environment

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
# Run the automated setup script
./dev-setup.sh
```

### Option 2: Manual Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Create environment file
cp .env.example .env

# Create directory structure
make setup
```

### Option 3: Using Makefile
```bash
# Complete setup with validation
make setup

# Or individual commands
make install
make validate
```

## 📦 Installed Dependencies

### Python Backend Dependencies
- **FastAPI 0.104.1** - Modern web framework
- **Uvicorn 0.24.0** - ASGI server
- **SQLAlchemy 2.0.23** - Database ORM
- **Pydantic 2.5.0** - Data validation
- **PyTest 7.4.3** - Testing framework
- **Bandit 1.7.5** - Security linter
- **Black 23.11.0** - Code formatter
- **Flake8 6.1.0** - Code linter

### JavaScript Frontend Dependencies
- **React 18.2.0** - UI framework
- **Vite 7.0.6** - Build tool and dev server
- **Vitest 3.2.4** - Testing framework
- **ESLint 8.53.0** - Code linter
- **Axios 1.6.2** - HTTP client
- **React Router 6.18.0** - Routing

## 📁 Project Structure

```
AutoDevHub/
├── backend/                 # FastAPI application
│   ├── app/                # Application code
│   ├── tests/              # Backend tests
│   └── migrations/         # Database migrations
├── frontend/               # React application
│   ├── src/               # Source code
│   ├── public/            # Static assets
│   └── tests/             # Frontend tests
├── docs/                  # Documentation
│   ├── api/              # API documentation
│   ├── architecture/     # System architecture
│   └── deployment/       # Deployment guides
├── .github/              # GitHub workflows
│   └── workflows/        # CI/CD configurations
├── tests/                # Integration tests
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── e2e/             # End-to-end tests
├── presentation/         # Demo materials
├── requirements.txt      # Python dependencies
├── package.json         # Node.js dependencies
├── pyproject.toml       # Python project configuration
├── vite.config.js       # Vite configuration
├── .env.example         # Environment template
├── dev-setup.sh         # Setup script
└── Makefile            # Development commands
```

## 🛠️ Development Commands

### Core Commands
```bash
# Start development servers
make dev                 # Both backend and frontend
uvicorn backend.app.main:app --reload  # Backend only
npm run dev             # Frontend only

# Run tests
make test               # All tests
pytest                  # Python tests only
npm test               # JavaScript tests only

# Code quality
make lint              # All linting
make format            # Format all code
make security          # Security scans
```

### Available Scripts

#### Python Scripts
```bash
# Development
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Testing
pytest -v --cov=backend --cov-report=html
pytest tests/unit/
pytest tests/integration/

# Code Quality
black backend tests/          # Format code
isort backend tests/          # Sort imports
flake8 backend tests/         # Lint code
bandit -r backend/           # Security scan
```

#### JavaScript Scripts
```bash
# Development
npm run dev              # Start dev server (port 5173)
npm run build           # Production build
npm run preview         # Preview production build

# Testing
npm test                # Run tests
npm run test:ui         # Test UI
npm run coverage        # Test coverage

# Code Quality
npm run lint            # ESLint
npm run lint -- --fix  # Auto-fix linting issues
```

## 🔧 Configuration Files

### Environment Configuration (.env)
```bash
# Application Settings
APP_NAME=AutoDevHub
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=sqlite:///./autodevhub.db

# Security
SECRET_KEY=your-secret-key-here

# AI Integration (Optional)
ANTHROPIC_API_KEY=your-key-here

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Development Proxy (Vite)
Frontend requests to `/api` are automatically proxied to the backend server at `http://localhost:8000`.

## 🧪 Testing Strategy

### Backend Testing
- **Unit Tests**: Individual function/class testing
- **Integration Tests**: API endpoint testing
- **Security Tests**: Automated security scanning
- **Coverage**: Minimum 80% test coverage

### Frontend Testing
- **Component Tests**: React component testing
- **Integration Tests**: User interaction testing
- **E2E Tests**: Full application workflow testing

### Test Structure
```
tests/
├── unit/
│   ├── test_backend.py
│   └── test_frontend.js
├── integration/
│   ├── test_api.py
│   └── test_components.js
└── e2e/
    └── test_workflows.js
```

## 🔒 Security Configuration

### Python Security (Bandit)
- Automated security vulnerability scanning
- Configuration in `pyproject.toml`
- Reports generated in `security-report.json`

### JavaScript Security
- NPM audit for dependency vulnerabilities
- ESLint security rules
- CORS configuration for secure API access

## 🚀 Deployment Preparation

### Production Build
```bash
# Build frontend for production
npm run build

# Production Python setup
pip install --no-dev -r requirements.txt

# Environment validation
make validate
```

### Docker Support (Future)
```dockerfile
# Future Dockerfile configuration
FROM python:3.12-slim
# ... (to be implemented)
```

## 📊 Development Workflow

1. **Start Development**
   ```bash
   make dev  # Starts both servers
   ```

2. **Make Changes**
   - Backend: Edit files in `backend/`
   - Frontend: Edit files in `frontend/src/`

3. **Test Changes**
   ```bash
   make test
   ```

4. **Code Quality Check**
   ```bash
   make lint
   make format
   make security
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: your changes"
   ```

## 🐛 Troubleshooting

### Common Issues

#### Python Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

#### Node.js Module Not Found
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Port Already in Use
```bash
# Kill processes on ports 8000 and 5173
lsof -ti:8000 | xargs kill
lsof -ti:5173 | xargs kill
```

#### Permission Denied
```bash
# Make scripts executable
chmod +x dev-setup.sh
```

### Validation Commands
```bash
# Check Python environment
python -c "import fastapi, uvicorn, sqlalchemy; print('✅ Python OK')"

# Check Node.js environment
node -e "console.log('✅ Node.js OK')"

# Full environment validation
make validate
```

## 🤖 Claude AI Integration (CONFIGURED)

### Quick Start
```bash
# Setup Claude GitHub App integration
./.github/setup-claude-integration.sh

# Or manually configure API key
gh secret set ANTHROPIC_API_KEY
```

### Available AI Features
- **Automatic PR Reviews**: AI reviews all new pull requests
- **Interactive Assistance**: Use @claude in comments for help
- **Code Analysis**: Manual dispatch for commit analysis
- **Integration Testing**: Validate AI functionality

### Usage Examples
```markdown
@claude please review this API endpoint for security issues
@claude help optimize this React component
@claude analyze the latest commit for potential bugs
```

**Documentation**: See `.github/CLAUDE_INTEGRATION_GUIDE.md` for complete setup guide.

## 📚 Next Steps

1. **Configure Claude Integration**: Run `.github/setup-claude-integration.sh`
2. **Review Configuration**: Update `.env` file with your settings
3. **Start Development**: Run `make dev` to begin development
4. **Create First API**: Implement user story generation endpoint
5. **Build Frontend**: Create React components for the UI
6. **Add Tests**: Write comprehensive tests for all features
7. **Documentation**: Generate API documentation
8. **Test AI Integration**: Create a PR and test @claude mentions

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Run `make validate` for environment checks
4. Review error logs in the console
5. Check GitHub repository issues for known problems

---

**Status**: ✅ Environment setup completed successfully  
**Last Updated**: 2025-07-31  
**Python**: 3.12.1  
**Node.js**: v22.17.0  
**Ready for Development**: Yes 🚀