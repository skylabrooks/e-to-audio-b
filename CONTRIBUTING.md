# Contributing to EtoAudioBook

Thank you for your interest in contributing to EtoAudioBook! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8 or higher
- Git

### Backend Setup
1. Navigate to the Backend directory:
   ```bash
   cd Backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install development dependencies:
   ```bash
   pip install black flake8 pytest pytest-cov mypy
   ```

### Frontend Setup
1. Navigate to the Frontend directory:
   ```bash
   cd Frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Install development dependencies:
   ```bash
   npm install --save-dev eslint prettier
   ```

## Code Style Guidelines

### Python (Backend)
- Follow PEP 8 style guide
- Use Black for code formatting (line length: 88)
- Use flake8 for linting
- Use type hints where appropriate
- Write docstrings for functions and classes

### JavaScript/React (Frontend)
- Use ESLint with the provided configuration
- Use Prettier for code formatting
- Follow React best practices
- Use functional components with hooks
- Write meaningful component and variable names

## Development Workflow

### Before Making Changes
1. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make sure all tools are working:
   ```bash
   # Backend
   cd Backend
   black --check .
   flake8 .
   pytest

   # Frontend
   cd Frontend
   npm run lint
   npm test
   ```

### Making Changes
1. Write your code following the style guidelines
2. Add tests for new functionality
3. Update documentation if needed
4. Run the linters and tests:
   ```bash
   # Backend
   black .
   flake8 .
   pytest

   # Frontend
   npm run lint:fix
   npm test
   ```

### Submitting Changes
1. Commit your changes with a clear message:
   ```bash
   git add .
   git commit -m "feat: add voice preview functionality"
   ```

2. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a pull request with:
   - Clear description of changes
   - Screenshots if UI changes
   - Test results

## Code Quality Tools

### Automated Formatting
- **Backend**: Black formatter (88 character line length)
- **Frontend**: Prettier with ESLint integration

### Linting
- **Backend**: flake8 with custom configuration
- **Frontend**: ESLint with React-specific rules

### Testing
- **Backend**: pytest with coverage reporting
- **Frontend**: Jest with React Testing Library

## Project Structure

```
EtoAudioBook/
├── Backend/                 # Flask API server
│   ├── app.py              # Main application
│   ├── requirements.txt    # Python dependencies
│   ├── .flake8            # Linting configuration
│   └── pyproject.toml     # Python project configuration
├── Frontend/               # React application
│   ├── src/               # Source code
│   ├── public/            # Static assets
│   ├── package.json       # Node dependencies
│   └── .eslintrc.js       # ESLint configuration
├── .vscode/               # VS Code settings
├── .editorconfig          # Editor configuration
├── .prettierrc            # Prettier configuration
└── .gitignore            # Git ignore rules
```

## Common Commands

### Backend
```bash
# Format code
black .

# Lint code
flake8 .

# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# Start development server
python app.py
```

### Frontend
```bash
# Start development server
npm start

# Run tests
npm test

# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Build for production
npm run build
```

## Troubleshooting

### Common Issues
1. **Import errors**: Make sure virtual environment is activated
2. **Linting failures**: Run formatters before committing
3. **Test failures**: Check that all dependencies are installed

### Getting Help
- Check existing issues on GitHub
- Review the documentation
- Ask questions in pull request discussions

## License
By contributing to EtoAudioBook, you agree that your contributions will be licensed under the same license as the project.