"""Input parsing utilities for dual-mode AI assistant."""

from dataclasses import dataclass
from enum import Enum


class Mode(Enum):
    """Available modes for the AI assistant."""

    CONVERSATIONAL = "conversational"
    REPHRASING = "rephrasing"
    HELP = "help"


@dataclass
class ParsedInput:
    """Represents parsed user input."""

    mode: Mode
    content: str
    is_valid: bool
    error_message: str = ""


class InputParser:
    """Handles parsing and validation of user input for different modes."""

    EXIT_COMMANDS = {"quit", "exit", "bye", "goodbye"}
    MODE_PREFIXES = {
        "conversational:": Mode.CONVERSATIONAL,
        "rephrasing:": Mode.REPHRASING,
    }

    @classmethod
    def parse(cls, user_input: str) -> ParsedInput:
        """
        Parse user input to determine mode and extract content.

        Args:
            user_input: Raw user input string

        Returns:
            ParsedInput object with mode, content, and validation info
        """
        user_input = user_input.strip()

        # Check for exit commands
        if user_input.lower() in cls.EXIT_COMMANDS:
            return ParsedInput(mode=Mode.HELP, content="exit", is_valid=True)

        # Check if input is empty
        if not user_input:
            return ParsedInput(
                mode=Mode.HELP,
                content="",
                is_valid=False,
                error_message="I didn't catch that. Could you say something?",
            )

        # Try to match mode prefixes
        for prefix, mode in cls.MODE_PREFIXES.items():
            if user_input.lower().startswith(prefix):
                content = user_input[len(prefix) :].strip()

                # Validate that content exists after prefix
                if not content:
                    return ParsedInput(
                        mode=mode,
                        content="",
                        is_valid=False,
                        error_message="Please provide content after the mode label.",
                    )

                return ParsedInput(mode=mode, content=content, is_valid=True)

        # No mode prefix found
        return ParsedInput(
            mode=Mode.HELP,
            content=user_input,
            is_valid=False,
            error_message="Please specify a mode to get started.",
        )

    @classmethod
    def is_exit_command(cls, user_input: str) -> bool:
        """Check if the input is an exit command."""
        return user_input.strip().lower() in cls.EXIT_COMMANDS

    @classmethod
    def get_help_message(cls) -> str:
        """Get the help message for mode usage."""
        return (
            "🤖 Please specify a mode to get started:\n"
            "   • Type 'conversational: [your message]' for friendly chat\n"
            "   • Type 'rephrasing: [your text]' for grammar/text help"
        )
