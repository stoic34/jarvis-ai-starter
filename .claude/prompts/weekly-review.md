---
name: weekly-review
description: "End-of-week review: what happened, what's next, what to clean up. Use Friday afternoon or Sunday evening to reset for the coming week."
variables:
  - name: week_number
    required: false
    description: "Week number or date range for the review"
---

# Weekly Review

## Step 1: Review the Week

Check what happened this week:

### Projects
Read `workspace/CONTEXT.md` and review each active project:
- What progress was made?
- What's still pending?
- Any blockers?

### Calendar
```bash
gogcli calendar list --days 7
```
Review past 7 days of events.

### Email
Review any email threads that need follow-up.

### Journal
Check `vault/Daily/journal/` for this week's entries.

## Step 2: Clean Up

### Inbox Zero
Process everything in `vault/Daily/inbox.md`:
- Actionable items → project notes or next week's priorities
- Reference items → `vault/Reference/`
- Completed items → remove

### Stale Continuations
Check for CONTINUATION notes older than 7 days:
- Still relevant? → Update status
- No longer needed? → Archive or delete (with permission)

### Project Health
For each active project:
- Is the status accurate?
- Are next actions current?
- Should any project be paused or archived?

## Step 3: Plan Next Week

Update `workspace/CONTEXT.md` with:
- Top 3 priorities for next week
- Any deadlines approaching
- Meetings that need prep

Update `vault/Daily/today.md` (or create Monday's) with:
- First priority for Monday morning
- Any prep needed before Monday

## Step 4: Report

```
Weekly Review{{#if week_number}} — Week {{week_number}}{{/if}}

Completed:
- [Key accomplishment 1]
- [Key accomplishment 2]

In Progress:
- [Project] — [status]
- [Project] — [status]

Next Week's Priorities:
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

Housekeeping:
- [N] inbox items processed
- [N] CONTINUATION notes reviewed
- [N] projects updated

Anything you want to adjust for next week?
```
