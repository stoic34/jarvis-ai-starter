# macOS Setup Guide

Complete setup instructions for the recommended Codex-first assistant on Mac.

**Time required:** 45-60 minutes

---

## What We're Installing

| Tool | Purpose |
|------|---------|
| Homebrew | Package manager |
| Git | Version control and safety |
| Node.js | Required for the Codex CLI install path |
| Codex | AI assistant runtime |
| Obsidian | Knowledge base |
| Python 3 | Local tools |
| gogcli | Gmail, Calendar, Drive, and Contacts |
| Tailscale | Optional remote Mac access |

---

## Step 1: Open Terminal

1. Press `Cmd + Space`
2. Type `Terminal`
3. Press Enter

---

## Step 2: Install Homebrew

Check:

```bash
brew --version
```

If missing:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Run the "Next steps" commands Homebrew prints at the end, then verify:

```bash
brew --version
```

---

## Step 3: Install Git

```bash
brew install git
git --version
```

Configure:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---

## Step 4: Install Node.js

```bash
brew install node
node --version
npm --version
```

---

## Step 5: Install Codex

```bash
npm install -g @openai/codex
codex --version
```

If Codex is already installed:

```bash
codex update
```

Launch and sign in:

```bash
codex
```

To open the desktop app:

```bash
codex app
```

---

## Step 6: Download the Starter Kit

```bash
cd ~/Documents
git clone https://github.com/stoic34/jarvis-ai-starter.git
cd jarvis-ai-starter
```

Verify:

```bash
ls AGENTS.md README.md docs vault workspace
```

---

## Step 7: Install Python Dependencies

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt
```

---

## Step 8: Install gogcli

```bash
brew install gogcli/tap/gogcli
gogcli auth login
gogcli gmail search "is:unread" --max 5
```

The assistant should only create drafts. It must never send email directly.

---

## Step 9: Install Obsidian

1. Download Obsidian from https://obsidian.md/
2. Install it in Applications
3. Open `jarvis-ai-starter/vault/` as a vault

---

## Step 10: Create a Launch Alias

Edit your shell config:

```bash
nano ~/.zshrc
```

Add:

```bash
alias jarvis='cd ~/Documents/jarvis-ai-starter && codex -s workspace-write -a on-request'
```

Reload:

```bash
source ~/.zshrc
```

Launch:

```bash
jarvis
```

---

## Step 11: Run Initial Setup

In Codex, say:

> "Let's do the initial setup."

The assistant should:

- Read `AGENTS.md`
- Ask for your name and assistant name
- Update `workspace/USER.md`
- Update `workspace/IDENTITY.md`
- Check `workspace/TOOLS.md`
- Capture your first note in `vault/Daily/inbox.md`

---

## Optional: Remote Mac Worker

For phone-triggered work, repeat the core setup on a second Mac and read [05-REMOTE-MAC.md](05-REMOTE-MAC.md).

At minimum, verify:

- Codex is installed and signed in
- Tailscale or private networking works
- Screen Sharing or SSH works
- the vault is available
- sleep settings will not interrupt work

---

## Troubleshooting

**`codex: command not found`**

- Restart Terminal
- Reinstall Codex with `npm install -g @openai/codex`
- Check `npm config get prefix` if global npm binaries are not in PATH

**Homebrew missing after install**

- Close and reopen Terminal
- Run the Homebrew shellenv command printed by the installer

**gogcli authentication failing**

- Confirm the right Google account
- Try `gogcli auth logout`, then `gogcli auth login`

**Python package install fails**

- Use the virtual environment shown above
- Do not fight system Python

---

## Next Steps

1. Complete onboarding
2. Open the vault in Obsidian
3. Connect Google Workspace
4. Enable desktop/browser automation where needed
5. Consider the remote Mac worker pattern
