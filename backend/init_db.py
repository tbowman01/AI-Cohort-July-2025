"""
Database initialization script for AutoDevHub.

This script creates the SQLite database, tables, indexes, and full-text search
capabilities as specified in ADR-003: Database Selection (SQLite).
"""

from models import UserStory
from database import init_database, get_database_info, vacuum_database
import asyncio
import logging
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def create_sample_data():
    """
    Create sample user stories for testing and demonstration.

    This function creates a few sample user stories to demonstrate
    the database functionality and provide test data.
    """
    from database import async_session_maker

    sample_stories = [
        {
            "feature_description": (
                "As a user, I want to be able to login to my account so that I can "
                "access my personal dashboard"
            ),
            "gherkin_output": """Feature: User Authentication
  As a user
  I want to be able to login to my account
  So that I can access my personal dashboard

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter valid username and password
    And I click the login button
    Then I should be redirected to my dashboard
    And I should see a welcome message

  Scenario: Failed login with invalid credentials
    Given I am on the login page
    When I enter invalid username or password
    And I click the login button
    Then I should see an error message
    And I should remain on the login page""",
            "metadata": {
                "ai_model": "gpt-4",
                "processing_time_ms": 1250,
                "confidence_score": 0.95,
                "sample_data": True,
            },
        },
        {
            "feature_description": (
                "As a project manager, I want to create user stories so that I can "
                "plan development sprints"
            ),
            "gherkin_output": """Feature: User Story Creation
  As a project manager
  I want to create user stories
  So that I can plan development sprints

  Scenario: Create a new user story
    Given I am logged in as a project manager
    When I navigate to the story creation page
    And I enter a feature description
    And I click the generate button
    Then a Gherkin scenario should be generated
    And the story should be saved to the database

  Scenario: Edit an existing user story
    Given I have an existing user story
    When I click the edit button
    And I modify the feature description
    And I save the changes
    Then the story should be updated
    And the timestamp should reflect the change""",
            "metadata": {
                "ai_model": "gpt-4",
                "processing_time_ms": 1850,
                "confidence_score": 0.92,
                "sample_data": True,
            },
        },
        {
            "feature_description": (
                "As an API user, I want to search through user stories so that I "
                "can find relevant examples"
            ),
            "gherkin_output": """Feature: User Story Search
  As an API user
  I want to search through user stories
  So that I can find relevant examples

  Scenario: Search by keyword
    Given there are multiple user stories in the database
    When I perform a search with keyword "login"
    Then I should receive stories containing "login"
    And the results should be ranked by relevance

  Scenario: Paginated search results
    Given there are many matching user stories
    When I perform a search with pagination
    Then I should receive a limited number of results
    And I should be able to request the next page""",
            "metadata": {
                "ai_model": "gpt-4",
                "processing_time_ms": 2100,
                "confidence_score": 0.88,
                "sample_data": True,
            },
        },
    ]

    async with async_session_maker() as session:
        try:
            for story_data in sample_stories:
                story = UserStory(
                    feature_description=story_data["feature_description"],
                    gherkin_output=story_data["gherkin_output"],
                )
                story.set_metadata(story_data["metadata"])
                session.add(story)

            await session.commit()
            logger.info(f"Created {len(sample_stories)} sample user stories")

        except Exception as e:
            await session.rollback()
            logger.error(f"Failed to create sample data: {e}")
            raise


async def main():
    """
    Main function to initialize the database.
    """
    logger.info("Starting database initialization...")

    try:
        # Initialize database (create tables, indexes, FTS)
        logger.info("Creating database tables and indexes...")
        await init_database()
        logger.info("Database tables created successfully")

        # Get database info for verification
        db_info = get_database_info()
        logger.info(f"Database info: {db_info}")

        # Create sample data if requested
        if (
            "--sample-data" in sys.argv
            or os.getenv("CREATE_SAMPLE_DATA", "false").lower() == "true"
        ):
            logger.info("Creating sample data...")
            await create_sample_data()
            logger.info("Sample data created successfully")

        # Perform initial vacuum for optimal performance
        logger.info("Performing initial database vacuum...")
        await vacuum_database()
        logger.info("Database vacuum completed")

        # Final database info
        final_info = get_database_info()
        logger.info(f"Final database info: {final_info}")

        logger.info("Database initialization completed successfully!")

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Check for help argument
    if "--help" in sys.argv or "-h" in sys.argv:
        print(
            """
AutoDevHub Database Initialization Script

Usage:
    python init_db.py [options]

Options:
    --sample-data    Create sample user stories for testing
    --help, -h       Show this help message

Environment Variables:
    DATABASE_FILE           Path to SQLite database file (default:
                            autodevhub.db)
    CREATE_SAMPLE_DATA      Set to 'true' to create sample data
                            (default: false)
    DEBUG                   Set to 'true' to enable SQL query logging
                            (default: false)

Examples:
    python init_db.py                    # Initialize database only
    python init_db.py --sample-data      # Initialize database with
                                         # sample data
    CREATE_SAMPLE_DATA=true python init_db.py  # Use environment variable
        """
        )
        sys.exit(0)

    # Run the main function
    asyncio.run(main())
