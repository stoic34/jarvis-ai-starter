# Contributing

We welcome contributions to make Jarvis AI Starter better for everyone.

---

## What We're Looking For

### High Priority
- **New prompt templates** — workflows people use daily
- **Skill definitions** — structured procedures for common tasks
- **Integration patterns** — connecting new services and APIs
- **Bug fixes** — especially in setup guides and tools
- **Documentation improvements** — clearer explanations, more examples

### Nice to Have
- **Platform support** — Windows improvements, Linux testing
- **Tool improvements** — better error handling, new features
- **Eval patterns** — new self-verification approaches
- **Translations** — setup guides in other languages

### Not Looking For
- **AI model comparisons** — this kit is built for Claude Code
- **Proprietary integrations** — must be usable by anyone
- **Complex infrastructure** — keep it simple, progressive disclosure

---

## How to Contribute

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR-USERNAME/jarvis-ai-starter.git
cd jarvis-ai-starter
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

Follow the patterns in existing files:
- **Prompt templates**: See `.claude/prompts/` for format
- **Skills**: See `.claude/skills/` for structure
- **Agents**: See `.claude/agents/` for format
- **Tools**: See `tools/` for Python script patterns
- **Docs**: See `docs/` for documentation style

### 4. Run Security Scan

```bash
python3 evals/pii-scanner.py
```

Make sure there are no findings before submitting.

### 5. Test

- If you added a tool, verify it works: `python3 evals/test-tools.py`
- If you modified CLAUDE.md, test the onboarding flow
- If you added a skill, verify the frontmatter is valid

### 6. Submit a Pull Request

- Clear title describing the change
- Brief description of what and why
- Reference any related issues

---

## Style Guide

### Documentation
- Use clear, simple language
- Write for a non-technical audience (unless in a technical section)
- Include examples and expected output
- Use consistent markdown formatting

### Code (Python)
- Follow PEP 8
- Include `--help` output for CLI tools
- Use `argparse` for argument parsing
- Include basic error handling

### Skills
- Use YAML frontmatter with `name`, `description`, `requires`
- Document the workflow step-by-step
- Include "When to use" and "When NOT to use" sections
- List dependencies in the `requires` block

### Prompt Templates
- Use YAML frontmatter with `name`, `description`, `variables`
- Keep templates focused on a single workflow
- Use `{{variable}}` syntax for user-provided values
- Include a brief description of what the template does

---

## Security Rules

**Before submitting a PR, ensure:**

1. No personal information (emails, phone numbers, real names)
2. No API keys, tokens, or credentials
3. No company-specific references
4. No internal URLs or infrastructure details
5. Example data uses `example.com`, `John Doe`, etc.
6. PII scanner passes clean: `python3 evals/pii-scanner.py`

---

## Code of Conduct

- Be respectful and constructive
- Focus on the work, not the person
- Help newcomers get started
- Give credit where due

---

## Questions?

Open a [GitHub Discussion](https://github.com/stoic34/jarvis-ai-starter/discussions) or file an issue.
