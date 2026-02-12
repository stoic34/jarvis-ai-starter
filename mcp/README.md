# Model Context Protocol (MCP) Servers

## What is MCP?

**Model Context Protocol (MCP)** is an open standard that allows AI assistants like Claude to connect to external tools and data sources. Think of it as a universal adapter that lets your AI assistant access capabilities beyond its built-in features.

Instead of every tool needing custom integration code, MCP provides a standardized way for:
- Your AI assistant to discover what tools are available
- Your AI to understand how to use those tools
- Tools to send data back to your AI in a consistent format

## Why Does This Matter?

With MCP, you can extend your AI assistant to:
- **Access real-time data** (weather, stock prices, news)
- **Interact with external services** (databases, APIs, file systems)
- **Integrate with your tools** (calendar, task managers, note-taking apps)
- **Add custom capabilities** specific to your workflow

All without waiting for the AI provider to build native integrations.

## How It Works (Conceptually)

```
┌─────────────────┐         ┌──────────────────┐
│  Claude Code    │ ◄─────► │   MCP Server     │
│  (AI Assistant) │   MCP   │   (Your Tool)    │
└─────────────────┘         └──────────────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │  External Data   │
                            │  or Service      │
                            └──────────────────┘
```

1. **You configure** Claude Code to connect to an MCP server
2. **The MCP server** exposes tools (like "get weather" or "search database")
3. **Claude discovers** these tools and understands their parameters
4. **When relevant**, Claude calls the tools to help answer your questions
5. **Results flow back** through MCP to inform Claude's responses

## What's Included Here

This directory contains:

- **`examples/`** — Working MCP servers you can run and learn from
  - `weather/` — Simple weather lookup tool (no API key needed)
- **`templates/`** — Starting points for building your own MCP servers
  - `basic-server/` — Blank template with structure and comments

## Prerequisites

To run these examples, you'll need:

- **Node.js** (version 18 or higher) — [Download here](https://nodejs.org/)
- **Claude Code CLI** — The examples assume you're using Claude Code

Check your Node.js version:
```bash
node --version
```

## How to Use an MCP Server

### Step 1: Choose or Build a Server

Start with an example from `examples/` or copy the `templates/basic-server/` template.

### Step 2: Install Dependencies

Navigate to the server directory and install packages:
```bash
cd mcp/examples/weather
npm install
```

### Step 3: Test the Server

Most MCP servers can be tested directly:
```bash
node server.js
```

### Step 4: Configure Claude Code

Add the MCP server to your `.claude/settings.json` file. Create or edit this file in your project root:

```json
{
  "mcp": {
    "weather": {
      "command": "node",
      "args": [
        "/absolute/path/to/jarvis-ai-starter/mcp/examples/weather/server.js"
      ]
    }
  }
}
```

**Important**: Use absolute paths, not relative paths like `./mcp/...`

### Step 5: Restart Claude Code

After updating `settings.json`, restart Claude Code to load the new MCP server.

### Step 6: Use It

Claude will automatically discover the new tools. You can now ask questions like:
- "What's the weather in San Francisco?"
- "Is it going to rain in London today?"

## Building Your Own MCP Server

1. **Copy the template**:
   ```bash
   cp -r mcp/templates/basic-server mcp/my-custom-server
   cd mcp/my-custom-server
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Edit `server.js`** — Add your tools following the TODO comments

4. **Test it** — Run `node server.js` and verify it starts without errors

5. **Configure Claude Code** — Add your server to `.claude/settings.json`

6. **Iterate** — Test with Claude, refine your tools, repeat

## Official MCP Documentation

For deeper technical details, see:
- **MCP Specification**: https://spec.modelcontextprotocol.io/
- **MCP SDK Documentation**: https://github.com/modelcontextprotocol/sdk
- **Claude MCP Guide**: https://docs.anthropic.com/en/docs/build-with-claude/mcp

## Learning Path

1. **Start with the weather example** — Run it, see how it works
2. **Read the code** — The comments explain each part
3. **Modify the weather example** — Change the city format or add more data
4. **Build from the template** — Create a simple tool for your own use case
5. **Explore advanced patterns** — Multiple tools, error handling, async operations

## Getting Help

If you run into issues:
- Check that Node.js is installed and up to date
- Verify absolute paths in your `.claude/settings.json`
- Look at the console output when Claude Code starts (it logs MCP server connections)
- Review the official MCP documentation linked above

Happy building!
