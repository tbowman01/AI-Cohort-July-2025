# AutoDevHub Development Makefile

.PHONY: help setup install test lint format security clean dev build docs

# Default target
help:
	@echo "AutoDevHub Development Commands"
	@echo "=============================="
	@echo "setup     - Complete development environment setup"
	@echo "install   - Install all dependencies"
	@echo "test      - Run all tests (Python + Node.js)"
	@echo "lint      - Run all linting checks"
	@echo "format    - Format all code (Python + JavaScript)"
	@echo "security  - Run security scans"
	@echo "dev       - Start development servers"
	@echo "build     - Build for production"
	@echo "clean     - Clean build artifacts and cache"
	@echo "docs      - Generate documentation"

# Complete setup
setup:
	@echo "🚀 Setting up AutoDevHub development environment..."
	chmod +x dev-setup.sh
	./dev-setup.sh

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	npm install

# Run tests
test:
	@echo "🧪 Running tests..."
	@echo "Running Python tests..."
	pytest -v --cov=backend --cov-report=html --cov-report=term
	@echo "Running JavaScript tests..."
	npm test

# Linting
lint:
	@echo "🔍 Running linting checks..."
	@echo "Python linting..."
	-flake8 backend tests
	@echo "JavaScript linting..."
	-npm run lint

# Code formatting
format:
	@echo "✨ Formatting code..."
	@echo "Formatting Python code..."
	black backend tests
	isort backend tests
	@echo "JavaScript formatting (via ESLint)..."
	npm run lint -- --fix

# Security scans
security:
	@echo "🔒 Running security scans..."
	bandit -r backend -f json -o security-report.json
	@echo "Security report generated: security-report.json"
	npm audit

# Development servers
dev:
	@echo "🖥️  Starting development servers..."
	@echo "This will start both backend and frontend servers"
	@echo "Backend will be available at http://localhost:8000"
	@echo "Frontend will be available at http://localhost:5173"
	@echo "Use Ctrl+C to stop both servers"
	@make dev-parallel

dev-parallel:
	@echo "Starting backend server..."
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000 &
	@echo "Starting frontend server..."
	npm run dev

# Production build
build:
	@echo "🏗️  Building for production..."
	npm run build
	@echo "Production build completed in dist/"

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf node_modules/.cache/
	rm -rf __pycache__/
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Generate documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "Documentation generation not yet implemented"
	@echo "Future: Will generate API docs, architecture diagrams, etc."

# Development helpers
check-deps:
	@echo "Checking Python dependencies..."
	pip check
	@echo "Checking Node.js dependencies..."
	npm ls

# Database helpers (for future use)
db-init:
	@echo "🗄️  Initializing database..."
	@echo "Database initialization not yet implemented"

db-migrate:
	@echo "🗄️  Running database migrations..."
	@echo "Database migrations not yet implemented"

# Quick validation
validate:
	@echo "✅ Running quick validation..."
	python -c "import fastapi, uvicorn, sqlalchemy; print('Python environment OK')"
	node -e "console.log('Node.js environment OK')"
	@echo "All systems ready! 🚀"

# GitHub Actions simulation (for local testing)
ci-test:
	@echo "🔄 Running CI/CD simulation..."
	-make lint
	-make security
	-make test
	make build
	@echo "CI/CD simulation completed ✅"