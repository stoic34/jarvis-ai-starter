---
name: session-handoff
description: "End-of-session context capture. Creates a CONTINUATION note so the next session can pick up where you left off. Use at the end of any multi-step or complex session, or when pausing work that will be resumed later."
requires:
  bins: ["git"]
  env: []
  tools: []
---

# Session Handoff

## When to Use

- End of any session with incomplete work
- When you're pausing a complex task
- Before switching to a different project
- When the user says "save progress", "let's stop here", or "pick this up later"
- Proactively when you detect a long session is ending

## When NOT to Use

- Short sessions with fully completed tasks
- Pure Q&A sessions with nothing to resume
- Tasks that don't have "next steps"

## Workflow

### Step 1: Assess What Happened

Review the session to identify:
- What was the goal?
- What was completed?
- What's still outstanding?
- What decisions were made?
- What files were created or modified?

### Step 2: Create CONTINUATION Note

Create a note in `vault/Daily/` with the naming pattern:

```
vault/Daily/CONTINUATION-[Topic-Name].md
```

Use this template:

```markdown
---
created: [ISO date]
status: in-progress
topic: [Brief-Topic-Name]
---

# CONTINUATION — [Topic Name]

## Context
[2-3 sentences explaining what we were working on and why]

## Progress
- [x] [Completed item 1]
- [x] [Completed item 2]
- [ ] [Outstanding item 1]
- [ ] [Outstanding item 2]

## Next Steps
1. [Most important next action — be specific]
2. [Second action]
3. [Third action if applicable]

## Files Touched
- `path/to/file` — [what was done to it]
- `path/to/file` — [what was done to it]

## Key Decisions Made
- **[Decision]**: [Rationale — why this choice was made]

## Blockers or Open Questions
- [Any unresolved issues the next session needs to address]
```

### Step 3: Update Context

Update `workspace/CONTEXT.md` if priorities changed during the session:
- Add new projects to the active list
- Update status of existing projects
- Note any new deadlines

### Step 4: Update Today

Update `vault/Daily/today.md` with a brief session summary:

```markdown
### [Time] — [Topic]
- [Key outcome 1]
- [Key outcome 2]
- Status: [in-progress / completed / blocked]
- CONTINUATION: [[CONTINUATION-Topic-Name]] (if applicable)
```

### Step 5: Git Status Check

Check for uncommitted changes:
```bash
git status
```

If there are changes that should be committed:
- Stage relevant files
- Commit with a descriptive message
- Note the commit in the CONTINUATION file

If there are changes that should NOT be committed yet:
- Note this in the CONTINUATION file's "Next Steps"

### Step 6: Confirm with User

```
Session handoff complete:

- CONTINUATION note: vault/Daily/CONTINUATION-[Topic].md
- [N] files touched, [committed/uncommitted]
- Next session should start with: "[specific instruction]"

Anything else before we wrap up?
```

## Session Resume (Start of Next Session)

At the beginning of a new session:

1. Check `vault/Daily/` for CONTINUATION files
2. If found, read the most recent one
3. Summarize to the user: "I found a CONTINUATION note from [date] about [topic]. Here's where we left off: [summary]. Want to continue?"
4. If resuming, follow the "Next Steps" from the CONTINUATION note
5. When the continued work is complete, update the CONTINUATION note status to `completed`

## Cleanup

CONTINUATION notes with `status: completed` can be:
- Left in place as history
- Moved to `vault/Archive/` during periodic cleanup
- Deleted if not needed (ask user first)

Stale CONTINUATION notes (> 7 days, still `in-progress`) should be flagged:
- "Found a stale CONTINUATION from [date] about [topic]. Is this still active, or should we archive it?"
