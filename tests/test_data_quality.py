"""
Data Quality Tests

Comprehensive pytest tests for validating cleaned sales data quality.

Author: Data Engineer
Date: October 2025
"""

import pytest
import pandas as pd
from pathlib import Path


# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_ROOT / 'data' / 'processed'

# Fixtures
@pytest.fixture(scope='module')
def sales_df():
    """Load sales_clean.csv for testing."""
    return pd.read_csv(PROCESSED_DIR / 'sales_clean.csv', parse_dates=['date'])


@pytest.fixture(scope='module')
def stores_df():
    """Load stores.csv for testing."""
    return pd.read_csv(PROCESSED_DIR / 'stores.csv')


@pytest.fixture(scope='module')
def products_df():
    """Load products.csv for testing."""
    return pd.read_csv(PROCESSED_DIR / 'products.csv')


# Test 1: No missing values in critical fields
def test_no_missing_critical_fields(sales_df):
    """
    Verify that critical fields have no missing values.

    Critical fields: transaction_id, date, store_id, product_category, sales_amount
    """
    critical_fields = ['transaction_id', 'date', 'store_id', 'product_category', 'sales_amount']

    for field in critical_fields:
        assert field in sales_df.columns, f"Missing column: {field}"
        missing_count = sales_df[field].isna().sum()
        assert missing_count == 0, f"Field '{field}' has {missing_count} missing values"


# Test 2: Valid date range (January 2024)
def test_valid_date_range(sales_df):
    """
    Verify all dates are within January 2024.
    """
    min_date = pd.Timestamp('2024-01-01')
    max_date = pd.Timestamp('2024-01-31')

    assert sales_df['date'].min() >= min_date, f"Found dates before {min_date}"
    assert sales_df['date'].max() <= max_date, f"Found dates after {max_date}"


# Test 3: Non-negative sales amounts
def test_non_negative_sales(sales_df):
    """
    Verify all sales amounts are >= 0.
    """
    negative_count = (sales_df['sales_amount'] < 0).sum()
    assert negative_count == 0, f"Found {negative_count} negative sales amounts"


# Test 4: Valid store IDs (S01-S10 only)
def test_valid_store_ids(sales_df):
    """
    Verify all store IDs are in valid range (S01-S10).
    """
    valid_stores = {f'S{str(i).zfill(2)}' for i in range(1, 11)}
    actual_stores = set(sales_df['store_id'].unique())

    invalid_stores = actual_stores - valid_stores
    assert len(invalid_stores) == 0, f"Found invalid store IDs: {invalid_stores}"


# Test 5: Correct data types
def test_data_types(sales_df):
    """
    Verify columns have correct data types.
    """
    expected_types = {
        'transaction_id': 'object',
        'date': 'datetime64[ns]',
        'store_id': 'object',
        'product_category': 'object',
        'sales_amount': ('float64', 'int64'),
        'day_of_week': 'object',
        'is_weekend': ('bool', 'boolean')
    }

    for col, expected_type in expected_types.items():
        if col not in sales_df.columns:
            continue

        actual_type = str(sales_df[col].dtype)

        if isinstance(expected_type, tuple):
            assert actual_type in expected_type, \
                f"Column '{col}' has type '{actual_type}', expected one of {expected_type}"
        else:
            assert actual_type == expected_type, \
                f"Column '{col}' has type '{actual_type}', expected '{expected_type}'"


# Test 6: Referential integrity (sales.store_id exists in stores.store_id)
def test_referential_integrity(sales_df, stores_df):
    """
    Verify all store IDs in sales data exist in stores metadata.
    """
    sales_stores = set(sales_df['store_id'].unique())
    metadata_stores = set(stores_df['store_id'].unique())

    orphaned_stores = sales_stores - metadata_stores
    assert len(orphaned_stores) == 0, \
        f"Found store IDs in sales data without metadata: {orphaned_stores}"


# Test 7: Unique transaction IDs
def test_unique_transaction_ids(sales_df):
    """
    Verify all transaction IDs are unique.
    """
    total_rows = len(sales_df)
    unique_ids = sales_df['transaction_id'].nunique()

    assert total_rows == unique_ids, \
        f"Found {total_rows - unique_ids} duplicate transaction IDs"


# Test 8: Data completeness (minimum row count)
def test_minimum_row_count(sales_df):
    """
    Verify we have a reasonable number of transactions.
    Expected: At least 500 transactions from 8+ stores over 31 days.
    """
    min_expected_rows = 500

    assert len(sales_df) >= min_expected_rows, \
        f"Expected at least {min_expected_rows} rows, got {len(sales_df)}"


# Test 9: Store metadata completeness
def test_store_metadata_completeness(stores_df):
    """
    Verify store metadata has all required fields and 10 stores.
    """
    required_cols = ['store_id', 'store_name_jp', 'store_name_en', 'city', 'region']

    for col in required_cols:
        assert col in stores_df.columns, f"Missing column: {col}"
        missing = stores_df[col].isna().sum()
        assert missing == 0, f"Column '{col}' has {missing} missing values"

    assert len(stores_df) == 10, f"Expected 10 stores, got {len(stores_df)}"


# Test 10: Product category standardization
def test_product_category_standardization(sales_df):
    """
    Verify product categories are standardized (English names).
    """
    valid_categories = {
        "Women's Apparel",
        "Men's Apparel",
        'Accessories',
        'Footwear',
        'Bags',
        'Kids',
        'Seasonal',
        'Sale Items'
    }

    actual_categories = set(sales_df['product_category'].unique())

    invalid_categories = actual_categories - valid_categories
    assert len(invalid_categories) == 0, \
        f"Found non-standard categories: {invalid_categories}"


# Test 11: Day of week consistency
def test_day_of_week_consistency(sales_df):
    """
    Verify day_of_week values are valid.
    """
    valid_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
    actual_days = set(sales_df['day_of_week'].unique())

    invalid_days = actual_days - valid_days
    assert len(invalid_days) == 0, f"Found invalid day_of_week values: {invalid_days}"


# Test 12: Weekend flag consistency
def test_weekend_flag_consistency(sales_df):
    """
    Verify is_weekend is True for Saturday/Sunday, False otherwise.
    """
    weekend_days = {'Saturday', 'Sunday'}

    for _, row in sales_df.sample(min(100, len(sales_df))).iterrows():
        expected_weekend = row['day_of_week'] in weekend_days
        actual_weekend = row['is_weekend']

        assert actual_weekend == expected_weekend, \
            f"Weekend flag mismatch for {row['day_of_week']}: got {actual_weekend}, expected {expected_weekend}"


# Test 13: Sales amount reasonable range
def test_sales_amount_reasonable_range(sales_df):
    """
    Verify sales amounts are within reasonable range for fashion retail.
    Expect: 1,000 JPY to 200,000 JPY per transaction.
    """
    min_reasonable = 1000
    max_reasonable = 200000

    too_low = (sales_df['sales_amount'] < min_reasonable).sum()
    too_high = (sales_df['sales_amount'] > max_reasonable).sum()

    # Allow up to 5% outliers
    total = len(sales_df)
    assert too_low / total < 0.05, f"{too_low} sales amounts below ¥{min_reasonable:,} ({too_low/total*100:.1f}%)"
    assert too_high / total < 0.05, f"{too_high} sales amounts above ¥{max_reasonable:,} ({too_high/total*100:.1f}%)"


# Test 14: Quantity reasonable values
def test_quantity_reasonable_values(sales_df):
    """
    Verify quantity values are reasonable (1-20 items per transaction).
    """
    if 'quantity' not in sales_df.columns:
        pytest.skip("Quantity column not present")

    # Check non-null quantities
    valid_quantities = sales_df['quantity'].dropna()

    if len(valid_quantities) == 0:
        pytest.skip("No quantity data available")

    assert (valid_quantities >= 1).all(), "Found quantities less than 1"
    assert (valid_quantities <= 20).all(), "Found quantities greater than 20"


# Test 15: UTF-8 encoding (Japanese text renders correctly)
def test_utf8_encoding(stores_df):
    """
    Verify Japanese text is properly encoded and readable.
    """
    # Check that we can read Japanese store names without errors
    japanese_names = stores_df['store_name_jp'].tolist()

    # Should contain Japanese characters
    has_japanese = any('店' in name for name in japanese_names)
    assert has_japanese, "No Japanese characters found - possible encoding issue"

    # All names should be readable (not containing replacement characters)
    for name in japanese_names:
        assert '�' not in name, f"Encoding error in store name: {name}"


# Test Summary Report
def test_generate_summary_report(sales_df, stores_df, products_df):
    """
    Generate and log a summary report of data quality.
    This test always passes but provides useful information.
    """
    print("\n" + "=" * 80)
    print("DATA QUALITY TEST SUMMARY REPORT")
    print("=" * 80)
    print(f"Sales Data:")
    print(f"  - Total transactions: {len(sales_df):,}")
    print(f"  - Date range: {sales_df['date'].min()} to {sales_df['date'].max()}")
    print(f"  - Stores: {sales_df['store_id'].nunique()} ({', '.join(sorted(sales_df['store_id'].unique()))})")
    print(f"  - Categories: {sales_df['product_category'].nunique()}")
    print(f"  - Total revenue: ¥{sales_df['sales_amount'].sum():,.0f}")
    print(f"  - Average transaction: ¥{sales_df['sales_amount'].mean():,.0f}")
    print(f"\nStore Metadata:")
    print(f"  - Total stores: {len(stores_df)}")
    print(f"  - Regions: {stores_df['region'].nunique()}")
    print(f"\nProduct Metadata:")
    print(f"  - Total categories: {len(products_df)}")
    print("=" * 80)

    # Test always passes
    assert True


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
