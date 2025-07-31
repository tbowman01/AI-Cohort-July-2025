# AutoDevHub CI/CD Workflows

GitHub Actions workflows for continuous integration and deployment of the AutoDevHub platform.

## 🔄 Workflow Overview

This directory contains automated workflows that handle testing, building, and deploying the AutoDevHub application across different environments.

```
.github/workflows/
├── README.md                    # This file
├── ci.yml                       # Continuous integration workflow
├── cd-staging.yml               # Staging deployment workflow
├── cd-production.yml            # Production deployment workflow
├── docs-deploy.yml              # Documentation deployment
├── security-scan.yml            # Security scanning workflow
├── dependency-update.yml        # Automated dependency updates
└── cleanup.yml                  # Cleanup old artifacts and branches
```

## 🚀 Workflow Details

### Continuous Integration (ci.yml)

**Trigger**: Push to any branch, Pull requests to main

**Jobs**:
- **Backend Testing**: Python unit tests, integration tests, linting
- **Frontend Testing**: React component tests, TypeScript checks, ESLint
- **Security Scanning**: Dependency vulnerability checks
- **Code Quality**: Code coverage analysis and quality gates

**Matrix Strategy**:
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: [3.9, 3.10, 3.11]
    node-version: [16, 18]
```

### Staging Deployment (cd-staging.yml)

**Trigger**: Push to `develop` branch

**Steps**:
1. Build and test backend application
2. Build and test frontend application
3. Build Docker images
4. Deploy to staging environment
5. Run smoke tests
6. Notify team of deployment status

**Environment**: Staging server with test data

### Production Deployment (cd-production.yml)

**Trigger**: Release tags (`v*.*.*`)

**Steps**:
1. Comprehensive testing suite
2. Security scans and compliance checks
3. Build production Docker images
4. Database migration (if needed)
5. Blue-green deployment to production
6. Health checks and monitoring
7. Rollback capability on failure

**Environment**: Production with real user data

### Documentation Deployment (docs-deploy.yml)

**Trigger**: Changes to `docs/` directory in main branch

**Steps**:
1. Build Jekyll site
2. Deploy to GitHub Pages
3. Update search index
4. Validate links and images

**Output**: Documentation site at GitHub Pages URL

### Security Scanning (security-scan.yml)

**Trigger**: Daily schedule, Pull requests

**Scans**:
- **SAST**: Static Application Security Testing
- **Dependency Check**: Known vulnerability scanning
- **Container Scanning**: Docker image security analysis
- **Secrets Detection**: Prevent credentials in code

**Tools**: CodeQL, Snyk, Trivy, GitLeaks

### Dependency Updates (dependency-update.yml)

**Trigger**: Weekly schedule

**Actions**:
- Update Python dependencies (pip-tools)
- Update Node.js dependencies (npm-check-updates)
- Create automated pull requests
- Run tests against updated dependencies

**Security**: Automated security patches

### Cleanup (cleanup.yml)

**Trigger**: Weekly schedule

**Tasks**:
- Remove old workflow artifacts
- Clean up stale branches
- Archive old deployment logs
- Optimize storage usage

## 🔧 Workflow Configuration

### Environment Variables

```yaml
env:
  NODE_VERSION: '18'
  PYTHON_VERSION: '3.10'
  DOCKER_REGISTRY: ghcr.io
  STAGING_URL: https://staging.autodevhub.com
  PRODUCTION_URL: https://autodevhub.com
```

### Secrets Configuration

Required repository secrets:

**Infrastructure**:
- `STAGING_SERVER_HOST`: Staging server hostname
- `PRODUCTION_SERVER_HOST`: Production server hostname
- `DOCKER_REGISTRY_TOKEN`: Container registry access token

**Database**:
- `STAGING_DATABASE_URL`: Staging database connection string
- `PRODUCTION_DATABASE_URL`: Production database connection string

**External Services**:
- `GITHUB_TOKEN`: GitHub API access (auto-provided)
- `SLACK_WEBHOOK_URL`: Team notifications
- `MONITORING_API_KEY`: Application monitoring service

**Security**:
- `JWT_SECRET_KEY`: JWT token signing key
- `ENCRYPTION_KEY`: Data encryption key

### Branch Protection Rules

**Main Branch**:
- Require pull request reviews (2 reviewers)
- Require status checks to pass
- Require branches to be up to date
- Restrict pushes to administrators

**Develop Branch**:
- Require pull request reviews (1 reviewer)
- Require status checks to pass
- Allow force pushes for maintainers

## 🧪 Testing Strategy

### Backend Testing

```yaml
- name: Run Backend Tests
  run: |
    cd backend
    python -m pytest tests/ -v --cov=app --cov-report=xml
    python -m flake8 app/
    python -m mypy app/
```

### Frontend Testing

```yaml
- name: Run Frontend Tests
  run: |
    cd frontend
    npm run test:coverage
    npm run lint
    npm run type-check
    npm run build
```

### Integration Testing

```yaml
- name: Integration Tests
  run: |
    docker-compose -f docker-compose.test.yml up -d
    npm run test:integration
    docker-compose -f docker-compose.test.yml down
```

## 🚀 Deployment Strategy

### Blue-Green Deployment

```yaml
deployment:
  strategy: blue-green
  health_check:
    path: /health
    timeout: 300s
    interval: 10s
  rollback:
    automatic: true
    threshold: 5m
```

### Database Migrations

```yaml
- name: Database Migration
  run: |
    alembic upgrade head
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Health Checks

```yaml
- name: Health Check
  run: |
    curl -f ${{ env.APP_URL }}/health || exit 1
    curl -f ${{ env.APP_URL }}/api/v1/status || exit 1
```

## 📊 Monitoring and Notifications

### Status Notifications

**Slack Integration**:
```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

**Email Notifications**:
- Deployment failures
- Security scan alerts
- Critical test failures

### Metrics Collection

```yaml
- name: Collect Metrics
  run: |
    echo "deployment_time=$(date +%s)" >> $GITHUB_OUTPUT
    echo "test_coverage=${{ steps.coverage.outputs.percentage }}" >> $GITHUB_OUTPUT
```

## 🔒 Security Best Practices

### Secrets Management

- Use GitHub encrypted secrets
- Rotate secrets regularly
- Limit secret access to necessary workflows
- Audit secret usage

### Container Security

```yaml
- name: Scan Docker Image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.IMAGE_NAME }}:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'
```

### Code Scanning

```yaml
- name: Initialize CodeQL
  uses: github/codeql-action/init@v2
  with:
    languages: python, javascript

- name: Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v2
```

## 🚧 TODO

- [ ] Set up basic CI workflow
- [ ] Configure staging deployment
- [ ] Implement production deployment
- [ ] Add security scanning
- [ ] Set up documentation deployment
- [ ] Configure dependency updates
- [ ] Add performance testing
- [ ] Implement blue-green deployment
- [ ] Set up monitoring and alerts
- [ ] Add cleanup workflows

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Security Hardening](https://docs.github.com/en/actions/security-guides)
- [Workflow Templates](https://github.com/actions/starter-workflows)

---

For questions about CI/CD workflows, please contact the DevOps team or [open an issue](https://github.com/[username]/AutoDevHub/issues).