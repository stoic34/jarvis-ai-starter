# Autonomy Modes

The old starter kit called this "YOLO mode" because Claude Code used a high-autonomy launch flag.

The Codex-first setup uses a more explicit idea: choose the right **sandbox** and **approval** level for the workspace.

---

## Recommended Starting Mode

Start with:

```bash
codex -s workspace-write -a on-request
```

This lets Codex work inside the starter-kit workspace while preserving human review for higher-risk actions.

---

## Safer Exploration

Use read-only mode when you only want analysis:

```bash
codex -s read-only -a on-request
```

Good for audits, planning, unfamiliar repos, and machine checks before changing settings.

---

## More Autonomous Work

Use looser settings only in a trusted local workspace where you have backups and version control.

Before increasing autonomy, confirm:

- the repo is under Git
- secrets are not in tracked files
- email sending is blocked by instruction and habit
- destructive commands are not needed
- you know how to interrupt the session

Do not start new users in a maximum-autonomy mode.

---

## Launch Alias

For macOS zsh:

```bash
alias jarvis='cd ~/Documents/jarvis-ai-starter && codex -s workspace-write -a on-request'
```

Reload:

```bash
source ~/.zshrc
```

---

## Non-Negotiable Guardrails

Even in more autonomous modes, the assistant must not:

- send email directly
- enter passwords or financial credentials
- make purchases
- expose private files externally without approval
- delete important files without explicit confirmation

The assistant drafts and prepares. The user authorizes and sends.
