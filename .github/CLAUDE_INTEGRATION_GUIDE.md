# Claude GitHub App Integration Guide

## 🎯 Overview

This guide provides complete setup instructions for integrating Claude GitHub App with the AutoDevHub repository to enable AI-powered development assistance.

## 🚨 Status: PARTIALLY CONFIGURED

The repository already has Claude GitHub workflows configured but requires API key setup to be fully functional.

## 📋 Current Configuration Analysis

### ✅ Already Configured:
- **Claude Code Action workflows** in `.github/workflows/`
- **Pull Request Assistant** (`claude.yml`) - responds to @claude mentions
- **Automatic PR Review** (`auto.yml`) - reviews all new PRs
- **Mode Examples** (`modes.yml`) - demonstrates tag vs agent modes
- **Manual Dispatch** (`workflow-dispatch-agent.yml`) - on-demand analysis

### ⚠️ Requires Setup:
- **ANTHROPIC_API_KEY** repository secret
- **Permissions verification** for Claude Code Action
- **Team documentation** for usage patterns

## 🔧 Setup Steps

### Step 1: Configure API Key (CRITICAL)

The workflows reference `${{ secrets.ANTHROPIC_API_KEY }}` which must be configured:

1. **Get Anthropic API Key**:
   - Visit: https://console.anthropic.com/
   - Create account or sign in
   - Navigate to API keys section
   - Generate a new API key for this repository

2. **Add Repository Secret**:
   ```bash
   # Using GitHub CLI (recommended)
   gh secret set ANTHROPIC_API_KEY
   # You'll be prompted to paste your API key
   
   # Or via GitHub web interface:
   # 1. Go to repository Settings
   # 2. Navigate to Secrets and variables > Actions
   # 3. Click "New repository secret"
   # 4. Name: ANTHROPIC_API_KEY
   # 5. Value: [your-api-key]
   ```

3. **Verify Secret**:
   ```bash
   # Check that secret exists (won't show value)
   gh secret list
   ```

### Step 2: Verify Workflow Permissions

Current workflows have these permissions configured:
- `contents: read/write` - Read repository content, create commits
- `pull-requests: read/write` - Review and comment on PRs
- `issues: read/write` - Manage issues and comments
- `id-token: write` - GitHub Actions authentication

These are appropriate for Claude's operations.

### Step 3: Test Integration

Test the integration with a sample operation:

1. **Test Manual Dispatch**:
   ```bash
   # Run the commit analysis workflow
   gh workflow run "Claude Commit Analysis" --field analysis_type=summarize-commit
   ```

2. **Test @claude Mentions**:
   - Create a test PR or issue
   - Add comment with "@claude please review this code"
   - Claude should respond within 10 minutes

3. **Test Automatic Review**:
   - Create a new PR
   - The auto-review workflow should trigger immediately
   - Check Actions tab for workflow execution

## 📚 Usage Documentation for Team

### Claude Interaction Modes

#### 1. Tag Mode (Interactive)
**Trigger**: @claude mentions in comments, issues, PRs
**Best for**: Interactive Q&A, on-demand code changes

```markdown
@claude please review this API endpoint for security issues

@claude help me optimize this database query

@claude explain how this authentication flow works
```

#### 2. Agent Mode (Automatic)
**Trigger**: Automatic on PR creation, workflow dispatch
**Best for**: CI/CD integration, automatic reviews

- Runs immediately without @claude mention
- Provides consistent code quality checks
- Integrates with CI/CD pipelines

### Available Workflows

#### 1. Claude PR Assistant (`claude.yml`)
- **Triggers**: @claude mentions in comments/reviews
- **Features**: Interactive assistance, code explanations
- **Timeout**: 10 minutes
- **Permissions**: Read repo, write PR comments

#### 2. Automatic PR Review (`auto.yml`)
- **Triggers**: New PRs, workflow dispatch
- **Features**: Comprehensive code review
- **Focus**: Quality, security, performance, testing
- **Timeout**: 10 minutes

#### 3. Manual Analysis (`workflow-dispatch-agent.yml`)
- **Triggers**: Manual dispatch only
- **Options**: Commit summary, security review
- **Use case**: On-demand analysis of specific commits

#### 4. Mode Examples (`modes.yml`)
- **Purpose**: Demonstrates different interaction patterns
- **Includes**: Tag mode and agent mode examples
- **Educational**: Shows best practices

## 🔒 Security Considerations

### API Key Security
- ✅ API key stored as GitHub secret (encrypted)
- ✅ Not exposed in workflow logs
- ✅ Limited to repository scope
- ✅ Can be rotated as needed

### Workflow Permissions
- ✅ Minimal necessary permissions
- ✅ Read-only access to sensitive data
- ✅ Write access limited to comments/reviews
- ✅ No admin or settings permissions

### Network Security
- Optional domain restrictions available:
  ```yaml
  experimental_allowed_domains: |
    .anthropic.com
    .github.com
    api.github.com
    .githubusercontent.com
  ```

## 🚀 Advanced Configuration

### Custom Prompts
Modify workflow files to customize Claude's behavior:

```yaml
override_prompt: |
  Review this code focusing on:
  - AutoDevHub specific patterns
  - FastAPI best practices
  - React component structure
  - Database security
```

### Timeout Configuration
Adjust timeout for complex operations:
```yaml
timeout_minutes: "15"  # Default is 10
```

### Tool Restrictions
Limit available tools for security:
```yaml
allowed_tools: "mcp__github__create_pending_pull_request_review,mcp__github__add_comment_to_pending_review"
```

## 🎯 Integration with AutoDevHub Features

### AI-Powered Development Workflows
1. **Story Generation Review**: Claude reviews generated user stories
2. **API Endpoint Analysis**: Automatic FastAPI code review
3. **React Component Review**: Frontend code quality checks
4. **Database Migration Review**: SQL and ORM validation
5. **Test Coverage Analysis**: Identifies missing test cases

### Workflow Integration Points
- **Pre-commit hooks**: Optional Claude validation
- **PR templates**: Include @claude review requests
- **Issue templates**: AI assistance for bug analysis
- **Release preparation**: Automated release notes with Claude

## 📊 Monitoring and Analytics

### Workflow Execution
Monitor Claude integration through:
- GitHub Actions logs
- Workflow run history
- Success/failure rates
- Response times

### Usage Metrics
Track Claude usage:
- API call frequency
- Token consumption
- Feature utilization
- Team adoption rates

## 🐛 Troubleshooting

### Common Issues

#### 1. "ANTHROPIC_API_KEY not found"
**Solution**: Verify repository secret is configured correctly
```bash
gh secret list  # Check if secret exists
```

#### 2. "HTTP 403: Forbidden"
**Solution**: Check API key validity and permissions
- Generate new API key
- Update repository secret

#### 3. "Workflow timeout"
**Solution**: Increase timeout or optimize prompts
```yaml
timeout_minutes: "15"
```

#### 4. "No response from Claude"
**Solution**: Check workflow triggers and permissions
- Verify @claude mention format
- Check Actions tab for execution logs

### Debug Commands
```bash
# Check workflow status
gh run list --workflow="Claude PR Assistant"

# View workflow logs
gh run view [run-id] --log

# Test repository access
gh api repos/tbowman01/AI-Cohort-July-2025
```

## 📈 Success Metrics

### Integration Health
- ✅ API key configured and valid
- ✅ Workflows executing successfully
- ✅ Team actively using @claude mentions
- ✅ PR reviews being enhanced by AI
- ✅ Code quality metrics improving

### Usage Indicators
- PR comments with Claude responses
- Workflow execution history
- Reduced manual review time
- Improved code quality scores

## 🚀 Next Steps

1. **Configure API Key** (PRIORITY 1)
2. **Test Integration** with sample PR
3. **Train Team** on usage patterns
4. **Monitor Usage** and optimize
5. **Expand Integration** to other repositories

## 📞 Support Resources

- **Claude Documentation**: https://docs.anthropic.com/claude/docs
- **GitHub Actions**: https://docs.github.com/actions
- **API Reference**: https://docs.anthropic.com/claude/reference
- **Repository Issues**: Create issue with `ai-integration` label

---

**Status**: 🟡 Ready for API key configuration  
**Last Updated**: 2025-07-31  
**Repository**: tbowman01/AI-Cohort-July-2025  
**Integration Level**: Advanced workflows configured, awaiting API key