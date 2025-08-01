import { http, HttpResponse } from 'msw'

const API_BASE_URL = 'http://localhost:8000'

export const handlers = [
  // Mock successful story generation
  http.post(`${API_BASE_URL}/api/v1/stories/generate`, async ({ request }) => {
    const body = await request.json()
    
    return HttpResponse.json({
      story_id: 'test-story-123',
      title: 'Test User Story',
      feature_description: body.description,
      gherkin: `Feature: ${body.project_context}
  
  Scenario: User can generate a story
    Given the user has provided a valid description
    When they submit the form
    Then a user story should be generated
    And the story should include acceptance criteria`,
      acceptance_criteria: [
        'System should validate all required fields',
        'Generated story should be in proper Gherkin format',
        'User should receive confirmation of successful generation'
      ],
      estimated_effort: 5,
      story_type: body.story_type || 'user_story',
      priority: 'medium',
      complexity: body.complexity || 'medium',
      status: 'draft',
      tags: ['frontend', 'user_story'],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      project_context: body.project_context,
      quality_metrics: {
        quality_score: 0.85,
        is_valid_gherkin: true,
        syntax_issues: [],
        scenario_count: 1,
        line_count: 6,
        completeness: 0.9
      }
    })
  }),

  // Mock API error responses
  http.post(`${API_BASE_URL}/api/v1/stories/generate-error`, () => {
    return HttpResponse.json(
      {
        error: true,
        message: 'Internal server error',
        status_code: 500
      },
      { status: 500 }
    )
  }),

  // Mock validation error
  http.post(`${API_BASE_URL}/api/v1/stories/generate-validation-error`, () => {
    return HttpResponse.json(
      {
        error: true,
        message: 'Request validation failed',
        details: [
          {
            field: 'description',
            message: 'Description is required'
          }
        ]
      },
      { status: 422 }
    )
  }),

  // Mock story refinement
  http.post(`${API_BASE_URL}/api/v1/stories/refine`, async ({ request }) => {
    const body = await request.json()
    
    return HttpResponse.json({
      story_id: body.story_id,
      title: 'Refined User Story',
      feature_description: 'Refined story description',
      gherkin: `Feature: Refined Story
  
  Scenario: Refined user story scenario
    Given the story has been refined
    When the user reviews the changes
    Then the story should be improved
    And include the requested feedback`,
      acceptance_criteria: [
        'Story should incorporate user feedback',
        'All original requirements should be preserved',
        'New requirements should be clearly defined'
      ],
      estimated_effort: 8,
      story_type: 'user_story',
      priority: 'medium',
      status: 'refined',
      version: 2,
      refinement_history: [
        {
          feedback: body.refinement_feedback,
          refined_at: new Date().toISOString()
        }
      ]
    })
  }),

  // Mock story validation
  http.post(`${API_BASE_URL}/api/v1/stories/validate`, async ({ request }) => {
    const body = await request.json()
    
    return HttpResponse.json({
      is_valid: true,
      issues: [],
      quality_metrics: {
        quality_score: 0.9,
        is_valid_gherkin: true,
        syntax_issues: [],
        scenario_count: 1,
        line_count: body.gherkin_content.split('\n').length,
        completeness: 0.95
      },
      suggestions: [
        'Consider adding more specific acceptance criteria',
        'Add edge case scenarios'
      ]
    })
  }),

  // Mock health check
  http.get(`${API_BASE_URL}/api/v1/stories/system/health`, () => {
    return HttpResponse.json({
      status: 'healthy',
      services: {
        story_generator: 'healthy',
        ai_client: 'healthy',
        storage: 'healthy'
      },
      ai_provider_status: {
        provider: 'mock',
        status: 'available',
        response_time_ms: 50
      }
    })
  })
]