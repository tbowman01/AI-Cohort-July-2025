"""
AutoDevHub Backend - FastAPI Application Entry Point

This module serves as the main entry point for the AutoDevHub FastAPI
application,
providing API endpoints for AI-powered DevOps tracking functionality.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import time
from typing import Dict, Any

from routers import stories
from config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="AutoDevHub API",
    description=(
        "AI-Powered DevOps Tracker - Backend API for managing development "
        "stories and workflows"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Get application settings
settings = get_settings()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers for performance monitoring."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with structured error responses."""
    logger.warning(f"HTTP {exc.status_code} error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors with detailed field information."""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Request validation failed",
            "details": exc.errors(),
            "path": str(request.url.path),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions with logging."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "path": str(request.url.path),
        },
    )


# Health check endpoint
@app.get("/health", tags=["Health"], summary="Health Check")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify API availability and basic functionality.

    Returns:
        Dict containing health status, version, and timestamp
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "AutoDevHub API",
        "timestamp": time.time(),
        "database": "pending",  # Will be updated once database models
        # are ready
        "ai_service": "pending"  # Will be updated once AI integration
        # is complete
    }


# Root endpoint - redirect to docs
@app.get("/", tags=["Root"], summary="API Root")
async def root():
    """
    Root endpoint redirects to API documentation.
    """
    return RedirectResponse(url="/docs")


# Include routers
app.include_router(stories.router, prefix="/api/v1", tags=["Stories"])




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
    )
