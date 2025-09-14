import logging

from flask import Blueprint, jsonify, request

from services.content_parser import ContentParser

# from services.openai_tts_service import OpenAITTSService
from services.tts_service import TTSService
from services.validation import ValidationService
try:
    from services.voice_tagger import VoiceTagger
except ImportError:
    VoiceTagger = None

try:
    from utils.cache import cached
except ImportError:
    def cached(ttl=3600, key_prefix=""):
        def decorator(func):
            return func
        return decorator

try:
    from utils.performance import measure_time
except ImportError:
    def measure_time(name):
        def decorator(func):
            return func
        return decorator

logger = logging.getLogger(__name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")

tts_service = TTSService()
content_parser = ContentParser()
validation_service = ValidationService()

# Initialize OpenAI service lazily
openai_tts_service = None


def get_openai_service():
    return None  # Temporarily disabled


@api_bp.route("/detect-roles", methods=["POST"])
def detect_roles():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        is_valid, error_msg = validation_service.validate_file_upload(file)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        try:
            content = file.read().decode("utf-8")
        except UnicodeDecodeError:
            return jsonify({"error": "File must be valid UTF-8 text"}), 400

        content = content_parser.sanitize_text_input(content)
        if not content:
            return jsonify({"error": "File content is empty or invalid"}), 400

        segments, roles = content_parser.parse_content_and_roles(content)
        return jsonify({"roles": roles, "segments": segments})

    except Exception as e:
        logger.error(f"Error in detect_roles: {e}")
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route("/voices", methods=["GET"])
def list_voices():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 100))
        gender = request.args.get("gender")
        q = request.args.get("q")

        # Fetch English voices only
        voices = tts_service.list_voices(
            page=page,
            per_page=per_page,
            language="en",
            gender=gender,
            q=q,
        )
        return jsonify({"voices": voices})
    except Exception as e:
        logger.error(f"TTS API error in /api/voices: {e}")
        return jsonify({"error": "Failed to retrieve voices."}), 500


@api_bp.route("/voices/all", methods=["GET"])
def list_all_voices():
    try:
        voices = sorted(tts_service.list_voices(language="en"), key=lambda x: x["name"])
        return jsonify({"voices": voices})
    except Exception as e:
        logger.error(f"TTS API error in /api/voices/all: {e}")
        mock_voices = tts_service._get_mock_voices("en")
        return jsonify({"voices": mock_voices})


@api_bp.route("/voices/tagged", methods=["GET"])
def list_tagged_voices():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 100))
        gender = request.args.get("gender")
        q = request.args.get("q")

        voices = tts_service.list_voices(
            page=page,
            per_page=per_page,
            language="en",
            gender=gender,
            q=q,
        )

        return jsonify(
            {
                "voices": voices,
                "total": len(voices),
                "filters_applied": {
                    "language": "en",
                    "gender": gender,
                    "q": q,
                },
            }
        )

    except Exception as e:
        logger.error(f"Error in tagged voices: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/languages", methods=["GET"])
def get_available_languages():
    # Only return English since we're limiting to English voices only
    return jsonify({"languages": [{"code": "en", "name": "English"}]})


@api_bp.route("/voices/by-language/<language_code>", methods=["GET"])
def get_voices_by_language(language_code):
    try:
        # Get voices filtered by language
        voices = tts_service.list_voices(language_filter=language_code)

        # Add OpenAI voices for English
        if language_code == "en":
            openai_service = get_openai_service()
            if openai_service:
                voices.extend(openai_service.list_voices())

        return jsonify(
            {"voices": voices, "language": language_code, "total": len(voices)}
        )

    except Exception as e:
        logger.error(f"Error getting voices for language {language_code}: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/voices/filter-options", methods=["GET"])
def get_voice_filter_options():
    try:
        return jsonify({
            "genders": ["MALE", "FEMALE"],
            "qualities": ["Standard", "Wavenet", "Neural2"],
            "regions": ["US", "GB", "AU"]
        })
    except Exception as e:
        logger.error(f"Error getting filter options: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/preview-voice", methods=["POST"])
def preview_voice():
    try:
        data = request.json
        voice_name = data.get("voiceName")
        language_code = data.get("languageCode")
        sample_text = content_parser.sanitize_text_input(
            data.get("text", "Hello, this is a voice preview.")
        )
        if len(sample_text) > 500:
            sample_text = sample_text[:500]

        if not voice_name:
            return jsonify({"error": "Voice name required"}), 400

        # Use OpenAI TTS for openai- prefixed voices
        if voice_name.startswith("openai-"):
            openai_service = get_openai_service()
            if openai_service:
                audio_base64 = openai_service.synthesize_speech(sample_text, voice_name)
            else:
                return (
                    jsonify({"error": "OpenAI TTS service not available"}),
                    500,
                )
        else:
            audio_base64 = tts_service.synthesize_speech(
                sample_text, voice_name, language_code
            )

        return jsonify({"audio": audio_base64})

    except Exception as e:
        logger.error(f"Voice preview error: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/synthesize", methods=["POST"])
def synthesize_speech():
    try:
        data = request.json
        segments = data.get("segments", [])
        voice_mapping = data.get("voiceMapping", {})

        if not segments:
            return jsonify({"error": "No segments provided"}), 400

        if not voice_mapping:
            return jsonify({"error": "No voice mapping provided"}), 400

        audio_segments = []

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

            try:
                audio_base64 = tts_service.synthesize_speech(
                    text, voice_name, language_code
                )

                audio_segments.append(
                    {"role": role, "text": text, "audio": audio_base64}
                )

            except Exception as e:
                logger.error(f"Error synthesizing speech for role {role}: {e}")
                continue

        return jsonify({"audioSegments": audio_segments})

    except Exception as e:
        logger.error(f"Error in synthesize_speech: {e}")
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route("/synthesize-single", methods=["POST"])
def synthesize_single():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        is_valid, error_msg = validation_service.validate_file_upload(file)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        try:
            content = file.read().decode("utf-8")
        except UnicodeDecodeError:
            return jsonify({"error": "File must be valid UTF-8 text"}), 400

        content = content_parser.sanitize_text_input(content)
        if not content:
            return jsonify({"error": "File content is empty or invalid"}), 400

        # For single narrator, use the first available voice
        voices = tts_service.list_voices(language_filter="en")
        if not voices:
            return jsonify({"error": "No voices available"}), 500

        default_voice = voices[0]["name"]
        language_code = voices[0].get("language_codes", ["en-US"])[0]

        # Generate audio for entire content
        audio_base64 = tts_service.synthesize_speech(
            content, default_voice, language_code
        )

        return jsonify(
            {
                "audio": audio_base64,
                "text": content,
                "voice": default_voice,
            }
        )

    except Exception as e:
        logger.error(f"Error in synthesize_single: {e}")
        return jsonify({"error": str(e)}), 500
