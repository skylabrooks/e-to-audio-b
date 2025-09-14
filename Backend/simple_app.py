from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "etoaudiobook-api"})

@app.route('/api/languages')
def languages():
    return jsonify({
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"}
        ]
    })

@app.route('/api/voices/by-language/<language_code>')
def voices_by_language(language_code):
    voices = [
        {"name": "en-US-Standard-A", "ssml_gender": "FEMALE", "language_codes": ["en-US"]},
        {"name": "en-US-Standard-B", "ssml_gender": "MALE", "language_codes": ["en-US"]}
    ]
    return jsonify({"voices": voices})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)