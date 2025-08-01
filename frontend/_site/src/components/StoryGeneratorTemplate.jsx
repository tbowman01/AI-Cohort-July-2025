import React, { useState } from 'react';
import styles from '../styles/StoryGenerator.module.css';

// This is a template component showing how to implement StoryGenerator with full styling
// Once the actual StoryGenerator component is created, these patterns can be applied

const StoryGeneratorTemplate = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    features: [],
    complexity: 'medium',
    language: 'javascript',
    framework: 'react'
  });
  
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedStory, setGeneratedStory] = useState('');
  const [message, setMessage] = useState({ type: '', content: '' });
  const [progress, setProgress] = useState(0);

  const availableFeatures = [
    {
      id: 'authentication',
      title: 'User Authentication',
      description: 'Login, registration, and user management system'
    },
    {
      id: 'database',
      title: 'Database Integration',
      description: 'Data persistence and CRUD operations'
    },
    {
      id: 'api',
      title: 'REST API',
      description: 'Backend API endpoints and data management'
    },
    {
      id: 'ui',
      title: 'Modern UI/UX',
      description: 'Responsive design with modern styling'
    },
    {
      id: 'testing',
      title: 'Testing Suite',
      description: 'Unit tests, integration tests, and quality assurance'
    },
    {
      id: 'deployment',
      title: 'CI/CD Pipeline',
      description: 'Automated deployment and continuous integration'
    }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFeatureToggle = (featureId) => {
    setFormData(prev => ({
      ...prev,
      features: prev.features.includes(featureId)
        ? prev.features.filter(id => id !== featureId)
        : [...prev.features, featureId]
    }));
  };

  const simulateProgress = () => {
    setProgress(0);
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + Math.random() * 15;
      });
    }, 200);
    return interval;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title.trim()) {
      setMessage({ type: 'error', content: 'Project title is required' });
      return;
    }

    setIsGenerating(true);
    setMessage({ type: 'info', content: 'Generating your user story...' });
    
    const progressInterval = simulateProgress();

    try {
      // Replace this with actual API call to backend
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      const mockStory = `# User Story: ${formData.title}

## Project Description
${formData.description || 'A comprehensive web application with modern features.'}

## Features Required
${formData.features.map(featureId => {
  const feature = availableFeatures.find(f => f.id === featureId);
  return `- **${feature?.title}**: ${feature?.description}`;
}).join('\n')}

## Technical Specifications
- **Language**: ${formData.language}
- **Framework**: ${formData.framework}
- **Complexity**: ${formData.complexity}

## Implementation Plan
1. Set up project structure and development environment
2. Implement core functionality and features
3. Add styling and responsive design
4. Write comprehensive tests
5. Set up CI/CD pipeline and deployment

## Acceptance Criteria
- All selected features are fully implemented
- Application is responsive across all devices
- Code coverage is above 80%
- Performance metrics meet industry standards
- Security best practices are followed

Generated on: ${new Date().toLocaleDateString()}`;

      setGeneratedStory(mockStory);
      setMessage({ type: 'success', content: 'User story generated successfully!' });
      
    } catch (error) {
      setMessage({ type: 'error', content: 'Failed to generate story. Please try again.' });
      console.error('Error generating story:', error);
    } finally {
      clearInterval(progressInterval);
      setProgress(100);
      setIsGenerating(false);
    }
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(generatedStory);
      setMessage({ type: 'success', content: 'Story copied to clipboard!' });
      setTimeout(() => setMessage({ type: '', content: '' }), 3000);
    } catch (error) {
      setMessage({ type: 'error', content: 'Failed to copy to clipboard' });
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>AI Story Generator</h1>
        <p className={styles.subtitle}>Generate comprehensive user stories for your projects</p>
        <p className={styles.brand}>Powered by AutoDevHub</p>
      </div>

      <div className={styles.main}>
        {message.content && (
          <div className={`${styles.message} ${styles[`message${message.type.charAt(0).toUpperCase() + message.type.slice(1)}`]} ${styles.fadeIn}`}>
            {message.content}
          </div>
        )}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.inputGroup}>
            <label htmlFor="title" className={styles.label}>
              Project Title *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              className={styles.input}
              placeholder="Enter your project title..."
              aria-required="true"
              disabled={isGenerating}
            />
          </div>

          <div className={styles.inputGroup}>
            <label htmlFor="description" className={styles.label}>
              Project Description
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              className={`${styles.input} ${styles.textarea}`}
              placeholder="Describe your project goals and requirements..."
              rows={4}
              disabled={isGenerating}
            />
          </div>

          <div className={styles.inputGroup}>
            <label className={styles.label}>
              Select Features
            </label>
            <div className={styles.featuresGrid}>
              {availableFeatures.map(feature => (
                <div
                  key={feature.id}
                  className={`${styles.featureCard} ${formData.features.includes(feature.id) ? styles.featureCardSelected : ''}`}
                  onClick={() => !isGenerating && handleFeatureToggle(feature.id)}
                  role="checkbox"
                  aria-checked={formData.features.includes(feature.id)}
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      !isGenerating && handleFeatureToggle(feature.id);
                    }
                  }}
                >
                  <div className={styles.featureTitle}>{feature.title}</div>
                  <div className={styles.featureDescription}>{feature.description}</div>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.inputGroup}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
              <div>
                <label htmlFor="complexity" className={styles.label}>
                  Complexity Level
                </label>
                <select
                  id="complexity"
                  name="complexity"
                  value={formData.complexity}
                  onChange={handleInputChange}
                  className={styles.select}
                  disabled={isGenerating}
                >
                  <option value="low">Low - Basic functionality</option>
                  <option value="medium">Medium - Standard features</option>
                  <option value="high">High - Advanced features</option>
                </select>
              </div>

              <div>
                <label htmlFor="language" className={styles.label}>
                  Primary Language
                </label>
                <select
                  id="language"
                  name="language"
                  value={formData.language}
                  onChange={handleInputChange}
                  className={styles.select}
                  disabled={isGenerating}
                >
                  <option value="javascript">JavaScript</option>
                  <option value="typescript">TypeScript</option>
                  <option value="python">Python</option>
                  <option value="java">Java</option>
                  <option value="csharp">C#</option>
                </select>
              </div>

              <div>
                <label htmlFor="framework" className={styles.label}>
                  Framework
                </label>
                <select
                  id="framework"
                  name="framework"
                  value={formData.framework}
                  onChange={handleInputChange}
                  className={styles.select}
                  disabled={isGenerating}
                >
                  <option value="react">React</option>
                  <option value="vue">Vue.js</option>
                  <option value="angular">Angular</option>
                  <option value="svelte">Svelte</option>
                  <option value="nextjs">Next.js</option>
                </select>
              </div>
            </div>
          </div>

          <button
            type="submit"
            className={`${styles.button} ${isGenerating ? styles.buttonLoading : ''}`}
            disabled={isGenerating}
            aria-label={isGenerating ? 'Generating story...' : 'Generate user story'}
          >
            {isGenerating && <div className={styles.spinner} aria-hidden="true" />}
            {isGenerating ? 'Generating...' : 'Generate User Story'}
          </button>

          {isGenerating && (
            <div className={styles.progressBar}>
              <div 
                className={styles.progressFill}
                style={{ width: `${progress}%` }}
                role="progressbar"
                aria-valuenow={progress}
                aria-valuemin="0"
                aria-valuemax="100"
                aria-label={`Generation progress: ${Math.round(progress)}%`}
              />
            </div>
          )}
        </form>

        {generatedStory && (
          <div className={`${styles.output} ${styles.slideIn}`}>
            <div className={styles.outputTitle}>
              Generated User Story
              <button
                onClick={copyToClipboard}
                className={styles.button}
                style={{ marginLeft: 'auto', padding: '0.5rem 1rem', fontSize: '0.9rem' }}
                aria-label="Copy story to clipboard"
              >
                Copy to Clipboard
              </button>
            </div>
            <pre className={styles.outputContent}>{generatedStory}</pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default StoryGeneratorTemplate;