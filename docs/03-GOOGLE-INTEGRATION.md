# Google Integration: Email, Calendar, and More

Google Workspace is the first high-value integration because it lets your assistant understand your inbox, calendar, contacts, and documents.

**Time required:** 20-30 minutes

---

## What is gogcli?

`gogcli` is a command-line tool for Google Workspace.

| Service | What Your Assistant Can Do |
|---------|----------------------------|
| Gmail | Search email, read full threads, create drafts |
| Calendar | View events, create draft plans, check availability |
| Contacts | Look up people and email addresses |
| Drive | Find and work with files |

CLI tools are better than browser clicking for routine assistant work because they return structured data and do not break when Gmail's interface changes.

---

## Step 1: Install gogcli

On Mac:

```bash
brew install gogcli/tap/gogcli
gogcli --version
```

If you are not on Mac, check the `gogcli` release page and adapt the setup. The starter kit's recommended path is still macOS.

---

## Step 2: Set Up Google Cloud Credentials

This is usually the fiddly part.

Ask your assistant:

> "Set up Google Cloud credentials for gogcli. Navigate the Cloud Console for me and tell me when I need to click or authorize."

The assistant can help you:

1. Create or select a Google Cloud project
2. Enable Gmail, Calendar, Drive, and People APIs
3. Configure the OAuth consent screen
4. Create OAuth credentials
5. Download or place the credentials file

You handle:

- logging into Google
- passwords
- final authorization clicks
- consent approvals

---

## Step 3: Authenticate

```bash
gogcli auth login
```

Then test:

```bash
gogcli gmail search "is:unread" --max 5
gogcli calendar list --days 7
gogcli contacts search "John"
```

---

## Step 4: Register the Tool

After the tests work, ask:

> "Mark gogcli as verified in workspace/TOOLS.md and include the exact commands that worked."

Only mark it verified after successful tests.

---

## Common Commands

### Gmail

```bash
gogcli gmail search "from:boss" --max 10
gogcli gmail search "subject:urgent" --max 5
gogcli gmail thread get THREAD_ID
gogcli gmail drafts create --to "sarah@example.com" --subject "Subject" --body "Draft body"
```

For email research, prefer full thread reads:

```bash
gogcli gmail thread get THREAD_ID --full
```

Do not rely on a single message when the surrounding conversation matters.

### Calendar

```bash
gogcli calendar list --days 7
gogcli calendar list --days 30
```

### Contacts

```bash
gogcli contacts search "John"
```

---

## Draft Only, Never Send

The assistant may create Gmail drafts.

The assistant must never send email directly.

Allowed:

```bash
gogcli gmail drafts create ...
```

Not allowed:

```bash
gogcli gmail send ...
gogcli gmail drafts send ...
```

Workflow:

1. Assistant drafts.
2. You review in Gmail.
3. You send manually.

---

## Troubleshooting

### Invalid credentials

- Re-run `gogcli auth login`
- Confirm the correct Google account
- Confirm the credentials file is in the expected location

### API not enabled

Enable the relevant API in Google Cloud Console:

- Gmail API
- Google Calendar API
- People API
- Drive API

### OAuth consent screen issue

Add yourself as a test user, then retry auth.

---

## What You Accomplished

- Installed `gogcli`
- Connected Google Workspace
- Verified Gmail, Calendar, and Contacts
- Registered the tool for future assistant sessions

Next: [04-EVAL-HARNESSES.md](04-EVAL-HARNESSES.md)
