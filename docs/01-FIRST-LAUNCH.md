# First Launch: Meet Your AI Assistant

In this step, you'll launch Claude Code for the first time, name your assistant, and create a shortcut to make launching easy forever.

**Time required:** 15-20 minutes

---

## Step 1: Download This Repository

If you haven't already:

1. Click the green **Code** button on this GitHub page
2. Select **Download ZIP**
3. Extract to a location you'll remember:
   - Mac: `~/Documents/jarvis-ai-starter`
   - Windows: `C:\Users\YourName\Documents\jarvis-ai-starter`

**Or use Git** (if you have it):
```bash
cd ~/Documents
git clone https://github.com/TarioGroup/jarvis-ai-starter.git
```

---

## Step 2: Launch Claude Code (No Installation Required)

Here's the magic: **you don't need to install Claude Code**. We use `npx` to run it directly.

### What is npx?

`npx` is a tool that comes with Node.js. It downloads and runs programs without installing them permanently.

**Why this matters:**
- No installation = no PATH issues
- No "command not found" errors
- It just works

### Install Node.js First

You need Node.js to use npx:

**Mac:**
```bash
# Using Homebrew (recommended)
brew install node

# Or download from https://nodejs.org/
```

**Windows:**
1. Go to [nodejs.org](https://nodejs.org/)
2. Download the LTS version
3. Run the installer (accept defaults)
4. Close and reopen Git Bash

**Verify it worked:**
```bash
node --version
npx --version
```

Both should show version numbers.

### Navigate to Your Vault

Open Terminal (Mac) or Git Bash (Windows):

```bash
cd ~/Documents/jarvis-ai-starter
```

Verify you're in the right place:
```bash
ls
```

You should see: `CLAUDE.md`, `README.md`, `docs/`, `vault/`, etc.

### Launch Claude Code

```bash
npx @anthropic-ai/claude-code
```

**First time?**
- It will download Claude Code (takes a minute)
- Then it opens a browser to authenticate with your Anthropic account
- Log in with your Claude account
- Return to the terminal—you're connected

---

## Step 3: The Naming Ceremony

Your AI assistant is now running. Time to give it a name.

**Say or type:**
> "Let's do the naming ceremony"

Your assistant will ask for:
1. **Your name** – What should it call you?
2. **Agent name** – What do you want to call it?

### Popular Agent Names

- **Jarvis** – The classic (Iron Man's AI)
- **Friday** – Tony Stark's other AI
- **Alfred** – Batman's butler
- **Henry** – Simple and friendly
- **Max** – Short and professional

Pick something that feels right. You'll be saying this name a lot.

**What happens:** Claude updates `CLAUDE.md` with your names, making the agent yours.

---

## Step 4: Create Your Launch Alias

Right now, launching your agent requires:
1. Opening terminal
2. Navigating to the right directory
3. Typing the long npx command

**Let's fix that.** We'll create an alias so you just type your agent's name.

### What is an Alias?

An alias is a shortcut. Instead of typing:
```bash
cd ~/Documents/jarvis-ai-starter && npx @anthropic-ai/claude-code --dangerously-skip-permissions --chrome
```

You type:
```bash
jarvis
```

Same result. Much easier.

### Understanding the Launch Command

Let's break down what the full command does:

```bash
cd ~/Documents/jarvis-ai-starter && npx @anthropic-ai/claude-code --dangerously-skip-permissions --chrome
```

| Part | What It Does |
|------|--------------|
| `cd ~/Documents/jarvis-ai-starter` | Navigate to your vault directory |
| `&&` | If that succeeds, then run... |
| `npx @anthropic-ai/claude-code` | Launch Claude Code |
| `--dangerously-skip-permissions` | YOLO mode (explained below) |
| `--chrome` | Enable browser control |

### What is YOLO Mode (--dangerously-skip-permissions)?

By default, Claude Code asks permission before every action:
> "Can I read this file?" → Yes
> "Can I edit this file?" → Yes
> "Can I run this command?" → Yes

This gets tedious fast.

**YOLO mode** (the `--dangerously-skip-permissions` flag) tells Claude: "I trust you. Just do it."

**Is it dangerous?**
- It's called "dangerously" as a warning, not because it's actually dangerous
- Claude still follows all safety rules
- It just stops asking permission for routine operations
- Use it in your personal vault where you trust the agent

**Don't use YOLO mode:**
- On production servers
- In shared environments
- When experimenting with untested tools

**Do use YOLO mode:**
- In your personal vault
- For daily assistant work
- When productivity matters

### What Does --chrome Do?

The `--chrome` flag enables browser automation. With it, your agent can:
- Open websites and navigate pages
- Fill out forms
- Click buttons
- Take screenshots
- Read page content

**Why this matters:** When you set up Google integrations later, Claude will navigate Google Cloud Console *for you*. You just watch and authorize when needed.

### Create the Alias

**Tell your agent:**
> "Create my launch alias so I can start you by just typing [AGENT_NAME]"

Claude will:
1. Detect your operating system
2. Find your shell profile (~/.zshrc, ~/.bashrc, or PowerShell $PROFILE)
3. Add the alias
4. Reload the profile or tell you to restart terminal

**Or do it manually:**

**Mac/Linux** – Add to `~/.zshrc` (or `~/.bashrc`):
```bash
alias jarvis='cd ~/Documents/jarvis-ai-starter && npx @anthropic-ai/claude-code --dangerously-skip-permissions --chrome'
```

Then reload:
```bash
source ~/.zshrc
```

**Windows (Git Bash)** – Add to `~/.bashrc`:
```bash
alias jarvis='cd ~/Documents/jarvis-ai-starter && npx @anthropic-ai/claude-code --dangerously-skip-permissions --chrome'
```

Then reload:
```bash
source ~/.bashrc
```

**Windows (PowerShell)** – Add to your profile:
```powershell
notepad $PROFILE
```

Add this function:
```powershell
function jarvis {
    Set-Location "$HOME\Documents\jarvis-ai-starter"
    npx @anthropic-ai/claude-code --dangerously-skip-permissions --chrome
}
```

Save and restart PowerShell.

### Test Your Alias

Close your terminal completely, then reopen it.

Type your agent name:
```bash
jarvis
```

Your agent should launch, ready to work.

---

## Step 5: Verify Everything Works

Before continuing, let's verify your setup.

**Say to your agent:**
> "Verify my setup is working"

Claude should confirm:
- It knows your name
- It knows its own name
- It can read files in the vault
- The alias is working (you're here, so it is)

---

## What You've Accomplished

- Launched Claude Code without installation hassles
- Named your AI assistant
- Created a one-word launch command
- Enabled YOLO mode for productivity
- Enabled browser control for automation

**Next:** Set up browser control → [02-CHROME-EXTENSION.md](02-CHROME-EXTENSION.md)

---

## Troubleshooting

### "npx: command not found"

Node.js isn't installed or isn't in your PATH.
- Reinstall Node.js from [nodejs.org](https://nodejs.org/)
- Windows: Make sure to restart Git Bash after installing

### "Authentication failed"

- Make sure you have a Claude account at [claude.ai](https://claude.ai)
- Try the authentication URL again
- Check that you're using the right account

### Alias doesn't work after restart

- Make sure you added it to the right file:
  - Mac with zsh: `~/.zshrc`
  - Mac with bash: `~/.bashrc`
  - Windows Git Bash: `~/.bashrc`
  - Windows PowerShell: `$PROFILE`
- Make sure you saved the file
- Try running `source ~/.zshrc` (or equivalent)

### "Permission denied" errors

On Mac/Linux, you might need to make the shell profile readable:
```bash
chmod 644 ~/.zshrc
```

---

*Time to complete: 15-20 minutes*
