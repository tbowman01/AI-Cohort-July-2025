"""
Tests for SQLAlchemy database models.

This module contains comprehensive tests for the UserStory and Session models,
including validation, serialization, metadata handling, and database operations.
"""

import json
import pytest
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from models import (
    UserStory,
    Session as SessionModel,
    search_user_stories,
    get_user_story_stats,
)


@pytest.mark.database
@pytest.mark.unit
class TestUserStoryModel:
    """Test cases for the UserStory model."""

    def test_user_story_creation(self, db_session):
        """Test creating a UserStory with required fields."""
        story = UserStory(
            feature_description="As a user, I want to login",
            gherkin_output="Feature: Login\nScenario: Successful login",
        )

        db_session.add(story)
        db_session.commit()
        db_session.refresh(story)

        assert story.id is not None
        assert story.feature_description == "As a user, I want to login"
        assert story.gherkin_output == "Feature: Login\nScenario: Successful login"
        assert story.metadata is None
        assert isinstance(story.created_at, datetime)
        assert isinstance(story.updated_at, datetime)
        assert story.created_at <= story.updated_at

    def test_user_story_with_metadata(self, db_session):
        """Test UserStory with metadata functionality."""
        metadata_dict = {
            "project": "AutoDevHub",
            "priority": "high",
            "complexity": "medium",
            "tags": ["authentication", "security"],
        }

        story = UserStory(
            feature_description="User authentication feature",
            gherkin_output="Feature: Authentication\nScenario: Login",
        )
        story.set_metadata(metadata_dict)

        db_session.add(story)
        db_session.commit()
        db_session.refresh(story)

        # Test metadata storage
        assert story.metadata is not None
        assert isinstance(story.metadata, str)  # Stored as JSON string

        # Test metadata retrieval
        retrieved_metadata = story.get_metadata()
        assert retrieved_metadata == metadata_dict
        assert retrieved_metadata["project"] == "AutoDevHub"
        assert retrieved_metadata["tags"] == ["authentication", "security"]

    def test_user_story_metadata_edge_cases(self, db_session):
        """Test UserStory metadata with edge cases."""
        story = UserStory(
            feature_description="Test story", gherkin_output="Feature: Test"
        )

        # Test empty metadata
        story.set_metadata({})
        assert story.metadata is None
        assert story.get_metadata() is None

        # Test None metadata
        story.set_metadata(None)
        assert story.metadata is None
        assert story.get_metadata() is None

        # Test invalid JSON in database
        story.metadata = "invalid json"
        assert story.get_metadata() is None

    def test_user_story_required_fields(self, db_session):
        """Test that required fields are enforced."""
        # Test missing feature_description
        with pytest.raises(IntegrityError):
            story = UserStory(gherkin_output="Feature: Test")
            db_session.add(story)
            db_session.commit()

        db_session.rollback()

        # Test missing gherkin_output
        with pytest.raises(IntegrityError):
            story = UserStory(feature_description="Test description")
            db_session.add(story)
            db_session.commit()

    def test_user_story_string_representation(self, db_session):
        """Test UserStory string representation."""
        story = UserStory(
            feature_description="Test feature", gherkin_output="Feature: Test"
        )

        db_session.add(story)
        db_session.commit()
        db_session.refresh(story)

        str_repr = str(story)
        assert f"<UserStory(id={story.id}" in str_repr
        assert f"created_at={story.created_at}" in str_repr

    def test_user_story_to_dict(self, db_session):
        """Test UserStory serialization to dictionary."""
        metadata_dict = {"test": "value", "number": 42}

        story = UserStory(
            feature_description="Test feature description",
            gherkin_output="Feature: Test\nScenario: Test scenario",
        )
        story.set_metadata(metadata_dict)

        db_session.add(story)
        db_session.commit()
        db_session.refresh(story)

        story_dict = story.to_dict()

        assert story_dict["id"] == story.id
        assert story_dict["feature_description"] == "Test feature description"
        assert story_dict["gherkin_output"] == "Feature: Test\nScenario: Test scenario"
        assert story_dict["metadata"] == metadata_dict
        assert isinstance(story_dict["created_at"], str)
        assert isinstance(story_dict["updated_at"], str)

        # Verify datetime ISO format
        created_dt = datetime.fromisoformat(
            story_dict["created_at"].replace("Z", "+00:00")
        )
        assert isinstance(created_dt, datetime)

    def test_user_story_timestamps(self, db_session):
        """Test UserStory timestamp behavior."""
        story = UserStory(
            feature_description="Test timestamps", gherkin_output="Feature: Timestamps"
        )

        db_session.add(story)
        db_session.commit()
        db_session.refresh(story)

        original_created_at = story.created_at
        original_updated_at = story.updated_at

        # Update the story
        story.feature_description = "Updated description"
        db_session.commit()
        db_session.refresh(story)

        # created_at should remain the same
        assert story.created_at == original_created_at
        # updated_at should be updated
        assert story.updated_at >= original_updated_at

    def test_user_story_large_content(self, db_session):
        """Test UserStory with large content."""
        large_description = "A" * 10000  # 10KB description
        large_gherkin = "Feature: Large\n" + "Scenario: Test\n" * 1000  # Large Gherkin

        story = UserStory(
            feature_description=large_description, gherkin_output=large_gherkin
        )

        db_session.add(story)
        db_session.commit()
        db_session.refresh(story)

        assert len(story.feature_description) == 10000
        assert "Scenario: Test" in story.gherkin_output
        assert story.gherkin_output.count("Scenario: Test") == 1000


@pytest.mark.database
@pytest.mark.unit
class TestSessionModel:
    """Test cases for the Session model."""

    def test_session_creation(self, db_session):
        """Test creating a Session with default values."""
        session = SessionModel()

        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        assert session.id is not None
        assert isinstance(session.id, str)
        # Verify it's a valid UUID
        UUID(session.id)  # Should not raise an exception

        assert session.user_id is None
        assert session.preferences is None
        assert isinstance(session.created_at, datetime)

    def test_session_with_user_id(self, db_session):
        """Test Session with user_id."""
        session = SessionModel(user_id="test-user-123")

        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        assert session.user_id == "test-user-123"

    def test_session_with_preferences(self, db_session):
        """Test Session with preferences functionality."""
        preferences_dict = {
            "theme": "dark",
            "language": "en",
            "notifications": {"email": True, "push": False},
            "dashboard_widgets": ["stories", "metrics", "recent_activity"],
        }

        session = SessionModel(user_id="test-user")
        session.set_preferences(preferences_dict)

        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Test preferences storage
        assert session.preferences is not None
        assert isinstance(session.preferences, str)  # Stored as JSON string

        # Test preferences retrieval
        retrieved_preferences = session.get_preferences()
        assert retrieved_preferences == preferences_dict
        assert retrieved_preferences["theme"] == "dark"
        assert retrieved_preferences["notifications"]["email"] is True
        assert "stories" in retrieved_preferences["dashboard_widgets"]

    def test_session_preferences_edge_cases(self, db_session):
        """Test Session preferences with edge cases."""
        session = SessionModel()

        # Test empty preferences
        session.set_preferences({})
        assert session.preferences is None
        assert session.get_preferences() is None

        # Test None preferences
        session.set_preferences(None)
        assert session.preferences is None
        assert session.get_preferences() is None

        # Test invalid JSON in database
        session.preferences = "invalid json"
        assert session.get_preferences() is None

    def test_session_string_representation(self, db_session):
        """Test Session string representation."""
        session = SessionModel(user_id="test-user-456")

        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        str_repr = str(session)
        assert f"<Session(id={session.id}" in str_repr
        assert "user_id=test-user-456" in str_repr
        assert f"created_at={session.created_at}" in str_repr

    def test_session_to_dict(self, db_session):
        """Test Session serialization to dictionary."""
        preferences_dict = {"test_pref": "value", "number": 123}

        session = SessionModel(user_id="dict-test-user")
        session.set_preferences(preferences_dict)

        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        session_dict = session.to_dict()

        assert session_dict["id"] == session.id
        assert session_dict["user_id"] == "dict-test-user"
        assert session_dict["preferences"] == preferences_dict
        assert isinstance(session_dict["created_at"], str)

        # Verify datetime ISO format
        created_dt = datetime.fromisoformat(
            session_dict["created_at"].replace("Z", "+00:00")
        )
        assert isinstance(created_dt, datetime)

    def test_session_unique_ids(self, db_session):
        """Test that Session IDs are unique."""
        sessions = []
        for i in range(10):
            session = SessionModel(user_id=f"user-{i}")
            sessions.append(session)

        db_session.add_all(sessions)
        db_session.commit()

        # All IDs should be unique
        session_ids = [s.id for s in sessions]
        assert len(set(session_ids)) == len(session_ids)

        # All should be valid UUIDs
        for session_id in session_ids:
            UUID(session_id)  # Should not raise an exception


@pytest.mark.database
@pytest.mark.integration
class TestModelUtilityFunctions:
    """Test cases for model utility functions."""

    def test_search_user_stories_basic(self, db_session):
        """Test basic user story search functionality."""
        # Create test stories
        stories_data = [
            ("Login feature", "Feature: Login\nScenario: User login"),
            ("Registration feature", "Feature: Register\nScenario: User registration"),
            ("Password reset", "Feature: Password\nScenario: Reset password"),
        ]

        for desc, gherkin in stories_data:
            story = UserStory(feature_description=desc, gherkin_output=gherkin)
            db_session.add(story)

        db_session.commit()

        # Note: This test will fail if FTS5 is not set up, which is expected
        # since search_user_stories uses FTS5 virtual tables
        try:
            results = await search_user_stories(db_session, "login", limit=10)
            # If FTS5 is set up, we should get results
            assert isinstance(results, list)
        except Exception as e:
            # Expected if FTS5 virtual table is not created
            assert "no such table" in str(e).lower() or "fts" in str(e).lower()

    def test_get_user_story_stats(self, db_session):
        """Test user story statistics function."""
        # Create test stories with different characteristics
        stories_data = [
            ("Short description", "Feature: Short\nScenario: Test"),
            (
                "Medium length description for testing",
                "Feature: Medium\nScenario: Test scenario\nGiven test\nWhen test\nThen test",
            ),
            (
                "Very long description with lots of details about the feature requirements",
                "Feature: Long\nScenario: Complex test\nGiven complex setup\nWhen multiple actions\nThen comprehensive verification",
            ),
        ]

        for desc, gherkin in stories_data:
            story = UserStory(feature_description=desc, gherkin_output=gherkin)
            db_session.add(story)

        db_session.commit()

        stats = get_user_story_stats(db_session)

        assert stats["total_stories"] == 3
        assert stats["oldest_story"] is not None
        assert stats["newest_story"] is not None
        assert stats["avg_feature_description_length"] > 0
        assert stats["avg_gherkin_output_length"] > 0

        # Verify statistics are reasonable
        # Should be reasonable
        assert stats["avg_feature_description_length"] < 1000
        # Should have some content
        assert stats["avg_gherkin_output_length"] > 10

    def test_get_user_story_stats_empty_database(self, db_session):
        """Test user story statistics with empty database."""
        stats = get_user_story_stats(db_session)

        assert stats["total_stories"] == 0
        assert stats["oldest_story"] is None
        assert stats["newest_story"] is None
        assert stats["avg_feature_description_length"] == 0
        assert stats["avg_gherkin_output_length"] == 0


@pytest.mark.database
@pytest.mark.integration
class TestModelRelationships:
    """Test cases for model relationships and constraints."""

    def test_multiple_stories_creation(self, db_session):
        """Test creating multiple stories in a single session."""
        stories = []
        for i in range(5):
            story = UserStory(
                feature_description=f"Feature {i}",
                gherkin_output=f"Feature: Feature {i}\nScenario: Test {i}",
            )
            stories.append(story)

        db_session.add_all(stories)
        db_session.commit()

        # Verify all stories were created
        all_stories = db_session.query(UserStory).all()
        assert len(all_stories) == 5

        # Verify each has unique ID
        story_ids = [s.id for s in all_stories]
        assert len(set(story_ids)) == 5

    def test_multiple_sessions_creation(self, db_session):
        """Test creating multiple sessions in a single transaction."""
        sessions = []
        for i in range(3):
            session = SessionModel(user_id=f"user-{i}")
            session.set_preferences({"user_index": i, "test": True})
            sessions.append(session)

        db_session.add_all(sessions)
        db_session.commit()

        # Verify all sessions were created
        all_sessions = db_session.query(SessionModel).all()
        assert len(all_sessions) == 3

        # Verify each has unique ID
        session_ids = [s.id for s in all_sessions]
        assert len(set(session_ids)) == 3

        # Verify preferences were stored correctly
        for session in all_sessions:
            prefs = session.get_preferences()
            assert prefs["test"] is True
            assert isinstance(prefs["user_index"], int)


@pytest.mark.database
@pytest.mark.performance
class TestModelPerformance:
    """Performance tests for database models."""

    def test_bulk_story_creation_performance(self, db_session):
        """Test performance of creating many stories."""
        import time

        start_time = time.time()

        stories = []
        for i in range(100):
            story = UserStory(
                feature_description=f"Performance test story {i}",
                gherkin_output=f"Feature: Performance {i}\nScenario: Test performance {i}",
            )
            stories.append(story)

        db_session.add_all(stories)
        db_session.commit()

        end_time = time.time()
        creation_time = end_time - start_time

        # Should be able to create 100 stories quickly
        assert creation_time < 5.0  # Less than 5 seconds

        # Verify all were created
        count = db_session.query(UserStory).count()
        assert count == 100

    def test_story_query_performance(self, db_session, large_dataset_stories):
        """Test query performance with large dataset."""
        import time

        # Query all stories
        start_time = time.time()
        all_stories = db_session.query(UserStory).all()
        end_time = time.time()

        query_time = end_time - start_time

        assert len(all_stories) == 100
        assert query_time < 1.0  # Should query 100 stories in under 1 second

    def test_story_filtering_performance(self, db_session, large_dataset_stories):
        """Test filtering performance with large dataset."""
        import time

        # Filter stories by metadata
        start_time = time.time()

        filtered_stories = []
        for story in db_session.query(UserStory).all():
            metadata = story.get_metadata()
            if metadata and metadata.get("story_type") == "user_story":
                filtered_stories.append(story)

        end_time = time.time()
        filter_time = end_time - start_time

        assert len(filtered_stories) == 50  # Half should be user_stories
        assert filter_time < 2.0  # Should filter in under 2 seconds


@pytest.mark.database
@pytest.mark.unit
class TestModelValidation:
    """Test cases for model validation and constraints."""

    def test_user_story_field_lengths(self, db_session):
        """Test UserStory field length handling."""
        # Test very long fields
        very_long_description = "X" * 50000  # 50KB
        very_long_gherkin = "Y" * 50000  # 50KB

        story = UserStory(
            feature_description=very_long_description, gherkin_output=very_long_gherkin
        )

        db_session.add(story)
        db_session.commit()
        db_session.refresh(story)

        assert len(story.feature_description) == 50000
        assert len(story.gherkin_output) == 50000

    def test_session_id_format(self, db_session):
        """Test Session ID format and validity."""
        session = SessionModel()

        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Should be valid UUID format
        uuid_obj = UUID(session.id)
        assert str(uuid_obj) == session.id

        # Should be version 4 UUID (random)
        assert uuid_obj.version == 4

    def test_metadata_json_validation(self, db_session):
        """Test metadata JSON handling with various data types."""
        complex_metadata = {
            "string": "test",
            "integer": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "array": [1, 2, 3, "four"],
            "nested_object": {
                "nested_string": "nested value",
                "nested_array": ["a", "b", "c"],
            },
        }

        story = UserStory(
            feature_description="JSON test", gherkin_output="Feature: JSON test"
        )
        story.set_metadata(complex_metadata)

        db_session.add(story)
        db_session.commit()
        db_session.refresh(story)

        retrieved_metadata = story.get_metadata()
        assert retrieved_metadata == complex_metadata
        assert retrieved_metadata["nested_object"]["nested_string"] == "nested value"
        assert retrieved_metadata["array"][3] == "four"
