"""
Data Cleaner Module

This module standardizes and cleans raw sales data from multiple stores.
Handles schema variations, missing values, and data type conversions.

Author: Data Engineer
Date: October 2025
"""

import pandas as pd
import numpy as np
from typing import Dict
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Column name mapping dictionary
COLUMN_MAPPINGS = {
    # Date columns
    '売上日': 'date',
    'Date': 'date',
    '横浜店売上管理表': 'date',  # Yokohama file has this as first column
    'Unnamed: 1': 'date',  # After header extraction

    # Store columns
    '店舗': 'store_name',
    'Store': 'store_name',
    '店舗名': 'store_name',

    # Category columns
    'カテゴリ': 'product_category',
    'Category': 'product_category',

    # Product columns
    '商品名': 'product_name',
    'Product': 'product_name',
    '商品': 'product_name',

    # Price columns
    '単価': 'unit_price',
    'Price': 'unit_price',
    '価格': 'unit_price',

    # Quantity columns
    '数量': 'quantity',
    'Qty': 'quantity',
    '個数': 'quantity',

    # Sales amount columns
    '売上金額': 'sales_amount',
    'Sales': 'sales_amount',
    '合計': 'sales_amount',
}

# Product category standardization
CATEGORY_MAPPINGS = {
    # Japanese to English
    'レディース': "Women's Apparel",
    'メンズ': "Men's Apparel",
    'アクセサリー': 'Accessories',
    'シューズ': 'Footwear',
    'バッグ': 'Bags',
    'キッズ': 'Kids',
    '季節商品': 'Seasonal',
    'セール商品': 'Sale Items',

    # English (already standardized)
    "Women's Apparel": "Women's Apparel",
    "Men's Apparel": "Men's Apparel",
    'Accessories': 'Accessories',
    'Footwear': 'Footwear',
    'Bags': 'Bags',
    'Kids': 'Kids',
    'Seasonal': 'Seasonal',
    'Sale Items': 'Sale Items',
}


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names across different file formats.

    Args:
        df: Raw DataFrame with various column names

    Returns:
        DataFrame with standardized English column names
    """
    df_clean = df.copy()

    # Rename columns using mapping
    rename_dict = {}
    for col in df_clean.columns:
        if col in COLUMN_MAPPINGS:
            rename_dict[col] = COLUMN_MAPPINGS[col]

    df_clean = df_clean.rename(columns=rename_dict)

    # Handle duplicate columns by coalescing (keeping first non-null value)
    if df_clean.columns.duplicated().any():
        logger.warning("Duplicate columns detected, coalescing duplicate columns")

        # Get unique column names
        unique_cols = df_clean.columns.unique()

        # For each unique column name, if there are duplicates, coalesce them
        coalesced_data = {}
        for col in unique_cols:
            if col in df_clean.columns:
                # Get all columns with this name
                col_data = df_clean[col]

                # If it's a DataFrame (multiple columns with same name), coalesce
                if isinstance(col_data, pd.DataFrame):
                    # Take first non-null value across all duplicate columns
                    coalesced_data[col] = col_data.bfill(axis=1).iloc[:, 0]
                else:
                    # Single column, keep as is
                    coalesced_data[col] = col_data

        # Reconstruct DataFrame with coalesced columns
        df_clean = pd.DataFrame(coalesced_data)

    logger.info(f"Standardized columns: {list(df_clean.columns)}")

    return df_clean


def extract_core_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract only the core columns needed for analysis.

    Args:
        df: DataFrame with standardized column names

    Returns:
        DataFrame with only core columns
    """
    core_columns = [
        'date', 'store_name', 'product_category',
        'product_name', 'unit_price', 'quantity', 'sales_amount',
        '_source_store_id', '_source_file'
    ]

    # Select only columns that exist
    existing_columns = [col for col in core_columns if col in df.columns]

    df_core = df[existing_columns].copy()

    logger.info(f"Extracted {len(existing_columns)} core columns")

    return df_core


def clean_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize date column.

    Args:
        df: DataFrame with 'date' column

    Returns:
        DataFrame with cleaned date column
    """
    df_clean = df.copy()

    # Convert to datetime
    df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')

    # Remove any rows with invalid dates
    invalid_dates = df_clean['date'].isna()
    if invalid_dates.sum() > 0:
        logger.warning(f"Removing {invalid_dates.sum()} rows with invalid dates")
        df_clean = df_clean[~invalid_dates]

    # Filter to January 2024 only
    df_clean = df_clean[
        (df_clean['date'] >= '2024-01-01') &
        (df_clean['date'] <= '2024-01-31')
    ]

    logger.info(f"Date range: {df_clean['date'].min()} to {df_clean['date'].max()}")

    return df_clean


def clean_sales_amount(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean sales amount column.

    Args:
        df: DataFrame with 'sales_amount' column

    Returns:
        DataFrame with cleaned sales amounts
    """
    df_clean = df.copy()

    # Convert to numeric, handling various formats
    df_clean['sales_amount'] = pd.to_numeric(
        df_clean['sales_amount'],
        errors='coerce'
    )

    # If sales_amount is missing but we have unit_price and quantity, calculate it
    if 'unit_price' in df_clean.columns and 'quantity' in df_clean.columns:
        # Convert unit_price and quantity to numeric
        df_clean['unit_price'] = pd.to_numeric(df_clean['unit_price'], errors='coerce')
        df_clean['quantity'] = pd.to_numeric(df_clean['quantity'], errors='coerce')

        # Calculate missing sales amounts
        missing_sales = df_clean['sales_amount'].isna()
        df_clean.loc[missing_sales, 'sales_amount'] = (
            df_clean.loc[missing_sales, 'unit_price'] *
            df_clean.loc[missing_sales, 'quantity']
        )

    # Remove rows where sales_amount is still missing or invalid
    valid_sales = df_clean['sales_amount'].notna() & (df_clean['sales_amount'] >= 0)
    removed = len(df_clean) - valid_sales.sum()

    if removed > 0:
        logger.warning(f"Removing {removed} rows with invalid/missing sales amounts")

    df_clean = df_clean[valid_sales]

    logger.info(f"Sales amount range: ¥{df_clean['sales_amount'].min():,.0f} to ¥{df_clean['sales_amount'].max():,.0f}")

    return df_clean


def standardize_product_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize product category names to English.

    Args:
        df: DataFrame with 'product_category' column

    Returns:
        DataFrame with standardized categories
    """
    df_clean = df.copy()

    # Map categories to standard English names
    df_clean['product_category'] = df_clean['product_category'].map(
        lambda x: CATEGORY_MAPPINGS.get(x, x) if pd.notna(x) else x
    )

    # Remove rows with missing categories
    missing_categories = df_clean['product_category'].isna()
    if missing_categories.sum() > 0:
        logger.warning(f"Removing {missing_categories.sum()} rows with missing categories")
        df_clean = df_clean[~missing_categories]

    logger.info(f"Unique categories: {df_clean['product_category'].unique()}")

    return df_clean


def assign_store_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign standardized store IDs (S01-S10).

    Args:
        df: DataFrame with '_source_store_id' column

    Returns:
        DataFrame with 'store_id' column
    """
    df_clean = df.copy()

    # Use the source store ID we added during loading
    df_clean['store_id'] = df_clean['_source_store_id']

    logger.info(f"Store IDs: {sorted(df_clean['store_id'].unique())}")

    return df_clean


def add_derived_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived fields for analysis.

    Args:
        df: DataFrame with 'date' column

    Returns:
        DataFrame with additional derived columns
    """
    df_clean = df.copy()

    # Extract day of week
    df_clean['day_of_week'] = df_clean['date'].dt.day_name()

    # Extract day of month
    df_clean['day_of_month'] = df_clean['date'].dt.day

    # Weekend flag
    df_clean['is_weekend'] = df_clean['date'].dt.dayofweek.isin([5, 6])

    # Week of month (1-5)
    df_clean['week_of_month'] = ((df_clean['date'].dt.day - 1) // 7) + 1

    logger.info("Added derived fields: day_of_week, day_of_month, is_weekend, week_of_month")

    return df_clean


def create_transaction_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create unique transaction IDs.

    Args:
        df: DataFrame

    Returns:
        DataFrame with 'transaction_id' column
    """
    df_clean = df.copy()

    # Create transaction ID as: StoreID_YYYYMMDD_RowNum
    df_clean['transaction_id'] = (
        df_clean['store_id'] + '_' +
        df_clean['date'].dt.strftime('%Y%m%d') + '_' +
        df_clean.groupby(['store_id', 'date']).cumcount().astype(str).str.zfill(4)
    )

    logger.info(f"Created {len(df_clean)} unique transaction IDs")

    return df_clean


def select_final_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select and order final columns for output.

    Args:
        df: Cleaned DataFrame

    Returns:
        DataFrame with final column selection and order
    """
    final_columns = [
        'transaction_id',
        'date',
        'store_id',
        'product_category',
        'sales_amount',
        'quantity',
        'day_of_week',
        'day_of_month',
        'is_weekend',
        'week_of_month'
    ]

    # Select columns that exist
    existing_cols = [col for col in final_columns if col in df.columns]

    df_final = df[existing_cols].copy()

    logger.info(f"Final columns: {list(df_final.columns)}")

    return df_final


def clean_raw_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Main cleaning pipeline - orchestrates all cleaning steps.

    Args:
        raw_df: Raw combined DataFrame from loader

    Returns:
        Cleaned DataFrame ready for analysis

    Process:
        1. Standardize column names
        2. Extract core columns
        3. Clean dates
        4. Clean sales amounts
        5. Standardize categories
        6. Assign store IDs
        7. Add derived fields
        8. Create transaction IDs
        9. Select final columns
    """
    logger.info("=" * 80)
    logger.info("STARTING DATA CLEANING PIPELINE")
    logger.info("=" * 80)
    logger.info(f"Input rows: {len(raw_df)}")

    # Step 1: Standardize column names
    df = standardize_column_names(raw_df)

    # Step 2: Extract core columns
    df = extract_core_columns(df)

    # Step 3: Clean dates
    df = clean_date_column(df)

    # Step 4: Clean sales amounts
    df = clean_sales_amount(df)

    # Step 5: Standardize categories
    df = standardize_product_categories(df)

    # Step 6: Assign store IDs
    df = assign_store_ids(df)

    # Step 7: Add derived fields
    df = add_derived_fields(df)

    # Step 8: Create transaction IDs
    df = create_transaction_ids(df)

    # Step 9: Select final columns
    df_clean = select_final_columns(df)

    # Remove duplicates
    original_len = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=['transaction_id'])
    duplicates_removed = original_len - len(df_clean)

    if duplicates_removed > 0:
        logger.warning(f"Removed {duplicates_removed} duplicate transaction IDs")

    logger.info("=" * 80)
    logger.info("DATA CLEANING COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Output rows: {len(df_clean)}")
    logger.info(f"Data quality: {len(df_clean) / len(raw_df) * 100:.1f}% of raw data retained")

    return df_clean


def create_store_metadata() -> pd.DataFrame:
    """
    Create store metadata table.

    Returns:
        DataFrame with store information
    """
    stores_data = {
        'store_id': ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10'],
        'store_name_jp': ['渋谷店', '新宿店', '池袋店', '横浜店', '大阪店',
                          '札幌店', '仙台店', '名古屋店', '広島店', '福岡店'],
        'store_name_en': ['Shibuya', 'Shinjuku', 'Ikebukuro', 'Yokohama', 'Osaka',
                          'Sapporo', 'Sendai', 'Nagoya', 'Hiroshima', 'Fukuoka'],
        'city': ['Tokyo', 'Tokyo', 'Tokyo', 'Yokohama', 'Osaka',
                 'Sapporo', 'Sendai', 'Nagoya', 'Hiroshima', 'Fukuoka'],
        'region': ['Kanto', 'Kanto', 'Kanto', 'Kanto', 'Kansai',
                   'Hokkaido', 'Tohoku', 'Chubu', 'Chugoku', 'Kyushu']
    }

    stores_df = pd.DataFrame(stores_data)

    logger.info(f"Created store metadata for {len(stores_df)} stores")

    return stores_df


def create_product_metadata(sales_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create product category metadata table.

    Args:
        sales_df: Cleaned sales DataFrame

    Returns:
        DataFrame with product category information
    """
    # Get unique categories from sales data
    unique_categories = sorted(sales_df['product_category'].unique())

    # Create reverse mapping for Japanese names
    reverse_category_map = {v: k for k, v in CATEGORY_MAPPINGS.items() if k != v}

    products_data = {
        'category_id': [f'C{str(i+1).zfill(2)}' for i in range(len(unique_categories))],
        'category_name_en': unique_categories,
        'category_name_jp': [reverse_category_map.get(cat, cat) for cat in unique_categories]
    }

    products_df = pd.DataFrame(products_data)

    logger.info(f"Created product metadata for {len(products_df)} categories")

    return products_df


if __name__ == "__main__":
    # Example usage
    from loader import load_all_store_files, combine_raw_data

    # Load raw data
    data_dir = "/Users/sho/code/project/claudecode-dataanalytics-example/data"
    all_data = load_all_store_files(data_dir)
    raw_combined = combine_raw_data(all_data)

    # Clean data
    sales_clean = clean_raw_data(raw_combined)

    # Create metadata
    stores = create_store_metadata()
    products = create_product_metadata(sales_clean)

    # Display summary
    print("\n" + "=" * 80)
    print("CLEANING SUMMARY")
    print("=" * 80)
    print(f"\nSales Data: {len(sales_clean)} transactions")
    print(f"Date Range: {sales_clean['date'].min()} to {sales_clean['date'].max()}")
    print(f"Stores: {len(stores)}")
    print(f"Product Categories: {len(products)}")
    print(f"\nSales by Store:")
    print(sales_clean.groupby('store_id')['sales_amount'].agg(['count', 'sum']).sort_values('sum', ascending=False))
