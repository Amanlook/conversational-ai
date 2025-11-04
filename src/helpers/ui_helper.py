"""UI helper utilities for displaying messages and formatting output."""


class UIHelper:
    """Handles user interface elements like welcome messages and formatting."""

    @staticmethod
    def print_welcome() -> None:
        """Print a friendly welcome message."""
        print("🤖 " + "=" * 65)
        print("   Welcome to your Dual-Mode AI Assistant!")
        print()
        print("   I have two operating modes:")
        print("   1. CONVERSATIONAL: Start with 'conversational:' for friendly chat")
        print("   2. REPHRASING: Start with 'rephrasing:' for grammar/text improvement")
        print()
        print("   Examples:")
        print("   • conversational: How do neural networks work?")
        print("   • rephrasing: I went to store yesterday and buy some food")
        print()
        print("   Type 'quit', 'exit', or 'bye' to end our conversation.")
        print("=" * 68)
        print()

    @staticmethod
    def print_goodbye() -> None:
        """Print a friendly goodbye message."""
        print("\n🤖 Thanks for chatting with me! Have a wonderful day! 👋")

    @staticmethod
    def print_help() -> None:
        """Print help message for mode usage."""
        print("🤖 Please specify a mode to get started:")
        print("   • Type 'conversational: [your message]' for friendly chat")
        print("   • Type 'rephrasing: [your text]' for grammar/text help")
        print()

    @staticmethod
    def print_error(message: str) -> None:
        """Print an error message with consistent formatting."""
        print(f"🤖 {message}")

    @staticmethod
    def print_conversational_response(response: str) -> None:
        """Print a conversational mode response with appropriate formatting."""
        print("🤖 ", end="", flush=True)
        print(response)

    @staticmethod
    def print_rephrasing_response(response: str) -> None:
        """Print a rephrasing mode response with appropriate formatting."""
        print("✏️  ", end="", flush=True)
        print(response)

    @staticmethod
    def get_user_input(prompt: str = "You: ") -> str:
        """Get user input with consistent prompting."""
        return input(prompt).strip()

    @staticmethod
    def print_thinking_indicator(mode: str) -> None:
        """Print a thinking indicator based on mode."""
        if mode == "conversational":
            print("🤖 ", end="", flush=True)
        elif mode == "rephrasing":
            print("✏️  ", end="", flush=True)

    @staticmethod
    def print_spacing() -> None:
        """Print consistent spacing between exchanges."""
        print()
