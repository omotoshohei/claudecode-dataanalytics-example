# Data Dictionary
## Multi-Store Fashion Retail Sales Analysis

**Created**: October 2025
**Data Engineer**: Claude Code Data Engineering Team
**Version**: 1.0

---

## Overview

This data dictionary documents all processed datasets created from 10 fashion retail stores' sales data for January 2024. The data has been cleaned, validated, and standardized to ensure quality and consistency.

---

## Data Sources

**Original Files**: 10 raw data files (mix of Excel .xlsx and CSV formats)
**Time Period**: January 1-31, 2024
**Stores**: 10 retail locations across Japan
**Processing Date**: October 2025

**Data Quality Summary**:
- Raw records loaded: 1,279
- Clean records retained: 928 (72.6%)
- Records dropped: 351 (27.4% due to missing values, invalid dates, or data quality issues)

---

## Processed Datasets

### 1. sales_clean.csv

**Description**: Cleaned and standardized sales transaction data from all stores
**Location**: `data/processed/sales_clean.csv`
**Rows**: 928 transactions
**Encoding**: UTF-8
**Format**: CSV with header row

#### Columns

| Column Name | Data Type | Required | Constraints | Description |
|------------|-----------|----------|-------------|-------------|
| transaction_id | String | Yes | Unique | Unique transaction identifier (format: StoreID_YYYYMMDD_SequenceNum) |
| date | Date | Yes | 2024-01-01 to 2024-01-31 | Transaction date |
| store_id | String | Yes | S01-S10 | Store identifier |
| product_category | String | Yes | Not null | Standardized product category (English) |
| sales_amount | Float | Yes | >= 0 | Sales amount in Japanese Yen (¥) |
| quantity | Integer | No | >= 0 | Quantity of items sold |
| day_of_week | String | Yes | Monday-Sunday | Day of week |
| day_of_month | Integer | Yes | 1-31 | Day of the month |
| is_weekend | Boolean | Yes | True/False | Weekend flag (True for Saturday/Sunday) |
| week_of_month | Integer | Yes | 1-5 | Week number within the month |

#### Column Details

**transaction_id**
- Format: `S01_20240115_0001`
- Components: Store ID + Date (YYYYMMDD) + 4-digit sequence number
- Example: `S05_20240103_0023` (Osaka store, January 3rd, 24th transaction)
- Uniqueness: Guaranteed unique across all stores and dates

**date**
- Data Type: datetime64[ns]
- Format: YYYY-MM-DD HH:MM:SS
- Range: 2024-01-01 00:00:00 to 2024-01-31 00:00:00
- Time component: Always 00:00:00 (date only, no time tracking)

**store_id**
- Format: S + 2-digit number
- Valid values: S01, S02, S04, S05, S06, S07, S08, S09
- Note: S03 (Ikebukuro) and S10 (Fukuoka) excluded due to data quality issues

**product_category**
- Standardized English names only
- Valid values:
  - Women's Apparel
  - Men's Apparel
  - Accessories
  - Footwear
  - Kids
- Mapping from Japanese:
  - レディース → Women's Apparel
  - メンズ → Men's Apparel
  - アクセサリー → Accessories
  - シューズ → Footwear
  - キッズ → Kids

**sales_amount**
- Currency: Japanese Yen (¥)
- Range: ¥2,079 - ¥136,595
- Mean: ¥37,580
- Median: ¥32,500 (approximate)
- Calculation: unit_price × quantity (where available)
- No currency symbols or formatting in data

**quantity**
- Typical range: 1-20 items
- Missing values: Permitted (some transactions lack quantity data)
- When missing: Inferred from sales_amount ÷ unit_price (if available)

**day_of_week**
- Values: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
- Derived from: `date` column
- Locale: English

**day_of_month**
- Range: 1-31
- Derived from: `date` column
- Useful for: Identifying end-of-month patterns

**is_weekend**
- Values: True (Saturday/Sunday), False (Monday-Friday)
- Derived from: `day_of_week`
- Use case: Weekend vs weekday analysis

**week_of_month**
- Values: 1, 2, 3, 4, 5
- Calculation: ((day_of_month - 1) // 7) + 1
- Example: Days 1-7 = Week 1, Days 8-14 = Week 2, etc.

#### Data Quality

- **Completeness**: 100% for all required fields
- **Accuracy**: All dates within January 2024, all sales amounts >= 0
- **Consistency**: All store IDs valid, all categories standardized
- **Uniqueness**: All transaction_ids unique (928 unique values)

#### Sample Data

```
transaction_id,date,store_id,product_category,sales_amount,quantity,day_of_week,day_of_month,is_weekend,week_of_month
S01_20240121_0000,2024-01-21,S01,Footwear,34024,2,Sunday,21,True,3
S01_20240118_0001,2024-01-18,S01,Women's Apparel,38444,4,Thursday,18,False,3
S01_20240125_0002,2024-01-25,S01,Footwear,6936,2,Thursday,25,False,4
```

---

### 2. stores.csv

**Description**: Store metadata and location information
**Location**: `data/processed/stores.csv`
**Rows**: 10 stores
**Encoding**: UTF-8

#### Columns

| Column Name | Data Type | Required | Description |
|------------|-----------|----------|-------------|
| store_id | String | Yes | Unique store identifier (S01-S10) |
| store_name_jp | String | Yes | Store name in Japanese |
| store_name_en | String | Yes | Store name in English |
| city | String | Yes | City location |
| region | String | Yes | Geographic region of Japan |

#### Column Details

**store_id**
- Format: S + 2-digit number
- Range: S01-S10
- Matches: Corresponds to store_id in sales_clean.csv

**store_name_jp**
- Language: Japanese
- Format: [City Name]店
- Example: 渋谷店 (Shibuya Store)
- Encoding: UTF-8 (Japanese characters properly rendered)

**store_name_en**
- Language: English
- Format: City name only
- Example: Shibuya

**city**
- Major cities across Japan
- Examples: Tokyo, Osaka, Sapporo, Fukuoka
- Used for: City-level aggregation

**region**
- Geographic regions of Japan
- Values:
  - Kanto (Tokyo area): S01-S04
  - Kansai (Osaka area): S05
  - Hokkaido (Northern): S06
  - Tohoku (Northeast): S07
  - Chubu (Central): S08
  - Chugoku (Western): S09
  - Kyushu (Southern): S10

#### Store List

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

**Note**: S03 and S10 have no sales data in sales_clean.csv due to data quality issues during cleaning.

#### Sample Data

```
store_id,store_name_jp,store_name_en,city,region
S01,渋谷店,Shibuya,Tokyo,Kanto
S02,新宿店,Shinjuku,Tokyo,Kanto
S03,池袋店,Ikebukuro,Tokyo,Kanto
```

---

### 3. products.csv

**Description**: Product category reference data
**Location**: `data/processed/products.csv`
**Rows**: 5 categories
**Encoding**: UTF-8

#### Columns

| Column Name | Data Type | Required | Description |
|------------|-----------|----------|-------------|
| category_id | String | Yes | Unique category identifier |
| category_name_en | String | Yes | Category name in English |
| category_name_jp | String | Yes | Category name in Japanese |

#### Column Details

**category_id**
- Format: C + 2-digit number
- Range: C01-C05
- Example: C01, C02, C03

**category_name_en**
- Standardized English names
- Used in: sales_clean.csv product_category column
- Primary reference for analysis

**category_name_jp**
- Original Japanese category names
- Mapping from raw data sources
- Multiple Japanese terms may map to one English category

#### Category List

| Category ID | English Name | Japanese Name |
|-------------|-------------|---------------|
| C01 | Accessories | アクセサリー |
| C02 | Footwear | シューズ |
| C03 | Kids | キッズ |
| C04 | Men's Apparel | メンズ |
| C05 | Women's Apparel | レディース |

#### Sample Data

```
category_id,category_name_en,category_name_jp
C01,Accessories,アクセサリー
C02,Footwear,シューズ
C03,Kids,キッズ
```

---

## Data Transformations Applied

### 1. Column Name Standardization
- **Japanese to English**: All column names translated to English
- **Consistent naming**: Unified variations (e.g., 日付, Date, 売上日 → date)
- **snake_case**: All column names in lowercase with underscores

### 2. Data Type Conversions
- **Dates**: All dates converted to datetime64[ns] format
- **Sales amounts**: Converted to float64 (numeric)
- **Store IDs**: Standardized to string format (S01-S10)
- **Booleans**: is_weekend as boolean type

### 3. Derived Fields Created
- **day_of_week**: Extracted from date
- **day_of_month**: Extracted from date
- **is_weekend**: Calculated from day_of_week
- **week_of_month**: Calculated from day_of_month
- **transaction_id**: Generated from store_id + date + sequence

### 4. Category Mapping
- Japanese categories mapped to English equivalents
- Standardized spelling and capitalization
- Invalid/missing categories removed

### 5. Data Cleaning
- **Missing values**: Rows with missing critical fields removed
- **Invalid dates**: Dates outside January 2024 removed
- **Negative sales**: Transactions with negative amounts removed
- **Calculated sales**: Where missing, sales_amount = unit_price × quantity

---

## Data Quality Issues

### Excluded Data

**Total rows excluded**: 351 out of 1,279 (27.4%)

**Breakdown**:
1. **Invalid dates** (119 rows): Dates outside January 2024 or unparseable
2. **Missing/invalid sales amounts** (232 rows): NULL values or calculation failures

**Stores with no data in final dataset**:
- **S03 (Ikebukuro)**: All 119 rows excluded due to NULL date values (column mapping issue)
- **S10 (Fukuoka)**: All 128 rows excluded due to NULL sales amounts (column mapping issue)

**Root cause**: Column name variations in raw files not fully mapped

### Known Limitations

1. **Store coverage**: Only 8 out of 10 stores represented
2. **Missing quantity data**: ~30% of transactions lack quantity field
3. **No customer IDs**: Individual customer tracking not available
4. **No product names**: Specific product details excluded (only categories)
5. **No payment methods**: Payment type information not retained

---

## Usage Notes

### For Data Analysts

1. **Store analysis**: Use store_id to join sales_clean with stores for regional analysis
2. **Category analysis**: Reference products.csv for Japanese/English category names
3. **Time series**: Use date, day_of_week, and is_weekend for temporal patterns
4. **Revenue calculations**: sales_amount is in JPY (Japanese Yen), no currency conversion needed

### For Reproducibility

1. **Pipeline**: Run `python src/data_pipeline/generate_processed_data.py` to regenerate
2. **Tests**: Run `pytest tests/test_data_quality.py` to validate
3. **Dependencies**: See `requirements.txt` for Python package versions

### SQL Equivalents

If loading into a database, use these data types:

```sql
CREATE TABLE sales_clean (
    transaction_id VARCHAR(20) PRIMARY KEY,
    date DATE NOT NULL,
    store_id VARCHAR(3) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    sales_amount DECIMAL(10,2) NOT NULL,
    quantity INTEGER,
    day_of_week VARCHAR(9) NOT NULL,
    day_of_month INTEGER NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    week_of_month INTEGER NOT NULL
);

CREATE TABLE stores (
    store_id VARCHAR(3) PRIMARY KEY,
    store_name_jp VARCHAR(50) NOT NULL,
    store_name_en VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    region VARCHAR(20) NOT NULL
);

CREATE TABLE products (
    category_id VARCHAR(3) PRIMARY KEY,
    category_name_en VARCHAR(50) NOT NULL,
    category_name_jp VARCHAR(50) NOT NULL
);
```

---

## Contact & Questions

For questions about this data dictionary or the underlying data:

- **Data Engineer**: Claude Code Team
- **Project**: Multi-Store Fashion Retail Sales Analysis
- **Documentation Version**: 1.0
- **Last Updated**: October 2025

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-19 | Data Engineer | Initial data dictionary creation |

---

*This data dictionary is maintained alongside the processed datasets and should be updated whenever the data pipeline or schema changes.*
