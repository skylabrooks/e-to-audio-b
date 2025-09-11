# EtoAudioBook Project Makefile
.PHONY: help install install-dev setup clean test lint format check-security run-backend run-frontend run-all build deploy

# Default target
help:
	@echo "EtoAudioBook Development Commands:"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make setup        - Complete project setup"
	@echo ""
	@echo "Development Commands:"
	@echo "  make run-backend  - Start Flask backend server"
	@echo "  make run-frontend - Start React frontend server"
	@echo "  make run-all      - Start both backend and frontend"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  make lint         - Run all linters"
	@echo "  make format       - Format all code"
	@echo "  make test         - Run all tests"
	@echo "  make check-security - Run security checks"
	@echo ""
	@echo "Build Commands:"
	@echo "  make build        - Build frontend for production"
	@echo "  make clean        - Clean build artifacts"

# Installation commands
install:
	@echo "Installing production dependencies..."
	cd Backend && pip install -r requirements.txt
	cd Frontend && npm install --production

install-dev:
	@echo "Installing development dependencies..."
	cd Backend && pip install -r requirements.txt
	@if exist Backend\requirements-dev.txt (cd Backend && pip install -r requirements-dev.txt) else (echo "requirements-dev.txt not found, skipping...")
	cd Frontend && npm install
	@where pre-commit >nul 2>&1 && pre-commit install || echo "pre-commit not installed, skipping..."

setup: install-dev
	@echo "Setting up project..."
	@if not exist .env (if exist .env.example (copy .env.example .env && echo "Created .env file - please add your API keys") else (echo ".env.example not found, please create .env manually"))
	@echo "Project setup complete!"

# Development servers
run-backend:
	@echo "Starting Flask backend server..."
	cd Backend && python app.py

run-frontend:
	@echo "Starting React frontend server..."
	cd Frontend && npm start

run-all:
	@echo "Starting both backend and frontend servers..."
	@echo "Backend will run on http://localhost:5000"
	@echo "Frontend will run on http://localhost:3000"
	@echo "Use Ctrl+C to stop both servers"
	start /b cmd /c "cd Backend && python app.py" && cd Frontend && npm start

# Code quality commands
lint:
	@echo "Running linters..."
	cd Backend && flake8 .
	cd Backend && mypy .
	cd Frontend && npm run lint

format:
	@echo "Formatting code..."
	cd Backend && black .
	cd Backend && isort .
	cd Frontend && npm run format

test:
	@echo "Running all tests..."
	test-runner.bat

test-backend:
	@echo "Running backend tests..."
	cd Backend && pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html:htmlcov

test-frontend:
	@echo "Running frontend tests..."
	cd Frontend && npm run test:coverage

test-integration:
	@echo "Running integration tests..."
	cd Backend && pytest tests/test_integration.py -v

test-performance:
	@echo "Running performance tests..."
	cd Backend && pytest tests/test_performance.py -v

test-watch:
	@echo "Running tests in watch mode..."
	cd Backend && pytest tests/ -v --cov=. -f

test-security:
	@echo "Running security tests..."
	cd Backend && bandit -r . -f json -o bandit-report.json -x tests/
	cd Backend && safety check
	cd Frontend && npm audit

check-security: test-security
	@echo "Security check complete. Review bandit-report.json for details."

# Build commands
build:
	@echo "Building frontend for production..."
	cd Frontend && npm run build

clean:
	@echo "Cleaning build artifacts..."
	@if exist Frontend\build rmdir /s /q Frontend\build
	@if exist Backend\__pycache__ rmdir /s /q Backend\__pycache__
	@if exist Backend\.pytest_cache rmdir /s /q Backend\.pytest_cache
	@if exist Backend\htmlcov rmdir /s /q Backend\htmlcov
	@for /d %%i in (Backend\*.egg-info) do @if exist "%%i" rmdir /s /q "%%i"
	@for /r . %%i in (*.pyc) do @if exist "%%i" del /q "%%i"
	@for /r . %%i in (*.pyo) do @if exist "%%i" del /q "%%i"

# Pre-commit hooks
pre-commit:
	pre-commit run --all-files

# Test coverage
coverage:
	@echo "Generating coverage reports..."
	cd Backend && pytest --cov=. --cov-report=html:htmlcov --cov-report=term
	cd Frontend && npm run test:coverage
	@echo "Coverage reports generated:"
	@echo "  Backend: Backend\htmlcov\index.html"
	@echo "  Frontend: Frontend\coverage\lcov-report\index.html"

# Quality checks
quality:
	@echo "Running code quality checks..."
	cd Backend && flake8 . --exclude=venv,htmlcov --max-line-length=88
	cd Backend && black --check .
	cd Backend && mypy . --ignore-missing-imports
	cd Frontend && npm run lint
	cd Frontend && npm run format:check

# Docker commands (if needed in future)
docker-build:
	docker build -t etoaudiobook-backend ./Backend
	docker build -t etoaudiobook-frontend ./Frontend

docker-run:
	docker-compose up -d

# Environment management
env-check:
	@echo "Checking environment variables..."
	@python -c "import os; print('✅ GOOGLE_APPLICATION_CREDENTIALS:', 'Set' if os.getenv('GOOGLE_APPLICATION_CREDENTIALS') else '❌ Missing')"