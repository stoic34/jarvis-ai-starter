#!/usr/bin/env node

/**
 * Weather MCP Server Example
 *
 * This is a simple Model Context Protocol (MCP) server that provides a weather
 * lookup tool to AI assistants like Claude.
 *
 * What it does:
 * - Exposes a "get_weather" tool that Claude can call
 * - Fetches weather data from wttr.in (a free weather API)
 * - Returns formatted weather information
 *
 * Key MCP concepts demonstrated:
 * - Server setup using the MCP SDK
 * - Tool registration (defining what the tool does)
 * - Tool handler (implementing the actual functionality)
 * - Error handling
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

/**
 * Fetch weather data from wttr.in
 *
 * wttr.in is a free weather service that doesn't require an API key.
 * We use the ?format=j1 parameter to get JSON output.
 *
 * @param {string} city - The city name to look up
 * @returns {Promise<Object>} Weather data
 */
async function getWeather(city) {
  const response = await fetch(
    `https://wttr.in/${encodeURIComponent(city)}?format=j1`
  );

  if (!response.ok) {
    throw new Error(`Weather API error: ${response.status} ${response.statusText}`);
  }

  return await response.json();
}

/**
 * Format weather data into a human-readable string
 *
 * @param {Object} data - Raw weather data from wttr.in
 * @returns {string} Formatted weather description
 */
function formatWeather(data) {
  const current = data.current_condition[0];
  const location = data.nearest_area[0];

  return `
Weather for ${location.areaName[0].value}, ${location.country[0].value}

Current Conditions:
- Temperature: ${current.temp_C}°C (${current.temp_F}°F)
- Feels Like: ${current.FeelsLikeC}°C (${current.FeelsLikeF}°F)
- Condition: ${current.weatherDesc[0].value}
- Humidity: ${current.humidity}%
- Wind: ${current.windspeedKmph} km/h ${current.winddir16Point}
- Visibility: ${current.visibility} km
- UV Index: ${current.uvIndex}
  `.trim();
}

/**
 * Create and configure the MCP server
 */
async function main() {
  // Create a new MCP server instance
  // The server handles communication between Claude and this tool
  const server = new Server(
    {
      name: 'weather-server',
      version: '1.0.0',
    },
    {
      capabilities: {
        tools: {},  // Declare that this server provides tools
      },
    }
  );

  /**
   * Handle the "list tools" request
   *
   * When Claude connects, it asks "what tools do you have?"
   * This handler responds with the list of available tools and their schemas.
   */
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: 'get_weather',
          description: 'Get current weather conditions for a city. Provides temperature, conditions, humidity, wind, and more.',
          inputSchema: {
            type: 'object',
            properties: {
              city: {
                type: 'string',
                description: 'The city name to get weather for (e.g., "San Francisco", "London", "Tokyo")',
              },
            },
            required: ['city'],
          },
        },
      ],
    };
  });

  /**
   * Handle the "call tool" request
   *
   * When Claude decides to use a tool, it sends a "call tool" request.
   * This handler executes the requested tool and returns the result.
   */
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    // Check which tool Claude wants to use
    if (request.params.name === 'get_weather') {
      // Extract the city parameter from the request
      const city = request.params.arguments?.city;

      // Validate that we got a city name
      if (!city || typeof city !== 'string') {
        throw new Error('City parameter is required and must be a string');
      }

      try {
        // Fetch weather data from the API
        const weatherData = await getWeather(city);

        // Format it nicely
        const formattedWeather = formatWeather(weatherData);

        // Return the result to Claude
        // The content array can contain multiple pieces of content
        return {
          content: [
            {
              type: 'text',
              text: formattedWeather,
            },
          ],
        };
      } catch (error) {
        // If something goes wrong, return a helpful error message
        return {
          content: [
            {
              type: 'text',
              text: `Error fetching weather for ${city}: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    }

    // If Claude asks for a tool we don't recognize, throw an error
    throw new Error(`Unknown tool: ${request.params.name}`);
  });

  /**
   * Set up the transport layer
   *
   * MCP servers communicate via standard input/output (stdio).
   * This is how Claude sends requests and receives responses.
   */
  const transport = new StdioServerTransport();

  // Connect the server to the transport
  await server.connect(transport);

  // Log that we're running (this goes to stderr, not stdout, so it won't interfere with MCP communication)
  console.error('Weather MCP server running on stdio');
}

// Start the server
main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
