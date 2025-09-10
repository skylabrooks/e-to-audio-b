# MCP Setup Guide - Updated

## ✅ Working MCP Agents 

Your MCP configuration now includes agents that work perfectly on Windows:

### Core Development
- **filesystem**: File system access (`npx @modelcontextprotocol/server-filesystem`)
- **git**: Git operations for this repo (`uvx mcp-server-git`)
- **fetch**: HTTP requests (`npx @modelcontextprotocol/server-fetch`)
- **memory**: Persistent memory (`npx @modelcontextprotocol/server-memory`)

### Python Development
- **python-sandbox**: ✅ VERIFIED - Secure Python/Flask execution (`uvx mcp-run-python`)

### Text-to-Speech Integration
- **openai-tts**: ✅ NEW - OpenAI TTS integration via FastMCP (installed successfully)

### Web Integration
- **github**: GitHub repository management (`npx @modelcontextprotocol/server-github`)
- **brave-search**: Web search capabilities (`npx @modelcontextprotocol/server-brave-search`)

### Document Processing
- **markitdown**: Document conversion (`uvx markitdown-mcp`)
- **huggingface**: AI/ML models (`https://hf.co/mcp`)

## 🔧 Build Tools Status

✅ **Visual Studio Build Tools installed successfully**

## 🚫 Problematic Audio Dependencies

- ❌ **webrtcvad & simpleaudio**: Still require additional C++ configuration
- ✅ **Alternative**: Using OpenAI TTS via FastMCP instead (no compilation needed)
- ✅ **Your Google Cloud TTS**: Still your primary solution in Flask backend

## 🛠 Quick Test Commands

```bash
# Test Python sandbox (confirmed working)
uvx mcp-run-python --help

# Test MCP components (confirmed working)  
python -c "import mcp, fastmcp, openai; print('All MCP components ready!')"

# Test other MCP servers (use as needed)
npx @modelcontextprotocol/server-fetch --help
npx @modelcontextprotocol/server-github --help
```

## 🎯 For Your Text-to-Speech App

### Recommended workflow:
1. **Use python-sandbox** for testing Flask backend code safely
2. **Use fetch** for testing API calls to Google Cloud TTS
3. **Use github** for version control operations
4. **Use filesystem** for file operations
5. **Use git** for repository management

### For Text-to-Speech:
- Your existing Google Cloud TTS integration in the Flask backend is your primary TTS solution
- MCP agents support development and testing, not core TTS functionality
- Consider future integration with voice MCP servers once C++ build tools are set up

## 🔧 Optional: Advanced TTS MCP Setup

If you want advanced voice capabilities later:

1. Install Visual Studio Build Tools:
   ```bash
   # Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   ```

2. Then retry:
   ```bash
   pip install voice-mode
   ```

## 🚀 Your Current Setup

Your [mcp.json](./mcp.json) is now configured with working agents that support your development workflow without compilation issues.
