# Security Infrastructure

This directory contains security tools that prevent accidental leaks of private information.

## Files

| File | Committed? | Purpose |
|------|-----------|---------|
| `blocklist.txt` | NO (.gitignored) | Your private terms that should never appear in commits |
| `README.md` | YES | This documentation |

## How It Works

### Three-Layer Defense

1. **Pre-commit hook** — Runs `evals/pii-scanner.py --staged` on every commit. Blocks the commit if it finds PII or blocklist terms.

2. **Blocklist** — Your private `.security/blocklist.txt` contains terms specific to you (company names, employee names, internal domains). This file is gitignored and never committed.

3. **Full-repo scan** — Run `python3 evals/pii-scanner.py` manually to scan the entire repo before publishing.

## Setup

The pre-commit hook is installed automatically when you clone this repo and run setup:

```bash
# Manual install (if not already set up)
cp .security/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Adding to Your Blocklist

Edit `.security/blocklist.txt` and add one term per line:

```
my-company-name
employee@company.com
internal.company.com
```

The scanner matches case-insensitively. For regex patterns, prefix with `regex:`:

```
regex:\bACCT-\d{6}\b
```
