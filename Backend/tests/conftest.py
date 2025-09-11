import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from app import app
from config import TestingConfig

@pytest.fixture
def client():
    """Create test client."""
    app.config.from_object(TestingConfig)
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def mock_tts_client():
    """Mock Google TTS client."""
    with patch('app.texttospeech.TextToSpeechClient') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        mock.from_service_account_info.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def sample_text_file():
    """Create sample text file for testing."""
    content = """**Narrator:** Once upon a time in a magical kingdom...

**Princess:** Help me, brave knight!

**Knight:** I shall save you, Princess!

**Dragon:** ROAAAAR! None shall pass!"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def mock_credentials():
    """Mock credentials."""
    return {
        "type": "service_account",
        "project_id": "test-project",
        "private_key": "test-key",
        "client_email": "test@test.iam.gserviceaccount.com"
    }