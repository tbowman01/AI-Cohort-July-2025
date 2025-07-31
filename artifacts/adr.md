# Architectural Decision Record (ADR)

**Date:** 2025-07-31  
**Version:** 1.0  
**Authors:** Jason J. McMullen

---

## Title

Use React, FastAPI, and SQLite3 for Web Application Stack

---

## Status

Status: Accepted

---

## Context

This project aims to build an educational web application that teaches software developers how to use AI tools effectively in their careers. The application must be fast, simple to deploy, easy to maintain, and allow rapid iteration of features.

Key project requirements include:

- Quick development and deployment cycles
- In-memory database support during development
- Separation of frontend and backend services for scalability
- Developer familiarity with JavaScript/React and Python
- Minimal setup complexity for early prototyping

Stakeholders: development team, educational content designers, future students of the platform.

---

## Decision

We will use React for the frontend, FastAPI for the backend, and SQLite3 as the development database.

- **React**: Provides a fast, component-driven UI framework with a rich ecosystem. Ideal for building dynamic, interactive interfaces.
- **FastAPI**: A modern Python web framework with automatic OpenAPI documentation generation and excellent async support. Ideal for clean API development.
- **SQLite3**: Lightweight, file-based relational database suitable for in-memory or development use cases. Reduces infrastructure overhead during early phases.

This stack aligns with the team's skills, project constraints, and the need for rapid iteration and teaching-focused design.

---

## Consequences

*Positive:*
- Fast, async backend development with automatic OpenAPI docs.
- Simplified local and cloud deployment with minimal dependencies.
- Ability to use SQLite3 for quick prototyping and FastAPI’s built-in validation for lesson content and quizzes.
- Reusability of React components for a modular, scalable frontend.

*Negative:*
- SQLite3 is not recommended for high-concurrency production use; will need migration later (e.g., to PostgreSQL).
- Two different languages (JavaScript and Python) increases cognitive overhead.
- DevOps complexity may increase as project scales and containers/services are split further.

---

## Alternatives Considered

- **Monolithic Django App**: Includes frontend templating and backend in one stack, but lacks modern SPA flexibility and would require additional effort to achieve decoupled interactivity.
- **Node.js Backend**: Would allow a unified JavaScript stack, but lacks built-in validation features and would diverge from the team's preference for Python.
- **PostgreSQL**: Strong choice for future scaling, but overkill for current in-memory prototype needs.

---

## Related Decisions

- PRD-001: AI Learning Platform Requirements
- Future ADR TBD: Migration from SQLite3 to PostgreSQL for production

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Official Docs](https://react.dev/)
- [SQLite Documentation](https://sqlite.org/docs.html)
- [Stack Overflow Developer Survey 2023](https://survey.stackoverflow.co/2023/#technology)

---
# Architectural Decision Record (ADR) Template

**Date:** 2024-06-11  
**Version:** 1.0  
**Authors:** Jane Doe, John Smith

---

## Title

**Description:**  
A short, descriptive name for this architectural decision.

**Example:**  
Use PostgreSQL as the primary database engine

---

## Status

**Description:**  
The current state of this decision. Common statuses include: Proposed, Accepted, Deprecated, Superseded, or Rejected.

**Example:**  
Status: Accepted

---

## Context

**Description:**  
A detailed explanation of the issue at hand, the forces at play, background information, and why this decision is necessary. This section should include relevant constraints, requirements, and stakeholders.

**Example:**  
Our application needs a reliable, open-source relational database system that supports complex queries and can easily scale. The team is already familiar with SQL databases, and we require strong community support and active development. Alternatives considered include MySQL, SQLite, and MongoDB.

---

## Decision

**Description:**  
A clear statement of the decision that has been made and why. This should summarize why this alternative was chosen over others.

**Example:**  
We will use PostgreSQL as the primary database engine for the application because it offers advanced features, robust performance, and aligns well with our team's expertise.

---

## Consequences

**Description:**  
The results of making this decision, both positive and negative. Include implications for the project, potential risks, and any technical debt introduced.

**Example:**  
*Positive:*  
- Advanced SQL support and extensibility.  
- Large community and solid documentation.  
- Easier to hire developers with relevant experience.

*Negative:*  
- Slightly steeper learning curve for some team members.  
- More complex configuration compared to SQLite.

---

## Alternatives Considered

**Description:**  
A summary of other options that were evaluated and why they were not chosen.

**Example:**  
- **MySQL:** Lacks some advanced SQL features required for our use case.  
- **SQLite:** Not suitable for high concurrency or production-scale deployments.  
- **MongoDB:** Does not support relational data as natively as required.

---

## Related Decisions

**Description:**  
References to other ADRs or architectural decisions that are related to or influenced by this decision.

**Example:**  
- ADR-003: Decision to use Kubernetes for orchestration  
- ADR-005: Use of Redis for caching

---

## References

**Description:**  
Links or citations to relevant documents, discussions, RFCs, or supporting materials.

**Example:**  
- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [Stack Overflow Survey 2023: Most Loved Databases](https://insights.stackoverflow.com/survey/2023#technology-databases)

---
