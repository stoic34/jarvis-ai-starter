# Desktop and Browser Automation

This file keeps its original name for link compatibility, but the recommended workflow is now broader than a Chrome extension.

Codex on macOS can support three useful control surfaces:

1. **Terminal and local shell** - reading files, editing files, running tools
2. **Browser workflows** - opening pages, navigating setup flows, researching
3. **Computer use** - clicking, typing, and inspecting local Mac apps when available

---

## Why This Matters

Many assistant setup tasks are not just command-line tasks.

Examples:

- Google Cloud OAuth setup
- App permission checks
- Obsidian vault setup
- Tailscale status checks
- Browser-based research
- Screen-based troubleshooting

The assistant should do the navigation and verification. You should handle sensitive approvals, passwords, and final sending.

---

## Recommended Path: Codex Desktop on Mac

Launch Codex Desktop:

```bash
codex app
```

Then confirm the app has the permissions needed for the workflows you want:

- Files and folders that contain your workspace
- Browser access if you want web navigation
- Accessibility and screen-related permissions if you want computer-control workflows

Ask the assistant:

> "Check what desktop or browser control you have available, then tell me what permissions are missing."

Do not grant broad permissions blindly. Grant the minimum needed for the workflows you actually want.

---

## Browser Workflows

Use browser workflows for:

- Research
- Reading documentation
- Filling non-sensitive forms
- Navigating setup screens while you authorize manually

Ask:

> "Open the browser and help me set up the Google Cloud OAuth client. I will handle passwords and final authorization clicks."

Rules:

- The assistant can navigate.
- The assistant can explain what to click.
- You handle passwords, payment details, and irreversible approvals.

---

## Computer Use Workflows

Use computer control when the task requires a real desktop app:

- Inspecting System Settings
- Checking Obsidian behavior
- Verifying an app is running
- Reading a local window
- Capturing visual evidence

Ask:

> "Use computer control to check whether Codex has the permissions it needs, then report only what you observed."

Good computer-use tasks are narrow and observable. Avoid vague instructions like "fix my computer."

---

## Legacy: Claude for Chrome

Claude Code users can still use Claude for Chrome if they prefer the legacy setup.

That path is no longer the recommended first setup because this starter kit now assumes Codex and `AGENTS.md`.

If you use Claude Code:

- Keep `CLAUDE.md`
- Read the legacy Claude for Chrome docs from Anthropic
- Treat `.claude/` as the Claude-specific capability layer

---

## Security Notes

Do not let any assistant:

- Enter passwords
- Enter credit card information
- Accept legal terms without your explicit approval
- Send email directly
- Move or delete important files without confirmation

The assistant navigates and drafts. You authorize and send.

---

## What You Accomplished

- Understood why Codex Desktop is recommended
- Separated terminal, browser, and computer-control workflows
- Kept Claude for Chrome as a legacy option

Next: [03-GOOGLE-INTEGRATION.md](03-GOOGLE-INTEGRATION.md)
