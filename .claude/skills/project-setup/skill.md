---
name: project-setup
description: "Scaffold a new project with note, context update, and optional notifications. Use when the user starts a new initiative, task, or area of work that needs tracking."
requires:
  bins: []
  env: []
  tools: []
---

# Project Setup

## When to Use

- User says "start a new project" or "I'm working on [thing]"
- A task emerges that will take multiple sessions
- User wants to formalize something they've been working on informally

## Workflow

### Step 1: Gather Information

Ask the user (skip what's obvious):
- **Project name**: What should we call this?
- **Goal**: What does "done" look like?
- **Timeline**: Any deadlines?
- **Key people**: Anyone else involved?

### Step 2: Create Project Note

Create from template:

```bash
cp vault/Projects/Active/_template.md "vault/Projects/Active/[Project-Name].md"
```

Fill in the template:

```markdown
---
status: active
created: [today's date]
updated: [today's date]
---

# [Project Name]

## Overview

[1-2 sentences about what this project is and why it matters]

## Goals

- [ ] [Goal 1 — specific and measurable]
- [ ] [Goal 2]

## Key People

- **[Name]** — [Role in this project]

## Next Actions

- [ ] [First concrete step]
- [ ] [Second step]

## Timeline

| Milestone | Target Date | Status |
|-----------|------------|--------|
| [Milestone] | [Date] | pending |

## Notes

### [Today's date]
- Project created
- [Any initial context]
```

### Step 3: Update Context

Add the project to `workspace/CONTEXT.md`:
- Add to "Active Projects" section
- Add any deadlines to the "Upcoming Deadlines" table
- Add any key people to the "Key People" section

### Step 4: Optional — Create People Notes

If the project involves people not yet in `vault/People/`:
- Create `vault/People/[Name].md` with basic info
- Link to the project note

### Step 5: Optional — Draft Kickoff Email

If the user wants to notify collaborators:
- Draft an email via gogcli summarizing the project
- Include goals, timeline, and first steps
- Create as draft only — never send

### Step 6: Confirm

```
Project "[Name]" is set up:

- Project note: vault/Projects/Active/[Name].md
- Added to CONTEXT.md active projects
- [People notes created / email drafted / etc.]

First action: [What to do next]
```

## Closing a Project

When a project is complete:

1. Update the project note: set `status: completed`, check off goals
2. Move to archive: `vault/Projects/Active/[Name].md` → `vault/Projects/Archive/[Name].md`
3. Update `workspace/CONTEXT.md`: remove from active projects
4. Optional: create a brief retrospective note

## Pausing a Project

When a project needs to be shelved temporarily:

1. Update the project note: set `status: paused`, note why
2. Add a "Resume" section with what to do when restarting
3. Keep in `vault/Projects/Active/` (don't archive yet)
4. Update `workspace/CONTEXT.md`: mark as paused
