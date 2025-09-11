import asyncio
import concurrent.futures
import logging
from typing import List, Dict, Any
from google.cloud import texttospeech
import base64
from credentials import get_credentials

logger = logging.getLogger(__name__)

class AsyncAudioProcessor:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    
    async def synthesize_segment_async(self, segment: Dict[str, str], voice_info: Dict[str, str]) -> Dict[str, str]:
        """Synthesize a single audio segment asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, 
            self._synthesize_segment_sync, 
            segment, 
            voice_info
        )
    
    def _synthesize_segment_sync(self, segment: Dict[str, str], voice_info: Dict[str, str]) -> Dict[str, str]:
        """Synchronous audio synthesis for thread pool."""
        try:
            # Initialize TTS client
            creds = get_credentials()
            if creds:
                client = texttospeech.TextToSpeechClient.from_service_account_info(creds)
            else:
                client = texttospeech.TextToSpeechClient()
            
            # Prepare synthesis request
            synthesis_input = texttospeech.SynthesisInput(text=segment['text'])
            voice = texttospeech.VoiceSelectionParams(
                name=voice_info['voiceName'],
                language_code=voice_info['languageCode']
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0,
                pitch=0.0
            )
            
            # Synthesize speech
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Encode audio
            audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
            
            return {
                'role': segment['role'],
                'audio': audio_base64,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Audio synthesis error for {segment['role']}: {e}")
            return {
                'role': segment['role'],
                'audio': None,
                'status': 'error',
                'error': str(e)
            }
    
    async def synthesize_batch_async(self, segments: List[Dict], voice_mapping: Dict) -> List[Dict]:
        """Synthesize multiple segments concurrently."""
        tasks = []
        
        for segment in segments:
            role = segment.get('role')
            voice_info = voice_mapping.get(role)
            
            if voice_info:
                task = self.synthesize_segment_async(segment, voice_info)
                tasks.append(task)
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter successful results
        audio_segments = []
        for result in results:
            if isinstance(result, dict) and result.get('status') == 'success':
                audio_segments.append({
                    'role': result['role'],
                    'audio': result['audio']
                })
        
        return audio_segments
    
    def __del__(self):
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)

# Global processor instance
audio_processor = AsyncAudioProcessor()