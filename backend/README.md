# AutoDevHub Backend Database Implementation

SQLite-based database implementation following **ADR-003: Database Selection**.

## 🗃️ Database Architecture

Based on ADR-003 specifications:
- **Database**: SQLite with WAL mode for concurrent reads
- **ORM**: SQLAlchemy with async support  
- **Driver**: aiosqlite for async operations
- **File**: `autodevhub.db` (configurable via environment)

## 📁 File Structure

```
backend/
├── __init__.py           # Package initialization
├── config.py             # Configuration management with pydantic-settings
├── database.py           # SQLite connection, session management, and setup
├── models.py             # SQLAlchemy ORM models (UserStory, Session)
├── schemas.py            # Pydantic schemas for API validation
├── init_db.py            # Database initialization script
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env if needed (defaults work for development)
```

### 3. Initialize Database

```bash
# Create database and tables
python init_db.py

# Create database with sample data for testing
python init_db.py --sample-data
```

### 4. Use in FastAPI Application

```python
from backend import get_db, UserStory, UserStoryCreate
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.post("/stories/", response_model=UserStoryResponse)
async def create_story(
    story: UserStoryCreate,
    db: AsyncSession = Depends(get_db)
):
    db_story = UserStory(
        feature_description=story.feature_description,
        gherkin_output="Generated Gherkin content..."  # AI generation
    )
    db_story.set_metadata(story.metadata)
    
    db.add(db_story)
    await db.commit()
    await db.refresh(db_story)
    
    return db_story.to_dict()
```

## 🗄️ Database Schema

### UserStory Table
```sql
CREATE TABLE user_stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feature_description TEXT NOT NULL,
    gherkin_output TEXT NOT NULL,
    metadata TEXT,  -- JSON as TEXT in SQLite
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Session Table (Future Enhancement)
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,  -- UUID as TEXT
    user_id TEXT,
    preferences TEXT,  -- JSON as TEXT
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔍 Full-Text Search

SQLite FTS5 is configured for searching user stories:

```python
from backend.models import search_user_stories

# Search stories by content
results = await search_user_stories(
    session=db_session,
    query="login authentication",
    limit=10
)
```

## ⚡ Performance Features

### SQLite Optimizations (Automatic)
- **WAL Mode**: Better concurrent read performance
- **Optimized Pragmas**: Cache size, synchronous mode
- **Automatic Indexing**: JSON queries and timestamps
- **Connection Pooling**: Efficient connection reuse

### Indexing Strategy
```sql
-- Automatic indexes created by init_db.py
CREATE INDEX idx_user_stories_created_at ON user_stories(created_at DESC);
CREATE INDEX idx_user_stories_updated_at ON user_stories(updated_at DESC);

-- Full-text search virtual table
CREATE VIRTUAL TABLE user_stories_fts USING fts5(
    feature_description, 
    gherkin_output, 
    content='user_stories'
);
```

## 🔧 Configuration Options

Environment variables (see `.env.example`):

```bash
# Database
DATABASE_FILE=autodevhub.db  # SQLite file path
DEBUG=false                  # Enable SQL query logging

# Performance  
MAX_DB_CONNECTIONS=20        # Connection pool size
DB_POOL_SIZE=5              # Concurrent connections

# Features
CREATE_SAMPLE_DATA=false    # Create sample stories on init
HEALTH_CHECK_ENABLED=true   # Enable health endpoints
```

## 🧪 Testing and Development

### Create Sample Data
```bash
# Via command line
python init_db.py --sample-data

# Via environment variable
CREATE_SAMPLE_DATA=true python init_db.py
```

### Database Health Check
```python
from backend.database import get_database_info

# Get database statistics
info = get_database_info()
print(f"Database size: {info['file_size_mb']} MB")
print(f"SQLite version: {info['sqlite_version']}")
print(f"Journal mode: {info['journal_mode']}")  # Should be "wal"
```

### Maintenance Operations
```python
from backend.database import vacuum_database

# Optimize database performance
await vacuum_database()
```

## 📊 Model Usage Examples

### UserStory Model
```python
from backend import UserStory

# Create story with metadata
story = UserStory(
    feature_description="As a user, I want to login...",
    gherkin_output="Feature: Login..."
)

# Set JSON metadata (stored as TEXT in SQLite)
story.set_metadata({
    "ai_model": "gpt-4",
    "processing_time_ms": 1250,
    "confidence_score": 0.95
})

# Retrieve metadata as dictionary
metadata = story.get_metadata()
```

### Session Model
```python
from backend import Session

# Create session with preferences
session = Session(user_id="user123")
session.set_preferences({
    "theme": "dark",
    "ai_model": "gpt-4",
    "notifications": True
})

# Convert to dictionary for API response
session_dict = session.to_dict()
```

## 🔒 Security Considerations

- **Input Validation**: All inputs validated via Pydantic schemas
- **SQL Injection**: SQLAlchemy ORM provides automatic protection
- **File Permissions**: Database file should have restricted access in production
- **JSON Validation**: Metadata parsing includes error handling

## 🚀 Production Deployment

### Backup Strategy
```bash
# Simple file backup (database is a single file)
cp autodevhub.db autodevhub.db.backup

# Or use SQLite backup command for hot backup
sqlite3 autodevhub.db ".backup autodevhub.db.backup"
```

### Performance Monitoring
```python
from backend.models import get_user_story_stats

# Get database statistics
stats = get_user_story_stats(db_session)
print(f"Total stories: {stats['total_stories']}")
print(f"Average feature length: {stats['avg_feature_description_length']}")
```

## 🔄 Migration Path

Future migration to PostgreSQL (post-capstone):
1. Export data using SQLAlchemy models
2. Update database URL in configuration
3. Run new initialization with PostgreSQL
4. Import data using same ORM models

The ORM abstraction makes this transition straightforward.

## 📚 API Schema Examples

See `schemas.py` for complete Pydantic model definitions:

```python
# Create user story
{
  "feature_description": "As a user, I want to login...",
  "metadata": {
    "priority": "high",
    "story_points": 3
  }
}

# Response includes generated Gherkin
{
  "id": 1,
  "feature_description": "As a user, I want to login...",
  "gherkin_output": "Feature: Login\n  Scenario: Successful login...",
  "metadata": {...},
  "created_at": "2025-07-31T17:00:00Z",
  "updated_at": "2025-07-31T17:00:00Z"
}
```

---

## 📋 Implementation Checklist

- ✅ SQLite database with WAL mode configuration
- ✅ SQLAlchemy async ORM models for UserStory and Session
- ✅ Pydantic schemas for API validation
- ✅ Full-text search with SQLite FTS5
- ✅ Database initialization script with sample data
- ✅ Performance optimizations (indexes, pragmas, pooling)
- ✅ Configuration management with environment variables
- ✅ Health check and monitoring capabilities
- ✅ JSON metadata support (stored as TEXT in SQLite)
- ✅ Connection pooling and async session management

**Status**: ✅ Complete - Ready for FastAPI integration