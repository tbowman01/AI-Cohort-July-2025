# AutoDevHub Story Generation Services

This directory contains the core services for converting natural language feature descriptions into structured Gherkin user stories.

## 🎯 Overview

The story generation system provides reliable, template-based user story generation with optional AI enhancement. It's designed for consistent demo functionality while supporting future AI integration.

## 📁 Service Files

### `story_generator.py`
**Core story generation service with template-based approach**

- **Purpose**: Converts natural language descriptions to Gherkin format
- **Features**:
  - Template-based generation for reliable output
  - Feature type detection (authentication, CRUD, API, search, etc.)
  - Story component extraction (role, action, benefit)
  - Gherkin syntax validation
  - Story refinement capabilities
  - Effort estimation (story points 1-13)

**Key Classes**:
- `StoryGenerator`: Main service class
- `StoryTemplate`: Template patterns and configurations
- `StoryType`, `Priority`: Enums for story classification

**Example Usage**:
```python
from services.story_generator import StoryGenerator

generator = StoryGenerator()
result = generator.generate_gherkin_story(
    "User authentication with social login",
    StoryType.FEATURE,
    Priority.HIGH
)
print(result['gherkin_content'])
```

### `ai_client.py`
**AI integration service with template fallback**

- **Purpose**: Provides AI-enhanced story generation with reliable fallback
- **Features**:
  - Multi-provider AI support (Claude, OpenAI)
  - Automatic fallback to template-based generation
  - Story quality analysis
  - Refinement capabilities
  - Suggestion generation

**Key Classes**:
- `AIClient`: Main AI integration service
- `AIClientConfig`: Configuration management
- `AIProvider`: Enum for provider selection

**Example Usage**:
```python
from services.ai_client import create_ai_client

client = create_ai_client()
result = await client.generate_story_with_ai("File upload functionality")
quality = await client.analyze_story_quality(result['gherkin_content'])
```

## 🔧 Features

### Template-Based Generation

**Reliable Core Functionality**:
- ✅ Works without external dependencies
- ✅ Consistent output format
- ✅ Handles 6+ feature types
- ✅ Proper Gherkin syntax
- ✅ Story point estimation

**Supported Feature Types**:
1. **Authentication** - Login, registration, security
2. **CRUD Operations** - Create, read, update, delete
3. **API Integration** - REST endpoints, services
4. **Search Functionality** - Search, filter, query
5. **File Management** - Upload, download, documents
6. **Notifications** - Alerts, messages, emails

### Story Components

**Extracted Elements**:
- **User Role**: Who will use the feature
- **Action**: What they want to do
- **Benefit**: Why they need it
- **Feature Name**: Generated title
- **Scenarios**: Given-When-Then test cases
- **Acceptance Criteria**: Testable requirements

### Quality Assurance

**Built-in Validation**:
- Gherkin syntax checking
- Completeness analysis
- Quality scoring (0-1 scale)
- Suggestion generation
- Error detection

## 📊 Story Generation Process

```
Input: "User authentication with social login"
    ↓
1. Normalize description
    ↓
2. Detect feature type → "authentication"
    ↓
3. Extract components:
   - Role: "user"
   - Action: "authenticate with social login"
   - Benefit: "securely access my account"
    ↓
4. Apply template:
   - Feature name
   - User story format
   - Scenarios (success, error cases)
    ↓
5. Generate Gherkin:
   ```gherkin
   Feature: User Authentication
     As a user
     I want to authenticate with social login
     So that I can securely access my account

     Scenario: Successful authentication
       Given I am on the login page
       When I enter valid credentials
       Then I should be logged in successfully
   ```
    ↓
6. Add metadata:
   - Story ID
   - Effort estimation
   - Quality metrics
   - Timestamps
```

## 🧪 Testing

### Test Coverage

**Core Functionality**:
- ✅ Story generation for all feature types
- ✅ Gherkin syntax validation
- ✅ Quality analysis
- ✅ Refinement capabilities
- ✅ Error handling

**Test Command**:
```bash
cd backend
python test_story_generation.py
```

**Expected Output**:
- Story Generator: 5/5 tests passed
- AI Client: Working with template fallback
- Schema Validation: All schemas valid
- Integration: End-to-end workflow functional

## 🎮 Demo Examples

### Example 1: Authentication Feature
**Input**: "User authentication with social login"

**Output**:
```gherkin
Feature: User Authentication
  As a user
  I want to authenticate with social login
  So that I can securely access my account

  Scenario: Successful authentication
    Given I am on the login page
    When I select social login with Google
    Then I should be logged in successfully

  Scenario: Invalid credentials
    Given I am on the login page
    When I enter invalid credentials
    Then I should see an error message
```

### Example 2: File Upload Feature
**Input**: "File upload functionality for documents"

**Output**:
```gherkin
Feature: File Management
  As a user
  I want to upload documents
  So that I can share and store my files

  Scenario: Upload file successfully
    Given I am on the file upload page
    When I select and upload a valid file
    Then the file should be uploaded successfully

  Scenario: Invalid file type
    Given I am on the file upload page
    When I try to upload an invalid file type
    Then I should see an error message
```

## 🔮 Future Enhancements

### AI Integration (Phase 2)
- **Claude API**: Enhanced story generation
- **OpenAI GPT**: Alternative AI provider
- **Custom Models**: Domain-specific training
- **Context Awareness**: Project-specific generation

### Advanced Features
- **Story Templates**: Custom organization templates
- **Integration Export**: Jira, Azure DevOps, GitHub Issues
- **Collaborative Editing**: Multi-user story refinement
- **Analytics**: Story quality trends and insights

## 🚀 Integration Points

### FastAPI Router
- **Endpoint**: `/api/v1/stories/generate`
- **Router**: `routers/story_router.py`
- **Dependencies**: Automatic injection of services

### Database Integration
- **Current**: In-memory storage for demo
- **Future**: SQLAlchemy models for persistence
- **Schema**: Defined in `schemas/story_schemas.py`

### Authentication
- **Ready**: JWT token support structure
- **Integration**: User context for personalized stories
- **Permissions**: Role-based story access

## 🛠️ Configuration

### Environment Variables
```bash
# Optional AI API keys (falls back to template if not provided)
CLAUDE_API_KEY=your_claude_key_here
OPENAI_API_KEY=your_openai_key_here

# Service configuration
STORY_GENERATION_TIMEOUT=30
MAX_STORY_LENGTH=2000
DEFAULT_STORY_TYPE=story
DEFAULT_PRIORITY=medium
```

### Service Configuration
```python
# AI Client configuration
config = AIClientConfig()
config.max_retries = 3
config.timeout_seconds = 30
config.fallback_to_template = True
```

## 📝 API Integration

### Story Generation Request
```json
{
  "feature_description": "User authentication with social login",
  "story_type": "feature",
  "priority": "high",
  "use_ai": true,
  "project_id": "proj_123"
}
```

### Story Response
```json
{
  "story_id": "STORY_20250731_173000",
  "gherkin_content": "Feature: User Authentication...",
  "acceptance_criteria": ["User can login with Google"],
  "estimated_effort": 8,
  "quality_metrics": {
    "quality_score": 0.95,
    "is_valid_gherkin": true
  }
}
```

## 🎯 Success Metrics

### Quality Standards
- **Gherkin Validity**: 100% syntactically correct
- **Completeness**: All stories have Feature, Scenario, Given-When-Then
- **Effort Accuracy**: Story points align with complexity
- **Generation Speed**: <2 seconds for template-based stories

### Demo Readiness
- ✅ No external dependencies required
- ✅ Consistent output format
- ✅ Error handling for edge cases
- ✅ Multiple feature type support
- ✅ Quality metrics for all stories

---

**Status**: ✅ **IMPLEMENTATION COMPLETE**  
**Generated by**: Story-Generator Agent  
**Last Updated**: July 31, 2025  
**Ready for**: Database-Designer and FastAPI-Developer integration