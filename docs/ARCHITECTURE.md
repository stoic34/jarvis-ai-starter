# Architecture Overview

How the Jarvis AI Starter Kit fits together after the Codex refactor.

---

## System Diagram

```
┌────────────────────────────────────────────────────────────┐
│                         You                                │
│                                                            │
│  Laptop, phone, voice dictation, email, messages, browser  │
└───────────────────────┬────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────────┐
│                   Codex on macOS                            │
│                                                            │
│  Reads AGENTS.md                                           │
│  Reads workspace/ for identity, tools, and context          │
│  Works against vault/ as the local knowledge base           │
└───────┬──────────┬──────────┬──────────────┬───────────────┘
        │          │          │              │
        ▼          ▼          ▼              ▼
   ┌────────┐ ┌────────┐ ┌────────────┐ ┌──────────────┐
   │ gogcli │ │ tools/ │ │ Codex app  │ │ Remote Mac   │
   │ Gmail  │ │ PDF    │ │ browser +  │ │ optional     │
   │ Cal    │ │ Audio  │ │ computer   │ │ always-on    │
   │ Drive  │ │ HTML   │ │ use        │ │ worker       │
   └────────┘ └────────┘ └────────────┘ └──────────────┘
        │          │             │              │
        ▼          ▼             ▼              ▼
   Google APIs  Local files   macOS apps    Phone-triggered work
```

Claude Code remains supported through `CLAUDE.md`, which points back to `AGENTS.md`.

---

## File Structure

```
jarvis-ai-starter/
├── AGENTS.md                    # Source-of-truth runtime instructions
├── CLAUDE.md                    # Claude Code compatibility loader
├── README.md
├── CHANGELOG.md
│
├── workspace/                   # User and assistant configuration
│   ├── IDENTITY.md
│   ├── USER.md
│   ├── TOOLS.md
│   └── CONTEXT.md
│
├── vault/                       # Local knowledge base
│   ├── Projects/
│   ├── Daily/
│   ├── Reference/
│   ├── People/
│   └── Archive/
│
├── tools/                       # Local automation scripts
├── evals/                       # Quality and safety checks
├── docs/                        # Human-readable setup and operations docs
├── infrastructure/              # Optional cloud infrastructure
├── mcp/                         # MCP examples and templates
└── .claude/                     # Legacy Claude Code capability files
```

---

## Instruction Layer

`AGENTS.md` is the operating contract.

Codex reads it directly. Claude Code reads `CLAUDE.md`, which instructs Claude to read `AGENTS.md`.

This avoids two divergent instruction systems.

---

## Runtime Layer

Recommended:

- Codex Desktop app for local Mac workflows
- Codex CLI for terminal-oriented work
- Optional Claude Code as a compatible alternate runtime

The assistant should not assume every runtime has the same tools. It should inspect available tools and report missing capabilities plainly.

---

## Context Layer

`workspace/` separates the user's context from the runtime instructions:

| File | Purpose |
|------|---------|
| `workspace/IDENTITY.md` | Assistant name, personality, communication style |
| `workspace/USER.md` | User profile, timezone, preferences |
| `workspace/TOOLS.md` | Tool inventory and verification status |
| `workspace/CONTEXT.md` | Current priorities and active work |

---

## Knowledge Layer

`vault/` is the persistent working memory.

Use it for:

- Daily capture
- Project tracking
- Reference notes
- People notes
- Continuation notes

The assistant should read before writing and archive rather than delete.

---

## Tool Layer

Core tools:

- `gogcli` for Google Workspace
- `tools/audio-transcribe.py` for audio transcription
- `tools/pdf-create.py` for PDF generation
- `tools/md-to-html.py` for HTML email drafts
- `evals/pii-scanner.py` for pre-share checks

Before claiming a tool does not exist, the assistant should read `workspace/TOOLS.md`, inspect `tools/`, and run `--help`.

---

## Desktop Layer

Codex is preferred because local assistant work often crosses out of the terminal:

- Browser setup and research
- macOS app verification
- Obsidian checks
- Permission troubleshooting
- Remote Mac diagnostics

Computer-control workflows should stay narrow, visible, and reversible.

---

## Remote Mac Layer

The optional remote pattern:

```
Phone instruction
    │
    ▼
Message / remote trigger
    │
    ▼
Always-on Mac with Codex
    │
    ├── Reads local vault
    ├── Uses local tools
    ├── Drafts outputs
    └── Reports back for review
```

This is useful when the user has only phone access but wants real work done on a Mac that has the vault, tools, and app permissions.

---

## Security Model

Core rules:

- Draft emails only, never send.
- Do not enter passwords or financial credentials.
- Do not expose private vault content externally without approval.
- Keep secrets out of repo files.
- Verify before claiming completion.

The AI proposes and drafts. The user authorizes and sends.

---

## Expansion Path

```
Level 1: Local Codex + AGENTS.md + vault + tools
Level 2: Google Workspace + desktop/browser workflows
Level 3: Remote Mac worker for phone-triggered execution
Level 4: Cloud infrastructure, scheduled jobs, MCP, business integrations
```
