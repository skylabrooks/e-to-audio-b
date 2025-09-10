#!/usr/bin/env python3
"""
Test script for EtoAudioBook Flask backend
Run with: uvx mcp-run-python test_backend.py
"""

import requests
import json
import base64

# Test configuration
BASE_URL = "http://localhost:5000"

def test_voices_endpoint():
    """Test the /api/voices endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/voices")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Voices endpoint: Found {len(data.get('voices', []))} voices")
            return True
        else:
            print(f"❌ Voices endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Voices endpoint error: {e}")
        return False

def test_detect_roles():
    """Test the /api/detect-roles endpoint"""
    try:
        # Create test content
        test_content = """**Narrator:** Once upon a time in a magical kingdom...

**Princess:** Help me, brave knight!

**Knight:** I shall save you, Princess!"""
        
        # Create a mock file
        files = {'file': ('test.md', test_content, 'text/markdown')}
        response = requests.post(f"{BASE_URL}/api/detect-roles", files=files)
        
        if response.status_code == 200:
            data = response.json()
            roles = data.get('roles', [])
            segments = data.get('segments', [])
            print(f"✅ Detect roles: Found {len(roles)} roles, {len(segments)} segments")
            print(f"   Roles: {roles}")
            return True
        else:
            print(f"❌ Detect roles failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Detect roles error: {e}")
        return False

def test_voice_preview():
    """Test the /api/preview-voice endpoint"""
    try:
        payload = {
            "voiceName": "en-US-Standard-A",
            "text": "Hello, this is a test preview."
        }
        response = requests.post(f"{BASE_URL}/api/preview-voice", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            audio_data = data.get('audio')
            if audio_data and len(audio_data) > 100:  # Check if we got substantial audio data
                print("✅ Voice preview: Audio generated successfully")
                return True
            else:
                print("❌ Voice preview: No audio data received")
                return False
        else:
            print(f"❌ Voice preview failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Voice preview error: {e}")
        return False

def run_all_tests():
    """Run all backend tests"""
    print("🧪 Testing EtoAudioBook Flask Backend")
    print("=" * 40)
    
    tests = [
        ("Voices Endpoint", test_voices_endpoint),
        ("Detect Roles", test_detect_roles),
        ("Voice Preview", test_voice_preview)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check your backend configuration.")

if __name__ == "__main__":
    run_all_tests()