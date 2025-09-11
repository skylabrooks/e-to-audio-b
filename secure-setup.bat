@echo off
echo ========================================
echo EtoAudioBook Secure Setup
echo ========================================
echo.

REM Check if .env file exists
if exist .env (
    echo [WARNING] .env file already exists. Please review it for security.
    echo.
) else (
    echo Creating .env file from template...
    copy .env.example .env
    echo [ACTION REQUIRED] Please edit .env file with your credentials
    echo.
)

REM Check for credential files in project directory
echo Checking for credential files in project directory...
if exist Backend\*.json (
    echo [SECURITY RISK] JSON files found in Backend directory!
    echo Please move credential files outside the project directory.
    echo.
)

REM Backend setup
echo Setting up Backend...
cd Backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Backend setup complete!
cd ..

REM Frontend setup
echo Setting up Frontend...
cd Frontend

echo Installing dependencies...
npm install

echo Checking for vulnerabilities...
npm audit

echo.
echo Frontend setup complete!
cd ..

echo.
echo ========================================
echo SECURITY CHECKLIST
echo ========================================
echo [ ] Move service account JSON file outside project directory
echo [ ] Set GOOGLE_APPLICATION_CREDENTIALS environment variable
echo [ ] Edit .env file with your configuration
echo [ ] Review SECURITY.md for additional guidelines
echo [ ] Run 'npm audit fix' if vulnerabilities found
echo.
echo Setup complete! Please complete the security checklist above.
pause