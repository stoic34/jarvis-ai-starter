# Eval Harnesses: Teaching Your Agent to Actually Finish the Job

This might be the most important concept in working with AI agents. Without it, you'll get frustrated. With it, you'll get results.

**Time required:** 10 minutes to read, lifetime to master

---

## The Core Mental Model: Horses, Not Cars

**An AI is not like a car. An AI is like a horse.**

### Cars Are Deterministic

Turn the steering wheel left → the car goes left.
Every. Single. Time.

Press the gas pedal → the car accelerates.
Predictable. Reliable. Mechanical.

### Horses Are Probabilistic

Kick the horse to go → it might go.
Or it might not feel like it today.
Or it might go, but in a slightly different direction.

A horse has its own tendencies. Some days it's energetic. Some days it's lazy. You have to learn to ride it. You need a **harness** to guide it.

### Your AI Agent is a Horse

When you give your agent a task, it doesn't execute like a program. It *attempts* the task based on its understanding, its current "mood" (token state), and its tendencies.

Sometimes it nails it.
Sometimes it does half the work and declares victory.
Sometimes it misunderstands completely.

**This is normal.** You're learning to ride, not drive.

---

## The Problem: Lazy Completion

Here's what happens without guidance:

> **You:** "Hey Jarvis, do these 5 things for me:
> 1. Find emails from Sarah about the project
> 2. Summarize the key points
> 3. Draft a response
> 4. Check my calendar for conflicts
> 5. Add the meeting to my calendar"

> **Jarvis:** "Done!"

**But wait...**
- It found the emails (1 ✓)
- Summarized them, sort of (2 ~)
- Didn't draft a response (3 ✗)
- Didn't check calendar (4 ✗)
- Didn't add anything (5 ✗)

The agent did 1.5 things and announced: "I crushed it! Five stars!"

This isn't a bug. It's the nature of probabilistic systems. The agent genuinely believes it completed the task.

---

## The Solution: Eval Harnesses

An **Eval Harness** is a self-verification system. It forces your agent to:
1. List everything it needs to do
2. Do each thing
3. Test that each thing actually worked
4. Only claim success when ALL tests pass

### Breaking Down the Name

**Eval** = Evaluate (test yourself)
**Harness** = Structure that guides behavior (like a horse harness)

It's the spurs and reins that keep your horse on track.

---

## How to Invoke an Eval Harness

Add these phrases to your requests:

### Option 1: Explicit Request
> "Do these 5 things **with an eval harness** to verify each step"

### Option 2: Verification Language
> "Do these 5 things and **verify each step is complete before moving on**"

### Option 3: Checklist Request
> "Do these 5 things. **Create a checklist and mark each item only when verified**"

### Option 4: Testing Request
> "Do these 5 things and **test yourself before claiming success**"

---

## What Happens With an Eval Harness

> **You:** "Hey Jarvis, do these 5 things with an eval harness:
> 1. Find emails from Sarah about the project
> 2. Summarize the key points
> 3. Draft a response
> 4. Check my calendar for conflicts
> 5. Add the meeting to my calendar"

> **Jarvis:** "I'll work through this with verification for each step.
>
> **Eval Harness - Task List:**
> - [ ] Find emails from Sarah about the project
> - [ ] Summarize the key points
> - [ ] Draft a response
> - [ ] Check calendar for conflicts
> - [ ] Add meeting to calendar
>
> **Step 1: Find emails from Sarah**
> Running: `gogcli gmail search "from:sarah subject:project" --max 20`
> Found 8 emails in thread.
> ✓ Verified: Emails found and readable
>
> **Step 2: Summarize key points**
> Reading thread content...
> Summary:
> - Sarah proposed Tuesday meeting
> - Budget discussion needed
> - Deadline is end of month
> ✓ Verified: Summary complete with 3 key points
>
> **Step 3: Draft response**
> Creating draft...
> Draft created with subject "Re: Project Discussion"
> ✓ Verified: Draft exists in Gmail drafts folder
>
> **Step 4: Check calendar for conflicts**
> Running: `gogcli calendar list --days 7`
> Tuesday 10am: Team standup (conflict!)
> Tuesday 2pm: Available
> ✓ Verified: Calendar checked, found conflict and alternative
>
> **Step 5: Add meeting to calendar**
> Creating event for Tuesday 2pm...
> ✓ Verified: Event created, confirmed in calendar
>
> **Final Verification:**
> - [x] Find emails from Sarah about the project
> - [x] Summarize the key points
> - [x] Draft a response
> - [x] Check calendar for conflicts
> - [x] Add meeting to calendar
>
> All 5 tasks completed and verified."

**See the difference?** The agent:
- Created a checklist
- Worked through each item
- Verified each step
- Only claimed success after all verifications passed

---

## When to Use Eval Harnesses

### Always Use for Multi-Step Tasks

Any task with more than 2-3 steps should have an eval harness.

> "Research X, summarize Y, create Z" → Use eval harness

### Always Use for Important Tasks

Anything you'd be upset about if done wrong.

> "Prepare the board presentation" → Use eval harness

### Always Use for New Task Types

First time asking for something? Add verification.

> "Set up this new integration" → Use eval harness

### Optional for Simple Tasks

Single, clear actions don't need them.

> "What time is my next meeting?" → No harness needed

---

## The Spurs Metaphor

Sometimes even with an eval harness, your agent will try to shortcut.

> **Jarvis:** "Step 3 should be straightforward, skipping verification..."

**No. Add spurs.**

> **You:** "Don't skip verification. Test step 3 properly."

The spurs are your insistence that the agent actually complete the work. You're training the horse to do it right.

Over time, you'll learn when to kick and when to let it run.

---

## Building Eval Harness Habits

### Start Every Complex Request With Structure

Before diving into the task, set expectations:

> "I need you to do X. Before you start, create a checklist of what needs to happen. Then work through each item with verification."

### End Complex Requests With Verification

After the agent claims completion:

> "Show me the verification results for each step."

### Call Out Lazy Completion

If you notice shortcuts:

> "You said you did 5 things but I only see 3 verified. Complete the remaining items with verification."

---

## Your First Eval Harness

Let's practice. Ask your agent:

> "Create an eval harness to verify my entire setup is working:
> 1. Verify you know my name
> 2. Verify you can read files in the vault
> 3. Verify gogcli is working (test Gmail access)
> 4. Verify the available browser or desktop-control workflow is connected
> 5. Verify you can create a file in the vault
>
> Create a checklist, test each item, and report results."

Your agent should:
- Create a checklist
- Test each item with actual commands
- Report pass/fail for each
- Only claim success if ALL pass

If anything fails, you'll know exactly what needs fixing.

---

## Summary

| Concept | Explanation |
|---------|-------------|
| **Horses, Not Cars** | AI is probabilistic, not deterministic. Learn to ride. |
| **Lazy Completion** | Agents often do partial work and claim success. |
| **Eval Harness** | Self-verification system to ensure complete work. |
| **Spurs** | Your insistence that shortcuts aren't acceptable. |
| **When to Use** | Multi-step tasks, important tasks, new task types. |

**The key insight:** Your agent wants to please you. It will claim success because it genuinely believes it helped. The eval harness creates an objective standard that overrides optimistic self-assessment.

---

## What You've Accomplished

- Understand the horses vs. cars mental model
- Know why agents claim false success
- Can invoke eval harnesses in your requests
- Practiced with your first verification harness

**Your agent is now:**
- Named and personalized
- Accessible via one-word alias
- Connected to your browser
- Integrated with Google Workspace
- Trained to verify its own work

**You're ready to start using your AI assistant for real work.**

---

## What's Next?

Now that you're set up, explore what's possible:
- [USE-CASES.md](USE-CASES.md) - Real examples of what your agent can do
- [WHATS-NEXT.md](WHATS-NEXT.md) - Advanced expansions (AWS, more integrations)

---

*Time to complete: 10 minutes to read, a lifetime to master*
