# Jarvis AI Starter Kit

Build your own personal AI assistant in under 90 minutes.

---

## What You Get

- A named AI assistant that knows who you are
- One-word launch command (just type `jarvis` or your chosen name)
- Email, calendar, and contacts integration (Google Workspace)
- Browser automation for complex web tasks
- Self-verification patterns so your agent actually finishes tasks

---

## Quick Start (5 Steps)

### Step 0: Prerequisites
Read [docs/00-PREREQUISITES.md](docs/00-PREREQUISITES.md) first.

You'll need:
- A laptop (not desktop)
- Basic terminal knowledge (we teach you)
- A dictation tool (we recommend one)
- Google Workspace (Gmail, Google Calendar)
- A Claude account (Pro or Max recommended)

### Step 1: First Launch
Follow [docs/01-FIRST-LAUNCH.md](docs/01-FIRST-LAUNCH.md).

You'll:
- Download this repo
- Launch Claude Code (no installation needed)
- Name your assistant
- Create your launch alias

**After this step:** Type `jarvis` (or your chosen name) to start your agent.

### Step 2: Browser Control
Follow [docs/02-CHROME-EXTENSION.md](docs/02-CHROME-EXTENSION.md).

You'll:
- Install Claude for Chrome
- Enable browser automation
- Verify your agent can control web pages

**After this step:** Your agent can navigate websites for you.

### Step 3: Google Integration
Follow [docs/03-GOOGLE-INTEGRATION.md](docs/03-GOOGLE-INTEGRATION.md).

You'll:
- Install gogcli (Google CLI)
- Set up credentials (Claude navigates Cloud Console for you)
- Connect email, calendar, and contacts

**After this step:** Your agent can read your email and check your calendar.

### Step 4: Learn Eval Harnesses
Read [docs/04-EVAL-HARNESSES.md](docs/04-EVAL-HARNESSES.md).

You'll:
- Understand why AI agents sometimes claim false success
- Learn to invoke self-verification
- Run your first eval harness

**After this step:** You know how to get reliable results from your agent.

---

## What Can Your AI Do?

Once set up, try these:

**Email**
> "Scan my inbox for anything urgent from the last 24 hours"

> "Find all emails from Sarah about the project and summarize them"

> "Draft a reply to John's email about the budget"

**Calendar**
> "What do I have scheduled this week?"

> "Find a time next Tuesday for a 1-hour meeting"

> "Block 2 hours tomorrow morning for deep work"

**Research**
> "Research the top 5 CRM tools and compare their pricing"

> "Find information about [topic] and create a summary note"

**Documents**
> "Turn my meeting notes into a professional PDF"

> "Create an agenda for tomorrow's team meeting"

**And much more** — see [docs/USE-CASES.md](docs/USE-CASES.md) for examples.

---

## Important Notes

### This is for Google Workspace

The core integrations work with Gmail and Google Calendar. If you use Outlook/Microsoft 365, you can still use this kit, but email/calendar integrations won't work out of the box.

### Drafts Only, Never Send

Your agent creates email **drafts**, not sent emails. You always review before sending. This is intentional.

### YOLO Mode

Your alias includes `--dangerously-skip-permissions`. This means your agent won't ask permission for routine operations. It's safe for personal use in your own vault.

### Browser Control

Your alias includes `--chrome`. This enables the agent to control your browser for web tasks. You'll see what it's doing, and it will ask before taking sensitive actions.

---

## Time Breakdown

| Step | Time |
|------|------|
| Prerequisites | 10-15 min |
| First Launch | 15-20 min |
| Chrome Extension | 10-15 min |
| Google Integration | 20-30 min |
| Eval Harnesses | 10 min |
| **Total** | **~75 minutes** |

---

## What's Next?

After you're comfortable with the basics:

- [docs/USE-CASES.md](docs/USE-CASES.md) - Real examples and prompts
- [docs/WHATS-NEXT.md](docs/WHATS-NEXT.md) - Advanced expansions
- [tools/REGISTRY.md](tools/REGISTRY.md) - See all installed tools

---

## Troubleshooting

Common issues are covered in each doc. For quick fixes:

**"Command not found"**
- Use `npx @anthropic-ai/claude-code` instead of `claude`
- This bypasses PATH issues entirely

**Chrome extension not connecting**
- Make sure your alias includes `--chrome`
- Restart both terminal and Chrome

**gogcli authentication issues**
- Re-run `gogcli auth login`
- Make sure you're using the right Google account

---

## Credits

Built with lessons learned from months of daily AI assistant usage.

Based on insights from real onboarding sessions with non-technical users.

---

*Questions? Issues? Open a GitHub issue.*
