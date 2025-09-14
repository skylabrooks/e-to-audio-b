import requests
import json
from services.voice_tagger import VoiceTagger

def test_voice_tagging():
    """Test voice tagging functionality"""
    
    # Get voices from the existing API
    try:
        response = requests.get('http://localhost:5000/api/voices/all')
        data = response.json()
        voices = data['voices'][:20]  # Test with first 20 voices
    except Exception as e:
        print(f"Error fetching voices, using mock data: {e}")
        # Use some mock voices for testing
        voices = [
            {"name": "Charon", "language_codes": ["en-US"], "ssml_gender": "MALE"},
            {"name": "Fenrir", "language_codes": ["en-US"], "ssml_gender": "MALE"},
            {"name": "Puck", "language_codes": ["en-US"], "ssml_gender": "MALE"},
            {"name": "Zephyr", "language_codes": ["en-US"], "ssml_gender": "FEMALE"},
            {"name": "en-US-Neural2-A", "language_codes": ["en-US"], "ssml_gender": "MALE"},
            {"name": "es-ES-Standard-A", "language_codes": ["es-ES"], "ssml_gender": "FEMALE"}
        ]
    
    print("=== VOICE TAGGING TEST ===")
    print(f"Testing with {len(voices)} voices\n")
    
    # Tag all voices
    tagged_voices = VoiceTagger.tag_all_voices(voices)
    
    # Show some examples
    print("TAGGED VOICE EXAMPLES:")
    for voice in tagged_voices[:5]:
        print(f"Voice: {voice['name']}")
        print(f"  Tags: {voice['tags']}")
        print(f"  Search: {voice['search_text'][:50]}...")
        print()
    
    # Test filtering
    print("FILTERING TESTS:")
    
    # Filter by character theme
    dark_voices = VoiceTagger.filter_voices(tagged_voices, {'character_theme': 'dark'})
    print(f"Dark character voices: {len(dark_voices)}")
    for voice in dark_voices:
        print(f"  - {voice['name']} ({voice['tags']['gender']})")
    
    # Filter by language
    english_voices = VoiceTagger.filter_voices(tagged_voices, {'language': 'English'})
    print(f"\nEnglish voices: {len(english_voices)}")
    
    # Filter by quality
    high_quality = VoiceTagger.filter_voices(tagged_voices, {'quality': 'high'})
    print(f"High quality voices: {len(high_quality)}")
    
    # Get filter options
    options = VoiceTagger.get_filter_options(tagged_voices)
    print(f"\nAVAILABLE FILTER OPTIONS:")
    for key, values in options.items():
        print(f"  {key}: {values}")
    
    # Save sample tagged voices
    with open('sample_tagged_voices.json', 'w') as f:
        json.dump(tagged_voices[:10], f, indent=2)
    
    print(f"\nSample tagged voices saved to sample_tagged_voices.json")
    
    return tagged_voices

if __name__ == "__main__":
    test_voice_tagging()