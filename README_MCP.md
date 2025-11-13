# MCP Server for PydanticAI Conversation Agent

This MCP (Model Context Protocol) server exposes your PydanticAI conversation agent functionality to other applications that support MCP, such as Claude Desktop.

## 🚀 Quick Start

### Prerequisites
- Python 3.14+ with all project dependencies installed
- Your OpenAI API key configured in `.env` file
- MCP client (like Claude Desktop) installed

### Installation

1. **Install the MCP dependency:**
```bash
cd /path/to/pydantic_ai
pip install mcp>=1.0.0
# or with uv
uv add mcp>=1.0.0
```

2. **Ensure your .env file has your OpenAI API key:**
```bash
echo "OPENAI_API_KEY=your_api_key_here" >> .env
```

### Running the MCP Server

#### Option 1: Using the startup script (Recommended)
```bash
python run_mcp_server.py
```

#### Option 2: Direct execution
```bash
python src/mcp/simple_server.py
```

The server will start and communicate via stdio (standard input/output), which is the protocol MCP uses.

## 🔧 Configuration with Claude Desktop

To use this MCP server with Claude Desktop, you need to add it to your Claude Desktop configuration.

### Step 1: Find your Claude Desktop config file

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Add the MCP server configuration

Edit the config file and add your PydanticAI MCP server:

```json
{
  "mcpServers": {
    "pydantic-ai-conversation": {
      "command": "python",
      "args": ["/absolute/path/to/your/pydantic_ai/run_mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}
```

**Important:** Replace `/absolute/path/to/your/pydantic_ai/` with the actual absolute path to your project directory.

### Step 3: Restart Claude Desktop

After saving the configuration, restart Claude Desktop to load the new MCP server.

## 🛠️ Available Tools

Once connected, Claude Desktop will have access to these tools:

### 1. **conversational_chat**
- **Description:** Have a conversational chat with the AI assistant. Maintains context and conversation history.
- **Parameters:**
  - `message` (required): Your message or question for the AI assistant
  - `session_id` (optional): Session ID to maintain conversation context (default: "default")

**Example usage in Claude Desktop:**
```
Use the conversational_chat tool to ask: "What are the benefits of using async/await in Python?"
```

### 2. **rephrase_text**
- **Description:** Improve grammar, clarity, and writing quality of text while preserving meaning and tone.
- **Parameters:**
  - `text` (required): The text to be rephrased and improved

**Example usage in Claude Desktop:**
```
Use the rephrase_text tool to improve: "Me and my friend goes to the store yesterday for buying some groceries."
```

### 3. **get_conversation_stats**
- **Description:** Get statistics about a conversation session including message count and context info.
- **Parameters:**
  - `session_id` (optional): Session ID to get stats for (default: "default")

### 4. **clear_conversation_history**
- **Description:** Clear the conversation history for a specific session.
- **Parameters:**
  - `session_id` (optional): Session ID to clear history for (default: "default")

## 🔍 Session Management

The MCP server supports multiple conversation sessions:

- **Default Session:** If no `session_id` is provided, uses "default"
- **Custom Sessions:** Use any string as a session ID to create isolated conversations
- **Context Preservation:** Each session maintains its own conversation history and context

## 📊 Usage Examples

### Conversational Mode with Session Management

```
1. Use conversational_chat with session_id "project_planning" to ask: "I'm building a web application. What architecture should I consider?"

2. Continue in the same session: Use conversational_chat with session_id "project_planning" to ask: "What about database choices for this architecture?"

3. Check session stats: Use get_conversation_stats with session_id "project_planning"
```

### Text Improvement

```
Use rephrase_text to improve: "The project are going very good and we expect to finish it soon. The team work hard and making good progress."
```

## 🐛 Troubleshooting

### Common Issues

**1. Server won't start**
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Ensure your OpenAI API key is set in `.env` file
- Verify Python path in Claude Desktop config

**2. Claude Desktop doesn't see the tools**
- Check the absolute path in `claude_desktop_config.json`
- Restart Claude Desktop after configuration changes
- Check Claude Desktop logs for error messages

**3. API errors**
- Verify your OpenAI API key is valid and has sufficient credits
- Check internet connectivity
- Monitor server logs for detailed error messages

### Testing the Server

You can test the server independently:

```bash
# Start the server
python run_mcp_server.py

# In another terminal, test with curl (advanced)
# The server uses stdio, so direct HTTP testing isn't applicable
```

### Debug Mode

To see detailed logs, modify the server's logging level:

```python
# In src/mcp/simple_server.py
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security Notes

- Keep your OpenAI API key secure and never commit it to version control
- The MCP server runs locally and communicates only with Claude Desktop
- Each session is isolated and doesn't share data with other sessions
- Conversation history is stored in memory and cleared when the server restarts

## 🚀 Advanced Configuration

### Custom Model Selection

You can modify the server to use different OpenAI models by editing the `DualModeAssistant` initialization:

```python
# In src/mcp/simple_server.py
assistant = DualModeAssistant(model_name="openai:gpt-4o-mini")  # Use mini model
```

### Environment Variables

The server respects these environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `DEFAULT_MODEL`: Default model to use (optional, defaults to "openai:gpt-4o")

## 📝 Development

### Adding New Tools

To add new tools to the MCP server:

1. Add a new `Tool` definition in `handle_list_tools()`
2. Add the tool handler in `handle_call_tool()`
3. Implement the handler method
4. Update this documentation

### Testing Changes

```bash
# Restart the MCP server
# Restart Claude Desktop
# Test the new functionality
```

## 📚 References

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/docs)
- [Claude Desktop MCP Configuration](https://docs.anthropic.com/claude/desktop)
- [PydanticAI Documentation](https://ai.pydantic.dev/)

---

**Need help?** Check the main project README.md for more information about the PydanticAI conversation agent itself.
