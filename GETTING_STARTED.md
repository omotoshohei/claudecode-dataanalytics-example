# Getting Started Guide
## Multi-Store Fashion Retail Sales Analysis

**Quick Start**: 5 minutes to explore the results
**Full Setup**: 15-30 minutes to run analysis yourself

---

## 🎯 For Executives (5 Minutes)

If you just want to **see the results**, skip to the deliverables:

### Main Deliverables

1. **📊 Detailed Analysis Report**
   - **Location**: `reports/detailed_report.pdf`
   - **Size**: 1.6 MB
   - **Format**: A4 portrait (20-30 pages)
   - **Best for**: Deep dive, strategic planning, board meetings

2. **📊 Executive Summary Slides**
   - **Location**: `reports/executive_slides.pdf`
   - **Size**: 1.3 MB
   - **Format**: 16:9 landscape presentation
   - **Best for**: Quick overview, C-level presentations

### How to View
**On macOS**:
```bash
open reports/detailed_report.pdf
open reports/executive_slides.pdf
```

**On Windows**:
```bash
start reports\detailed_report.pdf
start reports\executive_slides.pdf
```

**Or**: Simply navigate to the `reports/` folder and double-click the PDF files.

---

## 📊 For Analysts (15-30 Minutes)

If you want to **explore the data and analysis**:

### Step 1: Check the Analysis Notebook
```bash
jupyter notebook notebooks/eda_executed.ipynb
```

This notebook contains:
- All exploratory data analysis
- Statistical summaries
- Visualization code
- Insights discovery process

### Step 2: Review the Clean Data
The processed datasets are ready to use:
```python
import pandas as pd

# Load clean sales data
sales = pd.read_csv('data/processed/sales_clean.csv')
stores = pd.read_csv('data/processed/stores.csv')
products = pd.read_csv('data/processed/products.csv')

# Quick overview
print(f"Total transactions: {len(sales)}")
print(f"Total revenue: ¥{sales['sales_amount'].sum():,.0f}")
print(f"Date range: {sales['date'].min()} to {sales['date'].max()}")
```

### Step 3: Explore Visualizations
All charts are available in `reports/assets/`:
- daily_revenue_trend.png
- revenue_by_store.png
- revenue_by_region.png
- revenue_by_category.png
- revenue_by_day_of_week.png
- weekend_vs_weekday.png
- category_mix_by_store.png
- top_bottom_stores.png

### Step 4: Read the Markdown Report
For the full narrative with embedded charts:
```bash
# macOS
open reports/analysis_report.md

# Or use any Markdown viewer
```

---

## 💻 For Developers (Full Setup)

If you want to **run the analysis yourself** or **modify the code**:

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (optional, for version control)

### Installation

**Step 1: Install Python Dependencies**
```bash
pip install -r requirements.txt
```

For macOS users (if you get permission errors):
```bash
pip install -r requirements.txt --break-system-packages
```

This installs:
- pandas, numpy (data processing)
- matplotlib, seaborn (visualization)
- openpyxl (Excel support)
- weasyprint, markdown (PDF generation)
- pytest (testing)
- jupyter (notebooks)

**Step 2: Verify Installation**
```bash
python -c "import pandas; import matplotlib; print('✅ All dependencies installed')"
```

### Running the Analysis

#### Option A: Run Full Pipeline (Recommended)

**1. Generate Clean Data**
```bash
python src/data_pipeline/generate_processed_data.py
```

Expected output:
```
✅ Loaded 1,279 raw transactions
✅ Generated 928 clean transactions
✅ Created sales_clean.csv, stores.csv, products.csv
```

**2. Run Data Quality Tests**
```bash
pytest tests/test_data_quality.py -v
```

Expected output:
```
16 tests passed in 0.5s ✅
```

**3. Explore Data Interactively**
```bash
jupyter notebook notebooks/eda.ipynb
```

This opens an interactive notebook where you can:
- Modify analyses
- Create new visualizations
- Test hypotheses
- Export results

**4. Generate PDF Reports**
```bash
# Generate detailed report
python src/reporting/md_to_pdf_detailed.py

# Generate executive slides
python src/reporting/md_to_pdf_slides.py
```

PDFs will be created in `reports/` directory.

#### Option B: Use Existing Results

Everything is already generated, so you can skip the pipeline and just explore:

```bash
# Start Jupyter
jupyter notebook

# Navigate to notebooks/eda_executed.ipynb
# All outputs are already there!
```

---

## 📚 Understanding the Project Structure

### Key Directories

| Directory | Purpose | Files |
|-----------|---------|-------|
| **data/raw/** | Original store files | 10 Excel/CSV files |
| **data/processed/** | Clean datasets | 3 CSV files |
| **docs/** | Documentation | 7 planning docs |
| **notebooks/** | Interactive analysis | 2 Jupyter notebooks |
| **src/data_pipeline/** | Data engineering code | 5 Python files |
| **src/analysis/** | Analysis functions | 3 Python files |
| **src/reporting/** | PDF generation | 2 scripts + 2 CSS |
| **reports/** | Final outputs | 2 PDFs + 8 charts |
| **tests/** | Quality tests | 1 test file (16 tests) |

### Key Files

| File | Description |
|------|-------------|
| **README.md** | Main project documentation (start here) |
| **PROJECT_SUMMARY.md** | Executive summary of entire project |
| **GETTING_STARTED.md** | This file - how to use the project |
| **CLAUDE.md** | Instructions for Claude Code agents |
| **requirements.txt** | Python dependencies |
| **.gitignore** | Git ignore rules |

---

## 🔧 Common Tasks

### Task 1: Update Analysis for New Month

When you have February 2024 data:

```bash
# 1. Add new data files to data/raw/
cp new_february_files/*.xlsx data/raw/

# 2. Regenerate clean data
python src/data_pipeline/generate_processed_data.py

# 3. Run tests
pytest tests/ -v

# 4. Update notebook
jupyter notebook notebooks/eda.ipynb
# Change date filter from January to February

# 5. Update report
# Edit reports/analysis_report.md with February insights

# 6. Regenerate PDFs
python src/reporting/md_to_pdf_detailed.py
python src/reporting/md_to_pdf_slides.py
```

**Time**: 2-4 hours for recurring monthly analysis

### Task 2: Customize Visualizations

```python
# Use the analysis functions
from src.analysis import visualizations

# Create custom chart
fig = visualizations.create_store_comparison(
    sales_df,
    metric='revenue',
    title='My Custom Title'
)
fig.savefig('reports/assets/my_chart.png', dpi=300, bbox_inches='tight')
```

### Task 3: Calculate Custom Metrics

```python
# Use the metrics functions
from src.analysis import metrics

# Calculate custom KPI
weekend_revenue = metrics.calculate_weekend_revenue(sales_df)
print(f"Weekend revenue: ¥{weekend_revenue:,.0f}")
```

### Task 4: Regenerate PDFs with Changes

After modifying `reports/analysis_report.md`:

```bash
# Regenerate both PDFs
python src/reporting/md_to_pdf_detailed.py
python src/reporting/md_to_pdf_slides.py

# Check results
open reports/detailed_report.pdf
```

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors
**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "WeasyPrint error: Failed to load font"
**Solution** (for Japanese text on macOS):
```bash
# Install Japanese fonts
brew install font-noto-sans-jp

# Or download from Google Fonts
```

### Issue: "Jupyter kernel not found"
**Solution**:
```bash
python -m ipykernel install --user
```

### Issue: "Permission denied" when installing packages
**Solution** (macOS):
```bash
pip install -r requirements.txt --break-system-packages
# or
pip install -r requirements.txt --user
```

### Issue: CSV encoding errors
**Solution**: The pipeline auto-detects encoding (UTF-8, Shift-JIS). If you still have issues:
```python
import pandas as pd
df = pd.read_csv('file.csv', encoding='utf-8', errors='replace')
```

### Issue: Tests failing
**Solution**:
```bash
# See detailed test output
pytest tests/ -v --tb=short

# Run specific test
pytest tests/test_data_quality.py::test_no_missing_critical_fields -v
```

---

## 📖 Learning Path

**For Beginners**:
1. Read `README.md` (project overview)
2. Open `reports/detailed_report.pdf` (see results)
3. Read `reports/analysis_report.md` (understand methodology)
4. Open `notebooks/eda_executed.ipynb` (see code with outputs)

**For Intermediate**:
1. Review `docs/requirements.md` (understand business context)
2. Read `src/data_pipeline/README.md` (data engineering approach)
3. Explore `src/analysis/metrics.py` (KPI calculations)
4. Modify `notebooks/eda.ipynb` (create your own analysis)

**For Advanced**:
1. Study `docs/project_flow.md` (4-phase methodology)
2. Review all `src/` code (implementation details)
3. Run `pytest tests/ -v` (understand quality gates)
4. Customize for your own use case

---

## 🚀 Next Steps

### For Executives
1. ✅ Review `reports/detailed_report.pdf`
2. ✅ Present `reports/executive_slides.pdf` to stakeholders
3. ✅ Prioritize Q2 2024 recommendations
4. ✅ Allocate budget for implementation

### For Analysts
1. ✅ Explore `notebooks/eda_executed.ipynb`
2. ✅ Review calculation methodology in `src/analysis/`
3. ✅ Plan monthly recurring analysis
4. ✅ Identify additional metrics to track

### For Developers
1. ✅ Review code in `src/` directories
2. ✅ Run tests: `pytest tests/ -v`
3. ✅ Understand pipeline architecture
4. ✅ Adapt for your use case

---

## 💡 Pro Tips

**Tip 1**: Use the reusable functions
```python
# Don't reinvent the wheel
from src.analysis import metrics, visualizations

revenue = metrics.calculate_total_revenue_by_store(sales_df)
chart = visualizations.create_store_comparison(sales_df)
```

**Tip 2**: Check data quality frequently
```bash
# Run tests after any data changes
pytest tests/ -v
```

**Tip 3**: Keep documentation updated
When you modify analysis, update:
- `reports/analysis_report.md`
- Docstrings in Python code
- Comments explaining complex logic

**Tip 4**: Use version control
```bash
git add .
git commit -m "Updated analysis for February 2024"
```

---

## 📞 Getting Help

### Documentation
1. **README.md** - Main documentation
2. **PROJECT_SUMMARY.md** - High-level overview
3. **docs/** folder - Detailed specifications
4. **Code docstrings** - Function-level help

### Code Help
```python
# View function documentation
help(metrics.calculate_total_revenue_by_store)

# Or in Jupyter
?metrics.calculate_total_revenue_by_store
```

### File Locations
All key files are documented in `README.md` under "Project Structure"

---

## ✅ Quick Checklist

**I want to...**

- [ ] **See the results** → Open `reports/*.pdf`
- [ ] **Understand the methodology** → Read `reports/analysis_report.md`
- [ ] **Explore the data** → Open `notebooks/eda_executed.ipynb`
- [ ] **Run the analysis** → Follow "For Developers" section
- [ ] **Customize the analysis** → Modify `notebooks/eda.ipynb`
- [ ] **Update for new month** → Follow "Task 1: Update Analysis"
- [ ] **Create new charts** → Use `src/analysis/visualizations.py`
- [ ] **Calculate new metrics** → Use `src/analysis/metrics.py`
- [ ] **Regenerate PDFs** → Run `src/reporting/*.py` scripts
- [ ] **Understand business context** → Read `docs/requirements.md`

---

**Ready to get started?** Pick your path above and dive in! 🚀

---

*Last updated: October 19, 2025*
*Version: 1.0*
