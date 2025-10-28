from dotenv import load_dotenv
from pydantic_ai import Agent

# Load environment variables from .env file
load_dotenv()


agent = Agent(
    "openai:gpt-4o",  # Use gpt-4o or gpt-4o-mini available through GitHub
    system_prompt=(
        "You are an expert Python developer who writes code that is "
        "correct and efficient."
    ),
)
