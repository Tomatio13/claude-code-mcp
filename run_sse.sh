#!/bin/bash

# Claude Code MCP Server SSE Mode Run Script

set -e

echo "🎯 Starting Claude Code MCP Server in SSE mode..."

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
elif [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: No virtual environment found"
    echo "Please run ./setup.sh first to set up the environment"
    exit 1
fi

# Check if claude is available
if ! command -v claude &> /dev/null; then
    echo "❌ Error: 'claude' command not found"
    echo "Please install Claude Code:"
    echo "  pip install --upgrade anthropic[code]"
    exit 1
fi

# Parse command line arguments
PORT=${1:-8000}
HOST=${2:-localhost}

echo "The server will run in SSE mode on http://${HOST}:${PORT}"
echo "Press Ctrl+C to stop the server"
echo ""

# Run the MCP server in SSE mode
python claude_code_server.py --host "${HOST}" --port "${PORT}"