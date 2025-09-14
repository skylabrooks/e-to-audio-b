#!/usr/bin/env python3
"""
EtoAudioBook MCP Server
Provides project-specific context and tools for Amazon Q Developer
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add the backend directory to the path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

try:
    from mcp.server import Server
    from mcp.types import Resource, Tool, TextContent
    import mcp.server.stdio
except ImportError:
    print("MCP library not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Initialize the MCP server
server = Server("etoaudiobook")

@server.list_resources()
async def list_resources() -> List[Resource]:
    """List available project resources"""
    project_root = backend_dir.parent
    
    resources = [
        Resource(
            uri=f"file://{project_root}/README.md",
            name="Project README",
            description="Main project documentation and setup instructions",
            mimeType="text/markdown"
        ),
        Resource(
            uri=f"file://{project_root}/docs/AGENTS.md", 
            name="Development Guidelines",
            description="Development guidelines and project structure info",
            mimeType="text/markdown"
        ),
        Resource(
            uri=f"file://{project_root}/Backend/app.py",
            name="Flask Backend API",
            description="Main Flask application with TTS endpoints",
            mimeType="text/x-python"
        ),
        Resource(
            uri=f"file://{project_root}/Frontend/src/App.js",
            name="React Frontend",
            description="Main React application component",
            mimeType="text/javascript"
        ),
        Resource(
            uri=f"file://{project_root}/mcp.json",
            name="MCP Configuration", 
            description="Model Context Protocol server configuration",
            mimeType="application/json"
        )
    ]
    
    return resources

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource"""
    if not uri.startswith("file://"):
        raise ValueError(f"Unsupported URI scheme: {uri}")
    
    file_path = Path(uri[7:])  # Remove "file://" prefix
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        return file_path.read_text(encoding='utf-8')
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available project tools"""
    return [
        Tool(
            name="get_project_structure",
            description="Get the current project directory structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_depth": {
                        "type": "integer", 
                        "description": "Maximum depth to traverse (default: 2)",
                        "default": 2
                    }
                }
            }
        ),
        Tool(
            name="analyze_tts_config",
            description="Analyze the current TTS configuration and suggest improvements",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="check_api_endpoints",
            description="List and validate Flask API endpoints",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_env_template",
            description="Generate environment variable template for the project",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute a tool"""
    project_root = backend_dir.parent
    
    if name == "get_project_structure":
        max_depth = arguments.get("max_depth", 2)
        structure = _get_directory_structure(project_root, max_depth)
        return [TextContent(type="text", text=structure)]
    
    elif name == "analyze_tts_config":
        analysis = _analyze_tts_setup()
        return [TextContent(type="text", text=analysis)]
    
    elif name == "check_api_endpoints":
        endpoints = _check_flask_endpoints()
        return [TextContent(type="text", text=endpoints)]
    
    elif name == "get_env_template":
        template = _generate_env_template()
        return [TextContent(type="text", text=template)]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

def _get_directory_structure(path: Path, max_depth: int, current_depth: int = 0) -> str:
    """Get directory structure as a string"""
    if current_depth > max_depth:
        return ""
    
    items = []
    indent = "  " * current_depth
    
    try:
        for item in sorted(path.iterdir()):
            if item.name.startswith('.') and item.name not in ['.env.example', '.gitignore']:
                continue
            if item.name in ['node_modules', 'venv', '__pycache__', '.git']:
                continue
                
            if item.is_dir():
                items.append(f"{indent}{item.name}/")
                if current_depth < max_depth:
                    sub_structure = _get_directory_structure(item, max_depth, current_depth + 1)
                    if sub_structure:
                        items.append(sub_structure)
            else:
                items.append(f"{indent}{item.name}")
    except PermissionError:
        items.append(f"{indent}[Permission Denied]")
    
    return "\n".join(items)

def _analyze_tts_setup() -> str:
    """Analyze TTS configuration"""
    app_py = backend_dir / "app.py"
    credentials_py = backend_dir / "credentials.py"
    env_file = backend_dir / ".env"
    
    analysis = []
    analysis.append("# TTS Configuration Analysis\n")
    
    if app_py.exists():
        analysis.append("✅ Flask app.py exists")
    else:
        analysis.append("❌ Flask app.py missing")
    
    if credentials_py.exists():
        analysis.append("✅ credentials.py exists")
    else:
        analysis.append("❌ credentials.py missing")
    
    if env_file.exists():
        analysis.append("✅ .env file exists")
    else:
        analysis.append("⚠️  .env file missing - create from template")
    
    # Check if Google Cloud TTS is configured
    try:
        if app_py.exists():
            content = app_py.read_text()
            if "google.cloud" in content and "texttospeech" in content:
                analysis.append("✅ Google Cloud TTS integration found")
            else:
                analysis.append("❌ Google Cloud TTS integration missing")
    except Exception:
        analysis.append("⚠️  Could not analyze app.py")
    
    return "\n".join(analysis)

def _check_flask_endpoints() -> str:
    """Check Flask API endpoints"""
    app_py = backend_dir / "app.py"
    endpoints = []
    
    if not app_py.exists():
        return "❌ Flask app.py not found"
    
    try:
        content = app_py.read_text()
        lines = content.split('\n')
        
        endpoints.append("# Flask API Endpoints\n")
        
        for i, line in enumerate(lines):
            if '@app.route(' in line:
                route_line = line.strip()
                # Try to get the function name from the next few lines
                func_name = "Unknown"
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip().startswith('def '):
                        func_name = lines[j].strip().split('(')[0].replace('def ', '')
                        break
                
                endpoints.append(f"- {route_line} -> {func_name}()")
        
        if len(endpoints) == 1:  # Only header
            endpoints.append("No API endpoints found")
    
    except Exception as e:
        endpoints.append(f"Error analyzing endpoints: {e}")
    
    return "\n".join(endpoints)

def _generate_env_template() -> str:
    """Generate environment variable template"""
    return """# Environment Variables Template for EtoAudioBook

# Google Cloud Credentials
GOOGLE_APPLICATION_CREDENTIALS=Backend/service-account.json
# Or use individual variables:
# GOOGLE_PROJECT_ID=your-project-id
# GOOGLE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
# GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\\nYOUR_KEY\\n-----END PRIVATE KEY-----"

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=true
FLASK_PORT=5000

# API Keys (if using alternative TTS services)
OPENAI_API_KEY=your-openai-api-key-here

# Frontend Configuration
REACT_APP_API_URL=http://localhost:5000

# Development
DEBUG=true
"""

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
