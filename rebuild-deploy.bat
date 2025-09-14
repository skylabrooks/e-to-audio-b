@echo off
echo ========================================
echo    EtoAudioBook Rebuild & Deploy
echo ========================================

echo.
echo [1/5] Cleaning previous build...
if exist Backend\venv rmdir /s /q Backend\venv
if exist Frontend\node_modules rmdir /s /q Frontend\node_modules
if exist Frontend\build rmdir /s /q Frontend\build

echo.
echo [2/5] Setting up Backend...
cd Backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo [3/5] Testing TTS Connection...
python test_tts.py
if errorlevel 1 (
    echo ERROR: TTS test failed!
    pause
    exit /b 1
)

echo.
echo [4/5] Setting up Frontend...
cd ..\Frontend
npm install
npm run build

echo.
echo [5/5] Starting Services...
cd ..

echo Creating startup scripts...
echo @echo off > start-backend.bat
echo cd Backend >> start-backend.bat
echo call venv\Scripts\activate >> start-backend.bat
echo python app.py >> start-backend.bat

echo @echo off > start-frontend.bat
echo cd Frontend >> start-frontend.bat
echo npm start >> start-frontend.bat

echo.
echo ========================================
echo    Rebuild Complete!
echo ========================================
echo.
echo Starting backend server...
start "Backend" start-backend.bat

timeout /t 3 /nobreak > nul

echo Starting frontend server...
start "Frontend" start-frontend.bat

echo.
echo Application will open at http://localhost:3000
echo Backend API available at http://localhost:5000
echo.
pause