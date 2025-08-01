import { useState } from 'react'
import './StoryGenerator.css'

const StoryGenerator = () => {
  const [formData, setFormData] = useState({
    projectName: '',
    projectDescription: '',
    targetAudience: '',
    keyFeatures: '',
    technicalRequirements: ''
  })
  const [stories, setStories] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
      const apiEndpoint = import.meta.env.VITE_API_ENDPOINT || '/api/v1/stories/generate-story'
      
      // Transform frontend form data to match backend API schema
      const apiPayload = {
        description: [
          formData.projectDescription,
          formData.targetAudience ? `Target Audience: ${formData.targetAudience}` : '',
          formData.keyFeatures ? `Key Features: ${formData.keyFeatures}` : '',
          formData.technicalRequirements ? `Technical Requirements: ${formData.technicalRequirements}` : ''
        ].filter(Boolean).join('\n\n'),
        project_context: `Project: ${formData.projectName}`,
        story_type: 'user_story',
        complexity: 'medium'
      }
      
      const response = await fetch(`${apiBaseUrl}${apiEndpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(apiPayload),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => null)
        throw new Error(errorData?.message || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      // Transform the single story response into an array for display
      setStories([data])
    } catch (err) {
      setError(`Failed to generate stories: ${err.message}`)
      console.error('Error generating stories:', err)
    } finally {
      setLoading(false)
    }
  }

  const resetForm = () => {
    setFormData({
      projectName: '',
      projectDescription: '',
      targetAudience: '',
      keyFeatures: '',
      technicalRequirements: ''
    })
    setStories([])
    setError(null)
  }

  return (
    <div className="story-generator">
      <div className="generator-form">
        <h2>Project Information</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="projectName">Project Name*</label>
            <input
              type="text"
              id="projectName"
              name="projectName"
              value={formData.projectName}
              onChange={handleInputChange}
              required
              placeholder="Enter your project name"
            />
          </div>

          <div className="form-group">
            <label htmlFor="projectDescription">Project Description*</label>
            <textarea
              id="projectDescription"
              name="projectDescription"
              value={formData.projectDescription}
              onChange={handleInputChange}
              required
              rows="4"
              placeholder="Describe what your project does and its main purpose"
            />
          </div>

          <div className="form-group">
            <label htmlFor="targetAudience">Target Audience</label>
            <input
              type="text"
              id="targetAudience"
              name="targetAudience"
              value={formData.targetAudience}
              onChange={handleInputChange}
              placeholder="Who will use this application?"
            />
          </div>

          <div className="form-group">
            <label htmlFor="keyFeatures">Key Features</label>
            <textarea
              id="keyFeatures"
              name="keyFeatures"
              value={formData.keyFeatures}
              onChange={handleInputChange}
              rows="3"
              placeholder="List the main features you want to include"
            />
          </div>

          <div className="form-group">
            <label htmlFor="technicalRequirements">Technical Requirements</label>
            <textarea
              id="technicalRequirements"
              name="technicalRequirements"
              value={formData.technicalRequirements}
              onChange={handleInputChange}
              rows="3"
              placeholder="Any specific technical constraints or requirements"
            />
          </div>

          <div className="form-actions">
            <button type="submit" disabled={loading || !formData.projectName || !formData.projectDescription}>
              {loading ? 'Generating Stories...' : 'Generate User Stories'}
            </button>
            <button type="button" onClick={resetForm} disabled={loading}>
              Reset Form
            </button>
          </div>
        </form>
      </div>

      {error && (
        <div className="error-message">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      )}

      {loading && (
        <div className="loading-indicator">
          <div className="spinner"></div>
          <p>Generating user stories for your project...</p>
        </div>
      )}

      {stories.length > 0 && (
        <div className="generated-stories">
          <h2>Generated User Stories</h2>
          <div className="stories-list">
            {stories.map((story, index) => (
              <div key={index} className="story-card">
                <div className="story-header">
                  <h3>Story #{index + 1}</h3>
                  <span className="story-priority">{story.priority || 'Medium'}</span>
                </div>
                <div className="story-content">
                  <h4>User Story</h4>
                  <div className="story-text">
                    <pre>{story.gherkin || story.user_story || story.story || 'No story content available'}</pre>
                  </div>
                  
                  {story.acceptance_criteria && story.acceptance_criteria.length > 0 && (
                    <>
                      <h4>Acceptance Criteria</h4>
                      <ul className="acceptance-criteria">
                        {story.acceptance_criteria.map((criteria, idx) => (
                          <li key={idx}>{criteria}</li>
                        ))}
                      </ul>
                    </>
                  )}
                  
                  {story.estimated_points && (
                    <div className="story-meta">
                      <h4>Estimated Story Points</h4>
                      <p><strong>{story.estimated_points}</strong> points</p>
                    </div>
                  )}

                  {story.tags && story.tags.length > 0 && (
                    <div className="story-tags">
                      <h4>Tags</h4>
                      <div className="tags-list">
                        {story.tags.map((tag, idx) => (
                          <span key={idx} className="tag">{tag}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="story-meta">
                    <h4>Story Details</h4>
                    <p><strong>Type:</strong> {story.story_type}</p>
                    <p><strong>Complexity:</strong> {story.complexity}</p>
                    <p><strong>Status:</strong> {story.status}</p>
                    <p><strong>Created:</strong> {new Date(story.created_at).toLocaleString()}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default StoryGenerator