# Browser Integration Setup

Claude for Chrome extends your AI assistant's capabilities to the web browser, enabling research, data extraction, and web automation.

## What It Enables

With browser integration, your AI can:
- Navigate to websites and read content
- Extract data from web pages
- Fill out forms
- Take screenshots
- Research topics across multiple sources
- Interact with web applications

## Installation

### Step 1: Install the Extension

1. Open Chrome
2. Go to the Chrome Web Store
3. Search for "Claude for Chrome" (by Anthropic)
4. Click "Add to Chrome"
5. Confirm the installation

### Step 2: Configure the Extension

1. Click the Claude icon in your Chrome toolbar
2. Sign in with your Anthropic account (same as Claude Code)
3. Grant the requested permissions

### Step 3: Enable MCP Connection

The extension communicates with Claude Code via MCP (Model Context Protocol).

1. In Claude Code, the browser tools should appear automatically
2. Test by asking: "Take a screenshot of google.com"

## How It Works

When you ask your AI to do something web-related:

1. AI determines if browser automation is needed
2. Opens or navigates to the relevant page
3. Reads content, clicks buttons, fills forms as needed
4. Returns results to your conversation

## Example Uses

### Web Research
```
Research the top 5 project management tools and compare their pricing.
```

### Data Extraction
```
Go to [website] and extract the contact information.
```

### Form Filling
```
Fill out the contact form on [website] with my information.
```

### Screenshots
```
Take a screenshot of my Google Analytics dashboard.
```

## Privacy & Security

**Important considerations:**

- The browser extension can see pages you visit when activated
- Your AI will ask before taking actions on sensitive sites
- Never ask AI to enter passwords or financial information
- Be cautious with pages that have sensitive data visible

**Best practices:**
- Only use browser automation for research and non-sensitive tasks
- Review what pages AI navigates to
- Don't leave sensitive pages (banking, medical) open during sessions

## Troubleshooting

**Extension not connecting?**
- Make sure both Claude Code and the extension are using the same account
- Try restarting Claude Code
- Check that the extension has necessary permissions in Chrome settings

**Pages not loading correctly?**
- Some sites block automated access
- Try a different approach or research manually
- Wait a moment and retry

**AI can't see page content?**
- Some pages use JavaScript that takes time to load
- Ask AI to "wait 3 seconds then read the page"
- Dynamic content may require scrolling first

## Without Browser Integration

If you prefer not to use browser integration, your AI can still:
- Search the web (text results)
- Fetch and read public web pages
- Research using web search

Browser automation just adds the ability to interact with pages, not just read them.

---

*Browser integration is optional but powerful. Start with basic use and expand as you get comfortable.*
