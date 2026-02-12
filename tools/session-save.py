#!/usr/bin/env python3
"""
Session Save — Create a CONTINUATION note for the next session.

Captures session context, progress, and next steps so the next session
can pick up where this one left off.

Usage:
    session-save.py --topic "Project Name"                    # Create continuation
    session-save.py --topic "Project Name" --status blocked   # Mark as blocked
    session-save.py --list                                    # List existing continuations
    session-save.py --complete "Topic-Name"                   # Mark as completed
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path


def find_repo_root() -> Path:
    """Walk up from script location to find repo root."""
    current = Path(__file__).resolve().parent.parent
    if (current / 'CLAUDE.md').exists():
        return current
    cwd = Path.cwd()
    if (cwd / 'CLAUDE.md').exists():
        return cwd
    return current


def create_continuation(daily_path: Path, topic: str, status: str,
                        context: str = '', progress: str = '',
                        next_steps: str = '', files: str = '',
                        decisions: str = '', blockers: str = '') -> Path:
    """Create a CONTINUATION note."""
    # Sanitize topic for filename
    safe_topic = topic.replace(' ', '-').replace('/', '-')
    filename = f"CONTINUATION-{safe_topic}.md"
    filepath = daily_path / filename

    now = datetime.now().isoformat(timespec='minutes')

    content = f"""---
created: {now}
status: {status}
topic: {topic}
---

# CONTINUATION — {topic}

## Context
{context if context else '[Describe what was being worked on and why]'}

## Progress
{progress if progress else '- [ ] [List completed and remaining items]'}

## Next Steps
{next_steps if next_steps else '1. [Most important next action]'}

## Files Touched
{files if files else '- [List files that were created or modified]'}

## Key Decisions Made
{decisions if decisions else '- [Record any decisions and their rationale]'}

## Blockers or Open Questions
{blockers if blockers else '- [Note any unresolved issues]'}
"""

    filepath.write_text(content.strip() + '\n')
    return filepath


def list_continuations(daily_path: Path) -> None:
    """List all CONTINUATION notes."""
    notes = sorted(daily_path.glob('CONTINUATION-*.md'))

    if not notes:
        print("No CONTINUATION notes found.")
        return

    print(f"CONTINUATION notes ({len(notes)}):\n")

    for note in notes:
        content = note.read_text(encoding='utf-8', errors='ignore')
        status = 'unknown'
        topic = note.stem.replace('CONTINUATION-', '')

        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                for line in content[3:end].split('\n'):
                    if line.startswith('status:'):
                        status = line.split(':', 1)[1].strip()
                    elif line.startswith('topic:'):
                        topic = line.split(':', 1)[1].strip()

        status_icon = {'in-progress': '...', 'completed': 'OK', 'blocked': '!!'}
        icon = status_icon.get(status, '??')
        print(f"  [{icon}] {topic}")
        print(f"       Status: {status}")
        print(f"       File: {note.name}")
        print()


def complete_continuation(daily_path: Path, topic: str) -> bool:
    """Mark a CONTINUATION note as completed."""
    safe_topic = topic.replace(' ', '-').replace('/', '-')
    filepath = daily_path / f"CONTINUATION-{safe_topic}.md"

    if not filepath.exists():
        # Try case-insensitive match
        for f in daily_path.glob('CONTINUATION-*.md'):
            if safe_topic.lower() in f.stem.lower():
                filepath = f
                break

    if not filepath.exists():
        print(f"Error: No CONTINUATION note found matching '{topic}'")
        return False

    content = filepath.read_text()
    content = content.replace('status: in-progress', 'status: completed')
    content = content.replace('status: blocked', 'status: completed')
    filepath.write_text(content)

    print(f"Marked as completed: {filepath.name}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Create or manage session CONTINUATION notes'
    )
    parser.add_argument('--topic', '-t',
                        help='Topic name for the CONTINUATION note')
    parser.add_argument('--status', '-s', default='in-progress',
                        choices=['in-progress', 'blocked', 'completed'],
                        help='Status of the work (default: in-progress)')
    parser.add_argument('--list', '-l', action='store_true',
                        help='List existing CONTINUATION notes')
    parser.add_argument('--complete', '-c',
                        help='Mark a CONTINUATION note as completed')
    parser.add_argument('--context', help='Context description')
    parser.add_argument('--next', help='Next steps description')

    args = parser.parse_args()
    root = find_repo_root()
    daily_path = root / 'vault' / 'Daily'
    daily_path.mkdir(parents=True, exist_ok=True)

    if args.list:
        list_continuations(daily_path)
        sys.exit(0)

    if args.complete:
        success = complete_continuation(daily_path, args.complete)
        sys.exit(0 if success else 1)

    if not args.topic:
        parser.error("--topic is required when creating a CONTINUATION note")

    filepath = create_continuation(
        daily_path, args.topic, args.status,
        context=args.context or '',
        next_steps=args.next or '',
    )

    print(f"CONTINUATION note created: {filepath}")
    print(f"Status: {args.status}")
    print(f"\nEdit the note to add details about progress, files, and decisions.")


if __name__ == '__main__':
    main()
