#!/usr/bin/env python3
"""
MCP Server for PydanticAI Conversation Agent

This MCP server exposes the dual-mode AI assistant functionality through the
Model Context Protocol, allowing other applications to interact with the
conversational and rephrasing agents.
"""

import asyncio
import json
import logging
from typing import Any

from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    Resource,
    TextContent,
    Tool,
)
from pydantic import BaseModel

from mcp.server import Server
from src.core.assistant import DualModeAssistant

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-pydantic-ai")


class ConversationSession(BaseModel):
    """Represents a conversation session with history."""

    session_id: str
    assistant: DualModeAssistant
    created_at: str
    message_count: int = 0


class PydanticAIMCPServer:
    """MCP Server for PydanticAI Conversation Agent."""

    def __init__(self):
        """Initialize the MCP server."""
        self.server = Server("pydantic-ai-conversation-agent")
        self.sessions: dict[str, ConversationSession] = {}
        self.default_assistant = DualModeAssistant()

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
                    description="Have a conversational chat with the AI assistant. Maintains context and conversation history.",
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
                    description="Improve grammar, clarity, and writing quality of text while preserving meaning and tone.",
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
                    name="create_conversation_session",
                    description="Create a new conversation session with isolated context.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "Unique identifier for the new session",
                            },
                            "model_name": {
                                "type": "string",
                                "description": "AI model to use (default: openai:gpt-4o)",
                                "default": "openai:gpt-4o",
                            },
                        },
                        "required": ["session_id"],
                    },
                ),
                Tool(
                    name="get_conversation_stats",
                    description="Get statistics about a conversation session including message count and context info.",
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
                Tool(
                    name="list_sessions",
                    description="List all active conversation sessions.",
                    inputSchema={"type": "object", "properties": {}},
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
                elif name == "create_conversation_session":
                    return await self._handle_create_session(arguments)
                elif name == "get_conversation_stats":
                    return await self._handle_get_stats(arguments)
                elif name == "clear_conversation_history":
                    return await self._handle_clear_history(arguments)
                elif name == "list_sessions":
                    return await self._handle_list_sessions(arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            except Exception as e:
                logger.error(f"Error handling tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]

        @self.server.list_prompts()
        async def handle_list_prompts() -> list[Prompt]:
            """List available prompts."""
            return [
                Prompt(
                    name="conversation_starter",
                    description="Start a friendly conversation with the AI assistant",
                    arguments=[
                        {
                            "name": "topic",
                            "description": "Topic to discuss",
                            "required": False,
                        }
                    ],
                ),
                Prompt(
                    name="text_improvement",
                    description="Template for improving text quality",
                    arguments=[
                        {
                            "name": "text",
                            "description": "Text to improve",
                            "required": True,
                        },
                        {
                            "name": "style",
                            "description": "Writing style (formal, casual, professional)",
                            "required": False,
                        },
                    ],
                ),
            ]

        @self.server.get_prompt()
        @self.server.get_prompt()
        async def handle_get_prompt(name: str, arguments: dict[str, str] | None):
            """Get a specific prompt."""
            args = arguments or {}
            if name == "conversation_starter":
                topic = args.get("topic", "general topics")
                content = (
                    f"conversational: Let's have a friendly conversation "
                    f"about {topic}. What would you like to know or discuss?"
                )
                return GetPromptResult(
                    description="Start a conversation",
                    messages=[
                        {
                            "role": "user",
                            "content": TextContent(type="text", text=content),
                        }
                    ],
                )
            elif name == "text_improvement":
                text = args.get("text", "")
                style = args.get("style", "")
                if not text:
                    content = "rephrasing: [Please provide text to improve]"
                else:
                    style_note = f" in a {style} style" if style else ""
                    content = f"rephrasing: {text}"

                return GetPromptResult(
                    description=f"Improve text quality{style_note}",
                    messages=[
                        {
                            "role": "user",
                            "content": TextContent(type="text", text=content),
                        }
                    ],
                )
            else:
                raise ValueError(f"Unknown prompt: {name}")

        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="conversation://sessions",
                    name="Active Conversation Sessions",
                    description="Information about all active conversation sessions",
                    mimeType="application/json",
                ),
                Resource(
                    uri="conversation://capabilities",
                    name="Assistant Capabilities",
                    description=(
                        "Information about the AI assistant's capabilities and modes"
                    ),
                    mimeType="application/json",
                ),
            ]

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
            # Update session stats
            if session_id in self.sessions:
                self.sessions[session_id].message_count += 1

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
        result = await self.default_assistant.process_single_request(request_text)

        if result["success"]:
            return [TextContent(type="text", text=result["response"])]
        else:
            return [TextContent(type="text", text=f"Error: {result['error']}")]

    async def _handle_create_session(
        self, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle session creation requests."""
        session_id = arguments.get("session_id", "")
        model_name = arguments.get("model_name", "openai:gpt-4o")

        if not session_id:
            return [TextContent(type="text", text="Error: No session_id provided")]

        if session_id in self.sessions:
            return [
                TextContent(type="text", text=f"Session '{session_id}' already exists")
            ]

        # Create new session
        assistant = DualModeAssistant(model_name=model_name)
        from datetime import datetime

        session = ConversationSession(
            session_id=session_id,
            assistant=assistant,
            created_at=datetime.now().isoformat(),
        )

        self.sessions[session_id] = session

        return [
            TextContent(
                type="text",
                text=(
                    f"Created conversation session '{session_id}' "
                    f"with model {model_name}"
                ),
            )
        ]

    async def _handle_get_stats(self, arguments: dict[str, Any]) -> list[TextContent]:
        """Handle conversation stats requests."""
        session_id = arguments.get("session_id", "default")

        assistant = self._get_or_create_session(session_id)
        stats = assistant.get_conversation_stats()

        session_info = {}
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session_info = {
                "session_id": session_id,
                "created_at": session.created_at,
                "message_count": session.message_count,
            }

        combined_stats = {**stats, **session_info}

        return [
            TextContent(
                type="text",
                text=(
                    f"Conversation Statistics:\n{json.dumps(combined_stats, indent=2)}"
                ),
            )
        ]

    async def _handle_clear_history(
        self, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle conversation history clearing requests."""
        session_id = arguments.get("session_id", "default")

        assistant = self._get_or_create_session(session_id)
        assistant.clear_conversation_history()

        if session_id in self.sessions:
            self.sessions[session_id].message_count = 0

        return [
            TextContent(
                type="text",
                text=f"Cleared conversation history for session '{session_id}'",
            )
        ]

    async def _handle_list_sessions(
        self, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle session listing requests."""
        if not self.sessions:
            return [TextContent(type="text", text="No active sessions")]

        session_list = []
        for session_id, session in self.sessions.items():
            session_list.append(
                {
                    "session_id": session_id,
                    "created_at": session.created_at,
                    "message_count": session.message_count,
                }
            )

        return [
            TextContent(
                type="text",
                text=f"Active Sessions:\n{json.dumps(session_list, indent=2)}",
            )
        ]

    def _get_or_create_session(self, session_id: str) -> DualModeAssistant:
        """Get existing session or create a new one."""
        if session_id not in self.sessions:
            from datetime import datetime

            assistant = DualModeAssistant()
            session = ConversationSession(
                session_id=session_id,
                assistant=assistant,
                created_at=datetime.now().isoformat(),
            )
            self.sessions[session_id] = session
            logger.info(f"Created new session: {session_id}")

        return self.sessions[session_id].assistant

    async def run(self):
        """Run the MCP server."""
        logger.info("Starting PydanticAI MCP Server...")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream)


async def main():
    """Main entry point for the MCP server."""
    server = PydanticAIMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
