# 🧪 Testing Guide

## Overview

Comprehensive test suite covering unit tests, integration tests, performance tests, and end-to-end testing.

## Test Structure

```
Backend/tests/
├── __init__.py
├── conftest.py              # Test fixtures and configuration
├── test_app.py              # API endpoint tests
├── test_credentials.py      # Credential management tests
├── test_config.py           # Configuration tests
├── test_integration.py      # Integration tests
└── test_performance.py      # Performance tests

Frontend/src/
├── App.test.js              # Main app tests
├── setupTests.js            # Test configuration
└── components/__tests__/    # Component tests
    ├── FileUploader.test.js
    └── AudioPlayer.test.js
```

## Running Tests

### Quick Test Run
```bash
# Run all tests
test-runner.bat

# Backend only
cd Backend && pytest

# Frontend only
cd Frontend && npm test
```

### Detailed Test Commands

#### Backend Tests
```bash
cd Backend

# Unit tests with coverage
pytest tests/ -v --cov=. --cov-report=html

# Integration tests only
pytest tests/test_integration.py -v

# Performance tests
pytest tests/test_performance.py -v

# Security scan
bandit -r . -f json -o bandit-report.json

# Code quality
flake8 . --max-line-length=88
black --check .
mypy . --ignore-missing-imports
```

#### Frontend Tests
```bash
cd Frontend

# Unit tests with coverage
npm run test:coverage

# Watch mode for development
npm test

# Linting
npm run lint

# Format check
npm run format:check
```

## Test Coverage Goals

- **Backend**: Minimum 80% code coverage
- **Frontend**: Minimum 75% code coverage
- **Integration**: All critical user flows
- **Performance**: Response time benchmarks

## Test Categories

### 1. Unit Tests
- Individual function testing
- Component isolation
- Mock external dependencies
- Fast execution (< 1s per test)

### 2. Integration Tests
- API endpoint workflows
- Database interactions
- External service integration
- Complete user journeys

### 3. Performance Tests
- Response time validation
- Memory usage monitoring
- Concurrent request handling
- Rate limiting verification

### 4. Security Tests
- Input validation
- File upload restrictions
- Rate limiting enforcement
- XSS/injection prevention

## Test Data

### Sample Files
```
tests/fixtures/
├── sample-story.txt         # Valid story file
├── sample-story.md          # Markdown story
├── invalid-file.exe         # Invalid file type
└── large-story.txt          # Performance testing
```

### Mock Data
- Google TTS API responses
- Voice listings
- Audio synthesis results
- Error scenarios

## Continuous Integration

### GitHub Actions (Future)
```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Backend Tests
        run: |
          cd Backend
          pip install -r requirements-dev.txt
          pytest --cov=. --cov-report=xml
      - name: Run Frontend Tests
        run: |
          cd Frontend
          npm install
          npm run test:coverage
```

## Test Environment Setup

### Backend Environment
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Set test environment variables
set FLASK_ENV=testing
set GOOGLE_APPLICATION_CREDENTIALS=test-credentials.json
```

### Frontend Environment
```bash
# Install dependencies
npm install

# Set test environment
set REACT_APP_API_URL=http://localhost:5000
```

## Writing New Tests

### Backend Test Template
```python
import pytest
from unittest.mock import patch, Mock

class TestNewFeature:
    def test_feature_success(self, client):
        """Test successful feature operation."""
        response = client.post('/api/new-feature', json={'data': 'test'})
        assert response.status_code == 200
    
    def test_feature_error(self, client):
        """Test feature error handling."""
        response = client.post('/api/new-feature', json={})
        assert response.status_code == 400
```

### Frontend Test Template
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import NewComponent from '../NewComponent';

describe('NewComponent', () => {
  test('renders correctly', () => {
    render(<NewComponent />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });
  
  test('handles user interaction', () => {
    const mockCallback = jest.fn();
    render(<NewComponent onAction={mockCallback} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(mockCallback).toHaveBeenCalled();
  });
});
```

## Test Best Practices

### Do's
- ✅ Write tests before fixing bugs
- ✅ Use descriptive test names
- ✅ Test both success and error cases
- ✅ Mock external dependencies
- ✅ Keep tests independent
- ✅ Use appropriate assertions

### Don'ts
- ❌ Test implementation details
- ❌ Write flaky tests
- ❌ Skip error case testing
- ❌ Use real external services
- ❌ Make tests dependent on each other
- ❌ Ignore test failures

## Debugging Tests

### Backend Debugging
```bash
# Run specific test with verbose output
pytest tests/test_app.py::TestDetectRoles::test_detect_roles_success -v -s

# Debug with pdb
pytest --pdb tests/test_app.py

# Show coverage gaps
pytest --cov=. --cov-report=html
# Open htmlcov/index.html
```

### Frontend Debugging
```bash
# Run tests in debug mode
npm test -- --verbose

# Run specific test file
npm test FileUploader.test.js

# Debug in browser
npm test -- --debug
```

## Performance Benchmarks

### Response Time Targets
- Health check: < 100ms
- File upload: < 2s
- Voice listing: < 1s
- Audio synthesis: < 10s per segment

### Memory Usage Targets
- Idle memory: < 100MB
- Peak memory: < 500MB
- Memory leaks: 0

## Test Reports

### Coverage Reports
- Backend: `Backend/htmlcov/index.html`
- Frontend: `Frontend/coverage/lcov-report/index.html`

### Security Reports
- Bandit: `Backend/bandit-report.json`
- npm audit: `Frontend/npm-audit.json`

## Troubleshooting

### Common Issues

**Tests failing locally but passing in CI:**
- Check environment variables
- Verify dependency versions
- Clear test caches

**Flaky tests:**
- Add proper waits for async operations
- Mock time-dependent operations
- Ensure test isolation

**Low coverage:**
- Identify untested code paths
- Add edge case tests
- Test error conditions

**Performance test failures:**
- Check system resources
- Adjust timeout values
- Profile slow operations