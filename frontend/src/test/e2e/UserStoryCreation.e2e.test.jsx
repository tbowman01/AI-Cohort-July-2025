import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { http, HttpResponse } from 'msw'
import { server } from '../mocks/server'
import App from '../../App'
import { 
  generateMockFormData, 
  generateMockStoryResponse,
  setupTestEnvironment
} from '../utils/testUtils'

describe('User Story Creation - End-to-End Tests', () => {
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

  describe('Complete User Journey', () => {
    it('allows user to complete full story creation workflow', async () => {
      const projectData = {
        projectName: 'TaskFlow Pro',
        projectDescription: 'A comprehensive project management application for agile teams',
        targetAudience: 'Project managers, developers, and team leads',
        keyFeatures: 'Task management, sprint planning, team collaboration, reporting dashboard',
        technicalRequirements: 'React frontend, REST API, real-time updates, mobile responsive'
      }

      const expectedStoryResponse = generateMockStoryResponse({
        title: 'TaskFlow Pro - Project Management User Story',
        gherkin: `Feature: TaskFlow Pro Project Management
  As a project manager
  I want to manage tasks and sprints
  So that I can deliver projects efficiently

Scenario: Create new project
  Given I am logged into TaskFlow Pro
  When I click "New Project"
  And I enter project details
  Then a new project should be created
  And I should see the project dashboard

Scenario: Manage sprint tasks
  Given I have an active project
  When I navigate to the sprint board
  Then I should see all sprint tasks
  And I should be able to drag tasks between columns`,
        acceptance_criteria: [
          'User must be able to create projects with name, description, and timeline',
          'Sprint board must support drag-and-drop functionality',
          'Real-time updates must be visible to all team members',
          'Application must be responsive on mobile devices',
          'Dashboard must show project progress and team metrics'
        ],
        estimated_points: 13,
        tags: ['project-management', 'agile', 'collaboration', 'dashboard']
      })

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', async ({ request }) => {
          const body = await request.json()
          
          // Verify the complete request structure
          expect(body.description).toContain(projectData.projectDescription)
          expect(body.description).toContain(`Target Audience: ${projectData.targetAudience}`)
          expect(body.description).toContain(`Key Features: ${projectData.keyFeatures}`)
          expect(body.description).toContain(`Technical Requirements: ${projectData.technicalRequirements}`)
          expect(body.project_context).toBe(`Project: ${projectData.projectName}`)

          return HttpResponse.json(expectedStoryResponse)
        })
      )

      // Render the full application
      render(<App />)

      // Verify initial app state
      expect(screen.getByText(/autodevhub story generator/i)).toBeInTheDocument()
      expect(screen.getByText(/generate compelling user stories/i)).toBeInTheDocument()

      // Navigate to the form section
      expect(screen.getByText(/project information/i)).toBeInTheDocument()

      // Step 1: Fill out project information
      await user.type(screen.getByLabelText(/project name/i), projectData.projectName)
      await user.type(screen.getByLabelText(/project description/i), projectData.projectDescription)
      await user.type(screen.getByLabelText(/target audience/i), projectData.targetAudience)
      await user.type(screen.getByLabelText(/key features/i), projectData.keyFeatures)
      await user.type(screen.getByLabelText(/technical requirements/i), projectData.technicalRequirements)

      // Verify form is properly filled
      expect(screen.getByDisplayValue(projectData.projectName)).toBeInTheDocument()
      expect(screen.getByDisplayValue(projectData.projectDescription)).toBeInTheDocument()

      // Step 2: Submit the form
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      expect(submitButton).toBeEnabled()
      
      await user.click(submitButton)

      // Step 3: Verify loading state
      expect(screen.getByText(/generating stories/i)).toBeInTheDocument()
      expect(screen.getByText(/generating user stories for your project/i)).toBeInTheDocument()
      expect(submitButton).toBeDisabled()

      // Step 4: Wait for story generation to complete
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      }, { timeout: 5000 })

      // Step 5: Verify the generated story content
      const storyCard = screen.getByRole('region', { name: /story/i }) || screen.querySelector('.story-card')
      expect(storyCard).toBeInTheDocument()

      // Verify story header
      expect(screen.getByText(/story #1/i)).toBeInTheDocument()
      expect(screen.getByText('Medium')).toBeInTheDocument() // priority

      // Verify Gherkin content
      expect(screen.getByText(/feature: taskflow pro project management/i)).toBeInTheDocument()
      expect(screen.getByText(/scenario: create new project/i)).toBeInTheDocument()
      expect(screen.getByText(/scenario: manage sprint tasks/i)).toBeInTheDocument()

      // Verify acceptance criteria
      expect(screen.getByText(/acceptance criteria/i)).toBeInTheDocument()
      expect(screen.getByText(/user must be able to create projects/i)).toBeInTheDocument()
      expect(screen.getByText(/sprint board must support drag-and-drop/i)).toBeInTheDocument()
      expect(screen.getByText(/real-time updates must be visible/i)).toBeInTheDocument()

      // Verify story metadata
      expect(screen.getByText(/estimated story points/i)).toBeInTheDocument()
      expect(screen.getByText('13')).toBeInTheDocument()

      // Verify tags
      expect(screen.getByText(/tags/i)).toBeInTheDocument()
      expect(screen.getByText('project-management')).toBeInTheDocument()
      expect(screen.getByText('agile')).toBeInTheDocument()
      expect(screen.getByText('collaboration')).toBeInTheDocument()

      // Verify story details
      expect(screen.getByText(/story details/i)).toBeInTheDocument()
      expect(screen.getByText(/type:/i)).toBeInTheDocument()
      expect(screen.getByText(/complexity:/i)).toBeInTheDocument()
      expect(screen.getByText(/status:/i)).toBeInTheDocument()
      expect(screen.getByText(/created:/i)).toBeInTheDocument()

      // Step 6: Verify form is still intact (not reset)
      expect(screen.getByDisplayValue(projectData.projectName)).toBeInTheDocument()
      expect(submitButton).toBeEnabled()
    })

    it('handles complete error recovery workflow', async () => {
      const projectData = generateMockFormData()
      let requestCount = 0

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          requestCount++
          
          if (requestCount === 1) {
            return HttpResponse.json(
              { 
                error: true, 
                message: 'Service temporarily unavailable. Please try again.',
                code: 'SERVICE_UNAVAILABLE'
              },
              { status: 503 }
            )
          } else {
            return HttpResponse.json(generateMockStoryResponse({
              title: 'Recovered Story Generation'
            }))
          }
        })
      )

      render(<App />)

      // Fill form
      await user.type(screen.getByLabelText(/project name/i), projectData.projectName)
      await user.type(screen.getByLabelText(/project description/i), projectData.projectDescription)

      // First attempt - should fail
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/service temporarily unavailable/i)).toBeInTheDocument()
      })

      // Verify error state
      expect(screen.getByText(/error/i)).toBeInTheDocument()
      expect(screen.queryByText(/generated user stories/i)).not.toBeInTheDocument()

      // Retry - should succeed
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Verify recovery
      expect(screen.queryByText(/service temporarily unavailable/i)).not.toBeInTheDocument()
      expect(screen.getByText(/recovered story generation/i)).toBeInTheDocument()
    })

    it('supports complete form reset and regeneration workflow', async () => {
      const initialData = generateMockFormData({
        projectName: 'Initial Project',
        projectDescription: 'Initial description'
      })

      const newData = generateMockFormData({
        projectName: 'New Project',
        projectDescription: 'New description'
      })

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', async ({ request }) => {
          const body = await request.json()
          
          if (body.project_context.includes('Initial Project')) {
            return HttpResponse.json(generateMockStoryResponse({
              title: 'Initial Project Story'
            }))
          } else {
            return HttpResponse.json(generateMockStoryResponse({
              title: 'New Project Story'
            }))
          }
        })
      )

      render(<App />)

      // Fill initial form
      await user.type(screen.getByLabelText(/project name/i), initialData.projectName)
      await user.type(screen.getByLabelText(/project description/i), initialData.projectDescription)

      // Generate initial story
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/initial project story/i)).toBeInTheDocument()
      })

      // Reset form
      await user.click(screen.getByRole('button', { name: /reset form/i }))

      // Verify reset
      expect(screen.getByLabelText(/project name/i)).toHaveValue('')
      expect(screen.getByLabelText(/project description/i)).toHaveValue('')
      expect(screen.queryByText(/generated user stories/i)).not.toBeInTheDocument()

      // Fill new form data
      await user.type(screen.getByLabelText(/project name/i), newData.projectName)
      await user.type(screen.getByLabelText(/project description/i), newData.projectDescription)

      // Generate new story
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/new project story/i)).toBeInTheDocument()
      })

      // Verify old story is not present
      expect(screen.queryByText(/initial project story/i)).not.toBeInTheDocument()
    })
  })

  describe('User Experience Flow', () => {
    it('provides clear visual feedback throughout the entire process', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', async () => {
          // Simulate processing time for visual feedback testing
          await new Promise(resolve => setTimeout(resolve, 100))
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<App />)

      // Initial state - submit button disabled
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      expect(submitButton).toBeDisabled()

      // Fill required fields
      await user.type(screen.getByLabelText(/project name/i), 'Test Project')
      await user.type(screen.getByLabelText(/project description/i), 'Test description')

      // Submit button should be enabled
      expect(submitButton).toBeEnabled()

      // Click submit
      await user.click(submitButton)

      // Verify loading state visual elements
      expect(screen.getByText(/generating stories/i)).toBeInTheDocument()
      expect(screen.getByRole('progressbar') || screen.querySelector('.spinner')).toBeInTheDocument()
      expect(submitButton).toBeDisabled()
      expect(submitButton).toHaveTextContent(/generating/i)

      // Wait for completion
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Verify post-completion state
      expect(screen.queryByText(/generating stories/i)).not.toBeInTheDocument()
      expect(submitButton).toBeEnabled()
      expect(submitButton).toHaveTextContent(/generate user stories/i)
    })

    it('maintains accessibility throughout the workflow', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<App />)

      // Verify initial accessibility
      expect(screen.getByLabelText(/project name/i)).toHaveAttribute('required')
      expect(screen.getByLabelText(/project description/i)).toHaveAttribute('required')

      // Fill form and verify accessibility is maintained
      const projectNameField = screen.getByLabelText(/project name/i)
      await user.type(projectNameField, 'Accessible Project')
      
      expect(projectNameField).toHaveFocus()

      // Tab navigation should work
      await user.tab()
      expect(screen.getByLabelText(/project description/i)).toHaveFocus()

      await user.type(screen.getByLabelText(/project description/i), 'Accessible description')

      // Submit with keyboard
      await user.tab({ shift: true }) // Go back to submit button area
      await user.tab() // Navigate to submit button
      await user.tab() // Navigate to submit button
      await user.tab() // Navigate to submit button
      await user.tab() // Navigate to submit button
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      await user.click(submitButton)

      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Verify generated content has proper structure for screen readers
      const storyHeading = screen.getByText(/generated user stories/i)
      expect(storyHeading).toHaveProperty('tagName', 'H2')
    })

    it('handles edge cases in user interaction patterns', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<App />)

      // Edge case: Rapid form filling
      const projectName = screen.getByLabelText(/project name/i)
      const projectDescription = screen.getByLabelText(/project description/i)

      await user.type(projectName, 'Rapid Test')
      await user.clear(projectName)
      await user.type(projectName, 'Final Name')
      
      await user.type(projectDescription, 'Quick description')

      // Edge case: Multiple rapid clicks on submit
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      
      // Click multiple times rapidly
      await user.click(submitButton)
      await user.click(submitButton)
      await user.click(submitButton)

      // Should only generate one story
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Should only show one story card
      const storyCards = screen.getAllByText(/story #/i)
      expect(storyCards).toHaveLength(1)
    })
  })

  describe('Data Persistence and State Management', () => {
    it('maintains form state during API interactions', async () => {
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

      render(<App />)

      const formData = generateMockFormData()
      
      // Fill all form fields
      await user.type(screen.getByLabelText(/project name/i), formData.projectName)
      await user.type(screen.getByLabelText(/project description/i), formData.projectDescription)
      await user.type(screen.getByLabelText(/target audience/i), formData.targetAudience)
      await user.type(screen.getByLabelText(/key features/i), formData.keyFeatures)
      await user.type(screen.getByLabelText(/technical requirements/i), formData.technicalRequirements)

      // Submit form
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      // Verify form fields are still populated during loading
      expect(screen.getByDisplayValue(formData.projectName)).toBeInTheDocument()
      expect(screen.getByDisplayValue(formData.projectDescription)).toBeInTheDocument()
      expect(screen.getByDisplayValue(formData.targetAudience)).toBeInTheDocument()
      expect(screen.getByDisplayValue(formData.keyFeatures)).toBeInTheDocument()
      expect(screen.getByDisplayValue(formData.technicalRequirements)).toBeInTheDocument()

      // Complete the request
      resolveRequest()

      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Verify form fields are still populated after completion
      expect(screen.getByDisplayValue(formData.projectName)).toBeInTheDocument()
      expect(screen.getByDisplayValue(formData.projectDescription)).toBeInTheDocument()
    })

    it('handles browser navigation and page refresh scenarios', async () => {
      // Note: This is a simplified test since we can't actually refresh the page in this environment
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<App />)

      // Fill form and generate story
      await user.type(screen.getByLabelText(/project name/i), 'Navigation Test')
      await user.type(screen.getByLabelText(/project description/i), 'Testing navigation handling')

      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Simulate component remount (similar to page refresh)
      const { unmount } = render(<App />)
      unmount()
      render(<App />)

      // Verify app returns to initial state
      expect(screen.getByLabelText(/project name/i)).toHaveValue('')
      expect(screen.queryByText(/generated user stories/i)).not.toBeInTheDocument()
    })
  })
})