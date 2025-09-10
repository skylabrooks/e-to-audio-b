from sympy import python
python
import os
import json
import logging
from dotenv import load_dotenv
from google.cloud import secretmanager

load_dotenv()
logger = logging.getLogger(__name__)

def get_credentials():
    """Retrieve Google Cloud credentials."""
    key_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if key_path:
        try:
            if not os.path.isabs(key_path):
                key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', key_path))
            if os.path.exists(key_path):
                with open(key_path, 'r', encoding='utf-8') as f:
                    logger.info(f"Loading service account from file: {key_path}")
                    return json.load(f)
            else:
                logger.warning(f"GOOGLE_APPLICATION_CREDENTIALS is set but file not found: {key_path}")
        except Exception as e:
            logger.error(f"Failed to load credentials file {key_path}: {e}")

    try:
        client = secretmanager.SecretManagerServiceClient()
        name = os.environ.get('TTS_CREDENTIALS_SECRET_NAME', 'projects/e-to-audio-book/secrets/tts-credentials/versions/latest')
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode('utf-8')
        logger.info("Loaded service account from Secret Manager")
        return json.loads(payload)
    except Exception as e:
        logger.error(f"Could not load credentials from Secret Manager: {e}")

    return None
