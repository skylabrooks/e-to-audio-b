@echo off
echo ========================================
echo EtoAudioBook Production Deployment
echo ========================================
echo.

REM Pre-deployment checks
echo [1/8] Pre-deployment checks...
if not exist .env (
    echo [ERROR] .env file not found. Copy from .env.example and configure.
    exit /b 1
)

if not defined GOOGLE_CREDENTIALS_PATH (
    echo [ERROR] GOOGLE_CREDENTIALS_PATH not set. Please set environment variable.
    exit /b 1
)

if not exist "%GOOGLE_CREDENTIALS_PATH%" (
    echo [ERROR] Google credentials file not found at %GOOGLE_CREDENTIALS_PATH%
    exit /b 1
)

echo [2/8] Running security checks...
cd Backend
call venv\Scripts\activate
bandit -r . -f json -o bandit-report.json -x tests/ || echo "Security warnings found - review bandit-report.json"
cd ..

echo [3/8] Running tests...
test-runner.bat
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Tests failed. Fix issues before deployment.
    exit /b 1
)

echo [4/8] Building Docker images...
docker-compose build --no-cache
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker build failed.
    exit /b 1
)

echo [5/8] Starting Redis...
docker run -d --name etoaudiobook-redis -p 6379:6379 redis:7-alpine
timeout /t 3

echo [6/8] Starting services...
docker-compose up -d
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Service startup failed.
    exit /b 1
)

echo [7/8] Waiting for services to be ready...
timeout /t 10

echo [8/8] Running health checks...
curl -f http://localhost:5000/health || (
    echo [ERROR] Backend health check failed
    docker-compose logs backend
    exit /b 1
)

curl -f http://localhost/ || (
    echo [ERROR] Frontend health check failed
    docker-compose logs frontend
    exit /b 1
)

echo.
echo ========================================
echo ✅ Deployment Successful!
echo ========================================
echo Frontend: http://localhost
echo Backend API: http://localhost:5000
echo Metrics: http://localhost:5000/metrics
echo.
echo To stop: docker-compose down
echo To view logs: docker-compose logs -f