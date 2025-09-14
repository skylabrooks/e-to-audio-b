@echo off
echo Starting EtoAudioBook Docker Deployment...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Check if credentials file exists
if not exist "Backend\credentials\service-account.json" (
    echo Error: Google Cloud service account credentials not found.
    echo Please place your service-account.json file in Backend\credentials\
    pause
    exit /b 1
)

REM Stop existing containers
echo Stopping existing containers...
docker-compose down

REM Build and start containers
echo Building and starting containers...
docker-compose up --build -d

REM Wait for services to start
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check container status
echo Checking container status...
docker-compose ps

echo.
echo Deployment complete!
echo Frontend: http://localhost
echo Backend API: http://localhost:5000
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
pause