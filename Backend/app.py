from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import texttospeech
import os
import re
import base64
import logging
import json
from dotenv import load_dotenv
from credentials import get_credentials

app = Flask(__name__)
CORS(app)
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_speaker_roles(content):
    """Extract speaker roles from markdown content."""
    pattern = r'\*\*(.*?):\*\*'
    roles = set(re.findall(pattern, content))
    return list(roles)

def parse_content_by_role(content):
    """Parse content into segments by speaker role."""
    segments = []
    lines = content.split('\n')
    current_role = None
    current_text = []
    
    for line in lines:
        role_match = re.match(r'\*\*(.*?):\*\*', line)
        if role_match:
            # Save previous segment if exists
            if current_role and current_text:
                segments.append({
                    'role': current_role,
                    'text': ' '.join(current_text).strip()
                })
            current_role = role_match.group(1)
            current_text = [line[len(role_match.group(0)):].strip()]
        elif line.strip() and current_role:
            current_text.append(line.strip())
    
    # Add final segment
    if current_role and current_text:
        segments.append({
            'role': current_role,
            'text': ' '.join(current_text).strip()
        })
    
    return segments

@app.route('/api/detect-roles', methods=['POST'])
def detect_roles():
    """Endpoint to detect speaker roles in uploaded content."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    content = file.read().decode('utf-8')
    roles = detect_speaker_roles(content)
    segments = parse_content_by_role(content)
    
    return jsonify({
        'roles': roles,
        'segments': segments
    })

@app.route('/api/voices', methods=['GET'])
def list_voices():
    """Endpoint to list available Google Cloud TTS voices."""
    # Initialize client using provided credentials if available to avoid ADC/quota issues
    creds = None
    try:
        creds = get_credentials()
    except Exception:
        logger.warning('get_credentials() raised an exception; falling back to ADC')

    if creds:
        client = texttospeech.TextToSpeechClient.from_service_account_info(creds)
        logger.info('Initialized TTS client from service account info')
    else:
        client = texttospeech.TextToSpeechClient()
        logger.info('Initialized TTS client using Application Default Credentials')

    response = client.list_voices()
    voices = []
    
    for voice in response.voices:
        voices.append({
            'name': voice.name,
            'language_codes': voice.language_codes,
            'ssml_gender': texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            'natural_sample_rate_hertz': voice.natural_sample_rate_hertz
        })
    
    return jsonify(voices)

@app.route('/api/synthesize', methods=['POST'])
def synthesize_speech():
    """Endpoint to convert text to speech using selected voices."""
    try:
        data = request.json
        # Initialize client using provided credentials if available
        creds = None
        try:
            creds = get_credentials()
        except Exception:
            logger.warning('get_credentials() raised an exception; falling back to ADC')

        if creds:
            client = texttospeech.TextToSpeechClient.from_service_account_info(creds)
            logger.info('Initialized TTS client from service account info')
        else:
            client = texttospeech.TextToSpeechClient()
            logger.info('Initialized TTS client using Application Default Credentials')
        
        segments = data.get('segments', [])
        voice_mapping = data.get('voiceMapping', {})
        
        audio_segments = []
        
        for segment in segments:
            role = segment['role']
            text = segment['text']
            voice_name = voice_mapping.get(role)
            
            if not voice_name:
                continue
                
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                name=voice_name,
                language_code='en-US'  # Assuming English for now
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Convert binary audio content to base64
            audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
            
            audio_segments.append({
                'role': role,
                'audio': audio_base64
            })
        
        return jsonify({'audio_segments': audio_segments})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
