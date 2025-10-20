# Multi-Store Fashion Retail Sales Analysis

**Project Type**: Data Analytics Portfolio Project
**Business Domain**: Fashion/Apparel Retail
**Analysis Period**: January 2024
**Stores Analyzed**: 10 of 10 locations across Japan (100% coverage)
**Status**: ✅ Complete (All 4 phases + 4 output formats)

---

## 📊 Project Overview

This project demonstrates a complete end-to-end data analytics workflow for a multi-store fashion retail chain operating across Japan. The analysis provides executive-level insights on sales performance, seasonal patterns, emerging trends, and strategic recommendations for Q2 2024.

**Key Objective**: Analyze January 2024 sales data to identify patterns, benchmark store performance, and provide actionable recommendations for executive decision-making.

---

## 🎯 Key Results

### Business Impact
- **Total Revenue Analyzed**: ¥43,999,553 (January 2024)
- **Transactions Processed**: 1,155 clean transactions
- **Stores Covered**: All 10 stores (100% network coverage)
- **Regions Covered**: 7 regions (Kanto, Kansai, Hokkaido, Tohoku, Chubu, Chugoku, Kyushu)
- **Insights Delivered**: 6 actionable insights
- **Strategic Recommendations**: 6 Q2 2024 initiatives
- **Output Formats**: 4 professional formats (PDF×2, Word, PowerPoint)

### Top Findings
1. **Kanto regional dominance**: 39.22% of revenue from 4 stores (including new Ikebukuro)
2. **Kyushu market success**: Fukuoka debuts at #3 nationally, validating southern expansion
3. **Category leader**: Footwear drives 29.13% of total sales (winter season strength)
4. **Balanced top-tier**: Top 5 stores each contribute 10-12% with healthy portfolio distribution
5. **Weekday advantage**: 29% higher daily revenue on weekdays vs weekends
6. **National coverage**: 7-region presence with ¥528M annual run-rate potential

---

## 📁 Project Structure

```
claudecode-dataanalytics-example/
│
├── README.md                    # This file
├── CLAUDE.md                    # Project instructions for Claude Code
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── data/                        # Data storage
│   ├── raw/                     # Original store files (10 Excel/CSV files)
│   └── processed/               # Clean datasets
│       ├── sales_clean.csv      # 1,155 transactions (all 10 stores)
│       ├── stores.csv           # 10 store metadata
│       └── products.csv         # 5 product categories
│
├── archive/                     # Old/backup files (version history)
│
├── docs/                        # Project documentation
│   ├── requirements.md          # Business requirements
│   ├── project_flow.md          # Workflow design
│   ├── wbs.md                   # Work breakdown structure
│   ├── data_requirements.md     # Data specifications
│   ├── success_criteria.md      # Success metrics
│   ├── data_dictionary.md       # Field documentation
│   └── reporting_guide.md       # PDF generation guide
│
├── notebooks/                   # Analysis notebooks
│   ├── eda.ipynb               # Exploratory data analysis
│   └── eda_executed.ipynb      # Executed version with outputs
│
├── src/                         # Source code
│   ├── data_pipeline/           # Data engineering (Phase 2)
│   │   ├── loader.py           # Load Excel/CSV files
│   │   ├── cleaner.py          # Clean and standardize data
│   │   ├── validator.py        # Data quality validation
│   │   ├── generate_processed_data.py  # Pipeline orchestration
│   │   └── README.md           # Pipeline documentation
│   │
│   ├── analysis/                # Data analysis (Phase 3)
│   │   ├── __init__.py
│   │   ├── metrics.py          # KPI calculation functions (16 functions)
│   │   └── visualizations.py   # Chart generation functions (10 functions)
│   │
│   └── reporting/               # Multi-format reporting (Phase 4)
│       ├── md_to_pdf_detailed.py      # Generate detailed report PDF
│       ├── md_to_pdf_slides.py        # Generate executive slides PDF
│       ├── md_to_word.py              # Generate Word document
│       ├── md_to_pptx.py              # Generate PowerPoint presentation
│       └── templates/
│           ├── detailed_report.css    # A4 portrait styling
│           └── slides.css             # 16:9 landscape styling
│
├── reports/                     # Analysis outputs
│   ├── analysis_report.md       # Comprehensive Markdown report (15,000 words)
│   ├── detailed_report.pdf      # ⭐ Detailed PDF report (1.6 MB, A4 portrait)
│   ├── executive_slides.pdf     # ⭐ Executive PDF slides (1.3 MB, 16:9)
│   ├── detailed_report.docx     # ⭐ Editable Word document (42 KB)
│   ├── executive_slides.pptx    # ⭐ PowerPoint presentation (1 MB, 13 slides)
│   ├── phase3_validation.md     # Phase 3 validation checklist
│   ├── assets/                  # Visualizations (8 PNG files at 300 DPI)
│   │   ├── daily_revenue_trend.png
│   │   ├── revenue_by_store.png
│   │   ├── revenue_by_region.png
│   │   ├── revenue_by_category.png
│   │   ├── revenue_by_day_of_week.png
│   │   ├── weekend_vs_weekday.png
│   │   ├── category_mix_by_store.png
│   │   └── top_bottom_stores.png
│   └── *.csv                    # Summary tables (3 files)
│
└── tests/                       # Quality tests
    └── test_data_quality.py     # Data validation tests (16 tests, 100% passing)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

For macOS users:
```bash
pip install -r requirements.txt --break-system-packages
```

### Running the Analysis

#### Option 1: View Existing Results (Recommended)
The analysis is already complete. Simply open:
- **Detailed Report**: `reports/detailed_report.pdf`
- **Executive Slides**: `reports/executive_slides.pdf`

#### Option 2: Regenerate Analysis

**Step 1: Run Data Pipeline**
```bash
python src/data_pipeline/generate_processed_data.py
```

**Step 2: Run Tests**
```bash
pytest tests/test_data_quality.py -v
```

**Step 3: Explore Data**
```bash
jupyter notebook notebooks/eda.ipynb
```

**Step 4: Generate Reports (All Four Formats)**
```bash
# Generate all four professional formats
python src/reporting/md_to_pdf_detailed.py && \
python src/reporting/md_to_pdf_slides.py && \
python src/reporting/md_to_word.py && \
python src/reporting/md_to_pptx.py
```

---

## 📊 Key Deliverables

### For Executives (4 Professional Formats)

#### 1. **Detailed PDF Report** (`reports/detailed_report.pdf`)
   - **Format**: A4 portrait
   - **Size**: 1.6 MB
   - **Length**: 20-30 pages
   - **Content**: Complete analysis with all findings and recommendations
   - **Best for**: Board meetings, strategic planning, archival
   - **Editable**: ❌ No

#### 2. **Executive PDF Slides** (`reports/executive_slides.pdf`)
   - **Format**: 16:9 landscape (presentation)
   - **Size**: 1.3 MB
   - **Length**: 14 slides
   - **Content**: Key findings and recommendations
   - **Best for**: Distribution, printing, universal viewing
   - **Editable**: ❌ No

#### 3. **Word Document** (`reports/detailed_report.docx`)
   - **Format**: A4 Word document
   - **Size**: 42 KB
   - **Length**: 20-30 pages
   - **Content**: Complete analysis (same as PDF)
   - **Best for**: Collaboration, comments, track changes
   - **Editable**: ✅ Yes (Word, Google Docs, LibreOffice)

#### 4. **PowerPoint Presentation** (`reports/executive_slides.pptx`)
   - **Format**: 16:9 PowerPoint
   - **Size**: 1 MB
   - **Length**: 13 slides
   - **Content**: Executive summary with charts
   - **Best for**: Live presentations, animations, speaker notes
   - **Editable**: ✅ Yes (PowerPoint, Google Slides, Keynote)

### Format Comparison Matrix

| Feature | PDF | Word | PowerPoint |
|---------|-----|------|------------|
| **Viewing** | Universal | Requires Office | Requires Office |
| **Editing** | ❌ | ✅ | ✅ |
| **File Size** | 1.3-1.6 MB | 42 KB | 1 MB |
| **Collaboration** | Limited | Comments/Track Changes | Speaker Notes |
| **Presentation** | Basic | ❌ | Native Mode ✅ |
| **Print Quality** | Excellent | Excellent | Excellent |

**Recommendation**: Generate all four formats
- **PDF**: For final distribution and archival
- **Word**: For internal review and collaboration
- **PowerPoint**: For live presentations

### For Technical Teams
- Clean datasets ready for further analysis (1,155 transactions, 10 stores)
- Reusable Python functions for metrics and visualizations
- Complete data pipeline for monthly/quarterly updates
- Comprehensive documentation (8 files, 30,000+ words)

---

## 🏆 Team Structure & Methodology

This project was executed using a **4-phase sequential workflow** with specialized roles:

### Phase 1: Project Management ✅
- **Agent**: project-manager-planner
- **Duration**: 1-2 days
- **Deliverables**: 5 planning documents
- **Output**: Requirements, project flow, WBS, data specs, success criteria

### Phase 2: Data Engineering ✅
- **Agent**: data-engineer
- **Duration**: 2-3 days
- **Deliverables**: Data pipeline + clean datasets + tests
- **Output**: 1,155 clean transactions (all 10 stores), 100% test pass rate

### Phase 3: Data Analysis ✅
- **Agent**: data-analyst
- **Duration**: 3-4 days
- **Deliverables**: Analysis notebook + visualizations + report
- **Output**: 6 insights, 6 recommendations, 8 charts

### Phase 4: Multi-Format Reporting ✅
- **Agent**: pdf-reporting-specialist
- **Duration**: 1-2 days
- **Deliverables**: 4 professional report formats
- **Output**: Detailed PDF + Slides PDF + Word document + PowerPoint presentation

**Total Project Duration**: 8-11 days

---

## 📈 Analysis Highlights

### Revenue Performance
- **Total Revenue**: ¥43,999,553 (all 10 stores)
- **Average Transaction**: ¥38,095
- **Top Store**: Osaka (¥5.2M, 11.82%)
- **Top Region**: Kanto (¥17.3M, 39.22% of total revenue)
- **Top Category**: Footwear (¥12.8M, 29.13%)

### Key Insights
1. **Regional Performance**: Kanto stores generate over 1/3 of revenue despite performance gaps
2. **Category Strength**: Footwear dominates due to winter season (January)
3. **Temporal Patterns**: Weekdays outperform weekends by 29% (counter-intuitive)
4. **Store Benchmarking**: 42% performance gap between top and bottom stores
5. **Emerging Opportunity**: Weekend activation potential identified
6. **Best Practices**: Osaka store model ready for replication

### Strategic Recommendations (Q2 2024)
1. Replicate Osaka success model across underperforming stores
2. Expand footwear inventory by 20-25% capitalizing on strength
3. Launch weekday VIP loyalty program leveraging current patterns
4. Implement weekend activation initiatives
5. Deploy dynamic staffing model based on demand patterns
6. Create real-time performance dashboard for management

**Expected Impact**: ¥66M net benefit, 4.0x ROI

---

## 🛠️ Technology Stack

### Programming Language
- **Python 3.8+**

### Data Processing
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **openpyxl** - Excel file handling

### Data Visualization
- **matplotlib** - Core plotting library
- **seaborn** - Statistical visualizations
- **plotly** - Interactive charts

### Report Generation
- **weasyprint** - HTML/CSS to PDF conversion
- **markdown** - Markdown to HTML parsing
- **python-docx** - Word document (.docx) generation
- **python-pptx** - PowerPoint presentation (.pptx) generation

### Testing
- **pytest** - Testing framework
- **pytest-cov** - Code coverage

### Analysis Tools
- **Jupyter** - Interactive notebooks
- **scipy** - Statistical analysis

---

## 📊 Data Overview

### Input Data
- **Source**: 10 store sales files (January 2024)
- **Format**: Mixed Excel (.xlsx) and CSV
- **Language**: Japanese (UTF-8 encoded)
- **Raw Transactions**: 1,279

### Processed Data
- **Clean Transactions**: 1,155 (90.3% retention rate)
- **Stores**: All 10 of 10 (100% coverage)
- **Date Range**: January 1-31, 2024 (31 days)
- **Categories**: 5 (Women's Apparel, Men's Apparel, Accessories, Footwear, Kids)
- **Regions**: 7 (Kanto, Kansai, Hokkaido, Tohoku, Chubu, Chugoku, Kyushu)

### Data Quality
- **Test Pass Rate**: 100% (16/16 tests passing)
- **Critical Fields**: 100% complete (no missing values)
- **Date Validity**: 100% within January 2024
- **Amount Validity**: 100% non-negative
- **Encoding**: UTF-8 (Japanese text correctly handled)

---

## 📚 Documentation

All project documentation is located in the `docs/` directory:

| Document | Description |
|----------|-------------|
| **requirements.md** | Business requirements and objectives |
| **project_flow.md** | Complete workflow and phase dependencies |
| **wbs.md** | Work breakdown structure with task estimates |
| **data_requirements.md** | Data schema specifications and quality standards |
| **success_criteria.md** | Measurable success criteria for each phase |
| **data_dictionary.md** | Complete field-level data documentation |
| **reporting_guide.md** | How to regenerate PDF reports |

---

## ✅ Quality Assurance

### Code Quality
- **PEP 8 Compliant**: All Python code follows style guidelines
- **Documented**: Google-style docstrings for all functions
- **Type Hints**: Function parameters include type annotations
- **Tested**: 16 comprehensive data quality tests (100% passing)

### Data Quality
- No missing values in critical fields
- All dates within valid range
- All sales amounts non-negative
- Referential integrity maintained
- UTF-8 encoding validated

### Visualization Quality
- All charts 300 DPI resolution
- Professional styling and consistent branding
- Clear titles, labels, and legends
- Japanese text renders correctly
- Executive-ready quality

---

## 🔄 Recurring Analysis Framework

This project establishes a **repeatable framework** for monthly/quarterly analysis:

### Monthly Update Process
1. Add new month's data files to `data/raw/`
2. Run data pipeline: `python src/data_pipeline/generate_processed_data.py`
3. Validate data: `pytest tests/test_data_quality.py -v`
4. Update analysis: Open `notebooks/eda.ipynb`, modify date range
5. Regenerate report: Update `reports/analysis_report.md`
6. Generate PDFs: Run both PDF generation scripts
7. Review and distribute to stakeholders

**Estimated Time**: 2-4 hours for recurring monthly updates

---

## 🎓 Skills Demonstrated

This project showcases:
- ✅ **Project Management**: Requirements gathering, planning, WBS creation
- ✅ **Data Engineering**: ETL pipeline, data cleaning, quality validation
- ✅ **Data Analysis**: Exploratory analysis, statistical insights, visualization
- ✅ **Business Intelligence**: KPI definition, metric calculation, trend analysis
- ✅ **Technical Writing**: Comprehensive documentation and reporting
- ✅ **PDF Generation**: Professional document creation for executives
- ✅ **Python Programming**: Clean, documented, tested code
- ✅ **Multi-language Support**: Japanese text handling (UTF-8)
- ✅ **Testing**: Automated quality assurance with pytest
- ✅ **Visualization**: Professional charts for executive presentation

---

## 📞 Contact & Usage

### For Portfolio Review
This project is part of a data analytics portfolio demonstrating end-to-end analytics capabilities from requirements gathering through executive reporting.

### For Recurring Use
The analysis framework can be adapted for:
- Monthly/quarterly sales reviews
- Multi-location performance tracking
- Category/product analysis
- Regional expansion planning
- Store benchmarking programs

---

## 📝 License & Attribution

**Built with**: Claude Code (claude.ai/code)
**Project Type**: Portfolio / Educational
**Data**: Synthetic data generated for demonstration purposes

---

## 🎯 Next Steps

For organizations implementing this framework:

1. **Immediate (Q2 2024)**:
   - Review executive PDFs with C-level team
   - Prioritize top 3 recommendations
   - Allocate budget for implementation

2. **Short-term (Next 30 days)**:
   - Launch Osaka best practice replication pilot
   - Implement weekday VIP program
   - Deploy weekend activation campaign

3. **Ongoing**:
   - Run monthly analysis updates
   - Monitor recommendation KPIs
   - Refine based on results

---

**Project Status**: ✅ Complete
**Last Updated**: October 2025
**Version**: 1.0

---

For questions about methodology, technical implementation, or results interpretation, refer to the comprehensive documentation in the `docs/` directory.
