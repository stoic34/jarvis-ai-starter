# Component Taxonomy

Your AI assistant organizes its capabilities into three tiers. This guide helps you understand when each type is used.

## Quick Decision Tree

```
Is it routine and quick (< 2 min)?
  → YES → Prompt Template (command)

Does it need a structured, repeatable procedure?
  → YES → Skill

Does it require deep domain expertise or a separate thinking context?
  → YES → Agent

None of the above?
  → Handle directly in conversation
```

## The Three Tiers

### 1. Prompt Templates (Commands)

**What**: Pre-written prompts with variable slots for routine workflows.
**When**: Quick, repeatable tasks you do regularly.
**How**: Natural language or reference by name.
**Location**: `.claude/prompts/`

| Example | What It Does |
|---------|-------------|
| `morning-routine` | Check inbox, calendar, set priorities |
| `project-kickoff` | Create project note, set up structure |
| `research-brief` | Structured research on a topic |

**Format**:
```yaml
---
name: template-name
description: "When to use this"
variables:
  - name: topic
    required: true
---
# Template content with {{topic}} placeholders
```

---

### 2. Skills

**What**: Structured workflows with eligibility checks, steps, and quality gates.
**When**: Tasks that need methodology — not just "do the thing" but "do the thing correctly."
**How**: Auto-detected from context, or invoked with `/skill-name`.
**Location**: `.claude/skills/`

| Example | What It Does |
|---------|-------------|
| `eval-harness` | Self-verification for multi-step tasks |
| `code-review` | 5-gate quality review for code changes |
| `session-handoff` | End-of-session context capture |
| `content-ingest` | URL or file → structured vault note |

**Format**:
```yaml
---
name: skill-name
description: "What it does — when to use it"
requires:
  bins: ["git"]           # Required CLI tools
  env: ["API_KEY"]        # Required environment variables
  tools: ["script.py"]    # Required local scripts
---
# Workflow steps, guardrails, output format
```

**Key Property**: Skills check their dependencies before running. If `requires.bins` lists `git` and `git` isn't installed, the skill says so instead of failing silently.

**Skills vs. Tools**: A tool is `git commit`. A skill is "commit workflow with message formatting, scope checking, and pre-commit verification." Skills add **judgment and methodology** on top of tools.

---

### 3. Agents

**What**: Specialized AI personas with deep domain expertise and distinct reasoning patterns.
**When**: Complex problems where a generalist would miss nuances.
**How**: Spawned as subagents via the Task tool — separate context from main conversation.
**Location**: `.claude/agents/`

| Example | What It Does |
|---------|-------------|
| `researcher` | Deep web/knowledge research with source evaluation |
| `writer` | Content creation with audience awareness |
| `developer` | Software development with code review gates |

**Format**:
```yaml
---
name: agent-name
description: "Domain expertise and when to invoke"
---
# Purpose, scope, tools, behavioral guidelines, output formats
```

**Key Property**: Agents run in a **separate context** from your main conversation. This means:
- They don't pollute your main thread with research noise
- They can think independently without bias from prior conversation
- Multiple agents can work in parallel on different aspects

**When NOT to use agents**: Simple tasks, quick lookups, anything that doesn't need specialized expertise. Don't spawn an agent to check the weather.

---

## Comparison Table

| Aspect | Template | Skill | Agent |
|--------|----------|-------|-------|
| **Complexity** | Low | Medium | High |
| **Duration** | < 2 min | 2-30 min | 5 min - hours |
| **Context** | Main conversation | Main conversation | Separate context |
| **Reusability** | High (daily use) | Medium (weekly) | Low (as-needed) |
| **Quality gates** | None | Built-in checks | Domain-specific |
| **Customization** | Variable slots | Workflow steps | Full persona |

## How They Work Together

A complex task might use all three:

1. **Template** kicks off a morning routine
2. Routine triggers a **skill** to process inbox items
3. One inbox item requires deep research → spawns a **researcher agent**
4. Agent returns findings → skill formats them into a note
5. Template wraps up with today's priorities

## Adding Your Own

### New Template
Create a `.md` file in `.claude/prompts/` with YAML frontmatter.

### New Skill
Create a folder in `.claude/skills/your-skill/` with a `skill.md` file.

### New Agent
Create a `.md` file in `.claude/agents/` with the agent definition.

See the existing examples in each directory for the format.
