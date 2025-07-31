# AutoDevHub Backend Test Suite

This directory contains comprehensive tests for the AutoDevHub backend implementation. The test suite provides >80% code coverage and includes unit tests, integration tests, and performance tests.

## Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── test_main.py             # FastAPI application tests
├── test_models.py           # Database model tests  
├── test_story_generator.py  # AI story generation tests
├── test_endpoints.py        # API endpoint integration tests
├── test_runner.py           # Test execution utilities
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Individual function and class testing
- Isolated component validation
- Mock-based testing for external dependencies

### Integration Tests (`@pytest.mark.integration`)
- API endpoint testing with FastAPI TestClient
- Database integration testing
- Service interaction testing

### Performance Tests (`@pytest.mark.performance`)
- Response time validation
- Concurrent request handling
- Memory usage optimization
- Scalability testing

### Database Tests (`@pytest.mark.database`)
- SQLAlchemy model testing
- Database operation validation
- Migration and schema testing

### AI Service Tests (`@pytest.mark.ai_service`)
- Story generation functionality
- AI service integration
- Mock AI service testing

## Running Tests

### Prerequisites

Ensure you have all dependencies installed:

```bash
cd /workspaces/AI-Cohort-July-2025/backend
pip install -r requirements.txt
```

### Quick Start

Run all tests with coverage:
```bash
python tests/test_runner.py --coverage
```

### Specific Test Categories

Run only unit tests:
```bash
python tests/test_runner.py --unit
```

Run only integration tests:
```bash
python tests/test_runner.py --integration
```

Run only performance tests:
```bash
python tests/test_runner.py --performance
```

Run only database tests:
```bash
python tests/test_runner.py --database
```

Run only AI service tests:
```bash
python tests/test_runner.py --ai-service
```

### Specific Test Files

Run tests from a specific file:
```bash
python tests/test_runner.py --file test_main.py
python tests/test_runner.py --file test_models.py
python tests/test_runner.py --file test_endpoints.py
```

### Direct Pytest Commands

You can also run pytest directly:

```bash
# All tests with coverage
pytest tests/ --cov=. --cov-report=html --cov-report=term -v

# Specific test file
pytest tests/test_main.py -v

# Tests with specific marker
pytest tests/ -m "unit" -v
pytest tests/ -m "integration" -v
pytest tests/ -m "performance" -v

# Specific test function
pytest tests/test_main.py::TestApplication::test_app_creation -v
```

## Test Configuration

### Environment Variables

Tests use the following environment variables:

- `DATABASE_URL`: Test database URL (defaults to SQLite)
- `DEBUG`: Enable debug mode for tests
- `ENVIRONMENT`: Set to "testing" for test runs

### Test Database

Tests use an in-memory SQLite database by default for isolation and speed. Each test gets a fresh database instance.

### Mock Services

External dependencies are mocked during testing:

- **AI Service**: Mock implementation provides consistent test data
- **Database**: In-memory SQLite for fast, isolated tests
- **Authentication**: Mock user authentication for testing

## Coverage Requirements

The test suite maintains >80% code coverage across all modules:

- **Unit Tests**: >90% coverage for individual functions
- **Integration Tests**: >85% coverage for API endpoints  
- **Database Tests**: >90% coverage for model operations
- **Overall Coverage**: >80% across entire codebase

## Test Reports

Generate comprehensive test reports:

```bash
python tests/test_runner.py --report
```

This generates:
- HTML coverage report: `htmlcov/index.html`
- HTML test report: `test-report.html`
- JUnit XML report: `test-results.xml`

## Test Data and Fixtures

### Database Fixtures
- `db_session`: Provides isolated database session
- `async_db_session`: Provides async database session
- `sample_user_story`: Creates test UserStory instance
- `sample_session`: Creates test Session instance
- `large_dataset_stories`: Creates 100 test stories for performance testing

### Service Fixtures
- `mock_ai_service`: Mock AI service for story generation
- `test_client`: FastAPI test client with mocked dependencies
- `auth_headers`: Authentication headers for testing

### Utility Fixtures
- `sample_story_data`: Standard story data for tests
- `mock_stories_storage`: In-memory story storage for testing
- `simulate_db_error`: Database error simulation
- `simulate_ai_service_error`: AI service error simulation

## Writing New Tests

### Test File Naming
- Use `test_*.py` naming convention
- Group related tests in classes with `Test*` naming
- Use descriptive test function names starting with `test_`

### Test Structure
```python
@pytest.mark.unit  # or integration, performance, etc.
class TestNewFeature:
    """Test cases for new feature."""
    
    def test_basic_functionality(self, fixture_name):
        """Test basic functionality with clear description."""
        # Arrange
        test_data = {"key": "value"}
        
        # Act
        result = function_under_test(test_data)
        
        # Assert
        assert result.success is True
        assert result.data == expected_data
```

### Best Practices
1. **Arrange-Act-Assert**: Structure tests clearly
2. **Descriptive Names**: Test names should explain what is being tested
3. **Isolated Tests**: Each test should be independent
4. **Mock External Dependencies**: Don't rely on external services
5. **Test Edge Cases**: Include boundary conditions and error cases
6. **Performance Awareness**: Mark slow tests appropriately

## Continuous Integration

Tests are designed to run in CI/CD environments:

- **Fast Execution**: Most tests complete in <5 seconds
- **No External Dependencies**: All external services are mocked
- **Deterministic Results**: Tests produce consistent results
- **Comprehensive Coverage**: >80% code coverage requirement
- **Multiple Python Versions**: Compatible with Python 3.8+

## Troubleshooting

### Common Issues

**Import Errors**: Ensure you're running tests from the backend directory
```bash
cd /workspaces/AI-Cohort-July-2025/backend
python -m pytest tests/
```

**Database Errors**: Tests use in-memory SQLite, no external database needed

**Coverage Issues**: Exclude test files and virtual environments in pytest.ini

**Mock Failures**: Check that fixtures are properly imported in conftest.py

### Debug Mode

Run tests with more verbose output:
```bash
pytest tests/ -v -s --tb=long
```

### Test Specific Function
```bash
pytest tests/test_main.py::TestApplication::test_app_creation -v -s
```

## Performance Benchmarks

Expected performance benchmarks:

- **Unit Tests**: <50ms per test
- **Integration Tests**: <200ms per test
- **Database Tests**: <100ms per test
- **Full Test Suite**: <30 seconds
- **Coverage Analysis**: <10 seconds additional

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure >80% coverage for new code
3. Include unit, integration, and edge case tests
4. Update fixtures in conftest.py if needed
5. Document new test markers or categories
6. Run full test suite before committing

For questions or issues with tests, refer to the test documentation or create an issue in the project repository.