#!/usr/bin/env python3
"""
Multi-Store Fashion Retail Sales Analysis - Executive Slides PDF Generator

This script extracts key insights from the analysis report and creates
executive summary slides in PDF format.

Format: 16:9 Landscape (297mm x 167mm)
Target: 10-15 high-impact slides
Output: reports/executive_slides.pdf

Dependencies:
    - weasyprint: PDF generation engine
    - markdown: Markdown to HTML conversion (minimal use)

Usage:
    python src/reporting/md_to_pdf_slides.py

Author: Data Reporting Specialist
Project: Multi-Store Sales Analysis
Phase: 4 - PDF Reporting
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from weasyprint import HTML, CSS

# ============================================
# CONFIGURATION
# ============================================

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Input and output paths
MARKDOWN_INPUT = PROJECT_ROOT / "reports" / "analysis_report.md"
CSS_TEMPLATE = PROJECT_ROOT / "src" / "reporting" / "templates" / "slides.css"
PDF_OUTPUT = PROJECT_ROOT / "reports" / "executive_slides.pdf"
ASSETS_DIR = PROJECT_ROOT / "reports" / "assets"


# ============================================
# SLIDE CONTENT CREATION
# ============================================

def create_slides_html():
    """
    Create HTML content for executive slides by extracting key insights
    from the analysis report.

    Returns:
        str: Complete HTML document for slides
    """
    print("\n" + "="*60)
    print("EXECUTIVE SLIDES PDF GENERATOR")
    print("="*60)
    print(f"\nCreating slide content...")

    slides_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Store Sales Analysis - Executive Summary</title>
</head>
<body>

<!-- SLIDE 1: TITLE SLIDE -->
<section class="slide title-slide">
    <h1>Multi-Store Fashion Retail<br>Sales Analysis</h1>
    <div class="subtitle">January 2024 Performance Analysis</div>
    <div class="meta">
        <p>Prepared for Executive Management Team</p>
        <p>Data Analysis Team | October 2025</p>
    </div>
</section>

<!-- SLIDE 2: EXECUTIVE SUMMARY -->
<section class="slide summary-slide">
    <h2>Executive Summary</h2>
    <ul>
        <li><strong>¥34.9M revenue</strong> from 928 transactions across 8 stores</li>
        <li><strong>42% performance gap</strong> between top (Osaka) and bottom (Hiroshima) stores</li>
        <li><strong>Footwear dominates</strong> with 29.1% revenue share (¥10.1M)</li>
        <li><strong>Weekdays outperform weekends</strong> by 29% (untapped weekend opportunity)</li>
        <li><strong>¥66M net benefit</strong> potential from Q2 recommendations (4.0x ROI)</li>
    </ul>
</section>

<!-- SLIDE 3: PERFORMANCE OVERVIEW -->
<section class="slide">
    <h2>January 2024 Performance Overview</h2>

    <div class="stat-grid">
        <div class="stat-box">
            <span class="number">¥34.9M</span>
            <span class="label">Total Revenue</span>
        </div>
        <div class="stat-box">
            <span class="number">928</span>
            <span class="label">Transactions</span>
        </div>
        <div class="stat-box">
            <span class="number">¥37.6K</span>
            <span class="label">Avg Transaction</span>
        </div>
        <div class="stat-box">
            <span class="number">8</span>
            <span class="label">Active Stores</span>
        </div>
    </div>

    <img src="assets/daily_revenue_trend.png" alt="Daily Revenue Trend" class="chart-image">
</section>

<!-- SLIDE 4: STORE PERFORMANCE COMPARISON -->
<section class="slide finding-slide">
    <h2>Store Performance: 42% Gap Between Top & Bottom</h2>

    <img src="assets/revenue_by_store.png" alt="Revenue by Store" class="chart-image">

    <ul>
        <li><strong>Osaka leads</strong> with ¥5.2M (14.9% of total)</li>
        <li><strong>Top 3 stores</strong> generate 41.2% of revenue</li>
        <li><strong>Hiroshima underperforms</strong> at ¥3.6M (opportunity for improvement)</li>
    </ul>
</section>

<!-- SLIDE 5: REGIONAL INSIGHTS -->
<section class="slide finding-slide">
    <h2>Regional Performance: Kanto Dominates, Kansai Excels</h2>

    <img src="assets/revenue_by_region.png" alt="Revenue by Region" class="chart-image">

    <ul>
        <li><strong>Kanto region:</strong> 36.6% of revenue (3 stores)</li>
        <li><strong>Regional stores outperform</strong> Kanto on per-store basis</li>
        <li><strong>Osaka's success</strong> suggests Kansai expansion opportunity</li>
    </ul>
</section>

<!-- SLIDE 6: CATEGORY PERFORMANCE -->
<section class="slide finding-slide">
    <h2>Category Performance: Footwear Leads at 29%</h2>

    <img src="assets/revenue_by_category.png" alt="Revenue by Category" class="chart-image">

    <ul>
        <li><strong>Footwear:</strong> ¥10.1M (29.1%) - winter season strength</li>
        <li><strong>Women's Apparel:</strong> ¥8.9M (25.4%) - urban concentration</li>
        <li><strong>Top 2 categories</strong> drive 54.5% of total revenue</li>
    </ul>
</section>

<!-- SLIDE 7: WEEKDAY VS WEEKEND PATTERN -->
<section class="slide finding-slide">
    <h2>Traffic Pattern: Weekday Dominance (29% Higher Revenue)</h2>

    <img src="assets/revenue_by_day_of_week.png" alt="Revenue by Day of Week" class="chart-image">

    <ul>
        <li><strong>Weekdays:</strong> ¥1.2M average daily revenue (77% of total)</li>
        <li><strong>Weekends:</strong> ¥0.9M average daily revenue (23% of total)</li>
        <li><strong>Major opportunity</strong> to activate weekend sales</li>
    </ul>
</section>

<!-- SLIDE 8: CATEGORY MIX BY STORE -->
<section class="slide finding-slide">
    <h2>Category Mix Varies by Store Location</h2>

    <img src="assets/category_mix_by_store.png" alt="Category Mix by Store" class="chart-image">

    <ul>
        <li><strong>Urban stores</strong> favor Women's Apparel (30-35%)</li>
        <li><strong>Regional stores</strong> prefer Footwear (35-40%)</li>
        <li><strong>Insight:</strong> Tailor inventory to local preferences</li>
    </ul>
</section>

<!-- SLIDE 9: TOP PERFORMERS VS UNDERPERFORMERS -->
<section class="slide finding-slide">
    <h2>Best Practice Replication Opportunity</h2>

    <img src="assets/top_bottom_stores.png" alt="Top vs Bottom Stores" class="chart-image">

    <ul>
        <li><strong>Osaka's success factors:</strong> Category mix + transaction volume</li>
        <li><strong>Replication potential:</strong> +17% revenue for bottom performers</li>
        <li><strong>Action:</strong> Deploy top performer best practices network-wide</li>
    </ul>
</section>

<!-- SLIDE 10: KEY RECOMMENDATIONS -->
<section class="slide recommendation-slide">
    <h2>Strategic Recommendations for Q2 2024</h2>

    <ol>
        <li class="priority-high"><strong>Replicate Osaka Success Model</strong><br>
        Deploy best practices to underperforming stores (Target: +¥18M annual)</li>

        <li class="priority-high"><strong>Expand Footwear Inventory 20-25%</strong><br>
        Capitalize on category strength (Target: +¥2M monthly)</li>

        <li class="priority-high"><strong>Launch Weekday VIP Program</strong><br>
        Leverage high-value weekday customers (Target: +¥37M annual)</li>

        <li class="priority-medium"><strong>Weekend Activation Program</strong><br>
        Events and promotions to drive weekend traffic (Target: +¥11M Apr-Aug)</li>
    </ol>
</section>

<!-- SLIDE 11: FINANCIAL IMPACT -->
<section class="slide">
    <h2>Q2 Recommendations: ¥66M Net Benefit Potential</h2>

    <div class="stat-grid">
        <div class="stat-box">
            <span class="number">¥16.3M</span>
            <span class="label">Total Investment</span>
        </div>
        <div class="stat-box">
            <span class="number">¥66M</span>
            <span class="label">Year 1 Net Benefit</span>
        </div>
        <div class="stat-box">
            <span class="number">4.0x</span>
            <span class="label">ROI</span>
        </div>
    </div>

    <ul class="mb-small">
        <li>Revenue increase: <strong>+¥60M</strong> from growth initiatives</li>
        <li>Cost reduction: <strong>-¥6M</strong> from dynamic staffing</li>
        <li>Implementation timeline: <strong>Q2 2024 (April-June)</strong></li>
    </ul>
</section>

<!-- SLIDE 12: Q2 ACTION PLAN -->
<section class="slide">
    <h2>Q2 2024 Action Plan</h2>

    <h3>April (Month 1)</h3>
    <ul>
        <li><strong>Week 1:</strong> Approve strategic plan, start operational audits</li>
        <li><strong>Week 2-3:</strong> Finalize Footwear orders, design VIP program</li>
        <li><strong>Week 4:</strong> Launch weekend activation and VIP pilot</li>
    </ul>

    <h3>May-June (Month 2-3)</h3>
    <ul>
        <li><strong>May:</strong> Analyze April results, expand VIP network-wide</li>
        <li><strong>June:</strong> Full Q2 analysis and Q3 planning</li>
    </ul>
</section>

<!-- SLIDE 13: NEXT STEPS -->
<section class="slide">
    <h2>Next Steps</h2>

    <div class="priority-high">
        <h3>Immediate Actions (This Week)</h3>
        <ul>
            <li>Executive team approval of ¥16.3M Q2 budget</li>
            <li>Form cross-functional implementation team</li>
            <li>Schedule Osaka store manager operational audits</li>
        </ul>
    </div>

    <div class="priority-medium">
        <h3>Short-term (Next 2 Weeks)</h3>
        <ul>
            <li>Finalize Footwear spring collection orders</li>
            <li>Design Weekday VIP program benefits and IT requirements</li>
            <li>Plan Saturday Social event calendar</li>
        </ul>
    </div>
</section>

<!-- SLIDE 14: CLOSING SLIDE -->
<section class="slide closing-slide">
    <h2>Thank You</h2>
    <p>Questions & Discussion</p>
    <br>
    <p style="font-size: 18pt; opacity: 0.8;">For detailed analysis, see full report:<br><em>Multi-Store Sales Analysis - Detailed Report.pdf</em></p>
    <br>
    <p style="font-size: 16pt; opacity: 0.7;">Generated with Claude Code | Data Analysis Team</p>
</section>

</body>
</html>"""

    print(f"✓ Created 14 executive slides")
    print(f"  - Slide 1: Title")
    print(f"  - Slides 2-9: Key findings with visuals")
    print(f"  - Slides 10-13: Recommendations and action plan")
    print(f"  - Slide 14: Closing")

    return slides_html


def validate_files():
    """
    Validate that all required files exist.

    Returns:
        bool: True if all files exist, False otherwise
    """
    print(f"\nValidating required files...")

    errors = []

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

        # Verify key images exist
        required_images = [
            "daily_revenue_trend.png",
            "revenue_by_store.png",
            "revenue_by_region.png",
            "revenue_by_category.png",
            "revenue_by_day_of_week.png",
            "category_mix_by_store.png",
            "top_bottom_stores.png"
        ]

        missing_images = []
        for img in required_images:
            if not (ASSETS_DIR / img).exists():
                missing_images.append(img)

        if missing_images:
            errors.append(f"❌ Missing required images: {', '.join(missing_images)}")
        else:
            print(f"✓ All required images present")

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


def generate_pdf(html_content):
    """
    Generate PDF from HTML content using WeasyPrint.

    Args:
        html_content (str): Complete HTML document
    """
    print(f"\nGenerating executive slides PDF...")
    print(f"This may take 20-40 seconds for 14 slides...")

    try:
        # Create HTML object
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
        print(f"  2. Verify WeasyPrint is properly installed: pip install weasyprint")
        print(f"  3. Check CSS template for syntax errors")
        print(f"  4. Verify image paths in HTML match actual file names")
        sys.exit(1)


def display_summary():
    """Display generation summary and project completion."""
    print("\n" + "="*60)
    print("EXECUTIVE SLIDES GENERATION COMPLETE")
    print("="*60)
    print(f"\n✓ Executive slides generated: {PDF_OUTPUT}")
    print(f"\n" + "="*60)
    print("PHASE 4 COMPLETE - ALL DELIVERABLES GENERATED")
    print("="*60)
    print(f"\nFinal deliverables:")
    print(f"  1. Detailed Report (A4): {PROJECT_ROOT / 'reports' / 'detailed_report.pdf'}")
    print(f"  2. Executive Slides (16:9): {PDF_OUTPUT}")
    print(f"\nNext steps:")
    print(f"  1. Open both PDFs to verify quality")
    print(f"  2. Check formatting, images, and page breaks")
    print(f"  3. Review docs/reporting_guide.md for regeneration instructions")
    print(f"  4. Project complete - ready for executive presentation!")
    print(f"\nTo regenerate slides:")
    print(f"  python {Path(__file__).relative_to(PROJECT_ROOT)}")
    print("="*60 + "\n")


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main execution function."""

    # Step 1: Validate required files
    if not validate_files():
        sys.exit(1)

    # Step 2: Create slides HTML content
    html_content = create_slides_html()

    # Step 3: Generate PDF
    generate_pdf(html_content)

    # Step 4: Display summary
    display_summary()


if __name__ == "__main__":
    main()
