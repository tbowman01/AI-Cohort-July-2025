#!/bin/bash
# Claude Automation Setup Script
# Automated setup for claude-code-action@beta documentation generation
# Usage: ./setup-claude-automation.sh [repository-type] [api-key]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
GITHUB_WORKFLOWS_DIR=".github/workflows"
DOCS_DIR="docs"
TEMPLATES_BASE_URL="https://raw.githubusercontent.com/ai-cohort-july-2025/AI-Cohort-July-2025/main"

# Default values
REPO_TYPE="${1:-web-app}"
API_KEY="${2:-}"
WORKFLOW_NAME="claude-auto-docs.yml"
CONFIG_NAME="repository-config.yml"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository. Please run this script from the root of your git repository."
        exit 1
    fi
    
    # Check if GitHub CLI is available
    if ! command -v gh &> /dev/null; then
        print_warning "GitHub CLI (gh) not found. API key will need to be set manually."
        GITHUB_CLI_AVAILABLE=false
    else
        GITHUB_CLI_AVAILABLE=true
    fi
    
    # Check if curl is available
    if ! command -v curl &> /dev/null; then
        print_error "curl is required but not found. Please install curl."
        exit 1
    fi
    
    print_success "Prerequisites check completed"
}

# Function to create directory structure
create_directories() {
    print_status "Creating directory structure..."
    
    # Create necessary directories
    mkdir -p "$GITHUB_WORKFLOWS_DIR"
    mkdir -p "$DOCS_DIR"
    mkdir -p "$DOCS_DIR/adr"
    mkdir -p "$DOCS_DIR/architecture"
    mkdir -p ".github"
    
    print_success "Directory structure created"
}

# Function to download workflow template
download_workflow() {
    print_status "Downloading workflow template..."
    
    local workflow_url="$TEMPLATES_BASE_URL/.github/workflow-templates/claude-auto-docs.yml"
    local workflow_path="$GITHUB_WORKFLOWS_DIR/$WORKFLOW_NAME"
    
    if curl -fsSL "$workflow_url" -o "$workflow_path"; then
        print_success "Workflow template downloaded to $workflow_path"
    else
        print_error "Failed to download workflow template"
        exit 1
    fi
}

# Function to download configuration template
download_config() {
    print_status "Downloading configuration template..."
    
    local config_url="$TEMPLATES_BASE_URL/.github/workflow-templates/repository-config-template.yml"
    local config_path=".github/$CONFIG_NAME"
    
    if curl -fsSL "$config_url" -o "$config_path"; then
        print_success "Configuration template downloaded to $config_path"
    else
        print_warning "Failed to download configuration template (optional)"
    fi
}

# Function to customize workflow for repository type
customize_workflow() {
    print_status "Customizing workflow for repository type: $REPO_TYPE"
    
    local workflow_path="$GITHUB_WORKFLOWS_DIR/$WORKFLOW_NAME"
    
    # Repository type specific customizations
    case "$REPO_TYPE" in
        "web-app")
            sed -i.bak 's/MIN_COMPLEXITY_FOR_PRD: 3/MIN_COMPLEXITY_FOR_PRD: 3/' "$workflow_path"
            sed -i.bak 's/MIN_COMPLEXITY_FOR_ADR: 4/MIN_COMPLEXITY_FOR_ADR: 4/' "$workflow_path"
            ;;
        "library")
            sed -i.bak 's/MIN_COMPLEXITY_FOR_PRD: 3/MIN_COMPLEXITY_FOR_PRD: 5/' "$workflow_path"
            sed -i.bak 's/MIN_COMPLEXITY_FOR_ADR: 4/MIN_COMPLEXITY_FOR_ADR: 3/' "$workflow_path"
            ;;
        "microservice")
            sed -i.bak 's/MIN_COMPLEXITY_FOR_PRD: 3/MIN_COMPLEXITY_FOR_PRD: 2/' "$workflow_path"
            sed -i.bak 's/MIN_COMPLEXITY_FOR_ADR: 4/MIN_COMPLEXITY_FOR_ADR: 2/' "$workflow_path"
            ;;
        "cli-tool")
            sed -i.bak 's/MIN_COMPLEXITY_FOR_PRD: 3/MIN_COMPLEXITY_FOR_PRD: 4/' "$workflow_path"
            sed -i.bak 's/MIN_COMPLEXITY_FOR_ADR: 4/MIN_COMPLEXITY_FOR_ADR: 3/' "$workflow_path"
            ;;
        *)
            print_warning "Unknown repository type: $REPO_TYPE. Using default configuration."
            ;;
    esac
    
    # Remove backup file
    rm -f "$workflow_path.bak"
    
    print_success "Workflow customized for $REPO_TYPE"
}

# Function to set up API key
setup_api_key() {
    if [ -n "$API_KEY" ]; then
        print_status "Setting up API key..."
        
        if [ "$GITHUB_CLI_AVAILABLE" = true ]; then
            if gh secret set ANTHROPIC_API_KEY --body "$API_KEY"; then
                print_success "API key set successfully using GitHub CLI"
            else
                print_error "Failed to set API key using GitHub CLI"
                print_manual_api_key_instructions
            fi
        else
            print_manual_api_key_instructions
        fi
    else
        print_warning "No API key provided. You'll need to set it manually."
        print_manual_api_key_instructions
    fi
}

# Function to print manual API key setup instructions
print_manual_api_key_instructions() {
    echo ""
    print_status "Manual API Key Setup Instructions:"
    echo "1. Go to your repository on GitHub"
    echo "2. Navigate to Settings → Secrets and variables → Actions"
    echo "3. Click 'New repository secret'"
    echo "4. Name: ANTHROPIC_API_KEY"
    echo "5. Value: Your Anthropic API key (starts with sk-ant-)"
    echo ""
}

# Function to create initial documentation structure
create_initial_docs() {
    print_status "Creating initial documentation structure..."
    
    # Create ADR index if it doesn't exist
    if [ ! -f "$DOCS_DIR/adr/index.md" ]; then
        cat > "$DOCS_DIR/adr/index.md" << EOF
# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for this project.

## Index

ADRs will be automatically generated and listed here by the Claude automation system.

## Format

Each ADR follows the standard format:
- **Status**: Proposed, Accepted, Deprecated, or Superseded
- **Context**: The situation requiring a decision
- **Decision**: The specific choice made
- **Consequences**: Positive and negative outcomes
- **Alternatives**: Other options considered

## Automated Generation

ADRs are automatically generated based on architectural decisions detected in the codebase. The system analyzes:
- Technology choices and frameworks
- Design patterns and architectural styles
- Database and storage decisions
- Security and deployment strategies
EOF
        print_success "Created ADR index"
    fi
    
    # Create architecture docs index if it doesn't exist
    if [ ! -f "$DOCS_DIR/architecture/index.md" ]; then
        cat > "$DOCS_DIR/architecture/index.md" << EOF
# Architecture Documentation

This directory contains comprehensive architecture documentation for this project.

## Documents

Architecture documentation is automatically generated and maintained by the Claude automation system.

### Generated Documentation
- **System Overview**: High-level architecture and component relationships
- **Component Architecture**: Detailed component design and interfaces
- **Data Architecture**: Database schema and data flow patterns
- **Deployment Architecture**: Infrastructure and deployment strategies
- **Security Architecture**: Security controls and threat mitigation

## Diagrams

All architecture diagrams are generated using Mermaid syntax for maintainability and version control compatibility.
EOF
        print_success "Created architecture index"
    fi
}

# Function to detect repository characteristics
detect_repository_info() {
    print_status "Detecting repository characteristics..."
    
    local repo_name
    repo_name=$(basename "$(git rev-parse --show-toplevel)")
    
    # Detect primary language
    local primary_language="unknown"
    if [ -f "package.json" ]; then
        primary_language="javascript"
    elif [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
        primary_language="python"
    elif [ -f "Cargo.toml" ]; then
        primary_language="rust"
    elif [ -f "go.mod" ]; then
        primary_language="go"
    elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
        primary_language="java"
    fi
    
    # Detect frameworks
    local frameworks=""
    if [ -f "package.json" ] && grep -q "react" package.json; then
        frameworks="$frameworks react"
    fi
    if [ -f "requirements.txt" ] && grep -q "fastapi\|django\|flask" requirements.txt; then
        frameworks="$frameworks $(grep -o "fastapi\|django\|flask" requirements.txt | head -1)"
    fi
    
    print_success "Repository: $repo_name ($primary_language)${frameworks:+ with $frameworks}"
}

# Function to test workflow setup
test_workflow() {
    print_status "Testing workflow setup..."
    
    if [ "$GITHUB_CLI_AVAILABLE" = true ]; then
        # Check if workflow exists
        if gh workflow list | grep -q "$WORKFLOW_NAME"; then
            print_success "Workflow is available in GitHub Actions"
            
            # Offer to run test
            echo ""
            read -p "Would you like to run a test execution? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_status "Triggering test workflow execution..."
                if gh workflow run "$WORKFLOW_NAME" --field artifacts=readme; then
                    print_success "Test workflow triggered successfully"
                    print_status "Check the Actions tab in your GitHub repository for execution status"
                else
                    print_warning "Failed to trigger test workflow (may need to push changes first)"
                fi
            fi
        else
            print_warning "Workflow not yet available (may need to push changes first)"
        fi
    else
        print_status "GitHub CLI not available - skipping workflow test"
    fi
}

# Function to print setup summary
print_setup_summary() {
    echo ""
    print_success "🎉 Claude Automation Setup Complete!"
    echo ""
    echo "📁 Files Created:"
    echo "   - $GITHUB_WORKFLOWS_DIR/$WORKFLOW_NAME"
    echo "   - .github/$CONFIG_NAME"
    echo "   - $DOCS_DIR/adr/index.md"
    echo "   - $DOCS_DIR/architecture/index.md"
    echo ""
    echo "🚀 Next Steps:"
    echo "   1. Commit and push the changes:"
    echo "      git add ."
    echo "      git commit -m 'feat: add Claude automation for documentation generation'"
    echo "      git push"
    echo ""
    echo "   2. Verify API key is set in repository secrets"
    echo ""
    echo "   3. Test the automation:"
    echo "      gh workflow run $WORKFLOW_NAME --field artifacts=all"
    echo ""
    echo "   4. Customize the configuration in .github/$CONFIG_NAME if needed"
    echo ""
    echo "📚 Documentation:"
    echo "   - Setup Guide: docs/automation/claude-automation-setup.md"
    echo "   - Workflow File: $GITHUB_WORKFLOWS_DIR/$WORKFLOW_NAME"
    echo ""
    print_success "Happy automating! 🤖"
}

# Function to display usage information
show_usage() {
    echo "Claude Automation Setup Script"
    echo ""
    echo "Usage: $0 [repository-type] [api-key]"
    echo ""
    echo "Repository Types:"
    echo "  web-app      - Web applications (React, Vue, etc.)"
    echo "  library      - Code libraries and packages"
    echo "  microservice - Microservice applications"
    echo "  cli-tool     - Command-line tools"
    echo ""
    echo "Examples:"
    echo "  $0 web-app sk-ant-api03-your-key-here"
    echo "  $0 library"
    echo "  $0 microservice sk-ant-api03-your-key-here"
    echo ""
    echo "If no API key is provided, manual setup instructions will be shown."
}

# Main execution function
main() {
    # Check for help flag
    if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
        show_usage
        exit 0
    fi
    
    echo "🤖 Claude Automation Setup Script"
    echo "================================="
    echo ""
    
    # Run setup steps
    check_prerequisites
    detect_repository_info
    create_directories
    download_workflow
    download_config
    customize_workflow
    setup_api_key
    create_initial_docs
    test_workflow
    print_setup_summary
}

# Execute main function
main "$@"