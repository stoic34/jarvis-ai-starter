#!/usr/bin/env python3
"""
PII Scanner
Scans files for potentially sensitive personal information.

Use this before publishing or sharing the repo to ensure no private data leaks.

Usage:
    pii-scanner.py                    # Scan entire repo
    pii-scanner.py --path ./docs      # Scan specific directory
    pii-scanner.py --file README.md   # Scan specific file
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple


# Patterns to detect
PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone_us': r'\b(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
    'phone_intl': r'\b\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b',
    'ssn': r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b',
    'credit_card': r'\b(?:\d{4}[-.\s]?){3}\d{4}\b',
    'api_key': r'\b(?:sk[-_]|api[-_]?key|token)[A-Za-z0-9_-]{20,}\b',
    'aws_key': r'\bAKIA[A-Z0-9]{16}\b',
    'private_key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    'mac_address': r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b',
}

# File extensions to scan
SCANNABLE_EXTENSIONS = {
    '.md', '.txt', '.json', '.yaml', '.yml', '.toml',
    '.py', '.js', '.ts', '.sh', '.bash', '.zsh',
    '.html', '.css', '.env', '.conf', '.cfg'
}

# Files/directories to skip
SKIP_PATTERNS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    '.DS_Store', '*.pyc', '*.pyo'
}


def should_scan(path: Path) -> bool:
    """Determine if a file should be scanned."""
    # Skip directories in skip list
    for part in path.parts:
        if part in SKIP_PATTERNS:
            return False

    # Only scan certain extensions
    if path.suffix.lower() not in SCANNABLE_EXTENSIONS:
        return False

    return True


def scan_content(content: str, filename: str) -> List[Tuple[str, str, int, str]]:
    """Scan content for PII patterns."""
    findings = []

    for line_num, line in enumerate(content.split('\n'), 1):
        for pattern_name, pattern in PATTERNS.items():
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                # Mask the finding for display
                value = match.group()
                masked = mask_value(value, pattern_name)
                findings.append((filename, pattern_name, line_num, masked))

    return findings


def mask_value(value: str, pattern_type: str) -> str:
    """Mask sensitive values for safe display."""
    if len(value) <= 4:
        return '*' * len(value)

    if pattern_type in ('email',):
        # Show first 2 chars and domain
        at_pos = value.find('@')
        if at_pos > 2:
            return value[:2] + '***' + value[at_pos:]
        return '***' + value[at_pos:]

    if pattern_type in ('phone_us', 'phone_intl'):
        return value[:3] + '***' + value[-2:]

    if pattern_type in ('api_key', 'aws_key'):
        return value[:6] + '***'

    # Default: show first and last 2 chars
    return value[:2] + '***' + value[-2:]


def scan_file(filepath: Path) -> List[Tuple[str, str, int, str]]:
    """Scan a single file."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        return scan_content(content, str(filepath))
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return []


def scan_directory(dirpath: Path) -> List[Tuple[str, str, int, str]]:
    """Scan all files in a directory recursively."""
    all_findings = []

    for filepath in dirpath.rglob('*'):
        if filepath.is_file() and should_scan(filepath):
            findings = scan_file(filepath)
            all_findings.extend(findings)

    return all_findings


def main():
    parser = argparse.ArgumentParser(
        description='Scan files for sensitive personal information',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
What it detects:
  - Email addresses
  - Phone numbers (US and international)
  - Social Security Numbers
  - Credit card numbers
  - API keys and tokens
  - AWS access keys
  - Private keys
  - IP addresses
  - MAC addresses

Examples:
  Scan entire repo:
    pii-scanner.py

  Scan specific directory:
    pii-scanner.py --path ./vault

  Scan specific file:
    pii-scanner.py --file CLAUDE.md
        """
    )

    parser.add_argument('--path', '-p', default='.',
                        help='Directory to scan (default: current directory)')
    parser.add_argument('--file', '-f',
                        help='Specific file to scan')

    args = parser.parse_args()

    print("PII Scanner - Checking for sensitive information...")
    print("-" * 60)

    if args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            sys.exit(1)
        findings = scan_file(filepath)
    else:
        dirpath = Path(args.path)
        if not dirpath.exists():
            print(f"Error: Directory not found: {dirpath}")
            sys.exit(1)
        findings = scan_directory(dirpath)

    if findings:
        print(f"\n⚠️  Found {len(findings)} potential PII item(s):\n")

        for filename, pattern_type, line_num, masked_value in findings:
            print(f"  {filename}:{line_num}")
            print(f"    Type: {pattern_type}")
            print(f"    Value: {masked_value}")
            print()

        print("-" * 60)
        print("Review these findings before publishing.")
        print("Some may be false positives (example data, documentation).")
        sys.exit(1)
    else:
        print("\n✓ No PII detected")
        print("\nNote: This scanner may not catch all sensitive data.")
        print("Always manually review before publishing.")


if __name__ == '__main__':
    main()
