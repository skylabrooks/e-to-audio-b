# LLM Extensions Rules & Configuration

## Overview
This document outlines the rules, configurations, and best practices for all LLM extensions in the EtoAudioBook project.

## 🔐 Security Rules

### API Key Management
- **NEVER** commit API keys to version control
- Use environment variables for all sensitive credentials
- Store example configurations in `.env.example`
- Add `.env` to `.gitignore` (already configured)

### Current API Keys Required:
```bash
GEMINI_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
BRAVE_API_KEY=your-brave-api-key-here
```

## 📋 Configured LLM Extensions

### 1. VS Code Chat MCP Integration
**Location**: `.vscode/settings.json`
```json
"chat.mcp.serverSampling": {
    "gemini": {
        "command": "npx",
        "args": ["@modelcontextprotocol/server-gemini"],
        "env": {
            "GEMINI_API_KEY": "${env:GEMINI_API_KEY}"
        }
    }
}
```

**Rules**:
- ✅ Uses environment variable for API key
- ✅ Timeout configured (30 seconds)
- ✅ Logging enabled for debugging

### 2. MCP Servers Configuration
**Location**: `mcp.json`

#### AI/LLM Related Servers:

**HuggingFace** (`huggingface`)
- Type: HTTP
- URL: https://hf.co/mcp
- Purpose: AI model hub integration
- Status: ✅ No credentials required

**OpenAI TTS** (`openai-tts`)
- Type: stdio
- Purpose: Text-to-speech integration
- Credentials: ✅ Uses environment variable
- Status: ✅ Properly configured

**Python Sandbox** (`python-sandbox`)
- Type: stdio
- Purpose: Secure code execution
- Status: ✅ No credentials required

#### Development & Productivity Servers:

**GitHub** (`github`)
- Purpose: Repository management
- Status: ⚠️ May require GitHub token

**Git** (`git`)
- Purpose: Version control operations
- Repository: Hardcoded path
- Status: ✅ No credentials required

**Memory** (`memory`)
- Purpose: Context persistence
- Status: ✅ No credentials required

**Filesystem** (`filesystem`)
- Purpose: File operations
- Status: ✅ No credentials required

**Brave Search** (`brave-search`)
- Purpose: Web search capabilities
- Credentials: ✅ Uses environment variable
- Status: ✅ Properly configured

## 🛡️ Security Best Practices

### 1. Environment Variables Setup
Create `.env` file in project root:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

### 2. VS Code Settings
- API keys referenced via `${env:VARIABLE_NAME}`
- Timeout settings configured
- Logging enabled for troubleshooting

### 3. MCP Configuration
- All sensitive data uses environment variables
- Server descriptions provided for clarity
- Proper type definitions (stdio/http)

## 🔧 Configuration Rules

### Required Environment Variables
```bash
# Core LLM APIs
GEMINI_API_KEY=          # Google Gemini API
OPENAI_API_KEY=          # OpenAI API (for TTS)
BRAVE_API_KEY=           # Brave Search API

# Optional GitHub Integration
GITHUB_TOKEN=            # GitHub API token (if using GitHub server)

# Google Cloud (for existing TTS)
GOOGLE_APPLICATION_CREDENTIALS=  # Path to service account JSON
```

### VS Code Extension Settings
```json
{
    "chat.mcp.enabled": true,
    "chat.mcp.timeout": 30000,
    "chat.mcp.logLevel": "info",
    "chat.mcp.serverSampling": {
        // Server configurations
    }
}
```

## 📊 Server Status Overview

| Server | Type | Status | Credentials | Purpose |
|--------|------|--------|-------------|---------|
| gemini | stdio | ✅ Configured | Environment | VS Code Chat |
| huggingface | http | ✅ Ready | None | AI Models |
| openai-tts | stdio | ✅ Configured | Environment | Text-to-Speech |
| python-sandbox | stdio | ✅ Ready | None | Code Execution |
| github | stdio | ⚠️ Needs Token | Optional | Repository |
| git | stdio | ✅ Ready | None | Version Control |
| memory | stdio | ✅ Ready | None | Context |
| filesystem | stdio | ✅ Ready | None | File Ops |
| brave-search | stdio | ✅ Configured | Environment | Web Search |
| notion | stdio | ⚠️ Needs Token | Optional | Documentation |
| slack | stdio | ⚠️ Needs Token | Optional | Communication |
| monday | stdio | ⚠️ Needs Token | Optional | Project Mgmt |
| google-calendar | stdio | ⚠️ Needs Token | Optional | Calendar |
| jira-server-alt | stdio | ⚠️ Needs Token | Optional | Issue Tracking |
| airtable | stdio | ⚠️ Needs Token | Optional | Database |
| docker | stdio | ✅ Ready | None | Containers |
| kubernetes | stdio | ⚠️ Needs Config | Optional | Orchestration |
| stripe | stdio | ⚠️ Needs Token | Optional | Payments |
| fetch | stdio | ✅ Ready | None | Web Requests |
| markitdown | stdio | ✅ Ready | None | Document Convert |
| everything | stdio | ✅ Ready | None | Universal Search |

## 🚀 Setup Instructions

### 1. Install Required Dependencies
```bash
# Install MCP servers
npm install -g @modelcontextprotocol/server-gemini
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-brave-search
# ... other servers as needed

# Install Python MCP tools
pip install markitdown-mcp
pip install mcp-run-python
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env
```

### 3. Test Configuration
```bash
# Test MCP servers
npx @modelcontextprotocol/server-gemini --help
uvx markitdown-mcp --help
```

## 🐛 Troubleshooting

### Common Issues:
1. **API Key Errors**: Ensure environment variables are set
2. **Server Not Found**: Install missing MCP servers
3. **Timeout Issues**: Increase timeout in VS Code settings
4. **Permission Errors**: Check file permissions for credentials

### Debug Commands:
```bash
# Check environment variables
echo $GEMINI_API_KEY
echo $OPENAI_API_KEY

# Test MCP server connectivity
npx @modelcontextprotocol/server-gemini --test
```

## 📝 Maintenance

### Regular Tasks:
- [ ] Update MCP server versions monthly
- [ ] Rotate API keys quarterly
- [ ] Review server usage and remove unused ones
- [ ] Monitor API usage and costs
- [ ] Update documentation when adding new servers

### Security Audits:
- [ ] Check for exposed credentials in commits
- [ ] Verify environment variable usage
- [ ] Review server permissions and access
- [ ] Update dependencies for security patches