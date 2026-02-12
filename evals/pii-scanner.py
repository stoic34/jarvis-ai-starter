#!/usr/bin/env python3
"""
PII Scanner — Enhanced Security Scanner

Scans files for sensitive personal information, proprietary terms, and secrets.
Supports a local blocklist for custom terms that should never appear in commits.

Usage:
    pii-scanner.py                          # Scan entire repo
    pii-scanner.py --path ./docs            # Scan specific directory
    pii-scanner.py --file README.md         # Scan specific file
    pii-scanner.py --staged                 # Scan only git-staged files (for pre-commit)
    pii-scanner.py --blocklist path.txt     # Use custom blocklist file
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional


# ── Pattern Definitions ──────────────────────────────────────────────

PATTERNS = {
    # Personal identifiers
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone_us': r'\b(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
    'phone_intl': r'\b\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b',
    'ssn': r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b',
    'credit_card': r'\b(?:\d{4}[-.\s]?){3}\d{4}\b',

    # Secrets and credentials
    'api_key': r'\b(?:sk[-_]|api[-_]?key|token)[A-Za-z0-9_-]{20,}\b',
    'aws_access_key': r'\bAKIA[A-Z0-9]{16}\b',
    'aws_account_id': r'\b\d{12}\b',
    'private_key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'github_pat': r'\bghp_[A-Za-z0-9]{36}\b',
    'slack_token': r'\bxox[bpas]-[A-Za-z0-9-]+\b',

    # Infrastructure identifiers
    'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    'mac_address': r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b',
    'slack_channel_id': r'\b[CTUDW](?=[A-Z0-9]*\d)[A-Z0-9]{8,12}\b',
    'aws_arn': r'\barn:aws:[a-z0-9-]+:[a-z0-9-]*:\d{12}:[a-zA-Z0-9/._-]+\b',
}

# Patterns that are commonly false-positive — require extra context to flag
SOFT_PATTERNS = {'aws_account_id', 'ip_address', 'slack_channel_id'}

# Known safe values (example data in documentation)
ALLOWLIST = {
    'email': {
        'recipient@example.com', 'user@example.com', 'boss@example.com',
        'you@example.com', 'name@example.com', 'john.doe@example.com',
        'employee@company.com', 'sample@example.com', 'email@example.com',
        'sarah@example.com', 'your.email@example.com',
        'your-email@example.com', 'test@example.com',
    },
    'ip_address': {
        '127.0.0.1', '0.0.0.0', '255.255.255.255',
        '192.168.1.1', '10.0.0.1', '172.16.0.1',
        # RFC 5737 documentation ranges
        '192.0.2.1', '198.51.100.1', '203.0.113.1',
        # GitHub webhook source IP (used in examples)
        '140.82.115.1',
    },
    'aws_account_id': {
        '123456789012',  # AWS example account ID
    },
    'aws_arn': {
        # AWS documentation example ARNs (regex captures up to resource-type segment)
        'arn:aws:events:us-east-1:123456789012:rule/daily-backup-task',
        'arn:aws:events:us-east-1:123456789012:rule/daily-task',
        'arn:aws:events:us-east-1:123456789012:rule/daily-backup',
        'arn:aws:iam::123456789012:role/lambda-execution-role',
        'arn:aws:lambda:us-east-1:123456789012:function',
        'arn:aws:secretsmanager:us-east-1:123456789012:secret',
    },
    'credit_card': {
        # GitHub delivery UUIDs contain segments that match CC patterns
        '12345678-1234-1234',
        '1234-123456789012',
    },
    'slack_channel_id': set(),  # No safe defaults
}

# File extensions to scan
SCANNABLE_EXTENSIONS = {
    '.md', '.txt', '.json', '.yaml', '.yml', '.toml',
    '.py', '.js', '.ts', '.sh', '.bash', '.zsh',
    '.html', '.css', '.env', '.conf', '.cfg',
    '.jsx', '.tsx', '.mjs', '.cjs',
}

# Files/directories to skip
SKIP_PATTERNS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    '.DS_Store', '.security',
}

# Files that are expected to contain example PII (documentation)
DOCUMENTATION_FILES = {
    'pii-scanner.py',  # This file contains pattern examples
}


# ── Blocklist Loading ────────────────────────────────────────────────

def load_blocklist(blocklist_path: Optional[Path] = None) -> List[dict]:
    """Load custom blocklist terms from file."""
    if blocklist_path is None:
        # Default location: .security/blocklist.txt relative to repo root
        repo_root = find_repo_root()
        if repo_root:
            blocklist_path = repo_root / '.security' / 'blocklist.txt'
        else:
            return []

    if not blocklist_path.exists():
        return []

    terms = []
    for line in blocklist_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.startswith('regex:'):
            # Regex pattern
            pattern = line[6:].strip()
            try:
                re.compile(pattern)
                terms.append({'type': 'regex', 'value': pattern})
            except re.error as e:
                print(f"Warning: Invalid regex in blocklist: {pattern} ({e})",
                      file=sys.stderr)
        else:
            # Plain text (case-insensitive)
            terms.append({'type': 'text', 'value': line})

    return terms


def find_repo_root() -> Optional[Path]:
    """Find the git repository root."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True, text=True, check=True
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


# ── Scanning ─────────────────────────────────────────────────────────

def should_scan(path: Path) -> bool:
    """Determine if a file should be scanned."""
    for part in path.parts:
        if part in SKIP_PATTERNS:
            return False

    if path.suffix.lower() not in SCANNABLE_EXTENSIONS:
        return False

    return True


def is_in_allowlist(pattern_name: str, value: str) -> bool:
    """Check if a detected value is in the allowlist (known-safe)."""
    if pattern_name in ALLOWLIST:
        return value in ALLOWLIST[pattern_name]
    return False


def scan_content(content: str, filename: str,
                 blocklist: List[dict] = None,
                 strict: bool = False) -> List[Tuple[str, str, int, str]]:
    """Scan content for PII patterns and blocklist terms."""
    findings = []
    is_doc_file = Path(filename).name in DOCUMENTATION_FILES

    for line_num, line in enumerate(content.split('\n'), 1):
        # Skip comment-only lines in code files
        stripped = line.strip()
        if stripped.startswith('#') and filename.endswith('.py'):
            # Still check blocklist against comments
            pass

        # Check PII patterns
        for pattern_name, pattern in PATTERNS.items():
            # Skip soft patterns unless in strict mode
            if pattern_name in SOFT_PATTERNS and not strict:
                continue

            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                value = match.group()

                # Skip allowlisted values
                if is_in_allowlist(pattern_name, value):
                    continue

                # Skip documentation files for non-critical patterns
                if is_doc_file and pattern_name not in (
                    'private_key', 'aws_access_key', 'github_pat', 'slack_token'
                ):
                    continue

                masked = mask_value(value, pattern_name)
                findings.append((filename, pattern_name, line_num, masked))

        # Check blocklist terms
        if blocklist:
            for term in blocklist:
                if term['type'] == 'text':
                    if term['value'].lower() in line.lower():
                        findings.append((
                            filename, 'BLOCKLIST',
                            line_num, f"Contains blocked term: '{term['value']}'"
                        ))
                elif term['type'] == 'regex':
                    if re.search(term['value'], line, re.IGNORECASE):
                        findings.append((
                            filename, 'BLOCKLIST',
                            line_num, f"Matches blocked pattern: {term['value']}"
                        ))

    return findings


def mask_value(value: str, pattern_type: str) -> str:
    """Mask sensitive values for safe display."""
    if len(value) <= 4:
        return '*' * len(value)

    if pattern_type == 'email':
        at_pos = value.find('@')
        if at_pos > 2:
            return value[:2] + '***' + value[at_pos:]
        return '***' + value[at_pos:]

    if pattern_type in ('phone_us', 'phone_intl'):
        return value[:3] + '***' + value[-2:]

    if pattern_type in ('api_key', 'aws_access_key', 'github_pat', 'slack_token'):
        return value[:6] + '***'

    if pattern_type == 'aws_arn':
        return value[:20] + '***'

    # Default: show first and last 2 chars
    return value[:2] + '***' + value[-2:]


def scan_file(filepath: Path, blocklist: List[dict] = None,
              strict: bool = False) -> List[Tuple[str, str, int, str]]:
    """Scan a single file."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        return scan_content(content, str(filepath), blocklist, strict)
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return []


def scan_directory(dirpath: Path, blocklist: List[dict] = None,
                   strict: bool = False) -> List[Tuple[str, str, int, str]]:
    """Scan all files in a directory recursively."""
    all_findings = []

    for filepath in sorted(dirpath.rglob('*')):
        if filepath.is_file() and should_scan(filepath):
            findings = scan_file(filepath, blocklist, strict)
            all_findings.extend(findings)

    return all_findings


def get_staged_files() -> List[Path]:
    """Get list of files staged for commit."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR'],
            capture_output=True, text=True, check=True
        )
        repo_root = find_repo_root()
        if not repo_root:
            return []

        files = []
        for line in result.stdout.strip().split('\n'):
            if line:
                filepath = repo_root / line
                if filepath.exists() and should_scan(filepath):
                    files.append(filepath)
        return files
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


# ── Output ───────────────────────────────────────────────────────────

def print_findings(findings: List[Tuple[str, str, int, str]],
                   context: str = "repo") -> None:
    """Print findings in a structured format."""
    if findings:
        # Group by severity
        blocklist_findings = [f for f in findings if f[1] == 'BLOCKLIST']
        critical_findings = [f for f in findings if f[1] in (
            'private_key', 'aws_access_key', 'github_pat', 'slack_token'
        )]
        other_findings = [f for f in findings
                         if f[1] != 'BLOCKLIST' and f not in critical_findings]

        total = len(findings)
        print(f"\n{'='*60}")
        print(f"  BLOCKED — {total} finding(s) in {context}")
        print(f"{'='*60}")

        if blocklist_findings:
            print(f"\n  BLOCKLIST VIOLATIONS ({len(blocklist_findings)}):")
            for filename, _, line_num, masked in blocklist_findings:
                print(f"    {filename}:{line_num} — {masked}")

        if critical_findings:
            print(f"\n  CRITICAL SECRETS ({len(critical_findings)}):")
            for filename, ptype, line_num, masked in critical_findings:
                print(f"    {filename}:{line_num} [{ptype}] — {masked}")

        if other_findings:
            print(f"\n  PII DETECTED ({len(other_findings)}):")
            for filename, ptype, line_num, masked in other_findings:
                print(f"    {filename}:{line_num} [{ptype}] — {masked}")

        print(f"\n{'='*60}")
        print("  Review findings above. Some may be false positives.")
        print("  To allow a value, add it to the ALLOWLIST in pii-scanner.py")
        print(f"{'='*60}\n")
    else:
        print(f"\n  PASSED — No PII or blocklist violations found in {context}\n")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Scan files for sensitive information and blocked terms',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
What it detects:
  PII:        Email, phone, SSN, credit card numbers
  Secrets:    API keys, AWS keys, GitHub PATs, Slack tokens, private keys
  Infra:      AWS ARNs, IP addresses, MAC addresses (strict mode)
  Blocklist:  Custom terms from .security/blocklist.txt

Modes:
  Default:    Scan repo directory
  --staged:   Scan only git-staged files (for pre-commit hooks)
  --strict:   Enable soft patterns (AWS account IDs, IPs, Slack channel IDs)

Examples:
  pii-scanner.py                      # Scan repo
  pii-scanner.py --staged             # Pre-commit hook mode
  pii-scanner.py --strict             # Include soft patterns
  pii-scanner.py --path ./docs        # Scan specific directory
  pii-scanner.py --file CLAUDE.md     # Scan specific file
        """
    )

    parser.add_argument('--path', '-p', default='.',
                        help='Directory to scan (default: current directory)')
    parser.add_argument('--file', '-f',
                        help='Specific file to scan')
    parser.add_argument('--staged', action='store_true',
                        help='Scan only git-staged files (pre-commit mode)')
    parser.add_argument('--strict', action='store_true',
                        help='Enable soft patterns (AWS account IDs, IPs, etc.)')
    parser.add_argument('--blocklist', '-b',
                        help='Path to blocklist file (default: .security/blocklist.txt)')
    parser.add_argument('--no-blocklist', action='store_true',
                        help='Skip blocklist checking')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Only output if findings exist')

    args = parser.parse_args()

    # Load blocklist
    blocklist = []
    if not args.no_blocklist:
        bl_path = Path(args.blocklist) if args.blocklist else None
        blocklist = load_blocklist(bl_path)

    if not args.quiet:
        bl_count = len(blocklist)
        print(f"PII Scanner — checking for sensitive information "
              f"({bl_count} blocklist term{'s' if bl_count != 1 else ''})")
        print("-" * 60)

    # Scan
    if args.staged:
        staged_files = get_staged_files()
        if not staged_files:
            if not args.quiet:
                print("No staged files to scan.")
            sys.exit(0)

        all_findings = []
        for filepath in staged_files:
            findings = scan_file(filepath, blocklist, args.strict)
            all_findings.extend(findings)

        print_findings(all_findings, "staged files")

    elif args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            sys.exit(1)
        findings = scan_file(filepath, blocklist, args.strict)
        print_findings(findings, str(filepath))

    else:
        dirpath = Path(args.path)
        if not dirpath.exists():
            print(f"Error: Directory not found: {dirpath}")
            sys.exit(1)
        findings = scan_directory(dirpath, blocklist, args.strict)
        print_findings(findings, str(dirpath))
        all_findings = findings

    # Exit code: 1 if findings, 0 if clean
    if args.staged:
        sys.exit(1 if all_findings else 0)
    elif args.file:
        sys.exit(1 if findings else 0)
    else:
        sys.exit(1 if findings else 0)


if __name__ == '__main__':
    main()
