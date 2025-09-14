import requests
import json
from collections import defaultdict
from services.voice_classifier import VoiceClassifier

def analyze_voice_library():
    """Analyze and classify all voices in the library"""
    
    # Get all voices from the API
    try:
        response = requests.get('http://localhost:5000/api/voices/all')
        data = response.json()
        voices = data['voices']
    except Exception as e:
        print(f"Error fetching voices: {e}")
        return
    
    # Classification counters
    stats = {
        'total': len(voices),
        'by_language': defaultdict(int),
        'by_region': defaultdict(int),
        'by_gender': defaultdict(int),
        'by_quality': defaultdict(int),
        'by_use_case': defaultdict(int),
        'by_character_theme': defaultdict(int),
        'by_tone': defaultdict(int),
        'by_age': defaultdict(int)
    }
    
    classified_voices = []
    
    # Classify each voice
    for voice in voices:
        # Get language code (first one if multiple)
        language_code = voice['language_codes'][0] if voice['language_codes'] else 'unknown'
        
        # Classify the voice
        classification = VoiceClassifier.classify_voice(
            voice['name'], 
            language_code, 
            voice['ssml_gender']
        )
        
        # Add original voice data
        classified_voice = {
            **voice,
            **classification
        }
        classified_voices.append(classified_voice)
        
        # Update statistics
        stats['by_language'][classification['language']] += 1
        stats['by_region'][classification['region']] += 1
        stats['by_gender'][voice['ssml_gender']] += 1
        stats['by_quality'][classification['quality']] += 1
        stats['by_use_case'][classification['use_case']] += 1
        stats['by_character_theme'][classification['character_theme']] += 1
        stats['by_tone'][classification['tone']] += 1
        stats['by_age'][classification['age']] += 1
    
    # Print statistics
    print("=== VOICE LIBRARY ANALYSIS ===")
    print(f"Total Voices: {stats['total']}")
    print()
    
    print("BY LANGUAGE:")
    for lang, count in sorted(stats['by_language'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {lang}: {count}")
    print()
    
    print("BY GENDER:")
    for gender, count in sorted(stats['by_gender'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {gender}: {count}")
    print()
    
    print("BY QUALITY:")
    for quality, count in sorted(stats['by_quality'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {quality}: {count}")
    print()
    
    print("BY CHARACTER THEME:")
    for theme, count in sorted(stats['by_character_theme'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {theme}: {count}")
    print()
    
    print("BY USE CASE:")
    for use_case, count in sorted(stats['by_use_case'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {use_case}: {count}")
    print()
    
    print("BY TONE:")
    for tone, count in sorted(stats['by_tone'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {tone}: {count}")
    print()
    
    print("BY AGE:")
    for age, count in sorted(stats['by_age'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {age}: {count}")
    print()
    
    # Save detailed analysis
    with open('voice_analysis.json', 'w') as f:
        json.dump({
            'statistics': dict(stats),
            'classified_voices': classified_voices
        }, f, indent=2)
    
    print("Detailed analysis saved to voice_analysis.json")
    
    # Show some interesting findings
    print("\n=== INTERESTING FINDINGS ===")
    
    # Character themed voices
    themed_voices = [v for v in classified_voices if v['character_theme'] != 'neutral']
    print(f"Character-themed voices: {len(themed_voices)}")
    
    for theme in ['dark', 'playful', 'mythological']:
        theme_voices = [v for v in themed_voices if v['character_theme'] == theme]
        if theme_voices:
            print(f"  {theme.title()}: {len(theme_voices)} voices")
            for voice in theme_voices[:3]:  # Show first 3
                print(f"    - {voice['name']} ({voice['ssml_gender']})")
    
    return stats, classified_voices

if __name__ == "__main__":
    analyze_voice_library()