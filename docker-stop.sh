#!/bin/bash
# Docker stop script for AutoDevHub

set -e

echo "🛑 Stopping AutoDevHub Docker Environment..."

# Parse command line arguments
REMOVE_VOLUMES=false
REMOVE_IMAGES=false
CLEANUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --volumes)
            REMOVE_VOLUMES=true
            shift
            ;;
        --images)
            REMOVE_IMAGES=true
            shift
            ;;
        --cleanup)
            CLEANUP=true
            REMOVE_VOLUMES=true
            REMOVE_IMAGES=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --volumes    Remove named volumes (WARNING: This deletes data!)"
            echo "  --images     Remove built images"
            echo "  --cleanup    Full cleanup (volumes + images + networks)"
            echo "  --help       Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                   # Stop containers only"
            echo "  $0 --volumes         # Stop containers and remove volumes"
            echo "  $0 --cleanup         # Full cleanup"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Stop containers
echo "⏹️  Stopping containers..."
docker-compose down

# Remove volumes if requested
if [ "$REMOVE_VOLUMES" = true ]; then
    echo "🗑️  Removing volumes (this will delete data)..."
    docker-compose down -v
    
    # Remove named volumes explicitly
    echo "🧹 Cleaning up named volumes..."
    docker volume rm autodevhub_postgres_data 2>/dev/null || true
    docker volume rm autodevhub_backend_data 2>/dev/null || true
    docker volume rm autodevhub_backend_logs 2>/dev/null || true
    docker volume rm autodevhub_frontend_data 2>/dev/null || true
    docker volume rm autodevhub_fullstack_data 2>/dev/null || true
    docker volume rm autodevhub_fullstack_logs 2>/dev/null || true
    docker volume rm autodevhub_redis_data 2>/dev/null || true
    docker volume rm autodevhub_nginx_logs 2>/dev/null || true
fi

# Remove images if requested
if [ "$REMOVE_IMAGES" = true ]; then
    echo "🗑️  Removing built images..."
    
    # Remove project images
    docker image rm autodevhub-backend 2>/dev/null || true
    docker image rm autodevhub-frontend 2>/dev/null || true
    docker image rm autodevhub-fullstack 2>/dev/null || true
    
    # Remove dangling images
    echo "🧹 Removing dangling images..."
    docker image prune -f
fi

# Full cleanup if requested
if [ "$CLEANUP" = true ]; then
    echo "🧹 Performing full cleanup..."
    
    # Remove networks
    docker network rm autodevhub_autodevhub-network 2>/dev/null || true
    
    # System cleanup
    echo "🧹 Running system cleanup..."
    docker system prune -f
fi

echo "✅ AutoDevHub Docker environment stopped successfully!"

# Show remaining resources
echo ""
echo "📊 Remaining Docker resources:"
echo "Containers:"
docker ps -a --filter "name=autodevhub" --format "table {{.Names}}\t{{.Status}}" || echo "  None"

echo ""
echo "Images:"
docker images --filter "reference=autodevhub*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" || echo "  None"

echo ""
echo "Volumes:"
docker volume ls --filter "name=autodevhub" --format "table {{.Name}}\t{{.Driver}}" || echo "  None"

echo ""
echo "Networks:"
docker network ls --filter "name=autodevhub" --format "table {{.Name}}\t{{.Driver}}" || echo "  None"