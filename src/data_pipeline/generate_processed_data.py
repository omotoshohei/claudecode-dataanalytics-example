"""
Generate Processed Datasets Script

This script orchestrates the full data pipeline:
1. Load raw data
2. Clean and transform
3. Validate quality
4. Save processed datasets

Author: Data Engineer
Date: October 2025
"""

import pandas as pd
from pathlib import Path
import logging
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_pipeline.loader import load_all_store_files, combine_raw_data
from data_pipeline.cleaner import clean_raw_data, create_store_metadata, create_product_metadata
from data_pipeline.validator import validate_all, generate_data_quality_report

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main pipeline execution function.
    """
    # Define paths
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'data' / 'raw'  # Look in data/raw/ subdirectory
    processed_dir = project_root / 'data' / 'processed'

    # Create processed directory if it doesn't exist
    processed_dir.mkdir(exist_ok=True)

    logger.info("=" * 80)
    logger.info("STARTING DATA PIPELINE")
    logger.info("=" * 80)

    # Step 1: Load raw data
    logger.info("\nSTEP 1: Loading raw data...")
    all_data = load_all_store_files(str(data_dir))
    raw_combined = combine_raw_data(all_data)
    logger.info(f"✓ Loaded {len(raw_combined)} rows from {len(all_data)} files")

    # Step 2: Clean data
    logger.info("\nSTEP 2: Cleaning and transforming data...")
    sales_clean = clean_raw_data(raw_combined)
    logger.info(f"✓ Cleaned data: {len(sales_clean)} transactions retained")

    # Step 3: Create metadata
    logger.info("\nSTEP 3: Creating metadata tables...")
    stores = create_store_metadata()
    products = create_product_metadata(sales_clean)
    logger.info(f"✓ Created metadata: {len(stores)} stores, {len(products)} categories")

    # Step 4: Validate
    logger.info("\nSTEP 4: Validating data quality...")
    all_valid, messages = validate_all(sales_clean, stores)

    if not all_valid:
        logger.error("✗ Validation failed! Please review errors above.")
        return False

    logger.info("✓ All validations passed")

    # Step 5: Generate quality report
    logger.info("\nSTEP 5: Generating quality report...")
    report = generate_data_quality_report(sales_clean)

    # Step 6: Save processed data
    logger.info("\nSTEP 6: Saving processed datasets...")

    # Save sales_clean.csv
    sales_path = processed_dir / 'sales_clean.csv'
    sales_clean.to_csv(sales_path, index=False, encoding='utf-8')
    logger.info(f"✓ Saved: {sales_path}")

    # Save stores.csv
    stores_path = processed_dir / 'stores.csv'
    stores.to_csv(stores_path, index=False, encoding='utf-8')
    logger.info(f"✓ Saved: {stores_path}")

    # Save products.csv
    products_path = processed_dir / 'products.csv'
    products.to_csv(products_path, index=False, encoding='utf-8')
    logger.info(f"✓ Saved: {products_path}")

    # Print final summary
    logger.info("\n" + "=" * 80)
    logger.info("PIPELINE COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Processed datasets saved to: {processed_dir}")
    logger.info(f"\nFiles created:")
    logger.info(f"  1. sales_clean.csv   - {len(sales_clean):,} transactions")
    logger.info(f"  2. stores.csv        - {len(stores)} stores")
    logger.info(f"  3. products.csv      - {len(products)} categories")
    logger.info(f"\nData Quality:")
    logger.info(f"  - Date range: {report['date_range']['min']} to {report['date_range']['max']}")
    logger.info(f"  - Stores: {', '.join(report['stores']['ids'])}")
    logger.info(f"  - Total revenue: ¥{report['sales']['total']:,.0f}")
    logger.info(f"  - Average transaction: ¥{report['sales']['mean']:,.0f}")
    logger.info(f"  - Data retention: {len(sales_clean) / len(raw_combined) * 100:.1f}%")
    logger.info("=" * 80)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
