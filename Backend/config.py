import os
from typing import Dict, Any

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Google Cloud
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_PROJECT_ID = os.environ.get('GOOGLE_PROJECT_ID')
    
    # CORS
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'http://localhost').split(',')
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

config: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}