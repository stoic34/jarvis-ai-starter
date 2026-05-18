# Windows Setup Guide

Windows support is now a legacy/advanced path.

The recommended setup for this starter kit is **Codex on macOS** because the highest-value workflows use local Mac files, Obsidian, iMessage/SMS, desktop control, and optional remote Mac access.

Use Windows only if you understand that some workflows will not match the docs exactly.

---

## What Still Works on Windows

- `AGENTS.md` instruction format
- The local `vault/` folder
- Basic Codex CLI workflows
- Git-based change tracking
- Python tools, if dependencies install cleanly
- Some Google Workspace workflows through `gogcli`

## What Is Not First-Class Here

- macOS desktop takeover
- iMessage/SMS patterns
- Screen Sharing to a remote Mac
- Mac-specific Obsidian automation
- The recommended phone-triggered remote-worker pattern

---

## Minimal Windows Path

1. Install Git for Windows
2. Install Node.js
3. Install Codex:

```powershell
npm install -g @openai/codex
codex --version
```

4. Clone the starter kit:

```powershell
cd $HOME\Documents
git clone https://github.com/stoic34/jarvis-ai-starter.git
cd jarvis-ai-starter
```

5. Launch Codex:

```powershell
codex
```

6. Say:

> "Let's do the initial setup."

---

## Claude Code Legacy Path

If you specifically want the older Claude Code flow, you can still use `CLAUDE.md`.

That file now points Claude Code back to `AGENTS.md`, so do not maintain a separate instruction fork unless you have a deliberate reason.

---

## Recommendation

If your goal is the full assistant experience, use a Mac.

If your only machine is Windows, use this guide as a starting point and expect to adapt the desktop automation and remote-access sections.
