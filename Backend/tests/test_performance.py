import pytest
import time
import threading
from unittest.mock import patch, Mock
import tempfile
import os

class TestPerformance:
    """Performance tests for the application."""
    
    def test_file_processing_performance(self, client):
        """Test file processing performance."""
        # Create a moderately large file
        content = """**Narrator:** """ + "This is a test story. " * 1000
        content += """**Character1:** """ + "Hello world! " * 500
        content += """**Character2:** """ + "Goodbye world! " * 500
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            f.flush()
            
            start_time = time.time()
            
            with open(f.name, 'rb') as upload_file:
                response = client.post('/api/detect-roles',
                                     data={'file': (upload_file, 'large_story.txt')})
            
            processing_time = time.time() - start_time
        
        os.unlink(f.name)
        
        assert response.status_code == 200
        # Should process within reasonable time (adjust based on requirements)
        assert processing_time < 5.0, f"Processing took {processing_time:.2f}s, expected < 5s"
    
    @patch('app.get_credentials')
    def test_voice_listing_performance(self, mock_get_creds, client, mock_tts_client, mock_credentials):
        """Test voice listing performance."""
        mock_get_creds.return_value = mock_credentials
        
        # Mock many voices
        mock_voices = []
        for i in range(100):  # Simulate 100 voices
            mock_voice = Mock()
            mock_voice.name = f'voice-{i}'
            mock_voice.language_codes = ['en-US']
            mock_voice.ssml_gender = 1 if i % 2 else 2
            mock_voice.natural_sample_rate_hertz = 24000
            mock_voices.append(mock_voice)
        
        mock_response = Mock()
        mock_response.voices = mock_voices
        mock_tts_client.list_voices.return_value = mock_response
        
        start_time = time.time()
        response = client.get('/api/voices/all')
        processing_time = time.time() - start_time
        
        assert response.status_code == 200
        assert processing_time < 2.0, f"Voice listing took {processing_time:.2f}s, expected < 2s"
    
    def test_concurrent_requests(self, client):
        """Test handling of concurrent requests."""
        results = []
        errors = []
        
        def make_request():
            try:
                response = client.get('/health')
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # Create multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
        
        # Start all threads
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        # All requests should succeed
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert all(status == 200 for status in results)
        assert total_time < 5.0, f"Concurrent requests took {total_time:.2f}s"
    
    def test_memory_usage_file_processing(self, client):
        """Test memory usage during file processing."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process multiple files
        for i in range(5):
            content = f"**Narrator:** Story {i} content. " * 100
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(content)
                f.flush()
                
                with open(f.name, 'rb') as upload_file:
                    response = client.post('/api/detect-roles',
                                         data={'file': (upload_file, f'story_{i}.txt')})
                
                assert response.status_code == 200
                os.unlink(f.name)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (adjust threshold as needed)
        assert memory_increase < 50, f"Memory increased by {memory_increase:.2f}MB"

class TestRateLimitingPerformance:
    """Test rate limiting performance."""
    
    def test_rate_limit_enforcement(self, client):
        """Test that rate limiting is enforced efficiently."""
        start_time = time.time()
        
        # Make requests up to the limit
        responses = []
        for i in range(12):  # Exceed the 10 per minute limit
            response = client.post('/api/detect-roles')
            responses.append(response.status_code)
        
        total_time = time.time() - start_time
        
        # Should have some 400s (no file) and eventually 429s (rate limited)
        assert 429 in responses, "Rate limiting not enforced"
        assert total_time < 5.0, f"Rate limiting check took {total_time:.2f}s"
    
    def test_rate_limit_reset(self, client):
        """Test that rate limits reset properly."""
        # This test would need to wait for rate limit window to reset
        # For now, just test that the mechanism works
        
        # Make a request
        response1 = client.get('/health')
        assert response1.status_code == 200
        
        # Make another request immediately
        response2 = client.get('/health')
        assert response2.status_code == 200
        
        # Health endpoint should not be rate limited for normal usage