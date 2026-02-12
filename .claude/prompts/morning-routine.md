---
name: morning-routine
description: "Daily startup routine — process inbox, check calendar, review email, set priorities. Run at the start of each day or work session."
variables:
  - name: focus_area
    required: false
    description: "Optional area to prioritize today (e.g., 'project X', 'email catchup')"
---

# Morning Routine

## Step 1: Check for Continuations

Look in `vault/Daily/` for any CONTINUATION notes from previous sessions.
If found, summarize what was in progress.

## Step 2: Process Inbox

Read `vault/Daily/inbox.md`. For each item:
- If actionable → move to a project note or today.md
- If reference → file in `vault/Reference/`
- If done → remove from inbox

## Step 3: Check Calendar

```bash
gogcli calendar list --days 1
```

Report today's schedule. Flag any meetings that need prep.

## Step 4: Check Email

```bash
gogcli gmail search "is:unread" --max 10
```

Summarize unread emails. Flag anything urgent or requiring action.

## Step 5: Set Today's Priorities

{{#if focus_area}}
Focus area for today: {{focus_area}}
Pull relevant context from projects and reference notes.
{{/if}}

Update `vault/Daily/today.md` with:
- Top 3 priorities for today
- Any meetings or deadlines
- Carry-forward items from yesterday

## Step 6: Report

```
Good morning! Here's your daily briefing:

Calendar: [N] events today
  - [Key events]

Email: [N] unread
  - [Urgent items]

Priorities:
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

[Continuations to resume, if any]

What would you like to tackle first?
```
