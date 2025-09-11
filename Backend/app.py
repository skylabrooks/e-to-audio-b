import base64
import logging
import os
import re

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS  # type: ignore
from flask_limiter import Limiter  # type: ignore
from flask_limiter.util import get_remote_address  # type: ignore
from google.cloud import texttospeech
from werkzeug.utils import secure_filename

from cache import cache, cached
from config import config
from credentials import get_credentials
from logging_config import setup_logging
from performance import measure_time, monitor, track_request_metrics

load_dotenv()
setup_logging()

app = Flask(__name__)

# Load configuration
config_name = os.environ.get("FLASK_ENV", "development")
app.config.from_object(config[config_name])

# CORS configuration
CORS(app, origins=["http://localhost", "http://localhost:80", "http://localhost:3000"], supports_credentials=True)

# Rate limiting with Redis
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"],
    storage_uri=app.config.get("RATELIMIT_STORAGE_URL"),
)

# Get logger
logger = logging.getLogger(__name__)

# Setup performance monitoring
before_request_handler, after_request_handler = track_request_metrics()
app.before_request(before_request_handler)
app.after_request(after_request_handler)


# Security headers
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# Input validation helpers
def validate_file_upload(file):
    """Validate uploaded file."""
    if not file or file.filename == "":
        return False, "No file selected"

    filename = secure_filename(file.filename)
    if not filename.lower().endswith((".txt", ".md")):
        return False, "Only .txt and .md files are allowed"

    return True, None


def sanitize_text_input(text):
    """Sanitize text input to prevent injection attacks."""
    if not isinstance(text, str):
        return ""

    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', "", text)
    # Limit length
    return sanitized[:10000]  # Max 10k characters


# TTS client and data helpers
def get_tts_client():
    """Initializes and returns a TextToSpeechClient."""
    try:
        from google.oauth2 import service_account
        creds = get_credentials()
        if creds:
            credentials = service_account.Credentials.from_service_account_info(creds)
            client = texttospeech.TextToSpeechClient(credentials=credentials)
            logger.info("TTS client initialized from service account")
            return client
    except Exception as e:
        logger.warning(f"Credentials helper failed: {e}; falling back to ADC")

    # Fallback to Application Default Credentials (ADC)
    client = texttospeech.TextToSpeechClient()
    logger.info("TTS client initialized using ADC")
    return client


def get_mock_voices(lang_filter=None):
    """Returns a list of mock voices, optionally filtered by language."""
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
        {
            "name": "en-GB-Standard-A",
            "language_codes": ["en-GB"],
            "ssml_gender": "FEMALE",
            "natural_sample_rate_hertz": 24000,
        },
        {
            "name": "en-GB-Standard-B",
            "language_codes": ["en-GB"],
            "ssml_gender": "MALE",
            "natural_sample_rate_hertz": 24000,
        },
        {
            "name": "en-AU-Standard-A",
            "language_codes": ["en-AU"],
            "ssml_gender": "FEMALE",
            "natural_sample_rate_hertz": 24000,
        },
        {
            "name": "en-AU-Standard-B",
            "language_codes": ["en-AU"],
            "ssml_gender": "MALE",
            "natural_sample_rate_hertz": 24000,
        },
        {
            "name": "en-IN-Standard-A",
            "language_codes": ["en-IN"],
            "ssml_gender": "FEMALE",
            "natural_sample_rate_hertz": 24000,
        },
        {
            "name": "en-IN-Standard-B",
            "language_codes": ["en-IN"],
            "ssml_gender": "MALE",
            "natural_sample_rate_hertz": 24000,
        },
        {
            "name": "fr-FR-Standard-A",
            "language_codes": ["fr-FR"],
            "ssml_gender": "FEMALE",
            "natural_sample_rate_hertz": 24000,
        },
        {
            "name": "fr-FR-Standard-B",
            "language_codes": ["fr-FR"],
            "ssml_gender": "MALE",
            "natural_sample_rate_hertz": 24000,
        },
        {
            "name": "de-DE-Standard-A",
            "language_codes": ["de-DE"],
            "ssml_gender": "FEMALE",
            "natural_sample_rate_hertz": 24000,
        },
        {
            "name": "de-DE-Standard-B",
            "language_codes": ["de-DE"],
            "ssml_gender": "MALE",
            "natural_sample_rate_hertz": 24000,
        },
        {
            "name": "es-ES-Standard-A",
            "language_codes": ["es-ES"],
            "ssml_gender": "FEMALE",
            "natural_sample_rate_hertz": 24000,
        },
    ]
    if lang_filter:
        return [
            voice
            for voice in all_mock_voices
            if any(lang_filter in code for code in voice["language_codes"])
        ]
    return all_mock_voices


def _process_voice(voice):
    """Formats a voice object from the TTS API into a dictionary."""
    return {
        "name": voice.name,
        "language_codes": list(voice.language_codes),
        "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
        "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
    }


def parse_content_and_roles(content):
    """
    Parse content into segments by speaker role and extract all unique roles.
    Returns a tuple of (segments, roles).
    """
    segments = []
    roles = set()
    lines = content.split("\n")
    current_role = None
    current_text = []

    for line in lines:
        role_match = re.match(r"^\s*\*\*(.*?)\*\*", line)
        if role_match:
            # Save previous segment if it exists
            if current_role and current_text:
                segment = {
                    "role": current_role,
                    "text": " ".join(current_text).strip(),
                }
                segments.append(segment)

            # Start new segment
            current_role = role_match.group(1).strip()
            roles.add(current_role)
            # Get the text following the role marker.
            text_after_role = line[role_match.end() :].strip()
            current_text = [text_after_role] if text_after_role else []
        elif line.strip() and current_role:
            current_text.append(line.strip())

    # Add the final segment
    if current_role and current_text:
        final_segment = {
            "role": current_role,
            "text": " ".join(current_text).strip(),
        }
        segments.append(final_segment)

    return segments, list(roles)


@app.route("/api/detect-roles", methods=["POST"])
@limiter.limit("10 per minute")
def detect_roles():
    """Endpoint to detect speaker roles in uploaded content."""
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        is_valid, error_msg = validate_file_upload(file)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        try:
            content = file.read().decode("utf-8")
        except UnicodeDecodeError:
            return jsonify({"error": "File must be valid UTF-8 text"}), 400

        # Sanitize content
        content = sanitize_text_input(content)
        if not content:
            return jsonify({"error": "File content is empty or invalid"}), 400

        segments, roles = parse_content_and_roles(content)

        return jsonify({"roles": roles, "segments": segments})

    except Exception as e:
        logger.error(f"Error in detect_roles: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/voices", methods=["GET"])
@limiter.limit("30 per minute")
@cached(ttl=1800, key_prefix="voices")
@measure_time("api.list_voices")
def list_voices():
    """Endpoint to list available English Google Cloud TTS voices."""
    try:
        client = get_tts_client()
        response = client.list_voices()

        voices = [
            _process_voice(voice)
            for voice in response.voices
            if any("en" in lang for lang in voice.language_codes)
        ]

        return jsonify({"voices": voices})
    except Exception as e:
        logger.error(f"TTS API error in /api/voices: {e}")
        # Return mock voices for development
        mock_voices = get_mock_voices(lang_filter="en")
        return jsonify({"voices": mock_voices})


@app.route("/api/voices/all", methods=["GET"])
@limiter.limit("10 per minute")
@cached(ttl=3600, key_prefix="all_voices")
@measure_time("api.list_all_voices")
def list_all_voices():
    """Endpoint to list ALL available Google Cloud TTS voices."""
    try:
        client = get_tts_client()
        response = client.list_voices()

        voices = sorted(
            [_process_voice(voice) for voice in response.voices],
            key=lambda x: x["name"],
        )

        return jsonify({"voices": voices})
    except Exception as e:
        logger.error(f"TTS API error in /api/voices/all: {e}")
        # Return expanded mock voices for development
        mock_voices = get_mock_voices()
        return jsonify({"voices": mock_voices})


@app.route("/api/preview-voice", methods=["POST"])
@limiter.limit("20 per minute")
@measure_time("api.preview_voice")
def preview_voice():
    """Endpoint to preview a voice with sample text."""
    try:
        data = request.json
        voice_name = data.get("voiceName")
        language_code = data.get("languageCode")
        sample_text = sanitize_text_input(
            data.get("text", "Hello, this is a voice preview.")
        )
        if len(sample_text) > 500:  # Limit preview text length
            sample_text = sample_text[:500]

        logger.info(f"Voice preview for {voice_name} ({language_code})")

        if not voice_name or not language_code:
            return (
                jsonify({"error": "Voice name and language code required"}),
                400,
            )

        client = get_tts_client()

        synthesis_input = texttospeech.SynthesisInput(text=sample_text)
        
        # Use Standard voices for preview (they work without model names)
        if "Standard" not in voice_name:
            # Fallback to a basic Standard voice for preview
            voice_name = "en-US-Standard-A" if "en-US" in language_code else "en-GB-Standard-A"
            language_code = "en-US" if "en-US" in language_code else "en-GB"
        
        voice = texttospeech.VoiceSelectionParams(
            name=voice_name, language_code=language_code
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
        )

        audio_base64 = base64.b64encode(response.audio_content).decode("utf-8")
        logger.info("Successfully synthesized voice preview")
        return jsonify({"audio": audio_base64})

    except Exception as e:
        logger.error(f"Voice preview error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/synthesize", methods=["POST"])
@limiter.limit("5 per minute")
@measure_time("api.synthesize_speech")
def synthesize_speech():
    """Endpoint to convert text to speech using selected voices."""
    try:
        data = request.json
        segments = data.get("segments", [])
        voice_mapping = data.get("voiceMapping", {})

        try:
            client = get_tts_client()

            audio_segments = []

            for segment in segments:
                role = sanitize_text_input(segment.get("role", ""))
                text = sanitize_text_input(segment.get("text", ""))

                if not role or not text:
                    continue

                voice_info = voice_mapping.get(role)

                if not voice_info:
                    continue

                voice_name = voice_info.get("voiceName")
                language_code = voice_info.get("languageCode")

                if not voice_name or not language_code:
                    continue

                synthesis_input = texttospeech.SynthesisInput(text=text)
                voice = texttospeech.VoiceSelectionParams(
                    name=voice_name, language_code=language_code
                )
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3
                )

                response = client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice,
                    audio_config=audio_config,
                )

                # Convert binary audio content to base64
                audio_base64 = base64.b64encode(response.audio_content).decode("utf-8")

                audio_segments.append({"role": role, "audio": audio_base64})

            return jsonify({"audio_segments": audio_segments})

        except Exception as tts_error:
            logger.error(f"TTS API error: {tts_error}")
            # Return mock audio segments for development
            audio_segments = []
            for segment in segments:
                role = segment["role"]
                if role in voice_mapping:
                    audio_segments.append(
                        {
                            "role": role,
                            "audio": "mock-audio-data",  # Mock base64 audio
                        }
                    )
            return jsonify({"audio_segments": audio_segments})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({"status": "healthy", "service": "etoaudiobook-api"})


# Performance metrics endpoint
@app.route("/metrics", methods=["GET"])
def get_metrics():
    """Get performance metrics."""
    system_metrics = monitor.get_system_metrics()
    metrics_summary = monitor.get_metrics_summary()

    return jsonify(
        {
            "system": system_metrics,
            "application": metrics_summary,
            "cache_stats": {
                "enabled": cache.enabled,
                "redis_available": cache.redis_client is not None,
            },
        }
    )


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(
        debug=debug_mode,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
    )
