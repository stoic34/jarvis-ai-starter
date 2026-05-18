# Tool Inventory

This file is the assistant's local registry. Before claiming a tool is unavailable, inspect this file, then inspect `tools/`, then run the relevant `--help`.

## Core Runtime

| Tool | Purpose | Status | Example |
|------|---------|--------|---------|
| `codex` | AI assistant runtime, CLI, desktop app launcher | [pending setup] | `codex --version` |
| Codex Desktop | Browser, app, and computer-control workflows where available | [pending setup] | `codex app` |
| `git` | Version control and safety net | [pending setup] | `git status --short` |
| `python3` | Runs local tools | [pending setup] | `python3 --version` |

## Starter Kit Tools

| Tool | Purpose | Status | Example |
|------|---------|--------|---------|
| `gogcli` | Gmail, Calendar, Contacts, Drive | [pending setup] | `gogcli gmail search "from:boss"` |
| `audio-transcribe.py` | Voice memo to text | [pending setup] | `python3 tools/audio-transcribe.py recording.m4a` |
| `pdf-create.py` | Markdown to PDF | [pending setup] | `python3 tools/pdf-create.py --input notes.md` |
| `md-to-html.py` | Markdown to HTML for email drafts | [pending setup] | `python3 tools/md-to-html.py --input draft.md` |

## Optional Remote Mac Tools

| Tool | Purpose | Status | Example |
|------|---------|--------|---------|
| Tailscale | Private remote access to another Mac | [optional] | `tailscale status` |
| SSH | Remote shell access | [optional] | `ssh user@host` |
| Screen Sharing | Remote desktop access | [optional] | macOS Screen Sharing app |

## Legacy Claude Code Compatibility

| Tool | Purpose | Status | Notes |
|------|---------|--------|-------|
| Claude Code | Alternate runtime | [optional] | Uses `CLAUDE.md`, which points back to `AGENTS.md` |
| Claude for Chrome | Legacy browser-control route | [optional] | Prefer Codex Desktop for the current setup |

## Environment Variables

| Variable | Tool | How to Get |
|----------|------|------------|
| `GEMINI_API_KEY` | `audio-transcribe.py` | https://ai.google.dev/ |

## Discovery Protocol

1. Check this file.
2. Check `tools/`.
3. Run `tool-name --help`.
4. Check whether a desktop app and shell binary are different.
5. If still stuck, report the exact missing dependency.
