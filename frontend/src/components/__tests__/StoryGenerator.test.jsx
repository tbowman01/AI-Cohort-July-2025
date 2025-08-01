import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import StoryGenerator from '../StoryGenerator'
import { 
  renderWithProviders, 
  generateMockFormData, 
  generateMockStoryResponse,
  mockFetch,
  fillFormFields,
  expectFormFieldsToBeEmpty,
  expectFormFieldsToHaveValues,
  expectErrorMessage,
  expectNoErrorMessage,
  expectLoadingState,
  expectStoryToBeDisplayed,
  setupTestEnvironment
} from '../../test/utils/testUtils'

describe('StoryGenerator Component', () => {
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

  describe('Component Rendering', () => {
    it('renders the component with all form fields', () => {
      render(<StoryGenerator />)
      
      expect(screen.getByRole('heading', { name: /project information/i })).toBeInTheDocument()
      expect(screen.getByLabelText(/project name/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/project description/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/target audience/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/key features/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/technical requirements/i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /generate user stories/i })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /reset form/i })).toBeInTheDocument()
    })

    it('renders with correct initial state', () => {
      render(<StoryGenerator />)
      
      expectFormFieldsToBeEmpty()
      expect(screen.getByRole('button', { name: /generate user stories/i })).toBeDisabled()
      expectNoErrorMessage()
      expectLoadingState(false)
    })

    it('has proper form labels and placeholders', () => {
      render(<StoryGenerator />)
      
      expect(screen.getByPlaceholderText(/enter your project name/i)).toBeInTheDocument()
      expect(screen.getByPlaceholderText(/describe what your project does/i)).toBeInTheDocument()
      expect(screen.getByPlaceholderText(/who will use this application/i)).toBeInTheDocument()
      expect(screen.getByPlaceholderText(/list the main features/i)).toBeInTheDocument()
      expect(screen.getByPlaceholderText(/any specific technical constraints/i)).toBeInTheDocument()
    })
  })

  describe('Form Interactions', () => {
    it('allows user to fill all form fields', async () => {
      render(<StoryGenerator />)
      const formData = generateMockFormData()
      
      await fillFormFields(user, formData)
      
      expectFormFieldsToHaveValues(formData)
    })

    it('enables submit button when required fields are filled', async () => {
      render(<StoryGenerator />)
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      
      expect(submitButton).toBeDisabled()
      
      await user.type(screen.getByLabelText(/project name/i), 'Test Project')
      await user.type(screen.getByLabelText(/project description/i), 'Test Description')
      
      expect(submitButton).toBeEnabled()
    })

    it('keeps submit button disabled if only one required field is filled', async () => {
      render(<StoryGenerator />)
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      
      await user.type(screen.getByLabelText(/project name/i), 'Test Project')
      expect(submitButton).toBeDisabled()
      
      await user.clear(screen.getByLabelText(/project name/i))
      await user.type(screen.getByLabelText(/project description/i), 'Test Description')
      expect(submitButton).toBeDisabled()
    })

    it('allows user to clear individual fields', async () => {
      render(<StoryGenerator />)
      
      await user.type(screen.getByLabelText(/project name/i), 'Test Project')
      expect(screen.getByLabelText(/project name/i)).toHaveValue('Test Project')
      
      await user.clear(screen.getByLabelText(/project name/i))
      expect(screen.getByLabelText(/project name/i)).toHaveValue('')
    })
  })

  describe('Form Submission - Success Cases', () => {
    it('submits form successfully and displays generated story', async () => {
      const mockStoryResponse = generateMockStoryResponse()
      global.fetch = mockFetch(mockStoryResponse)
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      await user.click(submitButton)
      
      // Check loading state
      expectLoadingState(true)
      
      // Wait for API call to complete
      await waitFor(() => {
        expectLoadingState(false)
      })
      
      // Verify story is displayed
      expectStoryToBeDisplayed(mockStoryResponse)
    })

    it('makes correct API call with transformed payload', async () => {
      const mockStoryResponse = generateMockStoryResponse()
      global.fetch = mockFetch(mockStoryResponse)
      
      render(<StoryGenerator />)
      const formData = generateMockFormData()
      await fillFormFields(user, formData)
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      await user.click(submitButton)
      
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/v1/stories/generate',
          expect.objectContaining({
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: expect.stringContaining(formData.projectDescription)
          })
        )
      })
      
      // Verify the payload structure
      const callArgs = global.fetch.mock.calls[0]
      const payload = JSON.parse(callArgs[1].body)
      
      expect(payload).toMatchObject({
        description: expect.stringContaining(formData.projectDescription),
        project_context: `Project: ${formData.projectName}`,
        story_type: 'user_story',
        complexity: 'medium'
      })
    })

    it('displays all story details correctly', async () => {
      const mockStoryResponse = generateMockStoryResponse({
        gherkin: 'Feature: Test Feature\n\nScenario: Test scenario\n  Given a condition\n  When an action\n  Then a result',
        acceptance_criteria: ['Criteria 1', 'Criteria 2', 'Criteria 3'],
        estimated_points: 8,
        tags: ['frontend', 'api', 'testing']
      })
      global.fetch = mockFetch(mockStoryResponse)
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
      
      // Check story content
      expect(screen.getByText(/feature: test feature/i)).toBeInTheDocument()
      expect(screen.getByText(/criteria 1/i)).toBeInTheDocument()
      expect(screen.getByText(/criteria 2/i)).toBeInTheDocument()
      expect(screen.getByText(/criteria 3/i)).toBeInTheDocument()
      expect(screen.getByText('8')).toBeInTheDocument()
      expect(screen.getByText('frontend')).toBeInTheDocument()
      expect(screen.getByText('api')).toBeInTheDocument()
      expect(screen.getByText('testing')).toBeInTheDocument()
    })
  })

  describe('Form Submission - Error Cases', () => {
    it('displays error message when API returns 500 error', async () => {
      global.fetch = mockFetch(
        { error: true, message: 'Internal server error' },
        { status: 500, ok: false }
      )
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expectErrorMessage('Failed to generate stories: Internal server error')
      })
      
      expectLoadingState(false)
    })

    it('displays error message when API returns 422 validation error', async () => {
      global.fetch = mockFetch(
        { 
          error: true, 
          message: 'Validation failed',
          details: [{ field: 'description', message: 'Description is required' }]
        },
        { status: 422, ok: false }
      )
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expectErrorMessage('Failed to generate stories: Validation failed')
      })
    })

    it('displays generic error message when API returns non-JSON response', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        json: vi.fn().mockRejectedValue(new Error('Invalid JSON'))
      })
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expectErrorMessage('Failed to generate stories: HTTP error! status: 500')
      })
    })

    it('displays error message when network request fails', async () => {
      global.fetch = vi.fn().mockRejectedValue(new Error('Network error'))
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expectErrorMessage('Failed to generate stories: Network error')
      })
    })

    it('clears previous error when making new successful request', async () => {
      // First request fails
      global.fetch = mockFetch(
        { error: true, message: 'Server error' },
        { status: 500, ok: false }
      )
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expectErrorMessage('Failed to generate stories: Server error')
      })
      
      // Second request succeeds
      global.fetch = mockFetch(generateMockStoryResponse())
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expectNoErrorMessage()
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
    })
  })

  describe('Loading States', () => {
    it('shows loading state during API request', async () => {
      // Create a delayed response
      global.fetch = vi.fn().mockImplementation(() => 
        new Promise(resolve => {
          setTimeout(() => {
            resolve({
              ok: true,
              status: 200,
              json: () => Promise.resolve(generateMockStoryResponse())
            })
          }, 100)
        })
      )
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      // Should show loading immediately
      expectLoadingState(true)
      
      // Wait for completion
      await waitFor(() => {
        expectLoadingState(false)
      }, { timeout: 1000 })
    })

    it('disables form fields during loading', async () => {
      global.fetch = vi.fn().mockImplementation(() => 
        new Promise(resolve => {
          setTimeout(() => {
            resolve({
              ok: true,
              status: 200,
              json: () => Promise.resolve(generateMockStoryResponse())
            })
          }, 100)
        })
      )
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      const resetButton = screen.getByRole('button', { name: /reset form/i })
      
      await user.click(submitButton)
      
      expect(submitButton).toBeDisabled()
      expect(resetButton).toBeDisabled()
      expect(submitButton).toHaveTextContent(/generating/i)
      
      await waitFor(() => {
        expect(submitButton).not.toBeDisabled()
        expect(resetButton).not.toBeDisabled()
      }, { timeout: 1000 })
    })
  })

  describe('Form Reset', () => {
    it('resets all form fields when reset button is clicked', async () => {
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      // Verify fields are filled
      expectFormFieldsToHaveValues(generateMockFormData())
      
      const resetButton = screen.getByRole('button', { name: /reset form/i })
      await user.click(resetButton)
      
      // Verify fields are cleared
      expectFormFieldsToBeEmpty()
    })

    it('clears generated stories when reset button is clicked', async () => {
      const mockStoryResponse = generateMockStoryResponse()
      global.fetch = mockFetch(mockStoryResponse)
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      // Generate story first
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
      
      // Reset form
      const resetButton = screen.getByRole('button', { name: /reset form/i })
      await user.click(resetButton)
      
      // Verify stories are cleared
      expect(screen.queryByText(/generated user stories/i)).not.toBeInTheDocument()
    })

    it('clears error messages when reset button is clicked', async () => {
      global.fetch = mockFetch(
        { error: true, message: 'Server error' },
        { status: 500, ok: false }
      )
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      // Generate error
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expectErrorMessage('Failed to generate stories: Server error')
      })
      
      // Reset form
      const resetButton = screen.getByRole('button', { name: /reset form/i })
      await user.click(resetButton)
      
      // Verify error is cleared
      expectNoErrorMessage()
    })

    it('resets submit button state when form is reset', async () => {
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      expect(submitButton).toBeEnabled()
      
      const resetButton = screen.getByRole('button', { name: /reset form/i })
      await user.click(resetButton)
      
      expect(submitButton).toBeDisabled()
    })
  })

  describe('Accessibility', () => {
    it('has proper form labels and ARIA attributes', () => {
      render(<StoryGenerator />)
      
      expect(screen.getByLabelText(/project name/i)).toHaveAttribute('required')
      expect(screen.getByLabelText(/project description/i)).toHaveAttribute('required')
      expect(screen.getByRole('button', { name: /generate user stories/i })).toHaveAttribute('disabled')
    })

    it('maintains focus management during interactions', async () => {
      render(<StoryGenerator />)
      
      const projectNameField = screen.getByLabelText(/project name/i)
      projectNameField.focus()
      
      expect(projectNameField).toHaveFocus()
    })
  })

  describe('Edge Cases', () => {
    it('handles empty API response gracefully', async () => {
      global.fetch = mockFetch({})
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
        expect(screen.getByText(/no story content available/i)).toBeInTheDocument()
      })
    })

    it('handles API response with missing fields', async () => {
      const incompleteResponse = {
        story_id: 'test-id',
        // Missing other fields
      }
      global.fetch = mockFetch(incompleteResponse)
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
        // Should handle missing fields gracefully
      })
    })

    it('prevents double submission during loading', async () => {
      let resolvePromise
      global.fetch = vi.fn().mockImplementation(() => 
        new Promise(resolve => {
          resolvePromise = () => resolve({
            ok: true,
            status: 200,
            json: () => Promise.resolve(generateMockStoryResponse())
          })
        })
      )
      
      render(<StoryGenerator />)
      await fillFormFields(user)
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      
      // First click
      await user.click(submitButton)
      expect(submitButton).toBeDisabled()
      
      // Second click should not trigger another request
      await user.click(submitButton)
      expect(global.fetch).toHaveBeenCalledTimes(1)
      
      // Complete the request
      resolvePromise()
      
      await waitFor(() => {
        expect(submitButton).not.toBeDisabled()
      })
    })
  })
})