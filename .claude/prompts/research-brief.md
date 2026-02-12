---
name: research-brief
description: "Structured research on a topic with sources, summary, and recommendations. Use when the user needs to understand a topic, compare options, or make an informed decision."
variables:
  - name: topic
    required: true
    description: "The topic or question to research"
  - name: depth
    required: false
    description: "How deep to go: 'quick' (5 min), 'standard' (15 min), or 'deep' (30+ min)"
  - name: decision
    required: false
    description: "If this research supports a decision, what is the decision?"
---

# Research Brief: {{topic}}

## Step 1: Define Scope

Topic: {{topic}}
{{#if depth}}Depth: {{depth}}{{/if}}
{{#if decision}}Decision to inform: {{decision}}{{/if}}

Identify 3-5 specific questions to answer.

## Step 2: Research

Use available tools:
- Web search for current information
- WebFetch for specific articles or documentation
- Vault search for existing notes on this topic

For each source, note:
- What it says
- How credible/recent it is
- How it relates to the user's question

## Step 3: Synthesize

Create a research note at `vault/Reference/Research-{{topic}}.md`:

```markdown
---
type: research
topic: {{topic}}
date: [today]
---

# Research: {{topic}}

## Summary
[3-5 bullet points with the key findings]

## Key Findings

### [Finding 1]
[Details with source attribution]

### [Finding 2]
[Details with source attribution]

### [Finding 3]
[Details with source attribution]

{{#if decision}}
## Recommendation
**Confidence**: [HIGH/MEDIUM/LOW]
**Recommendation**: [What to do]
**Basis**: [Why]
**Alternatives**: [Other options considered]
{{/if}}

## Sources
- [Source 1 — description]
- [Source 2 — description]

## Open Questions
- [What couldn't be answered]
```

## Step 4: Report

Present findings to the user with:
- A 2-3 sentence summary
- The key recommendation (if decision-oriented)
- Confidence level
- Where the full research note is filed
