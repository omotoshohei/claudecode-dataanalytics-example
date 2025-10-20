# PDF and Word Document Reporting Guide

## Multi-Store Fashion Retail Sales Analysis

**Phase 4: PDF & Word Document Reporting**
**Author**: Data Reporting Specialist
**Last Updated**: October 20, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Deliverables](#deliverables)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Word Document Generation](#word-document-generation)
7. [Customization](#customization)
8. [Troubleshooting](#troubleshooting)
9. [File Locations](#file-locations)
10. [Regeneration Instructions](#regeneration-instructions)
11. [Quality Checklist](#quality-checklist)

---

## Overview

Phase 4 (PDF & Word Document Reporting) is the final phase of the Multi-Store Sales Analysis project. This phase transforms the comprehensive Markdown analysis report into three professional, executive-ready documents:

1. **Detailed PDF Report** (A4 Portrait, 20-30 pages): Complete analysis with all findings, visualizations, and recommendations
2. **Executive Slides PDF** (16:9 Landscape, 10-15 slides): High-impact summary for C-level presentation
3. **Word Document** (.docx format): Editable version for collaboration and customization

### Purpose

- Provide polished, professional documents suitable for executive review
- Enable offline distribution and printing
- Deliver visual impact with embedded charts and professional formatting
- Support strategic decision-making with clear, well-organized content
- Allow stakeholders to edit and comment on analysis (Word format)

### Design Philosophy

- **Detailed Report**: Comprehensive, data-rich, suitable for deep analysis
- **Executive Slides**: Visual-first, concise bullet points, presentation-ready
- **Word Document**: Editable, collaborative, Microsoft Office compatible
- **Consistency**: All documents use coordinated color schemes and branding
- **Accessibility**: Professional typography with Japanese text support

---

## Deliverables

### 1. Detailed Report PDF

**File**: `reports/detailed_report.pdf`
**Format**: A4 Portrait (210mm × 297mm)
**Pages**: ~25-30 pages
**Size**: ~1.5-2 MB

**Content Structure**:
- Title page and executive summary
- Project overview and data summary
- Key findings (8 major insights with visualizations)
- Detailed analysis by store, region, category, and time
- Comprehensive recommendations for Q2 2024
- Action plan and next steps
- Appendix (methodology, data dictionary, limitations)

**Features**:
- Professional typography (Georgia serif for body, Helvetica for headers)
- Japanese text support (Hiragino, Yu Gothic, Meiryo fonts)
- Page numbers and running headers
- Automatic page breaks at major sections
- High-quality embedded PNG images (300 DPI)
- Color-coded tables with alternating rows
- Professional blue color scheme (#3498db primary)

### 2. Executive Slides PDF

**File**: `reports/executive_slides.pdf`
**Format**: 16:9 Landscape (297mm × 167mm)
**Slides**: 14 slides
**Size**: ~1.0-1.5 MB

**Slide Structure**:
1. Title slide
2. Executive summary (5 key points)
3. Performance overview with metrics
4. Store performance comparison
5. Regional insights
6. Category performance
7. Weekday vs weekend patterns
8. Category mix by store
9. Top vs bottom performers
10. Strategic recommendations
11. Financial impact projection
12. Q2 action plan
13. Next steps
14. Closing slide

**Features**:
- Large, readable fonts (20-48pt)
- Maximum 5 bullet points per slide
- Full-width chart images
- Gradient backgrounds for key slides
- Minimal text, maximum visual impact
- Slide numbers in bottom right corner
- Consistent slide layout and branding

---

## Prerequisites

### Required Files

Before generating PDFs, ensure these files exist:

1. **Analysis Report**: `reports/analysis_report.md`
   - Created by Data Analyst in Phase 3
   - Must be complete Markdown file with all sections

2. **Visualizations**: `reports/assets/*.png`
   - 8 PNG image files at 300 DPI
   - Files required:
     - `daily_revenue_trend.png`
     - `revenue_by_store.png`
     - `revenue_by_region.png`
     - `revenue_by_category.png`
     - `revenue_by_day_of_week.png`
     - `category_mix_by_store.png`
     - `top_bottom_stores.png`
     - `weekend_vs_weekday.png`

3. **Project Structure**:
   ```
   project-root/
   ├── reports/
   │   ├── analysis_report.md
   │   └── assets/
   │       └── *.png (8 images)
   ├── src/
   │   └── reporting/
   │       ├── md_to_pdf_detailed.py
   │       ├── md_to_pdf_slides.py
   │       └── templates/
   │           ├── detailed_report.css
   │           └── slides.css
   └── docs/
       └── reporting_guide.md (this file)
   ```

### System Requirements

- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.8 or higher
- **Memory**: Minimum 2GB RAM available
- **Disk Space**: 100MB for dependencies + generated PDFs

---

## Installation

### Step 1: Install Python Dependencies

Install the required Python packages using pip:

```bash
pip install weasyprint markdown --break-system-packages
```

**Required packages**:
- `weasyprint` (v65.1+): PDF generation engine
- `markdown` (v3.4+): Markdown to HTML conversion

**Additional dependencies** (installed automatically):
- `pydyf`: PDF writing library
- `cffi`: C Foreign Function Interface
- `tinyhtml5`: HTML parsing
- `tinycss2`: CSS parsing
- `Pillow`: Image processing
- `fonttools`: Font handling

### Step 2: Verify Installation

Test that WeasyPrint is properly installed:

```bash
python -c "from weasyprint import HTML, CSS; print('✓ WeasyPrint installed successfully')"
```

Expected output: `✓ WeasyPrint installed successfully`

### Step 3: Check File Structure

Verify all required files are in place:

```bash
# Check Markdown report
ls -lh reports/analysis_report.md

# Check assets directory
ls -lh reports/assets/*.png

# Check reporting scripts
ls -lh src/reporting/*.py

# Check CSS templates
ls -lh src/reporting/templates/*.css
```

---

## Usage

### Generating the Detailed Report

Run the detailed report generation script from the project root:

```bash
python src/reporting/md_to_pdf_detailed.py
```

**Expected output**:
```
============================================================
DETAILED PDF REPORT GENERATOR
============================================================

Validating required files...
✓ Markdown input: reports/analysis_report.md
✓ CSS template: src/reporting/templates/detailed_report.css
✓ Assets directory: reports/assets (8 images)
✓ Output directory: reports

✓ All required files validated successfully!

Reading Markdown file...
✓ Read 781 lines (33,670 characters)

Converting Markdown to HTML...
✓ HTML conversion successful (42,222 characters)

Creating HTML document structure...
✓ HTML document created

Generating PDF...
This may take 30-60 seconds for a 20-30 page report...
✓ PDF generated successfully!
  Output: reports/detailed_report.pdf
  Size: 1.56 MB (1,638,153 bytes)
```

**Processing time**: 30-60 seconds depending on system performance

**Output**: `reports/detailed_report.pdf` (~1.5 MB, A4 portrait)

### Generating Executive Slides

Run the executive slides generation script:

```bash
python src/reporting/md_to_pdf_slides.py
```

**Expected output**:
```
============================================================
EXECUTIVE SLIDES PDF GENERATOR
============================================================

Validating required files...
✓ CSS template: src/reporting/templates/slides.css
✓ Assets directory: reports/assets (8 images)
✓ All required images present

Creating slide content...
✓ Created 14 executive slides
  - Slide 1: Title
  - Slides 2-9: Key findings with visuals
  - Slides 10-13: Recommendations and action plan
  - Slide 14: Closing

Generating executive slides PDF...
This may take 20-40 seconds for 14 slides...
✓ PDF generated successfully!
  Output: reports/executive_slides.pdf
  Size: 1.29 MB (1,356,780 bytes)
```

**Processing time**: 20-40 seconds

**Output**: `reports/executive_slides.pdf` (~1.3 MB, 16:9 landscape)

### Generating Both PDFs

To generate both PDFs in sequence:

```bash
python src/reporting/md_to_pdf_detailed.py && python src/reporting/md_to_pdf_slides.py
```

---

## Word Document Generation

### Overview

In addition to PDF outputs, you can generate an **editable Microsoft Word document** (.docx) from the Markdown analysis report. This format is ideal for:

- **Collaborative editing**: Stakeholders can add comments and track changes
- **Internal distribution**: Easier to share within organizations using Microsoft Office
- **Customization**: Executives can modify content before final presentation
- **Accessibility**: Compatible with Microsoft Word, Google Docs, and LibreOffice

### Installing python-docx

The Word document generator requires the `python-docx` library:

```bash
# macOS
pip install python-docx --break-system-packages

# Linux/Windows
pip install python-docx
```

**Verify installation**:
```bash
python -c "from docx import Document; print('✓ python-docx installed successfully')"
```

### Generating the Word Document

Run the Word conversion script from the project root:

```bash
python src/reporting/md_to_word.py
```

**Expected output**:
```
================================================================================
MARKDOWN TO WORD CONVERSION
================================================================================
Input file:  /path/to/reports/analysis_report.md
Output file: /path/to/reports/detailed_report.docx
Assets dir:  /path/to/reports

Converting Markdown to Word document...
✅ Word document created: reports/detailed_report.docx
   File size: 42.47 KB

================================================================================
✅ CONVERSION COMPLETE
================================================================================

Word document ready: reports/detailed_report.docx

You can now:
  - Open in Microsoft Word
  - Edit and add comments
  - Share with stakeholders
  - Print for distribution
```

**Processing time**: 5-10 seconds

**Output**: `reports/detailed_report.docx` (~40-50 KB, A4 portrait)

### Word Document Features

The generated Word document includes:

**Content**:
- All headings (H1-H4) from Markdown
- Body paragraphs with proper line spacing
- Bullet lists and numbered lists
- Tables with professional styling
- Embedded images from `reports/assets/`

**Styling**:
- Heading 1: 24pt, bold, dark blue (#0a4073)
- Heading 2: 18pt, bold, blue with bottom border
- Heading 3: 14pt, bold, medium blue
- Body text: 11pt Calibri, 1.5 line spacing
- Tables: Blue header row, alternating row colors
- Images: Centered, 5.5 inches wide

**Page Setup**:
- A4 page size (21cm × 29.7cm)
- Margins: 2.5cm all around
- Header: Project title centered at top
- Footer: Page numbers centered at bottom

**Japanese Text Support**:
- Compatible with Japanese characters
- Uses system fonts (Hiragino Sans, Yu Gothic)
- UTF-8 encoding throughout

### Editing the Word Document

After generation, you can:

1. **Open in Microsoft Word**:
   ```bash
   # macOS
   open reports/detailed_report.docx

   # Windows
   start reports\detailed_report.docx
   ```

2. **Edit content**:
   - Modify text, headings, and recommendations
   - Add comments and track changes
   - Insert additional sections or analysis

3. **Reformat**:
   - Change fonts and colors
   - Adjust page margins
   - Modify table styles
   - Resize images

4. **Export to PDF** (from Word):
   - File → Save As → PDF
   - Maintains formatting and embedded images

### Word vs PDF Comparison

| Feature | Word (.docx) | PDF |
|---------|--------------|-----|
| **Editable** | ✅ Yes | ❌ No |
| **Collaboration** | ✅ Comments, track changes | ⚠️ Limited (annotations only) |
| **File Size** | ~40-50 KB | ~1.5 MB |
| **Formatting Consistency** | ⚠️ May vary by software | ✅ Always consistent |
| **Print Quality** | ✅ High | ✅ High |
| **Universal Viewing** | ⚠️ Requires Word/compatible software | ✅ Any PDF reader |
| **Professional Look** | ✅ Good | ✅ Excellent |

**Recommendation**: Generate both formats
- **Word (.docx)**: For internal review and collaboration
- **PDF**: For final distribution and executive presentation

### Generating All Three Formats

To generate all outputs (detailed PDF, slides PDF, and Word document):

```bash
# Generate all three documents
python src/reporting/md_to_pdf_detailed.py && \
python src/reporting/md_to_pdf_slides.py && \
python src/reporting/md_to_word.py
```

**Total processing time**: ~60-90 seconds

**Outputs**:
- `reports/detailed_report.pdf` (~1.5 MB)
- `reports/executive_slides.pdf` (~1.3 MB)
- `reports/detailed_report.docx` (~40-50 KB)

---

## PowerPoint Presentation Generation

### Overview

In addition to PDF slides, you can generate a **fully editable PowerPoint presentation** (.pptx) with the same content. This format is ideal for:

- **Live presentations**: Native PowerPoint format for smooth presenting
- **Slide editing**: Modify text, colors, layouts directly in PowerPoint
- **Animations**: Add transitions and custom animations
- **Speaker notes**: Add presenter notes for each slide
- **Rearranging**: Drag and drop slides to change order
- **Compatibility**: Works with PowerPoint, Google Slides, Keynote

### Installing python-pptx

The PowerPoint generator requires the `python-pptx` library:

```bash
# macOS
pip install python-pptx --break-system-packages

# Linux/Windows
pip install python-pptx
```

**Verify installation**:
```bash
python -c "from pptx import Presentation; print('✓ python-pptx installed successfully')"
```

### Generating the PowerPoint Presentation

Run the PowerPoint generation script from the project root:

```bash
python src/reporting/md_to_pptx.py
```

**Expected output**:
```
================================================================================
POWERPOINT PRESENTATION GENERATOR
================================================================================

Assets directory: reports/assets
Output file: reports/executive_slides.pptx

Loading sales data...
✓ Loaded 1,155 transactions

Creating PowerPoint presentation...
✓ Presentation initialized (16:9 format)

Generating slides:
  [1/13] Title slide
  [2/13] Executive summary
  [3/13] Business metrics
  [4/13] Store performance chart
  [5/13] Regional analysis chart
  [6/13] Category performance chart
  [7/13] Day of week chart
  [8/13] Weekend vs weekday chart
  [9/13] Category mix by store
 [10/13] Top vs bottom performers
 [11/13] Key findings
 [12/13] Recommendations
 [13/13] Closing slide

Saving PowerPoint presentation...
✓ PowerPoint created: reports/executive_slides.pptx
  File size: 1043.08 KB

================================================================================
✅ POWERPOINT GENERATION COMPLETE
================================================================================
```

**Processing time**: 5-10 seconds

**Output**: `reports/executive_slides.pptx` (~1 MB, 16:9 widescreen, 13 slides)

### PowerPoint Slide Structure

The generated presentation includes **13 professional slides**:

**Slide 1: Title Slide**
- Blue gradient background
- Project name and subtitle
- Date

**Slide 2: Executive Summary**
- 5 key findings in bullet points
- High-level overview

**Slide 3: Business Metrics**
- 4 metric boxes in 2×2 grid
- Total Revenue, Transactions, Avg Transaction, Active Stores
- Large numbers with blue backgrounds

**Slides 4-10: Data Visualizations**
- Embedded PNG charts from `reports/assets/`
- Full-width images for maximum impact
- Captions explaining key insights

**Slide 11: Key Findings**
- 5 critical insights
- Supporting the business case

**Slide 12: Strategic Recommendations**
- 5 actionable recommendations for Q2 2024
- Prioritized by impact

**Slide 13: Closing Slide**
- Thank you message
- Dark blue background
- Call to action

### PowerPoint Features

**Design**:
- 16:9 widescreen format (10 × 5.625 inches)
- Professional blue color scheme
  - Primary: #3498db (bright blue)
  - Dark: #0a4073 (navy blue)
  - Light: #aed6f1 (light blue)
- Calibri font throughout
- Clean, modern layout

**Content**:
- Clear hierarchy with large titles (32-44pt)
- Readable body text (18pt minimum)
- Maximum 5 bullet points per slide
- High-quality embedded charts (300 DPI)
- Consistent spacing and alignment

**Editability**:
- All text boxes are editable
- Images can be resized/repositioned
- Slides can be reordered
- New slides can be added
- Fully compatible with:
  - Microsoft PowerPoint (Windows/Mac)
  - Google Slides (web-based)
  - Apple Keynote (Mac/iPad)
  - LibreOffice Impress (open source)

### Editing the PowerPoint Presentation

After generation, you can:

1. **Open in PowerPoint**:
   ```bash
   # macOS
   open reports/executive_slides.pptx

   # Windows
   start reports\executive_slides.pptx
   ```

2. **Edit content**:
   - Click any text box to edit
   - Modify bullet points and findings
   - Update numbers and metrics
   - Change slide titles

3. **Customize design**:
   - Change theme colors
   - Apply different fonts
   - Modify layouts
   - Add company logo
   - Insert additional slides

4. **Add animations**:
   - Apply slide transitions
   - Animate bullet points
   - Add chart reveals
   - Set timing for auto-advance

5. **Add speaker notes**:
   - View → Notes Page
   - Add presenter notes for each slide
   - Print notes for reference

6. **Present**:
   - Slide Show → From Beginning
   - Use presenter view for notes
   - Navigate with arrow keys or clicker

### PowerPoint vs PDF Slides Comparison

| Feature | PowerPoint (.pptx) | PDF Slides |
|---------|-------------------|------------|
| **Editable** | ✅ Fully editable | ❌ Fixed layout |
| **Animations** | ✅ Transitions, effects | ❌ Static |
| **Presenting** | ✅ Native presentation mode | ⚠️ Basic slideshow |
| **File Size** | ~1 MB | ~1.3 MB |
| **Rearrange Slides** | ✅ Drag and drop | ❌ No |
| **Speaker Notes** | ✅ Yes | ⚠️ Limited |
| **Universal Viewing** | ⚠️ Requires compatible software | ✅ Any PDF reader |
| **Formatting Consistency** | ⚠️ May vary by software | ✅ Always consistent |
| **Print Quality** | ✅ High | ✅ High |

**Recommendation**: Use both formats
- **PowerPoint (.pptx)**: For live presentations and editing
- **PDF**: For distribution and archival

### Generating All Four Formats

To generate all report formats (detailed PDF, slides PDF, Word, PowerPoint):

```bash
# Generate all four documents
python src/reporting/md_to_pdf_detailed.py && \
python src/reporting/md_to_pdf_slides.py && \
python src/reporting/md_to_word.py && \
python src/reporting/md_to_pptx.py
```

**Total processing time**: ~90-120 seconds

**Complete outputs**:
- `reports/detailed_report.pdf` (~1.5 MB) - Comprehensive analysis
- `reports/executive_slides.pdf` (~1.3 MB) - PDF slides for distribution
- `reports/detailed_report.docx` (~40-50 KB) - Editable Word document
- `reports/executive_slides.pptx` (~1 MB) - Editable PowerPoint presentation

### PowerPoint Best Practices

**For Presentations**:
1. Use presenter view (View → Presenter View)
2. Add speaker notes for talking points
3. Practice with slide transitions
4. Test on presentation equipment beforehand
5. Have backup PDF in case of compatibility issues

**For Customization**:
1. Keep consistent color scheme when editing
2. Maintain large font sizes (18pt minimum)
3. Limit text per slide (5 bullets max)
4. Use high-quality images only
5. Test edited version before presenting

**For Distribution**:
1. Export to PDF from PowerPoint for final version
2. Include both .pptx and .pdf when sharing
3. Use "Save As → PDF" to preserve animations as static
4. Check file size before email distribution

---

## Customization

### Modifying CSS Styles

#### Detailed Report Styling

Edit `src/reporting/templates/detailed_report.css` to customize:

**Color scheme**:
```css
/* Primary brand color */
h1, h2 { color: #0a4073; }
hr { border-top: 2px solid #3498db; }

/* Change to your brand colors */
h1, h2 { color: #your-color; }
```

**Typography**:
```css
/* Body text */
body {
    font-family: Georgia, 'Hiragino Mincho ProN', serif;
    font-size: 11pt;
    line-height: 1.7;
}

/* Adjust font sizes */
h1 { font-size: 24pt; }
h2 { font-size: 18pt; }
```

**Page margins**:
```css
@page {
    size: A4 portrait;
    margin: 25mm 20mm 25mm 20mm; /* top, right, bottom, left */
}
```

**Table styling**:
```css
thead {
    background: #3498db; /* Header background */
    color: white;
}

tbody tr:nth-child(even) {
    background-color: #f8f9fa; /* Alternating row color */
}
```

#### Executive Slides Styling

Edit `src/reporting/templates/slides.css` to customize:

**Slide dimensions**:
```css
@page {
    size: 297mm 167mm; /* 16:9 landscape */
    /* Or change to: size: 210mm 297mm; for A4 portrait */
}
```

**Title slide background**:
```css
.title-slide {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Change gradient colors */
}
```

**Font sizes**:
```css
h1 { font-size: 48pt; }
h2 { font-size: 36pt; }
li { font-size: 20pt; }
/* Adjust as needed for readability */
```

**Bullet point styling**:
```css
li:before {
    content: "▸";
    color: #3498db;
    font-size: 28pt;
}
/* Change bullet symbol or color */
```

### Modifying Slide Content

Edit `src/reporting/md_to_pdf_slides.py` to customize slide content:

**Adding a new slide**:
```python
# Add after existing slides in create_slides_html() function
"""
<!-- SLIDE X: YOUR CUSTOM SLIDE -->
<section class="slide">
    <h2>Your Slide Title</h2>
    <ul>
        <li>Point 1</li>
        <li>Point 2</li>
        <li>Point 3</li>
    </ul>
    <img src="assets/your_image.png" alt="Description" class="chart-image">
</section>
"""
```

**Changing slide order**: Reorder the `<section>` blocks in the HTML string

**Modifying metrics**: Update the numbers in stat boxes:
```python
<div class="stat-box">
    <span class="number">¥34.9M</span>  <!-- Change value here -->
    <span class="label">Total Revenue</span>
</div>
```

### Adding Custom Fonts

To use custom fonts, add font files and update CSS:

1. Place font files in `src/reporting/templates/fonts/`
2. Update CSS with `@font-face` declarations:

```css
@font-face {
    font-family: 'YourCustomFont';
    src: url('fonts/YourFont.woff2') format('woff2');
}

body {
    font-family: 'YourCustomFont', sans-serif;
}
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Markdown input not found"

**Error**: `❌ Markdown input not found: reports/analysis_report.md`

**Solution**:
1. Verify the file exists: `ls reports/analysis_report.md`
2. If missing, Phase 3 (Data Analysis) must be completed first
3. Ensure you're running the script from the project root directory

#### Issue 2: "Assets directory not found"

**Error**: `❌ Assets directory not found: reports/assets`

**Solution**:
1. Create the directory: `mkdir -p reports/assets`
2. Ensure Phase 3 generated all 8 PNG visualization files
3. Verify image files: `ls -lh reports/assets/*.png`

#### Issue 3: "Missing required images"

**Error**: `❌ Missing required images: daily_revenue_trend.png, ...`

**Solution**:
1. Re-run the analysis notebook in Phase 3 to regenerate visualizations
2. Ensure all chart-saving code executed successfully
3. Verify image file names match exactly (case-sensitive)

#### Issue 4: WeasyPrint installation fails

**Error**: `ERROR: Failed building wheel for weasyprint`

**Solution (macOS)**:
```bash
# Install system dependencies using Homebrew
brew install cairo pango gdk-pixbuf libffi

# Then install WeasyPrint
pip install weasyprint --break-system-packages
```

**Solution (Linux - Ubuntu/Debian)**:
```bash
sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

pip install weasyprint
```

**Solution (Windows)**:
1. Download GTK3 runtime from https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
2. Install GTK3
3. Then install WeasyPrint: `pip install weasyprint`

#### Issue 5: PDF generation is very slow

**Problem**: PDF generation takes more than 2 minutes

**Solution**:
1. Optimize images: Reduce PNG file sizes if they're very large (>5 MB each)
2. Use image compression:
   ```bash
   # Install optipng
   brew install optipng  # macOS

   # Optimize all PNGs
   optipng -o5 reports/assets/*.png
   ```
3. Close other applications to free up memory
4. This is normal for first-time generation; subsequent runs may be faster

#### Issue 6: Japanese text not rendering

**Problem**: Japanese characters appear as boxes or replacement characters

**Solution**:
1. Ensure Japanese fonts are installed on your system:
   - macOS: Hiragino Sans (built-in)
   - Windows: Yu Gothic (built-in)
   - Linux: Install: `sudo apt-get install fonts-noto-cjk`
2. Update CSS font stack to include fallback fonts
3. Verify file encoding is UTF-8: `file -I reports/analysis_report.md`

#### Issue 7: Images not appearing in PDF

**Problem**: PDF generates but images are missing or broken

**Solution**:
1. Verify image paths in Markdown are correct: `assets/filename.png` (relative paths)
2. Ensure `base_url` parameter is set correctly in Python script
3. Check image files aren't corrupted:
   ```bash
   # Test each image
   file reports/assets/*.png
   ```
4. Verify images are in PNG format (not JPEG with .png extension)

#### Issue 8: PDF file size too large

**Problem**: PDF is larger than 5 MB

**Solution**:
1. Optimize PNG images before generation:
   ```python
   from PIL import Image

   img = Image.open('reports/assets/chart.png')
   img.save('reports/assets/chart.png', optimize=True, quality=85)
   ```
2. Reduce image DPI from 300 to 200 if print quality isn't required
3. Consider converting to JPEG for photographic content (not charts)

---

## File Locations

### Input Files

| File | Path | Created By | Purpose |
|------|------|------------|---------|
| Analysis report | `reports/analysis_report.md` | Phase 3 Analyst | Source content for PDFs |
| Visualizations | `reports/assets/*.png` | Phase 3 Analyst | Charts and graphs (8 files) |

### Output Files

| File | Path | Format | Size | Pages/Slides |
|------|------|--------|------|--------------|
| Detailed report | `reports/detailed_report.pdf` | A4 Portrait | ~1.5 MB | ~25-30 pages |
| Executive slides | `reports/executive_slides.pdf` | 16:9 Landscape | ~1.3 MB | 14 slides |

### Script Files

| File | Path | Purpose |
|------|------|---------|
| Detailed PDF script | `src/reporting/md_to_pdf_detailed.py` | Generate A4 detailed report |
| Slides PDF script | `src/reporting/md_to_pdf_slides.py` | Generate 16:9 executive slides |

### Style Templates

| File | Path | Purpose |
|------|------|---------|
| Detailed report CSS | `src/reporting/templates/detailed_report.css` | Styling for A4 report |
| Slides CSS | `src/reporting/templates/slides.css` | Styling for slides |

### Documentation

| File | Path | Purpose |
|------|------|---------|
| Reporting guide | `docs/reporting_guide.md` | This document |
| Project requirements | `docs/requirements.md` | Phase 1 planning |
| Data dictionary | `docs/data_dictionary.md` | Phase 2 data reference |

---

## Regeneration Instructions

### When to Regenerate PDFs

Regenerate PDFs when:

1. **Analysis report updated**: Insights, recommendations, or data changed
2. **New visualizations**: Charts updated with new styling or data
3. **Styling changes**: CSS templates modified for branding
4. **Content corrections**: Typos or errors found in report
5. **Presentation date**: Update metadata with current date

### Quick Regeneration

From project root directory:

```bash
# Regenerate both PDFs
python src/reporting/md_to_pdf_detailed.py && \
python src/reporting/md_to_pdf_slides.py
```

### Regeneration After Analysis Changes

If you update the analysis report or visualizations:

```bash
# 1. Update analysis report
# Edit reports/analysis_report.md

# 2. Regenerate visualizations (if needed)
# Re-run notebooks/eda.ipynb

# 3. Regenerate PDFs
python src/reporting/md_to_pdf_detailed.py
python src/reporting/md_to_pdf_slides.py

# 4. Verify outputs
open reports/detailed_report.pdf
open reports/executive_slides.pdf
```

### Batch Regeneration Script

Create a shell script for convenience:

```bash
#!/bin/bash
# File: regenerate_pdfs.sh

echo "Regenerating PDF reports..."

# Detailed report
echo "1/2 Generating detailed report..."
python src/reporting/md_to_pdf_detailed.py

# Executive slides
echo "2/2 Generating executive slides..."
python src/reporting/md_to_pdf_slides.py

echo "✓ Both PDFs regenerated successfully!"
echo "  - reports/detailed_report.pdf"
echo "  - reports/executive_slides.pdf"
```

Make executable and run:
```bash
chmod +x regenerate_pdfs.sh
./regenerate_pdfs.sh
```

---

## Quality Checklist

### Pre-Generation Checklist

Before running PDF generation scripts, verify:

- [ ] `reports/analysis_report.md` exists and is complete
- [ ] All 8 PNG visualization files exist in `reports/assets/`
- [ ] Image files are valid (not corrupted)
- [ ] Image file names match references in Markdown
- [ ] WeasyPrint and Markdown packages installed
- [ ] Running from project root directory
- [ ] No pending changes to analysis content

### Post-Generation Checklist - Detailed Report

After generating `detailed_report.pdf`, verify:

**Content**:
- [ ] All sections from Markdown appear in PDF
- [ ] Section headings are properly formatted
- [ ] Body text is readable and justified
- [ ] Lists and bullet points render correctly
- [ ] Tables are complete with all rows and columns

**Images**:
- [ ] All 8 visualizations appear in PDF
- [ ] Images are clear and high-quality (not blurry)
- [ ] Image captions/alt text appear correctly
- [ ] Images are properly sized (not too small/large)
- [ ] No broken image placeholders

**Formatting**:
- [ ] Page breaks occur at appropriate sections
- [ ] Headers and footers appear on all pages
- [ ] Page numbers are sequential and correct
- [ ] No orphaned headings (heading at bottom of page)
- [ ] No widowed lines (single line at top of page)
- [ ] Margins are consistent throughout

**Typography**:
- [ ] Fonts render correctly (no missing glyphs)
- [ ] Japanese text appears properly (if applicable)
- [ ] Font sizes are appropriate and readable
- [ ] Bold and italic styling work correctly
- [ ] Code blocks (if any) use monospace font

**Overall Quality**:
- [ ] PDF is 20-30 pages long
- [ ] File size is reasonable (~1-2 MB)
- [ ] Document opens correctly in PDF reader
- [ ] Professional appearance suitable for executives
- [ ] No rendering errors or artifacts

### Post-Generation Checklist - Executive Slides

After generating `executive_slides.pdf`, verify:

**Content**:
- [ ] All 14 slides present in correct order
- [ ] Slide 1: Title slide with project name
- [ ] Slide 2: Executive summary with 5 key points
- [ ] Slides 3-9: Key findings with visualizations
- [ ] Slides 10-13: Recommendations and action plan
- [ ] Slide 14: Closing slide

**Images**:
- [ ] 7 charts appear across multiple slides
- [ ] Images are large and clearly visible
- [ ] Charts are centered and properly sized
- [ ] No broken image placeholders
- [ ] Image quality suitable for projection

**Formatting**:
- [ ] Each slide is on separate PDF page
- [ ] Slide numbers appear (except title slide)
- [ ] Landscape orientation (16:9 ratio)
- [ ] Bullet points use custom styling
- [ ] Maximum 5 bullets per slide maintained

**Typography**:
- [ ] Large fonts (20-48pt) are readable
- [ ] Headings are bold and prominent
- [ ] Text contrasts well with backgrounds
- [ ] No text overflow or cut-off content
- [ ] Japanese text renders if applicable

**Visual Design**:
- [ ] Title slide has gradient background
- [ ] Summary slide uses brand colors
- [ ] Stat boxes display metrics clearly
- [ ] Color scheme is consistent across slides
- [ ] Professional appearance for C-level audience

**Overall Quality**:
- [ ] PDF is 14 slides (pages) long
- [ ] File size is reasonable (~1-1.5 MB)
- [ ] Slides suitable for presentation/projection
- [ ] High visual impact with minimal text
- [ ] No rendering errors or artifacts

---

## Advanced Topics

### Automating PDF Generation

Set up a workflow to auto-generate PDFs when analysis changes:

```bash
#!/bin/bash
# File: auto_regenerate.sh
# Watch for changes and regenerate PDFs

while true; do
    inotifywait -e modify reports/analysis_report.md reports/assets/*.png
    echo "Changes detected, regenerating PDFs..."
    python src/reporting/md_to_pdf_detailed.py
    python src/reporting/md_to_pdf_slides.py
    echo "✓ PDFs updated at $(date)"
done
```

### Version Control for PDFs

Add PDF metadata for versioning:

```python
# In md_to_pdf_detailed.py, add to HTML head:
<meta name="version" content="1.0">
<meta name="date" content="2024-10-19">
<meta name="status" content="Final">
```

### Embedding Clickable Links

Make tables of contents clickable:

```html
<!-- In Markdown -->
## Table of Contents
- [Executive Summary](#executive-summary)
- [Key Findings](#key-findings)

<!-- Anchor -->
<a name="executive-summary"></a>
## Executive Summary
```

### Adding Watermarks

Add a watermark for draft versions:

```css
/* In CSS */
@page {
    background: url('watermark-draft.png') no-repeat center;
    background-size: 50%;
    opacity: 0.1;
}
```

---

## Support and Resources

### Documentation

- **WeasyPrint Documentation**: https://doc.courtbouillon.org/weasyprint/
- **Markdown Guide**: https://www.markdownguide.org/
- **CSS Print Guide**: https://www.smashingmagazine.com/2015/01/designing-for-print-with-css/

### Getting Help

If you encounter issues:

1. Check this troubleshooting guide first
2. Review error messages carefully
3. Verify all prerequisites are met
4. Check WeasyPrint GitHub issues: https://github.com/Kozea/WeasyPrint/issues

### Reporting Bugs

When reporting issues, include:

- Operating system and version
- Python version: `python --version`
- WeasyPrint version: `pip show weasyprint`
- Complete error message
- Steps to reproduce
- Sample files (if applicable)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-19 | Initial release with detailed report and executive slides |

---

## Conclusion

You now have complete documentation for generating professional PDF reports from the Multi-Store Sales Analysis. This reporting phase transforms raw data analysis into polished, executive-ready documents suitable for strategic decision-making.

**Key takeaways**:

1. Two professional PDFs are generated: detailed report (A4) and executive slides (16:9)
2. Both scripts include validation, error handling, and user-friendly output
3. CSS templates provide complete control over styling and branding
4. Regeneration is simple and can be automated
5. Comprehensive quality checklist ensures professional results

**Project completion**: Phase 4 deliverables mark the completion of all four project phases:

- Phase 1: Project planning and requirements (Project Manager)
- Phase 2: Data engineering and pipeline (Data Engineer)
- Phase 3: Analysis and insights (Data Analyst)
- Phase 4: PDF reporting (Data Reporting Specialist) ✓

The final deliverables are ready for executive presentation and strategic decision-making.

---

**Generated with Claude Code**
**Data Reporting Specialist | Phase 4**
**Multi-Store Fashion Retail Sales Analysis Project**
