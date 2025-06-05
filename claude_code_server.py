#!/usr/bin/env python3
"""
Claude Code MCP Server for use with Claude.
This server implements MCP protocol to wrap the Claude Code CLI.
Supports SSE (Server-Sent Events) mode only.
"""

import os
import sys
import subprocess
import json
import argparse
from typing import Optional, Dict, Any

from fastmcp import FastMCP


# Initialize FastMCP server
mcp = FastMCP("Claude Code MCP Server")


def run_claude_code(
    prompt: Optional[str] = None,
    model: Optional[str] = None,
    output_format: str = "text"
) -> Dict[str, Any]:
    """
    Run the Claude Code CLI tool with the given parameters.
    
    Args:
        prompt: The prompt to send to Claude Code
        model: The model to use (e.g., "sonnet", "opus", "claude-sonnet-4-20250514")
        output_format: Output format for print mode (text, json, stream-json)
    Returns:
        A dictionary containing the response from Claude Code
    """
    # Build command
    cmd = ["claude"]
    
    # Add model if specified
    if model:
        cmd.extend(["--model", model])
    
    # Add print mode for non-interactive execution
    cmd.append("--print")

    # Add output format if not text
    if output_format and output_format != "text":
        cmd.extend(["--output-format", output_format])
    
    # Add the prompt if provided
    if prompt:
        cmd.append(prompt)
    
    print(f"Executing command: {' '.join(cmd)}", file=sys.stderr)
    
    try:
        # Run the command and capture output
        result = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            check=True
        )
        
        output = result.stdout.strip()
        # Try to parse JSON output if output format is json
        if output_format == "json" and output:
            try:
                parsed_output = json.loads(output)
                return {
                    "status": "success",
                    "output": parsed_output,
                    "raw_output": output,
                    "stderr": result.stderr,
                    "command": " ".join(cmd)
                }
            except json.JSONDecodeError:
                pass
        return {
            "status": "success",
            "output": output,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
    except subprocess.CalledProcessError as e:
        print(f"Error running claude: {e}", file=sys.stderr)
        return {
            "status": "error",
            "error": str(e),
            "output": e.stdout,
            "stderr": e.stderr,
            "exit_code": e.returncode,
            "command": " ".join(cmd)
        }
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return {
            "status": "error",
            "error": str(e),
            "command": " ".join(cmd)
        }


@mcp.tool()
def claude_code_query(
    prompt: str,
    model: str = "sonnet",
    output_format: str = "text"
) -> Dict[str, Any]:
    """
    Send a query to Claude Code in print mode (non-interactive).
    
    Args:
        prompt: The query or task to send to Claude Code
        model: AI model to use (default: sonnet, options: sonnet, opus, claude-sonnet-4-20250514, etc.)
        output_format: Output format (text, json, stream-json)
    Returns:
        Dictionary with status, output, and execution details
    Examples:
        # Basic query
        claude_code_query("Explain this codebase structure")
        # Code generation
        claude_code_query("Create a Python REST API", model="opus", output_format="json")
    """
    if not prompt:
        return {
            "status": "error",
            "error": "Missing required parameter: prompt"
        }
    return run_claude_code(
        prompt=prompt,
        model=model,
        output_format=output_format
    )


@mcp.tool()
def claude_code_status() -> Dict[str, Any]:
    """
    Get Claude Code status and version information.
    
    This runs basic Claude Code commands to check installation and status.
    
    Returns:
        Dictionary with Claude Code status information
    """
    try:
        # Check if claude command exists
        which_result = subprocess.run(["which", "claude"], capture_output=True, text=True)
        if which_result.returncode != 0:
            return {
                "status": "error",
                "error": "Claude Code CLI not found in PATH",
                "suggestion": "Please install Claude Code CLI following the instructions at https://docs.anthropic.com/claude-code"
            }
        # Try to get version/status info
        status_result = subprocess.run(
            ["claude", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            "status": "success",
            "claude_path": which_result.stdout.strip(),
            "help_output": status_result.stdout,
            "message": "Claude Code CLI is installed and available"
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "warning",
            "message": "Claude Code CLI found but --help command timed out",
            "suggestion": "The CLI may be waiting for authentication or have other issues"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Error checking Claude Code status"
        }


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Claude Code MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python claude_code_server.py                         # Run in SSE mode on default port 8000
  python claude_code_server.py --port 8080            # Run in SSE mode on port 8080
  python claude_code_server.py --host 0.0.0.0         # Run accessible from all interfaces
        """
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number for SSE mode (default: 8000)"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host address for SSE mode (default: localhost)"
    )
    return parser.parse_args()


def main():
    """Main entry point for the MCP server."""
    # Parse command line arguments
    args = parse_args()
    # Check if claude is installed
    try:
        result = subprocess.run(["which", "claude"], capture_output=True, text=True)
        if result.returncode != 0:
            print("ERROR: 'claude' command not found in PATH", file=sys.stderr)
            print("Please install Claude Code CLI following the instructions at:", file=sys.stderr)
            print("https://docs.anthropic.com/claude-code", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error checking for claude: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Starting Claude Code MCP Server in SSE mode...", file=sys.stderr)
    print(f"Server will run on http://{args.host}:{args.port}", file=sys.stderr)
    print("Available tools:", file=sys.stderr)
    print("  - claude_code_query: Primary tool for programmatic Claude Code queries", file=sys.stderr)
    print("  - claude_code_status: Check Claude Code status", file=sys.stderr)
    print("Server will use Server-Sent Events for communication", file=sys.stderr)
    mcp.run(transport="sse", host=args.host, port=args.port)


if __name__ == "__main__":
    main() 