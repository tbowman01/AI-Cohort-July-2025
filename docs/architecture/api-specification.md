---
layout: default
title: API Specification
parent: Architecture
nav_order: 2
---

# API Specification
{: .fs-9 }

RESTful API documentation and endpoint specifications
{: .fs-6 .fw-300 }

---

## API Overview

AutoDevHub provides a RESTful API built with FastAPI, offering comprehensive endpoints for AI-powered story generation, project management, and documentation automation.

**Base URL**: `http://localhost:8000/api/v1`  
**Documentation**: `http://localhost:8000/docs`  
**Interactive Testing**: `http://localhost:8000/redoc`

---

## Authentication

### JWT Token Authentication
```http
Authorization: Bearer <jwt_token>
```

### Login Endpoint
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

## Core Endpoints

### Story Generation

#### Generate User Stories
```http
POST /api/v1/stories/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "project_name": "E-commerce Platform",
  "description": "Online shopping platform with mobile support",
  "target_audience": "Mobile-first shoppers aged 25-45",
  "key_features": "Product catalog, shopping cart, payments",
  "project_type": "web_application",
  "complexity": "medium"
}
```

**Response**:
```json
{
  "request_id": "req_123456789",
  "stories": [
    {
      "id": "story_1",
      "title": "User Registration",
      "description": "As a new user, I want to create an account so that I can access personalized features",
      "acceptance_criteria": [
        "Given I am on the registration page",
        "When I enter valid registration details",
        "Then I should receive a confirmation email",
        "And my account should be created successfully"
      ],
      "priority": "HIGH",
      "story_points": 5,
      "tasks": [
        "Create registration form component",
        "Implement email validation",
        "Add password strength validation",
        "Create email confirmation system"
      ],
      "tags": ["authentication", "user-management"]
    }
  ],
  "metadata": {
    "total_stories": 8,
    "generation_time": 2.3,
    "ai_model": "claude-3",
    "created_at": "2025-08-01T10:30:00Z"
  }
}
```

#### Get Story by ID
```http
GET /api/v1/stories/{story_id}
Authorization: Bearer <token>
```

#### Update Story
```http
PUT /api/v1/stories/{story_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Story Title",
  "description": "Updated description",
  "acceptance_criteria": ["Updated criteria"],
  "priority": "MEDIUM"
}
```

#### Delete Story
```http
DELETE /api/v1/stories/{story_id}
Authorization: Bearer <token>
```

---

### Project Management

#### Create Project
```http
POST /api/v1/projects
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "E-commerce Platform",
  "description": "Modern online shopping platform",
  "repository_url": "https://github.com/user/ecommerce",
  "settings": {
    "ai_model": "claude-3",
    "story_template": "agile",
    "default_priority": "MEDIUM"
  }
}
```

#### List Projects
```http
GET /api/v1/projects?page=1&limit=10
Authorization: Bearer <token>
```

#### Get Project Details
```http
GET /api/v1/projects/{project_id}
Authorization: Bearer <token>
```

---

### User Management

#### Get Current User
```http
GET /api/v1/users/me
Authorization: Bearer <token>
```

#### Update User Profile
```http
PUT /api/v1/users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "preferences": {
    "theme": "dark",
    "notifications": true
  }
}
```

---

## Data Models

### Story Model
```typescript
interface Story {
  id: string;
  title: string;
  description: string;
  acceptance_criteria: string[];
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  story_points: number;
  tasks: string[];
  tags: string[];
  status: 'DRAFT' | 'READY' | 'IN_PROGRESS' | 'DONE';
  project_id: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}
```

### Project Model
```typescript
interface Project {
  id: string;
  name: string;
  description: string;
  repository_url?: string;
  settings: {
    ai_model: string;
    story_template: string;
    default_priority: string;
  };
  owner_id: string;
  created_at: string;
  updated_at: string;
}
```

### User Model
```typescript
interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'USER' | 'ADMIN';
  preferences: {
    theme: string;
    notifications: boolean;
  };
  created_at: string;
  last_login: string;
}
```

---

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    },
    "timestamp": "2025-08-01T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

### HTTP Status Codes

| Code | Description | Usage |
|------|-------------|-------|
| 200 | OK | Successful GET, PUT requests |
| 201 | Created | Successful POST requests |
| 204 | No Content | Successful DELETE requests |
| 400 | Bad Request | Invalid request format |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side errors |

---

## Rate Limiting

### Default Limits
- **Authentication**: 5 requests per minute
- **Story Generation**: 10 requests per minute
- **General API**: 100 requests per minute
- **File Upload**: 5 requests per minute

### Rate Limit Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1625097600
```

---

## Pagination

### Query Parameters
```http
GET /api/v1/stories?page=1&limit=20&sort_by=created_at&order=desc
```

### Response Format
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## Filtering and Search

### Story Filtering
```http
GET /api/v1/stories?
  project_id=proj_123&
  priority=HIGH&
  status=READY&
  search=authentication&
  tags=user-management,security
```

### Advanced Search
```http
POST /api/v1/stories/search
Content-Type: application/json

{
  "query": "user authentication",
  "filters": {
    "priority": ["HIGH", "MEDIUM"],
    "created_after": "2025-07-01",
    "tags": ["authentication"]
  },
  "sort": {
    "field": "created_at",
    "order": "desc"
  }
}
```

---

## WebSocket Events

### Story Generation Progress
```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/stories');

// Listen for generation progress
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};

// Example progress events
{
  "type": "generation_started",
  "request_id": "req_123456789",
  "timestamp": "2025-08-01T10:30:00Z"
}

{
  "type": "generation_progress",
  "request_id": "req_123456789",
  "progress": 50,
  "message": "Analyzing project requirements"
}

{
  "type": "generation_completed",
  "request_id": "req_123456789",
  "stories_count": 8
}
```

---

## API Versioning

### Version Headers
```http
API-Version: v1
Accept: application/vnd.autodevhub.v1+json
```

### Deprecation Notice
```http
Deprecation: Sun, 01 Jan 2026 00:00:00 GMT
Sunset: Sun, 01 Jan 2027 00:00:00 GMT
```

---

## OpenAPI Specification

### Access Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### Download Specification
```bash
# Download OpenAPI spec
curl http://localhost:8000/openapi.json > autodevhub-api.json

# Generate client SDK
npx @openapitools/openapi-generator-cli generate \
  -i autodevhub-api.json \
  -g typescript-fetch \
  -o ./sdk
```

---

## Performance Considerations

### Response Times
- **Authentication**: <100ms
- **Story Generation**: <3000ms
- **CRUD Operations**: <200ms
- **Search Queries**: <500ms

### Optimization Features
- **Response Caching**: Redis-based caching
- **Database Indexing**: Optimized query performance
- **Async Processing**: Background task queues
- **Connection Pooling**: Efficient database connections

---

*For implementation details, see [System Overview](/docs/architecture/system-overview.md). For database structure, see [Database Schema](/docs/architecture/database-schema.md).*