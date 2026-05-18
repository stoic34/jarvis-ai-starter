# AI Agent Migration Guide: Claude Code to AGENTS.md + Codex

This guide is written for both humans and AI agents. Give this file to your assistant if you already used an older Jarvis AI Starter Kit based on Claude Code and want to migrate to the newer portable setup.

The goal is not to abandon Claude Code. The goal is to move the system's source of truth into `AGENTS.md` so the same operating instructions can run under Codex, Claude Code, or another AGENTS-compatible assistant.

---

## What Changed

The first version of the starter kit was Claude Code-first:

- `CLAUDE.md` was the primary instruction file
- most work happened from Terminal
- browser automation usually depended on Claude-specific browser tooling
- Claude Code skills, agents, and prompts were the main expansion mechanism

The current version is AGENTS-first:

- `AGENTS.md` is the source-of-truth instruction file
- Codex on macOS is the recommended first runtime
- Claude Code remains a compatible secondary runtime
- Codex Desktop is used for local files, browser workflows, and computer/desktop control
- a second MacBook or Mac mini can act as an always-on worker that can be triggered remotely

---

## Target Architecture

```text
Human
  |
  v
Codex Desktop on Mac
  |
  v
AGENTS.md  <----- Claude Code can also read this through CLAUDE.md
  |
  +-- workspace/  identity, preferences, current context
  +-- vault/      notes, projects, reference material
  +-- tools/      local scripts and workflow automation
  +-- gogcli      Gmail, Calendar, Drive, Contacts
  +-- browser     research, web apps, OAuth setup
  +-- desktop     app setup, permission checks, local UI workflows
```

The recommended mental model:

> `AGENTS.md` is the operating manual. Codex and Claude Code are runtimes.

---

## Runtime Roles

Use Codex when:

- you are setting up the system on a Mac
- you want the assistant to work with local files and apps
- you want browser control and desktop/computer control
- you want the assistant to help configure OAuth, app permissions, local tooling, and system settings
- you want a remote Mac that can keep working when you only have phone access

Use Claude Code when:

- you already have a working Claude Code setup
- your workflow is mostly terminal-based coding
- you depend on existing Claude Code skills, agents, or prompt templates
- you want a second compatible runtime using the same instructions

Do not maintain two competing operating manuals. Keep one primary `AGENTS.md` and make Claude Code point back to it.

---

## Migration Checklist for the AI Agent

If you are the user's AI agent, execute this checklist carefully. Read before writing, preserve private information, and do not send email automatically.

### 1. Inspect the Current Setup

Run:

```bash
pwd
ls -la
test -f AGENTS.md && echo "AGENTS.md exists"
test -f CLAUDE.md && echo "CLAUDE.md exists"
test -d .claude && echo ".claude exists"
```

Then read:

```bash
sed -n '1,220p' AGENTS.md 2>/dev/null || true
sed -n '1,220p' CLAUDE.md 2>/dev/null || true
```

If there is no `AGENTS.md`, create it from the current `CLAUDE.md` instructions after removing Claude-only assumptions.

### 2. Make AGENTS.md the Source of Truth

Preferred public-repo pattern:

- Keep `AGENTS.md` as the full instruction file
- Replace `CLAUDE.md` with a short compatibility loader that tells Claude Code to read `AGENTS.md`

Example `CLAUDE.md`:

```markdown
# CLAUDE.md

This file exists for Claude Code compatibility.

The source-of-truth instructions live in `AGENTS.md`.

Read `AGENTS.md` before doing any work. If this file and `AGENTS.md` conflict, follow `AGENTS.md`.
```

Preferred personal-machine symlink pattern:

```bash
ln -sf AGENTS.md CLAUDE.md
ls -l CLAUDE.md
readlink CLAUDE.md
```

Expected result:

```text
CLAUDE.md -> AGENTS.md
```

Use the compatibility-loader file in public repos if you want the behavior to be obvious on GitHub. Use the symlink pattern on a personal machine if you want both filenames to resolve to the exact same file.

### 3. Optional Global Instruction Symlink

If the user wants the same instructions available across their home directory, create a user-level symlink:

```bash
ln -sf /absolute/path/to/jarvis-ai-starter/AGENTS.md ~/AGENTS.md
ls -l ~/AGENTS.md
readlink ~/AGENTS.md
```

Only do this if the user confirms they want these instructions to apply broadly. Project-specific instructions are safer for most people.

### 4. Preserve Claude Code Compatibility

Do not delete `.claude/` just because Codex is now recommended.

Keep these as optional compatibility material:

```text
.claude/skills/
.claude/agents/
.claude/prompts/
.claude/settings.json
.claude/TAXONOMY.md
```

Codex may not use those files directly, but they can remain useful documentation and migration material.

### 5. Move From Terminal-Only to Codex Desktop

Install and launch Codex on the Mac. Then verify:

```bash
codex --version
python3 --version
git --version
```

Inside Codex Desktop, enable the workflows the user needs:

- local workspace/file access
- browser control
- computer/desktop control
- any plugin or connector permissions needed for the user's workflow

Then ask Codex to verify the local tooling:

```bash
gogcli --help
gogcli auth status
brew --version
```

If `gogcli` is not authenticated, run the login flow and verify with a harmless read, such as searching a few recent messages or listing the calendar. Never send email automatically.

### 6. Configure Remote Mac Control

The most reliable remote pattern is:

```text
Phone instruction -> always-on Mac -> Codex executes locally -> draft/report back
```

Recommended setup:

- keep a MacBook or Mac mini on power
- install Codex Desktop and sign in
- install Tailscale or another private network
- enable Screen Sharing or another remote desktop method
- prevent sleep from interrupting work
- keep the vault and tools available locally on that Mac
- confirm the same ChatGPT/Codex account can reach the work session from the phone

Simple phone-trigger options:

- use the ChatGPT app on the phone to open the relevant Codex/assistant thread
- text or email yourself a command that the Mac-side assistant can read
- use a private Slack, chat, or command channel
- later, add a webhook or automation queue only after the simple version is reliable

The phone is the control surface. The Mac is the execution environment.

### 7. Verify the Migration

The migration is working when all of these are true:

- `AGENTS.md` exists and contains the source-of-truth assistant instructions
- Claude Code can still find instructions through `CLAUDE.md`
- if using a symlink, `readlink CLAUDE.md` returns `AGENTS.md`
- Codex can open the project and read `AGENTS.md`
- Codex can use local files in the starter-kit directory
- Codex can use browser control when asked
- Codex can use desktop/computer control when asked
- the assistant can create email drafts but does not send them automatically
- a phone-originated instruction can cause work to happen on the Mac, with the result reported back for review

Suggested smoke-test prompt:

```text
Read AGENTS.md, inspect this starter kit, and verify whether Codex and Claude Code can both use the same instruction layer. Do not change files yet. Report the exact files, symlinks, and runtime assumptions you found.
```

Suggested remote-control smoke-test prompt:

```text
From my phone, I want to trigger a simple local action on the Mac. Confirm the Mac-side Codex session can see this instruction, write a timestamped note to the local inbox, and report the file path back to me. Do not send any messages or email.
```

---

## Security Rules

- Do not publish private vault content
- Do not publish `.env` files, API keys, tokens, OAuth credentials, or local auth caches
- Do not include personal phone numbers or private email addresses in public examples
- Do not send email automatically
- Run the PII scanner before publishing changes:

```bash
python3 evals/pii-scanner.py
```

If the scanner fails, stop and fix the leak before sharing the repo.

---

## Recommended Upgrade Path

1. Pull the latest starter kit
2. Read `README.md`, `AGENTS.md`, and this file
3. Move old `CLAUDE.md` instructions into `AGENTS.md`
4. Make `CLAUDE.md` a compatibility loader or symlink
5. Launch Codex Desktop from the starter-kit folder
6. Enable local files, browser control, and desktop control
7. Verify `gogcli`, Homebrew, Python, Git, PDF tooling, and transcription tooling
8. Keep Claude Code available as a secondary runtime if useful
9. Set up an always-on Mac only after the local laptop setup works
10. Verify the phone-to-Mac workflow with a harmless local note before trusting it with real work

