import pytest
import json
import base64
from unittest.mock import patch, Mock
from io import BytesIO

class TestHealthEndpoint:
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'etoaudiobook-api'

class TestDetectRoles:
    def test_detect_roles_success(self, client, sample_text_file):
        """Test successful role detection."""
        with open(sample_text_file, 'rb') as f:
            response = client.post('/api/detect-roles', 
                                 data={'file': (f, 'test.txt')})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'roles' in data
        assert 'segments' in data
        assert 'Narrator' in data['roles']
        assert 'Princess' in data['roles']

    def test_detect_roles_no_file(self, client):
        """Test role detection without file."""
        response = client.post('/api/detect-roles')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_detect_roles_invalid_file_type(self, client):
        """Test role detection with invalid file type."""
        data = {'file': (BytesIO(b'test'), 'test.exe')}
        response = client.post('/api/detect-roles', data=data)
        assert response.status_code == 400

    def test_detect_roles_empty_file(self, client):
        """Test role detection with empty file."""
        data = {'file': (BytesIO(b''), 'test.txt')}
        response = client.post('/api/detect-roles', data=data)
        assert response.status_code == 400

class TestVoicesEndpoint:
    @patch('app.get_credentials')
    def test_list_voices_success(self, mock_get_creds, client, mock_tts_client, mock_credentials):
        """Test successful voice listing."""
        mock_get_creds.return_value = mock_credentials
        
        # Mock voice response
        mock_voice = Mock()
        mock_voice.name = 'en-US-Standard-A'
        mock_voice.language_codes = ['en-US']
        mock_voice.ssml_gender = 1  # FEMALE
        mock_voice.natural_sample_rate_hertz = 24000
        
        mock_response = Mock()
        mock_response.voices = [mock_voice]
        mock_tts_client.list_voices.return_value = mock_response
        
        response = client.get('/api/voices')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'voices' in data
        assert len(data['voices']) > 0

    @patch('app.get_credentials')
    def test_list_voices_fallback(self, mock_get_creds, client):
        """Test voice listing fallback to mock data."""
        mock_get_creds.side_effect = Exception("API Error")
        
        response = client.get('/api/voices')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'voices' in data
        assert len(data['voices']) > 0

class TestPreviewVoice:
    @patch('app.get_credentials')
    def test_preview_voice_success(self, mock_get_creds, client, mock_tts_client, mock_credentials):
        """Test successful voice preview."""
        mock_get_creds.return_value = mock_credentials
        
        # Mock synthesis response
        mock_response = Mock()
        mock_response.audio_content = b'fake_audio_data'
        mock_tts_client.synthesize_speech.return_value = mock_response
        
        data = {
            'voiceName': 'en-US-Standard-A',
            'languageCode': 'en-US',
            'text': 'Hello world'
        }
        
        response = client.post('/api/preview-voice', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'audio' in response_data

    def test_preview_voice_missing_params(self, client):
        """Test voice preview with missing parameters."""
        data = {'voiceName': 'en-US-Standard-A'}
        
        response = client.post('/api/preview-voice',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400

class TestSynthesizeSpeech:
    @patch('app.get_credentials')
    def test_synthesize_success(self, mock_get_creds, client, mock_tts_client, mock_credentials):
        """Test successful speech synthesis."""
        mock_get_creds.return_value = mock_credentials
        
        # Mock synthesis response
        mock_response = Mock()
        mock_response.audio_content = b'fake_audio_data'
        mock_tts_client.synthesize_speech.return_value = mock_response
        
        data = {
            'segments': [
                {'role': 'Narrator', 'text': 'Once upon a time...'}
            ],
            'voiceMapping': {
                'Narrator': {
                    'voiceName': 'en-US-Standard-A',
                    'languageCode': 'en-US'
                }
            }
        }
        
        response = client.post('/api/synthesize',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'audio_segments' in response_data

    @patch('app.get_credentials')
    def test_synthesize_fallback(self, mock_get_creds, client):
        """Test synthesis fallback to mock data."""
        mock_get_creds.side_effect = Exception("API Error")
        
        data = {
            'segments': [
                {'role': 'Narrator', 'text': 'Once upon a time...'}
            ],
            'voiceMapping': {
                'Narrator': {
                    'voiceName': 'en-US-Standard-A',
                    'languageCode': 'en-US'
                }
            }
        }
        
        response = client.post('/api/synthesize',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200

class TestRateLimiting:
    def test_rate_limiting(self, client):
        """Test rate limiting on endpoints."""
        # Make multiple requests to trigger rate limit
        for _ in range(15):  # Exceed 10 per minute limit
            response = client.post('/api/detect-roles')
        
        # Should get rate limited
        assert response.status_code == 429

class TestSecurityHeaders:
    def test_security_headers(self, client):
        """Test security headers are present."""
        response = client.get('/health')
        
        assert 'X-Content-Type-Options' in response.headers
        assert 'X-Frame-Options' in response.headers
        assert 'X-XSS-Protection' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'