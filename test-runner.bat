@echo off
echo ========================================
echo EtoAudioBook Test Suite Runner
echo ========================================
echo.

set FAILED=0

echo Running Backend Tests...
echo ========================
cd Backend

REM Activate virtual environment
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo [ERROR] Virtual environment not found. Run setup first.
    exit /b 1
)

REM Install test dependencies
echo Installing test dependencies...
pip install -r requirements-dev.txt

REM Run backend tests
echo.
echo Running Python tests...
pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html:htmlcov
if %ERRORLEVEL% neq 0 set FAILED=1

REM Run security checks
echo.
echo Running security checks...
bandit -r . -f json -o bandit-report.json -x tests/
if %ERRORLEVEL% neq 0 set FAILED=1

REM Run code quality checks
echo.
echo Running code quality checks...
flake8 . --exclude=venv,htmlcov --max-line-length=88
if %ERRORLEVEL% neq 0 set FAILED=1

black --check .
if %ERRORLEVEL% neq 0 set FAILED=1

mypy . --ignore-missing-imports
if %ERRORLEVEL% neq 0 set FAILED=1

cd ..

echo.
echo Running Frontend Tests...
echo =========================
cd Frontend

REM Install dependencies
echo Installing frontend dependencies...
npm install

REM Run frontend tests
echo.
echo Running React tests...
npm run test:coverage
if %ERRORLEVEL% neq 0 set FAILED=1

REM Run linting
echo.
echo Running ESLint...
npm run lint
if %ERRORLEVEL% neq 0 set FAILED=1

REM Run formatting check
echo.
echo Checking code formatting...
npm run format:check
if %ERRORLEVEL% neq 0 set FAILED=1

cd ..

echo.
echo ========================================
if %FAILED% equ 0 (
    echo ✅ All tests passed!
    echo.
    echo Test Reports:
    echo - Backend Coverage: Backend\htmlcov\index.html
    echo - Security Report: Backend\bandit-report.json
    echo - Frontend Coverage: Frontend\coverage\lcov-report\index.html
) else (
    echo ❌ Some tests failed!
    echo Please check the output above for details.
)
echo ========================================

exit /b %FAILED%