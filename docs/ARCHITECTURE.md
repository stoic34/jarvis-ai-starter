# Architecture Overview

How all the pieces of Jarvis AI Starter fit together.

---

## System Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     You (the user)                       │
│                                                          │
│  "Hey Jarvis, check my email and draft a response"      │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   Claude Code (CLI)                      │
│                                                          │
│  Reads CLAUDE.md → understands role, tools, workflows   │
│  Reads workspace/ → knows your identity and context     │
│  Uses .claude/ → skills, agents, prompts, permissions   │
└──────┬──────────┬──────────┬──────────┬─────────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐
   │ gogcli │ │ tools/ │ │ Chrome │ │ .claude/   │
   │        │ │        │ │ ext.   │ │ skills/    │
   │ Gmail  │ │ PDF    │ │ Web    │ │ agents/    │
   │ Cal    │ │ Audio  │ │ browse │ │ prompts/   │
   │ Drive  │ │ HTML   │ │ forms  │ │            │
   └────────┘ └────────┘ └────────┘ └────────────┘
       │          │
       ▼          ▼
   ┌────────┐ ┌────────┐
   │ Google │ │ Local  │
   │ APIs   │ │ files  │
   └────────┘ └────────┘
```

---

## File Structure

```
jarvis-ai-starter/
│
├── CLAUDE.md                    # Master configuration (AI reads this first)
├── README.md                    # Quick start for humans
├── CHANGELOG.md                 # Version history
│
├── workspace/                   # Your personal config (separated from code)
│   ├── IDENTITY.md             #   Agent name, personality, style
│   ├── USER.md                 #   Your profile, preferences, timezone
│   ├── TOOLS.md                #   Tool inventory and status
│   └── CONTEXT.md              #   Current priorities and active projects
│
├── .claude/                     # AI capability definitions
│   ├── settings.json           #   Permission rules
│   ├── TAXONOMY.md             #   Command/Skill/Agent decision guide
│   ├── agents/                 #   Domain expert definitions
│   ├── skills/                 #   Structured workflow definitions
│   └── prompts/                #   Reusable prompt templates
│
├── vault/                       # Your Obsidian vault (knowledge base)
│   ├── Projects/Active/        #   Current work
│   ├── Projects/Archive/       #   Completed work
│   ├── Daily/                  #   Inbox, today, journal
│   ├── Reference/              #   Permanent knowledge
│   ├── People/                 #   Contact notes
│   └── Archive/                #   Retired items
│
├── tools/                       # Python scripts for automation
│   ├── audio-transcribe.py     #   Voice → text
│   ├── pdf-create.py           #   Markdown → PDF
│   ├── md-to-html.py           #   Markdown → email HTML
│   └── requirements.txt        #   Python dependencies
│
├── evals/                       # Quality assurance
│   ├── pii-scanner.py          #   Sensitive data detection
│   └── test-tools.py           #   Tool verification suite
│
├── .security/                   # Security infrastructure
│   ├── blocklist.txt           #   Your private blocked terms (gitignored)
│   ├── hooks/pre-commit        #   Git pre-commit scanner
│   └── README.md               #   Security setup docs
│
├── docs/                        # Human-readable documentation
│   ├── 00-PREREQUISITES.md     #   What you need before starting
│   ├── 01-FIRST-LAUNCH.md      #   Download and first run
│   ├── 02-CHROME-EXTENSION.md  #   Browser automation setup
│   ├── 03-GOOGLE-INTEGRATION.md#   Google Workspace connection
│   ├── 04-EVAL-HARNESSES.md    #   Self-verification mental model
│   ├── ARCHITECTURE.md         #   This file
│   ├── TROUBLESHOOTING.md      #   Common issues and fixes
│   ├── INTEGRATIONS.md         #   Available integrations
│   └── WHATS-NEXT.md           #   Expansion paths
│
└── infrastructure/              # Cloud infrastructure templates (Level 2)
    ├── README.md               #   AWS architecture overview
    ├── secrets-manager/        #   Secure credential storage
    ├── lambda/templates/       #   Serverless function templates
    ├── s3/                     #   Storage and backup
    └── monitoring/             #   Alerts and logging
```

---

## How It Works

### 1. Launch

When you type your agent's name (e.g., `jarvis`), the shell alias:
1. Navigates to this directory
2. Launches Claude Code with your settings
3. Claude reads `CLAUDE.md` first (its instructions)
4. Then reads `workspace/` files for your identity and context

### 2. Understanding

Claude now knows:
- **Who it is** (IDENTITY.md)
- **Who you are** (USER.md)
- **What tools exist** (TOOLS.md)
- **What you're working on** (CONTEXT.md)
- **How to behave** (CLAUDE.md — rules, workflows, permissions)

### 3. Working

When you give a task, Claude:
1. **Classifies** it (routine? structured? expertise needed?)
2. **Selects** the right tier (template, skill, agent, or direct)
3. **Executes** using available tools
4. **Verifies** results (eval harness for multi-step tasks)

### 4. Persisting

At session end:
- Notes are saved in `vault/`
- If work is incomplete, a CONTINUATION note is created
- Next session picks up where you left off

---

## Three-Tier Capability Model

```
┌─────────────────────────────────────────┐
│           Agents (Deep Expertise)        │
│  Researcher · Writer · Developer         │
│  Separate context, domain knowledge      │
├─────────────────────────────────────────┤
│           Skills (Methodology)           │
│  Code Review · Eval Harness · Handoff    │
│  Structured steps, quality gates         │
├─────────────────────────────────────────┤
│       Prompt Templates (Routine)         │
│  Morning Routine · Project Kickoff       │
│  Quick, variable-driven, repeatable      │
├─────────────────────────────────────────┤
│          Direct Conversation             │
│  Simple questions, quick tasks           │
│  No framework needed                     │
└─────────────────────────────────────────┘
```

---

## Security Model

### Three-Layer Defense

```
Layer 1: Pre-commit hook
  → Scans staged files for PII and blocklist terms
  → Blocks commits with sensitive data

Layer 2: Blocklist (.security/blocklist.txt)
  → Your custom terms that should never appear
  → Gitignored — stays local only

Layer 3: Full-repo scan
  → Run manually before publishing/sharing
  → Catches anything the hook might have missed
```

### Permission Tiers

The `.claude/settings.json` controls what the AI can do without asking:

- **Allow**: Tools and operations pre-approved for automatic use
- **Deny**: Operations that are always blocked (e.g., sending emails, `rm -rf`)
- Everything else: Claude asks for your permission before running

---

## Data Flow

```
You speak/type
    │
    ▼
Claude Code processes
    │
    ├── Read vault notes? → vault/
    ├── Check email? → gogcli → Google API
    ├── Generate PDF? → tools/pdf-create.py → local file
    ├── Research web? → Chrome extension → websites
    ├── Draft email? → gogcli gmail drafts create → Gmail drafts
    │
    ▼
Results shown to you
    │
    ▼
You review and approve
    │
    ├── Send the draft email yourself in Gmail
    ├── Review the generated PDF
    └── Confirm vault changes
```

**Key principle**: The AI **proposes**, you **approve**. It drafts emails but never sends. It suggests changes but asks before destructive operations.

---

## Expansion Path

```
Level 1 (Starter Kit — you are here)
  → Local tools, Google Workspace, browser, vault

Level 2 (Infrastructure)
  → AWS Secrets Manager, Lambda, S3 backup
  → See infrastructure/ directory

Level 3 (Business Integrations)
  → Shopify, CRM, accounting, marketing
  → See docs/INTEGRATIONS.md

Level 4 (Multi-Agent)
  → Multiple AI agents working together
  → See docs/WHATS-NEXT.md
```

Each level builds on the previous. Start with Level 1, expand as needed.
