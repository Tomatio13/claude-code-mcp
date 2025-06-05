<h1 align="center">Claude Code MCP Server</h1>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python Version"/>
    <img src="https://img.shields.io/badge/MCP-Protocol-green.svg" alt="MCP Protocol"/>
    <img src="https://img.shields.io/badge/Claude-Code-orange.svg" alt="Claude Code"/>
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"/>
</p>

<p align="center">
    <a href="README_JP.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
    <a href="README.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</p>

<p align="center">
    Wraps Claude Code as an MCP (Model Context Protocol) server for integration with Claude and other MCP clients.
</p>

## 🚀 Features

This MCP server provides the following tools:

- **`claude_code_query`**: Send prompts to Claude Code for code generation, explanation, debugging, etc.
- **`claude_code_status`**: Check Claude Code installation and version

## 🔌 Supported Modes

- **SSE mode only**: Uses Server-Sent Events (for Web API)

## 📋 Prerequisites

1. **Claude Code**: 
   ```bash
   pip install --upgrade anthropic[code]
   # Or see the official documentation
   ```

2. **Python 3.12 or higher**

3. **Environment setup**: Copy `.env.example` to `.env` and configure as needed

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Tomatio13/claude-code-mcp.git
cd claude-code-mcp
```

### 2. Setup
```bash
./setup.sh
```

### 3. Start the server

#### SSE mode (for Web API)
```bash
./run_sse.sh [port] [host]

# Examples:
./run_sse.sh 8080 0.0.0.0  # Port 8080, listen on all interfaces
./run_sse.sh              # Default: localhost:8000
```

#### Manual startup
```bash
python claude_code_server.py --port 8000 --host localhost
```


### Manual installation
```bash
pip install -e .
python claude_code_server.py
```

## 💡 Usage

Once the Claude Code MCP server is running, you can use the tools from any MCP client (e.g., Claude Desktop, Web UI):

### Basic query
```
@claude-code claude_code_query prompt="Explain this codebase structure"
```

### Specify model and output format
```
@claude-code claude_code_query prompt="Create a Python REST API" model="opus" output_format="json"
```

### Status check
```
@claude-code claude_code_status
```

## 🎯 Parameters

- `prompt` : Instruction for Claude Code CLI
- `model` : Model to use (e.g., sonnet, opus, claude-sonnet-4-20250514, etc.)
- `output_format` : Output format (text, json, stream-json)

## 🛡️ Security

- File operations and command execution follow Claude Code CLI specifications
- Server supports SSE mode only
- File operations are limited to the working directory

## 🐛 Troubleshooting

### Common Issues

1. **"claude command not found"**
   ```bash
   pip install --upgrade anthropic[code]
   # Or see the official documentation
   ```

2. **Permission denied on scripts**
   ```bash
   chmod +x *.sh
   ```

3. **Python version issues**
   - Ensure Python 3.12+ is installed
   - Use virtual environment: `python3 -m venv venv && source venv/bin/activate`

4. **MCP connection issues**
   - Check client configuration file syntax
   - Verify file paths are absolute
   - Restart client after configuration changes

## 📝 License

MIT License with Attribution - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

<p align="center">
    Made with ❤️ for the Claude + Claude Code CLI community
</p>

# Check if claude CLI is available
if ! command -v claude &> /dev/null; then
    echo "❌ Error: 'claude' command not found"
    echo "Please install Claude Code:"
    echo "  pip install --upgrade anthropic[code]"
    exit 1
fi