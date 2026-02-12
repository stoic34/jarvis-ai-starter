# Weather MCP Server Example

A simple Model Context Protocol (MCP) server that provides weather lookup capabilities to AI assistants.

## What This Does

This MCP server exposes a single tool called `get_weather` that:
- Takes a city name as input
- Fetches current weather data from wttr.in (a free weather API)
- Returns formatted weather information including temperature, conditions, humidity, wind, and more

## How to Run It

### 1. Install Dependencies

First, make sure you have Node.js installed (version 18 or higher):
```bash
node --version
```

Then install the required packages:
```bash
npm install
```

### 2. Test the Server

You can test that the server starts without errors:
```bash
npm start
```

You should see:
```
Weather MCP server running on stdio
```

Press `Ctrl+C` to stop it. The server is now ready to be used with Claude Code.

### 3. Configure Claude Code

Add this server to your `.claude/settings.json` file. If the file doesn't exist, create it in your project root:

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

**Important**: Replace `/absolute/path/to/` with the actual full path to your jarvis-ai-starter directory.

To get the absolute path, run this from the weather directory:
```bash
pwd
```

### 4. Restart Claude Code

After updating `settings.json`, restart Claude Code to load the MCP server.

### 5. Try It Out

Ask Claude questions like:
- "What's the weather in San Francisco?"
- "Is it going to rain in London?"
- "What's the temperature in Tokyo right now?"

Claude will automatically use the `get_weather` tool to answer your questions.

## How It Works

Let's break down the key parts of `server.js`:

### 1. Server Setup
```javascript
const server = new Server(
  { name: 'weather-server', version: '1.0.0' },
  { capabilities: { tools: {} } }
);
```
Creates an MCP server that declares it provides tools.

### 2. Tool Registration
```javascript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [{
      name: 'get_weather',
      description: 'Get current weather...',
      inputSchema: { /* parameters */ }
    }]
  };
});
```
Tells Claude what tools are available and how to use them.

### 3. Tool Handler
```javascript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === 'get_weather') {
    const city = request.params.arguments?.city;
    const weatherData = await getWeather(city);
    return { content: [{ type: 'text', text: formatWeather(weatherData) }] };
  }
});
```
Executes the tool when Claude calls it.

### 4. Communication Transport
```javascript
const transport = new StdioServerTransport();
await server.connect(transport);
```
Sets up stdin/stdout communication with Claude.

## Troubleshooting

### Server won't start
- Check that you ran `npm install` first
- Verify Node.js version is 18 or higher: `node --version`

### Claude can't find the tool
- Check that the path in `.claude/settings.json` is absolute (starts with `/`)
- Verify the path points to `server.js` exactly
- Restart Claude Code after changing `settings.json`

### Weather lookup fails
- Check your internet connection
- The wttr.in service might be temporarily down (try again in a few minutes)
- Try a different city name or use a more specific name like "San Francisco, CA"

## Customizing This Example

Want to modify this example? Here are some ideas:

### Add More Weather Details
The wttr.in API returns forecast data. Modify `formatWeather()` to include:
- 3-day forecast
- Sunrise/sunset times
- Air pressure

### Support Different Units
Add a `units` parameter (metric/imperial) to the tool schema and use it in the API call.

### Cache Results
Store recent weather lookups in memory to avoid repeated API calls for the same city.

### Different Weather API
Replace `getWeather()` to use a different weather service like OpenWeatherMap or WeatherAPI.

## What You Learned

By studying this example, you learned:
- How to structure an MCP server
- How to define a tool with parameters
- How to handle tool calls from Claude
- How to fetch external data and return it
- How to handle errors gracefully

Use this as a starting point to build your own MCP servers!

## Next Steps

1. **Read the code** — Open `server.js` and read through the comments
2. **Modify it** — Change the weather format or add more data
3. **Build your own** — Copy the `templates/basic-server/` template to create a new tool
4. **Go deeper** — Read the official MCP documentation: https://spec.modelcontextprotocol.io/
