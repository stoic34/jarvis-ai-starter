# Jarvis AI Starter Kit

Build your own personal AI assistant in under 90 minutes. Then grow it into a framework that scales with you.

---

## What You Get

**Level 1 — Starter Kit** (90-minute setup)
- A named AI assistant that knows who you are
- One-word launch command (just type `jarvis` or your chosen name)
- Email, calendar, and contacts integration (Google Workspace)
- Browser automation for web research and tasks
- Self-verification patterns so your agent actually finishes tasks

**Level 2 — Framework** (included, activate as needed)
- Skill system with 5 built-in skills (eval harness, code review, session handoff, content ingestion, project setup)
- Agent specializations (researcher, writer, developer)
- Session continuity across conversations
- Prompt templates for daily workflows
- Software development protocol with quality gates
- Security infrastructure with pre-commit scanning

---

## Quick Start (5 Steps)

### Step 0: Prerequisites
Read [docs/00-PREREQUISITES.md](docs/00-PREREQUISITES.md) first.

You'll need:
- A laptop (Mac, Windows, or Linux)
- Basic terminal knowledge (we teach you)
- Google Workspace (Gmail, Google Calendar)
- A Claude account (Pro or Max recommended)

### Step 1: First Launch
Follow [docs/01-FIRST-LAUNCH.md](docs/01-FIRST-LAUNCH.md).

- Download this repo
- Launch Claude Code (no installation needed)
- Name your assistant and set up your identity
- Create your one-word launch alias

### Step 2: Browser Control
Follow [docs/02-CHROME-EXTENSION.md](docs/02-CHROME-EXTENSION.md).

- Install Claude for Chrome
- Enable browser automation
- Verify your agent can navigate web pages

### Step 3: Google Integration
Follow [docs/03-GOOGLE-INTEGRATION.md](docs/03-GOOGLE-INTEGRATION.md).

- Install gogcli (Google Workspace CLI)
- Set up credentials (your AI navigates Cloud Console for you)
- Connect email, calendar, and contacts

### Step 4: Learn Eval Harnesses
Read [docs/04-EVAL-HARNESSES.md](docs/04-EVAL-HARNESSES.md).

- Understand the "Horses, Not Cars" mental model
- Learn to invoke self-verification for reliable results
- Run your first eval harness

---

## Architecture

```
You ──→ Claude Code ──→ CLAUDE.md (instructions)
              │              workspace/ (your identity + context)
              │              .claude/ (skills, agents, prompts)
              │
              ├──→ gogcli (email, calendar, contacts)
              ├──→ tools/ (PDF, audio, HTML)
              ├──→ Chrome (web automation)
              └──→ vault/ (your knowledge base)
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full system diagram.

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `workspace/` | Your identity, preferences, tool inventory, current context |
| `.claude/skills/` | Structured workflows: eval harness, code review, session handoff, content ingestion, project setup |
| `.claude/agents/` | Specialist agents: researcher, writer, developer |
| `.claude/prompts/` | Reusable templates: morning routine, project kickoff, research brief, weekly review |
| `vault/` | Your Obsidian knowledge base (projects, daily notes, reference) |
| `tools/` | Python scripts: PDF generation, audio transcription, session management |
| `evals/` | Quality assurance: PII scanner, tool tests |
| `infrastructure/` | AWS templates: Secrets Manager, Lambda, S3 backup, budget alerts |
| `mcp/` | MCP server examples and templates for tool integration |

---

## What Can Your AI Do?

**Email & Calendar**
> "Scan my inbox for anything urgent from the last 24 hours"
> "Draft a reply to John's email about the budget"
> "What do I have scheduled this week?"

**Research**
> "Research the top 5 CRM tools and compare pricing"
> "Create a research brief on [topic]"

**Documents**
> "Turn my meeting notes into a professional PDF"
> "Create an agenda for tomorrow's meeting"

**Projects**
> "Start a new project for the website redesign"
> "Run my morning routine"
> "Do a weekly review"

**Development**
> "Build a Python tool that converts CSV to JSON"
> "Review this code change before I commit"

**And much more** — see [docs/USE-CASES.md](docs/USE-CASES.md) for 22+ workflow examples.

---

## How It Grows With You

```
Week 1-2    Master the basics (email, calendar, notes, documents)
Week 3-4    Use skills (eval harness, session handoff, content ingestion)
Month 2     Customize (add your own skills, templates, agents)
Month 3+    Expand (AWS infrastructure, business integrations)
```

The framework is progressive — start simple, activate features as you need them. See [docs/WHATS-NEXT.md](docs/WHATS-NEXT.md) for expansion paths.

---

## Important Notes

**Drafts Only, Never Send** — Your agent creates email drafts for your review. It never sends anything automatically.

**Google Workspace** — Core integrations work with Gmail and Google Calendar. Microsoft 365 users can still use the vault, tools, and skills — just not the email/calendar features.

**YOLO Mode** — Your launch alias includes `--dangerously-skip-permissions`. This skips routine permission prompts. Safe for personal use in your own vault. See [docs/YOLO-MODE.md](docs/YOLO-MODE.md) for details.

**Security** — A pre-commit hook scans for PII and sensitive data before every commit. See [.security/README.md](.security/README.md) for the full security model.

---

## Time Breakdown

| Step | Time |
|------|------|
| Prerequisites | 10-15 min |
| First Launch + Identity | 15-20 min |
| Chrome Extension | 10-15 min |
| Google Integration | 20-30 min |
| Eval Harnesses | 10 min |
| **Total** | **~75 minutes** |

---

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues. Quick fixes:

- **"Command not found"** — Use `npx @anthropic-ai/claude-code` instead of `claude`
- **Chrome not connecting** — Ensure `--chrome` is in your alias, restart terminal and Chrome
- **gogcli auth issues** — Re-run `gogcli auth login` with the right Google account

---

## Contributing

We welcome contributions. See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

---

## Credits

Built with lessons learned from months of daily AI assistant usage and real onboarding sessions with non-technical users.

---

*Questions? Issues? Open a [GitHub Issue](https://github.com/stoic34/jarvis-ai-starter/issues).*
