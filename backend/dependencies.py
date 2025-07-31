"""
AutoDevHub Backend Dependencies

This module provides dependency injection functions for FastAPI endpoints,
including database session management, authentication, and other shared resources.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator, Optional
import logging
from functools import lru_cache

from config import get_settings

logger = logging.getLogger(__name__)

# Security scheme for JWT authentication
security = HTTPBearer(auto_error=False)

# Database engine and session configuration
settings = get_settings()


@lru_cache()
def get_database_engine():
    """
    Create and cache database engine.
    
    Returns:
        SQLAlchemy Engine configured with application settings
    """
    # SQLite-specific engine creation
    if "sqlite" in settings.database_url:
        engine = create_engine(
            settings.database_url,
            echo=settings.database_echo,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False}
        )
    else:
        # PostgreSQL/other databases with connection pooling
        engine = create_engine(
            settings.database_url,
            echo=settings.database_echo,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=10,
            max_overflow=20
        )
    return engine


# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_database_engine()
)


def get_database_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    
    Provides a database session for the duration of a request
    and ensures proper cleanup after the request completes.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        logger.debug("Database session created")
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        logger.debug("Database session closed")
        db.close()


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """
    Dependency to get current authenticated user.
    
    Args:
        credentials: JWT token from Authorization header
        
    Returns:
        dict: User information if authenticated, None if optional
        
    Raises:
        HTTPException: If authentication is required but invalid
    """
    if not credentials:
        # For now, return None to allow unauthenticated access
        # This will be updated once user authentication is implemented
        logger.debug("No authentication credentials provided")
        return None
    
    try:
        # TODO: Implement JWT token validation once user models are ready
        # For now, this is a placeholder that allows any bearer token
        token = credentials.credentials
        logger.debug(f"Authentication token received: {token[:10]}...")
        
        # Placeholder user data - replace with actual JWT validation
        return {
            "id": "placeholder-user-id",
            "username": "placeholder-user",
            "email": "user@example.com"
        }
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_authentication(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Dependency that requires authentication.
    
    Args:
        current_user: Current user from get_current_user dependency
        
    Returns:
        dict: Authenticated user information
        
    Raises:
        HTTPException: If user is not authenticated
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


def get_settings_dependency():
    """
    Dependency to get application settings.
    
    Returns:
        Settings: Application configuration settings
    """
    return get_settings()


class RateLimiter:
    """
    Simple rate limiter for API endpoints.
    
    This is a basic implementation that can be enhanced with Redis
    for distributed rate limiting in production.
    """
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed based on rate limits.
        
        Args:
            identifier: Unique identifier (IP address, user ID, etc.)
            
        Returns:
            bool: True if request is allowed, False if rate limited
        """
        import time
        current_time = time.time()
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Remove expired requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if current_time - req_time < self.window_seconds
        ]
        
        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(current_time)
            return True
        
        return False


# Global rate limiter instance
rate_limiter = RateLimiter(
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_period
)


async def check_rate_limit(request_id: str = "default") -> bool:
    """
    Dependency to check rate limits.
    
    Args:
        request_id: Identifier for rate limiting (IP, user ID, etc.)
        
    Returns:
        bool: True if request is allowed
        
    Raises:
        HTTPException: If rate limit is exceeded
    """
    if not rate_limiter.is_allowed(request_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    return True


# AI Service Dependencies
class AIServiceManager:
    """
    Manager for AI service connections and configurations.
    
    This class will handle OpenAI API connections and other AI services
    once they are integrated into the application.
    """
    
    def __init__(self):
        self.openai_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AI service clients."""
        try:
            if settings.openai_api_key:
                # TODO: Initialize OpenAI client when AI integration is ready
                logger.info("AI services configuration loaded")
            else:
                logger.warning("OpenAI API key not configured")
        except Exception as e:
            logger.error(f"Failed to initialize AI services: {str(e)}")
    
    async def generate_story(self, description: str) -> dict:
        """
        Generate Gherkin story from feature description.
        
        Args:
            description: Feature description
            
        Returns:
            dict: Generated story data
        """
        # Placeholder implementation until AI integration is complete
        return {
            "title": f"Story for: {description[:50]}...",
            "description": description,
            "gherkin": f"""
Feature: {description[:100]}

  Scenario: Basic functionality
    Given the system is ready
    When I perform the action
    Then I should see the expected result
            """.strip(),
            "acceptance_criteria": [
                "System should handle the basic use case",
                "Error handling should be implemented",
                "Performance should meet requirements"
            ]
        }


# Global AI service manager
ai_service = AIServiceManager()


async def get_ai_service() -> AIServiceManager:
    """
    Dependency to get AI service manager.
    
    Returns:
        AIServiceManager: AI service manager instance
    """
    return ai_service


# Health check dependencies
async def check_database_health() -> dict:
    """
    Check database connectivity for health checks.
    
    Returns:
        dict: Database health status
    """
    try:
        # Test database connection
        engine = get_database_engine()
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


async def check_ai_service_health() -> dict:
    """
    Check AI service connectivity for health checks.
    
    Returns:
        dict: AI service health status
    """
    try:
        # TODO: Implement actual AI service health check
        if settings.openai_api_key:
            return {"status": "configured", "ai_service": "ready"}
        else:
            return {"status": "not_configured", "ai_service": "missing_api_key"}
    except Exception as e:
        logger.error(f"AI service health check failed: {str(e)}")
        return {"status": "unhealthy", "ai_service": "error", "error": str(e)}