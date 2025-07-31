# AutoDevHub Backend

FastAPI-based backend for the AutoDevHub AI-powered DevOps tracking platform.

## 🏗️ Architecture

- **Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens
- **API Documentation**: Automatically generated with OpenAPI/Swagger
- **Testing**: pytest with async support

## 📁 Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and environment variables
│   ├── database.py          # Database connection and session management
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas for request/response
│   ├── api/                 # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── projects.py      # Project management endpoints
│   │   ├── teams.py         # Team management endpoints
│   │   └── analytics.py     # Analytics and insights endpoints
│   ├── core/                # Core business logic
│   │   ├── __init__.py
│   │   ├── security.py      # JWT and password hashing
│   │   └── ai_insights.py   # AI-powered analytics
│   └── tests/               # Test files
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── Dockerfile              # Docker configuration
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip or poetry

### Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secrets
   ```

4. **Run database migrations**:
   ```bash
   # TODO: Add Alembic migration commands
   ```

5. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

## 🐳 Docker

```bash
# Build image
docker build -t autodevhub-backend .

# Run container
docker run -p 8000:8000 autodevhub-backend
```

## 🔧 Development

### Code Style

- **Formatter**: Black
- **Linter**: Flake8
- **Type Checker**: mypy
- **Import Sorter**: isort

```bash
# Format code
black .

# Lint code
flake8 .

# Type check
mypy app/

# Sort imports
isort .
```

### Database

- **ORM**: SQLAlchemy 2.0+ with async support
- **Migrations**: Alembic
- **Connection Pooling**: Built-in FastAPI/SQLAlchemy pooling

## 🌟 Key Features

- **Async/Await**: Full async support for better performance
- **Dependency Injection**: FastAPI's built-in DI system
- **Automatic Validation**: Pydantic models for request/response validation
- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: API rate limiting with Redis
- **Monitoring**: Health checks and metrics endpoints
- **AI Integration**: Built-in AI analytics and insights

## 📈 Performance

- **Async Database Operations**: Non-blocking database queries
- **Connection Pooling**: Efficient database connection management
- **Response Caching**: Redis-based caching for frequently accessed data
- **Background Tasks**: Celery for heavy processing tasks

## 🔒 Security

- **JWT Tokens**: Secure authentication with refresh tokens
- **Password Hashing**: bcrypt for secure password storage
- **CORS**: Configurable cross-origin resource sharing
- **Input Validation**: Automatic request validation with Pydantic
- **SQL Injection Prevention**: SQLAlchemy ORM protections

## 🚧 TODO

- [ ] Set up Alembic migrations
- [ ] Implement authentication endpoints
- [ ] Create project management APIs
- [ ] Add team collaboration features
- [ ] Integrate AI analytics
- [ ] Set up background task processing
- [ ] Add comprehensive test coverage
- [ ] Implement rate limiting
- [ ] Add monitoring and logging
- [ ] Set up CI/CD pipeline

---

For more information, see the [main project README](../README.md).