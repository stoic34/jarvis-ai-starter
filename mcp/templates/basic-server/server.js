#!/usr/bin/env node

/**
 * Basic MCP Server Template
 *
 * This is a blank template for building your own Model Context Protocol (MCP) server.
 * Follow the TODO comments to add your custom tools.
 *
 * Steps to use this template:
 * 1. Copy this directory to a new location
 * 2. Run `npm install` to install dependencies
 * 3. Fill in the TODOs below with your tool logic
 * 4. Test with `npm start`
 * 5. Add to Claude Code's .claude/settings.json
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

// ============================================================================
// TODO: Add your helper functions here
// ============================================================================
//
// Example:
// async function myCustomFunction(param) {
//   // Your logic here
//   return result;
// }
//
// This is where you put the actual implementation of your tools.
// These functions will be called by the tool handlers below.

/**
 * Main server setup
 */
async function main() {
  // Create the MCP server
  const server = new Server(
    {
      // TODO: Customize your server name and version
      name: 'my-custom-server',
      version: '1.0.0',
    },
    {
      capabilities: {
        tools: {},  // This server provides tools
      },
    }
  );

  // ============================================================================
  // Handle "list tools" - Tell Claude what tools are available
  // ============================================================================
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        // TODO: Define your tools here
        // Each tool needs:
        // - name: unique identifier for the tool
        // - description: what the tool does (Claude uses this to decide when to call it)
        // - inputSchema: JSON schema defining the parameters
        //
        // Example:
        // {
        //   name: 'my_tool',
        //   description: 'Does something useful with the provided input',
        //   inputSchema: {
        //     type: 'object',
        //     properties: {
        //       param1: {
        //         type: 'string',
        //         description: 'Description of this parameter',
        //       },
        //       param2: {
        //         type: 'number',
        //         description: 'Another parameter (optional)',
        //       },
        //     },
        //     required: ['param1'],  // List required parameters
        //   },
        // },
      ],
    };
  });

  // ============================================================================
  // Handle "call tool" - Execute tools when Claude requests them
  // ============================================================================
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    // TODO: Implement your tool handlers
    //
    // Template for adding a tool handler:
    //
    // if (request.params.name === 'my_tool') {
    //   // Extract parameters from the request
    //   const param1 = request.params.arguments?.param1;
    //   const param2 = request.params.arguments?.param2;
    //
    //   // Validate parameters
    //   if (!param1 || typeof param1 !== 'string') {
    //     throw new Error('param1 is required and must be a string');
    //   }
    //
    //   try {
    //     // Call your helper function
    //     const result = await myCustomFunction(param1, param2);
    //
    //     // Return the result to Claude
    //     return {
    //       content: [
    //         {
    //           type: 'text',
    //           text: result,
    //         },
    //       ],
    //     };
    //   } catch (error) {
    //     // Handle errors gracefully
    //     return {
    //       content: [
    //         {
    //           type: 'text',
    //           text: `Error: ${error.message}`,
    //         },
    //       ],
    //       isError: true,
    //     };
    //   }
    // }

    // If we get here, Claude requested an unknown tool
    throw new Error(`Unknown tool: ${request.params.name}`);
  });

  // ============================================================================
  // Set up communication transport (stdio)
  // ============================================================================
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // TODO: Customize your startup message
  console.error('My Custom MCP server running on stdio');
}

// Start the server
main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
