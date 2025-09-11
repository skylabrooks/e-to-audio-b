@echo off
echo ========================================
echo EtoAudioBook Deployment Verification
echo ========================================
echo.

set PASS=0
set FAIL=0

echo Testing deployment components...
echo.

REM Test 1: Docker containers running
echo [TEST 1] Checking Docker containers...
docker ps | findstr etoaudiobook >nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Docker containers running
    set /a PASS+=1
) else (
    echo ❌ Docker containers not found
    set /a FAIL+=1
)

REM Test 2: Backend health
echo [TEST 2] Backend health check...
curl -f -s http://localhost:5000/health >nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Backend healthy
    set /a PASS+=1
) else (
    echo ❌ Backend health check failed
    set /a FAIL+=1
)

REM Test 3: Frontend accessibility
echo [TEST 3] Frontend accessibility...
curl -f -s http://localhost/ >nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Frontend accessible
    set /a PASS+=1
) else (
    echo ❌ Frontend not accessible
    set /a FAIL+=1
)

REM Test 4: Redis connection
echo [TEST 4] Redis connection...
curl -s http://localhost:5000/metrics | findstr "redis_available.*true" >nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Redis connected
    set /a PASS+=1
) else (
    echo ❌ Redis connection failed
    set /a FAIL+=1
)

REM Test 5: API endpoints
echo [TEST 5] API endpoints...
curl -f -s http://localhost:5000/api/voices >nul
if %ERRORLEVEL% equ 0 (
    echo ✅ API endpoints working
    set /a PASS+=1
) else (
    echo ❌ API endpoints failed
    set /a FAIL+=1
)

REM Test 6: Performance metrics
echo [TEST 6] Performance metrics...
curl -s http://localhost:5000/metrics | findstr "memory_rss_mb" >nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Performance monitoring active
    set /a PASS+=1
) else (
    echo ❌ Performance monitoring failed
    set /a FAIL+=1
)

REM Test 7: Security headers
echo [TEST 7] Security headers...
curl -I -s http://localhost:5000/health | findstr "X-Frame-Options" >nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Security headers present
    set /a PASS+=1
) else (
    echo ❌ Security headers missing
    set /a FAIL+=1
)

echo.
echo ========================================
echo Deployment Verification Results
echo ========================================
echo Tests Passed: %PASS%
echo Tests Failed: %FAIL%
echo.

if %FAIL% equ 0 (
    echo ✅ ALL TESTS PASSED - Deployment Successful!
    echo.
    echo Your EtoAudioBook application is ready for use:
    echo 🌐 Frontend: http://localhost
    echo 🔧 Backend API: http://localhost:5000
    echo 📊 Metrics: http://localhost:5000/metrics
    echo 💚 Health: http://localhost:5000/health
    echo.
    echo Next steps:
    echo 1. Upload demo-story.md to test the full workflow
    echo 2. Run integration-test.bat for comprehensive testing
    echo 3. Run load-test.bat to verify performance
    exit /b 0
) else (
    echo ❌ DEPLOYMENT ISSUES DETECTED
    echo.
    echo Please check the following:
    echo 1. Docker containers: docker-compose ps
    echo 2. Service logs: docker-compose logs
    echo 3. Environment variables in .env file
    echo 4. Google Cloud credentials path
    exit /b 1
)