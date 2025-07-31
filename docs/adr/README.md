# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for the AutoDevHub project. Each ADR documents a significant architectural decision made during the development process.

## ADR Index

| ADR | Title | Status | Decision |
|-----|-------|--------|----------|
| [ADR-001](./ADR-001-backend-framework-selection.md) | Backend Framework Selection | Accepted | FastAPI |
| [ADR-002](./ADR-002-frontend-framework-selection.md) | Frontend Framework Selection | Accepted | React with Vite |
| [ADR-003](./ADR-003-database-selection.md) | Database Selection | Accepted | PostgreSQL |
| [ADR-004](./ADR-004-ai-integration-platform.md) | AI Integration Platform | Accepted | Claude AI |
| [ADR-005](./ADR-005-cicd-platform-selection.md) | CI/CD Platform Selection | Accepted | GitHub Actions |
| [ADR-006](./ADR-006-documentation-hosting.md) | Documentation Hosting | Accepted | GitHub Pages |
| [ADR-007](./ADR-007-development-environment.md) | Development Environment | Accepted | GitHub Codespaces |

## About ADRs

Architecture Decision Records (ADRs) are documents that capture important architectural decisions made during a project. Each ADR includes:

- **Context**: The situation that led to the need for a decision
- **Decision**: The architectural decision that was made
- **Consequences**: The positive and negative impacts of the decision
- **Alternatives Considered**: Other options that were evaluated

## Format

All ADRs follow a consistent format:

```markdown
# ADR-XXX: [Title]

## Status
[Proposed/Accepted/Deprecated]

## Context
[Description of the issue and context]

## Decision
[The decision that was made]

## Consequences
[Positive and negative consequences]

## Alternatives Considered
[Other options that were evaluated]
```

## Contributing

When making significant architectural decisions:

1. Create a new ADR using the next sequential number
2. Follow the established format
3. Include thorough context and rationale
4. Document all alternatives considered
5. Update this index with the new ADR

---

*Generated as part of the AutoDevHub capstone project demonstrating AI-assisted development practices.*