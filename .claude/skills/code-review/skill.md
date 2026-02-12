---
name: code-review
description: "5-gate quality review for code changes. Enforces scope discipline, pattern consistency, security, and minimalism. Auto-invoked for Tier 2+ software development tasks. Use a separate context from the code writer."
requires:
  bins: ["git"]
  env: []
  tools: []
---

# Code Review — 5-Gate Quality Check

## Core Principle

**Writer ≠ Reviewer.** The context that wrote the code should NOT review it. Use the Task tool to spawn a separate reviewer agent, or review in a fresh session.

Why: The writing context has sunk-cost bias, remembers its intent (not what it wrote), and will rationalize its own mistakes.

## When to Use

| Tier | Auto-Invoke? | Review Type |
|------|-------------|-------------|
| 1: Trivial (< 5 min) | No | Quick security scan only |
| 2: Simple (5-30 min) | Yes | Gates 1, 3, 4 (scope, security, minimalism) |
| 3: Standard (30 min+) | Yes | All 5 gates |
| 4: Complex (multi-session) | Yes | All 5 gates + cross-model review if available |

## The Five Gates

### Gate 1: Scope Discipline

**Question**: Does the change match the spec exactly?

Check for:
- [ ] No unrelated changes (no "while I was here" cleanup)
- [ ] No feature creep beyond what was requested
- [ ] No removed code that wasn't asked to be removed
- [ ] No new dependencies that weren't specified
- [ ] Commit message accurately describes the change

**Verdict**: PASS / FAIL / N/A

---

### Gate 2: Pattern Consistency

**Question**: Does the change match the codebase's existing patterns?

Check for:
- [ ] Naming conventions match (camelCase vs. snake_case, etc.)
- [ ] File organization follows existing structure
- [ ] Error handling matches existing patterns
- [ ] Import/export style is consistent
- [ ] Comment style matches (if comments are used)

**Verdict**: PASS / FAIL / N/A

---

### Gate 3: Security Scan

**Question**: Are there any security vulnerabilities?

Check for:
- [ ] No command injection (unsanitized input in shell commands)
- [ ] No XSS (unsanitized input in HTML output)
- [ ] No SQL injection (string concatenation in queries)
- [ ] No exposed secrets (API keys, tokens, passwords in code)
- [ ] No path traversal (unsanitized file paths)
- [ ] No insecure dependencies (known vulnerable versions)
- [ ] Input validation at system boundaries

**Verdict**: PASS / FAIL

*Security gate cannot be N/A — always evaluate.*

---

### Gate 4: Minimalism

**Question**: Is this the simplest correct solution?

Check for:
- [ ] No premature abstractions (helpers for one-time operations)
- [ ] No unnecessary configuration (feature flags for non-configurable things)
- [ ] No over-engineering (designing for hypothetical future requirements)
- [ ] No redundant validation (trusting internal code and framework guarantees)
- [ ] Three similar lines of code is better than a premature abstraction

**Verdict**: PASS / FAIL / N/A

---

### Gate 5: Verification

**Question**: Is the change verified to work?

Check for:
- [ ] Tests pass (if test suite exists)
- [ ] New tests added for new functionality (if test suite exists)
- [ ] Manual verification for changes without tests
- [ ] Edge cases considered
- [ ] No broken existing functionality

**Verdict**: PASS / FAIL / N/A

---

## Output Format

After reviewing all gates, produce a summary:

```markdown
## Code Review — [Brief Description]

| Gate | Verdict | Notes |
|------|---------|-------|
| 1. Scope | PASS | Changes match the spec |
| 2. Patterns | PASS | Follows existing conventions |
| 3. Security | PASS | No vulnerabilities found |
| 4. Minimalism | PASS | Clean, no over-engineering |
| 5. Verification | PASS | Tests pass |

**Overall: PASS** — Ready to commit/merge.
```

Or if something fails:

```markdown
**Overall: FAIL** — Gate 3 (Security) failed.

**Issues:**
1. Line 42: User input passed directly to shell command without sanitization
2. Line 89: API key hardcoded in source file

**Recommended fixes:**
1. Use subprocess with argument list instead of shell=True
2. Move API key to environment variable
```

## Review Checklist Shortcut

For quick reviews (Tier 2), use this abbreviated format:

```
Scope: PASS — matches spec
Security: PASS — no injection or exposed secrets
Minimalism: PASS — simple implementation
→ Ready to commit
```

## What This Skill Does NOT Do

- Does not review architecture decisions (that's planning, not review)
- Does not suggest refactoring beyond the current change
- Does not add comments, docstrings, or type annotations to unchanged code
- Does not enforce personal style preferences over codebase conventions
