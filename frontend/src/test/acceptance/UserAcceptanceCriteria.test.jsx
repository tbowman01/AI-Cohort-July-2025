import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { http, HttpResponse } from 'msw'
import { server } from '../mocks/server'
import StoryGenerator from '../../components/StoryGenerator'
import App from '../../App'
import { 
  generateMockFormData, 
  generateMockStoryResponse,
  setupTestEnvironment
} from '../utils/testUtils'

/**
 * User Acceptance Criteria Tests
 * 
 * These tests validate that the application meets the specific acceptance criteria
 * defined for the user story creation feature. Each test corresponds to a specific
 * user requirement or business rule.
 */

describe('User Acceptance Criteria Validation', () => {
  let user
  let testEnv

  beforeEach(() => {
    user = userEvent.setup()
    testEnv = setupTestEnvironment()
    vi.clearAllMocks()
  })

  afterEach(() => {
    testEnv.restoreFetch()
  })

  describe('AC1: User can access the story generation form', () => {
    it('displays the story generation form when user visits the application', () => {
      render(<App />)
      
      // Verify form is immediately accessible
      expect(screen.getByRole('heading', { name: /autodevhub story generator/i })).toBeInTheDocument()
      expect(screen.getByRole('heading', { name: /project information/i })).toBeInTheDocument()
      expect(screen.getByLabelText(/project name/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/project description/i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /generate user stories/i })).toBeInTheDocument()
    })

    it('form is immediately usable without additional setup', async () => {
      render(<StoryGenerator />)
      
      // User should be able to start typing immediately
      const projectNameField = screen.getByLabelText(/project name/i)
      await user.type(projectNameField, 'Test')
      
      expect(projectNameField).toHaveValue('Test')
    })
  })

  describe('AC2: User must provide required project information', () => {
    it('requires project name before allowing submission', async () => {
      render(<StoryGenerator />)
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      
      // Should be disabled without project name
      expect(submitButton).toBeDisabled()
      
      // Should remain disabled with only description
      await user.type(screen.getByLabelText(/project description/i), 'Some description')
      expect(submitButton).toBeDisabled()
      
      // Should be enabled with both required fields
      await user.type(screen.getByLabelText(/project name/i), 'Test Project')
      expect(submitButton).toBeEnabled()
    })

    it('requires project description before allowing submission', async () => {
      render(<StoryGenerator />)
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      
      // Should remain disabled with only project name
      await user.type(screen.getByLabelText(/project name/i), 'Test Project')
      expect(submitButton).toBeDisabled()
      
      // Should be enabled with both required fields
      await user.type(screen.getByLabelText(/project description/i), 'Test description')
      expect(submitButton).toBeEnabled()
    })

    it('validates minimum content requirements', async () => {
      render(<StoryGenerator />)
      
      // Very short inputs should still work (basic validation)
      await user.type(screen.getByLabelText(/project name/i), 'A')
      await user.type(screen.getByLabelText(/project description/i), 'B')
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      expect(submitButton).toBeEnabled()
    })
  })

  describe('AC3: User can provide optional project details', () => {
    it('accepts target audience information', async () => {
      render(<StoryGenerator />)
      
      const targetAudienceField = screen.getByLabelText(/target audience/i)
      expect(targetAudienceField).not.toHaveAttribute('required')
      
      await user.type(targetAudienceField, 'Software developers and project managers')
      expect(targetAudienceField).toHaveValue('Software developers and project managers')
    })

    it('accepts key features information', async () => {
      render(<StoryGenerator />)
      
      const keyFeaturesField = screen.getByLabelText(/key features/i)
      expect(keyFeaturesField).not.toHaveAttribute('required')
      
      await user.type(keyFeaturesField, 'User authentication, dashboard, reporting')
      expect(keyFeaturesField).toHaveValue('User authentication, dashboard, reporting')
    })

    it('accepts technical requirements information', async () => {
      render(<StoryGenerator />)
      
      const technicalReqField = screen.getByLabelText(/technical requirements/i)
      expect(technicalReqField).not.toHaveAttribute('required')
      
      await user.type(technicalReqField, 'React, Node.js, PostgreSQL, Docker')
      expect(technicalReqField).toHaveValue('React, Node.js, PostgreSQL, Docker')
    })

    it('works correctly when optional fields are left empty', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      
      // Only fill required fields
      await user.type(screen.getByLabelText(/project name/i), 'Minimal Project')
      await user.type(screen.getByLabelText(/project description/i), 'Basic description')
      
      // Submit should work
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
    })
  })

  describe('AC4: System generates user story in Gherkin format', () => {
    it('produces valid Gherkin format with Feature, Scenario, Given/When/Then', async () => {
      const gherkinStory = `Feature: User Authentication
  As a user
  I want to log into the system
  So that I can access my account

Scenario: Successful login
  Given I am on the login page
  When I enter valid credentials
  Then I should be logged into the system
  And I should see my dashboard

Scenario: Failed login
  Given I am on the login page
  When I enter invalid credentials
  Then I should see an error message
  And I should remain on the login page`

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse({
            gherkin: gherkinStory
          }))
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Auth System')
      await user.type(screen.getByLabelText(/project description/i), 'User authentication system')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/feature: user authentication/i)).toBeInTheDocument()
        expect(screen.getByText(/scenario: successful login/i)).toBeInTheDocument()
        expect(screen.getByText(/scenario: failed login/i)).toBeInTheDocument()
        expect(screen.getByText(/given i am on the login page/i)).toBeInTheDocument()
        expect(screen.getByText(/when i enter valid credentials/i)).toBeInTheDocument()
        expect(screen.getByText(/then i should be logged into the system/i)).toBeInTheDocument()
      })
    })

    it('displays the generated story in a readable format', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Test Project')
      await user.type(screen.getByLabelText(/project description/i), 'Test description')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        const storyContent = screen.getByRole('region', { name: /story/i }) || screen.querySelector('.story-content')
        expect(storyContent).toBeInTheDocument()
      })

      // Verify story is displayed in a pre-formatted block for readability
      const preElement = screen.querySelector('pre')
      expect(preElement).toBeInTheDocument()
    })
  })

  describe('AC5: System provides acceptance criteria for the story', () => {
    it('displays acceptance criteria as a list', async () => {
      const acceptanceCriteria = [
        'User must be able to enter valid email address',
        'Password must meet security requirements',
        'System must provide clear error messages for invalid inputs',
        'Successful login must redirect to user dashboard'
      ]

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse({
            acceptance_criteria: acceptanceCriteria
          }))
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Login System')
      await user.type(screen.getByLabelText(/project description/i), 'User login functionality')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/acceptance criteria/i)).toBeInTheDocument()
      })

      // Verify all acceptance criteria are displayed
      acceptanceCriteria.forEach(criteria => {
        expect(screen.getByText(criteria)).toBeInTheDocument()
      })

      // Verify they are displayed as a list
      const criteriaList = screen.getByRole('list', { name: /acceptance criteria/i }) || 
                          screen.querySelector('.acceptance-criteria')
      expect(criteriaList).toBeInTheDocument()
    })

    it('handles empty acceptance criteria gracefully', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse({
            acceptance_criteria: []
          }))
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Test Project')
      await user.type(screen.getByLabelText(/project description/i), 'Test description')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Should not crash or show error when acceptance criteria is empty
      expect(screen.queryByText(/acceptance criteria/i)).not.toBeInTheDocument()
    })
  })

  describe('AC6: System provides story metadata (points, type, priority)', () => {
    it('displays estimated story points', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse({
            estimated_points: 8
          }))
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Complex Feature')
      await user.type(screen.getByLabelText(/project description/i), 'A complex feature requiring significant effort')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/estimated story points/i)).toBeInTheDocument()
        expect(screen.getByText('8')).toBeInTheDocument()
      })
    })

    it('displays story type and complexity', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse({
            story_type: 'user_story',
            complexity: 'high'
          }))
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Test Feature')
      await user.type(screen.getByLabelText(/project description/i), 'Test description')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/story details/i)).toBeInTheDocument()
        expect(screen.getByText(/type:/i)).toBeInTheDocument()
        expect(screen.getByText(/complexity:/i)).toBeInTheDocument()
      })
    })

    it('displays story tags when available', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse({
            tags: ['authentication', 'security', 'frontend', 'api']
          }))
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Auth Feature')
      await user.type(screen.getByLabelText(/project description/i), 'Authentication feature')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/tags/i)).toBeInTheDocument()
        expect(screen.getByText('authentication')).toBeInTheDocument()
        expect(screen.getByText('security')).toBeInTheDocument()
        expect(screen.getByText('frontend')).toBeInTheDocument()
        expect(screen.getByText('api')).toBeInTheDocument()
      })
    })
  })

  describe('AC7: User receives clear feedback during story generation', () => {
    it('shows loading state with progress indicator', async () => {
      let resolveRequest
      const requestPromise = new Promise(resolve => {
        resolveRequest = resolve
      })

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', async () => {
          await requestPromise
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Loading Test')
      await user.type(screen.getByLabelText(/project description/i), 'Testing loading states')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      // Verify loading indicators
      expect(screen.getByText(/generating stories/i)).toBeInTheDocument()
      expect(screen.getByText(/generating user stories for your project/i)).toBeInTheDocument()
      expect(screen.getByRole('progressbar') || screen.querySelector('.spinner')).toBeInTheDocument()
      
      // Button should show loading state
      const submitButton = screen.getByRole('button', { name: /generating/i })
      expect(submitButton).toBeDisabled()
      
      // Complete the request
      resolveRequest()
      
      await waitFor(() => {
        expect(screen.queryByText(/generating stories/i)).not.toBeInTheDocument()
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
    })

    it('displays success message after successful generation', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Success Test')
      await user.type(screen.getByLabelText(/project description/i), 'Testing success feedback')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Verify story is displayed as success indicator
      expect(screen.querySelector('.story-card')).toBeInTheDocument()
    })

    it('displays clear error messages when generation fails', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(
            { 
              error: true, 
              message: 'Unable to generate story due to service limitations' 
            },
            { status: 500 }
          )
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Error Test')
      await user.type(screen.getByLabelText(/project description/i), 'Testing error feedback')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument()
        expect(screen.getByText(/unable to generate story due to service limitations/i)).toBeInTheDocument()
      })
    })
  })

  describe('AC8: User can reset form and start over', () => {
    it('provides reset functionality that clears all fields', async () => {
      render(<StoryGenerator />)
      
      const formData = generateMockFormData()
      
      // Fill all fields
      await user.type(screen.getByLabelText(/project name/i), formData.projectName)
      await user.type(screen.getByLabelText(/project description/i), formData.projectDescription)
      await user.type(screen.getByLabelText(/target audience/i), formData.targetAudience)
      await user.type(screen.getByLabelText(/key features/i), formData.keyFeatures)
      await user.type(screen.getByLabelText(/technical requirements/i), formData.technicalRequirements)
      
      // Verify fields are filled
      expect(screen.getByDisplayValue(formData.projectName)).toBeInTheDocument()
      expect(screen.getByDisplayValue(formData.projectDescription)).toBeInTheDocument()
      
      // Reset form
      await user.click(screen.getByRole('button', { name: /reset form/i }))
      
      // Verify all fields are cleared
      expect(screen.getByLabelText(/project name/i)).toHaveValue('')
      expect(screen.getByLabelText(/project description/i)).toHaveValue('')
      expect(screen.getByLabelText(/target audience/i)).toHaveValue('')
      expect(screen.getByLabelText(/key features/i)).toHaveValue('')
      expect(screen.getByLabelText(/technical requirements/i)).toHaveValue('')
    })

    it('clears generated stories when form is reset', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      
      // Generate a story
      await user.type(screen.getByLabelText(/project name/i), 'Reset Test')
      await user.type(screen.getByLabelText(/project description/i), 'Testing reset functionality')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
      
      // Reset form
      await user.click(screen.getByRole('button', { name: /reset form/i }))
      
      // Verify stories are cleared
      expect(screen.queryByText(/generated user stories/i)).not.toBeInTheDocument()
    })

    it('resets submit button state after form reset', async () => {
      render(<StoryGenerator />)
      
      // Fill required fields to enable submit button
      await user.type(screen.getByLabelText(/project name/i), 'Test')
      await user.type(screen.getByLabelText(/project description/i), 'Test')
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      expect(submitButton).toBeEnabled()
      
      // Reset form
      await user.click(screen.getByRole('button', { name: /reset form/i }))
      
      // Submit button should be disabled again
      expect(submitButton).toBeDisabled()
    })
  })

  describe('AC9: Application is responsive and accessible', () => {
    it('maintains functionality with keyboard navigation', async () => {
      render(<StoryGenerator />)
      
      // Tab through form fields
      const projectNameField = screen.getByLabelText(/project name/i)
      projectNameField.focus()
      
      await user.type(projectNameField, 'Keyboard Test')
      await user.tab()
      
      const projectDescField = screen.getByLabelText(/project description/i)
      expect(projectDescField).toHaveFocus()
      
      await user.type(projectDescField, 'Testing keyboard navigation')
      
      // Navigate to submit button via keyboard
      await user.tab()
      await user.tab()
      await user.tab()
      await user.tab()
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      expect(submitButton).toHaveFocus()
    })

    it('provides proper ARIA labels and attributes', () => {
      render(<StoryGenerator />)
      
      // Check required field attributes
      expect(screen.getByLabelText(/project name/i)).toHaveAttribute('required')
      expect(screen.getByLabelText(/project description/i)).toHaveAttribute('required')
      
      // Check proper labeling
      expect(screen.getByLabelText(/project name/i)).toHaveAttribute('id')
      expect(screen.getByLabelText(/project description/i)).toHaveAttribute('id')
      
      // Check button accessibility
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      expect(submitButton).toBeInTheDocument()
    })

    it('handles form validation errors accessibly', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(
            { error: true, message: 'Validation failed' },
            { status: 422 }
          )
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Error Test')
      await user.type(screen.getByLabelText(/project description/i), 'Testing error accessibility')
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        const errorMessage = screen.getByText(/validation failed/i)
        expect(errorMessage).toBeInTheDocument()
        
        // Error should be announced to screen readers
        expect(errorMessage.closest('.error-message')).toBeInTheDocument()
      })
    })
  })

  describe('AC10: System handles edge cases gracefully', () => {
    it('handles very long project descriptions', async () => {
      const longDescription = 'A'.repeat(5000) // Very long description

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Long Description Test')
      await user.type(screen.getByLabelText(/project description/i), longDescription)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
    })

    it('handles special characters in input fields', async () => {
      const specialCharacters = '!@#$%^&*()_+{}|:"<>?[]\\;\',./'

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), `Special ${specialCharacters}`)
      await user.type(screen.getByLabelText(/project description/i), `Description with ${specialCharacters}`)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
    })

    it('maintains state during network interruptions', async () => {
      let shouldFail = true

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          if (shouldFail) {
            shouldFail = false
            throw new Error('Network error')
          }
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      
      const formData = generateMockFormData()
      await user.type(screen.getByLabelText(/project name/i), formData.projectName)
      await user.type(screen.getByLabelText(/project description/i), formData.projectDescription)
      
      // First attempt fails
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/failed to generate stories/i)).toBeInTheDocument()
      })
      
      // Form data should still be intact
      expect(screen.getByDisplayValue(formData.projectName)).toBeInTheDocument()
      expect(screen.getByDisplayValue(formData.projectDescription)).toBeInTheDocument()
      
      // Retry should work
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
    })
  })
})