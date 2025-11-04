"""Conversation management utilities for maintaining chat history and context."""


class ConversationManager:
    """Manages conversation history and context for conversational mode."""

    def __init__(self, max_history_pairs: int = 3):
        """
        Initialize the conversation manager.

        Args:
            max_history_pairs: Maximum number of exchange pairs to keep in context
        """
        self.max_history_pairs = max_history_pairs
        self._history: list[str] = []

    def add_user_message(self, message: str) -> None:
        """
        Add a user message to the conversation history.

        Args:
            message: The user's message content
        """
        self._history.append(f"Human: {message}")

    def add_assistant_message(self, message: str) -> None:
        """
        Add an assistant message to the conversation history.

        Args:
            message: The assistant's response content
        """
        self._history.append(f"AI: {message}")

    def get_context(self) -> str | None:
        """
        Get the conversation context for the AI agent.

        Returns:
            Formatted conversation context string, or None if no history exists
        """
        if len(self._history) <= 1:
            return None

        # Get the last few exchanges (max_history_pairs * 2 messages)
        max_messages = self.max_history_pairs * 2
        recent_history = self._history[-max_messages:]

        return "\n".join(recent_history)

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self._history.clear()

    def get_history_length(self) -> int:
        """Get the number of messages in history."""
        return len(self._history)

    def has_context(self) -> bool:
        """Check if there's conversation context available."""
        return len(self._history) > 1

    def get_last_exchange(self) -> tuple[str | None, str | None]:
        """
        Get the last user message and AI response pair.

        Returns:
            Tuple of (last_user_message, last_ai_response) or (None, None)
        """
        if len(self._history) < 2:
            return None, None

        # Look for the last Human: and AI: pair
        last_human = None
        last_ai = None

        for message in reversed(self._history):
            if message.startswith("AI: ") and last_ai is None:
                last_ai = message[4:]  # Remove "AI: " prefix
            elif message.startswith("Human: ") and last_human is None:
                last_human = message[7:]  # Remove "Human: " prefix
                if last_ai is not None:
                    break

        return last_human, last_ai

    def format_context_prompt(self, current_message: str) -> str:
        """
        Format the current message with conversation context for the AI agent.

        Args:
            current_message: The current user message

        Returns:
            Formatted prompt including context if available
        """
        context = self.get_context()
        if context:
            return f"Previous conversation:\n{context}\n\nHuman: {current_message}"
        else:
            return current_message
