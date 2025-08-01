"""
SQLite database connection and setup for AutoDevHub.

Based on ADR-003: Database Selection (SQLite)
- Zero-configuration SQLite database
- WAL mode for concurrent reads
- Async SQLAlchemy support
- Connection pooling
"""

import os
import sqlite3
from typing import AsyncGenerator

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


# Database configuration
DATABASE_FILE = os.getenv("DATABASE_FILE", "autodevhub.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE}"

# Create async engine with SQLite optimizations
engine = create_async_engine(
    DATABASE_URL,
    echo=bool(os.getenv("DEBUG", False)),  # Log SQL queries in debug mode
    future=True,
    pool_pre_ping=True,  # Validate connections before use
    pool_recycle=300,  # Recycle connections every 5 minutes
)

# Create session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Set SQLite pragmas for optimal performance and data integrity.

    Based on ADR-003 implementation notes:
    - WAL mode for better concurrent read performance
    - Foreign key enforcement
    - JSON support optimization
    """
    cursor = dbapi_connection.cursor()

    # Enable WAL mode for better concurrent performance
    cursor.execute("PRAGMA journal_mode=WAL")

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys=ON")

    # Optimize for better performance
    # Faster than FULL, safer than OFF
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=10000")  # 10MB cache
    # Use memory for temporary tables
    cursor.execute("PRAGMA temp_store=memory")

    # Enable automatic index creation for JSON queries
    cursor.execute("PRAGMA automatic_index=ON")

    cursor.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.

    Yields:
        AsyncSession: Database session
    """
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_database():
    """
    Initialize the database by creating all tables.

    This function should be called on application startup.
    """
    async with engine.begin() as conn:
        # Import models to ensure they're registered with Base.metadata
        from .models import UserStory, Session  # noqa: F401

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

        # Create indexes for performance (based on ADR-003 notes)
        await conn.execute(
            text(
                """
            CREATE INDEX IF NOT EXISTS idx_user_stories_created_at
            ON user_stories(created_at DESC)
        """
            )
        )

        await conn.execute(
            text(
                """
            CREATE INDEX IF NOT EXISTS idx_user_stories_updated_at
            ON user_stories(updated_at DESC)
        """
            )
        )

        # Enable FTS5 full-text search on feature descriptions and Gherkin
        # output
        await conn.execute(
            text(
                """
            CREATE VIRTUAL TABLE IF NOT EXISTS user_stories_fts USING fts5(
                feature_description,
                gherkin_output,
                content='user_stories',
                content_rowid='id'
            )
        """
            )
        )

        # Create triggers to keep FTS index updated
        await conn.execute(
            text(
                """
            CREATE TRIGGER IF NOT EXISTS user_stories_fts_insert AFTER INSERT ON user_stories
            BEGIN
                INSERT INTO user_stories_fts(rowid, feature_description, gherkin_output)
                VALUES (new.id, new.feature_description, new.gherkin_output);
            END
        """
            )
        )

        await conn.execute(
            text(
                """
            CREATE TRIGGER IF NOT EXISTS user_stories_fts_delete AFTER DELETE ON user_stories
            BEGIN
                INSERT INTO user_stories_fts(user_stories_fts, rowid, feature_description, gherkin_output)
                VALUES ('delete', old.id, old.feature_description, old.gherkin_output);
            END
        """
            )
        )

        await conn.execute(
            text(
                """
            CREATE TRIGGER IF NOT EXISTS user_stories_fts_update AFTER UPDATE ON user_stories
            BEGIN
                INSERT INTO user_stories_fts(user_stories_fts, rowid, feature_description, gherkin_output)
                VALUES ('delete', old.id, old.feature_description, old.gherkin_output);
                INSERT INTO user_stories_fts(rowid, feature_description, gherkin_output)
                VALUES (new.id, new.feature_description, new.gherkin_output);
            END
        """
            )
        )


async def close_database():
    """
    Close database connections.

    This function should be called on application shutdown.
    """
    await engine.dispose()


async def vacuum_database():
    """
    Perform VACUUM operation for optimal SQLite performance.

    This should be called periodically (e.g., during maintenance windows).
    Based on ADR-003 performance considerations.
    """
    async with engine.begin() as conn:
        await conn.execute(text("VACUUM"))


def get_database_info() -> dict:
    """
    Get database information for health checks and monitoring.

    Returns:
        dict: Database information including file size, version, etc.
    """
    try:
        file_size = (
            os.path.getsize(DATABASE_FILE) if os.path.exists(DATABASE_FILE) else 0
        )

        # Get SQLite version using sync connection
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version()")
        sqlite_version = cursor.fetchone()[0]

        cursor.execute("PRAGMA journal_mode")
        journal_mode = cursor.fetchone()[0]

        cursor.execute("PRAGMA page_count")
        page_count = cursor.fetchone()[0]

        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]

        conn.close()

        return {
            "database_file": DATABASE_FILE,
            "file_size_bytes": file_size,
            "file_size_mb": round(file_size / 1024 / 1024, 2),
            "sqlite_version": sqlite_version,
            "journal_mode": journal_mode,
            "page_count": page_count,
            "page_size": page_size,
            "estimated_size_mb": round((page_count * page_size) / 1024 / 1024, 2),
        }
    except Exception as e:
        return {"error": str(e)}
