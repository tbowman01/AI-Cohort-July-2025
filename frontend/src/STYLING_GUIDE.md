# AutoDevHub Frontend Styling Guide

## UI/UX Agent Ready for Integration

This styling system has been prepared by the UI/UX agent and is ready to be applied to the StoryGenerator component once it's created by other agents.

## Overview

The AutoDevHub frontend uses a professional, modern styling system with:
- **CSS Modules** for component-specific styles
- **Global utility classes** for consistent spacing and typography
- **Responsive design** with mobile-first approach
- **Accessibility** features built-in
- **Professional color scheme** with gradient backgrounds

## File Structure

```
frontend/src/
├── styles/
│   ├── globals.css                    # Global styles and utilities
│   └── StoryGenerator.module.css      # Component-specific styles
├── components/
│   ├── StoryGeneratorTemplate.jsx     # Example implementation
│   └── LoadingSpinner.jsx             # Reusable loading component
├── index.css                          # Entry point (imports globals)
└── STYLING_GUIDE.md                   # This documentation
```

## How to Apply Styles to StoryGenerator Component

### 1. Import the CSS Module

```jsx
import styles from '../styles/StoryGenerator.module.css';
```

### 2. Apply Component Classes

The CSS module provides these main classes:

```jsx
const StoryGenerator = () => {
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>AI Story Generator</h1>
        <p className={styles.subtitle}>Generate comprehensive user stories</p>
        <p className={styles.brand}>Powered by AutoDevHub</p>
      </div>
      
      <div className={styles.main}>
        {/* Form content */}
      </div>
    </div>
  );
};
```

### 3. Form Styling

```jsx
<form onSubmit={handleSubmit} className={styles.form}>
  <div className={styles.inputGroup}>
    <label htmlFor="title" className={styles.label}>
      Project Title *
    </label>
    <input
      type="text"
      id="title"
      name="title"
      className={styles.input}
      placeholder="Enter your project title..."
    />
  </div>
  
  <button 
    type="submit" 
    className={`${styles.button} ${isGenerating ? styles.buttonLoading : ''}`}
    disabled={isGenerating}
  >
    {isGenerating && <div className={styles.spinner} />}
    {isGenerating ? 'Generating...' : 'Generate User Story'}
  </button>
</form>
```

### 4. Feature Cards Grid

```jsx
<div className={styles.featuresGrid}>
  {features.map(feature => (
    <div
      key={feature.id}
      className={`${styles.featureCard} ${
        selectedFeatures.includes(feature.id) 
          ? styles.featureCardSelected 
          : ''
      }`}
      onClick={() => toggleFeature(feature.id)}
    >
      <div className={styles.featureTitle}>{feature.title}</div>
      <div className={styles.featureDescription}>{feature.description}</div>
    </div>
  ))}
</div>
```

### 5. Output Display

```jsx
{generatedStory && (
  <div className={`${styles.output} ${styles.slideIn}`}>
    <div className={styles.outputTitle}>
      Generated User Story
      <button onClick={copyToClipboard} className={styles.button}>
        Copy to Clipboard
      </button>
    </div>
    <pre className={styles.outputContent}>{generatedStory}</pre>
  </div>
)}
```

### 6. Message States

```jsx
{message.content && (
  <div className={`${styles.message} ${styles[`message${message.type.charAt(0).toUpperCase() + message.type.slice(1)}`]} ${styles.fadeIn}`}>
    {message.content}
  </div>
)}
```

Message types: `messageSuccess`, `messageError`, `messageInfo`

### 7. Loading States

```jsx
{isGenerating && (
  <div className={styles.progressBar}>
    <div 
      className={styles.progressFill}
      style={{ width: `${progress}%` }}
      role="progressbar"
      aria-valuenow={progress}
      aria-valuemin="0"
      aria-valuemax="100"
    />
  </div>
)}
```

## Available CSS Classes

### Layout Classes
- `container` - Main wrapper with max-width and padding
- `header` - Header section with centered content
- `main` - Main content area with white background and shadow
- `form` - Form wrapper

### Typography Classes
- `title` - Main heading (3rem, gradient text shadow)
- `subtitle` - Secondary heading (1.2rem, light opacity)
- `brand` - Brand text (gold color)
- `label` - Form labels (semibold, dark gray)

### Form Classes
- `input` - Text inputs and textareas with focus states
- `textarea` - Specific textarea styling
- `select` - Select dropdowns
- `button` - Primary button with gradient and hover effects
- `buttonLoading` - Loading state for buttons
- `spinner` - Loading spinner animation

### Feature Card Classes
- `featuresGrid` - Responsive grid layout
- `featureCard` - Individual feature card
- `featureCardSelected` - Selected state
- `featureTitle` - Feature card title
- `featureDescription` - Feature card description

### Output Classes
- `output` - Output container
- `outputTitle` - Output section title
- `outputContent` - Generated content display

### Message Classes
- `message` - Base message styling
- `messageSuccess` - Success message (green)
- `messageError` - Error message (red)
- `messageInfo` - Info message (blue)

### Progress Classes
- `progressBar` - Progress bar container
- `progressFill` - Progress bar fill with animation

### Animation Classes
- `fadeIn` - Fade in animation
- `slideIn` - Slide in from left animation

## Global Utility Classes

The global styles provide utility classes for:

### Typography
- `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl`, `text-4xl`
- `font-light`, `font-normal`, `font-medium`, `font-semibold`, `font-bold`
- `text-center`, `text-left`, `text-right`

### Spacing
- `mb-1` through `mb-8` (margin-bottom)
- `mt-1` through `mt-8` (margin-top)
- `p-1` through `p-8` (padding)

### Colors
- `text-primary`, `text-secondary`, `text-success`, `text-warning`, `text-error`
- `bg-primary`, `bg-secondary`, `bg-success`, `bg-warning`, `bg-error`

### Layout
- `flex`, `inline-flex`, `flex-col`, `flex-row`
- `items-center`, `items-start`, `items-end`
- `justify-center`, `justify-between`, `justify-start`, `justify-end`
- `w-full`, `h-full`, `w-auto`, `h-auto`

### Borders & Shadows
- `border`, `border-2`, `border-primary`, `border-gray`
- `rounded`, `rounded-lg`, `rounded-xl`, `rounded-full`
- `shadow-sm`, `shadow`, `shadow-md`, `shadow-lg`, `shadow-xl`

## Color Scheme

### Primary Colors
- **Primary**: `#667eea` (Blue gradient start)
- **Secondary**: `#764ba2` (Purple gradient end)
- **Success**: `#48bb78` (Green)
- **Warning**: `#ed8936` (Orange)
- **Error**: `#e53e3e` (Red)

### Neutral Colors
- **Dark Text**: `#2d3748`
- **Medium Text**: `#4a5568`
- **Light Text**: `#a0aec0`
- **Background**: `#f7fafc`
- **White**: `#ffffff`

### Gradients
- **Primary Gradient**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **Background Gradient**: Same as primary gradient

## Responsive Breakpoints

- **Mobile**: `< 480px`
- **Tablet**: `480px - 768px`
- **Desktop**: `> 768px`

### Mobile Optimizations
- Smaller font sizes
- Reduced padding
- Single-column layouts
- Full-width buttons
- Simplified navigation

## Accessibility Features

### Built-in Accessibility
- **Focus indicators**: 2px solid outline with offset
- **ARIA labels**: Built into components
- **Keyboard navigation**: Tab order and Enter/Space handling
- **Screen reader support**: Semantic HTML and ARIA attributes
- **Color contrast**: WCAG AA compliant colors

### Usage Examples
```jsx
// Proper ARIA usage
<button
  aria-label={isGenerating ? 'Generating story...' : 'Generate user story'}
  disabled={isGenerating}
>

// Progress bar with accessibility
<div 
  role="progressbar"
  aria-valuenow={progress}
  aria-valuemin="0"
  aria-valuemax="100"
  aria-label={`Generation progress: ${Math.round(progress)}%`}
/>

// Form accessibility
<label htmlFor="title">Project Title *</label>
<input
  id="title"
  aria-required="true"
  aria-describedby="title-help"
/>
```

## Loading Components

### LoadingSpinner Component
```jsx
import LoadingSpinner from './LoadingSpinner';

// Usage examples
<LoadingSpinner size="small" inline text="Loading..." />
<LoadingSpinner size="medium" color="#667eea" />
<LoadingSpinner size="large" overlay text="Generating story..." />
```

### Props
- `size`: 'small', 'medium', 'large'
- `color`: Any valid CSS color
- `text`: Loading text to display
- `inline`: Boolean for inline display
- `overlay`: Boolean for full-screen overlay

## Integration Steps for Other Agents

### For React Component Developers

1. **Import the styles**:
   ```jsx
   import styles from '../styles/StoryGenerator.module.css';
   ```

2. **Use the template**: Reference `StoryGeneratorTemplate.jsx` for implementation patterns

3. **Apply classes**: Use the CSS module classes documented above

4. **Handle states**: Implement loading, error, and success states with provided classes

5. **Add accessibility**: Use the built-in ARIA patterns and focus management

### For Backend Integration Developers

The styling system expects these data structures:

```javascript
// Form data structure
const formData = {
  title: string,
  description: string,
  features: string[],
  complexity: 'low' | 'medium' | 'high',
  language: string,
  framework: string
};

// Message structure
const message = {
  type: 'success' | 'error' | 'info',
  content: string
};

// Feature structure
const feature = {
  id: string,
  title: string,
  description: string
};
```

## Performance Considerations

### Optimizations Included
- **CSS Modules**: Scoped styles prevent conflicts
- **Minimal dependencies**: Pure CSS without external libraries
- **Efficient animations**: Hardware-accelerated transforms
- **Responsive images**: Proper sizing and optimization
- **Progressive enhancement**: Works without JavaScript

### Best Practices
- Use `transform` and `opacity` for animations
- Minimize DOM manipulations during interactions
- Implement proper loading states to improve perceived performance
- Use debouncing for search/filter inputs

## Browser Support

The styling system supports:
- **Modern browsers**: Chrome 88+, Firefox 85+, Safari 14+, Edge 88+
- **Mobile browsers**: iOS Safari 14+, Chrome Mobile 88+
- **Accessibility tools**: Screen readers and keyboard navigation

## Next Steps

1. **Wait for StoryGenerator component creation** by React developers
2. **Apply styling classes** using this guide
3. **Test responsive design** across devices
4. **Validate accessibility** with screen readers
5. **Integrate with backend** API endpoints
6. **Performance testing** and optimization

## Questions or Issues?

If you encounter any styling issues or need additional components:

1. Check this guide for existing solutions
2. Review the `StoryGeneratorTemplate.jsx` for implementation examples
3. Use the global utility classes for common styling needs
4. Extend the CSS modules for component-specific requirements

The UI/UX agent has prepared a comprehensive styling system that's ready for immediate integration!