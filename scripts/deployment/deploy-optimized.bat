@echo off
echo Starting optimized deployment for EtoAudioBook...

REM Set production environment
set FLASK_ENV=production
set ASYNC_WORKERS=8
set TTS_BATCH_SIZE=10

echo Setting up Backend with optimizations...
cd Backend

REM Install dependencies with optimizations
pip install --upgrade pip
pip install -r requirements.txt

REM Start Redis for caching (if not already running)
echo Starting Redis server...
start /B redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru

REM Start backend with Gunicorn for production
echo Starting optimized backend server...
start /B gunicorn --workers 4 --threads 2 --worker-class gthread --bind 0.0.0.0:5000 --timeout 120 app:app

cd ..

echo Setting up Frontend with optimizations...
cd Frontend

REM Install dependencies
call npm ci --production

REM Build optimized production bundle
call npm run build

REM Serve with optimized settings
echo Starting optimized frontend server...
start /B npx serve -s build -l 3000

cd ..

echo Optimized deployment complete!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo Monitoring: http://localhost:5000/monitoring/health

timeout /t 5