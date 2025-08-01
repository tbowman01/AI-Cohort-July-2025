import { render } from '@testing-library/react'
import { vi } from 'vitest'

// Custom render function with common providers if needed
export const renderWithProviders = (ui, options = {}) => {
  return render(ui, {
    // Add providers here if needed (Router, Context, etc.)
    ...options
  })
}

// Mock form data generator
export const generateMockFormData = (overrides = {}) => ({
  projectName: 'Test Project',
  projectDescription: 'A comprehensive test project for story generation',
  targetAudience: 'Developers and QA engineers',
  keyFeatures: 'User authentication, Story generation, API integration',
  technicalRequirements: 'React, FastAPI, PostgreSQL',
  ...overrides
})

// Mock API response generator
export const generateMockStoryResponse = (overrides = {}) => ({
  story_id: 'test-story-123',
  title: 'Test User Story',
  feature_description: 'Test feature description',
  gherkin: `Feature: Test Feature
  
  Scenario: User can complete action
    Given the user is on the test page
    When they perform an action
    Then they should see the expected result`,
  acceptance_criteria: [
    'System should validate user input',
    'Story should be generated successfully',
    'User should receive confirmation'
  ],
  estimated_points: 5,
  story_type: 'user_story',
  priority: 'medium',
  complexity: 'medium',
  status: 'draft',
  tags: ['test', 'user_story'],
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  ...overrides
})

// Mock fetch implementation
export const mockFetch = (response, options = {}) => {
  const { status = 200, ok = true } = options
  
  return vi.fn().mockResolvedValue({
    ok,
    status,
    json: vi.fn().mockResolvedValue(response),
    text: vi.fn().mockResolvedValue(JSON.stringify(response))
  })
}

// Form validation helpers
export const fillFormFields = async (user, fields = {}) => {
  const defaultFields = generateMockFormData(fields)
  
  // Helper to fill form field if element exists
  const fillField = async (selector, value) => {
    const element = document.querySelector(selector)
    if (element && value) {
      await user.clear(element)
      await user.type(element, value)
    }
  }
  
  await fillField('#projectName', defaultFields.projectName)
  await fillField('#projectDescription', defaultFields.projectDescription)
  await fillField('#targetAudience', defaultFields.targetAudience)
  await fillField('#keyFeatures', defaultFields.keyFeatures)
  await fillField('#technicalRequirements', defaultFields.technicalRequirements)
  
  return defaultFields
}

// Wait for async operations
export const waitForRequest = async (requestHandler, timeout = 3000) => {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      reject(new Error(`Request timeout after ${timeout}ms`))
    }, timeout)
    
    requestHandler()
      .then(resolve)
      .catch(reject)
      .finally(() => clearTimeout(timer))
  })
}

// Assertion helpers
export const expectFormFieldsToBeEmpty = () => {
  expect(document.querySelector('#projectName')).toHaveValue('')
  expect(document.querySelector('#projectDescription')).toHaveValue('')
  expect(document.querySelector('#targetAudience')).toHaveValue('')
  expect(document.querySelector('#keyFeatures')).toHaveValue('')
  expect(document.querySelector('#technicalRequirements')).toHaveValue('')
}

export const expectFormFieldsToHaveValues = (values) => {
  if (values.projectName !== undefined) {
    expect(document.querySelector('#projectName')).toHaveValue(values.projectName)
  }
  if (values.projectDescription !== undefined) {
    expect(document.querySelector('#projectDescription')).toHaveValue(values.projectDescription)
  }
  if (values.targetAudience !== undefined) {
    expect(document.querySelector('#targetAudience')).toHaveValue(values.targetAudience)
  }
  if (values.keyFeatures !== undefined) {
    expect(document.querySelector('#keyFeatures')).toHaveValue(values.keyFeatures)
  }
  if (values.technicalRequirements !== undefined) {
    expect(document.querySelector('#technicalRequirements')).toHaveValue(values.technicalRequirements)
  }
}

// Error message helpers
export const expectErrorMessage = (message) => {
  const errorElement = document.querySelector('.error-message')
  expect(errorElement).toBeInTheDocument()
  expect(errorElement).toHaveTextContent(message)
}

export const expectNoErrorMessage = () => {
  const errorElement = document.querySelector('.error-message')
  expect(errorElement).not.toBeInTheDocument()
}

// Loading state helpers
export const expectLoadingState = (isLoading = true) => {
  const loadingElement = document.querySelector('.loading-indicator')
  const submitButton = document.querySelector('button[type="submit"]')
  
  if (isLoading) {
    if (loadingElement) {
      expect(loadingElement).toBeInTheDocument()
    }
    if (submitButton) {
      expect(submitButton).toBeDisabled()
      expect(submitButton).toHaveTextContent(/generating/i)
    }
  } else {
    if (loadingElement) {
      expect(loadingElement).not.toBeInTheDocument()
    }
    if (submitButton) {
      // Only check if button should be enabled when required fields are filled
      const projectName = document.querySelector('#projectName')?.value || ''
      const projectDescription = document.querySelector('#projectDescription')?.value || ''
      
      if (projectName && projectDescription) {
        expect(submitButton).not.toBeDisabled()
      }
      expect(submitButton).toHaveTextContent(/generate user stories/i)
    }
  }
}

// Story display helpers
export const expectStoryToBeDisplayed = (story) => {
  const storyCard = document.querySelector('.story-card')
  expect(storyCard).toBeInTheDocument()
  
  if (story.gherkin) {
    expect(storyCard).toHaveTextContent(story.gherkin)
  }
  
  if (story.acceptance_criteria) {
    story.acceptance_criteria.forEach(criteria => {
      expect(storyCard).toHaveTextContent(criteria)
    })
  }
  
  if (story.estimated_points) {
    expect(storyCard).toHaveTextContent(story.estimated_points.toString())
  }
}

// Environment setup
export const setupTestEnvironment = () => {
  // Mock import.meta.env
  // Mock import.meta.env for components
  Object.defineProperty(import.meta, 'env', {
    value: {
      VITE_API_BASE_URL: 'http://localhost:8000',
      VITE_API_ENDPOINT: '/api/v1/stories/generate'
    },
    writable: true
  })
  
  // Mock window.fetch
  global.fetch = vi.fn()
  
  return {
    restoreFetch: () => {
      global.fetch.mockRestore()
    }
  }
}