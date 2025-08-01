"""
Tests for the AI story generation service and related functionality.

This module contains comprehensive tests for the story generation features,
including AI service integration, story validation, and error handling.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from dependencies import AIServiceManager
from routers.stories import (
    StoryGenerationRequest,
    StoryResponse,
    _estimate_story_points,
    _generate_tags,
)


@pytest.mark.ai_service
@pytest.mark.unit
class TestAIServiceManager:
    """Test cases for the AIServiceManager class."""

    def test_ai_service_manager_initialization(self):
        """Test AIServiceManager initialization."""
        ai_service = AIServiceManager()

        assert ai_service.openai_client is None  # Should be None in test environment
        assert hasattr(ai_service, "generate_story")

    @pytest.mark.asyncio
    async def test_generate_story_basic(self):
        """Test basic story generation functionality."""
        ai_service = AIServiceManager()

        description = "As a user, I want to create an account"
        result = await ai_service.generate_story(description)

        assert isinstance(result, dict)
        assert "title" in result
        assert "description" in result
        assert "gherkin" in result
        assert "acceptance_criteria" in result

        assert result["description"] == description
        assert isinstance(result["acceptance_criteria"], list)
        assert len(result["acceptance_criteria"]) > 0

    @pytest.mark.asyncio
    async def test_generate_story_content_quality(self):
        """Test the quality and structure of generated story content."""
        ai_service = AIServiceManager()

        description = (
            "As a developer, I want to implement user authentication with JWT tokens"
        )
        result = await ai_service.generate_story(description)

        # Verify title is meaningful
        assert len(result["title"]) > 10
        assert (
            description[:20] in result["title"]
            or "authentication" in result["title"].lower()
        )

        # Verify Gherkin structure
        gherkin = result["gherkin"]
        assert "Feature:" in gherkin
        assert "Scenario:" in gherkin
        assert "Given" in gherkin
        assert "When" in gherkin
        assert "Then" in gherkin

        # Verify acceptance criteria
        criteria = result["acceptance_criteria"]
        assert len(criteria) >= 3
        for criterion in criteria:
            assert isinstance(criterion, str)
            assert len(criterion) > 10

    @pytest.mark.asyncio
    async def test_generate_story_different_descriptions(self):
        """Test story generation with various description types."""
        ai_service = AIServiceManager()

        test_descriptions = [
            "Simple feature description",
            "As a user, I want to login so that I can access my account",
            "Implement API endpoint for user registration with email validation",
            "Bug fix: Login button not working on mobile devices",
            "Epic: Complete user management system with CRUD operations",
        ]

        for description in test_descriptions:
            result = await ai_service.generate_story(description)

            assert isinstance(result, dict)
            assert result["description"] == description
            assert len(result["title"]) > 0
            # Should have substantial content
            assert len(result["gherkin"]) > 50
            assert len(result["acceptance_criteria"]) > 0

    @pytest.mark.asyncio
    async def test_generate_story_edge_cases(self):
        """Test story generation with edge cases."""
        ai_service = AIServiceManager()

        # Very short description
        short_result = await ai_service.generate_story("Login")
        assert isinstance(short_result, dict)
        assert "Login" in short_result["title"]

        # Very long description
        long_description = "A" * 500  # 500 character description
        long_result = await ai_service.generate_story(long_description)
        assert isinstance(long_result, dict)
        assert long_result["description"] == long_description

        # Description with special characters
        special_description = (
            "Feature with émojis 🚀 and spéciâl châràctérs & symbols @#$%"
        )
        special_result = await ai_service.generate_story(special_description)
        assert isinstance(special_result, dict)
        assert special_result["description"] == special_description


@pytest.mark.unit
class TestStoryValidationModels:
    """Test cases for Pydantic models used in story validation."""

    def test_story_generation_request_valid(self):
        """Test valid StoryGenerationRequest creation."""
        request = StoryGenerationRequest(
            description="As a user, I want to create an account",
            project_context="User management system",
            story_type="user_story",
            complexity="medium",
        )

        assert request.description == "As a user, I want to create an account"
        assert request.project_context == "User management system"
        assert request.story_type == "user_story"
        assert request.complexity == "medium"

    def test_story_generation_request_defaults(self):
        """Test StoryGenerationRequest with default values."""
        request = StoryGenerationRequest(description="Test feature description")

        assert request.description == "Test feature description"
        assert request.project_context is None
        assert request.story_type == "user_story"
        assert request.complexity == "medium"

    def test_story_generation_request_validation_errors(self):
        """Test StoryGenerationRequest validation errors."""
        # Test minimum length validation
        with pytest.raises(ValueError, match="at least 10 characters"):
            StoryGenerationRequest(description="short")

        # Test maximum length validation
        with pytest.raises(ValueError, match="at most 1000 characters"):
            StoryGenerationRequest(description="A" * 1001)

        # Test invalid story type
        with pytest.raises(ValueError, match="story_type must be one of"):
            StoryGenerationRequest(
                description="Valid description", story_type="invalid_type"
            )

        # Test invalid complexity
        with pytest.raises(ValueError, match="complexity must be one of"):
            StoryGenerationRequest(
                description="Valid description", complexity="invalid_complexity"
            )

    def test_story_generation_request_valid_enums(self):
        """Test StoryGenerationRequest with all valid enum values."""
        valid_story_types = ["user_story", "epic", "bug_fix", "technical_task"]
        valid_complexities = ["low", "medium", "high", "epic"]

        for story_type in valid_story_types:
            request = StoryGenerationRequest(
                description="Test description for validation", story_type=story_type
            )
            assert request.story_type == story_type

        for complexity in valid_complexities:
            request = StoryGenerationRequest(
                description="Test description for validation", complexity=complexity
            )
            assert request.complexity == complexity

    def test_story_response_model(self):
        """Test StoryResponse model creation."""
        response = StoryResponse(
            id="test-id-123",
            title="Test Story Title",
            description="Test description",
            gherkin="Feature: Test\nScenario: Test scenario",
            acceptance_criteria=["Criterion 1", "Criterion 2"],
            story_type="user_story",
            complexity="medium",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert response.id == "test-id-123"
        assert response.title == "Test Story Title"
        assert response.status == "draft"  # Default value
        assert response.estimated_points is None  # Default value
        assert response.tags == []  # Default value


@pytest.mark.unit
class TestStoryUtilityFunctions:
    """Test cases for story utility functions."""

    def test_estimate_story_points(self):
        """Test story points estimation based on complexity."""
        assert _estimate_story_points("low") == 2
        assert _estimate_story_points("medium") == 5
        assert _estimate_story_points("high") == 8
        assert _estimate_story_points("epic") == 13

        # Test default case
        assert _estimate_story_points("unknown") == 5

    def test_generate_tags_basic(self):
        """Test basic tag generation."""
        tags = _generate_tags("User login feature", "user_story")

        assert "user_story" in tags
        assert isinstance(tags, list)
        assert len(tags) > 0

    def test_generate_tags_technology_detection(self):
        """Test technology keyword detection in tag generation."""
        test_cases = [
            ("API endpoint for user data", ["api"]),
            ("Database migration script", ["database"]),
            ("Frontend component for login", ["frontend"]),
            ("Backend service implementation", ["backend"]),
            ("Authentication and security features", ["authentication", "security"]),
            ("Performance optimization task", ["performance"]),
            ("UI/UX improvements", ["ui-ux"]),
            ("Testing framework setup", ["testing"]),
        ]

        for description, expected_tech_tags in test_cases:
            tags = _generate_tags(description, "user_story")

            assert "user_story" in tags
            for tech_tag in expected_tech_tags:
                assert tech_tag in tags

    def test_generate_tags_case_insensitive(self):
        """Test that tag generation is case insensitive."""
        tags_upper = _generate_tags("API ENDPOINT WITH DATABASE", "user_story")
        tags_lower = _generate_tags("api endpoint with database", "user_story")
        tags_mixed = _generate_tags("Api Endpoint With Database", "user_story")

        # Should all contain the same technology tags
        for tags in [tags_upper, tags_lower, tags_mixed]:
            assert "api" in tags
            assert "database" in tags
            assert "user_story" in tags

    def test_generate_tags_duplicate_removal(self):
        """Test that duplicate tags are removed."""
        # Description that would generate duplicate tags
        tags = _generate_tags("User story for user authentication", "user_story")

        # Should not have duplicates
        assert len(tags) == len(set(tags))
        assert "user_story" in tags

    def test_generate_tags_multiple_keywords(self):
        """Test tag generation with multiple technology keywords."""
        description = (
            "Full-stack API with database, frontend UI, backend security, and testing"
        )
        tags = _generate_tags(description, "technical_task")

        expected_tags = [
            "technical_task",
            "api",
            "database",
            "frontend",
            "backend",
            "security",
            "ui-ux",
            "testing",
        ]

        for expected_tag in expected_tags:
            assert expected_tag in tags


@pytest.mark.integration
class TestStoryGenerationIntegration:
    """Integration tests for story generation functionality."""

    def test_mock_ai_service_integration(self, mock_ai_service):
        """Test integration with mock AI service."""
        assert hasattr(mock_ai_service, "generate_story")
        assert callable(mock_ai_service.generate_story)

    @pytest.mark.asyncio
    async def test_story_generation_with_mock_service(self, mock_ai_service):
        """Test story generation using mock AI service."""
        description = "Test story generation integration"
        result = await mock_ai_service.generate_story(description)

        assert isinstance(result, dict)
        assert result["description"] == description
        assert "Test Story:" in result["title"]
        assert "Feature:" in result["gherkin"]
        assert len(result["acceptance_criteria"]) == 3

    @pytest.mark.asyncio
    async def test_story_generation_request_processing(self, mock_ai_service):
        """Test processing of story generation requests."""
        request = StoryGenerationRequest(
            description="Integration test feature",
            project_context="Test project",
            story_type="user_story",
            complexity="high",
        )

        # Process the request (simulating the endpoint logic)
        generated_story = await mock_ai_service.generate_story(request.description)

        # Create response model
        response = StoryResponse(
            id="test-id",
            title=generated_story["title"],
            description=request.description,
            gherkin=generated_story["gherkin"],
            acceptance_criteria=generated_story["acceptance_criteria"],
            story_type=request.story_type,
            complexity=request.complexity,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            project_context=request.project_context,
            estimated_points=_estimate_story_points(request.complexity),
            tags=_generate_tags(request.description, request.story_type),
        )

        assert response.description == "Integration test feature"
        assert response.project_context == "Test project"
        assert response.story_type == "user_story"
        assert response.complexity == "high"
        assert response.estimated_points == 8  # High complexity = 8 points


@pytest.mark.ai_service
@pytest.mark.performance
class TestStoryGenerationPerformance:
    """Performance tests for story generation."""

    @pytest.mark.asyncio
    async def test_story_generation_performance(self, mock_ai_service):
        """Test story generation performance."""
        import time

        description = "Performance test story generation"

        start_time = time.time()
        result = await mock_ai_service.generate_story(description)
        end_time = time.time()

        generation_time = end_time - start_time

        # Mock service should be very fast
        assert generation_time < 0.1  # Less than 100ms
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_concurrent_story_generation(self, mock_ai_service):
        """Test concurrent story generation requests."""
        import asyncio
        import time

        async def generate_story_task(index):
            description = f"Concurrent test story {index}"
            return await mock_ai_service.generate_story(description)

        start_time = time.time()

        # Generate 10 stories concurrently
        tasks = [generate_story_task(i) for i in range(10)]
        results = await asyncio.gather(*tasks)

        end_time = time.time()
        total_time = end_time - start_time

        # Should handle concurrent requests efficiently
        assert total_time < 1.0  # Less than 1 second for 10 concurrent requests
        assert len(results) == 10

        # Verify all results are valid
        for i, result in enumerate(results):
            assert isinstance(result, dict)
            assert f"Concurrent test story {i}" in result["description"]

    @pytest.mark.asyncio
    async def test_large_description_performance(self, mock_ai_service):
        """Test performance with large descriptions."""
        import time

        # Create a large description (1000 characters)
        large_description = "This is a very detailed feature description. " * 20

        start_time = time.time()
        result = await mock_ai_service.generate_story(large_description)
        end_time = time.time()

        generation_time = end_time - start_time

        # Should handle large descriptions efficiently
        assert generation_time < 0.5  # Less than 500ms
        assert isinstance(result, dict)
        assert result["description"] == large_description


@pytest.mark.unit
class TestStoryGenerationErrorHandling:
    """Test cases for error handling in story generation."""

    @pytest.mark.asyncio
    async def test_ai_service_error_simulation(self, simulate_ai_service_error):
        """Test handling of AI service errors."""
        ai_service = AIServiceManager()

        # Enable error simulation
        simulate_ai_service_error["enable"]()

        with pytest.raises(Exception, match="AI service unavailable"):
            await ai_service.generate_story("Test description")

        # Disable error simulation
        simulate_ai_service_error["disable"]()

        # Should work normally now
        result = await ai_service.generate_story("Test description")
        assert isinstance(result, dict)

    def test_invalid_request_data_handling(self):
        """Test handling of invalid request data."""
        # Test with invalid JSON-like data
        with pytest.raises(ValueError):
            StoryGenerationRequest(
                description="", story_type="user_story"  # Empty description should fail
            )

        with pytest.raises(ValueError):
            StoryGenerationRequest(
                description="Valid description",
                story_type="nonexistent_type",  # Invalid story type
            )

    def test_utility_function_error_handling(self):
        """Test error handling in utility functions."""
        # Test with None or empty inputs
        tags = _generate_tags("", "user_story")
        assert "user_story" in tags

        # Should handle None gracefully
        tags = _generate_tags(None, "user_story")
        assert "user_story" in tags

        # Test story points with invalid complexity
        points = _estimate_story_points(None)
        assert points == 5  # Should return default

        points = _estimate_story_points("")
        assert points == 5  # Should return default


@pytest.mark.ai_service
@pytest.mark.integration
class TestRealAIServiceIntegration:
    """Tests for real AI service integration (when available)."""

    @pytest.mark.skip(reason="Requires actual AI service configuration")
    @pytest.mark.asyncio
    async def test_real_ai_service_story_generation(self):
        """Test story generation with real AI service (when configured)."""
        # This test would only run when actual AI service is configured
        # Skip by default to avoid API calls in testing
        ai_service = AIServiceManager()

        # Only test if API key is actually configured
        from config import get_settings

        settings = get_settings()

        if settings.openai_api_key and settings.openai_api_key != "your-api-key-here":
            description = "As a user, I want to securely login to the application"
            result = await ai_service.generate_story(description)

            # Verify the result structure
            assert isinstance(result, dict)
            assert "title" in result
            assert "gherkin" in result
            assert "acceptance_criteria" in result

            # Real AI should generate more sophisticated content
            assert len(result["gherkin"]) > 100
            assert len(result["acceptance_criteria"]) >= 3

    def test_ai_service_configuration_validation(self):
        """Test AI service configuration validation."""
        ai_service = AIServiceManager()

        # Should initialize without errors even without API key
        assert ai_service is not None

        # Should have the generate_story method
        assert hasattr(ai_service, "generate_story")
        assert callable(ai_service.generate_story)
