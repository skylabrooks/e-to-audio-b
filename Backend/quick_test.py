import requests

# Quick backend health check
try:
    response = requests.get("http://localhost:5000/api/voices")
    if response.status_code == 200:
        voices = response.json().get('voices', [])
        print(f"✅ Backend is running! Found {len(voices)} voices available.")
    else:
        print(f"❌ Backend responded with status: {response.status_code}")
except Exception as e:
    print(f"❌ Cannot connect to backend: {e}")
    print("Make sure Flask is running on http://localhost:5000")