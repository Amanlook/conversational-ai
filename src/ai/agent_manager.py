"""AI Agent Manager for handling different types of AI agents."""

from dotenv import load_dotenv
from pydantic_ai import Agent


class AgentManager:
    """Manages AI agents for different modes and operations."""

    def __init__(self, model_name: str = "openai:gpt-4o"):
        """
        Initialize the agent manager.

        Args:
            model_name: The AI model to use for all agents
        """
        load_dotenv()
        self.model_name = model_name
        self._conversation_agent: Agent | None = None
        self._rephrasing_agent: Agent | None = None

    @property
    def conversation_agent(self) -> Agent:
        """Get or create the conversation agent."""
        if self._conversation_agent is None:
            self._conversation_agent = self._create_conversation_agent()
        return self._conversation_agent

    @property
    def rephrasing_agent(self) -> Agent:
        """Get or create the rephrasing agent."""
        if self._rephrasing_agent is None:
            self._rephrasing_agent = self._create_rephrasing_agent()
        return self._rephrasing_agent

    def _create_conversation_agent(self) -> Agent:
        """Create a conversational AI agent."""
        system_prompt = (
            "You are a friendly, helpful, and engaging conversational AI assistant. "
            "Your personality is warm, approachable, and genuinely interested in "
            "helping users. You should:\n"
            "- Be conversational and natural in your responses\n"
            "- Show enthusiasm and interest in the user's questions\n"
            "- Provide helpful and detailed answers when needed\n"
            "- Ask follow-up questions to better understand what the user needs\n"
            "- Use a warm, friendly tone like you're talking to a good friend\n"
            "- Remember context from the conversation to make it flow naturally\n"
            "- Be encouraging and supportive\n"
            "- Keep responses engaging but not overly long unless requested"
        )
        return Agent(self.model_name, system_prompt=system_prompt)

    def _create_rephrasing_agent(self) -> Agent:
        """Create a rephrasing/grammar correction agent."""
        system_prompt = (
            "You are a professional writing assistant specialized in rephrasing "
            "and grammar correction. Your job is to improve text while preserving "
            "the original meaning, tone, and intent. You should:\n"
            "- Fix grammar, spelling, and punctuation errors\n"
            "- Improve clarity and readability\n"
            "- Enhance word choice and sentence structure\n"
            "- Maintain the original tone and style\n"
            "- Preserve the author's voice and intent\n"
            "- Return ONLY the improved version without explanations or commentary\n"
            "- Keep the same level of formality as the original\n"
            "- Don't add new information or change the meaning"
        )
        return Agent(self.model_name, system_prompt=system_prompt)

    async def get_response(
        self, content: str, mode: str, context: str | None = None
    ) -> str:
        """
        Get a response from the appropriate agent based on mode (async version).

        Args:
            content: The user's input content
            mode: The mode ('conversational' or 'rephrasing')
            context: Optional conversation context for conversational mode

        Returns:
            The agent's response

        Raises:
            ValueError: If mode is not supported
        """
        if mode == "conversational":
            prompt = content
            if context:
                prompt = f"Previous conversation:\n{context}\n\nHuman: {content}"
            result = await self.conversation_agent.run(prompt)
            return str(result)
        elif mode == "rephrasing":
            result = await self.rephrasing_agent.run(content)
            return str(result)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    def get_response_sync(
        self, content: str, mode: str, context: str | None = None
    ) -> str:
        """
        Synchronous version of get_response for backward compatibility.

        Args:
            content: The user's input content
            mode: The mode ('conversational' or 'rephrasing')
            context: Optional conversation context for conversational mode

        Returns:
            The agent's response

        Raises:
            ValueError: If mode is not supported
        """
        if mode == "conversational":
            prompt = content
            if context:
                prompt = f"Previous conversation:\n{context}\n\nHuman: {content}"
            result = self.conversation_agent.run_sync(prompt)
            return str(result)
        elif mode == "rephrasing":
            result = self.rephrasing_agent.run_sync(content)
            return str(result)
        else:
            raise ValueError(f"Unsupported mode: {mode}")
