# AutoDevHub Frontend

React-based frontend for the AutoDevHub AI-powered DevOps tracking platform.

## 🏗️ Architecture

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development and builds
- **State Management**: Redux Toolkit + RTK Query
- **Routing**: React Router v6
- **UI Components**: Material-UI (MUI) v5
- **Styling**: Emotion (CSS-in-JS) + Material-UI theming
- **Testing**: Jest + React Testing Library
- **Code Quality**: ESLint + Prettier + Husky

## 📁 Directory Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── common/          # Generic components
│   │   ├── forms/           # Form components
│   │   └── charts/          # Data visualization components
│   ├── pages/               # Page components
│   │   ├── Dashboard/
│   │   ├── Projects/
│   │   ├── Teams/
│   │   ├── Analytics/
│   │   └── Auth/
│   ├── hooks/               # Custom React hooks
│   ├── services/            # API services and utilities
│   │   ├── api.ts           # API client configuration
│   │   ├── auth.ts          # Authentication services
│   │   └── projects.ts      # Project-related services
│   ├── store/               # Redux store configuration
│   │   ├── index.ts
│   │   ├── authSlice.ts
│   │   ├── projectsSlice.ts
│   │   └── uiSlice.ts
│   ├── types/               # TypeScript type definitions
│   ├── utils/               # Utility functions
│   ├── assets/              # Images, icons, and static files
│   ├── App.tsx              # Main App component
│   ├── index.tsx            # Entry point
│   └── theme.ts             # Material-UI theme configuration
├── package.json
├── tsconfig.json
├── vite.config.ts
├── .eslintrc.js
├── .prettierrc
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites

- Node.js 16+
- npm or yarn

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API endpoint and other config
   ```

3. **Start development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

The application will be available at `http://localhost:3000`

## 🛠️ Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build

# Testing
npm run test         # Run tests
npm run test:watch   # Run tests in watch mode
npm run test:coverage # Run tests with coverage

# Code Quality
npm run lint         # Run ESLint
npm run lint:fix     # Fix ESLint issues
npm run format       # Format with Prettier
npm run type-check   # TypeScript type checking
```

## 🎨 UI Components

### Design System

- **Theme**: Custom Material-UI theme with AutoDevHub branding
- **Colors**: Primary (blue), secondary (green), error, warning, info
- **Typography**: Roboto font family with consistent sizing
- **Spacing**: 8px base unit for consistent spacing
- **Breakpoints**: Mobile-first responsive design

### Component Library

- **Common Components**: Button, Input, Card, Modal, Spinner
- **Form Components**: FormField, FormSelect, FormDatePicker
- **Data Components**: DataTable, Chart, MetricCard
- **Layout Components**: Header, Sidebar, Footer, Container

## 📊 State Management

### Redux Toolkit Structure

```typescript
// Store slices
- authSlice: User authentication and profile
- projectsSlice: Project data and operations
- teamsSlice: Team management
- analyticsSlice: Analytics data and insights
- uiSlice: UI state (modals, notifications, theme)
```

### RTK Query APIs

```typescript
// API endpoints
- authApi: Login, logout, profile, refresh token
- projectsApi: CRUD operations for projects
- teamsApi: Team management operations
- analyticsApi: Analytics and reporting data
```

## 🔒 Authentication

- **JWT Tokens**: Access and refresh token management
- **Protected Routes**: Route guards for authenticated pages
- **Automatic Refresh**: Token refresh before expiration
- **Logout Handling**: Automatic logout on token expiration

## 📱 Responsive Design

- **Mobile First**: Designed for mobile devices first
- **Breakpoints**: sm (600px), md (900px), lg (1200px), xl (1536px)
- **Grid System**: Material-UI Grid for responsive layouts
- **Navigation**: Responsive sidebar that collapses on mobile

## 🧪 Testing Strategy

### Testing Stack

- **Unit Tests**: Jest + React Testing Library
- **Component Tests**: Testing user interactions and rendering
- **Integration Tests**: Testing component integration with Redux
- **E2E Tests**: Cypress for end-to-end testing (TODO)

### Testing Guidelines

```typescript
// Example test structure
describe('Dashboard Component', () => {
  it('renders project metrics correctly', () => {
    // Arrange
    const mockData = { projects: 5, activeProjects: 3 };
    
    // Act
    render(<Dashboard />, { 
      preloadedState: { projects: mockData } 
    });
    
    // Assert
    expect(screen.getByText('5 Total Projects')).toBeInTheDocument();
  });
});
```

## 🎯 Key Features

### Dashboard
- **Project Overview**: Quick metrics and status
- **Recent Activity**: Latest commits, PRs, deployments
- **Team Performance**: Member activity and contributions
- **AI Insights**: Intelligent recommendations and alerts

### Project Management
- **Project List**: Filterable and sortable project grid
- **Project Details**: Comprehensive project information
- **Repository Integration**: GitHub/GitLab integration
- **Deployment Tracking**: Deployment history and status

### Team Collaboration
- **Team Dashboard**: Team-specific metrics and activity
- **Member Profiles**: Individual contributor insights
- **Communication Tools**: Integrated chat and notifications
- **Role Management**: Permission-based access control

### Analytics & Insights
- **Performance Metrics**: Code quality, deployment frequency
- **Trend Analysis**: Historical data visualization
- **AI Recommendations**: Intelligent insights and suggestions
- **Custom Reports**: Configurable reporting dashboard

## 🚀 Performance Optimization

- **Code Splitting**: Route-based code splitting with React.lazy
- **Bundle Analysis**: Webpack bundle analyzer for optimization
- **Image Optimization**: WebP format with fallbacks
- **Caching**: Service worker for offline support
- **Lazy Loading**: Lazy load components and images
- **Memoization**: React.memo and useMemo for expensive operations

## 🔧 Development Tools

- **Hot Reload**: Fast refresh during development
- **DevTools**: Redux DevTools integration
- **Error Boundaries**: Graceful error handling
- **Debugging**: Source maps for production debugging
- **Performance**: React DevTools Profiler integration

## 🚧 TODO

- [ ] Set up Vite configuration
- [ ] Create Material-UI theme
- [ ] Implement authentication components
- [ ] Build dashboard layout
- [ ] Create project management pages
- [ ] Add team collaboration features
- [ ] Implement analytics dashboard
- [ ] Set up testing framework
- [ ] Add responsive design
- [ ] Implement performance optimizations
- [ ] Set up CI/CD pipeline
- [ ] Add accessibility features

## 🌐 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📚 Additional Resources

- [React Documentation](https://reactjs.org/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Material-UI Documentation](https://mui.com/)
- [Redux Toolkit Documentation](https://redux-toolkit.js.org/)
- [Vite Documentation](https://vitejs.dev/)

---

For more information, see the [main project README](../README.md).