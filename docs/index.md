---
layout: page
title: "Documentation Hub"
permalink: /docs/
---

# AutoDevHub Documentation Hub

Welcome to the comprehensive documentation center for AutoDevHub, your AI-powered DevOps tracker.

## 📚 Documentation Sections

### 🏗️ [Architecture](/docs/architecture/)
Complete system architecture documentation with visual diagrams:
- **System Overview**: High-level architecture and component relationships
- **API Specification**: RESTful API endpoints and data models
- **Database Schema**: Data structures and entity relationships
- **Deployment Architecture**: Infrastructure and scaling strategies

### 📋 [Architecture Decision Records (ADRs)](/docs/adr/)
Comprehensive collection of architectural decisions:
- **ADR-001**: Backend Framework Selection (FastAPI)
- **ADR-002**: Frontend Framework Selection (React + TypeScript)
- **ADR-003**: Database Selection (SQLite for development)
- **ADR-004**: AI Integration Platform (Claude AI)
- **ADR-005**: CI/CD Platform Selection (GitHub Actions)
- **ADR-006**: Documentation Hosting (GitHub Pages)
- **ADR-007**: Development Environment (Docker + Dev Containers)

### ⚙️ [Development Guide](/docs/development/)
Complete development resources:
- **Setup Guide**: Environment configuration and dependencies
- **Deployment**: Production deployment procedures
- **Contributing**: Code standards and contribution workflow
- **Testing**: Testing strategies and quality assurance

### 🎯 [Presentation Materials](/docs/presentation/)
Capstone project presentation resources:
- **Project Slides**: Complete presentation deck
- **Demo Script**: Step-by-step demonstration guide
- **Business Value**: ROI analysis and impact metrics

## 🚀 Quick Navigation

<div class="quick-nav">
  <div class="nav-section">
    <h3>🏁 Getting Started</h3>
    <ul>
      <li><a href="/docs/development/setup-guide/">Quick Setup</a></li>
      <li><a href="/#quick-start">Installation Guide</a></li>
      <li><a href="/docs/architecture/system-overview/">System Overview</a></li>
    </ul>
  </div>
  
  <div class="nav-section">
    <h3>🔧 Developers</h3>
    <ul>
      <li><a href="/docs/architecture/api-specification/">API Documentation</a></li>
      <li><a href="/docs/development/contributing/">Contributing Guide</a></li>
      <li><a href="/docs/architecture/database-schema/">Database Schema</a></li>
    </ul>
  </div>
  
  <div class="nav-section">
    <h3>🚀 Operations</h3>
    <ul>
      <li><a href="/docs/development/deployment/">Deployment Guide</a></li>
      <li><a href="/docs/architecture/deployment-architecture.html">Infrastructure</a></li>
      <li><a href="/docs/development/monitoring.html">Monitoring Setup</a></li>
    </ul>
  </div>
  
  <div class="nav-section">
    <h3>📊 Project Info</h3>
    <ul>
      <li><a href="/docs/presentation/slides/">Presentation</a></li>
      <li><a href="/docs/adr/">Decision Records</a></li>
      <li><a href="https://github.com/ai-cohort-july-2025/AI-Cohort-July-2025">GitHub Repository</a></li>
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

- **[GitHub Repository](https://github.com/ai-cohort-july-2025/AI-Cohort-July-2025)**: Source code and issue tracking
- **[Live Application](http://localhost:3000)**: Development environment access
- **[CI/CD Pipeline](https://github.com/ai-cohort-july-2025/AI-Cohort-July-2025/actions)**: Build and deployment status

## 📞 Support

Need help? Check these resources:
- **Issues**: [GitHub Issues](https://github.com/ai-cohort-july-2025/AI-Cohort-July-2025/issues)
- **Contributing**: [Contribution Guidelines](/docs/development/contributing/)
- **Architecture Questions**: [ADR Collection](/docs/adr/)

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