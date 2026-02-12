#!/usr/bin/env python3
"""
Session Init — Load context at the start of each session.

Checks for CONTINUATION notes, loads current context, and reports
what the AI should know before starting work.

Usage:
    session-init.py                     # Full init
    session-init.py --continuations     # Only check for continuations
    session-init.py --quiet             # Minimal output
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path


def find_repo_root() -> Path:
    """Walk up from script location to find repo root (contains CLAUDE.md)."""
    current = Path(__file__).resolve().parent.parent
    if (current / 'CLAUDE.md').exists():
        return current
    # Fallback to cwd
    cwd = Path.cwd()
    if (cwd / 'CLAUDE.md').exists():
        return cwd
    return current


def find_continuations(vault_path: Path) -> list:
    """Find CONTINUATION notes in the vault."""
    continuations = []
    daily_path = vault_path / 'Daily'

    if not daily_path.exists():
        return continuations

    for f in sorted(daily_path.glob('CONTINUATION-*.md')):
        content = f.read_text(encoding='utf-8', errors='ignore')

        # Parse frontmatter
        status = 'unknown'
        topic = f.stem.replace('CONTINUATION-', '')
        created = None

        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                frontmatter = content[3:end]
                for line in frontmatter.split('\n'):
                    if line.startswith('status:'):
                        status = line.split(':', 1)[1].strip()
                    elif line.startswith('topic:'):
                        topic = line.split(':', 1)[1].strip()
                    elif line.startswith('created:'):
                        created = line.split(':', 1)[1].strip()

        # Calculate age
        age_days = None
        if created:
            try:
                created_date = datetime.fromisoformat(created.split('T')[0])
                age_days = (datetime.now() - created_date).days
            except (ValueError, IndexError):
                pass

        continuations.append({
            'path': str(f),
            'name': f.name,
            'status': status,
            'topic': topic,
            'created': created,
            'age_days': age_days,
            'stale': age_days is not None and age_days > 7 and status == 'in-progress',
        })

    return continuations


def check_context(workspace_path: Path) -> dict:
    """Check workspace context files for completeness."""
    context = {}
    files = {
        'IDENTITY.md': 'identity',
        'USER.md': 'user',
        'TOOLS.md': 'tools',
        'CONTEXT.md': 'context',
    }

    for filename, key in files.items():
        filepath = workspace_path / filename
        if filepath.exists():
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            has_placeholders = '[' in content and ']' in content
            context[key] = {
                'exists': True,
                'configured': not has_placeholders or len(content) > 500,
                'path': str(filepath),
            }
        else:
            context[key] = {'exists': False, 'configured': False, 'path': str(filepath)}

    return context


def main():
    parser = argparse.ArgumentParser(
        description='Initialize session context for AI assistant'
    )
    parser.add_argument('--continuations', '-c', action='store_true',
                        help='Only check for CONTINUATION notes')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Minimal output')

    args = parser.parse_args()
    root = find_repo_root()
    vault_path = root / 'vault'
    workspace_path = root / 'workspace'

    if not args.quiet:
        print(f"Session Init — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("=" * 50)

    # Check continuations
    continuations = find_continuations(vault_path)
    active = [c for c in continuations if c['status'] == 'in-progress']
    stale = [c for c in continuations if c['stale']]

    if active:
        print(f"\nCONTINUATION notes found ({len(active)} active):")
        for c in active:
            age = f" ({c['age_days']}d ago)" if c['age_days'] is not None else ""
            stale_flag = " [STALE]" if c['stale'] else ""
            print(f"  - {c['topic']}{age}{stale_flag}")
            print(f"    {c['path']}")
    elif not args.quiet:
        print("\nNo active CONTINUATION notes.")

    if args.continuations:
        sys.exit(0)

    # Check workspace config
    if not args.quiet:
        context = check_context(workspace_path)
        unconfigured = [k for k, v in context.items() if not v['configured']]

        if unconfigured:
            print(f"\nWorkspace files needing setup: {', '.join(unconfigured)}")
            print("  Run onboarding: say 'Let's do the initial setup'")
        else:
            print("\nWorkspace: all files configured.")

    # Check today.md
    today_path = vault_path / 'Daily' / 'today.md'
    if today_path.exists():
        content = today_path.read_text(encoding='utf-8', errors='ignore')
        if content.strip():
            if not args.quiet:
                print(f"\nToday's focus loaded ({len(content.split(chr(10)))} lines)")
    elif not args.quiet:
        print("\nNo today.md found — consider setting today's priorities.")

    # Summary
    if not args.quiet:
        print("\n" + "=" * 50)
        if active:
            print(f"Resume work: Read the CONTINUATION note(s) above")
        if stale:
            print(f"Stale notes: {len(stale)} CONTINUATION(s) older than 7 days")
        print("Ready.")

    # Exit code: 0 if clean, 1 if stale continuations need attention
    sys.exit(1 if stale else 0)


if __name__ == '__main__':
    main()
