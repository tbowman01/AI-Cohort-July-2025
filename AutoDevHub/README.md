# AutoDevHub - AI-Powered DevOps Tracker

AutoDevHub is an AI-powered DevOps tracking and automation platform designed to streamline development workflows, enhance team collaboration, and provide intelligent insights into project health and performance.

## 🚀 Features

- **Real-time Project Monitoring**: Track commits, pull requests, deployments, and team activity
- **AI-Powered Insights**: Get intelligent recommendations and trend analysis
- **Team Collaboration**: Enhanced communication and coordination tools
- **Automated Workflows**: Streamline repetitive DevOps tasks
- **Performance Analytics**: Comprehensive dashboards and reporting

## 📁 Project Structure

```
AutoDevHub/
├── backend/          # FastAPI application (Python)
├── frontend/         # React application (TypeScript)
├── docs/            # Documentation (GitHub Pages)
├── .github/         
│   └── workflows/   # CI/CD configurations
├── presentation/    # Slides and demo materials
└── README.md        # This file
```

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React (TypeScript)
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Deployment**: Docker + GitHub Actions
- **Documentation**: GitHub Pages

## 🚀 Quick Start

1. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Documentation**:
   ```bash
   cd docs
   # GitHub Pages automatically serves from this directory
   ```

## 📚 Documentation

- [Backend API Documentation](./backend/README.md)
- [Frontend Development Guide](./frontend/README.md)
- [Deployment Guide](./docs/deployment.md)
- [Contributing Guidelines](./docs/contributing.md)

## 🤝 Contributing

Please read our [Contributing Guidelines](./docs/contributing.md) before submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🎯 Project Status

This is a capstone project for the AI Cohort July 2025. Current phase: **Setup and Environment Configuration**.

---

**Built with ❤️ by the AI Cohort July 2025 Team**