"""
Test configuration and fixtures for AutoDevHub backend tests.

This module provides pytest fixtures and configuration for testing the
FastAPI application,
database models, and dependencies with proper isolation and cleanup.
"""

import asyncio
import os
import tempfile
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.orm import Session, sessionmaker

# Import application components
from main import app
from config import get_testing_settings
from database import Base, get_db
from dependencies import get_database_session, get_ai_service, AIServiceManager
from models import UserStory, Session as SessionModel


# Test configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_settings():
    """Get test-specific settings."""
    return get_testing_settings()


@pytest.fixture(scope="session")
def temp_db_file():
    """Create a temporary database file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        temp_db_path = tmp_file.name
    yield temp_db_path
    # Cleanup
    if os.path.exists(temp_db_path):
        os.unlink(temp_db_path)


@pytest.fixture(scope="session")
def test_engine(temp_db_file):
    """Create a test database engine."""
    database_url = f"sqlite:///{temp_db_file}"
    engine = create_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False}
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
async def async_test_engine(temp_db_file):
    """Create an async test database engine."""
    database_url = f"sqlite+aiosqlite:///{temp_db_file}"
    engine = create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True
    )

    # Initialize database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
def db_session(test_engine) -> Generator[Session, None, None]:
    """Create a database session for testing."""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

    with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def async_db_session(
        async_test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create an async database session for testing."""
    AsyncTestingSessionLocal = async_sessionmaker(
        async_test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with AsyncTestingSessionLocal() as session:
        yield session


@pytest.fixture
def override_get_db(db_session):
    """Override the get_database_session dependency for testing."""
    def _override_get_db():
        yield db_session
    return _override_get_db


@pytest.fixture
def override_async_get_db(async_db_session):
    """Override the async get_db dependency for testing."""
    async def _override_async_get_db():
        yield async_db_session
    return _override_async_get_db


@pytest.fixture
def mock_ai_service():
    """Create a mock AI service for testing."""
    mock_service = MagicMock(spec=AIServiceManager)

    # Mock the generate_story method
    async def mock_generate_story(description: str) -> dict:
        return {
            "title": f"Test Story: {description[:30]}...",
            "description": description,
            "gherkin": f"""
Feature: Test Feature for {description[:50]}

  Scenario: Basic test scenario
    Given the system is ready
    When I perform the test action
    Then I should see the expected test result
            """.strip(),
            "acceptance_criteria": [
                "Test criterion 1",
                "Test criterion 2",
                "Test criterion 3"
            ]
        }

    mock_service.generate_story = AsyncMock(side_effect=mock_generate_story)
    return mock_service


@pytest.fixture
def override_ai_service(mock_ai_service):
    """Override the AI service dependency for testing."""
    async def _override_ai_service():
        return mock_ai_service
    return _override_ai_service


@pytest.fixture
def test_client(override_get_db, override_ai_service):
    """Create a test client with overridden dependencies."""
    # Override dependencies
    app.dependency_overrides[get_database_session] = override_get_db
    app.dependency_overrides[get_ai_service] = override_ai_service

    with TestClient(app) as client:
        yield client

    # Clear overrides
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_test_client(override_async_get_db, override_ai_service):
    """Create an async test client with overridden dependencies."""
    # Override dependencies
    app.dependency_overrides[get_db] = override_async_get_db
    app.dependency_overrides[get_ai_service] = override_ai_service

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

    # Clear overrides
    app.dependency_overrides.clear()


# Test data fixtures
@pytest.fixture
def sample_story_data():
    """Sample story data for testing."""
    return {
        "description": (\n            "As a user, I want to create a new account so I can access the system"\n        ),
        "project_context": "User management system",
        "story_type": "user_story",
        "complexity": "medium"}


@pytest.fixture
def sample_user_story(db_session, sample_story_data) -> UserStory:
    """Create a sample UserStory in the database."""
    story = UserStory(
        feature_description=sample_story_data["description"],
        gherkin_output="""
Feature: User Account Creation

  Scenario: Successful account creation
    Given I am on the registration page
    When I fill in valid account details
    And I submit the registration form
    Then I should see a success message
    And I should receive a confirmation email
        """.strip()
    )
    story.set_metadata({
        "project_context": sample_story_data["project_context"],
        "story_type": sample_story_data["story_type"],
        "complexity": sample_story_data["complexity"]
    })

    db_session.add(story)
    db_session.commit()
    db_session.refresh(story)
    return story


@pytest.fixture
def sample_session_data():
    """Sample session data for testing."""
    return {
        "user_id": "test-user-123",
        "preferences": {
            "theme": "dark",
            "language": "en",
            "notifications": True,
            "story_templates": ["user_story", "bug_fix"]
        }
    }


@pytest.fixture
def sample_session(db_session, sample_session_data) -> SessionModel:
    """Create a sample Session in the database."""
    session = SessionModel(user_id=sample_session_data["user_id"])
    session.set_preferences(sample_session_data["preferences"])

    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session


@pytest.fixture
def mock_stories_storage():
    """Mock the in-memory stories storage for testing."""
    from routers.stories import STORIES_STORAGE
    original_storage = STORIES_STORAGE.copy()
    STORIES_STORAGE.clear()

    yield STORIES_STORAGE

    # Restore original storage
    STORIES_STORAGE.clear()
    STORIES_STORAGE.update(original_storage)


# Performance and load testing fixtures
@pytest.fixture
def large_dataset_stories(db_session):
    """Create a large dataset of stories for performance testing."""
    stories = []
    for i in range(100):
        story = UserStory(
            feature_description=f"Test feature description {i}",
            gherkin_output=f"Feature: Test Feature {i}\n\nScenario: Test scenario {i}\n  Given test condition {i}\n  When test action {i}\n  Then test result {i}"
        )
        story.set_metadata({
            "story_type": "user_story" if i % 2 == 0 else "bug_fix",
            "complexity": ["low", "medium", "high"][i % 3],
            "test_index": i
        })
        stories.append(story)

    db_session.add_all(stories)
    db_session.commit()
    return stories


# Error simulation fixtures
@pytest.fixture
def simulate_db_error(monkeypatch):
    """Simulate database connection errors."""
    def mock_db_session():
        raise Exception("Database connection failed")

    def enable_error():
        monkeypatch.setattr(
            "dependencies.get_database_session",
            mock_db_session)

    def disable_error():
        monkeypatch.undo()

    return {"enable": enable_error, "disable": disable_error}


@pytest.fixture
def simulate_ai_service_error(mock_ai_service):
    """Simulate AI service errors."""
    async def mock_generate_story_error(description: str):
        raise Exception("AI service unavailable")

    def enable_error():
        mock_ai_service.generate_story = AsyncMock(
            side_effect=mock_generate_story_error)

    def disable_error():
        async def mock_generate_story_success(description: str) -> dict:
            return {
                "title": f"Test Story: {description[:30]}...",
                "description": description,
                "gherkin": "Feature: Test\nScenario: Test\n  Given test\n  When test\n  Then test",
                "acceptance_criteria": ["Test criterion"]
            }
        mock_ai_service.generate_story = AsyncMock(
            side_effect=mock_generate_story_success)

    return {"enable": enable_error, "disable": disable_error}


# Authentication fixtures
@pytest.fixture
def mock_authenticated_user():
    """Mock authenticated user data."""
    return {
        "id": "test-user-123",
        "username": "testuser",
        "email": "test@example.com"
    }


@pytest.fixture
def auth_headers():
    """Authentication headers for testing."""
    return {"Authorization": "Bearer test-token-123"}


# Database cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_database(db_session):
    """Automatically clean up database after each test."""
    yield
    # Clean up all test data (only if tables exist)
    try:
        db_session.query(UserStory).delete()
        db_session.query(SessionModel).delete()
        db_session.commit()
    except Exception:
        # Tables might not exist in all tests, ignore cleanup errors
        db_session.rollback()


# Test environment markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "database: mark test as requiring database"
    )
    config.addinivalue_line(
        "markers", "ai_service: mark test as requiring AI service"
    )


# Utility functions for tests
def assert_story_response_valid(response_data: dict):
    """Assert that a story response has all required fields."""
    required_fields = [
        "id", "title", "description", "gherkin", "acceptance_criteria",
        "story_type", "complexity", "status", "created_at", "updated_at"
    ]
    for field in required_fields:
        assert field in response_data, f"Missing required field: {field}"
        assert response_data[field] is not None, f"Field {field} is None"


def assert_story_list_response_valid(response_data: dict):
    """Assert that a story list response has all required fields."""
    required_fields = ["stories", "total", "page", "page_size", "has_next"]
    for field in required_fields:
        assert field in response_data, f"Missing required field: {field}"

    assert isinstance(response_data["stories"],
                      list), "stories should be a list"
    assert isinstance(response_data["total"],
                      int), "total should be an integer"
    assert isinstance(response_data["page"], int), "page should be an integer"
    assert isinstance(response_data["page_size"],
                      int), "page_size should be an integer"
    assert isinstance(response_data["has_next"],
                      bool), "has_next should be a boolean"
