import base64
import logging
import os
from openai import OpenAI

logger = logging.getLogger(__name__)

class OpenAITTSService:
    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OpenAI API key not found. OpenAI TTS will not be available.")
            self.client = None
        else:
            try:
                self.client = OpenAI(api_key=api_key)
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.client = None
        self.voices = [
            {"name": "alloy", "gender": "NEUTRAL"},
            {"name": "echo", "gender": "MALE"},
            {"name": "fable", "gender": "NEUTRAL"},
            {"name": "onyx", "gender": "MALE"},
            {"name": "nova", "gender": "FEMALE"},
            {"name": "shimmer", "gender": "FEMALE"}
        ]
    
    def list_voices(self):
        if not self.client:
            return []
        return [
            {
                "name": f"openai-{voice['name']}",
                "language_codes": ["en-US"],
                "ssml_gender": voice["gender"],
                "natural_sample_rate_hertz": 24000,
            }
            for voice in self.voices
        ]
    
    def synthesize_speech(self, text, voice_name):
        if not self.client:
            raise Exception("OpenAI API key not configured")
            
        # Extract voice name (remove openai- prefix)
        voice = voice_name.replace("openai-", "") if voice_name.startswith("openai-") else "alloy"
        
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        return base64.b64encode(response.content).decode("utf-8")