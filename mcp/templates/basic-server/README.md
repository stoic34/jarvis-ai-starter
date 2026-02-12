# Basic MCP Server Template

A blank template for building your own Model Context Protocol (MCP) server with custom tools.

## What This Is

This template provides the basic structure of an MCP server with TODO comments guiding you through adding your own tools. Use this as a starting point to create custom integrations for Claude.

## How to Use This Template

### Step 1: Copy the Template

Copy this entire directory to a new location and give it a descriptive name:

```bash
# From the jarvis-ai-starter/mcp directory:
cp -r templates/basic-server my-custom-server
cd my-custom-server
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Customize the Server

Open `server.js` in your editor and work through the TODO comments:

1. **Add helper functions** (top of file)
   - Implement the actual logic for your tools
   - These could fetch data, process files, call APIs, etc.

2. **Define your tools** (in `ListToolsRequestSchema` handler)
   - Give each tool a unique name
   - Write a clear description (Claude uses this to decide when to call it)
   - Define the input parameters using JSON schema

3. **Implement tool handlers** (in `CallToolRequestSchema` handler)
   - Extract parameters from the request
   - Validate the parameters
   - Call your helper functions
   - Return formatted results

4. **Customize server metadata**
   - Change the server name and version
   - Update the startup message

### Step 4: Test Your Server

Test that the server starts without errors:

```bash
npm start
```

You should see your custom startup message. Press `Ctrl+C` to stop.

If you see errors, check that:
- All required parameters are defined
- Your tool names are unique
- Your helper functions are properly defined

### Step 5: Configure Claude Code

Add your server to `.claude/settings.json` in your project root:

```json
{
  "mcp": {
    "my-custom-server": {
      "command": "node",
      "args": [
        "/absolute/path/to/my-custom-server/server.js"
      ]
    }
  }
}
```

Use the absolute path (get it with `pwd` from your server directory).

### Step 6: Restart and Test

Restart Claude Code and try asking questions that should trigger your tool.

## Example: Building a Simple Calculator Tool

Here's a concrete example to illustrate the process:

### 1. Add Helper Function

```javascript
// At the top of server.js, after imports:

function calculate(operation, a, b) {
  switch (operation) {
    case 'add':
      return a + b;
    case 'subtract':
      return a - b;
    case 'multiply':
      return a * b;
    case 'divide':
      if (b === 0) throw new Error('Cannot divide by zero');
      return a / b;
    default:
      throw new Error(`Unknown operation: ${operation}`);
  }
}
```

### 2. Define Tool Schema

```javascript
// In the ListToolsRequestSchema handler:

{
  name: 'calculate',
  description: 'Perform basic arithmetic operations (add, subtract, multiply, divide)',
  inputSchema: {
    type: 'object',
    properties: {
      operation: {
        type: 'string',
        enum: ['add', 'subtract', 'multiply', 'divide'],
        description: 'The arithmetic operation to perform',
      },
      a: {
        type: 'number',
        description: 'First number',
      },
      b: {
        type: 'number',
        description: 'Second number',
      },
    },
    required: ['operation', 'a', 'b'],
  },
}
```

### 3. Implement Tool Handler

```javascript
// In the CallToolRequestSchema handler:

if (request.params.name === 'calculate') {
  const { operation, a, b } = request.params.arguments;

  // Validate parameters
  if (!operation || typeof operation !== 'string') {
    throw new Error('operation is required and must be a string');
  }
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new Error('a and b must be numbers');
  }

  try {
    const result = calculate(operation, a, b);
    return {
      content: [
        {
          type: 'text',
          text: `Result: ${a} ${operation} ${b} = ${result}`,
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
}
```

Now Claude can answer questions like "What's 42 times 17?" using your tool!

## Tool Ideas to Get Started

Here are some simple tool ideas to practice with:

### Easy
- **Text counter**: Count words, characters, or lines in text
- **Case converter**: Convert text to uppercase, lowercase, title case
- **JSON formatter**: Pretty-print or minify JSON

### Intermediate
- **File reader**: Read and return contents of local files
- **Simple database**: Store and retrieve key-value pairs
- **URL fetcher**: Fetch and return content from URLs

### Advanced
- **Database query**: Connect to a database and run queries
- **API wrapper**: Wrap a complex API with simpler tool interfaces
- **File processor**: Batch process files (resize images, convert formats, etc.)

## Tips for Building Good Tools

1. **Single responsibility**: Each tool should do one thing well
2. **Clear descriptions**: Claude decides when to use tools based on descriptions
3. **Validate inputs**: Always check that parameters are the right type
4. **Handle errors**: Return helpful error messages, don't crash
5. **Keep it simple**: Start with basic functionality, add features later
6. **Test independently**: Make helper functions easy to test separately

## Common Patterns

### Async Operations

Many tools need to perform async operations (fetch data, read files, etc.):

```javascript
async function fetchData(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error ${response.status}`);
  }
  return await response.json();
}
```

### Multiple Tools

One server can provide multiple tools. Just add more objects to the tools array and more handlers in the CallToolRequestSchema handler.

### Shared State

If your tools need to share state, define it at the module level:

```javascript
const cache = new Map();

function getCached(key) {
  return cache.get(key);
}

function setCached(key, value) {
  cache.set(key, value);
}
```

## Troubleshooting

### Server won't start
- Check for syntax errors in your code
- Verify all dependencies are installed (`npm install`)
- Look at the error message for clues

### Tool not being called
- Check that the tool description clearly explains what it does
- Make sure the tool name is unique
- Verify the inputSchema matches what Claude is trying to pass

### Parameters are undefined
- Check that parameter names in inputSchema match what you're extracting
- Verify required parameters are listed in the `required` array
- Use `request.params.arguments?.paramName` to safely access parameters

## Next Steps

1. **Start simple**: Build a single-tool server with basic functionality
2. **Test thoroughly**: Try various inputs to ensure it works correctly
3. **Iterate**: Add features, improve error handling, optimize performance
4. **Study examples**: Look at the weather example for a complete working server
5. **Read the docs**: Explore the official MCP documentation for advanced features

## Resources

- **MCP Specification**: https://spec.modelcontextprotocol.io/
- **MCP SDK**: https://github.com/modelcontextprotocol/sdk
- **Claude MCP Guide**: https://docs.anthropic.com/en/docs/build-with-claude/mcp
- **JSON Schema**: https://json-schema.org/ (for defining inputSchema)

Happy building!
