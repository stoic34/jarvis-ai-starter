# Troubleshooting

Common issues and how to fix them.

---

## Setup Issues

### "npx: command not found"

**Problem**: Node.js isn't installed or not in your PATH.

**Fix**:
```bash
# macOS
brew install node

# Windows
# Download from https://nodejs.org/
```

Then restart your terminal and try again.

---

### "gogcli: command not found"

**Problem**: gogcli isn't installed.

**Fix**:
```bash
# macOS
brew install gogcli/tap/gogcli

# Other platforms
# Download from https://github.com/gogcli/gogcli/releases
```

---

### Google OAuth "Access Denied" or "App not verified"

**Problem**: Your Google Cloud project needs OAuth consent screen configured.

**Fix**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to "APIs & Services" → "OAuth consent screen"
4. Set to "External" (or "Internal" if using Google Workspace)
5. Add your email as a test user
6. Try `gogcli auth login` again

---

### "weasyprint: command not found" (PDF generation fails)

**Problem**: WeasyPrint dependencies aren't installed.

**Fix**:
```bash
# macOS
brew install pango

# Then reinstall Python package
pip3 install weasyprint
```

---

### Python "externally-managed-environment" error

**Problem**: macOS Python 3.12+ uses PEP 668, blocking global pip installs.

**Fix**: Use a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or: .venv\Scripts\activate  # Windows
pip install -r tools/requirements.txt
```

---

## Runtime Issues

### Agent doesn't remember previous sessions

**This is expected.** Each Claude Code session starts fresh. That's why we use:
- `workspace/CONTEXT.md` — for standing context
- CONTINUATION notes — for in-progress work
- `vault/` notes — for persistent knowledge

**Tip**: Start each session with "Check for any CONTINUATION notes" or update CONTEXT.md with current priorities.

---

### Agent claims it can't use a tool that's installed

**Fix**: Check `workspace/TOOLS.md` — the agent reads this file to know what's available. If the tool isn't listed there, add it.

Then tell the agent: "Check workspace/TOOLS.md again — I've updated it."

---

### Agent tries to send an email directly

**This should never happen** — CLAUDE.md explicitly forbids it. If it does:
1. The `deny` rule in `.claude/settings.json` should block it
2. Cancel the operation
3. Remind the agent: "Only create drafts, never send"

---

### Pre-commit hook blocks a commit

**The hook found sensitive data in your staged files.**

Options:
1. **Remove the sensitive content** and re-stage the files
2. **Add false positives to the allowlist** in `evals/pii-scanner.py`
3. **Last resort**: `git commit --no-verify` (not recommended — bypasses the scanner)

To see what was flagged:
```bash
python3 evals/pii-scanner.py --staged
```

---

### Browser automation not working

**Check**:
1. Is the Claude for Chrome extension installed? Check `chrome://extensions/`
2. Is Chrome running? The extension needs an open Chrome window
3. Did you launch with `--chrome` flag? Check your alias

**If the extension is installed but not responding:**
- Close and reopen Chrome
- Check the extension's console for errors

---

### Audio transcription fails

**Check**:
1. Is `GEMINI_API_KEY` set in your environment?
   ```bash
   echo $GEMINI_API_KEY
   ```
2. Is the audio file a supported format? (m4a, mp3, wav, etc.)
3. Is the file too large? Gemini has upload limits.

**Set the API key**:
```bash
# Add to your shell profile (~/.zshrc or ~/.bashrc)
export GEMINI_API_KEY="your-key-here"
```

Get a key at [ai.google.dev](https://ai.google.dev/).

---

## Performance Issues

### Claude Code is slow to start

**Normal.** The first launch downloads the latest version via `npx`. Subsequent launches in the same terminal session are faster.

**Tip**: If you use it daily, consider installing globally:
```bash
npm install -g @anthropic-ai/claude-code
```

---

### Long responses get cut off

Claude has a maximum output length per response. If a response seems incomplete:
- Say "continue" to get the rest
- For very long outputs, ask for them in sections

---

## Getting More Help

1. **Claude Code docs**: [claude.ai/code/docs](https://claude.ai/code/docs)
2. **File an issue**: [GitHub Issues](https://github.com/stoic34/jarvis-ai-starter/issues)
3. **Ask your agent**: It can often diagnose and fix its own issues
