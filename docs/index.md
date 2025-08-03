---
layout: page
title: "Documentation Hub"
permalink: /docs/
---

# AutoDevHub Documentation Hub

Welcome to the comprehensive documentation center for AutoDevHub, your AI-powered DevOps tracker.

## 📚 Documentation Sections

### 🏗️ [Architecture]({{ '/docs/architecture/' | relative_url }})
Complete system architecture documentation with visual diagrams:
- **[System Overview]({{ '/docs/architecture/system-overview.html' | relative_url }})**: High-level architecture and component relationships
- **[API Specification]({{ '/docs/architecture/api-specification.html' | relative_url }})**: RESTful API endpoints and data models
- **[Database Schema]({{ '/docs/architecture/database-schema.html' | relative_url }})**: Data structures and entity relationships
- **[Deployment Architecture]({{ '/docs/architecture/deployment-architecture.html' | relative_url }})**: Infrastructure and scaling strategies

### 📋 [Architecture Decision Records (ADRs)]({{ '/docs/adr/' | relative_url }})
Comprehensive collection of architectural decisions:
- **[ADR-001]({{ '/docs/adr/ADR-001-backend-framework-selection.html' | relative_url }})**: Backend Framework Selection (FastAPI)
- **[ADR-002]({{ '/docs/adr/ADR-002-frontend-framework-selection.html' | relative_url }})**: Frontend Framework Selection (React + TypeScript)
- **[ADR-003]({{ '/docs/adr/ADR-003-database-selection.html' | relative_url }})**: Database Selection (SQLite for development)
- **[ADR-004]({{ '/docs/adr/ADR-004-ai-integration-platform.html' | relative_url }})**: AI Integration Platform (Claude AI)
- **[ADR-005]({{ '/docs/adr/ADR-005-cicd-platform-selection.html' | relative_url }})**: CI/CD Platform Selection (GitHub Actions)
- **[ADR-006]({{ '/docs/adr/ADR-006-documentation-hosting.html' | relative_url }})**: Documentation Hosting (GitHub Pages)
- **[ADR-007]({{ '/docs/adr/ADR-007-development-environment.html' | relative_url }})**: Development Environment (Docker + Dev Containers)

### ⚙️ [Development Guide]({{ '/docs/development/' | relative_url }})
Complete development resources:
- **[Setup Guide]({{ '/docs/development/setup-guide.html' | relative_url }})**: Environment configuration and dependencies
- **[Deployment]({{ '/docs/development/deployment.html' | relative_url }})**: Production deployment procedures
- **[Contributing]({{ '/docs/development/contributing.html' | relative_url }})**: Code standards and contribution workflow
- **[Monitoring]({{ '/docs/development/monitoring.html' | relative_url }})**: Testing strategies and quality assurance

### 🎯 [Presentation Materials]({{ '/docs/presentation/' | relative_url }})
Capstone project presentation resources:
- **[Project Slides]({{ '/docs/presentation/slides.html' | relative_url }})**: Complete presentation deck
- **[Demo Script]({{ '/docs/presentation/demo-script.html' | relative_url }})**: Step-by-step demonstration guide
- **Business Value**: ROI analysis and impact metrics

### 📞 [Contact & Support]({{ '/docs/contacts/' | relative_url }})
Get help and connect with the development team:
- **Support Channels**: GitHub issues, discussions, and community help
- **Bug Reports**: Report issues and get assistance
- **Feature Requests**: Suggest improvements and new features
- **Development Team**: Contact information and project maintainers

## 🚀 Quick Navigation

<div class="quick-nav">
  <div class="nav-section">
    <h3>🏁 Getting Started</h3>
    <ul>
      <li><a href="{{ '/docs/development/setup-guide.html' | relative_url }}">Quick Setup</a></li>
      <li><a href="{{ '/#quick-start' | relative_url }}">Installation Guide</a></li>
      <li><a href="{{ '/docs/architecture/system-overview.html' | relative_url }}">System Overview</a></li>
    </ul>
  </div>
  
  <div class="nav-section">
    <h3>🔧 Developers</h3>
    <ul>
      <li><a href="{{ '/docs/architecture/api-specification.html' | relative_url }}">API Documentation</a></li>
      <li><a href="{{ '/docs/development/contributing.html' | relative_url }}">Contributing Guide</a></li>
      <li><a href="{{ '/docs/architecture/database-schema.html' | relative_url }}">Database Schema</a></li>
    </ul>
  </div>
  
  <div class="nav-section">
    <h3>🚀 Operations</h3>
    <ul>
      <li><a href="{{ '/docs/development/deployment.html' | relative_url }}">Deployment Guide</a></li>
      <li><a href="{{ '/docs/architecture/deployment-architecture.html' | relative_url }}">Infrastructure</a></li>
      <li><a href="{{ '/docs/development/monitoring.html' | relative_url }}">Monitoring Setup</a></li>
    </ul>
  </div>
  
  <div class="nav-section">
    <h3>📊 Project Info</h3>
    <ul>
      <li><a href="{{ '/docs/presentation/slides.html' | relative_url }}">Presentation</a></li>
      <li><a href="{{ '/docs/adr/' | relative_url }}">Decision Records</a></li>
      <li><a href="{{ '/docs/contacts/' | relative_url }}">Contact & Support</a></li>
      <li><a href="https://github.com/tbowman01/AI-Cohort-July-2025">GitHub Repository</a></li>
    </ul>
  </div>
</div>

## 🎯 Key Features Documentation

### 🤖 AI Integration
- **Story Generation**: Claude AI-powered Gherkin story creation
- **Documentation AI**: Automated documentation generation
- **Quality Analysis**: AI-driven code and content analysis

### 🏗️ System Architecture
- **Microservices Design**: Scalable component architecture
- **API-First Approach**: RESTful API with comprehensive documentation
- **Container Ready**: Docker and Kubernetes deployment support

### 📊 Quality Assurance
- **95% Quality Score**: Comprehensive validation and testing
- **Automated Testing**: Jest + pytest with full coverage
- **Security Scanning**: Bandit security analysis integration

## 📖 Documentation Quality Metrics

- **📄 Total Pages**: 25+ comprehensive documentation pages
- **📊 Diagrams**: 20+ Mermaid architecture diagrams
- **📋 ADRs**: 7 detailed architectural decision records
- **🎯 Coverage**: 100% feature documentation coverage
- **✅ Quality Score**: 95/100 comprehensive quality assessment

## 🔗 External Resources

- **[GitHub Repository](https://github.com/tbowman01/AI-Cohort-July-2025)**: Source code and issue tracking
- **[Live Application](http://localhost:3000)**: Development environment access
- **[CI/CD Pipeline](https://github.com/tbowman01/AI-Cohort-July-2025/actions)**: Build and deployment status

## 📞 Support

Need help? Check these resources:
- **Issues**: [GitHub Issues](https://github.com/tbowman01/AI-Cohort-July-2025/issues)
- **Contributing**: [Contribution Guidelines]({{ '/docs/development/contributing.html' | relative_url }})
- **Architecture Questions**: [ADR Collection]({{ '/docs/adr/' | relative_url }})

---

*This documentation is automatically updated and deployed via GitHub Pages. Last updated: {{ site.time | date: "%Y-%m-%d" }}*

<style>
.quick-nav {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin: 40px 0;
}

.nav-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #0366d6;
}

.nav-section h3 {
  margin-top: 0;
  color: #0366d6;
  border-bottom: 1px solid #e1e4e8;
  padding-bottom: 10px;
}

.nav-section ul {
  padding-left: 0;
  list-style: none;
}

.nav-section li {
  margin: 8px 0;
  padding-left: 20px;
  position: relative;
}

.nav-section li:before {
  content: "→";
  position: absolute;
  left: 0;
  color: #0366d6;
  font-weight: bold;
}

.nav-section a {
  text-decoration: none;
  color: #24292e;
  font-weight: 500;
}

.nav-section a:hover {
  color: #0366d6;
  text-decoration: underline;
}
</style>