# MCP Agents Guide for Text-to-Speech Audiobook App

## Essential MCP Agents Configured

### Core Development
- **filesystem**: File system access for reading/writing project files
- **git**: Git operations for version control in this repository
- **memory**: Persistent memory across sessions
- **python-sandbox**: Secure Python execution for Flask backend testing
- **fetch**: HTTP requests for API testing

### Text-to-Speech Specific
- **voice-mode**: Complete voice interaction server with speech-to-text and text-to-speech
- **huggingface**: Access to HuggingFace models for AI/ML tasks

### Frontend Development
- **react-docs**: Access to React and 90+ framework documentation
- **playwright**: Browser automation for testing React frontend
- **markitdown**: Document conversion and processing

### Additional Tools
- **docker**: Container management for deployment
- **notion**: Documentation and project management
- **slack**: Team communication integration

## Recommended Additional Agents

### For Enhanced Development
```bash
# Install additional useful MCP servers
pip install voice-mode                      # Voice interaction server
uvx @modelcontextprotocol/server-puppeteer  # Alternative browser automation

# For Kokoro TTS (requires manual setup):
# git clone https://github.com/mberg/kokoro-tts-mcp.git
# Follow setup instructions in their README
```

### For Production
- **stripe**: Payment processing if monetizing
- **kubernetes**: Container orchestration
- **monitoring tools**: Application performance monitoring

## Usage Examples

### Voice Processing
```javascript
// Using voice-mode for TTS testing
// Voice-mode handles both speech-to-text and text-to-speech
// Requires OpenAI API key for advanced features
```

### React Development
```javascript
// Using react-docs for component patterns
const componentDocs = await react_docs.searchDocs("functional components hooks");
```

### Testing
```bash
# Using playwright for frontend testing
playwright.test("audiobook upload functionality");
```

## Setup Instructions

1. Install the available MCP servers:
   ```bash
   # Install voice interaction server
   pip install voice-mode
   
   # Python sandbox is available via uvx
   # Other servers in the config are installed via npx/uvx as needed
   ```

2. Configure environment variables for TTS services
3. Test MCP connections in your development environment
4. Use the agents during development for enhanced productivity

## Security Notes
- Keep API keys and credentials in .env files
- Use sandbox environments for code execution
- Regularly update MCP server packages
