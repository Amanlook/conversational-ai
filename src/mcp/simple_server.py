#!/usr/bin/env python3
"""
Simple MCP Server for PydanticAI Conversation Agent

This is a working MCP server that exposes the dual-mode AI assistant functionality.
It provides tools for conversational chat and text rephrasing.
"""

import asyncio
import json
import logging
from typing import Any

from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from mcp.server import Server
from src.core.assistant import DualModeAssistant

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-pydantic-ai")


class SimplePydanticAIMCPServer:
    """Simple MCP Server for PydanticAI Conversation Agent."""

    def __init__(self):
        """Initialize the MCP server."""
        self.server = Server("pydantic-ai-conversation-agent")
        self.assistant = DualModeAssistant()
        self.sessions: dict[str, DualModeAssistant] = {}

        # Register MCP handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register all MCP protocol handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="conversational_chat",
                    description=(
                        "Have a conversational chat with the AI assistant. "
                        "Maintains context and conversation history."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Your message or question for the AI assistant",
                            },
                            "session_id": {
                                "type": "string",
                                "description": "Optional session ID to maintain conversation context",
                                "default": "default",
                            },
                        },
                        "required": ["message"],
                    },
                ),
                Tool(
                    name="rephrase_text",
                    description=(
                        "Improve grammar, clarity, and writing quality of text "
                        "while preserving meaning and tone."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "The text to be rephrased and improved",
                            }
                        },
                        "required": ["text"],
                    },
                ),
                Tool(
                    name="get_conversation_stats",
                    description=(
                        "Get statistics about a conversation session including "
                        "message count and context info."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "Session ID to get stats for",
                                "default": "default",
                            }
                        },
                    },
                ),
                Tool(
                    name="clear_conversation_history",
                    description="Clear the conversation history for a specific session.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "Session ID to clear history for",
                                "default": "default",
                            }
                        },
                    },
                ),
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any]
        ) -> list[TextContent]:
            """Handle tool calls."""
            try:
                if name == "conversational_chat":
                    return await self._handle_conversational_chat(arguments)
                elif name == "rephrase_text":
                    return await self._handle_rephrase_text(arguments)
                elif name == "get_conversation_stats":
                    return await self._handle_get_stats(arguments)
                elif name == "clear_conversation_history":
                    return await self._handle_clear_history(arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            except Exception as e:
                logger.error(f"Error handling tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    async def _handle_conversational_chat(
        self, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle conversational chat requests."""
        message = arguments.get("message", "")
        session_id = arguments.get("session_id", "default")

        if not message:
            return [TextContent(type="text", text="Error: No message provided")]

        # Get or create session
        assistant = self._get_or_create_session(session_id)

        # Process the conversational request
        request_text = f"conversational: {message}"
        result = await assistant.process_single_request(request_text)

        if result["success"]:
            return [TextContent(type="text", text=result["response"])]
        else:
            return [TextContent(type="text", text=f"Error: {result['error']}")]

    async def _handle_rephrase_text(
        self, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle text rephrasing requests."""
        text = arguments.get("text", "")

        if not text:
            return [TextContent(type="text", text="Error: No text provided")]

        # Use default assistant for rephrasing (no session needed)
        request_text = f"rephrasing: {text}"
        result = await self.assistant.process_single_request(request_text)

        if result["success"]:
            return [TextContent(type="text", text=result["response"])]
        else:
            return [TextContent(type="text", text=f"Error: {result['error']}")]

    async def _handle_get_stats(self, arguments: dict[str, Any]) -> list[TextContent]:
        """Handle conversation stats requests."""
        session_id = arguments.get("session_id", "default")

        assistant = self._get_or_create_session(session_id)
        stats = assistant.get_conversation_stats()

        return [
            TextContent(
                type="text",
                text=f"Conversation Statistics for session '{session_id}':\n{json.dumps(stats, indent=2)}",
            )
        ]

    async def _handle_clear_history(
        self, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle conversation history clearing requests."""
        session_id = arguments.get("session_id", "default")

        assistant = self._get_or_create_session(session_id)
        assistant.clear_conversation_history()

        return [
            TextContent(
                type="text",
                text=f"Cleared conversation history for session '{session_id}'",
            )
        ]

    def _get_or_create_session(self, session_id: str) -> DualModeAssistant:
        """Get existing session or create a new one."""
        if session_id not in self.sessions:
            assistant = DualModeAssistant()
            self.sessions[session_id] = assistant
            logger.info(f"Created new session: {session_id}")

        return self.sessions[session_id]

    async def run(self):
        """Run the MCP server."""
        logger.info("Starting PydanticAI MCP Server...")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream)


async def main():
    """Main entry point for the MCP server."""
    server = SimplePydanticAIMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
