import json
import logging
import os
from typing import Dict, List

import google.generativeai as genai

logger = logging.getLogger(__name__)

class VoiceAnalyzer:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
            logger.warning("Gemini API key not found. Voice analysis disabled.")

    def analyze_voice_sample(self, audio_data: bytes, voice_name: str) -> Dict:
        """Analyze voice characteristics using Gemini"""
        if not self.model:
            return self._get_fallback_analysis(voice_name)
        
        try:
            prompt = """
            Analyze this voice sample and return ONLY a JSON object with:
            {
                "age": "young|middle-aged|elderly",
                "tone": "warm|professional|friendly|authoritative|casual",
                "mood": "cheerful|serious|calm|energetic|neutral",
                "use_case": "audiobook|commercial|educational|character|narrator",
                "accent": "american|british|neutral|other",
                "gender_perception": "masculine|feminine|neutral"
            }
            """
            
            response = self.model.generate_content([prompt, {"mime_type": "audio/mp3", "data": audio_data}])
            return json.loads(response.text)
            
        except Exception as e:
            logger.error(f"Gemini analysis failed for {voice_name}: {e}")
            return self._get_fallback_analysis(voice_name)

    def _get_fallback_analysis(self, voice_name: str) -> Dict:
        """Basic analysis based on voice name patterns"""
        analysis = {
            "age": "middle-aged",
            "tone": "professional", 
            "mood": "neutral",
            "use_case": "audiobook",
            "accent": "neutral",
            "gender_perception": "neutral"
        }
        
        # Basic pattern matching
        if "young" in voice_name.lower():
            analysis["age"] = "young"
        if "standard" in voice_name.lower():
            analysis["tone"] = "professional"
        if "wavenet" in voice_name.lower():
            analysis["tone"] = "warm"
            
        return analysis