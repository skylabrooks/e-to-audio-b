@echo off
echo ========================================
echo EtoAudioBook Load Testing
echo ========================================
echo.

set BASE_URL=http://localhost:5000

echo Testing concurrent health checks...
echo Starting 20 concurrent requests...

REM Create multiple background requests
for /l %%i in (1,1,20) do (
    start /b curl -s -w "%%{time_total}\n" %BASE_URL%/health
)

timeout /t 5

echo.
echo Testing voice endpoint under load...
for /l %%i in (1,1,10) do (
    start /b curl -s %BASE_URL%/api/voices
)

timeout /t 3

echo.
echo Checking system metrics after load...
curl -s %BASE_URL%/metrics | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print('Memory Usage:', data['system']['memory_rss_mb'], 'MB')
    print('CPU Usage:', data['system']['cpu_percent'], '%%')
    print('Active Threads:', data['system']['num_threads'])
    if 'request.duration' in data['application']:
        req_stats = data['application']['request.duration']
        print('Avg Response Time:', round(req_stats['avg'], 3), 'seconds')
        print('Max Response Time:', round(req_stats['max'], 3), 'seconds')
        print('Total Requests:', req_stats['count'])
except:
    print('Could not parse metrics')
"

echo.
echo ========================================
echo Load test complete!
echo Check metrics above for performance data.
echo ========================================