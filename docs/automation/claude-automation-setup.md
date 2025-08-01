# Claude Automation Setup Guide
## Automated Documentation Generation for Any Repository

This guide provides step-by-step instructions for implementing comprehensive automated documentation generation using `anthropics/claude-code-action@beta` in any repository.

## 🚀 Quick Start (5 Minutes)

### 1. Prerequisites
- GitHub repository with admin access
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- Basic familiarity with GitHub Actions

### 2. One-Command Setup
```bash
# Copy automation workflow to your repository
curl -fsSL https://raw.githubusercontent.com/ai-cohort-july-2025/AI-Cohort-July-2025/main/.github/workflow-templates/claude-auto-docs.yml \
  -o .github/workflows/claude-auto-docs.yml

# Add API key to repository secrets
gh secret set ANTHROPIC_API_KEY --body "your-api-key-here"

# Trigger initial documentation generation
gh workflow run claude-auto-docs.yml --field artifacts=all
```

## 📋 Detailed Setup Process

### Step 1: Repository Preparation

1. **Create GitHub Actions Directory**
   ```bash
   mkdir -p .github/workflows
   ```

2. **Copy Automation Workflow**
   Choose one of these methods:
   
   **Option A: Direct Copy**
   ```bash
   # Copy the comprehensive automation suite
   wget https://raw.githubusercontent.com/ai-cohort-july-2025/AI-Cohort-July-2025/main/.github/workflows/automated-documentation-suite.yml \
     -O .github/workflows/automated-documentation-suite.yml
   ```
   
   **Option B: Customizable Template**
   ```bash
   # Copy the template for customization
   wget https://raw.githubusercontent.com/ai-cohort-july-2025/AI-Cohort-July-2025/main/.github/workflow-templates/claude-auto-docs.yml \
     -O .github/workflows/claude-auto-docs.yml
   ```

### Step 2: API Key Configuration

1. **Get Anthropic API Key**
   - Visit [Anthropic Console](https://console.anthropic.com/)
   - Create account or sign in
   - Generate new API key
   - Copy the key (starts with `sk-ant-`)

2. **Add to Repository Secrets**
   ```bash
   # Using GitHub CLI
   gh secret set ANTHROPIC_API_KEY --body "sk-ant-your-key-here"
   
   # Or via GitHub UI:
   # Repository → Settings → Secrets and Variables → Actions → New Repository Secret
   # Name: ANTHROPIC_API_KEY
   # Value: sk-ant-your-key-here
   ```

### Step 3: Workflow Customization

1. **Basic Configuration**
   Edit the workflow file to customize for your repository:
   
   ```yaml
   # .github/workflows/claude-auto-docs.yml
   env:
     DOCS_DIR: 'docs'                    # Your documentation directory
     ADR_DIR: 'docs/adr'                 # Architecture Decision Records
     ARCHITECTURE_DIR: 'docs/architecture' # Architecture documentation
     MIN_COMPLEXITY_FOR_PRD: 3           # Complexity threshold for PRD
     MIN_COMPLEXITY_FOR_ADR: 4           # Complexity threshold for ADRs
   ```

2. **Trigger Customization**
   ```yaml
   on:
     push:
       branches: [main, develop]         # Your main branches
     pull_request:
       types: [opened, synchronize]
     workflow_dispatch:                  # Manual trigger
   ```

### Step 4: Repository-Specific Configuration

1. **Create Configuration File** (Optional)
   ```bash
   # Download configuration template
   wget https://raw.githubusercontent.com/ai-cohort-july-2025/AI-Cohort-July-2025/main/.github/workflow-templates/repository-config-template.yml \
     -O .github/repository-config.yml
   ```

2. **Customize Configuration**
   ```yaml
   # .github/repository-config.yml
   repository:
     name: "your-repo-name"
     type: "web-app"  # web-app, library, cli-tool, mobile-app, microservice
     domain: "general" # fintech, healthcare, e-commerce, general
   
   documentation:
     auto_generate:
       prd: true          # Generate Product Requirements Document
       adr: true          # Generate Architecture Decision Records
       architecture: true # Generate architecture documentation
       readme: true       # Enhance README.md
   ```

## 🎯 Generated Artifacts Overview

The automation system generates comprehensive documentation based on repository analysis:

### 1. Product Requirements Document (PRD)
- **File**: `docs/PRD.md`
- **Content**: Business requirements, user stories, success metrics
- **Triggers**: Generated for complex applications (score ≥ 3/10)

### 2. Architecture Decision Records (ADRs)
- **Directory**: `docs/adr/`
- **Content**: Technical decisions, alternatives considered, consequences
- **Triggers**: Generated for architecturally complex projects (score ≥ 4/10)

### 3. Architecture Documentation
- **Directory**: `docs/architecture/`
- **Content**: System diagrams, component design, data flow
- **Features**: Mermaid diagrams, visual documentation

### 4. Enhanced README
- **File**: `README.md`
- **Content**: Professional project overview, setup instructions
- **Features**: Badges, quick start, contribution guidelines

### 5. API Documentation
- **Files**: Various locations based on framework
- **Content**: Endpoint documentation, schemas, examples
- **Integration**: Framework-specific (OpenAPI, JSDoc, etc.)

## ⚙️ Automation Triggers

### Automatic Triggers
- **Push to Main**: Full documentation review and updates
- **Pull Requests**: Incremental documentation updates
- **Releases**: Complete documentation regeneration
- **Issue Labels**: Triggered by `documentation` or `architecture-review` labels

### Manual Triggers
- **Workflow Dispatch**: Manual execution with custom parameters
- **Repository Analysis**: On-demand comprehensive analysis

## 🔧 Customization Options

### 1. Workflow Behavior
```yaml
env:
  AUTO_CREATE_PR: true              # Automatically create PR with changes
  REQUIRE_HUMAN_REVIEW: true        # Flag for human review requirement
  ANALYSIS_DEPTH: 'comprehensive'   # Analysis thoroughness
```

### 2. Quality Thresholds
```yaml
env:
  MIN_COMPLEXITY_FOR_PRD: 3         # 1-10 scale
  MIN_COMPLEXITY_FOR_ADR: 4         # 1-10 scale  
  README_QUALITY_THRESHOLD: 6       # Enhancement threshold
```

### 3. Artifact Selection
```yaml
# Manual trigger with specific artifacts
gh workflow run claude-auto-docs.yml \
  --field artifacts=prd,adr \
  --field force_regenerate=true
```

## 📊 Repository Analysis Framework

The automation uses sophisticated analysis to understand your repository:

### Technology Detection
- **Languages**: Python, JavaScript, TypeScript, Go, Rust, Java, etc.
- **Frameworks**: React, FastAPI, Django, Express, Spring, etc.
- **Databases**: PostgreSQL, MongoDB, Redis, SQLite, etc.
- **Deployment**: Docker, Kubernetes, AWS, GCP, Azure, etc.

### Complexity Assessment
- **Code Metrics**: Lines of code, file count, module complexity
- **Architecture**: Patterns, dependencies, integration points
- **Team Indicators**: Contributor count, commit frequency

### Documentation Gap Analysis
- **Existing Docs**: Quality assessment, completeness check
- **Missing Artifacts**: Identified documentation needs
- **Consistency Issues**: Style and terminology problems

## 🔍 Quality Assurance

### Automated Validation
- **Markdown Syntax**: Lint checking and formatting
- **Link Validation**: Internal and external link testing  
- **Diagram Rendering**: Mermaid syntax validation
- **Cross-References**: Document consistency checking

### Human Review Integration
- **PR Creation**: Automated pull requests for review
- **Review Assignment**: Suggested reviewers based on expertise
- **Quality Metrics**: Before/after documentation coverage

## 🚀 Advanced Features

### 1. Multi-Repository Deployment
```bash
# Deploy to multiple repositories
for repo in repo1 repo2 repo3; do
  gh api repos/owner/$repo/actions/workflows/claude-auto-docs.yml/dispatches \
    -f ref=main -f inputs='{"artifacts":"all"}'
done
```

### 2. Organization-Wide Templates
```yaml
# .github/workflows/org-auto-docs.yml
name: Organization Documentation Sync
on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly at 2 AM
  workflow_dispatch:

jobs:
  deploy-automation:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        repo: ${{ fromJson(vars.MANAGED_REPOSITORIES) }}
    steps:
      - name: Deploy to ${{ matrix.repo }}
        # Implementation for organization-wide deployment
```

### 3. Custom Prompt Templates
```yaml
# Custom prompts for domain-specific documentation
custom_prompts:
  fintech_prd: |
    Focus on regulatory compliance and security requirements.
    Include PCI DSS and SOX compliance considerations.
    Emphasize audit trails and data protection.
  
  healthcare_architecture: |
    Prioritize HIPAA compliance and data privacy.
    Include security architecture and access controls.
    Document audit and monitoring requirements.
```

## 📈 Monitoring and Metrics

### Workflow Metrics
- **Execution Time**: Track automation performance
- **Success Rates**: Monitor generation success/failure
- **Quality Scores**: Documentation improvement metrics

### Repository Health
- **Documentation Coverage**: Percentage of documented components
- **Freshness Score**: How up-to-date documentation is
- **Consistency Rating**: Cross-document consistency measurement

## 🛠️ Troubleshooting

### Common Issues

**1. API Key Problems**
```bash
# Verify API key is set
gh secret list | grep ANTHROPIC_API_KEY

# Test API key validity
curl -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
  https://api.anthropic.com/v1/messages
```

**2. Workflow Permissions**
```yaml
# Ensure proper permissions in workflow
permissions:
  contents: write      # Required for file creation
  pull-requests: write # Required for PR creation
  id-token: write     # Required for claude-code-action
```

**3. Large Repository Timeouts**
```yaml
# Increase timeout for large repositories
timeout_minutes: "30"  # Default is 10 minutes
```

**4. Branch Protection Rules**
```bash
# Temporarily disable branch protection for automation
gh api repos/owner/repo/branches/main/protection \
  -X DELETE
```

### Debug Mode
```yaml
# Enable debug logging
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

## 🔐 Security Considerations

### API Key Security
- Store API keys in GitHub Secrets (never in code)
- Use organization-level secrets for multiple repositories
- Rotate API keys regularly
- Monitor API usage for anomalies

### Workflow Security
- Use specific action versions (not `@main`)
- Review generated content before merging
- Implement branch protection rules
- Require human approval for sensitive changes

### Content Security
- Exclude sensitive files from analysis
- Review generated documentation for confidential information
- Implement automated security scanning of generated content

## 📚 Examples and Templates

### Example 1: Web Application
```yaml
# Optimized for React/FastAPI web applications
repository:
  type: "web-app"
  tech_stack:
    frontend: ["react", "typescript"]
    backend: ["fastapi", "python"]
    database: ["postgresql"]
documentation:
  auto_generate:
    prd: true
    adr: true
    architecture: true
    api_docs: true
```

### Example 2: Python Library
```yaml
# Optimized for Python packages
repository:
  type: "library"
  tech_stack:
    primary: "python"
documentation:
  auto_generate:
    prd: false
    adr: true 
    api_docs: true
  custom_sections:
    - "Installation Guide"
    - "API Reference"
    - "Examples"
```

### Example 3: Microservices
```yaml
# Optimized for microservice architectures
repository:
  type: "microservice"
documentation:
  thresholds:
    min_complexity_for_adr: 2  # Lower threshold for microservices
  auto_generate:
    architecture: true
    api_docs: true
  custom_sections:
    - "Service Interface"
    - "Deployment Guide"
    - "Monitoring"
```

## 🚀 Getting Started Checklist

- [ ] Copy workflow file to `.github/workflows/`
- [ ] Add `ANTHROPIC_API_KEY` to repository secrets
- [ ] Customize workflow configuration for your repository
- [ ] Create optional repository configuration file
- [ ] Test with manual workflow dispatch
- [ ] Review generated documentation PR
- [ ] Merge and enable automatic triggers
- [ ] Monitor workflow execution and quality metrics
- [ ] Share with team and gather feedback
- [ ] Scale to additional repositories

## 🤝 Support and Contributing

### Getting Help
- **Documentation Issues**: [Create an issue](https://github.com/ai-cohort-july-2025/AI-Cohort-July-2025/issues)
- **Workflow Problems**: Check troubleshooting section above
- **Feature Requests**: Submit enhancement proposals

### Contributing Improvements
- **Workflow Enhancements**: Submit PRs with improvements
- **Template Additions**: Contribute repository-specific templates
- **Documentation**: Help improve setup and usage guides

---

**Claude Automation Suite** - Transform any repository into a documentation powerhouse with AI-powered automation. Copy, configure, and deploy in minutes!