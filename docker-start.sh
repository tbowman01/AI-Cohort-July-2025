#!/bin/bash
# Docker startup script for AutoDevHub

set -e

echo "🐳 Starting AutoDevHub Docker Environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please review and update the values."
fi

# Function to start services based on profile
start_services() {
    local profile=${1:-default}
    
    case $profile in
        "dev")
            echo "🚀 Starting development environment..."
            docker-compose up -d database backend frontend
            ;;
        "prod")
            echo "🚀 Starting production environment..."
            docker-compose --profile production up -d
            ;;
        "fullstack")
            echo "🚀 Starting full-stack single container..."
            docker-compose --profile fullstack up -d database fullstack
            ;;
        "cache")
            echo "🚀 Starting with Redis cache..."
            docker-compose --profile cache up -d
            ;;
        *)
            echo "🚀 Starting default services..."
            docker-compose up -d database backend frontend
            ;;
    esac
}

# Parse command line arguments
PROFILE="default"
REBUILD=false
LOGS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --profile)
            PROFILE="$2"
            shift 2
            ;;
        --rebuild)
            REBUILD=true
            shift
            ;;
        --logs)
            LOGS=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --profile PROFILE   Specify deployment profile (dev, prod, fullstack, cache)"
            echo "  --rebuild          Rebuild containers before starting"
            echo "  --logs            Follow logs after starting"
            echo "  --help            Show this help message"
            echo ""
            echo "Profiles:"
            echo "  dev               Development environment (default)"
            echo "  prod              Production environment with Nginx"
            echo "  fullstack         Single container with both frontend and backend"
            echo "  cache             Include Redis cache service"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Rebuild containers if requested
if [ "$REBUILD" = true ]; then
    echo "🔨 Rebuilding containers..."
    docker-compose build --no-cache
fi

# Start services
start_services "$PROFILE"

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

# Show logs if requested
if [ "$LOGS" = true ]; then
    echo "📋 Following logs (Press Ctrl+C to stop)..."
    docker-compose logs -f
else
    echo ""
    echo "✅ AutoDevHub is running!"
    echo ""
    echo "🌐 Services:"
    if docker-compose ps | grep -q "backend.*Up"; then
        echo "   Backend API: http://localhost:8000"
        echo "   API Docs: http://localhost:8000/docs"
    fi
    if docker-compose ps | grep -q "frontend.*Up"; then
        echo "   Frontend: http://localhost:3000"
    fi
    if docker-compose ps | grep -q "fullstack.*Up"; then
        echo "   Full Stack: http://localhost"
    fi
    if docker-compose ps | grep -q "database.*Up"; then
        echo "   Database: postgresql://localhost:5432/autodevhub"
    fi
    echo ""
    echo "📋 To view logs: docker-compose logs -f"
    echo "🛑 To stop: docker-compose down"
fi