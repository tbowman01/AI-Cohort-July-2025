"""
FastAPI router for story generation endpoints

This module provides REST API endpoints for user story generation,
refinement, validation, and management functionality.
"""

import logging
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from fastapi.responses import JSONResponse
import asyncio
import uuid

# Import services and schemas
from ..services.story_generator import StoryGenerator, StoryType as ServiceStoryType, Priority as ServicePriority
from ..services.ai_client import AIClient, create_ai_client
from ..schemas.story_schemas import (
    StoryGenerationRequest,
    StoryRefinementRequest,
    StoryResponse,
    StoryListResponse,
    StoryValidationRequest,
    StoryValidationResponse,
    StorySuggestionsRequest,
    StorySuggestionsResponse,
    AIProviderStatus,
    HealthCheckResponse,
    ErrorResponse,
    create_story_response,
    create_error_response,
    create_quality_metrics
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter(
    prefix="/api/v1/stories",
    tags=["stories"],
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)

# In-memory storage for demo purposes (replace with database in production)
story_storage = {}


# Dependency functions
async def get_story_generator() -> StoryGenerator:
    """Dependency to get story generator instance"""
    return StoryGenerator()


async def get_ai_client() -> AIClient:
    """Dependency to get AI client instance"""
    return create_ai_client()


# Utility functions
def convert_service_types(story_type: str, priority: str):
    """Convert API types to service types"""
    service_story_type = ServiceStoryType(story_type)
    service_priority = ServicePriority(priority)
    return service_story_type, service_priority


async def store_story(story_data: dict) -> str:
    """Store story in memory (replace with database persistence)"""
    story_id = story_data.get('story_id')
    story_storage[story_id] = story_data
    logger.info(f"Stored story with ID: {story_id}")
    return story_id


async def get_story(story_id: str) -> Optional[dict]:
    """Retrieve story from memory"""
    return story_storage.get(story_id)


async def update_story(story_id: str, story_data: dict) -> bool:
    """Update story in memory"""
    if story_id in story_storage:
        story_storage[story_id] = story_data
        logger.info(f"Updated story with ID: {story_id}")
        return True
    return False


# API Endpoints

@router.post(
    "/generate",
    response_model=StoryResponse,
    summary="Generate User Story",
    description="Generate a user story in Gherkin format from a natural language feature description",
    response_description="Generated user story with metadata"
)
async def generate_story(
    request: StoryGenerationRequest,
    background_tasks: BackgroundTasks,
    generator: StoryGenerator = Depends(get_story_generator),
    ai_client: AIClient = Depends(get_ai_client)
) -> StoryResponse:
    """
    Generate a user story from a feature description.
    
    This endpoint converts natural language feature descriptions into
    structured Gherkin user stories with acceptance criteria.
    """
    try:
        logger.info(f"Generating story for: {request.feature_description[:50]}...")
        
        # Convert API types to service types
        service_story_type, service_priority = convert_service_types(
            request.story_type.value, 
            request.priority.value
        )
        
        # Generate story using appropriate method
        if request.use_ai:
            # Use AI-enhanced generation
            story_data = await ai_client.generate_story_with_ai(
                request.feature_description,
                request.context
            )
        else:
            # Use template-based generation
            story_data = generator.generate_gherkin_story(
                request.feature_description,
                service_story_type,
                service_priority
            )
        
        # Add request metadata
        story_data.update({
            'project_id': request.project_id,
            'status': 'draft'
        })
        
        # Generate quality metrics
        quality_analysis = await ai_client.analyze_story_quality(story_data['gherkin_content'])
        story_data['quality_metrics'] = create_quality_metrics(
            quality_analysis['quality_score'],
            quality_analysis['is_valid_gherkin'],
            quality_analysis['syntax_issues'],
            quality_analysis['scenario_count'],
            quality_analysis['line_count'],
            quality_analysis['completeness']
        )
        
        # Store the story
        await store_story(story_data)
        
        # Schedule background tasks
        background_tasks.add_task(log_story_generation, story_data['story_id'], request.feature_description)
        
        # Create and return response
        response = create_story_response(story_data)
        logger.info(f"Successfully generated story: {response.story_id}")
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating story: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during story generation")


@router.post(
    "/refine",
    response_model=StoryResponse,
    summary="Refine User Story",
    description="Refine an existing user story based on feedback",
    response_description="Refined user story with updated metadata"
)
async def refine_story(
    request: StoryRefinementRequest,
    background_tasks: BackgroundTasks,
    generator: StoryGenerator = Depends(get_story_generator),
    ai_client: AIClient = Depends(get_ai_client)
) -> StoryResponse:
    """
    Refine an existing user story based on user feedback.
    
    This endpoint takes feedback and updates the story to incorporate
    the requested changes while maintaining proper Gherkin format.
    """
    try:
        logger.info(f"Refining story: {request.story_id}")
        
        # Retrieve original story
        original_story = await get_story(request.story_id)
        if not original_story:
            raise HTTPException(status_code=404, detail=f"Story not found: {request.story_id}")
        
        # Refine story using appropriate method
        if request.use_ai:
            # Use AI-enhanced refinement
            refined_data = await ai_client.refine_story_with_ai(
                request.story_id,
                original_story,
                request.refinement_feedback,
                request.context
            )
        else:
            # Use template-based refinement
            refined_data = generator.refine_story(
                request.story_id,
                request.refinement_feedback,
                original_story
            )
        
        # Generate updated quality metrics
        quality_analysis = await ai_client.analyze_story_quality(refined_data['gherkin_content'])
        refined_data['quality_metrics'] = create_quality_metrics(
            quality_analysis['quality_score'],
            quality_analysis['is_valid_gherkin'],
            quality_analysis['syntax_issues'],
            quality_analysis['scenario_count'],
            quality_analysis['line_count'],
            quality_analysis['completeness']
        )
        
        # Update the stored story
        await update_story(request.story_id, refined_data)
        
        # Schedule background tasks
        background_tasks.add_task(log_story_refinement, request.story_id, request.refinement_feedback)
        
        # Create and return response
        response = create_story_response(refined_data)
        logger.info(f"Successfully refined story: {response.story_id}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refining story: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during story refinement")


@router.post(
    "/validate",
    response_model=StoryValidationResponse,
    summary="Validate Gherkin Content",
    description="Validate Gherkin syntax and analyze story quality",
    response_description="Validation results and quality metrics"
)
async def validate_story(
    request: StoryValidationRequest,
    generator: StoryGenerator = Depends(get_story_generator),
    ai_client: AIClient = Depends(get_ai_client)
) -> StoryValidationResponse:
    """
    Validate Gherkin content for syntax correctness and quality.
    
    This endpoint checks the provided Gherkin content for proper syntax,
    completeness, and provides quality metrics and suggestions.
    """
    try:
        logger.info("Validating Gherkin content")
        
        # Validate syntax
        is_valid, issues = generator.validate_gherkin_syntax(request.gherkin_content)
        
        # Analyze quality
        quality_analysis = await ai_client.analyze_story_quality(request.gherkin_content)
        quality_metrics = create_quality_metrics(
            quality_analysis['quality_score'],
            quality_analysis['is_valid_gherkin'],
            quality_analysis['syntax_issues'],
            quality_analysis['scenario_count'],
            quality_analysis['line_count'],
            quality_analysis['completeness']
        )
        
        # Get suggestions (extract description from Gherkin if possible)
        feature_lines = [line for line in request.gherkin_content.split('\n') if line.strip().startswith('Feature:')]
        feature_description = feature_lines[0].replace('Feature:', '').strip() if feature_lines else request.gherkin_content[:100]
        suggestions = await ai_client.get_story_suggestions(feature_description)
        
        response = StoryValidationResponse(
            is_valid=is_valid,
            issues=issues,
            quality_metrics=quality_metrics,
            suggestions=suggestions
        )
        
        logger.info(f"Validation completed - Valid: {is_valid}, Quality: {quality_metrics.quality_score:.2f}")
        return response
        
    except Exception as e:
        logger.error(f"Error validating story: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during validation")


@router.post(
    "/suggestions",
    response_model=StorySuggestionsResponse,
    summary="Get Story Suggestions",
    description="Get suggestions for improving a feature description",
    response_description="Suggestions for improving the feature description"
)
async def get_story_suggestions(
    request: StorySuggestionsRequest,
    ai_client: AIClient = Depends(get_ai_client)
) -> StorySuggestionsResponse:
    """
    Get suggestions for improving a feature description.
    
    This endpoint analyzes a feature description and provides
    suggestions for making it more complete and actionable.
    """
    try:
        logger.info(f"Getting suggestions for: {request.feature_description[:50]}...")
        
        # Get suggestions
        suggestions = await ai_client.get_story_suggestions(request.feature_description)
        
        # Categorize suggestions (simple categorization)
        categories = {
            'clarity': [],
            'completeness': [],
            'technical': [],
            'general': []
        }
        
        for suggestion in suggestions:
            suggestion_lower = suggestion.lower()
            if any(word in suggestion_lower for word in ['specify', 'describe', 'detail']):
                categories['clarity'].append(suggestion)
            elif any(word in suggestion_lower for word in ['add', 'include', 'consider']):
                categories['completeness'].append(suggestion)
            elif any(word in suggestion_lower for word in ['security', 'format', 'integration']):
                categories['technical'].append(suggestion)
            else:
                categories['general'].append(suggestion)
        
        response = StorySuggestionsResponse(
            suggestions=suggestions,
            analyzed_description=request.feature_description,
            suggestion_categories=categories
        )
        
        logger.info(f"Generated {len(suggestions)} suggestions")
        return response
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error getting suggestions")


@router.get(
    "/{story_id}",
    response_model=StoryResponse,
    summary="Get Story by ID",
    description="Retrieve a specific story by its ID",
    response_description="Story details"
)
async def get_story_by_id(
    story_id: str
) -> StoryResponse:
    """
    Retrieve a specific story by its ID.
    
    Returns the complete story data including metadata,
    quality metrics, and generation history.
    """
    try:
        logger.info(f"Retrieving story: {story_id}")
        
        story_data = await get_story(story_id)
        if not story_data:
            raise HTTPException(status_code=404, detail=f"Story not found: {story_id}")
        
        response = create_story_response(story_data)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving story {story_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving story")


@router.get(
    "",
    response_model=StoryListResponse,
    summary="List Stories",
    description="List stories with optional filtering and pagination",
    response_description="Paginated list of stories"
)
async def list_stories(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of stories per page"),
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    story_type: Optional[str] = Query(None, description="Filter by story type"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    status: Optional[str] = Query(None, description="Filter by status")
) -> StoryListResponse:
    """
    List stories with optional filtering and pagination.
    
    Supports filtering by project, type, priority, and status.
    Results are paginated for better performance.
    """
    try:
        logger.info(f"Listing stories - Page: {page}, Size: {page_size}")
        
        # Get all stories
        all_stories = list(story_storage.values())
        
        # Apply filters
        filtered_stories = all_stories
        
        if project_id:
            filtered_stories = [s for s in filtered_stories if s.get('project_id') == project_id]
        
        if story_type:
            filtered_stories = [s for s in filtered_stories if s.get('story_type') == story_type]
        
        if priority:
            filtered_stories = [s for s in filtered_stories if s.get('priority') == priority]
        
        if status:
            filtered_stories = [s for s in filtered_stories if s.get('status') == status]
        
        # Sort by generated_at (newest first)
        filtered_stories.sort(key=lambda x: x.get('generated_at', ''), reverse=True)
        
        # Apply pagination
        total_count = len(filtered_stories)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_stories = filtered_stories[start_idx:end_idx]
        
        # Convert to response models
        story_responses = [create_story_response(story) for story in paginated_stories]
        
        response = StoryListResponse(
            stories=story_responses,
            total_count=total_count,
            page=page,
            page_size=page_size,
            has_next=end_idx < total_count,
            has_previous=page > 1
        )
        
        logger.info(f"Returned {len(story_responses)} stories (total: {total_count})")
        return response
        
    except Exception as e:
        logger.error(f"Error listing stories: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error listing stories")


@router.delete(
    "/{story_id}",
    summary="Delete Story",
    description="Delete a story by its ID",
    response_description="Confirmation of deletion"
)
async def delete_story(
    story_id: str,
    background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Delete a story by its ID.
    
    Removes the story from storage and logs the deletion.
    """
    try:
        logger.info(f"Deleting story: {story_id}")
        
        if story_id not in story_storage:
            raise HTTPException(status_code=404, detail=f"Story not found: {story_id}")
        
        # Delete the story
        del story_storage[story_id]
        
        # Schedule background logging
        background_tasks.add_task(log_story_deletion, story_id)
        
        logger.info(f"Successfully deleted story: {story_id}")
        return JSONResponse(
            status_code=200,
            content={
                "message": f"Story {story_id} deleted successfully",
                "deleted_at": datetime.utcnow().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting story {story_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error deleting story")


@router.get(
    "/system/health",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Check the health status of the story generation system",
    response_description="System health status"
)
async def health_check(
    ai_client: AIClient = Depends(get_ai_client)
) -> HealthCheckResponse:
    """
    Check the health status of the story generation system.
    
    Returns the status of all components including AI providers.
    """
    try:
        # Check AI provider status
        ai_status = ai_client.get_provider_status()
        
        # Check basic services
        services = {
            "story_generator": "healthy",
            "ai_client": "healthy",
            "storage": "healthy" if story_storage is not None else "unhealthy"
        }
        
        response = HealthCheckResponse(
            status="healthy",
            services=services,
            ai_provider_status=AIProviderStatus(**ai_status)
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthCheckResponse(
            status="unhealthy",
            services={"error": str(e)}
        )


# Background task functions
async def log_story_generation(story_id: str, feature_description: str):
    """Background task to log story generation"""
    logger.info(f"Story generated - ID: {story_id}, Description: {feature_description[:50]}...")


async def log_story_refinement(story_id: str, feedback: str):
    """Background task to log story refinement"""
    logger.info(f"Story refined - ID: {story_id}, Feedback: {feedback[:50]}...")


async def log_story_deletion(story_id: str):
    """Background task to log story deletion"""
    logger.info(f"Story deleted - ID: {story_id}")


# Error handlers
@router.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions"""
    return JSONResponse(
        status_code=400,
        content=create_error_response("validation_error", str(exc)).model_dump()
    )


@router.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 Not Found exceptions"""
    return JSONResponse(
        status_code=404,
        content=create_error_response("not_found", "Resource not found").model_dump()
    )


# Router setup complete
logger.info("Story router initialized successfully")


# Example usage for testing
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    
    app = FastAPI(title="Story Generation API")
    app.include_router(router)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)