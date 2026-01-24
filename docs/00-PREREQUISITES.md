# Prerequisites: Before You Start

**Read this first.** These prerequisites will save you hours of frustration.

---

## Hardware: Use Your Daily Driver Laptop

**Use a laptop, not a desktop.**

This system is designed for the computer you actually work on every day. Your AI assistant will live on this machine, access your files, and become part of your workflow.

**Don't set this up on:**
- A spare desktop in the corner
- A shared family computer
- A machine you'll forget about

**Do set this up on:**
- Your primary work laptop
- The device you carry to meetings
- The computer where you actually do your work

---

## Terminal Basics: 5 Commands You Need to Know

Your AI assistant runs in a **terminal** (also called command line). If you've never used a terminal before, don't worry—you only need 5 commands.

### What is a Terminal?

A terminal is just another way to navigate your computer. Instead of clicking folders, you type commands.

**Think of it this way:**
- Finder/File Explorer = Visual navigation (point and click)
- Terminal = Text navigation (type commands)

They see the same files. Just different interfaces.

### The 5 Essential Commands

| Command | What It Does | Example |
|---------|--------------|---------|
| `ls` | **L**i**s**t files in current directory | `ls` → shows all files here |
| `pwd` | **P**rint **w**orking **d**irectory (where am I?) | `pwd` → `/Users/yourname/Documents` |
| `cd [folder]` | **C**hange **d**irectory | `cd Documents` → moves into Documents |
| `cd ~` | Go to home directory | `cd ~` → goes to `/Users/yourname` |
| `cd ..` | Go up one directory | `cd ..` → moves to parent folder |

### Pro Tips

- **Tab key autocompletes**: Type `cd Doc` then press Tab → `cd Documents`
- **You can't use your mouse**: Arrow keys move the cursor
- **Case matters**: `Documents` is different from `documents`
- **Paths use forward slashes**: Even on Windows in Git Bash

### Windows Users: Use Git Bash, Not PowerShell

When you install Git for Windows, it includes **Git Bash**—a terminal that understands the commands above.

**PowerShell** (the default Windows terminal) uses different commands. The commands above won't work there.

**Always use Git Bash** for this setup.

### Try It Now

1. Open Terminal (Mac) or Git Bash (Windows)
2. Type `pwd` and press Enter → You'll see your current location
3. Type `ls` and press Enter → You'll see files in that location
4. Type `cd ~` and press Enter → You're now in your home directory
5. Type `ls` again → You'll see Documents, Desktop, etc.

If this works, you're ready.

---

## Dictation: Talk, Don't Type

AI agents work best when you speak to them naturally. Typing long prompts is slow and unnatural.

**Get a dictation tool before you start.**

### Recommended: Wispr Flow ($10/month)

[Wispr Flow](https://wisprflow.ai/) is the best dictation tool for AI work:

- **One-key activation**: Press Function key, speak, release
- **Grammar correction**: Cleans up your speech automatically
- **Custom dictionary**: Teach it company names, jargon, technical terms
- **Works everywhere**: Terminal, browser, any app

Worth every penny if you're going to use AI daily.

### Free Alternatives

**Mac** (built-in):
- Press `Fn` twice to start dictation
- Or enable in System Settings → Keyboard → Dictation

**Windows** (built-in):
- Press `Win + H` to start dictation
- Works in any text field

The built-in options are fine to start. Upgrade to Wispr Flow once you're hooked.

### Why This Matters

When you're working with your AI assistant, you'll say things like:

> "Hey Jarvis, scan my inbox for anything urgent from the last 24 hours, summarize the top 3 items, and draft a response to the one from Sarah about the project timeline"

Typing that takes 30 seconds. Speaking it takes 8 seconds.

**Speaking is 4x faster.** And it's more natural—you'll give better instructions when you're talking instead of typing.

---

## Google Workspace: This Kit is Built for Google

**Important:** The core integrations in this kit are designed for **Google Workspace**.

### If You Use Google (Gmail, Google Calendar)

You're good to go. Everything will work.

### If You Use Microsoft 365 (Outlook, Teams)

You can still use this kit, but:
- Email/Calendar integrations won't work out of the box
- You'll need to find or build Microsoft integrations yourself
- We don't provide support for non-Google setups

### If You Use Something Else

Same as above. The core tools assume Google.

### Why Google?

Two reasons:

1. **Most people use it**: Gmail is the dominant email for individuals and small businesses
2. **Better API access**: Google's APIs are more accessible for this kind of automation

We're not anti-Microsoft. We just had to pick one, and Google is what most of our users have.

---

## Claude Subscription: You Need Max or Pro

Your AI assistant is powered by **Claude** from Anthropic.

### Which Plan?

| Plan | Cost | Best For |
|------|------|----------|
| **Free** | $0 | Testing only—not enough usage |
| **Pro** | $20/month | Light usage, getting started |
| **Max** | $100/month | Daily use, recommended |
| **Max 5X** | $200/month | Heavy use, multiple agents |

**We recommend Max** if you're serious about using this daily. The extra headroom means you won't hit limits in the middle of important work.

### Sign Up

Go to [claude.ai](https://claude.ai) and create an account if you don't have one.

---

## Checklist Before You Continue

Before moving to the next step, confirm:

- [ ] I'm on a laptop (my daily driver)
- [ ] I can open Terminal (Mac) or Git Bash (Windows)
- [ ] I can run `pwd` and `ls` successfully
- [ ] I have a dictation method (built-in or Wispr Flow)
- [ ] I use Google Workspace (Gmail, Google Calendar)
- [ ] I have a Claude account (Pro or Max recommended)

**All checked?** Continue to [01-FIRST-LAUNCH.md](01-FIRST-LAUNCH.md)

---

*Time to complete: 10-15 minutes*
