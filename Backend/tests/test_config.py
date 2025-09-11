import pytest
import os
from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig

class TestConfiguration:
    """Test configuration classes."""
    
    def test_base_config(self):
        """Test base configuration."""
        config = Config()
        
        assert hasattr(config, 'SECRET_KEY')
        assert hasattr(config, 'MAX_CONTENT_LENGTH')
        assert config.MAX_CONTENT_LENGTH == 16 * 1024 * 1024
    
    def test_development_config(self):
        """Test development configuration."""
        config = DevelopmentConfig()
        
        assert config.DEBUG is True
        assert config.FLASK_ENV == 'development'
    
    def test_production_config(self):
        """Test production configuration."""
        config = ProductionConfig()
        
        assert config.DEBUG is False
        assert config.FLASK_ENV == 'production'
        assert config.SESSION_COOKIE_SECURE is True
        assert config.SESSION_COOKIE_HTTPONLY is True
    
    def test_testing_config(self):
        """Test testing configuration."""
        config = TestingConfig()
        
        assert config.TESTING is True
        assert config.DEBUG is True
    
    def test_environment_variables(self):
        """Test configuration from environment variables."""
        with pytest.MonkeyPatch.context() as m:
            m.setenv('SECRET_KEY', 'test-secret')
            m.setenv('GOOGLE_PROJECT_ID', 'test-project')
            m.setenv('ALLOWED_ORIGINS', 'https://test.com,https://test2.com')
            
            config = Config()
            
            assert config.SECRET_KEY == 'test-secret'
            assert config.GOOGLE_PROJECT_ID == 'test-project'
            assert 'https://test.com' in config.ALLOWED_ORIGINS
            assert 'https://test2.com' in config.ALLOWED_ORIGINS