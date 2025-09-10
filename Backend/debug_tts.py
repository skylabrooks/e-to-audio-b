from google.cloud import texttospeech
from credentials import get_credentials
import traceback

try:
    creds = get_credentials()
    if creds:
        client = texttospeech.TextToSpeechClient.from_service_account_info(creds)
    else:
        client = texttospeech.TextToSpeechClient()
    resp = client.list_voices()
    print(f"Got {len(resp.voices)} voices")
except Exception as e:
    print("ERROR initializing TTS client:")
    traceback.print_exc()
