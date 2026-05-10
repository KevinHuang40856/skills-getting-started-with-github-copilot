# Backend Test Suite

This directory contains comprehensive test coverage for the Mergington High School Activities API using pytest and FastAPI's TestClient.

## Structure

- **conftest.py** — Shared test fixtures and configuration
  - `client` fixture: Provides TestClient with fresh app state per test
  - Test data reset: Ensures test isolation by deep-copying original activities before each test

- **test_activities.py** — Tests for GET /activities endpoint
  - Validates response structure, data types, and completeness
  - 11 tests covering: status code, return type, activity count, field validation

- **test_signup.py** — Tests for POST /activities/{activity_name}/signup endpoint  
  - Happy path: successful signup and participant list updates
  - Error cases: non-existent activity (404), duplicate signup (400), missing parameters (422)
  - Edge cases: special characters in email, activity names with spaces
  - 11 tests

- **test_unsignup.py** — Tests for DELETE /activities/{activity_name}/signup endpoint
  - Happy path: removing participant and verifying removal
  - Error cases: non-existent activity (404), not signed up (400), missing parameters (422)
  - Sequences: signup → unsignup → signup workflows
  - 11 tests

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run with verbose output
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/test_activities.py -v
```

### Run specific test class
```bash
pytest tests/test_signup.py::TestSignupForActivity -v
```

### Run with coverage (if pytest-cov installed)
```bash
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

## Test Coverage

- **33 total tests** across 3 test modules
- **GET /activities**: 11 tests
- **POST signup**: 11 tests
- **DELETE unsignup**: 11 tests

### Coverage by endpoint:
- ✅ Status codes (200, 400, 404, 422)
- ✅ Response structure and data types
- ✅ Happy path scenarios
- ✅ Error cases and edge cases
- ✅ Participant list management
- ✅ Test isolation with fresh app state

## Test Fixtures

All tests use the `client` fixture from `conftest.py`:
- Fresh TestClient instance per test
- Activities data reset to original state (with deep copy)
- Ensures no cross-test contamination

### Using fixtures in tests:
```python
def test_example(self, client, existing_activity, sample_email):
    """Example test using fixtures."""
    response = client.get("/activities")
    assert response.status_code == 200
```

Available fixtures:
- `client` — FastAPI TestClient with reset app state
- `existing_activity` — "Chess Club" (guaranteed to exist)
- `non_existent_activity` — "Nonexistent Activity" (doesn't exist)
- `sample_email` — "test.student@mergington.edu"

## Key Design Decisions

1. **Test Isolation**: Deep copy of activities data before each test prevents state leakage
2. **By Endpoint**: Tests organized by API endpoint for clarity
3. **Comprehensive Coverage**: Both happy paths and error cases tested
4. **FastAPI TestClient**: In-process testing (no server startup needed)
5. **pytest Framework**: Uses pytest.ini config with pythonpath set to project root

## Adding New Tests

1. Add test method to appropriate test class (or create new module if needed)
2. Use `client` fixture and other fixtures as needed
3. Ensure test name is descriptive (e.g., `test_signup_with_invalid_email`)
4. Run tests to verify: `pytest tests/test_*.py -v`

## Troubleshooting

**Issue**: Tests fail with "Module not found" errors
- **Solution**: Ensure pytest.ini has `pythonpath = .` set

**Issue**: Test state leaks between tests
- **Solution**: The client fixture uses deep_copy to prevent this; if a new fixture is added, use deepcopy for mutable objects

**Issue**: Import errors for app module
- **Solution**: Verify conftest.py imports use `from src import app as app_module` to access the module-level app and activities

## Dependencies

- pytest (installed via `pip install pytest`)
- fastapi
- uvicorn  
- httpx (for TestClient compatibility)

These should already be in your requirements.txt. If not, install with:
```bash
pip install -r requirements.txt
```
