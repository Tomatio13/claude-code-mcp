#!/bin/bash

# Claude Code MCP Server Setup Script

set -e

echo "🚀 Setting up Claude Code MCP Server..."

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Not in a virtual environment. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Check if claude is installed
if ! command -v claude &> /dev/null; then
    echo "❌ Error: 'claude' command not found"
    echo "Please install Claude Code first:"
    echo "  pip install --upgrade anthropic[code]"
    exit 1
fi

echo "✅ Claude Code found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -e .

echo "✅ Setup completed successfully!"
echo ""
echo "To start the server, run:"
echo "  ./run.sh"