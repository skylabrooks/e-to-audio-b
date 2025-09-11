# GitHub Copilot Instructions for EtoAudioBook

## Project Context
This is a React + Flask web application for converting text documents into multi-voice audiobooks using Google Cloud Text-to-Speech.

## Architecture
- **Frontend**: React app in `/Frontend` directory
- **Backend**: Flask API in `/Backend` directory  
- **TTS**: Google Cloud Text-to-Speech integration
- **File Structure**: Multi-voice audiobook generation with character role detection

## Code Style Guidelines

### Python (Backend)
- Use snake_case for functions and variables
- Use PascalCase for classes
- Follow Google Cloud TTS patterns
- Use Python type hints
- Handle errors with proper logging
- Use environment variables for secrets (never hardcode credentials)

### JavaScript/React (Frontend)
- Use camelCase naming convention
- Prefer functional components with hooks
- Use destructured props
- Follow React best practices
- Use async/await for API calls

### File Organization
- Keep backend logic in `/Backend`
- Keep frontend components in `/Frontend/src`
- Use relative imports within same directory
- Group imports: external libraries first, then internal modules

## Security Requirements
- Never commit credentials or API keys
- Use environment variables for all secrets
- Validate all user inputs
- Sanitize text content before processing
- Use proper error handling that doesn't expose internal details

## TTS Implementation Notes
- Role detection uses markdown pattern `**Character Name:**`
- Support multiple voice assignments per role
- Generate MP3 audio output
- Handle long text content with appropriate chunking
- Provide progress feedback for generation process

## Testing Approach
- Write unit tests for business logic
- Test TTS integration with mock data first
- Test role detection patterns thoroughly
- Include error handling test cases
- Test file upload and processing workflows

## API Patterns
- Use RESTful API design
- Return consistent JSON responses
- Include proper HTTP status codes
- Handle CORS for frontend-backend communication
- Implement proper error response formats

## Common Patterns to Suggest
- Environment variable loading with `python-dotenv`
- Flask route error handling decorators
- React component error boundaries
- Async state management for TTS generation
- File upload progress tracking
- Audio playback controls

## Avoid These Patterns
- Hardcoded API keys or credentials
- Blocking synchronous operations for TTS
- Missing error handling for API calls
- Direct file system access from frontend
- Unvalidated user inputs
- Missing CORS configuration

## Helpful Libraries Already in Use
- **Backend**: Flask, google-cloud-texttospeech, python-dotenv, flask-cors
- **Frontend**: React, axios (for API calls)
- **Testing**: pytest for backend, Jest for frontend

## Development Workflow
- Use `make run-all` to start both servers
- Backend runs on localhost:5000
- Frontend runs on localhost:3000  
- Use environment variables from `.env` files
- Follow the commands in Makefile for testing and linting
