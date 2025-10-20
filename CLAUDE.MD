# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a data analysis portfolio project demonstrating a multi-role analytics workflow using Claude Code. The project analyzes sales data from 10 Japanese retail stores and delivers professional executive-ready reports.

**Business Context**: Multi-store retail chain operating across Japan (Shibuya, Shinjuku, Ikebukuro, Yokohama, Osaka, Sapporo, Sendai, Nagoya, Hiroshima, Fukuoka) with sales data for January 2024.

**Final Deliverables**:
1. Detailed analysis report (PDF, A4 portrait, 20-30 pages)
2. Executive summary slides (PDF, 16:9 landscape, 10-15 slides)

---

## Current Project Status

**Data Available**: 10 store sales files in `/data/` directory
- Files are mix of Excel (.xlsx) and CSV formats
- File naming is inconsistent (intentional - demonstrates real-world data challenges)
- Data is in Japanese with various formatting styles
- Time period: January 2024

**Next Steps**: Follow the 4-phase workflow below to complete the project.

---

## Using Claude Code Sub-Agents

This project is designed to work with **4 specialized sub-agents** that handle each phase autonomously. Each agent has expertise in their domain and will execute their phase end-to-end.

### Available Sub-Agents

1. **project-manager-planner** - Handles Phase 1 (Project Planning)
2. **data-engineer** - Handles Phase 2 (Data Pipeline & Quality)
3. **data-analyst** - Handles Phase 3 (Analysis & Insights)
4. **pdf-reporting-specialist** - Handles Phase 4 (PDF Report Generation)

### How to Use Sub-Agents

**Launch agents using the Task tool**:

```
Phase 1: Launch project-manager-planner
Phase 2: Launch data-engineer
Phase 3: Launch data-analyst
Phase 4: Launch pdf-reporting-specialist
```

**Important**: Execute phases sequentially. Each agent depends on the previous phase's deliverables.

### Manual Execution (Alternative)

You can also execute phases manually by following the detailed instructions below if sub-agents are not available.

---

## 4-Phase Workflow (Execute Sequentially)

### Phase 1: Project Manager (Documentation)
**Sub-Agent**: `project-manager-planner`
**Persona**: Experienced PM specializing in data analytics projects

**Create these files in `docs/`**:
- `requirements.md` - Project scope, objectives, stakeholders, key questions
- `project_flow.md` - Workflow design with phase dependencies
- `wbs.md` - Task breakdown with effort estimates
- `data_requirements.md` - Data field specifications and quality standards
- `success_criteria.md` - Measurable success metrics

**Key Specifications**:
- 10 stores across Japan
- January 2024 timeframe
- Retail business (specify type: coffee shop, convenience store, etc.)
- Include seasonality, store performance differences, product trends

---

### Phase 2: Data Engineer (Data Pipeline)
**Sub-Agent**: `data-engineer`
**Persona**: Data engineer building reliable datasets

**Tasks**:
1. Build data ingestion pipeline (`src/data_pipeline/`)
   - `loader.py` - Read Excel/CSV with encoding handling (Japanese text)
   - `cleaner.py` - Standardize schemas, handle missing values, fix data types
   - `validator.py` - Quality checks (non-negative sales, valid dates, consistent IDs)

2. Generate processed datasets (`data/processed/`)
   - `sales_clean.csv` - Unified sales transactions
   - `stores.csv` - Store metadata (location, size, region)
   - `products.csv` - Product categories

3. Create `tests/test_data_quality.py` with pytest assertions

4. Document in `docs/data_dictionary.md`

**Quality Standards**:
- No nulls in: date, store_id, sales_amount
- All sales amounts >= 0
- Dates within Jan 2024
- Consistent store IDs across files

---

### Phase 3: Data Analyst (Analysis & Insights)
**Sub-Agent**: `data-analyst`
**Persona**: Analyst finding business insights through data

**Deliverables**:
1. `notebooks/eda.ipynb` - Complete exploratory analysis
   - Load from `data/processed/`
   - Statistical summaries
   - Visualizations
   - Insight discovery

2. `src/analysis/` - Reusable functions
   - `metrics.py` - KPI calculations
   - `visualizations.py` - Chart functions

3. `reports/assets/` - Save all charts as PNG:
   - Sales trend over time
   - Store performance comparison (by region, by store)
   - Product category breakdown
   - Day-of-week patterns
   - Seasonality/weekend effects

4. `reports/analysis_report.md` - Main report in Markdown
   - Executive summary (3-5 key findings)
   - Data overview
   - Findings with embedded images
   - Recommendations
   - Next steps

**Report Structure**:
```markdown
# Multi-Store Sales Analysis Report

## Executive Summary
[3-5 key findings, main recommendations]

## 1. Project Overview

## 2. Data Overview

## 3. Key Findings
### 3.1 Sales Trend Analysis
![Sales Trend](assets/trend_chart.png)

### 3.2 Store Performance
![Store Comparison](assets/store_comparison.png)

### 3.3 Product Category Analysis
![Categories](assets/category_breakdown.png)

### 3.4 Temporal Patterns
![Patterns](assets/temporal_patterns.png)

## 4. Detailed Analysis

## 5. Recommendations

## 6. Next Steps

## Appendix
```

---

### Phase 4: Data Reporting Specialist (PDF Generation)
**Sub-Agent**: `pdf-reporting-specialist`
**Persona**: Reporting specialist creating executive-ready documents

**Tasks**:
1. Create `src/reporting/` scripts:
   - `md_to_pdf_detailed.py` - Generate A4 portrait detailed report
   - `md_to_pdf_slides.py` - Generate 16:9 landscape slides
   - `templates/detailed_report.css` - Professional styling
   - `templates/slides.css` - Presentation styling

2. Generate `reports/detailed_report.pdf`:
   - A4 portrait, 20-30 pages
   - Professional typography
   - High-quality images
   - Page breaks at sections

3. Generate `reports/executive_slides.pdf`:
   - 16:9 landscape, 10-15 slides
   - Large visuals, concise bullets
   - Slide structure:
     1. Title
     2. Executive summary
     3-4. Project & data overview
     5-10. Key findings (one per slide)
     11. Recommendations
     12-13. Next steps

4. Create `docs/reporting_guide.md` with regeneration instructions

**PDF Generation Template**:
```python
from weasyprint import HTML, CSS
from markdown import markdown

with open('reports/analysis_report.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>
    {markdown(md_content, extensions=['tables', 'fenced_code'])}
</body>
</html>
"""

HTML(string=html_content, base_url='.').write_pdf(
    'reports/detailed_report.pdf',
    stylesheets=[CSS('src/reporting/templates/detailed_report.css')]
)
```

---

## Technical Stack & Commands

### Dependencies
```bash
pip install pandas numpy matplotlib seaborn plotly weasyprint markdown pytest jupyter openpyxl --break-system-packages
```

**Note**: `openpyxl` is required for reading Excel files.

### Common Commands

**Run data pipeline**:
```bash
python data/raw/generate_sales_data.py  # If generating synthetic data
python src/data_pipeline/loader.py      # Load and clean existing data
```

**Run tests**:
```bash
pytest tests/test_data_quality.py -v
```

**Run analysis**:
```bash
jupyter notebook notebooks/eda.ipynb
```

**Generate reports**:
```bash
python src/reporting/md_to_pdf_detailed.py
python src/reporting/md_to_pdf_slides.py
```

---

## Directory Structure

```
claudecode-dataanalytics-example/
├── CLAUDE.md                   # This file
├── README.md                   # Project overview
├── requirements.txt            # Python dependencies
│
├── docs/                       # Project documentation
│   ├── requirements.md         # [PM] Requirements
│   ├── project_flow.md         # [PM] Workflow
│   ├── wbs.md                  # [PM] Task breakdown
│   ├── data_requirements.md    # [PM] Data specs
│   ├── success_criteria.md     # [PM] Success metrics
│   ├── data_dictionary.md      # [DE] Data dictionary
│   └── reporting_guide.md      # [RS] Report generation guide
│
├── data/
│   ├── raw/                    # Raw store data files (10 files)
│   │   ├── 01_渋谷店_売上_202401.xlsx
│   │   ├── 02_新宿店_売上_202401.xlsx
│   │   └── ... (8 more files)
│   └── processed/              # Cleaned datasets
│       ├── sales_clean.csv
│       ├── stores.csv
│       └── products.csv
│
├── notebooks/
│   └── eda.ipynb              # [DA] Exploratory analysis
│
├── src/
│   ├── data_pipeline/         # [DE] ETL code
│   │   ├── loader.py
│   │   ├── cleaner.py
│   │   └── validator.py
│   ├── analysis/              # [DA] Analysis functions
│   │   ├── metrics.py
│   │   └── visualizations.py
│   └── reporting/             # [RS] PDF generation
│       ├── md_to_pdf_detailed.py
│       ├── md_to_pdf_slides.py
│       └── templates/
│           ├── detailed_report.css
│           └── slides.css
│
├── reports/                   # Analysis outputs
│   ├── analysis_report.md     # [DA] Main Markdown report
│   ├── detailed_report.pdf    # [RS] Detailed PDF
│   ├── executive_slides.pdf   # [RS] Slides PDF
│   └── assets/                # [DA] Charts (PNG files)
│
└── tests/
    └── test_data_quality.py   # [DE] Data quality tests
```

---

## Code Architecture & Patterns

### Data Pipeline Flow
```
Raw Data (Excel/CSV)
  → loader.py (read with encoding handling)
  → cleaner.py (standardize, clean, transform)
  → validator.py (quality checks)
  → Processed CSV files
```

### Analysis Flow
```
Processed Data
  → metrics.py (calculate KPIs)
  → visualizations.py (generate charts)
  → eda.ipynb (exploratory analysis)
  → analysis_report.md (Markdown report)
```

### Reporting Flow
```
analysis_report.md
  → md_to_pdf_detailed.py → detailed_report.pdf (A4)
  → md_to_pdf_slides.py → executive_slides.pdf (16:9)
```

### Key Design Principles
- **Separation of Concerns**: Each phase has distinct responsibilities
- **Reusability**: Functions in `src/` are importable and reusable
- **Documentation**: All code has docstrings, all data has data dictionary
- **Testing**: Data quality is validated with automated tests
- **Bilingual Support**: Handle Japanese text properly (UTF-8 encoding)

---

## Handling Japanese Text Data

**Critical for this project**: Data files contain Japanese characters.

**Reading files**:
```python
# For CSV
df = pd.read_csv('file.csv', encoding='utf-8')

# For Excel
df = pd.read_excel('file.xlsx', engine='openpyxl')
```

**Writing files**:
```python
df.to_csv('output.csv', encoding='utf-8', index=False)
```

**PDF generation**:
- Use CSS fonts that support Japanese: `font-family: 'Noto Sans JP', sans-serif;`
- Ensure HTML has `<meta charset="UTF-8">`

---

## Development Workflow

### Starting Fresh
1. **Phase 1**: Create all documentation in `docs/` folder
2. **Phase 2**: Build data pipeline, create processed datasets, write tests
3. **Phase 3**: Analyze data, create visualizations, write Markdown report
4. **Phase 4**: Generate PDFs from Markdown

### Resuming Work
Check which phase is complete by looking for deliverables:
- Phase 1 complete: `docs/` has 5 MD files
- Phase 2 complete: `data/processed/` has clean CSVs, tests pass
- Phase 3 complete: `reports/analysis_report.md` exists with images
- Phase 4 complete: Both PDF files exist in `reports/`

### Code Quality Standards
- Follow PEP 8 (use `black` for formatting)
- Docstrings for all functions (Google style)
- Type hints for function parameters
- Meaningful variable names
- Comments for complex logic

---

## Success Criteria

**Project is complete when**:
1. All 4 phases executed with deliverables
2. `reports/detailed_report.pdf` - Professional A4 report (20-30 pages)
3. `reports/executive_slides.pdf` - Presentation slides (10-15 slides)
4. All code is clean, commented, and tested
5. Insights are meaningful and actionable
6. Documentation is comprehensive

**Quality Benchmarks**:
- Zero test failures in `pytest tests/`
- No missing values in key fields of processed data
- At least 5 distinct insights in analysis
- All visualizations are high-quality PNGs (300 DPI)
- PDFs are professionally formatted

---

## Tips for Claude Code Execution

1. **Execute phases sequentially** - Each phase depends on previous outputs
2. **Adopt the persona** for each phase (PM → DE → DA → RS)
3. **Validate deliverables** using the checklists before proceeding
4. **Make data realistic** - Add intentional patterns (seasonality, store differences)
5. **Focus on insights** - Analysis should tell a story, not just show numbers
6. **Professional output** - PDFs should be suitable for executive presentation
7. **Handle edge cases** - Missing data, encoding issues, file format differences

---

## Common Pitfalls to Avoid

- **Don't skip phases** - Each phase builds on previous work
- **Don't ignore Japanese encoding** - Always use UTF-8
- **Don't create generic insights** - Make them specific to the data patterns
- **Don't generate low-quality PDFs** - Test formatting and readability
- **Don't forget data validation** - Always run tests after data pipeline
- **Don't hard-code values** - Use configuration or calculate dynamically

---

## Quick Start

### Option 1: Using Sub-Agents (Recommended)

```bash
# 1. Create directory structure
mkdir -p docs data/processed src/{data_pipeline,analysis,reporting/templates} reports/assets notebooks tests

# 2. Install dependencies
pip install pandas numpy matplotlib seaborn plotly weasyprint markdown pytest jupyter openpyxl --break-system-packages

# 3. Launch Phase 1 agent
# Tell Claude: "Launch the project-manager-planner agent to start Phase 1"

# 4. After Phase 1 complete, launch Phase 2
# Tell Claude: "Launch the data-engineer agent to start Phase 2"

# 5. After Phase 2 complete, launch Phase 3
# Tell Claude: "Launch the data-analyst agent to start Phase 3"

# 6. After Phase 3 complete, launch Phase 4
# Tell Claude: "Launch the pdf-reporting-specialist agent to complete Phase 4"
```

### Option 2: Manual Execution

Follow the detailed phase instructions in sections above and execute tasks manually without using sub-agents.

---

## Agent Execution Guidelines

When using sub-agents, Claude Code will:

1. **Automatically adopt the correct persona** for each phase
2. **Execute all tasks** defined in that phase autonomously
3. **Validate deliverables** before completing
4. **Report completion status** and hand off to next phase

**User Responsibilities**:
- Launch agents in the correct order (Phase 1 → 2 → 3 → 4)
- Wait for each phase to complete before launching the next
- Review deliverables between phases if desired
- Provide feedback or request modifications as needed

**Agent Responsibilities**:
- Complete all tasks defined in their phase
- Create all required files and documentation
- Ensure quality standards are met
- Prepare outputs for the next phase
