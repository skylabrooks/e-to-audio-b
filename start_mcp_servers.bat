@echo off
echo Starting MCP servers...

echo Starting server: markitdown
start "markitdown" cmd /k uvx markitdown-mcp
echo Starting server: monday
start "monday" cmd /k npx mcp-server-monday
echo Starting server: google-calendar
start "google-calendar" cmd /k npx google-calendar-mcp-server
echo Starting server: jira-server-alt
start "jira-server-alt" cmd /k npx mcp-atlassian
echo Starting server: memory
start "memory" cmd /k npx @modelcontextprotocol/server-memory
echo Starting server: filesystem
start "filesystem" cmd /k npx @modelcontextprotocol/server-filesystem
echo Starting server: notion
start "notion" cmd /k npx notion-mcp-server
echo Starting server: fetch
start "fetch" cmd /k npx @modelcontextprotocol/server-fetch
echo Starting server: slack
start "slack" cmd /k npx slack-mcp-server
echo Starting server: airtable
start "airtable" cmd /k npx airtable-mcp-server
echo Starting server: docker
start "docker" cmd /k npx mcp-server-docker
echo Starting server: kubernetes
start "kubernetes" cmd /k npx mcp-server-kubernetes
echo Starting server: docker-server-alt
start "docker-server-alt" cmd /k npx mcp-server-docker
echo Starting server: stripe
start "stripe" cmd /k npx mcp-stripe
echo Starting server: git
start "git" cmd /k uvx mcp-server-git --repository "c:\Users\Clay\source\repos\EtoAudioBook - Copy"
echo Starting server: everything
start "everything" cmd /k npx @modelcontextprotocol/server-everything
echo Starting server: python-sandbox
start "python-sandbox" cmd /k uvx mcp-run-python
echo Starting server: openai-tts
start "openai-tts" cmd /k python -c "import fastmcp; from openai import OpenAI; client = OpenAI(); fastmcp.Server('openai-tts', description='OpenAI TTS integration').serve()"
echo Starting server: github
start "github" cmd /k npx @modelcontextprotocol/server-github
echo Starting server: brave-search
start "brave-search" cmd /k npx @modelcontextprotocol/server-brave-search

echo All MCP servers are starting in separate windows.
