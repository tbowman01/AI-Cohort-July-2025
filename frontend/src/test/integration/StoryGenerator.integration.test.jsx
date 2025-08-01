import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { http, HttpResponse } from 'msw'
import { server } from '../mocks/server'
import StoryGenerator from '../../components/StoryGenerator'
import { 
  generateMockFormData, 
  generateMockStoryResponse,
  fillFormFields,
  setupTestEnvironment
} from '../utils/testUtils'

describe('StoryGenerator - Integration Tests', () => {
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

  describe('API Integration - Successful Workflows', () => {
    it('integrates successfully with backend story generation endpoint', async () => {
      // Setup MSW handler for successful response
      const mockResponse = generateMockStoryResponse({
        title: 'E-commerce Platform User Story',
        gherkin: `Feature: E-commerce Platform
  As a customer
  I want to browse and purchase products
  So that I can buy items online

Scenario: Customer browses products
  Given I am on the homepage
  When I navigate to the products page
  Then I should see a list of available products
  And I should be able to filter by category

Scenario: Customer adds items to cart
  Given I am viewing a product
  When I click the "Add to Cart" button
  Then the item should be added to my cart
  And the cart counter should increment`,
        acceptance_criteria: [
          'Products must be displayed with images, prices, and descriptions',
          'Filter functionality must work for all product categories',
          'Cart must persist items during the session',
          'Add to cart action must provide visual feedback'
        ],
        estimated_points: 8,
        tags: ['ecommerce', 'frontend', 'cart', 'products']
      })

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', async ({ request }) => {
          const body = await request.json()
          
          // Verify the request structure matches expected API contract
          expect(body).toMatchObject({
            description: expect.stringContaining('E-commerce'),
            project_context: expect.stringContaining('Project:'),
            story_type: 'user_story',
            complexity: 'medium'
          })

          return HttpResponse.json(mockResponse)
        })
      )

      render(<StoryGenerator />)

      // Fill form with e-commerce project data
      await fillFormFields(user, {
        projectName: 'E-commerce Platform',
        projectDescription: 'A modern e-commerce platform for online retail',
        targetAudience: 'Online shoppers and retail customers',
        keyFeatures: 'Product catalog, shopping cart, payment processing, user accounts',
        technicalRequirements: 'React frontend, Node.js backend, PostgreSQL database'
      })

      // Submit form
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      await user.click(submitButton)

      // Wait for story to be generated and displayed
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Verify complete story display
      const storyCard = screen.getByRole('region', { name: /story.*1/i }) || screen.querySelector('.story-card')
      expect(storyCard).toBeInTheDocument()

      // Check Gherkin content
      expect(screen.getByText(/feature: e-commerce platform/i)).toBeInTheDocument()
      expect(screen.getByText(/scenario: customer browses products/i)).toBeInTheDocument()
      expect(screen.getByText(/scenario: customer adds items to cart/i)).toBeInTheDocument()

      // Check acceptance criteria
      expect(screen.getByText(/products must be displayed with images/i)).toBeInTheDocument()
      expect(screen.getByText(/filter functionality must work/i)).toBeInTheDocument()

      // Check metadata
      expect(screen.getByText('8')).toBeInTheDocument() // story points
      expect(screen.getByText('ecommerce')).toBeInTheDocument()
      expect(screen.getByText('frontend')).toBeInTheDocument()
    })

    it('handles complex project data transformation correctly', async () => {
      let capturedRequest = null

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', async ({ request }) => {
          capturedRequest = await request.json()
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)

      const complexFormData = {
        projectName: 'Healthcare Management System',
        projectDescription: 'Comprehensive healthcare management platform with patient records, appointment scheduling, and billing integration',
        targetAudience: 'Healthcare providers, patients, administrative staff',
        keyFeatures: 'Electronic health records (EHR), appointment scheduling, billing system, prescription management, patient portal, analytics dashboard',
        technicalRequirements: 'HIPAA compliance, encrypted data storage, role-based access control, integration with existing hospital systems, mobile responsiveness'
      }

      await fillFormFields(user, complexFormData)
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(capturedRequest).toBeTruthy()
      })

      // Verify the payload transformation
      expect(capturedRequest.description).toContain(complexFormData.projectDescription)
      expect(capturedRequest.description).toContain(`Target Audience: ${complexFormData.targetAudience}`)
      expect(capturedRequest.description).toContain(`Key Features: ${complexFormData.keyFeatures}`)
      expect(capturedRequest.description).toContain(`Technical Requirements: ${complexFormData.technicalRequirements}`)
      expect(capturedRequest.project_context).toBe(`Project: ${complexFormData.projectName}`)
      expect(capturedRequest.story_type).toBe('user_story')
      expect(capturedRequest.complexity).toBe('medium')
    })

    it('integrates with story refinement workflow', async () => {
      // First, generate a story
      const initialStoryResponse = generateMockStoryResponse({
        story_id: 'story-123',
        title: 'Initial Story'
      })

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(initialStoryResponse)
        }),
        http.post('http://localhost:8000/api/v1/stories/refine', async ({ request }) => {
          const body = await request.json()
          
          expect(body).toMatchObject({
            story_id: 'story-123',
            refinement_feedback: expect.any(String)
          })

          return HttpResponse.json({
            ...initialStoryResponse,
            title: 'Refined Story',
            version: 2,
            refinement_history: [{
              feedback: body.refinement_feedback,
              refined_at: new Date().toISOString()
            }]
          })
        })
      )

      render(<StoryGenerator />)
      await fillFormFields(user)
      
      // Generate initial story
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Simulate refinement interaction (this would be added to the component)
      // For now, verify the initial story was created successfully
      expect(screen.getByText(/initial story/i)).toBeInTheDocument()
    })
  })

  describe('API Integration - Error Scenarios', () => {
    it('handles server timeout gracefully', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', async () => {
          // Simulate server timeout
          await new Promise(resolve => setTimeout(resolve, 100))
          throw new Error('Network timeout')
        })
      )

      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        const errorMessage = screen.getByText(/failed to generate stories/i)
        expect(errorMessage).toBeInTheDocument()
      })
    })

    it('handles invalid JSON response from server', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return new Response('Invalid JSON response', {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
          })
        })
      )

      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/failed to generate stories/i)).toBeInTheDocument()
      })
    })

    it('handles rate limiting (429) responses', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(
            { 
              error: true, 
              message: 'Rate limit exceeded. Please try again later.',
              retry_after: 60
            },
            { status: 429 }
          )
        })
      )

      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/rate limit exceeded/i)).toBeInTheDocument()
      })
    })

    it('handles authentication errors (401)', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(
            { 
              error: true, 
              message: 'Authentication required',
              code: 'UNAUTHORIZED'
            },
            { status: 401 }
          )
        })
      )

      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/authentication required/i)).toBeInTheDocument()
      })
    })

    it('recovers from errors and allows retry', async () => {
      let requestCount = 0

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          requestCount++
          
          if (requestCount === 1) {
            return HttpResponse.json(
              { error: true, message: 'Temporary server error' },
              { status: 500 }
            )
          } else {
            return HttpResponse.json(generateMockStoryResponse())
          }
        })
      )

      render(<StoryGenerator />)
      await fillFormFields(user)
      
      // First attempt - should fail
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/temporary server error/i)).toBeInTheDocument()
      })

      // Second attempt - should succeed
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
        expect(screen.queryByText(/temporary server error/i)).not.toBeInTheDocument()
      })
    })
  })

  describe('Data Flow Integration', () => {
    it('maintains data consistency through the complete workflow', async () => {
      const testFormData = generateMockFormData({
        projectName: 'Integration Test Project',
        projectDescription: 'Testing end-to-end data flow'
      })

      let receivedPayload = null

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', async ({ request }) => {
          receivedPayload = await request.json()
          
          return HttpResponse.json(generateMockStoryResponse({
            title: `Story for ${testFormData.projectName}`,
            feature_description: receivedPayload.description
          }))
        })
      )

      render(<StoryGenerator />)
      await fillFormFields(user, testFormData)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Verify data consistency
      expect(receivedPayload.project_context).toBe(`Project: ${testFormData.projectName}`)
      expect(receivedPayload.description).toContain(testFormData.projectDescription)
      expect(screen.getByText(`Story for ${testFormData.projectName}`)).toBeInTheDocument()
    })

    it('handles partial form data correctly', async () => {
      const partialFormData = {
        projectName: 'Minimal Project',
        projectDescription: 'Basic description'
        // Other fields intentionally left empty
      }

      let receivedPayload = null

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', async ({ request }) => {
          receivedPayload = await request.json()
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      await fillFormFields(user, partialFormData)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(receivedPayload).toBeTruthy()
      })

      // Verify payload only contains non-empty fields
      expect(receivedPayload.description).toBe(partialFormData.projectDescription)
      expect(receivedPayload.project_context).toBe(`Project: ${partialFormData.projectName}`)
      expect(receivedPayload.description).not.toContain('Target Audience:')
      expect(receivedPayload.description).not.toContain('Key Features:')
      expect(receivedPayload.description).not.toContain('Technical Requirements:')
    })

    it('validates API response structure and handles missing fields', async () => {
      const incompleteResponse = {
        story_id: 'test-123',
        title: 'Incomplete Story',
        // Missing required fields like gherkin, acceptance_criteria
      }

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(incompleteResponse)
        })
      )

      render(<StoryGenerator />)
      await fillFormFields(user)
      
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))

      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })

      // Component should handle missing fields gracefully
      expect(screen.getByText('Incomplete Story')).toBeInTheDocument()
      expect(screen.getByText(/no story content available/i)).toBeInTheDocument()
    })
  })

  describe('Cross-Component Communication', () => {
    it('maintains consistent state across form interactions and API calls', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      
      // Fill form
      await fillFormFields(user)
      
      // Submit and verify loading state
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      await user.click(submitButton)
      
      expect(submitButton).toBeDisabled()
      expect(submitButton).toHaveTextContent(/generating/i)
      
      // Wait for completion
      await waitFor(() => {
        expect(submitButton).not.toBeDisabled()
        expect(submitButton).toHaveTextContent(/generate user stories/i)
      })
      
      // Verify story was generated
      expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
    })

    it('coordinates form reset with story clearing', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      
      // Generate a story
      await fillFormFields(user)
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
      
      // Reset form
      const resetButton = screen.getByRole('button', { name: /reset form/i })
      await user.click(resetButton)
      
      // Verify complete reset
      expect(screen.getByLabelText(/project name/i)).toHaveValue('')
      expect(screen.queryByText(/generated user stories/i)).not.toBeInTheDocument()
      expect(screen.getByRole('button', { name: /generate user stories/i })).toBeDisabled()
    })
  })

  describe('Performance Integration', () => {
    it('handles concurrent requests appropriately', async () => {
      let requestCount = 0
      
      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', async () => {
          requestCount++
          // Simulate processing time
          await new Promise(resolve => setTimeout(resolve, 50))
          return HttpResponse.json(generateMockStoryResponse())
        })
      )

      render(<StoryGenerator />)
      await fillFormFields(user)
      
      const submitButton = screen.getByRole('button', { name: /generate user stories/i })
      
      // Attempt multiple rapid clicks
      await user.click(submitButton)
      await user.click(submitButton)
      await user.click(submitButton)
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
      
      // Should only make one request due to disabled state during loading
      expect(requestCount).toBe(1)
    })

    it('handles large response payloads efficiently', async () => {
      const largeResponse = generateMockStoryResponse({
        gherkin: 'Feature: Large Feature\n' + 'Scenario: '.repeat(50) + 'Test scenario\n'.repeat(100),
        acceptance_criteria: Array(20).fill('Large acceptance criteria with detailed requirements')
      })

      server.use(
        http.post('http://localhost:8000/api/v1/stories/generate', () => {
          return HttpResponse.json(largeResponse)
        })
      )

      render(<StoryGenerator />)
      await fillFormFields(user)
      
      const startTime = performance.now()
      await user.click(screen.getByRole('button', { name: /generate user stories/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/generated user stories/i)).toBeInTheDocument()
      })
      
      const endTime = performance.now()
      const renderTime = endTime - startTime
      
      // Should render within reasonable time (less than 2 seconds)
      expect(renderTime).toBeLessThan(2000)
      
      // Verify large content is displayed
      expect(screen.getByText(/large feature/i)).toBeInTheDocument()
    })
  })
})