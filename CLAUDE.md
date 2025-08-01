# 🚀 AutoDevHub Claude Configuration (`CLAUDE.md`)

## 🎯 Project Context

**AutoDevHub**: AI-powered DevOps tracker that automates story generation, documentation, and workflow orchestration.

### Core Technologies
- **Backend**: FastAPI (Python 3.11+) with SQLite + Redis
- **Frontend**: React + TypeScript with Vite
- **AI**: Claude AI for story generation
- **Infrastructure**: Docker, GitHub Actions CI/CD
- **Testing**: pytest (backend), Jest (frontend)

---

## 🧠 Core Principles

1. **Batch Operations**: Maximize parallel execution for performance
2. **Defensive Security**: Only assist with security analysis and defensive coding
3. **Quality First**: All code must pass linting and type checking
4. **Documentation**: Update docs only when explicitly requested
5. **Memory Persistence**: Track insights across sessions for continuity

---

## 🔁 Specialized Agent Roles

| Role | Responsibilities | Primary Tools | Context |
|------|-----------------|---------------|---------|
| `backend-dev` | FastAPI endpoints, services, models | Python, SQLite, Redis | backend/ |
| `frontend-dev` | React components, UI/UX, state management | TypeScript, Vite, CSS | frontend/ |
| `tester` | Write/run tests, coverage reports | pytest, Jest, coverage | tests/, __tests__/ |
| `security-analyst` | Security scanning, vulnerability analysis | Bandit, defensive patterns | All code |
| `devops-engineer` | CI/CD, Docker, deployment | GitHub Actions, Docker | .github/, deployment/ |
| `api-docs` | API documentation, OpenAPI specs | FastAPI docs, Swagger | backend/routers/ |

---

## ⚡ Quick Commands

```bash
# Development
npm run dev              # Start both frontend and backend
npm run test            # Run all tests
npm run lint            # Lint all code

# Backend specific
cd backend && uvicorn main:app --reload
cd backend && pytest -v
cd backend && black . && isort . && flake8

# Frontend specific  
cd frontend && npm run dev
cd frontend && npm test
cd frontend && npm run lint

# Docker operations
docker-compose up -d    # Start services
docker-compose down     # Stop services
docker-compose logs -f  # View logs
```

---

## 📋 Task Templates

### 🔧 Backend Feature Implementation
```
1. Analyze existing patterns in backend/routers/ and backend/services/
2. Create/update service in backend/services/
3. Create/update router in backend/routers/
4. Update schemas in backend/schemas/
5. Write tests in backend/tests/
6. Run: cd backend && pytest && black . && flake8
```

### ⚛️ Frontend Component Development
```
1. Check existing components in frontend/src/components/
2. Create component with TypeScript and CSS modules
3. Add tests in __tests__/ directory
4. Update App.jsx if needed
5. Run: cd frontend && npm test && npm run lint
```

### 🔒 Security Review
```
1. Run: cd backend && bandit -r . -f json > bandit-report.json
2. Review authentication in backend/dependencies.py
3. Check API endpoints for injection vulnerabilities
4. Validate input sanitization in schemas
5. Document findings (only if requested)
```

---

## 🛡️ Security Guidelines

- **Authentication**: JWT tokens via backend/dependencies.py
- **Validation**: Pydantic schemas for all inputs
- **SQL**: Use SQLAlchemy ORM, never raw SQL
- **Secrets**: Environment variables only, never hardcode
- **CORS**: Configured in backend/main.py
- **Error Handling**: Never expose internal errors to users

---

## 📁 Project Structure Reference

```
backend/
├── main.py           # FastAPI app entry
├── routers/          # API endpoints
├── services/         # Business logic
├── schemas/          # Pydantic models
├── models.py         # SQLAlchemy models
├── database.py       # DB configuration
└── tests/           # Backend tests

frontend/
├── src/
│   ├── components/   # React components
│   ├── styles/       # CSS modules
│   └── App.jsx      # Main app
├── vite.config.js   # Vite config
└── package.json     # Dependencies
```

---

## 🔄 Workflow Patterns

### API Endpoint Creation
```javascript
// 1. Schema (backend/schemas/feature.py)
from pydantic import BaseModel

class FeatureCreate(BaseModel):
    name: str
    description: str

// 2. Service (backend/services/feature_service.py)
async def create_feature(db: Session, feature: FeatureCreate):
    // Business logic here
    pass

// 3. Router (backend/routers/feature_router.py)
@router.post("/features")
async def create_feature_endpoint(
    feature: FeatureCreate,
    db: Session = Depends(get_db)
):
    return await create_feature(db, feature)
```

### React Component Pattern
```typescript
// frontend/src/components/Feature.tsx
import styles from './Feature.module.css';

interface FeatureProps {
    title: string;
    onAction: () => void;
}

export const Feature: React.FC<FeatureProps> = ({ title, onAction }) => {
    return (
        <div className={styles.container}>
            <h2>{title}</h2>
            <button onClick={onAction}>Action</button>
        </div>
    );
};
```

---

## 📊 Quality Checks

Before marking any task complete:

1. **Backend**: `cd backend && pytest && black . && isort . && flake8`
2. **Frontend**: `cd frontend && npm test && npm run lint`
3. **Security**: `bandit -r backend/`
4. **Docker**: `docker-compose ps` (verify services running)

---

## 🧩 Memory Keys

Store insights using these standardized keys:

- `api-patterns`: REST API design decisions
- `component-patterns`: React component structures
- `test-strategies`: Testing approaches
- `security-findings`: Security analysis results
- `performance-opts`: Optimization techniques
- `deployment-notes`: Deployment configurations

---

## 🚨 Important Reminders

1. **NEVER** create documentation files unless explicitly requested
2. **ALWAYS** run linting and tests before completing tasks
3. **PREFER** editing existing files over creating new ones
4. **CHECK** existing patterns before implementing new features
5. **USE** TodoWrite for multi-step tasks
6. **VALIDATE** all user inputs with Pydantic schemas
7. **FOLLOW** defensive security practices

---

## 🔗 Quick References

- Backend API: http://localhost:8000/docs
- Frontend: http://localhost:3000
- GitHub: https://github.com/ai-cohort-july-2025/AI-Cohort-July-2025
- Docs: https://ai-cohort-july-2025.github.io/AI-Cohort-July-2025/

## 🚀 Task Workflow Guidelines

- After completing the task, always commit files and create PR to the defined branch you are working on