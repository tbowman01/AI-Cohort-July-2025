"""
AutoDevHub Backend - Stories Router

This router handles all story-related API endpoints including story generation,
retrieval, and management functionality.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import uuid

from dependencies import (
    get_database_session,
    get_current_user,
    get_ai_service,
    AIServiceManager,
    check_rate_limit
)

logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter()


# Pydantic models for request/response validation
from pydantic import BaseModel, Field, validator


class StoryGenerationRequest(BaseModel):
    """Request model for story generation."""
    
    description: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Feature description for story generation"
    )
    project_context: Optional[str] = Field(
        None,
        max_length=500,
        description="Additional project context for better story generation"
    )
    story_type: str = Field(
        default="user_story",
        description="Type of story to generate"
    )
    complexity: str = Field(
        default="medium",
        description="Complexity level of the feature"
    )
    
    @validator('story_type')
    def validate_story_type(cls, v):
        """Validate story type options."""
        allowed_types = ["user_story", "epic", "bug_fix", "technical_task"]
        if v not in allowed_types:
            raise ValueError(f"story_type must be one of: {allowed_types}")
        return v
    
    @validator('complexity')
    def validate_complexity(cls, v):
        """Validate complexity level options."""
        allowed_complexity = ["low", "medium", "high", "epic"]
        if v not in allowed_complexity:
            raise ValueError(f"complexity must be one of: {allowed_complexity}")
        return v


class StoryResponse(BaseModel):
    """Response model for story data."""
    
    id: str = Field(..., description="Unique story identifier")
    title: str = Field(..., description="Story title")
    description: str = Field(..., description="Original feature description")
    gherkin: str = Field(..., description="Generated Gherkin scenarios")
    acceptance_criteria: List[str] = Field(..., description="Acceptance criteria list")
    story_type: str = Field(..., description="Type of story")
    complexity: str = Field(..., description="Complexity level")
    status: str = Field(default="draft", description="Story status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    project_context: Optional[str] = Field(None, description="Project context")
    estimated_points: Optional[int] = Field(None, description="Story points estimation")
    tags: List[str] = Field(default_factory=list, description="Story tags")


class StoryListResponse(BaseModel):
    """Response model for story list with pagination."""
    
    stories: List[StoryResponse] = Field(..., description="List of stories")
    total: int = Field(..., description="Total number of stories")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    has_next: bool = Field(..., description="Whether there are more pages")


class StoryUpdateRequest(BaseModel):
    """Request model for story updates."""
    
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    gherkin: Optional[str] = Field(None, max_length=5000)
    acceptance_criteria: Optional[List[str]] = Field(None, max_items=20)
    status: Optional[str] = Field(None)
    estimated_points: Optional[int] = Field(None, ge=1, le=21)
    tags: Optional[List[str]] = Field(None, max_items=10)
    
    @validator('status')
    def validate_status(cls, v):
        """Validate story status options."""
        if v is not None:
            allowed_statuses = ["draft", "ready", "in_progress", "review", "done", "archived"]
            if v not in allowed_statuses:
                raise ValueError(f"status must be one of: {allowed_statuses}")
        return v


# In-memory storage for stories (will be replaced with database models)
# This is a temporary solution until Database-Designer completes the models
STORIES_STORAGE: Dict[str, Dict[str, Any]] = {}


@router.post(
    "/generate-story",
    response_model=StoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Gherkin Story",
    description="Generate a Gherkin story from a feature description using AI"
)
async def generate_story(
    request: StoryGenerationRequest,
    ai_service: AIServiceManager = Depends(get_ai_service),
    current_user: Optional[dict] = Depends(get_current_user),
    rate_limit_check: bool = Depends(check_rate_limit),
    db: Session = Depends(get_database_session)
) -> StoryResponse:
    """
    Generate a new Gherkin story from feature description.
    
    Args:
        request: Story generation request with description and options
        ai_service: AI service manager for story generation
        current_user: Current authenticated user (optional)
        rate_limit_check: Rate limiting validation
        db: Database session
        
    Returns:
        StoryResponse: Generated story with Gherkin scenarios
        
    Raises:
        HTTPException: If story generation fails
    """
    try:
        logger.info(f"Generating story for description: {request.description[:100]}")
        
        # Generate story using AI service
        generated_story = await ai_service.generate_story(request.description)
        
        # Create story record
        story_id = str(uuid.uuid4())
        current_time = datetime.utcnow()
        
        story_data = {
            "id": story_id,
            "title": generated_story["title"],
            "description": request.description,
            "gherkin": generated_story["gherkin"],
            "acceptance_criteria": generated_story["acceptance_criteria"],
            "story_type": request.story_type,
            "complexity": request.complexity,
            "status": "draft",
            "created_at": current_time,
            "updated_at": current_time,
            "project_context": request.project_context,
            "estimated_points": _estimate_story_points(request.complexity),
            "tags": _generate_tags(request.description, request.story_type),
            "user_id": current_user.get("id") if current_user else None
        }
        
        # Store in temporary storage (will be replaced with database)
        STORIES_STORAGE[story_id] = story_data
        
        logger.info(f"Story generated successfully with ID: {story_id}")
        
        return StoryResponse(**story_data)
        
    except Exception as e:
        logger.error(f"Story generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate story: {str(e)}"
        )


@router.get(
    "/stories",
    response_model=StoryListResponse,
    summary="List Stories",
    description="Retrieve a paginated list of all generated stories"
)
async def list_stories(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by story status"),
    story_type: Optional[str] = Query(None, description="Filter by story type"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    current_user: Optional[dict] = Depends(get_current_user),
    db: Session = Depends(get_database_session)
) -> StoryListResponse:
    """
    Retrieve a paginated list of stories with optional filtering.
    
    Args:
        page: Page number (1-based)
        page_size: Number of items per page
        status: Filter by story status
        story_type: Filter by story type
        search: Search term for title and description
        current_user: Current authenticated user (optional)
        db: Database session
        
    Returns:
        StoryListResponse: Paginated list of stories
    """
    try:
        logger.info(f"Listing stories - page: {page}, size: {page_size}")
        
        # Filter stories based on parameters
        filtered_stories = []
        for story in STORIES_STORAGE.values():
            # Apply filters
            if status and story["status"] != status:
                continue
            if story_type and story["story_type"] != story_type:
                continue
            if search:
                search_lower = search.lower()
                if (search_lower not in story["title"].lower() and 
                    search_lower not in story["description"].lower()):
                    continue
            
            filtered_stories.append(story)
        
        # Sort by creation date (newest first)
        filtered_stories.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Calculate pagination
        total = len(filtered_stories)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        paginated_stories = filtered_stories[start_index:end_index]
        has_next = end_index < total
        
        # Convert to response models
        story_responses = [StoryResponse(**story) for story in paginated_stories]
        
        return StoryListResponse(
            stories=story_responses,
            total=total,
            page=page,
            page_size=page_size,
            has_next=has_next
        )
        
    except Exception as e:
        logger.error(f"Failed to list stories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve stories: {str(e)}"
        )


@router.get(
    "/stories/{story_id}",
    response_model=StoryResponse,
    summary="Get Story",
    description="Retrieve a specific story by its ID"
)
async def get_story(
    story_id: str,
    current_user: Optional[dict] = Depends(get_current_user),
    db: Session = Depends(get_database_session)
) -> StoryResponse:
    """
    Retrieve a specific story by ID.
    
    Args:
        story_id: Unique story identifier
        current_user: Current authenticated user (optional)
        db: Database session
        
    Returns:
        StoryResponse: Story details
        
    Raises:
        HTTPException: If story is not found
    """
    try:
        logger.info(f"Retrieving story with ID: {story_id}")
        
        if story_id not in STORIES_STORAGE:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Story with ID {story_id} not found"
            )
        
        story_data = STORIES_STORAGE[story_id]
        return StoryResponse(**story_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve story {story_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve story: {str(e)}"
        )


@router.put(
    "/stories/{story_id}",
    response_model=StoryResponse,
    summary="Update Story",
    description="Update an existing story with new information"
)
async def update_story(
    story_id: str,
    request: StoryUpdateRequest,
    current_user: Optional[dict] = Depends(get_current_user),
    db: Session = Depends(get_database_session)
) -> StoryResponse:
    """
    Update an existing story.
    
    Args:
        story_id: Unique story identifier
        request: Story update request with new values
        current_user: Current authenticated user (optional)
        db: Database session
        
    Returns:
        StoryResponse: Updated story details
        
    Raises:
        HTTPException: If story is not found or update fails
    """
    try:
        logger.info(f"Updating story with ID: {story_id}")
        
        if story_id not in STORIES_STORAGE:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Story with ID {story_id} not found"
            )
        
        story_data = STORIES_STORAGE[story_id].copy()
        
        # Update fields that are provided
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            story_data[field] = value
        
        # Update timestamp
        story_data["updated_at"] = datetime.utcnow()
        
        # Save updated story
        STORIES_STORAGE[story_id] = story_data
        
        logger.info(f"Story {story_id} updated successfully")
        return StoryResponse(**story_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update story {story_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update story: {str(e)}"
        )


@router.delete(
    "/stories/{story_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Story",
    description="Delete a story by its ID"
)
async def delete_story(
    story_id: str,
    current_user: Optional[dict] = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Delete a story by ID.
    
    Args:
        story_id: Unique story identifier
        current_user: Current authenticated user (optional)
        db: Database session
        
    Raises:
        HTTPException: If story is not found
    """
    try:
        logger.info(f"Deleting story with ID: {story_id}")
        
        if story_id not in STORIES_STORAGE:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Story with ID {story_id} not found"
            )
        
        del STORIES_STORAGE[story_id]
        logger.info(f"Story {story_id} deleted successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete story {story_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete story: {str(e)}"
        )


# Helper functions
def _estimate_story_points(complexity: str) -> int:
    """
    Estimate story points based on complexity.
    
    Args:
        complexity: Complexity level
        
    Returns:
        int: Estimated story points
    """
    complexity_mapping = {
        "low": 2,
        "medium": 5,
        "high": 8,
        "epic": 13
    }
    return complexity_mapping.get(complexity, 5)


def _generate_tags(description: str, story_type: str) -> List[str]:
    """
    Generate relevant tags based on description and story type.
    
    Args:
        description: Feature description
        story_type: Type of story
        
    Returns:
        List[str]: Generated tags
    """
    tags = [story_type]
    
    # Add technology-based tags
    description_lower = description.lower()
    tech_keywords = {
        "api": "api",
        "database": "database",
        "frontend": "frontend",
        "backend": "backend",
        "auth": "authentication",
        "security": "security",
        "performance": "performance",
        "ui": "ui-ux",
        "test": "testing"
    }
    
    for keyword, tag in tech_keywords.items():
        if keyword in description_lower:
            tags.append(tag)
    
    return list(set(tags))  # Remove duplicates