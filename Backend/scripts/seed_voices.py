import os
import sys

from google.cloud import texttospeech

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.tts_service import TTSService
from utils.database import db


def seed_voices():
    """
    Fetches voices from the Google Text-to-Speech API and populates the
    database.
    """
    # Initialize the TTS service
    tts_service = TTSService()

    # Fetch the list of voices
    voices = tts_service.client.list_voices().voices

    # Get the database collection
    voice_collection = db.get_collection("voices")
    if voice_collection is None:
        print("Could not connect to the database. Aborting.")
        return

    # Clear existing voices to avoid duplicates
    voice_collection.delete_many({})

    voice_documents = []
    for voice in voices:
        voice_doc = {
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        }
        voice_documents.append(voice_doc)

    if voice_documents:
        voice_collection.insert_many(voice_documents)
        print(f"Successfully seeded {len(voice_documents)} voices into the database.")
    else:
        print("No voices found to seed.")


if __name__ == "__main__":
    seed_voices()
