# Windows Setup Guide

Complete setup instructions for running your AI assistant on Windows.

**Time Required:** 60-90 minutes

---

## What We're Installing

| Tool | Purpose |
|------|---------|
| **Windows Terminal** | Modern terminal for Windows |
| **Git for Windows** | Version control (safety net for your vault) |
| **Node.js** | Required to run Claude Code |
| **Claude Code** | The AI assistant engine |
| **Obsidian** | Your knowledge base |
| **Python 3** | For running tools |
| **gogcli** | Gmail, Calendar, Contacts integration |

---

## Step 1: Install Windows Terminal

Windows Terminal is Microsoft's modern terminal - much better than Command Prompt.

**From Microsoft Store:**
1. Open Microsoft Store (search "Microsoft Store" in Windows)
2. Search for "Windows Terminal"
3. Click "Get" or "Install"

**Or download directly:**
- Go to: https://aka.ms/terminal
- Download and install

**Launch:** Press `Windows + S`, type "Windows Terminal", press Enter

---

## Step 2: Install Git for Windows

Git is the version control system that tracks every change to your vault.

1. Go to: https://git-scm.com/download/win
2. Click "Click here to download" (64-bit version)
3. Run the installer

**Important settings during install:**
- Adjusting PATH: Select **"Git from the command line and also from 3rd-party software"**
- Line endings: Select **"Checkout as-is, commit as-is"**
- Everything else: defaults are fine

**Verify:** Open Windows Terminal and type:
```
git --version
```

**Configure Git:**
```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 3: Install Node.js

Claude Code requires Node.js.

1. Go to: https://nodejs.org/
2. Download the **LTS** version (recommended)
3. Run the installer
4. Accept defaults

**Verify:** Open a new Windows Terminal and type:
```
node --version
npm --version
```

---

## Step 4: Install Claude Code

In Windows Terminal:
```
npm install -g @anthropic-ai/claude-code
```

**Verify:**
```
claude --version
```

**First run - authenticate:**
```
claude
```

This opens a browser to authenticate with your Anthropic account.

---

## Step 5: Install Python

1. Go to: https://www.python.org/downloads/
2. Download latest Python 3
3. Run the installer

**Important:** Check the box that says **"Add Python to PATH"** before clicking Install!

**Verify:**
```
python --version
pip --version
```

**Install tool dependencies:**
```
cd C:\path\to\jarvis-ai-starter
pip install -r tools/requirements.txt
```

---

## Step 6: Install gogcli

gogcli provides Gmail, Calendar, and Contacts integration.

1. Go to: https://github.com/gogcli/gogcli/releases
2. Download the Windows binary (gogcli_windows_amd64.zip)
3. Extract the zip file
4. Move `gogcli.exe` to a folder in your PATH (like `C:\Users\YourName\bin\`)

**Or add to PATH:**
1. Extract to `C:\Program Files\gogcli\`
2. Add that folder to your system PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" under User variables
   - Add `C:\Program Files\gogcli\`

**Authenticate:**
```
gogcli auth login
```

This opens a browser to authenticate with your Google account.

**Test:**
```
gogcli gmail search "is:unread" --max 5
```

---

## Step 7: Install Obsidian

1. Go to: https://obsidian.md/
2. Download for Windows
3. Run the installer

**Open your vault:**
1. Launch Obsidian
2. Click "Open folder as vault"
3. Navigate to `jarvis-ai-starter\vault\`
4. Click "Open"

---

## Step 8: Set Up Your AI Alias (Optional but Recommended)

Create a shortcut to launch your AI easily.

**PowerShell method:**

1. Open Windows Terminal (PowerShell)
2. Create/edit your profile:
   ```powershell
   notepad $PROFILE
   ```
   (If it asks to create the file, click Yes)

3. Add this line (change "jarvis" to your preferred name):
   ```powershell
   function jarvis {
       Set-Location "C:\path\to\jarvis-ai-starter"
       claude --dangerously-skip-permissions
   }
   ```

4. Save and close Notepad

5. Reload profile:
   ```powershell
   . $PROFILE
   ```

Now type `jarvis` to start your AI.

---

## Step 9: Initialize Git for Your Vault

Track all changes to your vault with Git.

```
cd C:\path\to\jarvis-ai-starter
git init
git add .
git commit -m "Initial vault setup"
```

---

## Step 10: Run Initial Setup

```
cd C:\path\to\jarvis-ai-starter
claude
```

Then say: "Let's do the initial setup"

Your AI will walk you through:
- Naming your assistant
- Testing tool connections
- Creating your first note

---

## Troubleshooting

**"'git' is not recognized"**
- Close Windows Terminal and reopen
- Make sure you selected the right PATH option during Git install
- Try reinstalling Git

**"'claude' is not recognized"**
- Close Windows Terminal and reopen
- Run `npm install -g @anthropic-ai/claude-code` again
- Make sure Node.js is installed

**"'python' is not recognized"**
- Make sure you checked "Add Python to PATH" during install
- Try reinstalling Python with that option

**gogcli not working**
- Make sure the gogcli.exe location is in your PATH
- Try running with full path: `C:\path\to\gogcli.exe auth login`

**PowerShell profile not loading**
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Then try creating the profile again

---

## Windows-Specific Tips

**Voice Memos:**
- Windows voice recordings are typically in `C:\Users\YourName\Documents\Sound Recordings\`
- Or use the Windows Voice Recorder app

**File Paths:**
- Use forward slashes `/` or escaped backslashes `\\` in paths
- Or use raw strings in Python: `r"C:\path\to\file"`

**Terminal:**
- Windows Terminal supports multiple tabs
- You can customize colors and fonts in Settings

---

## Next Steps

1. Complete the onboarding with your AI
2. Try some example prompts from `Reference/Example-Prompts.md`
3. Set up browser integration (see BROWSER-SETUP.md)
4. Explore the use cases in `Reference/What-You-Can-Do.md`

---

*You're ready to go! Your AI assistant awaits.*
