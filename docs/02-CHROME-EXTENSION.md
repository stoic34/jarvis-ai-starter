# Chrome Extension: Give Your Agent Eyes and Hands

Claude Code can read files and run commands. But with the Chrome extension, it can also **see and interact with websites**.

This is how your agent will help you set up Google integrations without you having to navigate Google Cloud Console yourself.

**Time required:** 10-15 minutes

---

## Why Browser Control Matters

Without the Chrome extension, setting up APIs looks like this:

1. You open Google Cloud Console
2. You try to find the right menu
3. You click through 15 screens
4. You get confused about which button to click
5. You paste things in the wrong place
6. You spend an hour on something that should take 10 minutes

**With the Chrome extension:**

1. You tell your agent: "Set up Gmail access for me"
2. Claude opens the browser and navigates for you
3. Claude says: "Click the blue 'Authorize' button"
4. You click
5. Done

**The agent handles navigation. You handle authorization.**

This is possible because your alias includes `--chrome`, which enables browser control.

---

## Step 1: Install Claude for Chrome

1. Open Chrome
2. Go to the [Chrome Web Store](https://chrome.google.com/webstore)
3. Search for "Claude for Chrome" (by Anthropic)
4. Click **Add to Chrome**
5. Confirm by clicking **Add extension**

### Pin It to Your Toolbar

1. Click the puzzle piece icon (Extensions) in Chrome toolbar
2. Find "Claude for Chrome"
3. Click the pin icon

You'll see the Claude icon in your toolbar.

---

## Step 2: Connect to Claude Code

The Chrome extension needs to communicate with Claude Code running in your terminal.

**Launch your agent** (using your alias):
```bash
jarvis
```

The `--chrome` flag in your alias tells Claude Code to look for the Chrome extension.

**In Chrome:**
1. Click the Claude icon in your toolbar
2. It should show "Connected" or similar status
3. If prompted, allow the connection

---

## Step 3: Test Browser Control

Let's verify Claude can control your browser.

**Say to your agent:**
> "Test browser control by opening google.com and taking a screenshot"

Claude should:
1. Open a new Chrome tab
2. Navigate to google.com
3. Take a screenshot
4. Show you the result or confirm success

**If this works, browser control is ready.**

---

## What Your Agent Can Do in the Browser

With browser control enabled, your agent can:

### Navigate and Read
- Open any URL
- Read page content
- Extract text from articles
- Scroll through pages

### Interact
- Click buttons and links
- Fill out forms
- Select dropdowns
- Handle popups

### Capture
- Take screenshots
- Record actions as GIFs
- Save page content

### Research
- Search Google
- Gather information from multiple sites
- Compare data across pages

---

## What Your Agent Cannot Do

For security, your agent will **not**:

- Enter passwords for you
- Enter credit card information
- Accept terms and conditions without asking
- Download files without permission
- Access pages requiring login (unless you log in first)

**The rule:** Your agent navigates, you authorize.

---

## Common Use Cases

### Research
> "Research the top 5 CRM tools for small businesses, compare their pricing, and summarize in a table"

### Data Extraction
> "Go to [URL] and extract the product names and prices into a spreadsheet format"

### Form Assistance
> "Help me fill out this job application form—I'll give you the details and you navigate"

### API Setup (Coming Next)
> "Set up gogcli by navigating Google Cloud Console and telling me when to click"

---

## Troubleshooting

### "Not connected" in Chrome extension

- Make sure Claude Code is running with the `--chrome` flag
- Try restarting both the terminal and Chrome
- Check that the extension is enabled (not disabled in Chrome settings)

### Claude says it can't control the browser

- Verify your alias includes `--chrome`
- Try launching manually with the full command:
  ```bash
  npx @anthropic-ai/claude-code --dangerously-skip-permissions --chrome
  ```

### Screenshots are blank

- Some pages block screenshots (banking sites, etc.)
- Try a different page to verify it works
- Check Chrome's permissions for screen capture

### "Permission denied" for certain actions

This is intentional. Claude will ask before:
- Downloading files
- Entering form data
- Clicking "submit" or "purchase" buttons

Just confirm when asked.

---

## Security Notes

**Browser control is powerful.** A few safety tips:

1. **Don't use on banking sites**: Even though Claude won't enter passwords, avoid navigating to sensitive financial pages
2. **Watch what's happening**: Browser control is visible—you can see what Claude is doing
3. **Claude can only access open tabs**: It can't access private browsing or other browser profiles
4. **You control authorization**: For any OAuth flow, YOU click the authorize button

---

## What You've Accomplished

- Installed Claude for Chrome extension
- Connected it to Claude Code
- Verified browser control works
- Understand what's possible (and what's protected)

**Next:** Set up Google integration with AI-guided navigation → [03-GOOGLE-INTEGRATION.md](03-GOOGLE-INTEGRATION.md)

---

*Time to complete: 10-15 minutes*
