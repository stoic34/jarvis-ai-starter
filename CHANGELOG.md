# Changelog

All notable changes to the Jarvis AI Starter Kit.

---

## [2.0.0] — 2026-02-12

### Added
- **Component Taxonomy** — Three-tier system: prompt templates, skills, agents (`.claude/TAXONOMY.md`)
- **Workspace Identity** — Separated personal config from operational instructions (`workspace/IDENTITY.md`, `USER.md`, `TOOLS.md`, `CONTEXT.md`)
- **Session Continuity** — CONTINUATION notes for multi-session work
- **Software Development Protocol** — Auto-invoked on code tasks with complexity tiers
- **5-Gate Code Review** — Scope, patterns, security, minimalism, tests
- **Confidence Framework** — Signal HIGH/MEDIUM/LOW confidence on recommendations
- **Tool-Building Judgment** — Framework for when to build automation vs. do manually
- **Multi-Agent Safety** — Rules for running parallel Claude Code sessions
- **Security Infrastructure** — Enhanced PII scanner with blocklist support, pre-commit hook
- **Permission Model** — Tiered `.claude/settings.json` with pre-approved and blocked operations
- **Architecture Documentation** — How all components fit together (`docs/ARCHITECTURE.md`)
- **Troubleshooting Guide** — Common issues and fixes (`docs/TROUBLESHOOTING.md`)
- **Contributing Guide** — How to submit improvements (`docs/CONTRIBUTING.md`)
- **Expanded Vault Structure** — Projects/Active, Projects/Archive, Daily/journal, People, Archive
- **AWS Infrastructure Scaffold** — Secrets Manager, Lambda templates (cron + webhook), S3 vault backup, CloudWatch budget alerts (`infrastructure/`)
- **MCP Server Examples** — Weather API example and basic server template with setup guides (`mcp/`)

### Changed
- **CLAUDE.md** — Restructured to reference workspace/ for identity, added skill/agent protocols, dev workflow, session lifecycle
- **PII Scanner** — Now supports blocklist, staged-file scanning, allowlist, strict mode, severity grouping
- **.gitignore** — Added `.security/blocklist.txt`
- **Vault Structure** — Projects template moved to `Projects/Active/`
- **Settings** — Populated with balanced permission tier (pre-approve reads and local tools)

### Removed
- **Inline identity** — `[AGENT_NAME]` and `[USER_NAME]` moved from CLAUDE.md to workspace/ files
- **REGISTRY.md** — Replaced by `workspace/TOOLS.md`

---

## [1.0.0] — 2026-01-24

### Initial Release
- 90-minute onboarding flow with naming ceremony
- Google Workspace integration via gogcli (Gmail, Calendar, Contacts, Drive)
- Browser automation via Claude for Chrome
- Python tools: audio-transcribe.py, pdf-create.py, md-to-html.py
- Eval harness concept ("Horses, Not Cars" mental model)
- PII scanner for pre-publish security checks
- Obsidian vault starter structure (Projects, Daily, Reference)
- Setup guides for macOS and Windows
- Use case documentation with 22+ workflows
- Example prompts library
- YOLO mode documentation
- Integration stubs for Level 2+ expansions
