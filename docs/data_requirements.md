# Data Requirements Specification
## Multi-Store Fashion Retail Sales Analysis

**Version**: 1.0
**Date**: October 2025

---

## 1. Overview

This document specifies the data requirements for the Multi-Store Sales Analysis project, including expected schemas, quality standards, and validation rules.

---

## 2. Data Sources

### 2.1 Raw Data Files

**Location**: `data/` directory
**File Count**: 10 files (one per store)
**Time Period**: January 2024
**Formats**: Microsoft Excel (.xlsx) and CSV

| Store | File Name | Format | Region |
|-------|-----------|--------|--------|
| Shibuya | 01_渋谷店_売上_202401.xlsx | Excel | Kanto |
| Shinjuku | 02_新宿店_売上_202401.xlsx | Excel | Kanto |
| Ikebukuro | 03_池袋店_sales_202401.csv | CSV | Kanto |
| Yokohama | 04_横浜店_売上_202401_最終.xlsx | Excel | Kanto |
| Osaka | 05_大阪店_売上_202401.csv | CSV | Kansai |
| Sapporo | 06_札幌_売上202401.xlsx | Excel | Hokkaido |
| Sendai | 07_仙台店売上(1月).xlsx | Excel | Tohoku |
| Nagoya | 08_名古屋店_202401_売上.xlsx | Excel | Chubu |
| Hiroshima | 09_広島店_売上_2024_01.csv | CSV | Chugoku |
| Fukuoka | 10_福岡店_売上_202401_済.xlsx | Excel | Kyushu |

**Known Issues**:
- Inconsistent file naming conventions
- Mixed file formats (Excel and CSV)
- Japanese characters in file names and content
- Potentially different schemas across files

---

## 3. Expected Data Schema

### 3.1 Sales Transaction Data

**Expected Fields** (Raw Data):

| Field Name (EN) | Field Name (JP) | Data Type | Required | Description |
|-----------------|-----------------|-----------|----------|-------------|
| transaction_id | 取引ID | String/Integer | Yes | Unique transaction identifier |
| date | 日付 | Date | Yes | Transaction date (YYYY-MM-DD) |
| store_id | 店舗ID | String/Integer | Yes | Store identifier |
| store_name | 店舗名 | String | No | Store name (Japanese) |
| product_category | 商品カテゴリ | String | Yes | Product category |
| product_name | 商品名 | String | No | Product name (Japanese) |
| sales_amount | 売上金額 | Float | Yes | Sales amount in JPY |
| quantity | 数量 | Integer | No | Quantity sold |
| customer_count | 来店客数 | Integer | No | Number of customers |
| payment_method | 支払方法 | String | No | Payment method |
| day_of_week | 曜日 | String | No | Day of week |

**Notes**:
- Field names may vary across files
- Some files may use English, others Japanese
- Data engineer must standardize during cleaning

### 3.2 Store Metadata

**To Be Created** by Data Engineer in `data/processed/stores.csv`:

| Field Name | Data Type | Required | Description |
|------------|-----------|----------|-------------|
| store_id | String | Yes | Unique store identifier (S01-S10) |
| store_name_jp | String | Yes | Store name in Japanese |
| store_name_en | String | Yes | Store name in English |
| city | String | Yes | City location |
| region | String | Yes | Geographic region |
| opening_date | Date | No | Store opening date |
| store_size_sqm | Integer | No | Floor space in square meters |

**Store Information**:

| Store ID | Japanese Name | English Name | City | Region |
|----------|--------------|--------------|------|--------|
| S01 | 渋谷店 | Shibuya | Tokyo | Kanto |
| S02 | 新宿店 | Shinjuku | Tokyo | Kanto |
| S03 | 池袋店 | Ikebukuro | Tokyo | Kanto |
| S04 | 横浜店 | Yokohama | Yokohama | Kanto |
| S05 | 大阪店 | Osaka | Osaka | Kansai |
| S06 | 札幌店 | Sapporo | Sapporo | Hokkaido |
| S07 | 仙台店 | Sendai | Sendai | Tohoku |
| S08 | 名古屋店 | Nagoya | Nagoya | Chubu |
| S09 | 広島店 | Hiroshima | Hiroshima | Chugoku |
| S10 | 福岡店 | Fukuoka | Fukuoka | Kyushu |

### 3.3 Product Category Data

**To Be Created** by Data Engineer in `data/processed/products.csv`:

| Field Name | Data Type | Required | Description |
|------------|-----------|----------|-------------|
| category_id | String | Yes | Unique category identifier |
| category_name_jp | String | Yes | Category name in Japanese |
| category_name_en | String | Yes | Category name in English |
| category_type | String | No | Type (Men's, Women's, Accessories, etc.) |

**Expected Categories** (Fashion Retail):
- Women's Apparel (レディース)
- Men's Apparel (メンズ)
- Accessories (アクセサリー)
- Footwear (シューズ)
- Bags (バッグ)
- Seasonal Items (季節商品)
- Sale Items (セール商品)

---

## 4. Processed Data Schema

### 4.1 sales_clean.csv

**Purpose**: Unified, cleaned sales transaction data from all 10 stores

| Field Name | Data Type | Required | Constraints | Description |
|------------|-----------|----------|-------------|-------------|
| transaction_id | String | Yes | Unique | Unique transaction ID |
| date | Date | Yes | 2024-01-01 to 2024-01-31 | Transaction date |
| store_id | String | Yes | S01-S10 | Store identifier |
| product_category | String | Yes | Not null | Standardized category |
| sales_amount | Float | Yes | >= 0 | Sales in JPY |
| quantity | Integer | No | >= 0 | Quantity sold |
| customer_count | Integer | No | >= 0 | Customer traffic |
| day_of_week | String | Yes | Mon-Sun | Day of week |
| day_of_month | Integer | Yes | 1-31 | Day of month |
| is_weekend | Boolean | Yes | True/False | Weekend flag |
| week_of_month | Integer | Yes | 1-5 | Week number in month |

**Row Count**: Estimated 50,000-200,000 transactions (5,000-20,000 per store)

**Encoding**: UTF-8
**Format**: CSV with header
**Delimiter**: Comma (,)

### 4.2 stores.csv

**Purpose**: Store metadata for analysis grouping

| Field Name | Data Type | Required | Description |
|------------|-----------|----------|-------------|
| store_id | String | Yes | S01-S10 |
| store_name_jp | String | Yes | Japanese name |
| store_name_en | String | Yes | English name |
| city | String | Yes | City location |
| region | String | Yes | Geographic region |

**Row Count**: 10 rows (one per store)

### 4.3 products.csv

**Purpose**: Product category reference data

| Field Name | Data Type | Required | Description |
|------------|-----------|----------|-------------|
| category_id | String | Yes | Unique ID |
| category_name_jp | String | Yes | Japanese name |
| category_name_en | String | Yes | English name |

**Row Count**: 7-10 rows (one per category)

---

## 5. Data Quality Standards

### 5.1 Completeness

**Critical Fields** (No Missing Values Allowed):
- ✅ transaction_id
- ✅ date
- ✅ store_id
- ✅ product_category
- ✅ sales_amount
- ✅ day_of_week

**Optional Fields** (Missing Values Acceptable):
- quantity
- customer_count
- payment_method

**Target**: 100% completeness for critical fields

### 5.2 Accuracy

**Date Validation**:
- All dates must be within January 2024 (2024-01-01 to 2024-01-31)
- No future dates
- No dates before 2024-01-01

**Amount Validation**:
- sales_amount >= 0 (no negative sales)
- sales_amount <= 1,000,000 (flag outliers above 1M JPY)
- Reasonable distribution (log-normal expected)

**Store ID Validation**:
- All store_id values must match entries in stores.csv
- Only S01 through S10 allowed
- No orphaned store references

**Category Validation**:
- All product_category values must be standardized
- Map to category_id in products.csv

### 5.3 Consistency

**Encoding Consistency**:
- All Japanese text in UTF-8
- No encoding errors or mojibake (文字化け)

**Formatting Consistency**:
- Date format: YYYY-MM-DD
- Currency: No currency symbols, numeric only
- Store IDs: Consistent format (S01, S02, etc.)

**Schema Consistency**:
- All 10 files must map to unified schema
- Column names standardized
- Data types consistent

### 5.4 Uniqueness

**Transaction IDs**:
- Each transaction_id must be unique across all stores
- If duplicates found, create composite key: store_id + local_transaction_id

### 5.5 Timeliness

**Data Freshness**:
- January 2024 data (historical analysis)
- Data assumed complete for the full month

---

## 6. Data Validation Rules

### 6.1 Mandatory Validations

The data pipeline MUST implement these checks:

```python
# Validation Rule 1: No nulls in critical fields
assert sales_clean['date'].notna().all()
assert sales_clean['store_id'].notna().all()
assert sales_clean['sales_amount'].notna().all()

# Validation Rule 2: Sales amounts non-negative
assert (sales_clean['sales_amount'] >= 0).all()

# Validation Rule 3: Dates within January 2024
assert sales_clean['date'].min() >= pd.Timestamp('2024-01-01')
assert sales_clean['date'].max() <= pd.Timestamp('2024-01-31')

# Validation Rule 4: Valid store IDs
valid_stores = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10']
assert sales_clean['store_id'].isin(valid_stores).all()

# Validation Rule 5: Consistent data types
assert sales_clean['date'].dtype == 'datetime64[ns]'
assert sales_clean['sales_amount'].dtype == 'float64'
```

### 6.2 Warning-Level Checks

Generate warnings (but don't fail) for:
- Sales amounts > 1,000,000 JPY (outliers)
- Days with zero transactions for any store
- Unusual category distributions

---

## 7. Data Transformations Required

### 7.1 Column Standardization

| Original (Various) | Standardized |
|-------------------|--------------|
| 日付, date, 取引日 | date |
| 店舗ID, store_id, shop_id | store_id |
| 売上金額, 売上, sales_amount, amount | sales_amount |
| 商品カテゴリ, category, カテゴリー | product_category |

### 7.2 Data Type Conversions

- Dates: Convert all to pandas datetime64
- Sales amounts: Convert to float64
- Store IDs: Convert to string
- Quantities: Convert to int64 (nullable)

### 7.3 Derived Fields

Create these calculated fields:
- day_of_week: Extract from date
- day_of_month: Extract from date
- is_weekend: Boolean (Saturday/Sunday = True)
- week_of_month: Calculate week number (1-5)

### 7.4 Category Mapping

Map various category names to standardized English categories:
- レディース → Women's Apparel
- メンズ → Men's Apparel
- アクセサリー → Accessories
- シューズ → Footwear
- バッグ → Bags
- 季節商品 → Seasonal
- セール商品 → Sale Items

---

## 8. Data Volume Estimates

| Dataset | Estimated Rows | Estimated Size |
|---------|---------------|----------------|
| sales_clean.csv | 50,000-200,000 | 5-20 MB |
| stores.csv | 10 | < 1 KB |
| products.csv | 7-10 | < 1 KB |

**Total**: ~5-20 MB for all processed data

---

## 9. Technical Requirements

### 9.1 Encoding
- **All files**: UTF-8 encoding
- **Japanese text**: Properly encoded, no mojibake
- **CSV delimiter**: Comma (,)
- **Line endings**: LF (Unix-style) preferred

### 9.2 Python Libraries
- pandas >= 1.3.0
- openpyxl >= 3.0.0 (for Excel reading)
- numpy >= 1.20.0

### 9.3 File Locations
- Raw data: `data/01_渋谷店_売上_202401.xlsx` etc.
- Processed data: `data/processed/`
- Pipeline code: `src/data_pipeline/`

---

## 10. Data Quality Testing

All tests in `tests/test_data_quality.py` must pass:

```python
def test_no_missing_critical_fields():
    """Ensure no nulls in date, store_id, sales_amount"""

def test_valid_date_range():
    """All dates within January 2024"""

def test_non_negative_sales():
    """All sales amounts >= 0"""

def test_valid_store_ids():
    """All store_ids in valid range (S01-S10)"""

def test_data_types():
    """Verify correct data types for all columns"""

def test_referential_integrity():
    """All store_ids exist in stores.csv"""
```

---

## 11. Historical Data (Optional)

If available, January 2023 data would enable:
- Year-over-year growth analysis
- Trend identification
- Performance change tracking

**Format**: Same schema as January 2024 data
**Priority**: Nice to have, not required

---

## 12. Data Ownership

- **Raw Data**: Provided by individual stores
- **Processed Data**: Created by Data Engineer
- **Responsibility**: Data Engineer ensures quality and compliance with this spec

---

## 13. Compliance Notes

- All data is internal business data (not customer PII)
- No personal information (names, emails, phone numbers) in scope
- Financial data (sales amounts) is aggregated transaction-level only
- Japanese language data handled with proper encoding

---

*This data requirements specification guides the Data Engineer in Phase 2.*
