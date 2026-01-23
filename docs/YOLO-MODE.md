# YOLO Mode Setup

For the best experience with your AI assistant, you'll want to run Claude Code in a mode that allows it to work autonomously without asking permission for every action.

## What is YOLO Mode?

By default, Claude Code asks for permission before:
- Reading files
- Writing/editing files
- Running commands

This is safe but slow. "YOLO mode" (accept edits mode) lets Claude work more fluidly, like a real assistant who can just do things.

## Setting It Up

### Option 1: Command Line Flag

Run Claude Code with the flag:

```bash
claude --dangerously-skip-permissions
```

This skips all permission prompts for the session.

### Option 2: Create an Alias (Recommended)

Since Claude Code can't create shell aliases for you, you'll need to do this manually.

**On macOS/Linux (bash/zsh):**

1. Open your shell config file:
   ```bash
   # For zsh (default on modern Mac):
   nano ~/.zshrc

   # For bash:
   nano ~/.bashrc
   ```

2. Add this line at the end (replace "jarvis" with your agent's name):
   ```bash
   alias jarvis="claude --dangerously-skip-permissions"
   ```

3. Save and exit (Ctrl+X, then Y, then Enter)

4. Reload your shell:
   ```bash
   source ~/.zshrc  # or ~/.bashrc
   ```

5. Now you can start your AI with just:
   ```bash
   jarvis
   ```

**On Windows (PowerShell):**

1. Open PowerShell profile:
   ```powershell
   notepad $PROFILE
   ```

2. Add this line:
   ```powershell
   function jarvis { claude --dangerously-skip-permissions }
   ```

3. Save and close notepad

4. Reload profile:
   ```powershell
   . $PROFILE
   ```

5. Now use:
   ```powershell
   jarvis
   ```

## Is This Safe?

**Understand the tradeoffs:**

| Aspect | With Permissions | YOLO Mode |
|--------|------------------|-----------|
| Speed | Slower (constant approvals) | Fast (autonomous) |
| Control | High (approve everything) | Medium (trust the AI) |
| Learning | Good for beginners | Good once comfortable |
| Risk | Very low | Low (AI still has guardrails) |

**Built-in guardrails** (even in YOLO mode):
- AI won't delete files without asking
- AI won't send emails directly (only drafts)
- AI won't make financial transactions
- AI won't share sensitive data externally

**Recommendation:** Start with permissions enabled to see what Claude does. Once comfortable, switch to YOLO mode for efficiency.

## Combining with Your Vault

When you create the alias, you might also want to:

1. **Start in your vault directory:**
   ```bash
   alias jarvis="cd ~/Documents/Jarvis && claude --dangerously-skip-permissions"
   ```

2. **Set a specific model:**
   ```bash
   alias jarvis="claude --dangerously-skip-permissions --model claude-sonnet-4"
   ```

## Troubleshooting

**Alias not working?**
- Make sure you reloaded your shell config
- Check for typos in the alias definition
- Try opening a new terminal window

**Need to stop Claude mid-action?**
- Press `Ctrl+C` to interrupt
- Claude will stop and wait for your next instruction

---

*The AI can't create these aliases for you (shell config requires manual editing), but once set up, it makes the experience much smoother.*
