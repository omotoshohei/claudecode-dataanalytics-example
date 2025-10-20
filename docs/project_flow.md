# Project Flow Document
## Multi-Store Fashion Retail Sales Analysis

**Version**: 1.0
**Date**: October 2025

---

## 1. Overview

This document defines the overall workflow for the Multi-Store Sales Analysis project. The project follows a **4-phase sequential approach**, where each phase must be completed before the next begins.

---

## 2. High-Level Project Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     PROJECT LIFECYCLE                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: PROJECT MANAGEMENT                                     │
│ Agent: project-manager-planner                                  │
│                                                                 │
│ Input:  Business requirements from stakeholders                │
│ Output: 5 planning documents (requirements, flow, WBS, etc.)   │
│ Duration: 1-2 days                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: DATA ENGINEERING                                       │
│ Agent: data-engineer                                            │
│                                                                 │
│ Input:  10 raw store files + data requirements                 │
│ Output: Clean datasets + data pipeline + tests + dictionary    │
│ Duration: 2-3 days                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: DATA ANALYSIS                                          │
│ Agent: data-analyst                                             │
│                                                                 │
│ Input:  Processed datasets + requirements                       │
│ Output: EDA notebook + visualizations + Markdown report        │
│ Duration: 3-4 days                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: PDF REPORTING                                          │
│ Agent: pdf-reporting-specialist                                 │
│                                                                 │
│ Input:  analysis_report.md + visualizations                     │
│ Output: detailed_report.pdf + executive_slides.pdf             │
│ Duration: 1-2 days                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT COMPLETE                             │
│ Deliverables: 2 executive-ready PDFs + reusable code           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Phase Workflows

### Phase 1: Project Management

**Agent**: `project-manager-planner`

**Purpose**: Establish project foundation through comprehensive planning

**Input Dependencies**:
- Business requirements from stakeholders
- Data file inventory (10 store files)
- Executive audience definition

**Workflow**:
```
1. Gather requirements from stakeholders
   └─> Identify key business questions
   └─> Define success criteria
   └─> Clarify scope and constraints

2. Create requirements.md
   └─> Document objectives, stakeholders, scope

3. Create project_flow.md (this document)
   └─> Define 4-phase workflow

4. Create wbs.md
   └─> Break down all tasks by phase
   └─> Estimate effort

5. Create data_requirements.md
   └─> Specify expected data fields
   └─> Define quality standards

6. Create success_criteria.md
   └─> Define measurable outcomes
   └─> Set quality benchmarks
```

**Output Deliverables**:
- ✅ `docs/requirements.md`
- ✅ `docs/project_flow.md`
- ✅ `docs/wbs.md`
- ✅ `docs/data_requirements.md`
- ✅ `docs/success_criteria.md`

**Exit Criteria**: All 5 planning documents created and reviewed

---

### Phase 2: Data Engineering

**Agent**: `data-engineer`

**Purpose**: Build reliable, clean datasets from raw store data

**Input Dependencies**:
- Raw data files: `data/01_渋谷店_売上_202401.xlsx` ... `10_福岡店_売上_202401_済.xlsx`
- `docs/data_requirements.md` (specifications)
- `docs/requirements.md` (business context)

**Workflow**:
```
1. Explore raw data files
   └─> Understand schemas across 10 files
   └─> Identify data quality issues
   └─> Note encoding requirements (Japanese text)

2. Build data pipeline (src/data_pipeline/)
   └─> loader.py: Read Excel/CSV with UTF-8 support
   └─> cleaner.py: Standardize schemas, handle nulls, fix types
   └─> validator.py: Implement quality checks

3. Generate processed datasets (data/processed/)
   └─> sales_clean.csv: Unified transaction data
   └─> stores.csv: Store metadata (ID, name, region, location)
   └─> products.csv: Product categories

4. Create data quality tests
   └─> tests/test_data_quality.py with pytest

5. Document data
   └─> docs/data_dictionary.md
```

**Output Deliverables**:
- ✅ `src/data_pipeline/loader.py`
- ✅ `src/data_pipeline/cleaner.py`
- ✅ `src/data_pipeline/validator.py`
- ✅ `data/processed/sales_clean.csv`
- ✅ `data/processed/stores.csv`
- ✅ `data/processed/products.csv`
- ✅ `tests/test_data_quality.py`
- ✅ `docs/data_dictionary.md`

**Quality Gates**:
- All pytest tests pass (zero failures)
- No missing values in critical fields (date, store_id, sales_amount)
- All sales amounts >= 0
- Dates within January 2024
- Consistent store IDs

**Exit Criteria**: Clean datasets available + all tests passing + data documented

---

### Phase 3: Data Analysis

**Agent**: `data-analyst`

**Purpose**: Extract insights and create comprehensive analysis report

**Input Dependencies**:
- `data/processed/sales_clean.csv`
- `data/processed/stores.csv`
- `data/processed/products.csv`
- `docs/requirements.md` (business questions)
- `docs/success_criteria.md` (insight targets)

**Workflow**:
```
1. Exploratory Data Analysis (notebooks/eda.ipynb)
   └─> Load processed datasets
   └─> Statistical summaries
   └─> Initial visualizations
   └─> Pattern discovery

2. Create analysis functions (src/analysis/)
   └─> metrics.py: KPI calculations (revenue, growth, traffic)
   └─> visualizations.py: Reusable chart functions

3. Generate visualizations (reports/assets/)
   └─> Sales trend over time (line chart)
   └─> Store performance by region (bar chart)
   └─> Product category breakdown (bar/pie chart)
   └─> Day-of-week patterns (heatmap)
   └─> Seasonal patterns (line/area chart)
   └─> YoY growth comparison (if data available)
   └─> Customer traffic patterns
   └─> Regional comparison

4. Write Markdown report (reports/analysis_report.md)
   └─> Executive Summary (3-5 key findings)
   └─> Project Overview
   └─> Data Overview
   └─> Key Findings (with embedded images)
   └─> Detailed Analysis
   └─> Recommendations for Q2 2024
   └─> Regional expansion insights
   └─> Store benchmarking results
   └─> Next Steps
```

**Output Deliverables**:
- ✅ `notebooks/eda.ipynb`
- ✅ `src/analysis/metrics.py`
- ✅ `src/analysis/visualizations.py`
- ✅ `reports/assets/*.png` (8+ visualization files)
- ✅ `reports/analysis_report.md`

**Quality Gates**:
- Minimum 5 distinct, actionable insights
- All insights backed by data evidence
- 3-5 key findings highlighted for executives
- All charts high-quality (300 DPI)
- Report tells a clear story

**Exit Criteria**: Comprehensive Markdown report completed with all visualizations

---

### Phase 4: PDF Reporting

**Agent**: `pdf-reporting-specialist`

**Purpose**: Transform Markdown analysis into executive-ready PDF documents

**Input Dependencies**:
- `reports/analysis_report.md`
- `reports/assets/*.png` (all visualizations)
- `docs/requirements.md` (audience: C-level executives)

**Workflow**:
```
1. Create PDF generation scripts (src/reporting/)
   └─> md_to_pdf_detailed.py: A4 portrait report
   └─> md_to_pdf_slides.py: 16:9 landscape slides
   └─> templates/detailed_report.css: Professional styling
   └─> templates/slides.css: Presentation styling

2. Generate detailed report
   └─> Convert analysis_report.md to PDF
   └─> Apply professional formatting
   └─> Ensure Japanese text renders correctly
   └─> Add page breaks at sections
   └─> Verify image quality
   └─> Output: reports/detailed_report.pdf (20-30 pages)

3. Generate executive slides
   └─> Extract key points from analysis_report.md
   └─> Create slide-format PDF
   └─> Emphasize visuals over text
   └─> Structure: Title → Summary → Findings → Recommendations
   └─> Output: reports/executive_slides.pdf (10-15 slides)

4. Create reporting guide
   └─> docs/reporting_guide.md
   └─> Document regeneration process
   └─> Troubleshooting tips
```

**Output Deliverables**:
- ✅ `src/reporting/md_to_pdf_detailed.py`
- ✅ `src/reporting/md_to_pdf_slides.py`
- ✅ `src/reporting/templates/detailed_report.css`
- ✅ `src/reporting/templates/slides.css`
- ✅ `reports/detailed_report.pdf` (A4 portrait, 20-30 pages)
- ✅ `reports/executive_slides.pdf` (16:9 landscape, 10-15 slides)
- ✅ `docs/reporting_guide.md`

**Quality Gates**:
- Both PDFs professionally formatted
- Japanese text renders correctly
- Images high-quality and properly embedded
- Suitable for executive presentation
- No formatting errors

**Exit Criteria**: Both PDF deliverables complete and presentation-ready

---

## 4. Phase Dependencies

```
Phase 1 (Planning)
    └─ MUST COMPLETE before Phase 2
       ↓
Phase 2 (Data Engineering)
    └─ MUST COMPLETE before Phase 3
       ↓
Phase 3 (Data Analysis)
    └─ MUST COMPLETE before Phase 4
       ↓
Phase 4 (PDF Reporting)
    └─ PROJECT COMPLETE
```

**Critical Path**:
- No phase can start until previous phase completes
- Each phase builds on deliverables from previous phase
- Quality gates must pass before phase transition

---

## 5. Data Flow

```
Raw Data (10 Excel/CSV files)
    ↓
[Phase 2: Data Engineering]
    ↓
Processed CSVs (sales_clean, stores, products)
    ↓
[Phase 3: Data Analysis]
    ↓
Markdown Report + PNG Visualizations
    ↓
[Phase 4: PDF Reporting]
    ↓
Final PDFs (detailed + slides)
```

---

## 6. Communication & Handoffs

### Phase 1 → Phase 2 Handoff
**What**: Complete planning documentation
**Artifacts**: 5 MD files in `docs/`
**Validation**: All planning documents reviewed and approved

### Phase 2 → Phase 3 Handoff
**What**: Clean, validated datasets
**Artifacts**: 3 CSV files in `data/processed/`, passing tests
**Validation**: All data quality tests pass, data dictionary complete

### Phase 3 → Phase 4 Handoff
**What**: Complete Markdown analysis report with visualizations
**Artifacts**: `analysis_report.md` + PNG files in `reports/assets/`
**Validation**: Report has 5+ insights, all visualizations generated

### Phase 4 → Completion
**What**: Executive-ready PDF deliverables
**Artifacts**: 2 PDF files in `reports/`
**Validation**: Both PDFs professionally formatted and presentation-ready

---

## 7. Recurring Analysis Framework

This project establishes a **repeatable framework** for monthly/quarterly analysis:

```
Month N Analysis:
1. Update raw data files in data/ directory
2. Run data pipeline: python src/data_pipeline/loader.py
3. Run tests: pytest tests/
4. Run analysis: Open notebooks/eda.ipynb, update analysis
5. Update reports/analysis_report.md
6. Regenerate PDFs: python src/reporting/md_to_pdf_detailed.py

→ New PDFs ready for executive review
```

---

## 8. Success Metrics

**Project succeeds when**:
- ✅ All 4 phases completed
- ✅ 2 executive-ready PDFs delivered
- ✅ All code tested and documented
- ✅ Minimum 5 actionable insights identified
- ✅ Framework established for recurring analysis

---

## 9. Risk Management

### Phase Transition Risks
- **Risk**: Incomplete deliverables from previous phase
- **Mitigation**: Quality gates enforced at each phase exit

### Data Quality Risks
- **Risk**: Poor quality input data affects all downstream phases
- **Mitigation**: Comprehensive validation in Phase 2

### Timeline Risks
- **Risk**: Phase delays cascade to later phases
- **Mitigation**: Clear exit criteria, focused scope

---

## 10. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | Oct 2025 | Initial version | Project Manager |

---

*This project flow guides the execution of all 4 phases to deliver executive-ready sales analysis.*
