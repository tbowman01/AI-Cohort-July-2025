# AutoDevHub Development Makefile

.PHONY: help setup install test lint format security clean dev build docs docs-serve docs-serve-local docs-clean docs-setup docs-install docs-check docker-up docker-down docker-build docker-rebuild docker-logs docker-status docker-clean docker-dev docker-prod docker-shell docker-exec docker-check

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
	@echo "docs      - Generate documentation (Jekyll build)"
	@echo "docs-setup - Setup documentation environment (Ruby + Jekyll)"
	@echo "docs-install - Install documentation dependencies (bundle install)"
	@echo "docs-serve - Serve documentation locally (with GitHub Pages baseurl)"
	@echo "docs-serve-local - Serve documentation locally at http://localhost:4000"
	@echo "docs-clean - Clean documentation build artifacts"
	@echo "docs-check - Check documentation links and validate build"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "docker-up    - Start Docker containers (frontend:3000, backend:5000)"
	@echo "docker-down  - Stop and remove Docker containers"
	@echo "docker-build - Build Docker images"
	@echo "docker-rebuild - Rebuild Docker images from scratch"
	@echo "docker-logs  - View container logs"
	@echo "docker-status - Show container status and health"
	@echo "docker-clean - Clean up Docker images, containers, and volumes"
	@echo "docker-dev   - Start containers in development mode"
	@echo "docker-prod  - Start containers in production mode"
	@echo "docker-shell - Open shell in running backend container"
	@echo "docker-exec  - Execute command in running container"
	@echo "docker-check - Check Docker environment and prerequisites"

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
	rm -rf _site/
	rm -rf .jekyll-cache/
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Setup documentation environment
docs-setup:
	@echo "🛠️  Setting up documentation environment..."
	@echo "Checking Ruby installation..."
	@ruby --version || (echo "❌ Ruby not found. Please install Ruby 3.2+ first." && exit 1)
	@echo "Checking Bundler installation..."
	@if ! command -v bundle >/dev/null 2>&1; then \
		echo "Installing Bundler..."; \
		gem install bundler --user-install --quiet 2>/dev/null || \
		echo "⚠️  Bundler installation failed. You may need to install it manually: gem install bundler"; \
	else \
		echo "✅ Bundler already available"; \
	fi
	@echo "✅ Documentation environment setup complete!"
	@echo "💡 Next: Run 'make docs-install' to install dependencies"

# Install documentation dependencies
docs-install:
	@echo "📦 Installing documentation dependencies..."
	@echo "Installing Ruby gems via Bundler (local path)..."
	bundle config set --local path '.bundle' && bundle install --quiet
	@echo "✅ Documentation dependencies installed!"
	@echo "💡 Ready to build docs with 'make docs' or serve with 'make docs-serve'"

# Generate documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "Ensuring dependencies are installed..."
	@bundle check >/dev/null 2>&1 || bundle config set --local path '.bundle' && bundle install --quiet
	@echo "Building Jekyll site..."
	bundle exec jekyll build --destination _site
	@echo "✅ Documentation built successfully!"
	@echo "📖 Open _site/index.html in your browser to view the documentation"
	@echo "🌐 Or serve locally with: make docs-serve"

# Serve documentation locally
docs-serve:
	@echo "🌐 Starting Jekyll development server..."
	@echo "Ensuring dependencies are installed..."
	@bundle check >/dev/null 2>&1 || bundle config set --local path '.bundle' && bundle install --quiet
	@echo "📖 Documentation will be available at http://localhost:4000/AI-Cohort-July-2025/"
	@echo "🔄 Auto-reload enabled - changes will be reflected automatically"
	@echo "💡 Use Ctrl+C to stop the server"
	@echo "💡 Note: Due to GitHub Pages baseurl, visit http://localhost:4000/AI-Cohort-July-2025/"
	bundle exec jekyll serve --host 0.0.0.0 --port 4000 --livereload

# Serve documentation locally without baseurl (for easier access)
docs-serve-local:
	@echo "🌐 Starting Jekyll development server (local mode)..."
	@echo "Ensuring dependencies are installed..."
	@bundle check >/dev/null 2>&1 || bundle config set --local path '.bundle' && bundle install --quiet
	@echo "📖 Documentation will be available at http://localhost:4000/"
	@echo "🔄 Auto-reload enabled - changes will be reflected automatically"
	@echo "💡 Use Ctrl+C to stop the server"
	@echo "🚀 Starting server without baseurl for easier local access..."
	bundle exec jekyll serve --host 0.0.0.0 --port 4000 --baseurl "" --livereload

# Clean documentation build
docs-clean:
	@echo "🧹 Cleaning documentation build..."
	rm -rf _site/
	rm -rf .jekyll-cache/
	rm -rf .bundle/
	@echo "✅ Documentation build artifacts cleaned!"

# Check documentation links and validate
docs-check:
	@echo "🔍 Checking documentation links and validation..."
	@echo "Building documentation first..."
	@make docs-clean
	@make docs
	@echo "Checking for broken links..."
	@if command -v markdown-link-check >/dev/null 2>&1; then \
		find docs -name "*.md" -exec markdown-link-check {} \; || echo "⚠️  Some links may be broken - check output above"; \
	else \
		echo "💡 Install markdown-link-check for link validation: npm install -g markdown-link-check"; \
	fi
	@echo "Validating Jekyll configuration..."
	@bundle exec jekyll doctor
	@echo "✅ Documentation check complete!"

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

# Docker Commands
# ==============

# Start Docker containers
docker-up:
	@echo "🐳 Starting Docker containers..."
	@echo "Frontend will be available at http://localhost:3000"
	@echo "Backend API will be available at http://localhost:5000"
	@echo "Creating required directories..."
	mkdir -p data/backend logs/backend
	docker-compose up -d
	@echo "✅ Containers started successfully!"
	@echo "💡 Use 'make docker-logs' to view logs"
	@echo "💡 Use 'make docker-status' to check container health"

# Stop Docker containers
docker-down:
	@echo "🛑 Stopping Docker containers..."
	docker-compose down
	@echo "✅ Containers stopped successfully!"

# Build Docker images
docker-build:
	@echo "🔨 Building Docker images..."
	docker-compose build
	@echo "✅ Docker images built successfully!"

# Rebuild Docker images from scratch
docker-rebuild:
	@echo "🔨 Rebuilding Docker images from scratch..."
	docker-compose build --no-cache --pull
	@echo "✅ Docker images rebuilt successfully!"

# View container logs
docker-logs:
	@echo "📜 Viewing Docker container logs..."
	@echo "💡 Press Ctrl+C to stop following logs"
	docker-compose logs -f

# Show container status and health
docker-status:
	@echo "📊 Docker container status:"
	@echo "=========================="
	docker-compose ps
	@echo ""
	@echo "🏥 Container health status:"
	@echo "========================="
	@docker inspect --format='{{.Name}}: {{.State.Health.Status}}' $$(docker-compose ps -q) 2>/dev/null || echo "Health checks not available for all containers"

# Clean up Docker resources
docker-clean:
	@echo "🧹 Cleaning up Docker resources..."
	@echo "Stopping containers..."
	docker-compose down -v
	@echo "Removing unused images..."
	docker image prune -f
	@echo "Removing unused volumes..."
	docker volume prune -f
	@echo "Removing unused networks..."
	docker network prune -f
	@echo "✅ Docker cleanup completed!"

# Development mode (with live reload)
docker-dev:
	@echo "🛠️  Starting Docker containers in development mode..."
	@echo "Frontend will be available at http://localhost:3000"
	@echo "Backend API will be available at http://localhost:5000"
	@echo "Creating required directories..."
	mkdir -p data/backend logs/backend
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d 2>/dev/null || docker-compose up -d
	@echo "✅ Development containers started!"
	@echo "💡 Use 'make docker-logs' to view logs"

# Production mode
docker-prod:
	@echo "🚀 Starting Docker containers in production mode..."
	@echo "Creating required directories..."
	mkdir -p data/backend logs/backend
	ENVIRONMENT=production docker-compose up -d
	@echo "✅ Production containers started!"
	@echo "💡 Use 'make docker-status' to check health"

# Open shell in backend container
docker-shell:
	@echo "🐚 Opening shell in backend container..."
	@docker exec -it autodevhub-backend /bin/bash 2>/dev/null || \
	 docker exec -it autodevhub-backend /bin/sh 2>/dev/null || \
	 echo "❌ Backend container not running. Use 'make docker-up' first."

# Execute command in container
docker-exec:
	@echo "🔧 Execute command in container"
	@echo "Usage: make docker-exec SERVICE=backend COMMAND='ls -la'"
	@echo "       make docker-exec SERVICE=frontend COMMAND='npm list'"
	@if [ -z "$(SERVICE)" ] || [ -z "$(COMMAND)" ]; then \
		echo "❌ Please specify SERVICE and COMMAND"; \
		echo "Example: make docker-exec SERVICE=backend COMMAND='python --version'"; \
	else \
		echo "Executing '$(COMMAND)' in $(SERVICE) container..."; \
		docker-compose exec $(SERVICE) $(COMMAND); \
	fi

# Docker validation and prerequisites
docker-check:
	@echo "🔍 Checking Docker environment..."
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "❌ Docker is not installed"; \
		exit 1; \
	fi
	@if ! command -v docker-compose >/dev/null 2>&1; then \
		echo "❌ Docker Compose is not installed"; \
		exit 1; \
	fi
	@if ! docker info >/dev/null 2>&1; then \
		echo "❌ Docker daemon is not running"; \
		exit 1; \
	fi
	@echo "✅ Docker environment is ready!"
	@echo "Docker version: $$(docker --version)"
	@echo "Docker Compose version: $$(docker-compose --version)"