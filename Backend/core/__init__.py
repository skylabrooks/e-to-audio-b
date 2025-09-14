import logging
import logging.config
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS  # type: ignore

from config import config

from routes.monitoring import monitoring_bp
from utils.cache import cache
from utils.performance import monitor, track_request_metrics


def setup_logging():
    """Configure application logging."""

    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]"
            },
            "simple": {"format": "%(levelname)s - %(message)s"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": f'logs/app_{datetime.now().strftime("%Y%m%d")}.log',
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": f'logs/error_{datetime.now().strftime("%Y%m%d")}.log',
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file", "error_file"],
                "level": log_level,
                "propagate": False,
            }
        },
    }

    logging.config.dictConfig(logging_config)


print(os.environ.get("OPENAI_API_KEY"))


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
setup_logging()

app = Flask(__name__)

# Load configuration
config_name = os.environ.get("FLASK_ENV", "development")
app.config.from_object(config[config_name])

# CORS configuration
CORS(
    app,
    origins=[
        "http://localhost",
        "http://localhost:80",
        "http://localhost:3000",
    ],
    supports_credentials=True,
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
