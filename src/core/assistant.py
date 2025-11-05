"""Main dual-mode AI assistant orchestrating all components."""

from src.ai.agent_manager import AgentManager
from src.core.conversation_manager import ConversationManager
from src.helpers.input_parser import InputParser, Mode, ParsedInput
from src.helpers.ui_helper import UIHelper


class DualModeAssistant:
    """Main orchestrator for the dual-mode AI assistant."""

    def __init__(self, model_name: str = "openai:gpt-4o"):
        """
        Initialize the dual-mode assistant.

        Args:
            model_name: The AI model to use for all agents
        """
        self.agent_manager = AgentManager(model_name)
        self.conversation_manager = ConversationManager()
        self.ui_helper = UIHelper()
        self.input_parser = InputParser()

    async def start_interactive_session(self) -> None:
        """Start an interactive chat session."""
        self.ui_helper.print_welcome()

        try:
            await self._chat_loop()
        except KeyboardInterrupt:
            self.ui_helper.print_error("\nConversation interrupted. Goodbye!")
        finally:
            self.ui_helper.print_goodbye()

    async def _chat_loop(self) -> None:
        """Main chat loop handling user interactions."""
        while True:
            try:
                # Get user input
                user_input = await self.ui_helper.get_user_input_async()

                # Parse the input
                parsed_input = self.input_parser.parse(user_input)

                # Handle the parsed input
                if not await self._handle_parsed_input(parsed_input):
                    break  # Exit command received

                self.ui_helper.print_spacing()

            except Exception as e:
                self.ui_helper.print_error(f"Oops! Something went wrong: {e}")
                self.ui_helper.print_error("Let's keep chatting though!")

    async def _handle_parsed_input(self, parsed_input: ParsedInput) -> bool:
        """
        Handle parsed user input and return whether to continue.

        Args:
            parsed_input: The parsed input object

        Returns:
            True to continue the chat loop, False to exit
        """
        # Handle exit command
        if parsed_input.content == "exit":
            return False

        # Handle invalid input
        if not parsed_input.is_valid:
            if parsed_input.mode == Mode.HELP:
                self.ui_helper.print_help()
            else:
                self.ui_helper.print_error(parsed_input.error_message)
            return True

        # Process valid input based on mode
        if parsed_input.mode == Mode.CONVERSATIONAL:
            await self._handle_conversational_mode(parsed_input.content)
        elif parsed_input.mode == Mode.REPHRASING:
            await self._handle_rephrasing_mode(parsed_input.content)

        return True

    async def _handle_conversational_mode(self, content: str) -> None:
        """
        Handle conversational mode interaction.

        Args:
            content: The user's message content
        """
        # Add user message to conversation history
        self.conversation_manager.add_user_message(content)

        # Show thinking indicator
        self.ui_helper.print_thinking_indicator("conversational")

        try:
            # Get AI response
            response = await self.agent_manager.get_response(
                content, "conversational", self.conversation_manager.get_context()
            )

            # Print response
            print(response)

            # Add AI response to history
            self.conversation_manager.add_assistant_message(response)

        except Exception as e:
            self.ui_helper.print_error(f"Sorry, I couldn't process that: {e}")

    async def _handle_rephrasing_mode(self, content: str) -> None:
        """
        Handle rephrasing mode interaction.

        Args:
            content: The text to be rephrased
        """
        # Show thinking indicator
        self.ui_helper.print_thinking_indicator("rephrasing")

        try:
            # Get AI response (no context needed for rephrasing)
            response = await self.agent_manager.get_response(content, "rephrasing")

            # Print response
            print(response)

        except Exception as e:
            self.ui_helper.print_error(f"Sorry, I couldn't rephrase that: {e}")

    async def process_single_request(self, user_input: str) -> dict:
        """
        Process a single request and return the result (async version).

        Args:
            user_input: The raw user input

        Returns:
            Dictionary containing response data and metadata
        """
        parsed_input = self.input_parser.parse(user_input)

        if not parsed_input.is_valid:
            return {
                "success": False,
                "error": parsed_input.error_message,
                "mode": parsed_input.mode.value if parsed_input.mode else None,
            }

        try:
            if parsed_input.mode == Mode.CONVERSATIONAL:
                # For single requests, don't use conversation history
                response = await self.agent_manager.get_response(
                    parsed_input.content, "conversational"
                )
            elif parsed_input.mode == Mode.REPHRASING:
                response = await self.agent_manager.get_response(
                    parsed_input.content, "rephrasing"
                )
            else:
                return {
                    "success": False,
                    "error": "Unsupported mode",
                    "mode": parsed_input.mode.value,
                }

            return {
                "success": True,
                "response": response,
                "mode": parsed_input.mode.value,
                "original_input": parsed_input.content,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "mode": parsed_input.mode.value,
                "original_input": parsed_input.content,
            }

    def process_single_request_sync(self, user_input: str) -> dict:
        """
        Process a single request and return the result (sync version for compatibility).

        Args:
            user_input: The raw user input

        Returns:
            Dictionary containing response data and metadata
        """
        parsed_input = self.input_parser.parse(user_input)

        if not parsed_input.is_valid:
            return {
                "success": False,
                "error": parsed_input.error_message,
                "mode": parsed_input.mode.value if parsed_input.mode else None,
            }

        try:
            if parsed_input.mode == Mode.CONVERSATIONAL:
                # For single requests, don't use conversation history
                response = self.agent_manager.get_response_sync(
                    parsed_input.content, "conversational"
                )
            elif parsed_input.mode == Mode.REPHRASING:
                response = self.agent_manager.get_response_sync(
                    parsed_input.content, "rephrasing"
                )
            else:
                return {
                    "success": False,
                    "error": "Unsupported mode",
                    "mode": parsed_input.mode.value,
                }

            return {
                "success": True,
                "response": response,
                "mode": parsed_input.mode.value,
                "original_input": parsed_input.content,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "mode": parsed_input.mode.value,
                "original_input": parsed_input.content,
            }

    def clear_conversation_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_manager.clear_history()

    def get_conversation_stats(self) -> dict:
        """Get statistics about the current conversation."""
        return {
            "message_count": self.conversation_manager.get_history_length(),
            "has_context": self.conversation_manager.has_context(),
        }
