import os
import secrets
from typing import Any, Dict


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # Google Cloud
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")

    # CORS
    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost").split(",")

    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    FLASK_ENV = "development"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    FLASK_ENV = "production"

    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Enhanced caching
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT = 3600

    # Connection pooling
    REDIS_POOL_SIZE = 20
    REDIS_POOL_MAX_CONNECTIONS = 50

    # Rate limiting optimizations
    RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/1")
    RATELIMIT_STRATEGY = "moving-window"

    # Performance settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year cache for static files

    # Async processing
    ASYNC_WORKERS = int(os.environ.get("ASYNC_WORKERS", "4"))
    TTS_BATCH_SIZE = int(os.environ.get("TTS_BATCH_SIZE", "5"))

    # Compression
    COMPRESS_MIMETYPES = [
        "text/html",
        "text/css",
        "text/xml",
        "application/json",
        "application/javascript",
    ]


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True


config: Dict[str, Any] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
