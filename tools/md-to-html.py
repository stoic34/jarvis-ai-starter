#!/usr/bin/env python3
"""
Markdown to HTML Converter
Converts Markdown to HTML, optimized for email formatting.

Usage:
    md-to-html.py --input draft.md
    md-to-html.py --input draft.md --output email.html
    md-to-html.py --input draft.md --email  # Inline styles for email

Requirements:
    pip install markdown pygments
"""

import argparse
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Error: markdown not installed")
    print("Run: pip install markdown")
    sys.exit(1)


# Email-safe inline CSS (since email clients strip <style> tags)
EMAIL_STYLE = """
<style>
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 14px; line-height: 1.5; color: #333; }
h1 { font-size: 22px; font-weight: 600; margin: 0 0 16px 0; }
h2 { font-size: 18px; font-weight: 600; margin: 24px 0 12px 0; }
h3 { font-size: 16px; font-weight: 600; margin: 18px 0 8px 0; }
p { margin: 0 0 12px 0; }
ul, ol { margin: 0 0 12px 0; padding-left: 24px; }
li { margin-bottom: 4px; }
table { border-collapse: collapse; margin: 12px 0; }
th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
th { background-color: #f5f5f5; }
code { font-family: monospace; background-color: #f5f5f5; padding: 2px 4px; }
blockquote { margin: 12px 0; padding: 8px 16px; border-left: 4px solid #ddd; color: #666; }
</style>
"""


def markdown_to_html(md_content: str, for_email: bool = False) -> str:
    """Convert Markdown to HTML."""

    # Extensions for common markdown features
    extensions = ['tables', 'fenced_code', 'nl2br']

    # Convert
    html_body = markdown.markdown(md_content, extensions=extensions)

    if for_email:
        # Wrap with email-compatible HTML
        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{EMAIL_STYLE}
</head>
<body>
{html_body}
</body>
</html>"""
    else:
        # Simple HTML without wrapper
        html = html_body

    return html


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown to HTML',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Convert to HTML:
    md-to-html.py --input draft.md

  Save to file:
    md-to-html.py --input draft.md --output email.html

  Format for email (with inline styles):
    md-to-html.py --input draft.md --email
        """
    )

    parser.add_argument('--input', '-i', required=True,
                        help='Input Markdown file')
    parser.add_argument('--output', '-o',
                        help='Output HTML file (prints to stdout if not specified)')
    parser.add_argument('--email', '-e', action='store_true',
                        help='Format for email (includes styles)')

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input).expanduser()
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    md_content = input_path.read_text(encoding='utf-8')

    # Convert
    html = markdown_to_html(md_content, for_email=args.email)

    # Output
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.write_text(html, encoding='utf-8')
        print(f"HTML saved to: {output_path}")
    else:
        print(html)


if __name__ == '__main__':
    main()
