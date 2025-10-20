#!/usr/bin/env python3
"""
Multi-Store Fashion Retail Sales Analysis - Detailed PDF Report Generator

This script converts the Markdown analysis report to a professional PDF document
suitable for executive presentation.

Format: A4 Portrait (210mm x 297mm)
Target: 20-30 pages of well-formatted content
Output: reports/detailed_report.pdf

Dependencies:
    - weasyprint: PDF generation engine
    - markdown: Markdown to HTML conversion

Usage:
    python src/reporting/md_to_pdf_detailed.py

Author: Data Reporting Specialist
Project: Multi-Store Sales Analysis
Phase: 4 - PDF Reporting
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from weasyprint import HTML, CSS
from markdown import markdown

# ============================================
# CONFIGURATION
# ============================================

# Project root directory (2 levels up from this script)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Input and output paths
MARKDOWN_INPUT = PROJECT_ROOT / "reports" / "analysis_report.md"
CSS_TEMPLATE = PROJECT_ROOT / "src" / "reporting" / "templates" / "detailed_report.css"
PDF_OUTPUT = PROJECT_ROOT / "reports" / "detailed_report.pdf"
ASSETS_DIR = PROJECT_ROOT / "reports" / "assets"

# Markdown extensions for proper rendering
MARKDOWN_EXTENSIONS = [
    'tables',           # Support for tables
    'fenced_code',      # Support for code blocks
    'nl2br',            # Convert newlines to <br>
    'sane_lists',       # Better list handling
]


# ============================================
# HELPER FUNCTIONS
# ============================================

def validate_files():
    """
    Validate that all required files exist before PDF generation.

    Returns:
        bool: True if all files exist, False otherwise
    """
    print("\n" + "="*60)
    print("DETAILED PDF REPORT GENERATOR")
    print("="*60)
    print(f"\nValidating required files...")

    errors = []

    # Check Markdown input file
    if not MARKDOWN_INPUT.exists():
        errors.append(f"❌ Markdown input not found: {MARKDOWN_INPUT}")
    else:
        print(f"✓ Markdown input: {MARKDOWN_INPUT}")

    # Check CSS template
    if not CSS_TEMPLATE.exists():
        errors.append(f"❌ CSS template not found: {CSS_TEMPLATE}")
    else:
        print(f"✓ CSS template: {CSS_TEMPLATE}")

    # Check assets directory
    if not ASSETS_DIR.exists():
        errors.append(f"❌ Assets directory not found: {ASSETS_DIR}")
    else:
        image_count = len(list(ASSETS_DIR.glob("*.png")))
        print(f"✓ Assets directory: {ASSETS_DIR} ({image_count} images)")

    # Output directory
    PDF_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory: {PDF_OUTPUT.parent}")

    if errors:
        print("\n❌ Validation failed:")
        for error in errors:
            print(f"  {error}")
        return False

    print("\n✓ All required files validated successfully!")
    return True


def read_markdown_file():
    """
    Read and return the content of the Markdown file.

    Returns:
        str: Markdown content
    """
    print(f"\nReading Markdown file...")
    try:
        with open(MARKDOWN_INPUT, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = len(content.split('\n'))
        chars = len(content)
        print(f"✓ Read {lines:,} lines ({chars:,} characters)")
        return content

    except Exception as e:
        print(f"❌ Error reading Markdown file: {e}")
        sys.exit(1)


def convert_markdown_to_html(markdown_content):
    """
    Convert Markdown content to HTML with proper extensions.

    Args:
        markdown_content (str): Raw Markdown text

    Returns:
        str: HTML content
    """
    print(f"\nConverting Markdown to HTML...")
    try:
        html_body = markdown(
            markdown_content,
            extensions=MARKDOWN_EXTENSIONS
        )

        print(f"✓ HTML conversion successful ({len(html_body):,} characters)")
        return html_body

    except Exception as e:
        print(f"❌ Error converting Markdown to HTML: {e}")
        sys.exit(1)


def create_html_document(html_body):
    """
    Wrap HTML body in complete HTML document with proper metadata.

    Args:
        html_body (str): HTML content from Markdown conversion

    Returns:
        str: Complete HTML document
    """
    print(f"\nCreating HTML document structure...")

    # Build complete HTML document
    html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="Data Analysis Team">
    <meta name="description" content="Multi-Store Fashion Retail Sales Analysis - January 2024">
    <meta name="keywords" content="sales analysis, retail analytics, fashion retail, Japan">
    <meta name="generator" content="Claude Code - Data Reporting Specialist">
    <title>Multi-Store Sales Analysis - Detailed Report</title>
</head>
<body>
{html_body}

<div class="report-footer">
    <p><strong>Multi-Store Fashion Retail Sales Analysis</strong></p>
    <p>Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
    <p>Generated with Claude Code | Data Reporting Specialist</p>
</div>
</body>
</html>"""

    print(f"✓ HTML document created")
    return html_document


def generate_pdf(html_content):
    """
    Generate PDF from HTML content using WeasyPrint.

    Args:
        html_content (str): Complete HTML document
    """
    print(f"\nGenerating PDF...")
    print(f"This may take 30-60 seconds for a 20-30 page report...")

    try:
        # Create HTML object with base URL for resolving relative paths
        html_obj = HTML(
            string=html_content,
            base_url=str(PROJECT_ROOT / "reports")
        )

        # Load CSS stylesheet
        css_obj = CSS(filename=str(CSS_TEMPLATE))

        # Generate PDF
        html_obj.write_pdf(
            target=str(PDF_OUTPUT),
            stylesheets=[css_obj]
        )

        # Get PDF file size
        pdf_size = PDF_OUTPUT.stat().st_size
        pdf_size_mb = pdf_size / (1024 * 1024)

        print(f"✓ PDF generated successfully!")
        print(f"  Output: {PDF_OUTPUT}")
        print(f"  Size: {pdf_size_mb:.2f} MB ({pdf_size:,} bytes)")

    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        print(f"\nTroubleshooting tips:")
        print(f"  1. Ensure all images in reports/assets/ are valid PNG files")
        print(f"  2. Check that Markdown file doesn't have syntax errors")
        print(f"  3. Verify WeasyPrint is properly installed: pip install weasyprint")
        print(f"  4. Check CSS template for syntax errors")
        sys.exit(1)


def display_summary():
    """Display generation summary and next steps."""
    print("\n" + "="*60)
    print("PDF GENERATION COMPLETE")
    print("="*60)
    print(f"\n✓ Detailed report generated: {PDF_OUTPUT}")
    print(f"\nNext steps:")
    print(f"  1. Open the PDF to verify quality and formatting")
    print(f"  2. Check that all images are properly embedded")
    print(f"  3. Verify page breaks occur at appropriate sections")
    print(f"  4. Run: python src/reporting/md_to_pdf_slides.py")
    print(f"\nTo regenerate this PDF:")
    print(f"  python {Path(__file__).relative_to(PROJECT_ROOT)}")
    print(f"\nFor help, see: docs/reporting_guide.md")
    print("="*60 + "\n")


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main execution function."""

    # Step 1: Validate all required files exist
    if not validate_files():
        sys.exit(1)

    # Step 2: Read Markdown file
    markdown_content = read_markdown_file()

    # Step 3: Convert Markdown to HTML
    html_body = convert_markdown_to_html(markdown_content)

    # Step 4: Create complete HTML document
    html_document = create_html_document(html_body)

    # Step 5: Generate PDF
    generate_pdf(html_document)

    # Step 6: Display summary
    display_summary()


if __name__ == "__main__":
    main()
