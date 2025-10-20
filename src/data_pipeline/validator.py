"""
Data Validator Module

This module validates cleaned sales data to ensure quality standards are met.

Author: Data Engineer
Date: October 2025
"""

import pandas as pd
import numpy as np
from typing import Tuple, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_no_missing_critical_fields(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that critical fields have no missing values.

    Args:
        df: Cleaned sales DataFrame

    Returns:
        Tuple of (is_valid, message)
    """
    critical_fields = ['transaction_id', 'date', 'store_id', 'product_category', 'sales_amount']

    for field in critical_fields:
        if field not in df.columns:
            return False, f"Missing column: {field}"

        missing_count = df[field].isna().sum()
        if missing_count > 0:
            return False, f"Field '{field}' has {missing_count} missing values"

    return True, "All critical fields are complete"


def validate_date_range(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that all dates are within January 2024.

    Args:
        df: Cleaned sales DataFrame

    Returns:
        Tuple of (is_valid, message)
    """
    min_date = pd.Timestamp('2024-01-01')
    max_date = pd.Timestamp('2024-01-31')

    if df['date'].min() < min_date:
        return False, f"Found dates before {min_date}: {df['date'].min()}"

    if df['date'].max() > max_date:
        return False, f"Found dates after {max_date}: {df['date'].max()}"

    return True, f"All dates within range: {df['date'].min()} to {df['date'].max()}"


def validate_non_negative_sales(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that all sales amounts are non-negative.

    Args:
        df: Cleaned sales DataFrame

    Returns:
        Tuple of (is_valid, message)
    """
    negative_count = (df['sales_amount'] < 0).sum()

    if negative_count > 0:
        return False, f"Found {negative_count} negative sales amounts"

    return True, f"All sales amounts are non-negative (min: ¥{df['sales_amount'].min():,.0f})"


def validate_store_ids(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that all store IDs are valid (S01-S10).

    Args:
        df: Cleaned sales DataFrame

    Returns:
        Tuple of (is_valid, message)
    """
    valid_stores = {f'S{str(i).zfill(2)}' for i in range(1, 11)}
    actual_stores = set(df['store_id'].unique())

    invalid_stores = actual_stores - valid_stores

    if invalid_stores:
        return False, f"Found invalid store IDs: {invalid_stores}"

    return True, f"All store IDs valid. Found: {sorted(actual_stores)}"


def validate_data_types(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that columns have correct data types.

    Args:
        df: Cleaned sales DataFrame

    Returns:
        Tuple of (is_valid, message)
    """
    expected_types = {
        'transaction_id': 'object',
        'date': 'datetime64[ns]',
        'store_id': 'object',
        'product_category': 'object',
        'sales_amount': ('float64', 'int64'),
        'day_of_week': 'object',
        'is_weekend': 'bool'
    }

    for col, expected_type in expected_types.items():
        if col not in df.columns:
            continue  # Skip if column doesn't exist

        actual_type = str(df[col].dtype)

        if isinstance(expected_type, tuple):
            if actual_type not in expected_type:
                return False, f"Column '{col}' has type '{actual_type}', expected one of {expected_type}"
        else:
            if actual_type != expected_type:
                return False, f"Column '{col}' has type '{actual_type}', expected '{expected_type}'"

    return True, "All data types are correct"


def validate_referential_integrity(sales_df: pd.DataFrame, stores_df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that all store IDs in sales data exist in stores metadata.

    Args:
        sales_df: Cleaned sales DataFrame
        stores_df: Store metadata DataFrame

    Returns:
        Tuple of (is_valid, message)
    """
    sales_stores = set(sales_df['store_id'].unique())
    metadata_stores = set(stores_df['store_id'].unique())

    orphaned_stores = sales_stores - metadata_stores

    if orphaned_stores:
        return False, f"Found store IDs in sales data without metadata: {orphaned_stores}"

    return True, f"All {len(sales_stores)} store IDs have metadata"


def validate_unique_transaction_ids(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that all transaction IDs are unique.

    Args:
        df: Cleaned sales DataFrame

    Returns:
        Tuple of (is_valid, message)
    """
    total_rows = len(df)
    unique_ids = df['transaction_id'].nunique()

    if total_rows != unique_ids:
        duplicates = total_rows - unique_ids
        return False, f"Found {duplicates} duplicate transaction IDs"

    return True, f"All {total_rows} transaction IDs are unique"


def validate_all(sales_df: pd.DataFrame, stores_df: pd.DataFrame = None) -> Tuple[bool, List[str]]:
    """
    Run all validation checks on the data.

    Args:
        sales_df: Cleaned sales DataFrame
        stores_df: Store metadata DataFrame (optional)

    Returns:
        Tuple of (all_valid, list of messages)
    """
    logger.info("=" * 80)
    logger.info("RUNNING DATA VALIDATION")
    logger.info("=" * 80)

    validations = [
        ("No Missing Critical Fields", validate_no_missing_critical_fields(sales_df)),
        ("Date Range", validate_date_range(sales_df)),
        ("Non-Negative Sales", validate_non_negative_sales(sales_df)),
        ("Valid Store IDs", validate_store_ids(sales_df)),
        ("Correct Data Types", validate_data_types(sales_df)),
        ("Unique Transaction IDs", validate_unique_transaction_ids(sales_df)),
    ]

    if stores_df is not None:
        validations.append(("Referential Integrity", validate_referential_integrity(sales_df, stores_df)))

    all_valid = True
    messages = []

    for name, (is_valid, message) in validations:
        status = "✓ PASS" if is_valid else "✗ FAIL"
        log_message = f"{status}: {name} - {message}"

        if is_valid:
            logger.info(log_message)
        else:
            logger.error(log_message)
            all_valid = False

        messages.append(log_message)

    logger.info("=" * 80)
    if all_valid:
        logger.info("✓ ALL VALIDATIONS PASSED")
    else:
        logger.error("✗ SOME VALIDATIONS FAILED")
    logger.info("=" * 80)

    return all_valid, messages


def generate_data_quality_report(df: pd.DataFrame) -> dict:
    """
    Generate a comprehensive data quality report.

    Args:
        df: Cleaned sales DataFrame

    Returns:
        Dictionary with quality metrics
    """
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'date_range': {
            'min': str(df['date'].min()),
            'max': str(df['date'].max()),
            'days': (df['date'].max() - df['date'].min()).days + 1
        },
        'stores': {
            'count': df['store_id'].nunique(),
            'ids': sorted(df['store_id'].unique().tolist())
        },
        'categories': {
            'count': df['product_category'].nunique(),
            'list': sorted(df['product_category'].unique().tolist())
        },
        'sales': {
            'total': float(df['sales_amount'].sum()),
            'mean': float(df['sales_amount'].mean()),
            'median': float(df['sales_amount'].median()),
            'min': float(df['sales_amount'].min()),
            'max': float(df['sales_amount'].max()),
            'std': float(df['sales_amount'].std())
        },
        'completeness': {
            col: {
                'missing': int(df[col].isna().sum()),
                'missing_pct': float(df[col].isna().sum() / len(df) * 100)
            }
            for col in df.columns
        }
    }

    logger.info("\n" + "=" * 80)
    logger.info("DATA QUALITY REPORT")
    logger.info("=" * 80)
    logger.info(f"Total Transactions: {report['total_rows']:,}")
    logger.info(f"Date Range: {report['date_range']['min']} to {report['date_range']['max']} ({report['date_range']['days']} days)")
    logger.info(f"Stores: {report['stores']['count']} ({', '.join(report['stores']['ids'])})")
    logger.info(f"Categories: {report['categories']['count']} ({', '.join(report['categories']['list'])})")
    logger.info(f"Total Sales: ¥{report['sales']['total']:,.0f}")
    logger.info(f"Average Transaction: ¥{report['sales']['mean']:,.0f}")
    logger.info(f"Sales Range: ¥{report['sales']['min']:,.0f} - ¥{report['sales']['max']:,.0f}")
    logger.info("=" * 80)

    return report


if __name__ == "__main__":
    # Example usage
    from loader import load_all_store_files, combine_raw_data
    from cleaner import clean_raw_data, create_store_metadata, create_product_metadata

    # Load and clean data
    data_dir = "/Users/sho/code/project/claudecode-dataanalytics-example/data"
    all_data = load_all_store_files(data_dir)
    raw_combined = combine_raw_data(all_data)
    sales_clean = clean_raw_data(raw_combined)
    stores = create_store_metadata()

    # Validate
    all_valid, messages = validate_all(sales_clean, stores)

    # Generate quality report
    report = generate_data_quality_report(sales_clean)

    print("\n" + "=" * 80)
    if all_valid:
        print("✓ DATA VALIDATION SUCCESSFUL - Ready for analysis!")
    else:
        print("✗ DATA VALIDATION FAILED - Please review errors above")
    print("=" * 80)
