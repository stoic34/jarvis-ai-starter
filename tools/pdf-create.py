#!/usr/bin/env python3
"""
PDF Creator Tool
Converts Markdown files to professional PDF documents.

Usage:
    pdf-create.py --input notes.md
    pdf-create.py --input notes.md --output report.pdf
    pdf-create.py --input notes.md --title "My Report"

Requirements:
    pip install weasyprint markdown

    On macOS, you may also need:
    brew install pango

    On Windows, weasyprint may require GTK:
    https://weasyprint.readthedocs.io/en/stable/install.html
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

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("Error: weasyprint not installed")
    print("Run: pip install weasyprint")
    print("\nOn macOS, you may also need: brew install pango")
    sys.exit(1)


# Default CSS for professional-looking PDFs
DEFAULT_CSS = """
@page {
    size: letter;
    margin: 1in;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}

h1 {
    font-size: 24pt;
    font-weight: 600;
    color: #1a1a1a;
    margin-top: 0;
    margin-bottom: 16pt;
    padding-bottom: 8pt;
    border-bottom: 2px solid #e0e0e0;
}

h2 {
    font-size: 18pt;
    font-weight: 600;
    color: #1a1a1a;
    margin-top: 24pt;
    margin-bottom: 12pt;
}

h3 {
    font-size: 14pt;
    font-weight: 600;
    color: #333;
    margin-top: 18pt;
    margin-bottom: 8pt;
}

p {
    margin: 0 0 12pt 0;
}

ul, ol {
    margin: 0 0 12pt 0;
    padding-left: 24pt;
}

li {
    margin-bottom: 6pt;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 12pt 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 8pt 12pt;
    text-align: left;
}

th {
    background-color: #f5f5f5;
    font-weight: 600;
}

tr:nth-child(even) {
    background-color: #fafafa;
}

code {
    font-family: "SF Mono", Monaco, "Cascadia Code", monospace;
    font-size: 10pt;
    background-color: #f5f5f5;
    padding: 2pt 4pt;
    border-radius: 3pt;
}

pre {
    font-family: "SF Mono", Monaco, "Cascadia Code", monospace;
    font-size: 10pt;
    background-color: #f5f5f5;
    padding: 12pt;
    border-radius: 4pt;
    overflow-x: auto;
    margin: 12pt 0;
}

blockquote {
    margin: 12pt 0;
    padding: 8pt 16pt;
    border-left: 4px solid #ddd;
    color: #666;
    font-style: italic;
}

hr {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 24pt 0;
}

a {
    color: #0066cc;
    text-decoration: none;
}
"""


def markdown_to_html(md_content: str, title: str = None) -> str:
    """Convert Markdown to HTML with proper structure."""

    # Convert markdown to HTML
    md_extensions = ['tables', 'fenced_code', 'codehilite', 'toc']
    html_body = markdown.markdown(md_content, extensions=md_extensions)

    # Wrap in full HTML document
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title or 'Document'}</title>
</head>
<body>
{html_body}
</body>
</html>"""

    return html


def create_pdf(input_path: Path, output_path: Path, title: str = None):
    """Convert Markdown file to PDF."""

    # Read markdown content
    md_content = input_path.read_text(encoding='utf-8')

    # Use filename as title if not provided
    if not title:
        title = input_path.stem.replace('-', ' ').replace('_', ' ').title()

    # Convert to HTML
    html_content = markdown_to_html(md_content, title)

    # Create PDF with styling
    html = HTML(string=html_content)
    css = CSS(string=DEFAULT_CSS)
    html.write_pdf(output_path, stylesheets=[css])

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown to professional PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Convert a file:
    pdf-create.py --input notes.md

  Specify output path:
    pdf-create.py --input notes.md --output report.pdf

  Add custom title:
    pdf-create.py --input notes.md --title "Q1 Report"
        """
    )

    parser.add_argument('--input', '-i', required=True,
                        help='Input Markdown file')
    parser.add_argument('--output', '-o',
                        help='Output PDF path (default: same name with .pdf)')
    parser.add_argument('--title', '-t',
                        help='Document title (default: filename)')

    args = parser.parse_args()

    # Validate input
    input_path = Path(args.input).expanduser()
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output).expanduser()
    else:
        output_path = input_path.with_suffix('.pdf')

    # Create PDF
    try:
        result = create_pdf(input_path, output_path, args.title)
        print(f"PDF created: {result}")
    except Exception as e:
        print(f"Error creating PDF: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
