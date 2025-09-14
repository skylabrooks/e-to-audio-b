import asyncio
import base64
import concurrent.futures
import json
import logging
import os
from typing import Any, Dict, List

from google.cloud import texttospeech
from google.oauth2 import service_account

try:
    from core.credentials import get_credentials
except ImportError:
    from credentials import get_credentials

logger = logging.getLogger(__name__)


class TTSService:
    def __init__(self, max_workers=4):
        self._client = None
        self.max_workers = max_workers
        self._voices_cache = None
        self._cache_timestamp = None
        self._cache_ttl = 3600  # 1 hour

    @property
    def client(self):
        if self._client is None:
            self._client = self._get_tts_client()
        return self._client
    
    def _is_client_available(self):
        return self.client is not None

    def _get_tts_client(self):
        try:
            creds = get_credentials()
            if creds:
                credentials = service_account.Credentials.from_service_account_info(
                    creds
                )
                # Add retry configuration for network issues
                import google.api_core.retry as retry
                client = texttospeech.TextToSpeechClient(
                    credentials=credentials,
                    client_options={"api_endpoint": "texttospeech.googleapis.com:443"}
                )
                logger.info("TTS client initialized from service account")
                return client
        except Exception as e:
            logger.warning("Credentials helper failed: %s; falling back to mock", e)
            return None

        try:
            client = texttospeech.TextToSpeechClient()
            logger.info("TTS client initialized using ADC")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize TTS client: {e}")
            return None

    def list_voices(
        self,
        page: int = 1,
        per_page: int = 100,
        language: str = None,
        gender: str = None,
        q: str = None,
        language_filter: str = None
    ):
        try:
            # Check if client is available
            if not self._is_client_available():
                logger.warning("TTS client not available, using mock voices")
                return self._get_mock_voices(language or language_filter)
            
            # Check cache first
            import time
            current_time = time.time()
            if (self._voices_cache is None or 
                self._cache_timestamp is None or 
                current_time - self._cache_timestamp > self._cache_ttl):
                
                try:
                    # Fetch only English voices from Google Cloud TTS API
                    response = self.client.list_voices(language_code="en", timeout=10)
                    english_voices = [self._process_voice(voice) for voice in response.voices 
                                    if any("en" in code for code in voice.language_codes)]
                    self._voices_cache = english_voices
                    self._cache_timestamp = current_time
                    logger.info(f"Fetched {len(self._voices_cache)} English voices from TTS API")
                except Exception as api_error:
                    logger.error(f"TTS API call failed: {api_error}")
                    return self._get_mock_voices("en")
            
            voices = self._voices_cache.copy()
            
            # Apply filters (voices are already English-only)
            if gender:
                voices = [v for v in voices if v["ssml_gender"].upper() == gender.upper()]
            
            if q:
                voices = [v for v in voices if q.lower() in v["name"].lower()]
            
            # Apply pagination
            start = (page - 1) * per_page
            end = start + per_page
            return voices[start:end]
            
        except Exception as e:
            logger.error(f"Error fetching voices: {e}")
            return self._get_mock_voices("en")

    def synthesize_speech(self, text, voice_name, language_code):
        try:
            if not self._is_client_available():
                logger.error("TTS client not available for synthesis")
                raise Exception("TTS service unavailable")
            
            synthesis_input = texttospeech.SynthesisInput(text=text)

            # Validate and fix voice/language combination
            if not voice_name or "Standard" not in voice_name:
                voice_name = "en-US-Standard-A"
                language_code = "en-US"
            
            if not language_code:
                language_code = "en-US"

            voice = texttospeech.VoiceSelectionParams(
                name=voice_name, language_code=language_code
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
                timeout=30
            )

            return base64.b64encode(response.audio_content).decode("utf-8")
        except Exception as e:
            logger.error(f"TTS synthesis error: {e}")
            raise

    def _process_voice(self, voice):
        return {
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": (texttospeech.SsmlVoiceGender(voice.ssml_gender).name),
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        }

    def _get_mock_voices(self, lang_filter=None):
        all_mock_voices = [
            {
                "name": "en-US-Standard-A",
                "language_codes": ["en-US"],
                "ssml_gender": "FEMALE",
                "natural_sample_rate_hertz": 24000,
            },
            {
                "name": "en-US-Standard-B",
                "language_codes": ["en-US"],
                "ssml_gender": "MALE",
                "natural_sample_rate_hertz": 24000,
            },
            {
                "name": "en-US-Standard-C",
                "language_codes": ["en-US"],
                "ssml_gender": "FEMALE",
                "natural_sample_rate_hertz": 24000,
            },
            {
                "name": "en-US-Standard-D",
                "language_codes": ["en-US"],
                "ssml_gender": "MALE",
                "natural_sample_rate_hertz": 24000,
            },
        ]

        if lang_filter:
            return [
                v
                for v in all_mock_voices
                if any(lang_filter in code for code in v["language_codes"])
            ]
        return all_mock_voices

    async def process_segments_async(
        self, segments: List[Dict], voice_mapping: Dict[str, Any]
    ) -> List[Dict]:
        """Process multiple audio segments concurrently"""
        loop = asyncio.get_event_loop()

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            tasks = []

            for segment in segments:
                role = segment.get("role", "")
                text = segment.get("text", "")

                if not role or not text or role not in voice_mapping:
                    continue

                voice_info = voice_mapping[role]
                voice_name = voice_info.get("voiceName")
                language_code = voice_info.get("languageCode")

                if not voice_name or not language_code:
                    continue

                task = loop.run_in_executor(
                    executor,
                    self.synthesize_speech,
                    text,
                    voice_name,
                    language_code,
                )
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            audio_segments = []
            for i, result in enumerate(results):
                if isinstance(result, str):  # Base64 audio data
                    segment = segments[i].copy()
                    segment["audio"] = result
                    audio_segments.append(segment)
                elif isinstance(result, Exception):
                    logger.error(f"Async processing error: {result}")

            return audio_segments
