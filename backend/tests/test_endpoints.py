"""
Tests for API endpoints integration.

This module contains comprehensive integration tests for all API endpoints,
including story generation, CRUD operations, authentication, and error handling.
"""

import pytest
import json
from unittest.mock import patch
from fastapi import status

from conftest import assert_story_response_valid, assert_story_list_response_valid


@pytest.mark.integration
class TestStoryGenerationEndpoint:
    """Test cases for the story generation endpoint."""

    def test_generate_story_success(self, test_client, mock_stories_storage):
        """Test successful story generation."""
        request_data = {
            "description": "As a user, I want to create an account so I can access the system",
            "project_context": "User management system",
            "story_type": "user_story",
            "complexity": "medium"
        }
        
        response = test_client.post("/api/v1/generate-story", json=request_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert_story_response_valid(data)
        assert data["description"] == request_data["description"]
        assert data["story_type"] == request_data["story_type"]
        assert data["complexity"] == request_data["complexity"]
        assert data["project_context"] == request_data["project_context"]
        assert data["status"] == "draft"
        assert data["estimated_points"] == 5  # Medium complexity
        assert "user_story" in data["tags"]
        
        # Verify the story was stored
        assert len(mock_stories_storage) == 1
        assert data["id"] in mock_stories_storage

    def test_generate_story_minimal_request(self, test_client, mock_stories_storage):
        """Test story generation with minimal required data."""
        request_data = {
            "description": "Basic feature description for testing minimal request"
        }
        
        response = test_client.post("/api/v1/generate-story", json=request_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert_story_response_valid(data)
        assert data["description"] == request_data["description"]
        assert data["story_type"] == "user_story"  # Default value
        assert data["complexity"] == "medium"  # Default value
        assert data["project_context"] is None
        assert data["estimated_points"] == 5  # Medium complexity default

    def test_generate_story_all_complexities(self, test_client, mock_stories_storage):
        """Test story generation with all complexity levels."""
        complexities = ["low", "medium", "high", "epic"]
        expected_points = {"low": 2, "medium": 5, "high": 8, "epic": 13}
        
        for complexity in complexities:
            request_data = {
                "description": f"Test story with {complexity} complexity",
                "complexity": complexity
            }
            
            response = test_client.post("/api/v1/generate-story", json=request_data)
            
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            
            assert data["complexity"] == complexity
            assert data["estimated_points"] == expected_points[complexity]

    def test_generate_story_all_story_types(self, test_client, mock_stories_storage):
        """Test story generation with all story types."""
        story_types = ["user_story", "epic", "bug_fix", "technical_task"]
        
        for story_type in story_types:
            request_data = {
                "description": f"Test {story_type} description",
                "story_type": story_type
            }
            
            response = test_client.post("/api/v1/generate-story", json=request_data)
            
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            
            assert data["story_type"] == story_type
            assert story_type in data["tags"]

    def test_generate_story_validation_errors(self, test_client):
        """Test story generation with validation errors."""
        # Test short description
        response = test_client.post("/api/v1/generate-story", json={
            "description": "short"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test long description
        response = test_client.post("/api/v1/generate-story", json={
            "description": "A" * 1001
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test invalid story type
        response = test_client.post("/api/v1/generate-story", json={
            "description": "Valid description",
            "story_type": "invalid_type"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test invalid complexity
        response = test_client.post("/api/v1/generate-story", json={
            "description": "Valid description",
            "complexity": "invalid_complexity"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_generate_story_missing_description(self, test_client):
        """Test story generation without required description."""
        response = test_client.post("/api/v1/generate-story", json={})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert data["error"] is True
        assert "description" in str(data["details"]).lower()

    @patch('routers.stories.ai_service.generate_story')
    def test_generate_story_ai_service_error(self, mock_generate, test_client):
        """Test story generation when AI service fails."""
        mock_generate.side_effect = Exception("AI service error")
        
        request_data = {
            "description": "Test description for error handling"
        }
        
        response = test_client.post("/api/v1/generate-story", json=request_data)
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        data = response.json()
        
        assert data["error"] is True
        assert "Failed to generate story" in data["message"]


@pytest.mark.integration
class TestStoryListEndpoint:
    """Test cases for the story list endpoint."""

    def test_list_stories_empty(self, test_client, mock_stories_storage):
        """Test listing stories when storage is empty."""
        response = test_client.get("/api/v1/stories")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert_story_list_response_valid(data)
        assert data["stories"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert data["has_next"] is False

    def test_list_stories_with_data(self, test_client, mock_stories_storage):
        """Test listing stories with data."""
        # Create some test stories first
        stories_data = []
        for i in range(5):
            story_data = {
                "description": f"Test story {i}",
                "story_type": "user_story" if i % 2 == 0 else "bug_fix"
            }
            response = test_client.post("/api/v1/generate-story", json=story_data)
            assert response.status_code == status.HTTP_201_CREATED
            stories_data.append(response.json())
        
        # List all stories
        response = test_client.get("/api/v1/stories")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert_story_list_response_valid(data)
        assert len(data["stories"]) == 5
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert data["has_next"] is False
        
        # Verify stories are sorted by creation date (newest first)
        story_dates = [story["created_at"] for story in data["stories"]]
        assert story_dates == sorted(story_dates, reverse=True)

    def test_list_stories_pagination(self, test_client, mock_stories_storage):
        """Test story list pagination."""
        # Create 15 test stories
        for i in range(15):
            story_data = {"description": f"Pagination test story {i}"}
            response = test_client.post("/api/v1/generate-story", json=story_data)
            assert response.status_code == status.HTTP_201_CREATED
        
        # Test first page
        response = test_client.get("/api/v1/stories?page=1&page_size=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert len(data["stories"]) == 5
        assert data["total"] == 15
        assert data["page"] == 1
        assert data["page_size"] == 5
        assert data["has_next"] is True
        
        # Test second page
        response = test_client.get("/api/v1/stories?page=2&page_size=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert len(data["stories"]) == 5
        assert data["page"] == 2
        assert data["has_next"] is True
        
        # Test last page
        response = test_client.get("/api/v1/stories?page=3&page_size=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert len(data["stories"]) == 5
        assert data["page"] == 3
        assert data["has_next"] is False

    def test_list_stories_filtering_by_status(self, test_client, mock_stories_storage):
        """Test story list filtering by status."""
        # Create stories and update their status
        story_ids = []
        for i in range(3):
            story_data = {"description": f"Status test story {i}"}
            response = test_client.post("/api/v1/generate-story", json=story_data)
            story_ids.append(response.json()["id"])
        
        # Update one story to "ready" status
        response = test_client.put(f"/api/v1/stories/{story_ids[0]}", json={"status": "ready"})
        assert response.status_code == status.HTTP_200_OK
        
        # Filter by draft status
        response = test_client.get("/api/v1/stories?status=draft")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["stories"]) == 2
        for story in data["stories"]:
            assert story["status"] == "draft"
        
        # Filter by ready status
        response = test_client.get("/api/v1/stories?status=ready")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["stories"]) == 1
        assert data["stories"][0]["status"] == "ready"

    def test_list_stories_filtering_by_story_type(self, test_client, mock_stories_storage):
        """Test story list filtering by story type."""
        # Create stories with different types
        story_types = ["user_story", "user_story", "bug_fix", "epic"]
        for i, story_type in enumerate(story_types):
            story_data = {
                "description": f"Type test story {i}",
                "story_type": story_type
            }
            response = test_client.post("/api/v1/generate-story", json=story_data)
            assert response.status_code == status.HTTP_201_CREATED
        
        # Filter by user_story
        response = test_client.get("/api/v1/stories?story_type=user_story")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["stories"]) == 2
        for story in data["stories"]:
            assert story["story_type"] == "user_story"
        
        # Filter by bug_fix
        response = test_client.get("/api/v1/stories?story_type=bug_fix")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["stories"]) == 1
        assert data["stories"][0]["story_type"] == "bug_fix"

    def test_list_stories_search(self, test_client, mock_stories_storage):
        """Test story list search functionality."""
        # Create stories with searchable content
        stories_data = [
            {"description": "User login functionality"},
            {"description": "Password reset feature"},
            {"description": "User registration form"},
            {"description": "Admin dashboard design"}
        ]
        
        for story_data in stories_data:
            response = test_client.post("/api/v1/generate-story", json=story_data)
            assert response.status_code == status.HTTP_201_CREATED
        
        # Search for "user"
        response = test_client.get("/api/v1/stories?search=user")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["stories"]) == 2  # login and registration
        
        # Search for "password"
        response = test_client.get("/api/v1/stories?search=password")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["stories"]) == 1
        assert "password" in data["stories"][0]["description"].lower()
        
        # Search for non-existent term
        response = test_client.get("/api/v1/stories?search=nonexistent")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["stories"]) == 0

    def test_list_stories_combined_filters(self, test_client, mock_stories_storage):
        """Test story list with combined filters."""
        # Create diverse stories
        stories_data = [
            {"description": "User login feature", "story_type": "user_story"},
            {"description": "Login bug fix", "story_type": "bug_fix"},
            {"description": "User registration feature", "story_type": "user_story"},
            {"description": "Database optimization", "story_type": "technical_task"}
        ]
        
        for story_data in stories_data:
            response = test_client.post("/api/v1/generate-story", json=story_data)
            assert response.status_code == status.HTTP_201_CREATED
        
        # Combined filter: search "user" and story_type "user_story"
        response = test_client.get("/api/v1/stories?search=user&story_type=user_story")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["stories"]) == 2  # Both user stories with "user" in description
        
        for story in data["stories"]:
            assert story["story_type"] == "user_story"
            assert "user" in story["description"].lower()

    def test_list_stories_pagination_validation(self, test_client):
        """Test story list pagination parameter validation."""
        # Test invalid page number
        response = test_client.get("/api/v1/stories?page=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test invalid page size
        response = test_client.get("/api/v1/stories?page_size=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test page size too large
        response = test_client.get("/api/v1/stories?page_size=101")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.integration
class TestStoryDetailEndpoint:
    """Test cases for the individual story detail endpoint."""

    def test_get_story_success(self, test_client, mock_stories_storage):
        """Test successful story retrieval."""
        # Create a story first
        story_data = {"description": "Test story for retrieval"}
        create_response = test_client.post("/api/v1/generate-story", json=story_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        created_story = create_response.json()
        
        # Retrieve the story
        response = test_client.get(f"/api/v1/stories/{created_story['id']}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert_story_response_valid(data)
        assert data["id"] == created_story["id"]
        assert data["description"] == story_data["description"]

    def test_get_story_not_found(self, test_client):
        """Test retrieving non-existent story."""
        response = test_client.get("/api/v1/stories/nonexistent-id")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        
        assert data["error"] is True
        assert "not found" in data["message"].lower()

    def test_get_story_invalid_id_format(self, test_client):
        """Test retrieving story with various ID formats."""
        # Test with different ID formats - should all work as they're treated as strings
        test_ids = ["123", "abc-def", "uuid-like-string", ""]
        
        for test_id in test_ids:
            response = test_client.get(f"/api/v1/stories/{test_id}")
            # Should return 404 since these IDs don't exist
            assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
class TestStoryUpdateEndpoint:
    """Test cases for the story update endpoint."""

    def test_update_story_success(self, test_client, mock_stories_storage):
        """Test successful story update."""
        # Create a story first
        story_data = {"description": "Original story for update testing"}
        create_response = test_client.post("/api/v1/generate-story", json=story_data)
        created_story = create_response.json()
        
        # Update the story
        update_data = {
            "title": "Updated Story Title",
            "status": "ready",
            "estimated_points": 8,
            "tags": ["updated", "testing"]
        }
        
        response = test_client.put(f"/api/v1/stories/{created_story['id']}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert_story_response_valid(data)
        assert data["id"] == created_story["id"]
        assert data["title"] == update_data["title"]
        assert data["status"] == update_data["status"]
        assert data["estimated_points"] == update_data["estimated_points"]
        assert data["tags"] == update_data["tags"]
        assert data["description"] == story_data["description"]  # Unchanged
        
        # Verify updated_at timestamp changed
        assert data["updated_at"] > created_story["updated_at"]

    def test_update_story_partial_update(self, test_client, mock_stories_storage):
        """Test partial story update."""
        # Create a story first
        story_data = {"description": "Story for partial update"}
        create_response = test_client.post("/api/v1/generate-story", json=story_data)
        created_story = create_response.json()
        
        # Partial update - only status
        update_data = {"status": "in_progress"}
        
        response = test_client.put(f"/api/v1/stories/{created_story['id']}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["status"] == "in_progress"
        # Other fields should remain unchanged
        assert data["description"] == story_data["description"]
        assert data["story_type"] == created_story["story_type"]

    def test_update_story_all_fields(self, test_client, mock_stories_storage):
        """Test updating all possible fields."""
        # Create a story first
        story_data = {"description": "Story for complete update"}
        create_response = test_client.post("/api/v1/generate-story", json=story_data)
        created_story = create_response.json()
        
        # Update all possible fields
        update_data = {
            "title": "Completely Updated Story",
            "description": "Updated description",
            "gherkin": "Feature: Updated\nScenario: Updated scenario",
            "acceptance_criteria": ["Updated criterion 1", "Updated criterion 2"],
            "status": "done",
            "estimated_points": 13,
            "tags": ["updated", "complete", "testing"]
        }
        
        response = test_client.put(f"/api/v1/stories/{created_story['id']}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        for field, value in update_data.items():
            assert data[field] == value

    def test_update_story_validation_errors(self, test_client, mock_stories_storage):
        """Test story update with validation errors."""
        # Create a story first
        story_data = {"description": "Story for validation testing"}
        create_response = test_client.post("/api/v1/generate-story", json=story_data)
        created_story = create_response.json()
        
        # Test invalid status
        response = test_client.put(f"/api/v1/stories/{created_story['id']}", json={
            "status": "invalid_status"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test invalid estimated_points (too high)
        response = test_client.put(f"/api/v1/stories/{created_story['id']}", json={
            "estimated_points": 25
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test invalid estimated_points (too low)
        response = test_client.put(f"/api/v1/stories/{created_story['id']}", json={
            "estimated_points": 0
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_story_not_found(self, test_client):
        """Test updating non-existent story."""
        update_data = {"status": "ready"}
        
        response = test_client.put("/api/v1/stories/nonexistent-id", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["error"] is True
        assert "not found" in data["message"].lower()

    def test_update_story_empty_request(self, test_client, mock_stories_storage):
        """Test updating story with empty request body."""
        # Create a story first
        story_data = {"description": "Story for empty update test"}
        create_response = test_client.post("/api/v1/generate-story", json=story_data)
        created_story = create_response.json()
        
        # Empty update
        response = test_client.put(f"/api/v1/stories/{created_story['id']}", json={})
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Should return the story unchanged except for updated_at
        assert data["description"] == story_data["description"]
        assert data["updated_at"] > created_story["updated_at"]


@pytest.mark.integration
class TestStoryDeleteEndpoint:
    """Test cases for the story delete endpoint."""

    def test_delete_story_success(self, test_client, mock_stories_storage):
        """Test successful story deletion."""
        # Create a story first
        story_data = {"description": "Story to be deleted"}
        create_response = test_client.post("/api/v1/generate-story", json=story_data)
        created_story = create_response.json()
        
        # Verify story exists
        assert len(mock_stories_storage) == 1
        assert created_story["id"] in mock_stories_storage
        
        # Delete the story
        response = test_client.delete(f"/api/v1/stories/{created_story['id']}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.content == b""  # No content for 204 response
        
        # Verify story was deleted
        assert len(mock_stories_storage) == 0
        assert created_story["id"] not in mock_stories_storage

    def test_delete_story_not_found(self, test_client):
        """Test deleting non-existent story."""
        response = test_client.delete("/api/v1/stories/nonexistent-id")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["error"] is True
        assert "not found" in data["message"].lower()

    def test_delete_story_multiple_stories(self, test_client, mock_stories_storage):
        """Test deleting one story among multiple."""
        # Create multiple stories
        story_ids = []
        for i in range(3):
            story_data = {"description": f"Story {i} for deletion test"}
            create_response = test_client.post("/api/v1/generate-story", json=story_data)
            story_ids.append(create_response.json()["id"])
        
        assert len(mock_stories_storage) == 3
        
        # Delete the middle story
        response = test_client.delete(f"/api/v1/stories/{story_ids[1]}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify only the targeted story was deleted
        assert len(mock_stories_storage) == 2
        assert story_ids[0] in mock_stories_storage
        assert story_ids[1] not in mock_stories_storage
        assert story_ids[2] in mock_stories_storage


@pytest.mark.integration
class TestEndpointAuthentication:
    """Test cases for endpoint authentication and authorization."""

    def test_endpoints_work_without_auth(self, test_client, mock_stories_storage):
        """Test that endpoints work without authentication (current behavior)."""
        # Create story without auth
        story_data = {"description": "Test story without authentication"}
        response = test_client.post("/api/v1/generate-story", json=story_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # List stories without auth
        response = test_client.get("/api/v1/stories")
        assert response.status_code == status.HTTP_200_OK

    def test_endpoints_with_auth_headers(self, test_client, auth_headers, mock_stories_storage):
        """Test that endpoints work with authentication headers."""
        # Create story with auth
        story_data = {"description": "Test story with authentication"}
        response = test_client.post("/api/v1/generate-story", json=story_data, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        
        # List stories with auth
        response = test_client.get("/api/v1/stories", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.integration
@pytest.mark.performance
class TestEndpointPerformance:
    """Performance tests for API endpoints."""

    def test_story_generation_performance(self, test_client, mock_stories_storage):
        """Test story generation endpoint performance."""
        import time
        
        story_data = {"description": "Performance test story"}
        
        start_time = time.time()
        response = test_client.post("/api/v1/generate-story", json=story_data)
        end_time = time.time()
        
        assert response.status_code == status.HTTP_201_CREATED
        request_time = end_time - start_time
        
        # Should respond quickly with mock service
        assert request_time < 1.0  # Less than 1 second

    def test_story_list_performance_with_data(self, test_client, mock_stories_storage):
        """Test story list performance with multiple stories."""
        import time
        
        # Create 50 stories
        for i in range(50):
            story_data = {"description": f"Performance test story {i}"}
            response = test_client.post("/api/v1/generate-story", json=story_data)
            assert response.status_code == status.HTTP_201_CREATED
        
        # Test list performance
        start_time = time.time()
        response = test_client.get("/api/v1/stories")
        end_time = time.time()
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["stories"]) == 50
        
        request_time = end_time - start_time
        assert request_time < 2.0  # Should list 50 stories in under 2 seconds

    def test_concurrent_endpoint_requests(self, test_client, mock_stories_storage):
        """Test concurrent requests to endpoints."""
        import concurrent.futures
        import threading
        
        def create_story(index):
            story_data = {"description": f"Concurrent test story {index}"}
            return test_client.post("/api/v1/generate-story", json=story_data)
        
        # Make 10 concurrent story creation requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_story, i) for i in range(10)]
            responses = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == status.HTTP_201_CREATED
        
        # Verify all stories were created
        list_response = test_client.get("/api/v1/stories")
        assert list_response.status_code == status.HTTP_200_OK
        data = list_response.json()
        assert len(data["stories"]) == 10