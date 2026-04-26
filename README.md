# Dual-Mode Assistan

A professional, high-performance dual-mode AI assistant built with **PydanticAI** and **async/await** architecture for concurrent request processing and optimal performance.

![Python](https://img.shields.io/badge/python-3.14+-blue.svg)
![PydanticAI](https://img.shields.io/badge/PydanticAI-1.7.0+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange.svg)
![Async](https://img.shields.io/badge/async-enabled-purple.svg)

## 🎯 Features

### Dual Operating Modes
- **🗣️ Conversational Mode** - Context-aware friendly chat with conversation history
- **✏️ Rephrasing Mode** - Professional grammar correction and text improvement

### High-Performance Architecture
- **⚡ Async/Await** - Non-blocking operations for better performance
- **🚀 Concurrent Processing** - Handle multiple requests simultaneously
- **🔄 Backward Compatible** - Sync versions of all methods available
- **📦 Modular Design** - Clean separation of concerns with SOLID principles

### Professional Features
- **🎨 Clean Class-Based Architecture** - Maintainable and extensible code
- **🛡️ Type Safety** - Full type hints and validation
- **⚠️ Error Handling** - Graceful failure recovery and user feedback
- **📊 Usage Analytics** - Conversation statistics and metrics
- **🧪 Comprehensive Testing** - Demo script with various scenarios

## 🚀 Quick Start

### Prerequisites
- Python 3.14+
- OpenAI API key

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd pydantic_ai
```

2. **Install dependencies:**
```bash
pip install -e .
# or with uv
uv sync
```

3. **Set up environment:**
```bash
cp .env.example .env
# Add your OpenAI API key to .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### Usage

#### Interactive Mode
```bash
python main.py
```

Then use the dual-mode format:
```
You: conversational: How does machine learning work?
🤖 Machine learning is a fascinating field where...

You: rephrasing: I went to store yesterday and buy some food
✏️  I went to the store yesterday and bought some food.
```

#### Programmatic Usage
```python
import asyncio
from src.core.assistant import DualModeAssistant

async def main():
    assistant = DualModeAssistant()

    # Single request
    result = await assistant.process_single_request(
        "conversational: Explain neural networks"
    )
    print(result["response"])

    # Interactive session
    await assistant.start_interactive_session()

asyncio.run(main())
```

#### Concurrent Processing
```python
async def batch_process():
    assistant = DualModeAssistant()

    requests = [
        "conversational: What is Python?",
        "rephrasing: me and my friend goes to school",
        "conversational: How does async work?",
        "rephrasing: this code work good"
    ]

    # Process all requests concurrently (3-4x faster!)
    tasks = [assistant.process_single_request(req) for req in requests]
    results = await asyncio.gather(*tasks)

    for result in results:
        print(f"✅ {result['response']}")
```

#### Demo Mode
```bash
python demo_dual_mode.py
```

## 🏗️ Architecture

### Project Structure
```
pydantic_ai/
├── main.py                     # Async entry point
├── demo_dual_mode.py          # Comprehensive demo with concurrent examples
├── .env                       # API configuration
├── pyproject.toml            # Project dependencies
├── src/
│   ├── core/                 # Main business logic
│   │   ├── assistant.py      # DualModeAssistant orchestrator
│   │   └── conversation_manager.py # Chat history & context
│   ├── ai/                   # AI agent management
│   │   └── agent_manager.py  # PydanticAI agent wrapper
│   ├── helpers/              # Utility classes
│   │   ├── input_parser.py   # Mode detection & validation
│   │   └── ui_helper.py      # User interface utilities
│   └── scripts/              # Legacy/backup files
├── README.md                 # This file
├── README_ASYNC.md          # Detailed async documentation
└── README_REFACTORED.md     # Architecture details
```

### Component Overview

#### 🎛️ **DualModeAssistant** (Main Orchestrator)
- Coordinates all components
- Manages interactive sessions
- Handles async/sync compatibility
- Provides API-like interface

#### 🤖 **AgentManager** (AI Interface)
- Manages PydanticAI agents
- Handles model configuration
- Provides async and sync methods
- Supports multiple AI models

#### 💬 **ConversationManager** (Context Handling)
- Maintains conversation history
- Manages context windows
- Provides conversation analytics
- Optimizes memory usage

#### 🔍 **InputParser** (Request Processing)
- Validates user input
- Detects operating modes
- Handles edge cases
- Provides structured responses

#### 🎨 **UIHelper** (User Interface)
- Consistent message formatting
- Async/sync input handling
- Progress indicators
- Error display utilities

## 🎮 Usage Examples

### Mode Examples

#### Conversational Mode
```
Input:  conversational: What are the benefits of learning Python?
Output: Python offers numerous benefits including:
        - Easy-to-read syntax that's beginner-friendly
        - Vast ecosystem with libraries for data science, web dev, AI
        - Strong community support and extensive documentation
        - Cross-platform compatibility
        - High demand in job market...
```

#### Rephrasing Mode
```
Input:  rephrasing: The meeting was very productive and we discuss many topics
Output: The meeting was very productive and we discussed many topics.

Input:  rephrasing: This code need to be optimize for better performance
Output: This code needs to be optimized for better performance.
```

### API-Style Usage
```python
# Process single request
result = await assistant.process_single_request("conversational: Hello!")

# Response structure
{
    "success": True,
    "response": "Hello! How can I help you today?",
    "mode": "conversational",
    "original_input": "Hello!"
}

# Error handling
{
    "success": False,
    "error": "Please provide content after the mode label.",
    "mode": "conversational"
}
```

## ⚡ Performance Features

### Async Benefits
- **Concurrent AI Calls**: Process multiple requests simultaneously
- **Non-blocking I/O**: User input doesn't freeze the application
- **Better Resource Usage**: More efficient CPU and memory utilization
- **Scalability**: Handle hundreds of concurrent requests

### Performance Comparison
```python
# Sequential Processing (Old)
for request in requests:
    result = agent.run_sync(request)  # ~2-3 seconds each
# Total: 8-12 seconds for 4 requests

# Concurrent Processing (New)
tasks = [agent.run(req) for req in requests]
results = await asyncio.gather(*tasks)  # ~2-3 seconds total
# Total: 2-3 seconds for 4 requests (75% faster!)
```

## 🛠️ Configuration

### Model Selection
```python
# Use different OpenAI models
assistant = DualModeAssistant(model_name="openai:gpt-4o")
assistant = DualModeAssistant(model_name="openai:gpt-4o-mini")
```

### Conversation History
```python
from src.core.conversation_manager import ConversationManager

# Adjust history length
conversation_manager = ConversationManager(max_history_pairs=5)
```

### Environment Variables
```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Model configuration
DEFAULT_MODEL=openai:gpt-4o
MAX_HISTORY_PAIRS=3
```

## 🧪 Testing & Development

### Run Demo
```bash
python demo_dual_mode.py
```

### Development Setup
```bash
# Install dev dependencies
uv sync --group dev

# Run linting
ruff check .
ruff format .

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### Adding New Features

#### New Operating Mode
1. Extend `Mode` enum in `input_parser.py`
2. Add agent creation in `agent_manager.py`
3. Update parsing logic in `InputParser`
4. Add handling in `DualModeAssistant`

#### Custom Agent
```python
class CustomAgentManager(AgentManager):
    async def get_translation_response(self, text: str, target_lang: str) -> str:
        agent = self._create_translation_agent(target_lang)
        result = await agent.run(text)
        return str(result)
```

## 📊 Monitoring & Analytics

### Conversation Statistics
```python
# Get conversation metrics
stats = assistant.get_conversation_stats()
print(stats)  # {"message_count": 6, "has_context": True}

# Clear conversation history
assistant.clear_conversation_history()
```

### Error Tracking
```python
try:
    result = await assistant.process_single_request("conversational: Hello!")
    if not result["success"]:
        logger.error(f"Request failed: {result['error']}")
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
```

## 🚀 Advanced Usage

### Rate Limiting
```python
import asyncio
from asyncio import Semaphore

async def rate_limited_process(requests, max_concurrent=3):
    semaphore = Semaphore(max_concurrent)

    async def limited_request(request):
        async with semaphore:
            return await assistant.process_single_request(request)

    tasks = [limited_request(req) for req in requests]
    return await asyncio.gather(*tasks)
```

### Timeout Handling
```python
async def process_with_timeout(request, timeout=30):
    try:
        result = await asyncio.wait_for(
            assistant.process_single_request(request),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        return {"success": False, "error": "Request timed out"}
```

### Batch Processing
```python
async def batch_process(requests, batch_size=5):
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i + batch_size]
        tasks = [assistant.process_single_request(req) for req in batch]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result["success"]:
                yield result["response"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following the existing architecture
4. Add tests for new functionality
5. Run linting: `ruff check . && ruff format .`
6. Commit changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for classes and methods
- Maintain async/sync compatibility
- Add error handling for all operations

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **PydanticAI** - For the excellent AI agent framework
- **OpenAI** - For providing powerful language models
- **Python asyncio** - For enabling high-performance concurrent operations

---

## 📚 Documentation

- **[README_ASYNC.md](README_ASYNC.md)** - Detailed async architecture documentation
- **[README_REFACTORED.md](README_REFACTORED.md)** - Class-based architecture details
- **[Demo Script](demo_dual_mode.py)** - Comprehensive usage examples

## 🆘 Troubleshooting

### Common Issues

**API Key Error**
```bash
❌ Failed to start assistant: No OpenAI API key found
```
**Solution**: Add your API key to `.env` file

**Import Error**
```bash
ModuleNotFoundError: No module named 'src'
```
**Solution**: Run from project root or install with `pip install -e .`

**Async Runtime Error**
```bash
RuntimeError: asyncio.run() cannot be called from a running event loop
```
**Solution**: Use `await` in async contexts, not `asyncio.run()`

---

*Built with ❤️ using PydanticAI, Python asyncio, and modern software architecture principles*
