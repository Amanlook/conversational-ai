#!/usr/bin/env python3
"""
Main entry point for the Dual-Mode AI Assistant.

This script provides a clean interface to start the interactive chat session
using the refactored class-based architecture.
"""

from dotenv import load_dotenv

from src.core.assistant import DualModeAssistant

# Load environment variables from .env file
load_dotenv()


def main():
    """Main function to start the dual-mode AI assistant."""
    try:
        # Initialize the assistant
        assistant = DualModeAssistant()

        # Start interactive session
        assistant.start_interactive_session()

    except Exception as e:
        print(f"Failed to start assistant: {e}")
        print("Make sure you have your API keys configured in .env file")


if __name__ == "__main__":
    main()
