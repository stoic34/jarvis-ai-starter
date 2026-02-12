---
name: eval-harness
description: "Self-verification system for multi-step tasks. Prevents lazy completion by requiring verification of each step before claiming success. Use when tasks have 3+ steps, are important, or are unfamiliar."
requires:
  bins: []
  env: []
  tools: []
---

# Eval Harness

## Mental Model: Horses, Not Cars

AI agents are probabilistic, not deterministic. Like a horse, not a car:
- A car turns left when you steer left — every time
- A horse usually goes where you point it — but sometimes it doesn't

The eval harness is your reins and spurs. It keeps the horse on track.

See `references/horses-not-cars.md` for the full mental model.

## When to Use

**Always use for:**
- Multi-step tasks (3+ steps)
- Tasks where getting it wrong has real consequences
- Task types you haven't done before
- Any task the user invokes with "verify each step" or "with an eval harness"

**Skip for:**
- Single-step tasks
- Pure information lookup
- Casual conversation

## Trigger Phrases

Auto-invoke when the user says:
- "with an eval harness"
- "verify each step"
- "create a checklist and mark each item"
- "test yourself before claiming success"
- "make sure each step actually worked"

## Workflow

### Step 1: Decompose

Break the task into discrete, verifiable steps. Each step must have:
- A clear action
- A concrete verification method
- A pass/fail criteria

```
**Eval Harness — [Task Name]**

| # | Step | Verification | Status |
|---|------|-------------|--------|
| 1 | [Action] | [How to verify] | pending |
| 2 | [Action] | [How to verify] | pending |
| 3 | [Action] | [How to verify] | pending |
```

### Step 2: Execute and Verify

For each step:
1. Execute the action
2. Immediately verify it worked (don't batch verifications)
3. Record the result

```
**Step 1: [Description]**
Action: [What was done]
Verification: [How it was checked]
Result: PASS / FAIL
```

**If a step fails:**
- Stop and diagnose
- Fix the issue
- Re-verify
- Only proceed when the step passes

### Step 3: Final Report

After all steps:

```
**Eval Harness — Final Report**

| # | Step | Result |
|---|------|--------|
| 1 | [Description] | PASS |
| 2 | [Description] | PASS |
| 3 | [Description] | PASS |

**Overall: PASS — All [N] steps verified**
```

Or if something failed:

```
**Overall: FAIL — Step [N] could not be verified**
**Reason**: [What went wrong]
**Recommendation**: [What to do next]
```

## Anti-Patterns to Catch

### Lazy Completion
The agent claims "Done!" without verifying. **Never do this.**

Signs of lazy completion:
- "I've updated the file" — but didn't read it back to verify
- "Email drafted" — but didn't confirm the draft exists
- "Tests pass" — but didn't actually run them

### Batch Verification
Doing all steps, then checking at the end. **Verify after each step.**

If step 2 depends on step 1 succeeding, and step 1 silently failed, step 2 will also fail — and you won't know why.

### Optimistic Reporting
Marking a step as PASS when verification was ambiguous. **If you're not sure, it's a FAIL.**

## Example

Task: "Set up a new project with email notifications"

```
**Eval Harness — Project Setup with Notifications**

| # | Step | Verification | Status |
|---|------|-------------|--------|
| 1 | Create project note | File exists and has correct template | pending |
| 2 | Add to CONTEXT.md | Entry visible in active projects | pending |
| 3 | Draft notification email | Draft appears in Gmail drafts | pending |

**Step 1: Create project note**
Action: Created vault/Projects/Active/New-Project.md from template
Verification: Read file back — confirmed template structure present
Result: PASS

**Step 2: Add to CONTEXT.md**
Action: Added "New Project — Just created" to active projects
Verification: Read CONTEXT.md — entry confirmed on line 18
Result: PASS

**Step 3: Draft notification email**
Action: Created draft via gogcli gmail drafts create
Verification: Ran gogcli gmail search "in:drafts subject:New Project" — 1 result
Result: PASS

**Overall: PASS — All 3 steps verified**
```
