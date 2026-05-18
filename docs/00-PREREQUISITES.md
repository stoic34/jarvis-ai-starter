# Prerequisites: Before You Start

This starter kit is now **Mac-first** and **Codex-first**.

The older Claude Code setup still works as a legacy path, but the recommended version uses Codex with `AGENTS.md` so the same assistant instructions can work across Codex, Claude Code, and other compatible agents.

---

## Hardware: Use a Mac

Recommended:

- MacBook Air, MacBook Pro, Mac mini, or Mac Studio
- Apple Silicon preferred
- Enough free disk space for an Obsidian vault, local tools, and logs
- Admin access to install apps and grant permissions

Why Mac:

- Codex Desktop can participate in local desktop workflows.
- Obsidian, iMessage/SMS, local files, Tailscale, and Screen Sharing all fit cleanly on macOS.
- A second always-on Mac can become a remote worker that you trigger from your phone.

Windows and Linux are possible, but they are not the recommended path for this assistant pattern.

---

## Accounts

You need:

- A ChatGPT account with Codex access
- A Google account or Google Workspace account if you want Gmail, Calendar, Drive, and Contacts integration
- Optional: GitHub if you want version control or code workflows

You do not need an Anthropic account unless you also want to run Claude Code.

---

## Terminal Basics

You only need a few commands:

| Command | What It Does |
|---------|--------------|
| `pwd` | Shows where you are |
| `ls` | Lists files |
| `cd folder` | Moves into a folder |
| `cd ~` | Goes to your home folder |
| `cd ..` | Goes up one folder |

Useful habits:

- Press Tab to autocomplete paths.
- Use forward slashes in paths.
- Copy commands carefully.
- If something fails three times, stop and ask the assistant to check the tool's `--help`.

---

## Dictation

AI assistants work better when you can talk naturally.

Recommended:

- Wispr Flow for high-quality dictation
- macOS Dictation as a free starting point

Enable macOS Dictation:

1. Open System Settings
2. Go to Keyboard
3. Turn on Dictation
4. Use the shortcut shown there

---

## Core Apps and Tools

Install or be ready to install:

| Tool | Purpose |
|------|---------|
| Codex | AI runtime and desktop/CLI assistant |
| Obsidian | Local knowledge base |
| Homebrew | macOS package manager |
| Git | Version control and change safety |
| Python 3 | Local tools |
| gogcli | Google Workspace integration |
| Tailscale | Optional private network for remote Mac access |

---

## Google Workspace

This kit assumes Google for email and calendar.

If you use Gmail and Google Calendar, you are on the supported path.

If you use Microsoft 365, the vault and local tools still work, but email and calendar integration are not included out of the box.

---

## Optional: Remote Mac Worker

If you want phone-triggered access, prepare a second Mac:

- Keep it plugged in
- Install Codex
- Sign in with your ChatGPT account
- Install Tailscale
- Enable remote access intentionally
- Keep the vault available on that Mac

The phone does not run the whole assistant. The phone sends instructions; the Mac does the work.

---

## Checklist

- [ ] I am setting this up on a Mac, or I understand that non-Mac setup is legacy/advanced
- [ ] I can open Terminal
- [ ] I can run `pwd` and `ls`
- [ ] I have a ChatGPT account with Codex access
- [ ] I have a dictation method
- [ ] I use Google Workspace if I want email/calendar integration
- [ ] Optional: I have a second Mac available for the remote-worker pattern

Next: [01-FIRST-LAUNCH.md](01-FIRST-LAUNCH.md)
