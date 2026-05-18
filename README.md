# Jarvis AI Starter Kit

Build a local AI assistant on your Mac, then grow it into a durable operating layer for your work.

This kit now starts with **OpenAI Codex** and the portable **`AGENTS.md`** instruction format. Claude Code still works, but it is no longer the center of the architecture.

---

## Recommended Setup

**Use a Mac if you can.** The system is designed around macOS because the highest-leverage workflows use local files, Obsidian, iMessage/SMS, desktop automation, and optional remote access into an always-on Mac.

Windows and Linux can still run parts of the kit, but they are not the recommended starting point. If you need the older Claude Code path, keep it as a legacy fallback.

---

## General Workflow

1. Use a Mac. The full pattern assumes macOS because desktop control, browser control, Obsidian, local files, iMessage/SMS, and remote Mac access all fit together there.
2. Install Codex and sign in with your ChatGPT account.
3. Clone or download this directory, then launch Codex from the starter-kit folder so it reads `AGENTS.md`.
4. Enable the Codex Desktop workflows you need: local file access, browser control, and computer/desktop control.
5. Ask Codex to install and verify the primary tooling:
   - Homebrew
   - Git
   - Python and the starter-kit Python dependencies
   - `gogcli` for Gmail, Calendar, Drive, and Contacts
   - audio transcription tooling
   - PDF and document-summary tooling
   - any browser or desktop permissions required for setup
6. Use the assistant to read email, read calendar context, create Gmail drafts, transcribe audio, summarize documents, generate PDFs, and maintain the local vault.
7. Optionally add Claude Code as a compatible alternate runtime. In that case, `CLAUDE.md` should load back to `AGENTS.md` rather than becoming a separate instruction fork.

The assistant should draft and prepare external communications, not send them automatically.

See [CHANGELOG.md](CHANGELOG.md) for the archive of major changes.

---

## What You Get

**Level 1 - Starter Kit**
- A named AI assistant that knows who you are
- A local Obsidian-style vault for notes, projects, and context
- A portable `AGENTS.md` instruction layer that works in Codex and Claude Code
- Google Workspace integration through `gogcli` for Gmail, Calendar, Drive, and Contacts
- Local tools for PDFs, audio transcription, HTML email drafts, and setup checks
- Draft-only email workflow: the assistant drafts, you review and send manually

**Level 2 - Remote Mac Pattern**
- A second Mac or Mac mini that stays available as an always-on AI workstation
- Tailscale or another private network for secure remote access
- Codex Desktop app, CLI, and remote-control readiness
- Phone-triggered workflow: send an instruction from your phone, then let the Mac-based assistant execute locally

**Level 3 - Expandable Framework**
- Skills, prompt templates, and specialist-agent definitions for Claude Code compatibility
- MCP examples and templates
- AWS infrastructure starter templates
- Eval and security checks for more reliable work

---

## Quick Start

### Step 0: Prerequisites

Read [docs/00-PREREQUISITES.md](docs/00-PREREQUISITES.md).

You'll need:
- A Mac you actually use, ideally your daily laptop
- A ChatGPT account with Codex access
- Basic terminal comfort
- Google Workspace if you want Gmail and Calendar integration
- Optional but recommended: Obsidian, Wispr Flow or macOS Dictation, and Tailscale

### Step 1: Install and Launch Codex

Follow [docs/01-FIRST-LAUNCH.md](docs/01-FIRST-LAUNCH.md).

You will:
- Install Codex
- Sign in with your ChatGPT account
- Open this starter kit as the workspace
- Name your assistant
- Create a one-word launch shortcut

### Step 2: Enable Desktop and Browser Automation

Follow [docs/02-CHROME-EXTENSION.md](docs/02-CHROME-EXTENSION.md).

Codex is the preferred runtime because the desktop app can use browser and computer-control workflows on macOS. That matters for setup tasks where the assistant needs to look at a real screen, click through app settings, or guide you through OAuth flows.

### Step 3: Connect Google Workspace

Follow [docs/03-GOOGLE-INTEGRATION.md](docs/03-GOOGLE-INTEGRATION.md).

The assistant can search Gmail, read calendar context, create drafts, and work with Drive or Contacts through `gogcli`.

### Step 4: Learn Verification

Read [docs/04-EVAL-HARNESSES.md](docs/04-EVAL-HARNESSES.md).

The important habit is simple: for multi-step work, the assistant should verify that the work actually completed before claiming success.

### Step 5: Optional Remote Mac

Read [docs/05-REMOTE-MAC.md](docs/05-REMOTE-MAC.md).

This is the pattern for a separate MacBook or Mac mini that stays online so you can trigger assistant work from your phone when you are away from your main laptop.

---

## Architecture

```
You ──→ Codex on Mac ──→ AGENTS.md (portable instructions)
              │                 workspace/ (identity + context)
              │                 vault/ (notes and operating memory)
              │
              ├──→ gogcli (Gmail, Calendar, Drive, Contacts)
              ├──→ tools/ (PDF, audio, HTML)
              ├──→ Codex app tools (browser, computer use, plugins)
              ├──→ optional remote Mac (always-on worker)
              └──→ Claude Code compatibility through CLAUDE.md
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full system diagram.

### Key Files and Directories

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Source-of-truth assistant instructions for Codex and other AGENTS-compatible runtimes |
| `CLAUDE.md` | Claude Code compatibility loader that points back to `AGENTS.md` |
| `workspace/` | Your identity, preferences, tool inventory, and current context |
| `vault/` | Your local knowledge base: projects, daily notes, reference, people |
| `tools/` | Local automation scripts |
| `evals/` | Quality checks and PII scanning |
| `.claude/` | Legacy Claude Code skills, agents, prompts, and settings |
| `infrastructure/` | Optional AWS templates |
| `mcp/` | MCP examples and templates |

---

## What Can Your AI Do?

**Email and Calendar**
> "Scan my inbox for anything urgent from the last 24 hours."
> "Draft a reply to a colleague about the migration plan."
> "What does my week look like?"

**Desktop and Browser Work**
> "Open the app settings and tell me what permissions are missing."
> "Walk me through the Google Cloud OAuth setup."
> "Use the browser to research the top 5 CRM tools and compare pricing."

**Remote Work**
> "From my phone, ask the Mac mini assistant to process today's voice notes."
> "Check whether the remote Mac is online and ready for Codex work."

**Documents**
> "Turn these notes into a professional PDF."
> "Create an agenda for tomorrow's meeting."

**Projects**
> "Start a new project for the website redesign."
> "Run my morning routine."
> "Do a weekly review."

**Development**
> "Build a Python tool that converts CSV to JSON."
> "Review this code change before I commit."

See [docs/USE-CASES.md](docs/USE-CASES.md) for more workflow examples.

---

## Important Notes

**Drafts Only, Never Send** - Your agent creates email drafts for your review. It never sends email automatically.

**Mac First** - The recommended experience is macOS + Codex. This is the path that supports local files, desktop takeover, iMessage/SMS patterns, and remote Mac control most cleanly.

**Runtime Portable** - The assistant's operating instructions live in `AGENTS.md`. Codex reads it directly; Claude Code can use `CLAUDE.md` as a compatibility bridge.

**Google Workspace** - Core integrations assume Gmail and Google Calendar. Microsoft 365 users can still use the vault and tools, but email/calendar setup is not included.

**Autonomy Modes** - Codex supports sandbox and approval settings. Start with a review-friendly mode, then loosen approvals only after you trust the setup.

---

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

Quick fixes:
- **`codex` not found** - Install or update Codex, then restart Terminal.
- **Codex does not read instructions** - Confirm you launched from the starter-kit folder and that `AGENTS.md` exists at the repo root.
- **Google auth issues** - Re-run `gogcli auth login` with the right account.
- **Remote Mac unavailable** - Check Tailscale, wake/sleep settings, and whether the Codex app is running on the remote Mac.

---

## Credits

Built from daily use of local AI assistants, Obsidian vault operations, Google Workspace tooling, and remote Mac workstation patterns.

---

*Questions? Issues? Open a [GitHub Issue](https://github.com/stoic34/jarvis-ai-starter/issues).*
