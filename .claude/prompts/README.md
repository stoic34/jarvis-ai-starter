# Prompt Templates

Reusable prompt templates for common workflows. These are machine-readable prompts with variable substitution.

## How to Use

### As a User
Just describe what you want in natural language. Your AI will recognize when a template applies.

You can also reference templates directly:
- "Run the morning routine"
- "Do a project kickoff for [project name]"
- "Create a research brief on [topic]"

### As a Template Author

Templates use YAML frontmatter for metadata and `{{variable}}` syntax for placeholders:

```yaml
---
name: template-name
description: "When to use this template"
variables:
  - name: variable_name
    required: true
    description: "What this variable represents"
  - name: optional_var
    required: false
    description: "Optional context"
---

# Template Content

Do step 1 with {{variable_name}}.

{{#if optional_var}}
Also consider: {{optional_var}}
{{/if}}
```

## Available Templates

| Template | Purpose | Key Variables |
|----------|---------|--------------|
| `morning-routine` | Start the day: inbox, calendar, priorities | `focus_area` (optional) |
| `project-kickoff` | Set up a new project | `project_name`, `goal` |
| `research-brief` | Structured research on a topic | `topic`, `depth` |
| `weekly-review` | End-of-week review and planning | `week_number` (optional) |

## Adding Templates

1. Create a `.md` file in this directory
2. Add YAML frontmatter with `name`, `description`, `variables`
3. Write the template body with `{{variable}}` placeholders
4. Test by asking your AI to run it
