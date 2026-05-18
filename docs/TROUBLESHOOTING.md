# Troubleshooting

Common issues and how to fix them.

---

## Setup Issues

### `codex: command not found`

Codex is not installed or your shell cannot find it.

Fix:

```bash
npm install -g @openai/codex
codex --version
```

Then restart Terminal.

If installed through the desktop app, also try:

```bash
codex app
```

---

### Codex starts but ignores the starter-kit instructions

You probably launched Codex from the wrong directory.

Fix:

```bash
cd ~/Documents/jarvis-ai-starter
ls AGENTS.md
codex
```

`AGENTS.md` must be at the workspace root.

---

### `gogcli: command not found`

Install it:

```bash
brew install gogcli/tap/gogcli
```

Then:

```bash
gogcli auth login
```

---

### Google OAuth "Access Denied" or "App not verified"

Your Google Cloud project likely needs OAuth consent configured.

Fix:

1. Open Google Cloud Console
2. Select the project
3. Go to APIs & Services
4. Configure the OAuth consent screen
5. Add yourself as a test user if needed
6. Re-run `gogcli auth login`

Ask the assistant to navigate and explain, but you should handle final authorization clicks.

---

### Python `externally-managed-environment` error

Use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt
```

---

## Runtime Issues

### The assistant does not remember previous sessions

This is normal. Persistent context lives in files:

- `workspace/CONTEXT.md`
- `vault/Daily/`
- continuation notes
- project notes

Start by asking:

> "Read the current context and tell me what you know before we continue."

---

### The assistant claims a tool is unavailable

Ask it to check in order:

1. `workspace/TOOLS.md`
2. `tools/`
3. `tool-name --help`
4. shell PATH

Do not accept "I can't" until it has checked the local tool inventory.

---

### The assistant tries to send an email

Stop it.

The rule is draft-only:

```bash
gogcli gmail drafts create ...
```

Never:

```bash
gogcli gmail send ...
gogcli gmail drafts send ...
```

---

### Desktop or browser control is unavailable

Check:

- Are you using Codex Desktop, not only a headless shell?
- Has macOS granted the needed permissions?
- Is the browser open?
- Did you ask for a task that actually requires UI control?

Ask:

> "Inspect what desktop and browser tools are available in this session and list missing permissions."

---

### Remote Mac is unavailable

Check:

- Is the Mac awake?
- Is it on power?
- Is Tailscale connected?
- Is Screen Sharing or SSH reachable?
- Is Codex installed for the correct macOS user?
- Can that user read the vault path?

Important: the desktop app and SSH shell may not share the same PATH. A remote shell can fail to find `codex` even while the Codex desktop app is running.

---

### Audio transcription fails

Check:

```bash
echo $GEMINI_API_KEY
```

If missing, set it in your shell profile:

```bash
export GEMINI_API_KEY="your-key-here"
```

Then retry with a supported audio format.

---

## Getting More Help

- Read `AGENTS.md`
- Read `workspace/TOOLS.md`
- Read [docs/05-REMOTE-MAC.md](05-REMOTE-MAC.md) for remote setup
- File an issue at https://github.com/stoic34/jarvis-ai-starter/issues
