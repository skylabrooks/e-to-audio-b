@echo off
echo ========================================
echo    EtoAudioBook Local Deployment
echo ========================================

echo.
echo [1/4] Setting up Backend...
cd Backend

echo Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Setting up Frontend...
cd ..\Frontend

echo Installing Node.js dependencies...
npm install
if errorlevel 1 (
    echo Error: Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo.
echo [3/4] Creating startup scripts...
cd ..

echo Creating backend startup script...
echo @echo off > start-backend.bat
echo cd Backend >> start-backend.bat
echo call venv\Scripts\activate >> start-backend.bat
echo echo Starting Backend Server on http://localhost:5000 >> start-backend.bat
echo python app.py >> start-backend.bat

echo Creating frontend startup script...
echo @echo off > start-frontend.bat
echo cd Frontend >> start-frontend.bat
echo echo Starting Frontend Server on http://localhost:3000 >> start-frontend.bat
echo npm start >> start-frontend.bat

echo.
echo [4/4] Setup Complete!
echo ========================================
echo    Ready to Demo!
echo ========================================
echo.
echo To start your application:
echo 1. Run 'start-backend.bat' in one terminal
echo 2. Run 'start-frontend.bat' in another terminal
echo 3. Open http://localhost:3000 in your browser
echo.
echo Demo file: demo-story.md is ready to upload!
echo.
pause