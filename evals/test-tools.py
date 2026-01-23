#!/usr/bin/env python3
"""
Tool Test Suite
Tests that all starter kit tools are working correctly.

Usage:
    test-tools.py           # Run all tests
    test-tools.py --quick   # Quick tests only (no API calls)
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run_command(cmd: list, timeout: int = 30) -> tuple:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def test_python():
    """Test Python is available."""
    success, output = run_command(['python3', '--version'])
    return success, f"Python: {output.strip()}" if success else "Python not found"


def test_gogcli():
    """Test gogcli is installed."""
    success, output = run_command(['gogcli', '--version'])
    return success, f"gogcli: {output.strip()}" if success else "gogcli not found"


def test_gogcli_auth():
    """Test gogcli is authenticated."""
    success, output = run_command(['gogcli', 'auth', 'status'])
    if success and 'authenticated' in output.lower():
        return True, "gogcli: authenticated"
    return False, "gogcli: not authenticated (run: gogcli auth login)"


def test_gemini_key():
    """Test Gemini API key is set."""
    key = os.environ.get('GEMINI_API_KEY')
    if key:
        return True, f"GEMINI_API_KEY: set ({key[:8]}...)"
    return False, "GEMINI_API_KEY: not set"


def test_pdf_dependencies():
    """Test PDF generation dependencies."""
    try:
        import markdown
        import weasyprint
        return True, "PDF dependencies: installed"
    except ImportError as e:
        return False, f"PDF dependencies: missing ({e.name})"


def test_pdf_generation():
    """Test PDF generation works."""
    with tempfile.TemporaryDirectory() as tmpdir:
        md_file = Path(tmpdir) / "test.md"
        pdf_file = Path(tmpdir) / "test.pdf"

        md_file.write_text("# Test\n\nThis is a test document.")

        tools_dir = Path(__file__).parent.parent / "tools"
        pdf_script = tools_dir / "pdf-create.py"

        if not pdf_script.exists():
            return False, "pdf-create.py not found"

        success, output = run_command([
            'python3', str(pdf_script),
            '--input', str(md_file),
            '--output', str(pdf_file)
        ])

        if success and pdf_file.exists():
            return True, f"PDF generation: working ({pdf_file.stat().st_size} bytes)"
        return False, f"PDF generation: failed - {output}"


def test_html_generation():
    """Test HTML generation works."""
    with tempfile.TemporaryDirectory() as tmpdir:
        md_file = Path(tmpdir) / "test.md"
        html_file = Path(tmpdir) / "test.html"

        md_file.write_text("# Test\n\n- Item 1\n- Item 2")

        tools_dir = Path(__file__).parent.parent / "tools"
        html_script = tools_dir / "md-to-html.py"

        if not html_script.exists():
            return False, "md-to-html.py not found"

        success, output = run_command([
            'python3', str(html_script),
            '--input', str(md_file),
            '--output', str(html_file),
            '--email'
        ])

        if success and html_file.exists():
            content = html_file.read_text()
            if '<h1>' in content and '<li>' in content:
                return True, "HTML generation: working"
        return False, f"HTML generation: failed - {output}"


def main():
    parser = argparse.ArgumentParser(description='Test starter kit tools')
    parser.add_argument('--quick', '-q', action='store_true',
                        help='Quick tests only (no API calls)')
    args = parser.parse_args()

    print("Jarvis AI Starter Kit - Tool Tests")
    print("=" * 50)
    print()

    tests = [
        ("Python", test_python),
        ("gogcli installed", test_gogcli),
        ("gogcli authenticated", test_gogcli_auth),
        ("Gemini API key", test_gemini_key),
        ("PDF dependencies", test_pdf_dependencies),
    ]

    if not args.quick:
        tests.extend([
            ("PDF generation", test_pdf_generation),
            ("HTML generation", test_html_generation),
        ])

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            success, message = test_func()
            status = "✓" if success else "✗"
            print(f"  {status} {message}")
            if success:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ {name}: error - {e}")
            failed += 1

    print()
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")

    if failed > 0:
        print("\nSome tests failed. Review the output above.")
        print("Run the setup guide to install missing dependencies.")
        sys.exit(1)
    else:
        print("\nAll tests passed! Your tools are ready.")


if __name__ == '__main__':
    main()
