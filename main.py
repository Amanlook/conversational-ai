from dotenv import load_dotenv

from src.scripts.agents import conversation_agent, rephrasing_agent

# Load environment variables from .env file
load_dotenv()


def print_welcome():
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


def print_goodbye():
    """Print a friendly goodbye message."""
    print("\n🤖 Thanks for chatting with me! Have a wonderful day! 👋")


def parse_user_input(user_input):
    """Parse user input to determine mode and extract content."""
    user_input = user_input.strip()

    if user_input.lower().startswith("conversational:"):
        return "conversational", user_input[15:].strip()
    elif user_input.lower().startswith("rephrasing:"):
        return "rephrasing", user_input[11:].strip()
    else:
        return "help", user_input


def chat():
    """Main conversation loop with dual-mode support."""
    print_welcome()

    conversation_history = []

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            # Check for exit commands
            if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
                break

            # Skip empty inputs
            if not user_input:
                print("🤖 I didn't catch that. Could you say something?")
                continue

            # Parse input to determine mode
            mode, content = parse_user_input(user_input)

            # Handle different modes
            if mode == "help":
                print("🤖 Please specify a mode to get started:")
                print("   • Type 'conversational: [your message]' for friendly chat")
                print("   • Type 'rephrasing: [your text]' for grammar/text help")
                print()
                continue

            # Skip if content is empty after mode parsing
            if not content:
                print("🤖 Please provide some content after the mode label.")
                continue

            # Process based on mode
            if mode == "conversational":
                # Add to conversation history for context (only for conversational)
                conversation_history.append(f"Human: {content}")

                # Create context-aware prompt
                if len(conversation_history) > 1:
                    context = "\n".join(conversation_history[-6:])  # Last 3 exchanges
                    full_prompt = (
                        f"Previous conversation:\n{context}\n\nHuman: {content}"
                    )
                else:
                    full_prompt = content

                # Get AI response
                print("🤖 ", end="", flush=True)
                result = conversation_agent.run_sync(full_prompt)
                print(f"{result}")

                # Add AI response to history
                conversation_history.append(f"AI: {result}")

            elif mode == "rephrasing":
                # For rephrasing mode, don't use conversation history
                print("✏️  ", end="", flush=True)
                result = rephrasing_agent.run_sync(content)
                print(f"{result}")

            print()  # Add spacing between exchanges

        except KeyboardInterrupt:
            print("\n🤖 Conversation interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"🤖 Oops! Something went wrong: {e}")
            print("🤖 Let's keep chatting though!")


if __name__ == "__main__":
    try:
        chat()
    except KeyboardInterrupt:
        pass
    finally:
        print_goodbye()
