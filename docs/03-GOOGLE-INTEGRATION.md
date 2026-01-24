# Google Integration: Email, Calendar, and More

This is the most important integration. Once your agent can access Gmail and Google Calendar, it becomes genuinely useful for daily work.

**Time required:** 20-30 minutes

---

## What is gogcli?

**gogcli** (Google CLI) is a command-line tool that lets your AI agent interact with Google Workspace:

| Service | What Your Agent Can Do |
|---------|------------------------|
| **Gmail** | Search emails, read threads, create drafts |
| **Calendar** | View events, create meetings, check availability |
| **Contacts** | Look up people, find email addresses |
| **Drive** | Read documents, create files |

### Why a CLI? Why Not Just Use Gmail in the Browser?

Great question. Here's why CLI tools are essential for AI agents:

**Browser limitations:**
- Your agent would need to click through Gmail's interface
- Loading times, popups, and UI changes break automation
- Can't process hundreds of emails efficiently
- Visual navigation is slow

**CLI advantages:**
- Direct API access—fast and reliable
- Process 100 emails in seconds, not minutes
- Structured data your agent can actually parse
- Works the same way every time
- No UI changes to break things

**Example comparison:**

*Browser approach:* "Click inbox, scroll down, find email from Sarah, click it, read it, click reply, type response..."

*CLI approach:* `gogcli gmail search "from:sarah" --max 10` → Instant results your agent can process.

### CLI = Command Line Interface

When we say "CLI," we mean a text-based tool. Instead of clicking buttons, you type commands.

Your AI agent is **built** for CLI tools. It can type commands much faster than it can click through interfaces.

---

## What Can You Do With gogcli?

Once set up, you can ask your agent things like:

### Email
> "Scan my inbox for anything urgent in the last 24 hours"

> "Find all emails from John about the project proposal"

> "Draft a reply to Sarah's email about the timeline"

> "Summarize the email thread with the subject 'Q4 Budget'"

### Calendar
> "What do I have scheduled this week?"

> "Block 2 hours tomorrow morning for deep work"

> "Find a time next week when both John and I are free"

> "Add a reminder for the board meeting on Friday"

### Contacts
> "What's Sarah's email address?"

> "Look up everyone from Acme Corp in my contacts"

> "Add this new contact from the business card"

### Drive
> "Create a new document with my meeting notes"

> "Find the project proposal I worked on last month"

> "Share this document with the team"

---

## Step 1: Install gogcli

### Mac (Homebrew)

```bash
brew install gogcli/tap/gogcli
```

### Windows

1. Go to [github.com/gogcli/gogcli/releases](https://github.com/gogcli/gogcli/releases)
2. Download `gogcli_windows_amd64.zip`
3. Extract the zip
4. Move `gogcli.exe` to a folder in your PATH

**Or let Claude help:**
> "Download and install gogcli for Windows"

Claude can navigate the download and help you set up the PATH.

### Verify Installation

```bash
gogcli --version
```

You should see a version number.

---

## Step 2: Set Up Google Cloud Credentials

This is where most people get stuck. Google Cloud Console is confusing.

**Good news:** Claude can navigate it for you.

### AI-Guided Setup

**Say to your agent:**
> "Set up Google Cloud credentials for gogcli. Navigate the Cloud Console for me and tell me when I need to click or authorize."

Claude will:
1. Open Google Cloud Console in your browser
2. Help you create a project (if needed)
3. Enable the Gmail, Calendar, and other APIs
4. Create OAuth credentials
5. Guide you through the consent screen setup
6. Download the credentials file
7. Tell you where to put it

**You handle:**
- Clicking "Authorize" buttons
- Logging into your Google account
- Confirming consent screens

**Claude handles:**
- Navigating the confusing menus
- Clicking through the setup screens
- Finding the right buttons
- Dismissing popups

### What's Happening Behind the Scenes

When you set up Google Cloud credentials, you're:

1. **Creating a "project"** in Google Cloud (free)
2. **Enabling APIs** that allow external access to Gmail, Calendar, etc.
3. **Creating OAuth credentials** so gogcli can authenticate
4. **Setting up a consent screen** that you'll see when authorizing

This is a one-time setup. Once done, you won't need to touch Google Cloud Console again.

---

## Step 3: Authenticate gogcli

Once credentials are set up, authenticate:

```bash
gogcli auth login
```

This opens a browser window where you:
1. Select your Google account
2. Review the permissions
3. Click "Allow"

You'll see a success message in the terminal.

---

## Step 4: Test Your Connection

### Test Gmail

```bash
gogcli gmail search "is:unread" --max 5
```

You should see your recent unread emails.

### Test Calendar

```bash
gogcli calendar list --days 7
```

You should see your upcoming events.

### Test Contacts

```bash
gogcli contacts search "John"
```

You should see any contacts named John.

---

## Step 5: Register in Tooling Directory

Now that gogcli is working, we need to tell your agent it's available.

**Say to your agent:**
> "Register gogcli in the tooling directory"

Claude will update `tools/REGISTRY.md` with:
- Tool name and purpose
- Installation date
- Verification status
- Example commands

This way, your agent knows it can use gogcli for email and calendar tasks.

---

## Common Commands Reference

### Gmail

```bash
# Search emails
gogcli gmail search "from:boss" --max 10
gogcli gmail search "subject:urgent" --max 5
gogcli gmail search "is:unread newer_than:1d"

# Read a specific email
gogcli gmail get MESSAGE_ID

# Read entire conversation thread
gogcli gmail thread get THREAD_ID

# Create a draft
gogcli gmail drafts create --to "sarah@example.com" \
  --subject "Re: Project Update" \
  --body "Thanks for the update..."

# Create HTML draft (for formatted emails)
gogcli gmail drafts create --to "sarah@example.com" \
  --subject "Weekly Report" \
  --body "<h2>Summary</h2><p>Key points...</p>" \
  --html
```

### Calendar

```bash
# List upcoming events
gogcli calendar list --days 7
gogcli calendar list --days 30

# Create an event
gogcli calendar create --title "Team Meeting" \
  --start "2024-01-15 10:00" \
  --end "2024-01-15 11:00"
```

### Contacts

```bash
# Search contacts
gogcli contacts search "John"
gogcli contacts search "Acme Corp"
```

---

## Important: Draft Only, Never Send

Your agent will create email **drafts**, not send emails directly.

**Why?**
- You always review before sending
- Prevents accidental sends
- You catch mistakes before they go out

**The workflow:**
1. You tell your agent to draft an email
2. Agent creates the draft in Gmail
3. You open Gmail, review the draft
4. YOU click Send

Never configure your agent to send emails automatically. Always review first.

---

## Troubleshooting

### "Invalid credentials"

- Re-run `gogcli auth login`
- Make sure you authorized the correct Google account
- Check that the credentials file is in the right place

### "API not enabled"

Some APIs need to be enabled in Google Cloud Console:
- Gmail API
- Google Calendar API
- Google People API (for Contacts)

**Ask Claude:** "Enable the Gmail API in Google Cloud Console"

### "Quota exceeded"

Free tier Google Cloud has usage limits. For personal use, you won't hit them. If you do:
- Wait 24 hours (limits reset)
- Or upgrade to a paid Google Cloud tier

### Commands not found after install

On Windows, you may need to:
1. Add gogcli.exe location to your PATH
2. Restart Git Bash

**Ask Claude:** "Help me add gogcli to my Windows PATH"

---

## What You've Accomplished

- Installed gogcli
- Set up Google Cloud credentials (with Claude's help)
- Authenticated with your Google account
- Tested Gmail, Calendar, and Contacts access
- Registered the tool so your agent knows it's available

**Your agent can now:**
- Search and read your emails
- Check your calendar
- Look up contacts
- Create draft emails and events

**Next:** Learn about eval harnesses for reliable agent behavior → [04-EVAL-HARNESSES.md](04-EVAL-HARNESSES.md)

---

*Time to complete: 20-30 minutes*
