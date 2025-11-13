#!/usr/bin/env python3
"""
Simple MCP Server startup script for PydanticAI Conversation Agent

This script starts the MCP server that exposes the dual-mode AI assistant
functionality through the Model Context Protocol.
"""

import asyncio
import sys
from pathlib import Path


def setup_path():
    """Add the project root to Python path."""
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))


if __name__ == "__main__":
    print("🤖 Starting PydanticAI MCP Server...")
    print("📡 Server will communicate via stdio (standard input/output)")
    print("🔗 Use this server with MCP clients like Claude Desktop")
    print("=" * 50)

    # Setup path and import
    setup_path()
    from src.mcp.simple_server import main

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 MCP Server stopped")
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        sys.exit(1)
