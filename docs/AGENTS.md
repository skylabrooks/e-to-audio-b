# AGENTS.md

## Build/Lint/Test Commands
- **Frontend**: `cd Frontend && npm start` (dev), `npm run build`, `npm test`
- **Backend**: `cd Backend && python app.py` (dev), `pip install -r requirements.txt`
- **Single test**: `cd Frontend && npm test -- --testNamePattern="TestName"`

## Architecture & Structure
- **Fullstack app**: React frontend + Flask backend for text-to-speech audiobook generation
- **Backend** (`Backend/`): Flask API with Google Cloud TTS integration, handles role detection & speech synthesis
- **Frontend** (`Frontend/`): React app with file upload, voice assignment, and audio playback
- **Key APIs**: `/api/detect-roles` (POST), `/api/voices` (GET), `/api/synthesize` (POST)
- **Database**: None (stateless API)

## Code Style Guidelines
- **Python**: Snake_case functions/variables, PascalCase classes, Google Cloud TTS patterns
- **JavaScript/React**: CamelCase, functional components with hooks, destructured props
- **Imports**: Grouped (external, internal, relative), React imports first
- **Error handling**: Try/catch with JSON error responses, logging with Python `logging` module
- **Files**: `.env` for secrets (use `get_credentials()` from `credentials.py`)
- **Formatting**: Standard React/Python conventions, no specific linter config found
