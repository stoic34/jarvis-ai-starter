# First Launch: Meet Your AI Assistant

In this step, you install Codex, open this starter kit, and create a one-word launch command.

**Time required:** 20-30 minutes

---

## Step 1: Download This Repository

Download the repo or clone it:

```bash
cd ~/Documents
git clone https://github.com/stoic34/jarvis-ai-starter.git
cd jarvis-ai-starter
```

If you downloaded a ZIP, extract it to:

```text
~/Documents/jarvis-ai-starter
```

Verify:

```bash
ls
```

You should see `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/`, `workspace/`, `tools/`, and `vault/`.

---

## Step 2: Install Codex

Install Codex using the current OpenAI instructions for your preferred client.

Common CLI path:

```bash
npm install -g @openai/codex
```

Then verify:

```bash
codex --version
```

If Codex is already installed:

```bash
codex update
```

You can also launch the desktop app:

```bash
codex app
```

Sign in with your ChatGPT account when prompted.

---

## Step 3: Launch in This Workspace

From the starter kit folder:

```bash
cd ~/Documents/jarvis-ai-starter
codex
```

Codex should read `AGENTS.md` from the repo root.

If you want to start in a balanced approval mode:

```bash
codex -s workspace-write -a on-request
```

This lets the assistant edit files in the workspace while still asking when it decides an action needs approval.

---

## Step 4: Naming Ceremony

Say or type:

> "Let's do the naming ceremony"

The assistant should ask:

1. Your name
2. The assistant's name
3. Your timezone and location

It will update:

- `workspace/IDENTITY.md`
- `workspace/USER.md`

---

## Step 5: Create Your Launch Alias

Create a shortcut so you can launch the assistant by typing its name.

For macOS zsh:

```bash
nano ~/.zshrc
```

Add this line, replacing `jarvis` if you chose another assistant name:

```bash
alias jarvis='cd ~/Documents/jarvis-ai-starter && codex -s workspace-write -a on-request'
```

Reload:

```bash
source ~/.zshrc
```

Test:

```bash
jarvis
```

---

## Step 6: Verify Setup

Ask:

> "Verify my setup is working."

The assistant should check:

- It can read `AGENTS.md`
- It can read `workspace/USER.md` and `workspace/IDENTITY.md`
- It can see `vault/`
- It can run basic shell commands
- It can inspect `workspace/TOOLS.md`

---

## Optional: Claude Code Compatibility

If you want to use Claude Code too, keep `CLAUDE.md` in place. It now acts as a compatibility loader that tells Claude Code to read `AGENTS.md`.

Do not fork the instructions into two separate systems unless you have a specific reason. The whole point is to keep one portable operating layer.

---

## What You Accomplished

- Installed or updated Codex
- Opened the starter kit as a Codex workspace
- Confirmed the assistant reads `AGENTS.md`
- Named the assistant
- Created a one-word launch command

Next: [02-CHROME-EXTENSION.md](02-CHROME-EXTENSION.md)
