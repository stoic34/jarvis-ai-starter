# macOS Setup Guide

Complete setup instructions for running your AI assistant on macOS.

**Time Required:** 45-60 minutes

---

## What We're Installing

| Tool | Purpose |
|------|---------|
| **Homebrew** | Package manager for installing everything |
| **Git** | Version control (safety net for your vault) |
| **Node.js** | Required to run Claude Code |
| **Claude Code** | The AI assistant engine |
| **Obsidian** | Your knowledge base |
| **Python 3** | For running tools |
| **gogcli** | Gmail, Calendar, Contacts integration |

---

## Step 1: Open Terminal

1. Press `Cmd + Space` to open Spotlight
2. Type `Terminal` and press Enter
3. A window opens - this is your command line

---

## Step 2: Install Homebrew

Homebrew makes installing developer tools easy on Mac.

**Check if already installed:**
```bash
brew --version
```

If you see a version number, skip to Step 3.

**Install Homebrew:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the prompts (may ask for your Mac password).

**Important:** When it finishes, run the "Next steps" commands it shows:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Verify:**
```bash
brew --version
```

---

## Step 3: Install Git

```bash
brew install git
```

**Verify:**
```bash
git --version
```

**Configure Git:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 4: Install Node.js

Claude Code requires Node.js.

```bash
brew install node
```

**Verify:**
```bash
node --version
npm --version
```

---

## Step 5: Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

**Verify:**
```bash
claude --version
```

**First run - authenticate:**
```bash
claude
```

This will open a browser window to authenticate with your Anthropic account.

---

## Step 6: Install Python Dependencies

The tools in this kit require Python 3 and some packages.

**Check Python:**
```bash
python3 --version
```

If not installed:
```bash
brew install python
```

**Install tool dependencies:**
```bash
cd /path/to/jarvis-ai-starter
pip3 install -r tools/requirements.txt
```

---

## Step 7: Install gogcli

gogcli provides Gmail, Calendar, and Contacts integration.

```bash
brew install gogcli/tap/gogcli
```

**Authenticate:**
```bash
gogcli auth login
```

This opens a browser to authenticate with your Google account.

**Test:**
```bash
gogcli gmail search "is:unread" --max 5
```

---

## Step 8: Install Obsidian

1. Go to https://obsidian.md/
2. Download for macOS
3. Open the downloaded file and drag Obsidian to Applications
4. Launch Obsidian

**Open your vault:**
1. Click "Open folder as vault"
2. Navigate to `jarvis-ai-starter/vault/`
3. Click "Open"

---

## Step 9: Set Up Your AI Alias (Optional but Recommended)

Create a shortcut to launch your AI easily.

1. Open Terminal
2. Edit your shell config:
   ```bash
   nano ~/.zshrc
   ```
3. Add this line (change "jarvis" to your preferred name):
   ```bash
   alias jarvis="cd ~/path/to/jarvis-ai-starter && claude --dangerously-skip-permissions"
   ```
4. Save: `Ctrl+X`, then `Y`, then `Enter`
5. Reload:
   ```bash
   source ~/.zshrc
   ```

Now you can start your AI by typing `jarvis` in Terminal.

---

## Step 10: Initialize Git for Your Vault

Track all changes to your vault with Git.

```bash
cd /path/to/jarvis-ai-starter
git init
git add .
git commit -m "Initial vault setup"
```

---

## Step 11: Run Initial Setup

```bash
cd /path/to/jarvis-ai-starter
claude
```

Then say: "Let's do the initial setup"

Your AI will walk you through:
- Naming your assistant
- Testing tool connections
- Creating your first note

---

## Troubleshooting

**"command not found: brew"**
- Close Terminal and reopen
- Make sure you ran the "Next steps" after Homebrew install

**"command not found: claude"**
- Run `npm install -g @anthropic-ai/claude-code` again
- Make sure Node.js is installed correctly

**gogcli authentication failing**
- Make sure you're logged into the correct Google account
- Try `gogcli auth logout` then `gogcli auth login` again

**Python packages not installing**
- Try `pip3 install --user -r tools/requirements.txt`
- Check if pip3 is in your PATH

---

## Next Steps

1. Complete the onboarding with your AI
2. Try some example prompts from `Reference/Example-Prompts.md`
3. Set up browser integration (see BROWSER-SETUP.md)
4. Explore the use cases in `Reference/What-You-Can-Do.md`

---

*You're ready to go! Your AI assistant awaits.*
