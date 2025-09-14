#!/usr/bin/env python3
"""
Quick TTS API Test Script
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from services.tts_service import TTSService

def test_tts_connection():
    print("Testing TTS Service Connection...")
    
    try:
        # Initialize service
        tts = TTSService()
        print("[OK] TTS Service initialized")
        
        # Test voice listing
        voices = tts.list_voices(per_page=3)
        print(f"[OK] Found {len(voices)} voices")
        
        if voices:
            print("Sample voices:")
            for voice in voices[:3]:
                print(f"  - {voice['name']} ({voice['ssml_gender']})")
        
        # Test speech synthesis
        test_text = "Hello, this is a test."
        voice_name = "en-US-Standard-A"
        language_code = "en-US"
        
        print(f"\nTesting synthesis with voice: {voice_name}")
        audio_data = tts.synthesize_speech(test_text, voice_name, language_code)
        print(f"[OK] Generated audio: {len(audio_data)} characters (base64)")
        
        print("\n[SUCCESS] All tests passed! TTS API is working correctly.")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False

if __name__ == "__main__":
    test_tts_connection()