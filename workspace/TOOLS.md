# Tool Inventory

<!--
  This file is the authoritative registry of all tools available to your AI.
  Your AI checks this file before claiming it can't do something.

  When you install a new tool, add it here. When you remove one, delete the entry.
-->

## Core Tools (Included in Starter Kit)

| Tool | Purpose | Status | Example |
|------|---------|--------|---------|
| `gogcli` | Gmail, Calendar, Contacts, Drive | [pending setup] | `gogcli gmail search "from:boss"` |
| `audio-transcribe.py` | Voice memo → text | [pending setup] | `python3 tools/audio-transcribe.py recording.m4a` |
| `pdf-create.py` | Markdown → PDF | [pending setup] | `python3 tools/pdf-create.py --input notes.md` |
| `md-to-html.py` | Markdown → HTML (for emails) | [pending setup] | `python3 tools/md-to-html.py --input draft.md` |

## Browser Automation

| Tool | Purpose | Status | Notes |
|------|---------|--------|-------|
| Claude for Chrome | Web navigation, form filling, research | [pending setup] | Requires Chrome extension |

## User-Installed Tools

<!--
  Add tools you install yourself. Use this format:

  | `tool-name` | What it does | verified | `tool-name --example` |
-->

| Tool | Purpose | Status | Example |
|------|---------|--------|---------|
| | | | |

## Installation Notes

<!--
  Record any special setup steps, API keys needed, or quirks:

  - gogcli: Requires Google Cloud project + OAuth credentials
  - audio-transcribe.py: Needs GEMINI_API_KEY environment variable
  - pdf-create.py: Needs weasyprint (pip3 install weasyprint)
-->

### Environment Variables Needed

| Variable | Tool | How to Get |
|----------|------|------------|
| `GEMINI_API_KEY` | audio-transcribe.py | [ai.google.dev](https://ai.google.dev/) |

## Discovery Protocol

**Before claiming you can't do something:**

1. Check this file for available tools
2. Check `tools/` directory for scripts
3. Run `tool-name --help` to see capabilities
4. If still stuck, tell the user what you need
