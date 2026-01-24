# Tooling Registry

This file tracks all installed capabilities. **Check here before using any tool.**

When your agent needs to know what it can do, it reads this file.

---

## Why a Registry?

Your agent has amnesia. Every conversation starts fresh. Without a registry, it doesn't know:
- What tools are installed
- How to use them
- Whether they're working

The registry solves this:
- Lists all installed tools
- Shows example commands
- Tracks verification status

**After installing any new tool, register it here.**

---

## Core Tools (Pre-Installed)

### pdf-create.py
- **Purpose**: Convert Markdown notes to professional PDFs
- **Location**: `tools/pdf-create.py`
- **Status**: Ready to use
- **Usage**:
  ```bash
  python3 tools/pdf-create.py --input notes.md --output document.pdf
  ```
- **Requirements**: `pip install -r tools/requirements.txt`

### md-to-html.py
- **Purpose**: Convert Markdown to HTML (for email formatting)
- **Location**: `tools/md-to-html.py`
- **Status**: Ready to use
- **Usage**:
  ```bash
  python3 tools/md-to-html.py --input draft.md --output email.html
  ```
- **Requirements**: `pip install -r tools/requirements.txt`

### audio-transcribe.py
- **Purpose**: Transcribe voice memos and audio files
- **Location**: `tools/audio-transcribe.py`
- **Status**: Ready to use (requires Gemini API key)
- **Usage**:
  ```bash
  python3 tools/audio-transcribe.py recording.m4a
  python3 tools/audio-transcribe.py recording.m4a --timestamps
  ```
- **Requirements**:
  - `pip install -r tools/requirements.txt`
  - `GEMINI_API_KEY` environment variable

---

## Installed Integrations

*(Register new tools below this line)*

### gogcli
- **Purpose**: Google Workspace integration (Gmail, Calendar, Contacts, Drive)
- **Installed**: [DATE]
- **Verified**: [ ] Not yet verified
- **Auth Method**: OAuth via `gogcli auth login`
- **Usage Examples**:
  ```bash
  # Email
  gogcli gmail search "from:boss" --max 10
  gogcli gmail thread get THREAD_ID
  gogcli gmail drafts create --to "email@example.com" --subject "Subject" --body "Content"

  # Calendar
  gogcli calendar list --days 7
  gogcli calendar create --title "Meeting" --start "2024-01-15 10:00" --end "2024-01-15 11:00"

  # Contacts
  gogcli contacts search "John"
  ```
- **Notes**:
  - Always use `drafts create`, never `send`
  - Use `--html` flag for formatted emails
  - Use `thread get` for full conversations, not just `get`

---

## How to Register a New Tool

When you install a new tool, add an entry with:

```markdown
### tool-name
- **Purpose**: What it does in one line
- **Installed**: YYYY-MM-DD
- **Verified**: [x] Working OR [ ] Not yet verified
- **Auth Method**: How to authenticate (if applicable)
- **Usage Examples**:
  ```bash
  example commands here
  ```
- **Notes**: Any gotchas or tips
```

**Then verify it works:**
```bash
tool-name --version
tool-name --help
# Run a simple test command
```

Update the "Verified" checkbox once confirmed working.

---

## Verification Checklist for New Tools

Before marking a tool as verified:

- [ ] Tool is installed and in PATH (or full path is documented)
- [ ] `--help` or `--version` works
- [ ] At least one real command executes successfully
- [ ] Authentication is complete (if required)
- [ ] Example commands are tested and working

---

## Troubleshooting Tools

### "Command not found"
- Check if tool is in PATH
- Try using full path: `/full/path/to/tool`
- On Windows, check if .exe extension is needed

### "Permission denied"
- Mac/Linux: `chmod +x tool-name`
- Windows: Check file permissions

### "Authentication failed"
- Re-run auth command for the tool
- Check credentials/tokens haven't expired
- Verify correct account is authenticated

---

*Last updated: [Agent updates this when registering tools]*
