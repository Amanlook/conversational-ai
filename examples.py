#!/usr/bin/env python3
"""
Simple usage examples for the Dual-Mode AI Assistant.
Run this file to see basic functionality without the full demo.
"""

import asyncio

from dotenv import load_dotenv

from src.core.assistant import DualModeAssistant

# Load environment variables
load_dotenv()


async def basic_examples():
    """Basic usage examples."""
    print("🤖 Basic Dual-Mode AI Assistant Examples\n")

    # Initialize assistant
    assistant = DualModeAssistant()

    # Example 1: Conversational mode
    print("1️⃣ Conversational Mode Example:")
    result = await assistant.process_single_request(
        "conversational: What is the capital of France?"
    )
    if result["success"]:
        print("   Question: What is the capital of France?")
        print(f"   Response: {result['response']}\n")

    # Example 2: Rephrasing mode
    print("2️⃣ Rephrasing Mode Example:")
    result = await assistant.process_single_request(
        "rephrasing: I are going to the store for buying some groceries"
    )
    if result["success"]:
        print("   Original: I are going to the store for buying some groceries")
        print(f"   Improved: {result['response']}\n")

    # Example 3: Error handling
    print("3️⃣ Error Handling Example:")
    result = await assistant.process_single_request("invalid input")
    print("   Input: invalid input")
    print(f"   Error: {result['error']}\n")

    # Example 4: Conversation statistics
    print("4️⃣ Conversation Statistics:")
    stats = assistant.get_conversation_stats()
    print(f"   Stats: {stats}\n")


async def concurrent_example():
    """Demonstrate concurrent processing."""
    print("⚡ Concurrent Processing Example\n")

    assistant = DualModeAssistant()

    # Multiple requests to process concurrently
    requests = [
        "conversational: What is Python used for?",
        "rephrasing: me and my friend goes to school together everyday",
        "conversational: Explain machine learning briefly",
        "rephrasing: this program work very good and fast",
    ]

    print("Processing 4 requests concurrently...")

    # Process all requests at once
    tasks = [assistant.process_single_request(req) for req in requests]
    results = await asyncio.gather(*tasks)

    # Display results
    for i, (request, result) in enumerate(zip(requests, results, strict=True), 1):
        mode = "🗣️" if "conversational:" in request else "✏️"
        content = request.split(": ", 1)[1] if ": " in request else request

        print(f"{mode} Request {i}: {content}")
        if result["success"]:
            print(f"   Response: {result['response']}")
        else:
            print(f"   Error: {result['error']}")
        print()


async def main():
    """Run all examples."""
    try:
        await basic_examples()
        await concurrent_example()

        print("✅ All examples completed successfully!")
        print("\n💡 Try the interactive mode: python main.py")
        print("🧪 Or run the full demo: python demo_dual_mode.py")

    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("Make sure you have your OpenAI API key set in .env file")


if __name__ == "__main__":
    asyncio.run(main())
