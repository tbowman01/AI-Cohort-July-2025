"""
SQLAlchemy models for AutoDevHub.

Based on ADR-003: Database Selection (SQLite)
Schema implementation for user stories and sessions.
"""

import json
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserStory(Base):
    """
    User story model for storing feature descriptions and generated Gherkin scenarios.
    
    Based on ADR-003 schema:
    CREATE TABLE user_stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feature_description TEXT NOT NULL,
        gherkin_output TEXT NOT NULL,
        metadata TEXT, -- JSON as TEXT in SQLite
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    __tablename__ = "user_stories"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Core data fields
    feature_description: Mapped[str] = mapped_column(Text, nullable=False, doc="User-provided feature description")
    gherkin_output: Mapped[str] = mapped_column(Text, nullable=False, doc="AI-generated Gherkin scenarios")
    
    # Metadata as JSON stored as TEXT (SQLite approach)  
    story_metadata: Mapped[Optional[str]] = mapped_column(Text, nullable=True, doc="JSON metadata as TEXT")
    
    # Timestamps with automatic updates
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Story creation timestamp"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Story last update timestamp"
    )
    
    def __repr__(self) -> str:
        """String representation of UserStory."""
        return f"<UserStory(id={self.id}, created_at={self.created_at})>"
    
    def set_metadata(self, metadata_dict: Dict[str, Any]) -> None:
        """
        Set metadata from dictionary (converts to JSON string for SQLite).
        
        Args:
            metadata_dict: Dictionary to store as JSON metadata
        """
        self.story_metadata = json.dumps(metadata_dict) if metadata_dict else None
    
    def get_metadata(self) -> Optional[Dict[str, Any]]:
        """
        Get metadata as dictionary (parses JSON string from SQLite).
        
        Returns:
            Dictionary from JSON metadata or None if no metadata
        """
        if self.story_metadata:
            try:
                return json.loads(self.story_metadata)
            except json.JSONDecodeError:
                return None
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary for API responses.
        
        Returns:
            Dictionary representation of the user story
        """
        return {
            "id": self.id,
            "feature_description": self.feature_description,
            "gherkin_output": self.gherkin_output,
            "metadata": self.get_metadata(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Session(Base):
    """
    Session model for storing user sessions and preferences.
    
    Based on ADR-003 future enhancement schema:
    CREATE TABLE sessions (
        id TEXT PRIMARY KEY, -- UUID as TEXT
        user_id TEXT,
        preferences TEXT, -- JSON as TEXT
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    __tablename__ = "sessions"
    
    # Primary key as UUID string
    id: Mapped[str] = mapped_column(
        String, 
        primary_key=True, 
        default=lambda: str(uuid4()),
        doc="Session UUID as string"
    )
    
    # User identification (for future multi-user support)
    user_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, doc="User identifier")
    
    # User preferences as JSON stored as TEXT
    preferences: Mapped[Optional[str]] = mapped_column(Text, nullable=True, doc="User preferences as JSON")
    
    # Creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Session creation timestamp"
    )
    
    def __repr__(self) -> str:
        """String representation of Session."""
        return f"<Session(id={self.id}, user_id={self.user_id}, created_at={self.created_at})>"
    
    def set_preferences(self, preferences_dict: Dict[str, Any]) -> None:
        """
        Set preferences from dictionary (converts to JSON string for SQLite).
        
        Args:
            preferences_dict: Dictionary to store as JSON preferences
        """
        self.preferences = json.dumps(preferences_dict) if preferences_dict else None
    
    def get_preferences(self) -> Optional[Dict[str, Any]]:
        """
        Get preferences as dictionary (parses JSON string from SQLite).
        
        Returns:
            Dictionary from JSON preferences or None if no preferences
        """
        if self.preferences:
            try:
                return json.loads(self.preferences)
            except json.JSONDecodeError:
                return None
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary for API responses.
        
        Returns:
            Dictionary representation of the session
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "preferences": self.get_preferences(),
            "created_at": self.created_at.isoformat(),
        }


# Additional utility functions for database operations

async def search_user_stories(
    session, 
    query: str, 
    limit: int = 10, 
    offset: int = 0
) -> list[UserStory]:
    """
    Search user stories using SQLite FTS5 full-text search.
    
    Args:
        session: Database session
        query: Search query string
        limit: Maximum number of results
        offset: Result offset for pagination
        
    Returns:
        List of matching UserStory objects
    """
    from sqlalchemy import text
    
    # Use FTS5 virtual table for full-text search
    fts_query = text("""
        SELECT user_stories.* 
        FROM user_stories
        JOIN user_stories_fts ON user_stories.id = user_stories_fts.rowid
        WHERE user_stories_fts MATCH :query
        ORDER BY rank
        LIMIT :limit OFFSET :offset
    """)
    
    result = await session.execute(
        fts_query, 
        {"query": query, "limit": limit, "offset": offset}
    )
    
    return [UserStory(**row._asdict()) for row in result.fetchall()]


def get_user_story_stats(session) -> Dict[str, Any]:
    """
    Get statistics about user stories in the database.
    
    Args:
        session: Database session
        
    Returns:
        Dictionary with statistics
    """
    from sqlalchemy import func, text
    
    # Get basic counts and dates
    stats_query = text("""
        SELECT 
            COUNT(*) as total_stories,
            MIN(created_at) as oldest_story,
            MAX(created_at) as newest_story,
            AVG(LENGTH(feature_description)) as avg_feature_length,
            AVG(LENGTH(gherkin_output)) as avg_gherkin_length
        FROM user_stories
    """)
    
    result = session.execute(stats_query).fetchone()
    
    return {
        "total_stories": result.total_stories,
        "oldest_story": result.oldest_story.isoformat() if result.oldest_story else None,
        "newest_story": result.newest_story.isoformat() if result.newest_story else None,
        "avg_feature_description_length": round(result.avg_feature_length or 0, 2),
        "avg_gherkin_output_length": round(result.avg_gherkin_length or 0, 2),
    }