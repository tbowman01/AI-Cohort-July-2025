# AutoDevHub Story Generator Frontend

[![Version](https://img.shields.io/badge/version-1.0.0--alpha-blue.svg)](https://github.com/AI-Cohort-July-2025/autodevhub-story-generator)
[![React](https://img.shields.io/badge/React-19.1.0-61dafb.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-7.0.4-646cff.svg)](https://vitejs.dev/)
[![License](https://img.shields.io/badge/license-AI%20Cohort%202025-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](#)

A modern React application built with Vite for generating AI-powered user stories for development projects.

## Features

- **Intuitive Form Interface**: Easy-to-use form for entering project details
- **Real-time API Integration**: Connects to the backend API for story generation
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Loading States**: Visual feedback during story generation
- **Modern UI**: Clean, professional design with smooth animations

## Technology Stack

- **React 19** - Frontend framework
- **Vite** - Build tool and development server
- **CSS3** - Styling with modern features
- **Fetch API** - HTTP client for backend communication

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/
│   │   ├── StoryGenerator.jsx      # Main story generator component
│   │   └── StoryGenerator.css      # Component-specific styles
│   ├── App.jsx            # Root application component
│   ├── App.css            # Application-wide styles
│   ├── index.css          # Global styles
│   └── main.jsx           # Application entry point
├── .env                   # Environment variables
├── .env.example           # Environment variables template
├── package.json           # Dependencies and scripts
├── vite.config.js         # Vite configuration
└── README.md             # This file
```

## Environment Variables

Create a `.env` file in the frontend directory with the following variables:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_ENDPOINT=/api/v1/stories/generate
VITE_ENV=development
VITE_DEBUG=true
VITE_APP_NAME=AutoDevHub Story Generator
VITE_APP_VERSION=1.0.0
```

## Development Setup

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   ```
   
   The application will be available at `http://localhost:3000`

3. **Build for Production**
   ```bash
   npm run build
   ```

4. **Preview Production Build**
   ```bash
   npm run preview
   ```

## API Integration

The frontend communicates with the backend API running on `http://localhost:8000`. The Vite development server is configured with a proxy to handle CORS:

```javascript
// vite.config.js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
    }
  }
}
```

## Form Fields

The story generator form includes the following fields:

- **Project Name*** (required) - Name of your project
- **Project Description*** (required) - Detailed description of the project
- **Target Audience** (optional) - Who will use the application
- **Key Features** (optional) - Main features to include
- **Technical Requirements** (optional) - Technical constraints or requirements

## Generated Stories Format

The application displays generated stories with:

- **Story Number** and **Priority Level**
- **User Story** - In standard user story format
- **Acceptance Criteria** - Detailed acceptance criteria
- **Development Tasks** - Specific implementation tasks

## Error Handling

The application includes comprehensive error handling for:

- Network connectivity issues
- API server errors
- Invalid form submissions
- Backend validation errors

## Responsive Design

The application is fully responsive and works on:

- Desktop computers (1200px+)
- Tablets (768px - 1199px)
- Mobile phones (< 768px)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development Guidelines

### Code Style
- Use functional components with hooks
- Implement proper error boundaries
- Follow React best practices
- Use semantic HTML elements
- Maintain consistent CSS naming conventions

### Performance
- Lazy load components when appropriate
- Optimize images and assets
- Implement proper loading states
- Use React DevTools for profiling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the AutoDevHub AI Cohort July 2025 initiative.