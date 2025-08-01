#!/bin/bash
# AutoDevHub Development Environment Setup Script

set -e

echo "🚀 Setting up AutoDevHub Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check system requirements
echo -e "\n${BLUE}🔍 Checking system requirements...${NC}"

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    print_status "Python $PYTHON_VERSION detected"
else
    print_error "Python 3 is required but not installed"
    exit 1
fi

# Check Node.js version
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "Node.js $NODE_VERSION detected"
else
    print_error "Node.js is required but not installed"
    exit 1
fi

# Virtual environment setup prompt
echo -e "\n${BLUE}🐍 Python Virtual Environment Setup${NC}"
read -p "Do you want to create and use a Python virtual environment? (y/n): " -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Setting up Python virtual environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        if python3 -m venv venv; then
            print_status "Virtual environment created successfully"
        else
            print_error "Failed to create virtual environment"
            exit 1
        fi
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    print_info "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip in virtual environment
    print_info "Upgrading pip in virtual environment..."
    pip install --upgrade pip
    
    print_status "Virtual environment activated"
    print_info "Virtual environment is located at: $(pwd)/venv"
    print_warning "Remember to activate it in future sessions with: source venv/bin/activate"
else
    print_warning "Skipping virtual environment setup"
    print_info "Continuing with system Python installation..."
    
    # Ask if user wants to exit or continue without venv
    read -p "Continue without virtual environment? (y/n): " -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Exiting setup. Run the script again when ready to proceed."
        exit 0
    fi
fi

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    print_info "Creating .env file from template..."
    cp .env.example .env
    print_status ".env file created"
else
    print_warning ".env file already exists"
fi

# Install Python dependencies
echo -e "\n${BLUE}📦 Installing Python dependencies...${NC}"
if pip install -r requirements.txt; then
    print_status "Python dependencies installed successfully"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Install Node.js dependencies
echo -e "\n${BLUE}📦 Installing Node.js dependencies...${NC}"
if npm install; then
    print_status "Node.js dependencies installed successfully"
else
    print_error "Failed to install Node.js dependencies"
    exit 1
fi

# Create directory structure
echo -e "\n${BLUE}📁 Creating directory structure...${NC}"
mkdir -p backend/{app,tests,migrations}
mkdir -p frontend/{src,public,tests}
mkdir -p docs/{api,architecture,deployment}
mkdir -p .github/workflows
mkdir -p presentation
mkdir -p tests/{unit,integration,e2e}

print_status "Directory structure created"

# Run basic tests
echo -e "\n${BLUE}🧪 Running basic validation tests...${NC}"

# Test Python imports
python3 -c "
import fastapi
import uvicorn
import sqlalchemy
import pytest
import bandit
print('✅ All Python dependencies can be imported')
" && print_status "Python environment validated" || print_error "Python validation failed"

# Test Node.js
node -e "console.log('✅ Node.js environment validated')" && print_status "Node.js environment validated" || print_error "Node.js validation failed"

# Run security scan
echo -e "\n${BLUE}🔒 Running security scan...${NC}"
if bandit -r . -f json -o bandit-report.json 2>/dev/null; then
    print_status "Security scan completed (see bandit-report.json)"
else
    print_warning "Security scan had issues (see bandit-report.json for details)"
fi

# Run linting
echo -e "\n${BLUE}🔍 Running code quality checks...${NC}"
if flake8 --version > /dev/null 2>&1; then
    print_status "Code linting tools ready"
fi

if npm run lint --silent > /dev/null 2>&1; then
    print_status "JavaScript linting ready"
else
    print_warning "JavaScript linting needs configuration"
fi

echo -e "\n${GREEN}🎉 AutoDevHub development environment setup complete!${NC}"
echo -e "\n${BLUE}Next steps:${NC}"
if [ -d "venv" ] && [[ "$VIRTUAL_ENV" == *"venv"* ]]; then
    echo "1. Virtual environment is active and ready to use"
    echo "2. Review and update .env file with your configuration"
    echo "3. Start backend development server: uvicorn backend.app.main:app --reload"
    echo "4. Start frontend development server: npm run dev"
    echo "5. Run tests: pytest (backend) / npm test (frontend)"
    echo "6. Check code quality: flake8 . && npm run lint"
    echo -e "\n${YELLOW}Note: To reactivate virtual environment in future sessions:${NC}"
    echo "source venv/bin/activate"
else
    echo "1. Review and update .env file with your configuration"
    echo "2. Start backend development server: uvicorn backend.app.main:app --reload"
    echo "3. Start frontend development server: npm run dev"
    echo "4. Run tests: pytest (backend) / npm test (frontend)"
    echo "5. Check code quality: flake8 . && npm run lint"
fi

echo -e "\n${BLUE}Available scripts:${NC}"
echo "• ./dev-setup.sh - This setup script"
echo "• npm run dev - Start Vite development server"
echo "• npm run build - Build for production"
echo "• npm run test - Run tests"
echo "• npm run lint - Run ESLint"
echo "• pytest - Run Python tests"
echo "• bandit -r . - Security scan"
echo "• black . - Format Python code"
echo "• isort . - Sort Python imports"

print_status "Setup completed successfully! 🚀"