@echo off
echo ========================================
echo EtoAudioBook Production Deployment
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo [ERROR] .env file not found. Please create it from .env.example
    exit /b 1
)

REM Check if credentials are set
if not defined GOOGLE_CREDENTIALS_PATH (
    echo [ERROR] GOOGLE_CREDENTIALS_PATH environment variable not set
    echo Please set it to the path of your service account JSON file
    exit /b 1
)

REM Build and start services
echo Building Docker images...
docker-compose build

echo Starting services...
docker-compose up -d

echo.
echo Waiting for services to start...
timeout /t 10

echo.
echo Checking service health...
docker-compose ps

echo.
echo ========================================
echo Deployment complete!
echo ========================================
echo Frontend: http://localhost
echo Backend API: http://localhost:5000
echo Health check: http://localhost:5000/health
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down