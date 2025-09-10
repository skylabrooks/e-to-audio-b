import requests
import json

def test_voices_endpoint():
    """Test the /api/voices endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/voices')
        if response.status_code == 200:
            data = response.json()
            # Handle response being either a list or an object with 'voices'
            if isinstance(data, list):
                voices = data
            elif isinstance(data, dict) and 'voices' in data:
                voices = data['voices']
            else:
                print('Unexpected response shape:')
                print(json.dumps(data, indent=2))
                return

            print(f"Successfully retrieved {len(voices)} voices")
            print("\nSample voices:")
            for voice in voices[:5]:  # Show first 5 voices
                print(f"- {voice.get('name')} ({voice.get('ssml_gender')}, {voice.get('voice_type', 'Standard')})")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error testing voices endpoint: {str(e)}")

if __name__ == '__main__':
    test_voices_endpoint()
