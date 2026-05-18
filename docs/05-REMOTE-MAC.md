# Remote Mac Worker Pattern

This is the setup for a separate MacBook or Mac mini that stays online so you can trigger AI assistant work from your phone.

The pattern is simple:

```
Phone instruction -> remote Mac -> Codex executes locally -> draft/report back
```

The phone is the control surface. The Mac does the real work.

---

## Why Use a Separate Mac?

A local AI assistant depends on local context:

- Vault files
- Google auth
- app permissions
- local tools
- shell environment
- browser sessions
- desktop access

If that environment only exists on your laptop, the assistant is unavailable when the laptop is asleep, closed, or not with you.

A second Mac solves that by acting as an always-on worker.

---

## Recommended Hardware

Good options:

- Mac mini on power
- Spare MacBook on power
- Office Mac that stays awake

Avoid:

- Shared family machines
- Machines without reliable internet
- Machines where other people can access the assistant context

---

## Required Setup

On the remote Mac:

1. Install Codex
2. Sign in with the right ChatGPT account
3. Install Tailscale or equivalent private networking
4. Enable Screen Sharing or another remote desktop method
5. Install Git, Python, Obsidian, and `gogcli`
6. Make the vault available locally
7. Confirm sleep settings will not interrupt work
8. Confirm the Codex app and CLI can launch from that account

---

## Verification Checklist

Ask the assistant to verify:

- Tailscale is online
- SSH or Screen Sharing is reachable
- the logged-in user can read the vault
- Codex is installed
- Codex Desktop is running if desktop workflows are needed
- `codex --version` works in the shell
- `gogcli --help` works
- `python3 --version` works
- disk space is healthy
- sleep settings are appropriate

Do not assume the remote shell and the desktop app have identical environments. A desktop Codex app can be running even if the SSH shell cannot find `codex` in its PATH.

---

## Phone Trigger Options

Start simple:

- Text yourself the task
- Use iMessage/SMS sync to the Mac
- Use a private Slack or chat channel
- Use a short email to yourself

More advanced:

- A dedicated command channel
- A LaunchAgent that watches an inbox folder
- A small webhook receiver
- A scheduled automation queue

Keep the first version boring. The goal is reliable capture and execution, not a complicated command bus.

---

## iMessage and SMS

On Mac, iMessage/SMS is often the cleanest first communication channel:

- The Mac already receives the messages
- The assistant can inspect local message context if permissioned
- It avoids unofficial WhatsApp automation risks

WhatsApp is possible only through less stable or unofficial routes. Treat it as a later integration.

---

## Operating Rules

- The remote Mac should draft, not send.
- The assistant should report what it did and what needs review.
- Keep secrets out of synced folders.
- Use a private network rather than exposing services publicly.
- Verify current state before changing power, firewall, or remote-access settings.

---

## Example Prompt

> "Check whether the remote Mac is ready to act as my always-on Codex worker. Verify Tailscale, SSH or Screen Sharing, Codex app and CLI availability, vault access, core tools, disk space, and sleep settings. Report facts only and do not change settings without asking."
