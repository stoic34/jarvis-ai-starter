---
name: project-kickoff
description: "Set up a new project with note, context update, and kickoff checklist. Use when starting any initiative that will take more than one session."
variables:
  - name: project_name
    required: true
    description: "Name of the project"
  - name: goal
    required: true
    description: "What 'done' looks like for this project"
  - name: deadline
    required: false
    description: "Target completion date, if any"
  - name: collaborators
    required: false
    description: "People involved in the project"
---

# Project Kickoff: {{project_name}}

## Step 1: Create Project Note

Create `vault/Projects/Active/{{project_name}}.md` from the template.

Fill in:
- **Overview**: Based on the goal: {{goal}}
- **Goals**: Break the goal into 3-5 measurable milestones
{{#if deadline}}
- **Timeline**: Target completion by {{deadline}}
{{/if}}
{{#if collaborators}}
- **Key People**: {{collaborators}}
{{/if}}
- **Next Actions**: First 3 concrete steps

## Step 2: Update Context

Add to `workspace/CONTEXT.md`:
- Add to "Active Projects" list
{{#if deadline}}
- Add {{deadline}} to "Upcoming Deadlines"
{{/if}}
{{#if collaborators}}
- Add collaborators to "Key People" if not already listed
{{/if}}

## Step 3: First Actions

Identify and list the first 3 things that need to happen.
The first action should be something completable today.

## Step 4: Confirm

Report what was set up and what the first action is.
