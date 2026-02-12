---
name: content-ingest
description: "Ingest content from URLs, files, or clipboard into structured vault notes. Extracts key information, summarizes, and creates properly formatted notes. Use when the user shares a link, document, or wants content digested into the vault."
requires:
  bins: []
  env: []
  tools: []
---

# Content Ingestion

## When to Use

- User shares a URL and wants it captured
- User has a PDF, article, or document to digest
- User pastes content and wants it organized
- User says "save this", "digest this", or "add this to the vault"

## Supported Content Types

| Type | Method | Notes |
|------|--------|-------|
| Web article | WebFetch tool | Extract main content, skip nav/ads |
| YouTube video | WebFetch on transcript | Look for transcript/captions |
| PDF document | Read tool | Extract text content |
| Audio file | `audio-transcribe.py` | Requires GEMINI_API_KEY |
| Pasted text | Direct processing | User pastes into chat |

## Workflow

### Step 1: Identify Content Type

Determine what the user is sharing:
- URL? → Fetch and process
- File path? → Read and process
- Pasted text? → Process directly
- Audio file? → Transcribe first, then process

### Step 2: Extract Content

**For URLs**: Use WebFetch to get the page content. Extract:
- Title
- Author (if available)
- Date (if available)
- Main body text (skip navigation, ads, footers)

**For files**: Read the file content directly.

**For audio**: Run transcription first:
```bash
python3 tools/audio-transcribe.py [file] --output /tmp/transcript.txt
```

### Step 3: Summarize and Structure

Create a vault note with this structure:

```markdown
---
source: [URL or file path]
type: [article / video / document / audio / note]
author: [if known]
date_ingested: [today's date]
tags: [relevant tags]
---

# [Title]

## Summary
[3-5 bullet points capturing the key information]

## Key Points
- [Important point 1]
- [Important point 2]
- [Important point 3]

## Details
[Longer content, organized by topic or chronologically]

## Action Items
- [ ] [Any actions suggested by the content]

## Source
[Original URL or file reference]
```

### Step 4: File the Note

Determine where the note belongs:
- **Reference topic?** → `vault/Reference/[Topic-Name].md`
- **Related to a project?** → Link in the relevant project note
- **Just capture for now?** → `vault/Daily/inbox.md`

Ask the user if the filing location isn't obvious.

### Step 5: Link

If the content relates to existing notes:
- Add a `[[link]]` in the relevant project or area note
- Mention the connection to the user

## Quality Checks

- [ ] Title is clear and descriptive
- [ ] Summary captures the essential information (someone could skip Details)
- [ ] Source is properly attributed
- [ ] Note is filed in the right location
- [ ] Any action items are captured

## What NOT to Do

- Don't copy entire articles verbatim (summarize and extract key points)
- Don't ingest content without telling the user where it was filed
- Don't skip the summary — the summary is the most valuable part
- Don't ingest paywalled content that can't be accessed
