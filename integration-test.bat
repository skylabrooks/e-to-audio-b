@echo off
echo ========================================
echo EtoAudioBook Integration Testing
echo ========================================
echo.

set BASE_URL=http://localhost:5000
set FRONTEND_URL=http://localhost

echo [1/6] Testing backend health...
curl -f %BASE_URL%/health
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Backend health check failed
    exit /b 1
)
echo ✅ Backend healthy

echo.
echo [2/6] Testing voice endpoints...
curl -f %BASE_URL%/api/voices > voices.json
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Voice listing failed
    exit /b 1
)
echo ✅ Voice listing working

echo.
echo [3/6] Testing file upload...
echo **Narrator:** Test story > test-story.txt
curl -f -X POST -F "file=@test-story.txt" %BASE_URL%/api/detect-roles > roles.json
if %ERRORLEVEL% neq 0 (
    echo [ERROR] File upload failed
    exit /b 1
)
echo ✅ File upload working

echo.
echo [4/6] Testing performance metrics...
curl -f %BASE_URL%/metrics > metrics.json
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Metrics endpoint failed
    exit /b 1
)
echo ✅ Metrics endpoint working

echo.
echo [5/6] Testing frontend...
curl -f %FRONTEND_URL% > nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Frontend not accessible
    exit /b 1
)
echo ✅ Frontend accessible

echo.
echo [6/6] Running performance test...
performance-test.bat

echo.
echo ========================================
echo ✅ Integration Tests Passed!
echo ========================================
echo.
echo Test Results:
echo - Backend: ✅ Healthy
echo - API Endpoints: ✅ Working
echo - File Processing: ✅ Working
echo - Performance: ✅ Monitored
echo - Frontend: ✅ Accessible
echo.

REM Cleanup
del test-story.txt voices.json roles.json metrics.json 2>nul

echo Integration testing complete!