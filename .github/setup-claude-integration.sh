#!/bin/bash
# Claude GitHub Integration Setup Script
# AutoDevHub - AI-Powered DevOps Tracker

set -e

echo "🤖 Claude GitHub Integration Setup"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) is required but not installed${NC}"
    echo "Please install from: https://cli.github.com/"
    echo "Then run: gh auth login"
    exit 1
fi

echo -e "${GREEN}✅ GitHub CLI found${NC}"

# Check GitHub authentication
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not authenticated with GitHub${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

echo -e "${GREEN}✅ GitHub authentication verified${NC}"

# Check repository access
REPO_INFO=$(gh repo view --json name,owner,url 2>/dev/null || echo "")
if [ -z "$REPO_INFO" ]; then
    echo -e "${RED}❌ Cannot access repository${NC}"
    echo "Make sure you're in the correct repository directory"
    exit 1
fi

REPO_NAME=$(echo "$REPO_INFO" | jq -r '.name')
OWNER=$(echo "$REPO_INFO" | jq -r '.owner.login')
echo -e "${GREEN}✅ Repository access: ${OWNER}/${REPO_NAME}${NC}"

echo ""
echo "🔑 API Key Configuration"
echo "========================"

# Check if ANTHROPIC_API_KEY already exists
if gh secret list | grep -q "ANTHROPIC_API_KEY"; then
    echo -e "${GREEN}✅ ANTHROPIC_API_KEY already configured${NC}"
    read -p "Do you want to update it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping API key update"
    else
        echo "Please enter your Anthropic API Key:"
        gh secret set ANTHROPIC_API_KEY
        echo -e "${GREEN}✅ API key updated${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  ANTHROPIC_API_KEY not found${NC}"
    echo ""
    echo "To configure the API key:"
    echo "1. Visit: https://console.anthropic.com/"
    echo "2. Sign in or create an account"
    echo "3. Go to API keys section"
    echo "4. Generate a new API key"
    echo ""
    read -p "Do you have your API key ready? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Please enter your Anthropic API Key:"
        gh secret set ANTHROPIC_API_KEY
        echo -e "${GREEN}✅ API key configured${NC}"
    else
        echo -e "${YELLOW}⚠️  API key setup skipped${NC}"
        echo "You can configure it later with: gh secret set ANTHROPIC_API_KEY"
    fi
fi

echo ""
echo "🧪 Testing Integration"
echo "====================="

# Check workflows
WORKFLOWS=$(gh workflow list --json name,state | jq -r '.[] | select(.name | contains("Claude")) | .name')
if [ -z "$WORKFLOWS" ]; then
    echo -e "${YELLOW}⚠️  No Claude workflows found${NC}"
else
    echo -e "${GREEN}✅ Claude workflows found:${NC}"
    echo "$WORKFLOWS" | sed 's/^/  - /'
fi

echo ""
echo "🚀 Integration Test"
echo "=================="

# Test if we can run a workflow
if gh workflow list | grep -q "Claude Integration Test"; then
    echo -e "${BLUE}Running integration test...${NC}"
    RUN_ID=$(gh workflow run "Claude Integration Test" --field test_type=api-key-validation --json | jq -r '.url // empty')
    if [ -n "$RUN_ID" ]; then
        echo -e "${GREEN}✅ Integration test started${NC}"
        echo "View results at: ${RUN_ID}"
    else
        echo -e "${YELLOW}⚠️  Could not start integration test${NC}"
        echo "You can manually run it from the Actions tab"
    fi
else
    echo -e "${YELLOW}⚠️  Integration test workflow not found${NC}"
fi

echo ""
echo "📚 Usage Instructions"
echo "===================="
echo ""
echo "1. Interactive Mode:"
echo "   - Comment '@claude please review this code' in PRs"
echo "   - Use '@claude' in issues for assistance"
echo ""
echo "2. Automatic Mode:"
echo "   - New PRs automatically get reviewed"
echo "   - Manual dispatch available in Actions tab"
echo ""
echo "3. Available Workflows:"
echo "   - Claude PR Assistant (responds to @claude mentions)"
echo "   - Automatic PR Review (reviews all new PRs)"
echo "   - Claude Integration Test (manual testing)"
echo "   - Claude Commit Analysis (manual analysis)"
echo ""
echo "📖 Full documentation: .github/CLAUDE_INTEGRATION_GUIDE.md"
echo ""

# Final status
if gh secret list | grep -q "ANTHROPIC_API_KEY"; then
    echo -e "${GREEN}🎉 Claude GitHub Integration Setup Complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Test with a sample PR or issue"
    echo "2. Monitor workflow execution in Actions tab"
    echo "3. Review integration guide for advanced features"
else
    echo -e "${YELLOW}⚠️  Setup partially complete${NC}"
    echo ""
    echo "Missing: ANTHROPIC_API_KEY"
    echo "Configure with: gh secret set ANTHROPIC_API_KEY"
fi

echo ""
echo "🆘 Need help? Check the troubleshooting section in:"
echo "   .github/CLAUDE_INTEGRATION_GUIDE.md"