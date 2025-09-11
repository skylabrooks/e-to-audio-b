@echo off
echo ========================================
echo EtoAudioBook Performance Testing
echo ========================================
echo.

REM Check if backend is running
curl -s http://localhost:5000/health >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Backend not running. Please start the backend first.
    exit /b 1
)

echo Backend is running. Starting performance tests...
echo.

REM Test 1: Health endpoint response time
echo Testing health endpoint...
for /l %%i in (1,1,10) do (
    curl -s -w "Response time: %%{time_total}s\n" -o nul http://localhost:5000/health
)

echo.
echo Testing voice listing performance...
REM Test 2: Voice listing
curl -s -w "Voice listing time: %%{time_total}s\n" -o nul http://localhost:5000/api/voices

echo.
echo Testing concurrent requests...
REM Test 3: Concurrent requests (simplified)
start /b curl -s http://localhost:5000/health
start /b curl -s http://localhost:5000/health
start /b curl -s http://localhost:5000/health
start /b curl -s http://localhost:5000/health
start /b curl -s http://localhost:5000/health

timeout /t 2 >nul

echo.
echo Checking performance metrics...
curl -s http://localhost:5000/metrics | python -m json.tool

echo.
echo ========================================
echo Performance test complete!
echo Check the metrics above for performance data.
echo ========================================