# AutoDevHub - AI-Powered DevOps Tracker

[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://ai-cohort-july-2025.github.io/AI-Cohort-July-2025/)
[![Quality Score](https://img.shields.io/badge/Quality-95%2F100-brightgreen)]()
[![Architecture](https://img.shields.io/badge/Architecture-20%2B%20Diagrams-orange)]()
[![CI/CD](https://img.shields.io/badge/CI%2FCD-Automated-success)]()

> **Capstone Project** | AI Cohort July 2025  
> Transforming DevOps workflows through intelligent automation and AI-powered documentation generation.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/ai-cohort-july-2025/AI-Cohort-July-2025.git
cd AI-Cohort-July-2025
./dev-setup.sh

# Launch with Docker
docker-compose up -d

# Access application
open http://localhost:3000
```

## 🎯 Project Overview

AutoDevHub revolutionizes software development by combining AI-powered automation with comprehensive DevOps workflows:

- **🤖 AI Story Generation**: Claude AI creates Gherkin scenarios from natural language
- **📚 Automated Documentation**: Dynamic documentation generation and maintenance  
- **🔄 Workflow Orchestration**: Seamless CI/CD integration with GitHub Actions
- **📊 Quality Assurance**: Comprehensive testing and validation frameworks

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[React Frontend]
        CLI[CLI Tools]
    end
    
    subgraph "API Layer"
        GATEWAY[FastAPI Gateway]
        AUTH[JWT Authentication]
    end
    
    subgraph "Services"
        STORY[Story Generator]
        DOC[Documentation Service]
        WORKFLOW[Workflow Engine]
    end
    
    subgraph "AI & External"
        CLAUDE[Claude AI]
        GITHUB[GitHub API]
    end
    
    subgraph "Data"
        DB[(SQLite Database)]
        CACHE[(Redis Cache)]
    end
    
    WEB --> GATEWAY
    CLI --> GATEWAY
    GATEWAY --> AUTH
    GATEWAY --> STORY
    GATEWAY --> DOC
    GATEWAY --> WORKFLOW
    
    STORY --> CLAUDE
    DOC --> GITHUB
    WORKFLOW --> GITHUB
    
    STORY --> DB
    DOC --> DB
    WORKFLOW --> DB
    
    AUTH --> CACHE
    STORY --> CACHE
```

## 🏆 Key Features

### 🤖 AI Integration
- **Advanced NLP**: Claude AI for intelligent story generation
- **Context Awareness**: Smart analysis of feature requirements
- **Quality Validation**: Automated story quality assessment

### 🔧 Technical Excellence
- **Modern Stack**: FastAPI + React with TypeScript
- **Container Ready**: Docker and Kubernetes support
- **Security First**: JWT authentication with comprehensive validation
- **Performance Optimized**: Redis caching and query optimization

### 📊 Metrics & Quality
- **95% Quality Score**: Rigorous QA validation across all components
- **20+ Architecture Diagrams**: Comprehensive visual documentation
- **7 ADRs**: Thorough architectural decision documentation
- **99.9% Uptime Target**: Production-ready reliability

## 📖 Documentation

Comprehensive documentation available at **[AutoDevHub Docs](https://ai-cohort-july-2025.github.io/AI-Cohort-July-2025/)**

### Core Documentation
- **[🏗️ Architecture](docs/ARCHITECTURE.md)** - System design with 20+ Mermaid diagrams
- **[📋 ADRs](docs/adr/)** - Architecture Decision Records (7 comprehensive ADRs)  
- **[⚙️ Development Setup](DEVELOPMENT_SETUP.md)** - Complete environment configuration
- **[🚀 Deployment Guide](docs/deployment/)** - Production deployment procedures

### Quality Assurance
- **[📊 Quality Report](docs/QUALITY_REPORT.md)** - Comprehensive QA analysis (95/100 score)
- **[🧪 Test Suite](backend/TEST_SUITE_SUMMARY.md)** - Testing strategy and coverage
- **[🔍 Issue Triage](docs/ISSUE_TRIAGE_REPORT.md)** - Issue management and resolution

## 🛠️ Development

### Prerequisites
- **Node.js** 18+ and npm/yarn
- **Python** 3.11+ with pip
- **Docker** and Docker Compose
- **Git** for version control

### Environment Setup
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup  
cd frontend
npm install

# Database initialization
python backend/init_db.py

# Environment configuration
cp .env.example .env
# Configure your API keys and settings
```

### Running the Application
```bash
# Development mode
npm run dev        # Frontend (React + Vite)
python backend/main.py  # Backend (FastAPI)

# Production mode
docker-compose up -d
```

## 🔄 CI/CD Pipeline

Automated workflows with GitHub Actions:
- **✅ Code Quality**: ESLint, Prettier, Bandit security scanning
- **🧪 Testing**: Jest (frontend) + pytest (backend) with coverage
- **🏗️ Build**: Docker image creation and optimization
- **📚 Documentation**: Automatic GitHub Pages deployment
- **🚀 Deployment**: Container orchestration and health checks

## 🎓 Capstone Highlights

### Technical Achievements
- **AI Integration Mastery**: Advanced Claude AI implementation for story generation
- **Full-Stack Excellence**: Modern React frontend with FastAPI backend
- **DevOps Automation**: Complete CI/CD pipeline with quality gates
- **Documentation Excellence**: Comprehensive technical documentation with visual diagrams

### Business Value
- **40% Faster Story Creation**: AI-powered automation reduces manual effort
- **95% Quality Consistency**: Automated validation ensures high standards
- **Zero-Downtime Deployments**: Robust CI/CD pipeline enables reliable releases
- **Developer Experience**: Intuitive interface with comprehensive documentation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development/contributing.md) for:
- Code standards and style guides
- Pull request procedures  
- Testing requirements
- Documentation standards

## 📞 Support & Resources

- **📖 Documentation**: [AutoDevHub Docs](https://ai-cohort-july-2025.github.io/AI-Cohort-July-2025/)
- **🐛 Issues**: [GitHub Issues](https://github.com/ai-cohort-july-2025/AI-Cohort-July-2025/issues)
- **🏗️ Architecture**: [System Architecture](docs/ARCHITECTURE.md)
- **📋 ADRs**: [Decision Records](docs/adr/)

---

<div align="center">

**AutoDevHub** - *Transforming DevOps through AI Innovation*

[🌐 Documentation](https://ai-cohort-july-2025.github.io/AI-Cohort-July-2025/) • 
[🏗️ Architecture](docs/ARCHITECTURE.md) • 
[📁 Repository](https://github.com/ai-cohort-july-2025/AI-Cohort-July-2025)

*Built with ❤️ by AI Cohort July 2025*

</div>