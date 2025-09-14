import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils.scheduler import initialize_scheduler

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

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

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[os.environ.get("RATE_LIMIT", "200 per hour")],
)

# Import and register blueprints after app creation to avoid circular imports
try:
    from routes.api_routes import api_bp
    from routes.monitoring import monitoring_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(monitoring_bp)
except Exception as e:
    print(f"Error importing routes: {e}")

    # Create minimal fallback routes
    @app.route("/api/languages")
    def fallback_languages():
        return jsonify({"languages": [{"code": "en", "name": "English"}]})

    @app.route("/api/voices")
    def fallback_voices():
        return jsonify(
            {"voices": [{"name": "en-US-Standard-A", "ssml_gender": "FEMALE"}]}
        )


# Health check endpoint
@app.route("/health", methods=["GET"])
@limiter.exempt
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({"status": "healthy", "service": "etoaudiobook-api"})


# Security headers
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


if __name__ == "__main__":
    initialize_scheduler()
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(
        debug=debug_mode,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
    )
