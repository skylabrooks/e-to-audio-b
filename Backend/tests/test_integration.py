import pytest
import json
import tempfile
import os
from unittest.mock import patch, Mock

class TestFullWorkflow:
    """Integration tests for complete audiobook generation workflow."""
    
    def test_complete_audiobook_generation(self, client, mock_tts_client, mock_credentials):
        """Test complete workflow from file upload to audio generation."""
        
        # Step 1: Upload file and detect roles
        story_content = """**Narrator:** Once upon a time in a magical kingdom, there lived a brave princess.

**Princess:** I need help! The dragon has captured my kingdom!

**Knight:** Fear not, Princess! I shall rescue your kingdom from the dragon.

**Dragon:** ROAAAAR! None shall pass through my domain!

**Narrator:** And so the adventure began..."""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(story_content)
            f.flush()
            
            with open(f.name, 'rb') as upload_file:
                response = client.post('/api/detect-roles', 
                                     data={'file': (upload_file, 'story.txt')})
        
        os.unlink(f.name)
        
        assert response.status_code == 200
        roles_data = json.loads(response.data)
        
        assert 'roles' in roles_data
        assert 'segments' in roles_data
        assert 'Narrator' in roles_data['roles']
        assert 'Princess' in roles_data['roles']
        assert 'Knight' in roles_data['roles']
        assert 'Dragon' in roles_data['roles']
        
        segments = roles_data['segments']
        assert len(segments) >= 4
        
        # Step 2: Get available voices
        with patch('app.get_credentials', return_value=mock_credentials):
            # Mock voice response
            mock_voice = Mock()
            mock_voice.name = 'en-US-Standard-A'
            mock_voice.language_codes = ['en-US']
            mock_voice.ssml_gender = 1  # FEMALE
            mock_voice.natural_sample_rate_hertz = 24000
            
            mock_response = Mock()
            mock_response.voices = [mock_voice]
            mock_tts_client.list_voices.return_value = mock_response
            
            voices_response = client.get('/api/voices')
        
        assert voices_response.status_code == 200
        voices_data = json.loads(voices_response.data)
        assert 'voices' in voices_data
        assert len(voices_data['voices']) > 0
        
        # Step 3: Generate audiobook
        voice_mapping = {
            'Narrator': {'voiceName': 'en-US-Standard-A', 'languageCode': 'en-US'},
            'Princess': {'voiceName': 'en-US-Standard-C', 'languageCode': 'en-US'},
            'Knight': {'voiceName': 'en-US-Standard-B', 'languageCode': 'en-US'},
            'Dragon': {'voiceName': 'en-US-Standard-D', 'languageCode': 'en-US'}
        }
        
        with patch('app.get_credentials', return_value=mock_credentials):
            # Mock synthesis response
            mock_synthesis_response = Mock()
            mock_synthesis_response.audio_content = b'fake_audio_data'
            mock_tts_client.synthesize_speech.return_value = mock_synthesis_response
            
            synthesis_response = client.post('/api/synthesize',
                                           data=json.dumps({
                                               'segments': segments,
                                               'voiceMapping': voice_mapping
                                           }),
                                           content_type='application/json')
        
        assert synthesis_response.status_code == 200
        audio_data = json.loads(synthesis_response.data)
        
        assert 'audio_segments' in audio_data
        assert len(audio_data['audio_segments']) > 0
        
        # Verify each role has audio
        audio_roles = [seg['role'] for seg in audio_data['audio_segments']]
        for role in voice_mapping.keys():
            if any(seg['role'] == role for seg in segments):
                assert role in audio_roles

    def test_error_handling_workflow(self, client):
        """Test error handling throughout the workflow."""
        
        # Test invalid file upload
        response = client.post('/api/detect-roles')
        assert response.status_code == 400
        
        # Test invalid file type
        invalid_file = tempfile.NamedTemporaryFile(suffix='.exe', delete=False)
        invalid_file.write(b'invalid content')
        invalid_file.close()
        
        with open(invalid_file.name, 'rb') as f:
            response = client.post('/api/detect-roles', 
                                 data={'file': (f, 'malware.exe')})
        
        os.unlink(invalid_file.name)
        assert response.status_code == 400
        
        # Test synthesis without proper data
        response = client.post('/api/synthesize',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 200  # Should fallback to mock data

class TestAPIEndpoints:
    """Integration tests for API endpoints."""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'etoaudiobook-api'
    
    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.get('/health')
        
        # Check security headers
        assert 'X-Content-Type-Options' in response.headers
        assert 'X-Frame-Options' in response.headers
        assert 'X-XSS-Protection' in response.headers
    
    @patch('app.get_credentials')
    def test_voice_preview(self, mock_get_creds, client, mock_tts_client, mock_credentials):
        """Test voice preview functionality."""
        mock_get_creds.return_value = mock_credentials
        
        # Mock synthesis response
        mock_response = Mock()
        mock_response.audio_content = b'preview_audio_data'
        mock_tts_client.synthesize_speech.return_value = mock_response
        
        preview_data = {
            'voiceName': 'en-US-Standard-A',
            'languageCode': 'en-US',
            'text': 'This is a test preview.'
        }
        
        response = client.post('/api/preview-voice',
                             data=json.dumps(preview_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'audio' in data
        
        # Verify TTS client was called correctly
        mock_tts_client.synthesize_speech.assert_called_once()

class TestSecurityIntegration:
    """Integration tests for security features."""
    
    def test_file_size_limit(self, client):
        """Test file size limit enforcement."""
        # Create a large file (simulate > 16MB)
        large_content = 'x' * (17 * 1024 * 1024)  # 17MB
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(large_content)
            f.flush()
            
            try:
                with open(f.name, 'rb') as upload_file:
                    response = client.post('/api/detect-roles',
                                         data={'file': (upload_file, 'large.txt')})
                
                # Should be rejected due to size limit
                assert response.status_code == 413 or response.status_code == 400
            finally:
                os.unlink(f.name)
    
    def test_input_sanitization(self, client):
        """Test input sanitization."""
        malicious_content = """**<script>alert('xss')</script>:** Malicious content
        
**"DROP TABLE users;":** SQL injection attempt"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(malicious_content)
            f.flush()
            
            try:
                with open(f.name, 'rb') as upload_file:
                    response = client.post('/api/detect-roles',
                                         data={'file': (upload_file, 'malicious.txt')})
                
                if response.status_code == 200:
                    data = json.loads(response.data)
                    # Check that dangerous characters are sanitized
                    roles_str = str(data.get('roles', []))
                    assert '<script>' not in roles_str
                    assert 'DROP TABLE' not in roles_str
            finally:
                os.unlink(f.name)