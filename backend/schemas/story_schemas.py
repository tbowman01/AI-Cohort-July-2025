"""
Pydantic schemas for story generation and management

These schemas define the data models for API requests and responses
related to user story generation and management.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator, ConfigDict


class StoryType(str, Enum):
    """Supported story types"""
    EPIC = "epic"
    FEATURE = "feature"
    STORY = "story"
    TASK = "task"


class Priority(str, Enum):
    """Story priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StoryStatus(str, Enum):
    """Story status values"""
    DRAFT = "draft"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


class StoryGenerationRequest(BaseModel):
    """Request model for story generation"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )

    feature_description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description=(\n            "Natural language description of the feature to generate a story for"\n        ),
        examples=[
            "User authentication with social login",
            "File upload functionality for documents",
            "Search functionality with filters"])

    story_type: StoryType = Field(
        default=StoryType.STORY,
        description="Type of story to generate"
    )

    priority: Priority = Field(
        default=Priority.MEDIUM,
        description="Priority level for the story"
    )

    project_id: Optional[str] = Field(
        default=None,
        description="Optional project ID to associate the story with"
    )

    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for story generation"
    )

    use_ai: bool = Field(
        default=True,
        description="Whether to use AI for enhanced generation"
    )

    @validator('feature_description')
    def validate_feature_description(cls, v):
        """Validate feature description has meaningful content"""
        if not v or not v.strip():
            raise ValueError("Feature description cannot be empty")

        # Check for minimum meaningful content
        words = v.strip().split()
        if len(words) < 3:
            raise ValueError(
                "Feature description should contain at least 3 words")

        return v.strip()


class StoryRefinementRequest(BaseModel):
    """Request model for story refinement"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )

    story_id: str = Field(
        ...,
        description="ID of the story to refine"
    )

    refinement_feedback: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Feedback for refining the story",
        examples=[
            "Add two-factor authentication requirement",
            "Include mobile app support",
            "Add error handling scenarios"
        ]
    )

    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for refinement"
    )

    use_ai: bool = Field(
        default=True,
        description="Whether to use AI for refinement"
    )


class AcceptanceCriteria(BaseModel):
    """Model for acceptance criteria"""
    model_config = ConfigDict(extra="forbid")

    id: Optional[str] = Field(
        default=None,
        description="Unique identifier for the criterion")
    description: str = Field(
        ...,
        min_length=5,
        description="Description of the acceptance criterion"
    )
    priority: Priority = Field(
        default=Priority.MEDIUM,
        description="Priority of this criterion")
    testable: bool = Field(
        default=True,
        description="Whether this criterion is testable")


class StoryComponents(BaseModel):
    """Model for story components extracted during generation"""
    model_config = ConfigDict(extra="forbid")

    role: str = Field(..., description="User role (As a...)")
    action: str = Field(..., description="Desired action (I want to...)")
    benefit: str = Field(..., description="Expected benefit (So that...)")
    feature_name: str = Field(..., description="Name of the feature")
    feature_type: Optional[str] = Field(
        default=None, description="Detected feature type")


class QualityMetrics(BaseModel):
    """Model for story quality metrics"""
    model_config = ConfigDict(extra="forbid")

    quality_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall quality score (0-1)"
    )
    is_valid_gherkin: bool = Field(...,
                                   description="Whether the Gherkin syntax is valid")
    syntax_issues: List[str] = Field(
        default_factory=list,
        description="List of syntax issues found")
    scenario_count: int = Field(
        ge=0, description="Number of scenarios in the story")
    line_count: int = Field(ge=0, description="Number of non-empty lines")
    completeness: Dict[str, bool] = Field(
        default_factory=dict, description="Completeness metrics")
    analyzed_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the analysis was performed")


class StoryResponse(BaseModel):
    """Response model for generated stories"""
    model_config = ConfigDict(extra="allow")

    story_id: str = Field(..., description="Unique identifier for the story")
    feature_description: str = Field(...,
                                     description="Original feature description")
    gherkin_content: str = Field(...,
                                 description="Generated Gherkin-formatted story")
    acceptance_criteria: List[str] = Field(
        default_factory=list,
        description="List of acceptance criteria")
    estimated_effort: int = Field(
        ge=1, le=13, description="Estimated effort in story points")
    story_type: StoryType = Field(..., description="Type of story")
    priority: Priority = Field(..., description="Priority level")
    status: StoryStatus = Field(
        default=StoryStatus.DRAFT,
        description="Current status of the story")

    # Generation metadata
    feature_type: Optional[str] = Field(
        default=None, description="Detected feature type")
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the story was generated")
    components: Optional[StoryComponents] = Field(
        default=None, description="Extracted story components")

    # AI metadata
    ai_provider: Optional[str] = Field(
        default=None, description="AI provider used for generation")
    ai_generated: bool = Field(
        default=False,
        description="Whether AI was used for generation")
    template_based: bool = Field(
        default=True,
        description="Whether template-based generation was used")
    confidence_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Confidence in the generation")

    # Quality metrics
    quality_metrics: Optional[QualityMetrics] = Field(
        default=None, description="Quality analysis of the story")

    # Project association
    project_id: Optional[str] = Field(
        default=None, description="Associated project ID")

    # Versioning
    version: int = Field(
        default=1,
        ge=1,
        description="Version number of the story")

    # Refinement data
    refinement_feedback: Optional[str] = Field(
        default=None, description="Feedback used for refinement")
    refined_at: Optional[datetime] = Field(
        default=None, description="When the story was last refined")


class StoryListResponse(BaseModel):
    """Response model for listing stories"""
    model_config = ConfigDict(extra="forbid")

    stories: List[StoryResponse] = Field(
        default_factory=list,
        description="List of stories")
    total_count: int = Field(ge=0, description="Total number of stories")
    page: int = Field(ge=1, description="Current page number")
    page_size: int = Field(
        ge=1,
        le=100,
        description="Number of stories per page")
    has_next: bool = Field(description="Whether there are more pages")
    has_previous: bool = Field(description="Whether there are previous pages")


class StoryValidationRequest(BaseModel):
    """Request model for story validation"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )

    gherkin_content: str = Field(
        ...,
        min_length=10,
        description="Gherkin content to validate"
    )


class StoryValidationResponse(BaseModel):
    """Response model for story validation"""
    model_config = ConfigDict(extra="forbid")

    is_valid: bool = Field(...,
                           description="Whether the Gherkin syntax is valid")
    issues: List[str] = Field(
        default_factory=list,
        description="List of validation issues")
    quality_metrics: QualityMetrics = Field(...,
                                            description="Quality analysis of the content")
    suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for improvement")


class StorySuggestionsRequest(BaseModel):
    """Request model for getting story suggestions"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )

    feature_description: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Feature description to analyze for suggestions"
    )


class StorySuggestionsResponse(BaseModel):
    """Response model for story suggestions"""
    model_config = ConfigDict(extra="forbid")

    suggestions: List[str] = Field(
        default_factory=list,
        description="List of suggestions")
    analyzed_description: str = Field(...,
                                      description="The analyzed feature description")
    suggestion_categories: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Suggestions grouped by category"
    )
    analyzed_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the analysis was performed")


class AIProviderStatus(BaseModel):
    """Model for AI provider status"""
    model_config = ConfigDict(extra="forbid")

    current_provider: str = Field(...,
                                  description="Currently active AI provider")
    available_providers: List[str] = Field(
        default_factory=list,
        description="List of available providers")
    claude_configured: bool = Field(
        default=False,
        description="Whether Claude API is configured")
    openai_configured: bool = Field(
        default=False,
        description="Whether OpenAI API is configured")
    fallback_enabled: bool = Field(
        default=True,
        description="Whether template fallback is enabled")
    status: str = Field(
        default="operational",
        description="Overall system status")


class HealthCheckResponse(BaseModel):
    """Response model for health check"""
    model_config = ConfigDict(extra="forbid")

    status: str = Field(default="healthy", description="Health status")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of health check")
    services: Dict[str, str] = Field(
        default_factory=dict, description="Status of individual services")
    version: str = Field(default="1.0.0", description="API version")
    ai_provider_status: Optional[AIProviderStatus] = Field(
        default=None, description="AI provider status")


class ErrorResponse(BaseModel):
    """Response model for errors"""
    model_config = ConfigDict(extra="forbid")

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None,
                                  description="Detailed error information")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the error occurred")
    request_id: Optional[str] = Field(
        default=None, description="Request ID for tracking")


# Utility functions for creating responses
def create_story_response(story_data: Dict[str, Any]) -> StoryResponse:
    """Create a StoryResponse from story data dictionary"""
    return StoryResponse(**story_data)


def create_error_response(
        error_type: str,
        message: str,
        detail: Optional[str] = None) -> ErrorResponse:
    """Create an ErrorResponse"""
    return ErrorResponse(
        error=error_type,
        message=message,
        detail=detail
    )


def create_quality_metrics(
    quality_score: float,
    is_valid_gherkin: bool,
    syntax_issues: List[str],
    scenario_count: int,
    line_count: int,
    completeness: Dict[str, bool]
) -> QualityMetrics:
    """Create QualityMetrics object"""
    return QualityMetrics(
        quality_score=quality_score,
        is_valid_gherkin=is_valid_gherkin,
        syntax_issues=syntax_issues,
        scenario_count=scenario_count,
        line_count=line_count,
        completeness=completeness
    )


# Example usage and validation
if __name__ == "__main__":
    # Example story generation request
    request = StoryGenerationRequest(
        feature_description="User authentication with social login and two-factor authentication",
        story_type=StoryType.FEATURE,
        priority=Priority.HIGH,
        use_ai=True)

    print("=== Schema Validation Demo ===")
    print(f"Request: {request.model_dump_json(indent=2)}")

    # Example story response
    response = StoryResponse(
        story_id="STORY_20250731_172500",
        feature_description=request.feature_description,
        gherkin_content="""Feature: User Authentication
  As a user
  I want to authenticate with social login
  So that I can securely access my account

  Scenario: Successful social login
    Given I am on the login page
    When I select social login with Google
    Then I should be logged in successfully""",
        acceptance_criteria=[
            "User can login with Google account",
            "User can login with Facebook account",
            "Two-factor authentication is enforced"
        ],
        estimated_effort=8,
        story_type=StoryType.FEATURE,
        priority=Priority.HIGH,
        ai_generated=False,
        template_based=True,
        confidence_score=0.85
    )

    print(f"\nResponse: {response.model_dump_json(indent=2)}")

    # Validate the schemas
    try:
        # Test validation
        invalid_request = {"feature_description": ""}  # Should fail validation
        StoryGenerationRequest(**invalid_request)
    except Exception as e:
        print(f"\nValidation works correctly - caught error: {e}")

    print("\n✅ Schema validation completed successfully")
