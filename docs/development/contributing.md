---
layout: default
title: Contributing Guidelines
parent: Development
nav_order: 3
---

# Contributing Guidelines
{: .fs-9 }

Code standards, review process, and contribution workflow
{: .fs-6 .fw-300 }

---

## Welcome Contributors!

We welcome contributions to AutoDevHub! This guide will help you get started with contributing code, documentation, or reporting issues.

## Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/AI-Cohort-July-2025.git
cd AI-Cohort-July-2025

# Add upstream remote
git remote add upstream https://github.com/ai-cohort-july-2025/AI-Cohort-July-2025.git
```

### 2. Development Setup
Follow the [Setup Guide](/docs/development/setup-guide.md) to configure your development environment.

### 3. Create Feature Branch
```bash
# Create branch from main
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name
```

---

## Contribution Types

### Code Contributions
- **New Features**: Enhance existing functionality
- **Bug Fixes**: Resolve reported issues
- **Performance**: Optimize existing code
- **Refactoring**: Improve code quality without changing functionality

### Documentation
- **API Documentation**: Update endpoint documentation
- **User Guides**: Improve setup and usage instructions
- **Code Comments**: Add inline documentation
- **Examples**: Provide usage examples

### Testing
- **Unit Tests**: Test individual components
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete user workflows
- **Performance Tests**: Benchmark improvements

---

## Development Workflow

### 1. Issue Creation
Before starting work:
- Check existing issues for duplicates
- Create detailed issue with:
  - Clear description
  - Steps to reproduce (for bugs)
  - Expected vs actual behavior
  - Environment details

### 2. Development Process
```bash
# Keep your branch updated
git fetch upstream
git rebase upstream/main

# Make your changes
# Write tests for new functionality
# Update documentation as needed

# Run quality checks
npm run lint      # Frontend
black .          # Backend formatting
pytest          # Backend tests
npm test        # Frontend tests
```

### 3. Commit Standards
Use conventional commit format:
```
type(scope): description

Optional body with more details.

Optional footer with issue references.
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (no logic changes)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```bash
git commit -m "feat(api): add story generation endpoint"
git commit -m "fix(ui): resolve mobile responsive layout issue"
git commit -m "docs(readme): update installation instructions"
```

---

## Code Standards

### Backend (Python)

#### Code Style
- **Formatter**: Black (line length: 88)
- **Import Sorting**: isort
- **Linting**: pylint, flake8
- **Type Hints**: Required for all functions

#### Example Code Structure
```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

class StoryRequest(BaseModel):
    """Request model for story generation."""
    feature_description: str
    project_context: Optional[str] = None

class StoryResponse(BaseModel):
    """Response model for generated stories."""
    stories: List[str]
    metadata: dict

async def generate_stories(
    request: StoryRequest,
    current_user: User = Depends(get_current_user)
) -> StoryResponse:
    """Generate user stories from feature description.
    
    Args:
        request: Story generation request
        current_user: Authenticated user
        
    Returns:
        Generated stories with metadata
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        # Implementation here
        return StoryResponse(stories=stories, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Testing Standards
```python
import pytest
from fastapi.testclient import TestClient

def test_generate_stories_success(client: TestClient, auth_headers: dict):
    """Test successful story generation."""
    request_data = {
        "feature_description": "User authentication system",
        "project_context": "Web application"
    }
    
    response = client.post(
        "/api/v1/stories/generate",
        json=request_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "stories" in data
    assert len(data["stories"]) > 0

def test_generate_stories_invalid_input(client: TestClient, auth_headers: dict):
    """Test story generation with invalid input."""
    response = client.post(
        "/api/v1/stories/generate",
        json={},  # Missing required field
        headers=auth_headers
    )
    
    assert response.status_code == 422
```

### Frontend (React/TypeScript)

#### Code Style
- **Formatter**: Prettier
- **Linting**: ESLint with TypeScript rules
- **Component Style**: Functional components with hooks
- **File Naming**: PascalCase for components, camelCase for utilities

#### Component Structure
```typescript
import React, { useState, useCallback } from 'react';
import { StoryRequest, StoryResponse } from '../types/api';
import { LoadingSpinner } from './LoadingSpinner';
import './StoryGenerator.css';

interface StoryGeneratorProps {
  onStoriesGenerated?: (stories: StoryResponse) => void;
  className?: string;
}

export const StoryGenerator: React.FC<StoryGeneratorProps> = ({
  onStoriesGenerated,
  className = ''
}) => {
  const [formData, setFormData] = useState<StoryRequest>({
    feature_description: '',
    project_context: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/v1/stories/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Failed to generate stories');
      }

      const data: StoryResponse = await response.json();
      onStoriesGenerated?.(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [formData, onStoriesGenerated]);

  return (
    <div className={`story-generator ${className}`}>
      <form onSubmit={handleSubmit}>
        {/* Form fields */}
        <button type="submit" disabled={loading}>
          {loading ? <LoadingSpinner /> : 'Generate Stories'}
        </button>
      </form>
      {error && <div className="error">{error}</div>}
    </div>
  );
};
```

#### Testing Standards
```typescript
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { StoryGenerator } from './StoryGenerator';

// Mock fetch
global.fetch = jest.fn();

describe('StoryGenerator', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  it('renders form elements correctly', () => {
    render(<StoryGenerator />);
    
    expect(screen.getByLabelText(/feature description/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /generate stories/i })).toBeInTheDocument();
  });

  it('handles successful story generation', async () => {
    const mockResponse = {
      stories: ['Story 1', 'Story 2'],
      metadata: {}
    };
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    });

    const onStoriesGenerated = jest.fn();
    render(<StoryGenerator onStoriesGenerated={onStoriesGenerated} />);
    
    fireEvent.change(screen.getByLabelText(/feature description/i), {
      target: { value: 'User authentication' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /generate stories/i }));
    
    await waitFor(() => {
      expect(onStoriesGenerated).toHaveBeenCalledWith(mockResponse);
    });
  });
});
```

---

## Pull Request Process

### 1. Pre-PR Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] Branch is up to date with main

### 2. PR Creation
Create PR with:
- **Clear Title**: Summarize changes in <50 characters
- **Description**: Explain what, why, and how
- **Issue Reference**: Link related issues
- **Testing**: Describe test coverage
- **Screenshots**: For UI changes

### 3. PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### 4. Review Process
1. **Automated Checks**: CI/CD pipeline runs
2. **Code Review**: Team member reviews
3. **Testing**: Reviewer tests changes
4. **Approval**: Required approvals received
5. **Merge**: Squash and merge to main

---

## Quality Guidelines

### Code Quality
- **DRY Principle**: Don't repeat yourself
- **SOLID Principles**: Follow object-oriented design principles
- **Error Handling**: Comprehensive error handling
- **Performance**: Consider performance implications
- **Security**: Follow security best practices

### Documentation Quality
- **Clear**: Easy to understand
- **Complete**: Cover all functionality
- **Examples**: Provide usage examples
- **Up-to-date**: Keep in sync with code

### Test Quality
- **Coverage**: Aim for >90% test coverage
- **Meaningful**: Test behavior, not implementation
- **Fast**: Tests should run quickly
- **Isolated**: Tests should not depend on each other

---

## Issue Reporting

### Bug Reports
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., macOS 12.0]
- Browser: [e.g., Chrome 95]
- Node.js: [e.g., 18.0.0]
- Python: [e.g., 3.12.0]

**Screenshots**
If applicable, add screenshots
```

### Feature Requests
```markdown
**Feature Description**
Clear description of the feature

**Problem/Use Case**
What problem does this solve?

**Proposed Solution**
Describe your proposed solution

**Alternatives**
Other solutions you've considered

**Additional Context**
Any other context or screenshots
```

---

## Community Guidelines

### Code of Conduct
- **Be Respectful**: Treat everyone with respect
- **Be Inclusive**: Welcome diverse perspectives
- **Be Constructive**: Provide helpful feedback
- **Be Patient**: Help newcomers learn

### Communication
- **GitHub Issues**: For bugs and feature requests
- **Pull Requests**: For code discussions
- **Discussions**: For general questions
- **Email**: For security issues

---

## Recognition

### Contributors
All contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation
- Invited to team discussions

### Maintainers
Active contributors may be invited to become maintainers with:
- Repository write access
- Review responsibilities
- Release management participation
- Architecture decision involvement

---

*Thank you for contributing to AutoDevHub! Your contributions help make this project better for everyone.*