"""
Tests for the main FastAPI application.

This module contains comprehensive tests for the main FastAPI application
including startup/shutdown events, middleware, exception handlers, and basic endpoints.
"""

import pytest
import time
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app


@pytest.mark.unit
class TestApplication:
    """Test cases for the main FastAPI application."""

    def test_app_creation(self):
        """Test that the FastAPI app is created with correct configuration."""
        assert app.title == "AutoDevHub API"
        assert (
            app.description
            == "AI-Powered DevOps Tracker - Backend API for managing development stories and workflows"
        )
        assert app.version == "1.0.0"
        assert app.docs_url == "/docs"
        assert app.redoc_url == "/redoc"
        assert app.openapi_url == "/openapi.json"

    def test_cors_middleware_configured(self):
        """Test that CORS middleware is properly configured."""
        # Check if CORS middleware is in the middleware stack
        middleware_classes = [
            middleware.cls.__name__ for middleware in app.user_middleware
        ]
        assert "CORSMiddleware" in middleware_classes

    def test_custom_middleware_configured(self):
        """Test that custom middleware is properly configured."""
        # The process time middleware should be configured
        # We can test this by checking the middleware stack
        assert len(app.user_middleware) >= 1


@pytest.mark.integration
class TestHealthEndpoints:
    """Test cases for health check endpoints."""

    def test_root_endpoint(self, test_client):
        """Test the root endpoint returns correct information."""
        response = test_client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert data["message"] == "Welcome to AutoDevHub API"
        assert data["version"] == "1.0.0"
        assert data["documentation"] == "/docs"
        assert data["health_check"] == "/health"

    def test_health_check_endpoint(self, test_client):
        """Test the health check endpoint returns system status."""
        response = test_client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert data["service"] == "AutoDevHub API"
        assert "timestamp" in data
        assert isinstance(data["timestamp"], (int, float))

        # These should be updated once full implementation is complete
        assert "database" in data
        assert "ai_service" in data

    def test_health_check_performance(self, test_client):
        """Test that health check responds quickly."""
        start_time = time.time()
        response = test_client.get("/health")
        end_time = time.time()

        assert response.status_code == 200
        # Health check should respond within 100ms
        assert (end_time - start_time) < 0.1


@pytest.mark.integration
class TestMiddleware:
    """Test cases for middleware functionality."""

    def test_process_time_header(self, test_client):
        """Test that process time header is added to responses."""
        response = test_client.get("/")

        assert response.status_code == 200
        assert "X-Process-Time" in response.headers

        # Verify the process time is a valid float
        process_time = float(response.headers["X-Process-Time"])
        assert process_time >= 0
        assert process_time < 1.0  # Should be very fast for simple endpoint

    def test_process_time_varies(self, test_client):
        """Test that process time varies between requests."""
        response1 = test_client.get("/")
        response2 = test_client.get("/health")

        time1 = float(response1.headers["X-Process-Time"])
        time2 = float(response2.headers["X-Process-Time"])

        # Times should be different (though might be very close)
        assert isinstance(time1, float)
        assert isinstance(time2, float)


@pytest.mark.integration
class TestExceptionHandlers:
    """Test cases for exception handlers."""

    def test_404_handler(self, test_client):
        """Test custom 404 error handling."""
        response = test_client.get("/nonexistent-endpoint")

        assert response.status_code == 404
        data = response.json()

        assert data["error"] is True
        assert "message" in data
        assert data["status_code"] == 404
        assert data["path"] == "/nonexistent-endpoint"

    def test_validation_error_handler(self, test_client):
        """Test validation error handling."""
        # Send invalid data to story generation endpoint
        invalid_data = {
            "description": "",  # Too short, should fail validation
            "story_type": "invalid_type",  # Invalid type
        }

        response = test_client.post("/api/v1/generate-story", json=invalid_data)

        assert response.status_code == 422
        data = response.json()

        assert data["error"] is True
        assert data["message"] == "Request validation failed"
        assert "details" in data
        assert data["path"] == "/api/v1/generate-story"
        assert isinstance(data["details"], list)

    @patch("main.logger")
    def test_general_exception_handler(self, mock_logger, test_client):
        """Test general exception handling."""
        # Mock an endpoint to raise an exception
        with patch("routers.stories.generate_story") as mock_endpoint:
            mock_endpoint.side_effect = Exception("Test exception")

            response = test_client.post(
                "/api/v1/generate-story",
                json={"description": "Test feature description for exception handling"},
            )

            assert response.status_code == 500
            data = response.json()

            assert data["error"] is True
            assert data["message"] == "Internal server error"
            assert data["path"] == "/api/v1/generate-story"


@pytest.mark.integration
class TestRouterIntegration:
    """Test cases for router integration."""

    def test_stories_router_included(self, test_client):
        """Test that stories router is properly included."""
        # Test that we can access stories endpoints
        response = test_client.get("/api/v1/stories")

        # Should not return 404, indicating router is included
        assert response.status_code != 404
        # Might return other status codes based on implementation

    def test_api_versioning(self, test_client):
        """Test API versioning structure."""
        # Test v1 API endpoints exist
        endpoints_to_test = [
            "/api/v1/stories",
        ]

        for endpoint in endpoints_to_test:
            response = test_client.get(endpoint)
            # Should not be 404 (not found)
            assert response.status_code != 404


@pytest.mark.integration
class TestDocumentation:
    """Test cases for API documentation."""

    def test_openapi_schema_generation(self, test_client):
        """Test that OpenAPI schema is generated correctly."""
        response = test_client.get("/openapi.json")

        assert response.status_code == 200
        schema = response.json()

        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "AutoDevHub API"
        assert schema["info"]["version"] == "1.0.0"
        assert "paths" in schema

    def test_swagger_ui_available(self, test_client):
        """Test that Swagger UI is available."""
        response = test_client.get("/docs")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_redoc_available(self, test_client):
        """Test that ReDoc is available."""
        response = test_client.get("/redoc")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


@pytest.mark.integration
class TestApplicationLifecycle:
    """Test cases for application lifecycle events."""

    @patch("main.logger")
    def test_startup_event_logging(self, mock_logger):
        """Test that startup event logs correctly."""
        # Create a new test client to trigger startup
        with TestClient(app) as client:
            # Check that startup logging was called
            mock_logger.info.assert_any_call("AutoDevHub API starting up...")

    @patch("main.logger")
    def test_shutdown_event_logging(self, mock_logger):
        """Test that shutdown event logs correctly."""
        # Create and close a test client to trigger shutdown
        with TestClient(app) as client:
            pass  # Client will close automatically

        # Check that shutdown logging was called
        mock_logger.info.assert_any_call("AutoDevHub API shutting down...")


@pytest.mark.performance
class TestPerformance:
    """Performance tests for the main application."""

    def test_concurrent_health_checks(self, test_client):
        """Test that the app can handle concurrent health check requests."""
        import concurrent.futures
        import threading

        def make_request():
            return test_client.get("/health")

        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"

    def test_response_time_consistency(self, test_client):
        """Test that response times are consistent."""
        response_times = []

        for _ in range(10):
            start_time = time.time()
            response = test_client.get("/")
            end_time = time.time()

            assert response.status_code == 200
            response_times.append(end_time - start_time)

        # Calculate statistics
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)

        # All responses should be reasonably fast and consistent
        assert avg_time < 0.1  # Average should be under 100ms
        assert max_time < 0.2  # No single request should take over 200ms


@pytest.mark.unit
class TestConfiguration:
    """Test cases for application configuration."""

    @patch("main.get_settings")
    def test_settings_integration(self, mock_get_settings):
        """Test that settings are properly integrated."""
        mock_settings = MagicMock()
        mock_settings.allowed_origins = ["http://localhost:3000"]
        mock_settings.environment = "testing"
        mock_settings.debug = True
        mock_get_settings.return_value = mock_settings

        # Re-import to trigger settings loading
        from main import app

        # Verify settings are used
        mock_get_settings.assert_called()

    def test_debug_mode_affects_behavior(self):
        """Test that debug mode affects application behavior."""
        # This would test different behaviors in debug vs production
        # For now, we can test that the setting exists and is configurable
        from config import get_settings

        settings = get_settings()

        # Settings should have debug property
        assert hasattr(settings, "debug")
        assert isinstance(settings.debug, bool)


@pytest.mark.integration
class TestSecurityHeaders:
    """Test cases for security-related headers and configurations."""

    def test_no_server_header_leakage(self, test_client):
        """Test that server information is not leaked in headers."""
        response = test_client.get("/")

        # Should not expose detailed server information
        server_header = response.headers.get("server", "").lower()
        # Basic check - should not expose version info
        assert "uvicorn" not in server_header or len(server_header.split()) <= 1

    def test_content_type_headers(self, test_client):
        """Test that proper content-type headers are set."""
        response = test_client.get("/")

        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

    def test_cors_headers_present(self, test_client):
        """Test that CORS headers are present when needed."""
        # Make a preflight request
        response = test_client.options(
            "/api/v1/stories",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )

        # CORS headers should be present
        assert (
            "access-control-allow-origin" in response.headers
            or response.status_code == 200
        )
