# AGENTS.md

## Build/Lint/Test Commands
- **Frontend**: `cd Frontend && npm start` (dev), `npm run build`, `npm test`
- **Backend**: `cd Backend && python app.py` (dev), `pip install -r requirements.txt`
- **Single test**: `cd Frontend && npm test -- --testNamePattern="TestName"`
- **Make commands**: `make run-all`, `make test`, `make format`, `make lint`, `make setup`
- **Backend test with coverage**: `cd Backend && pytest tests/ -v --cov=. --cov-report=term-missing`

## Architecture & Structure
- **Fullstack app**: React frontend + Flask backend for text-to-speech audiobook generation
- **Backend** (`Backend/`): Flask API with Google Cloud TTS integration, handles role detection & speech synthesis
- **Frontend** (`Frontend/`): React app with file upload, voice assignment, and audio playbook
- **Key APIs**: `/api/detect-roles` (POST), `/api/voices` (GET), `/api/synthesize` (POST)
- **Database**: None (stateless API)
- **Text Format**: Markdown pattern `**Character Name:** dialogue` for role detection

## Code Style Guidelines
- **Python**: Snake_case functions/variables, PascalCase classes, Black formatter (88 chars), type hints required
- **JavaScript/React**: CamelCase, functional components with hooks, destructured props, Prettier (2 spaces)
- **Imports**: Grouped (external, internal, relative), React imports first
- **Error handling**: Try/catch with JSON error responses, logging with Python `logging` module, specific exceptions
- **Files**: `.env` for secrets (use `get_credentials()` from `credentials.py`), never commit credentials
- **Security**: Environment variables only, validate all inputs, use Google Cloud service accounts
