"""
Data Loader Module

This module provides functions to load raw sales data from multiple stores.
Handles mixed file formats (Excel and CSV) with different encodings.

Author: Data Engineer
Date: October 2025
"""

import pandas as pd
import chardet
from pathlib import Path
from typing import List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def detect_csv_encoding(filepath: str) -> str:
    """
    Detect the encoding of a CSV file.

    Args:
        filepath: Path to the CSV file

    Returns:
        Detected encoding (e.g., 'utf-8', 'shift_jis')
    """
    with open(filepath, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    confidence = result['confidence']
    logger.info(f"Detected encoding: {encoding} (confidence: {confidence:.2%})")
    return encoding


def read_excel_file(filepath: str) -> pd.DataFrame:
    """
    Read an Excel file with proper handling of various formats.

    Args:
        filepath: Path to the Excel file

    Returns:
        DataFrame containing the data

    Notes:
        - Handles files with header rows
        - Skips files with metadata/notes at the top
        - Tries multiple sheets if needed
        - Uses openpyxl engine for .xlsx files
    """
    try:
        # First check if file has multiple sheets
        excel_file = pd.ExcelFile(filepath, engine='openpyxl')
        sheet_names = excel_file.sheet_names

        # Try to find a sheet with data (not just metadata)
        for sheet_name in sheet_names:
            # Try different skiprows to find the header
            for skip in range(0, 6):
                df = pd.read_excel(filepath, engine='openpyxl',
                                 sheet_name=sheet_name, skiprows=skip)

                # Check if this looks like actual data
                # Data sheets should have > 5 rows and multiple columns
                if df.shape[0] > 5 and df.shape[1] >= 5:
                    # Look for common date column names in Japanese or English
                    date_columns = ['売上日', '日付', 'Date', '取引日']
                    has_date_column = any(col in df.columns for col in date_columns)

                    # Check if columns look like real data (not Unnamed or NaN)
                    has_real_columns = not str(df.columns[0]).startswith('Unnamed')

                    if has_date_column and has_real_columns:
                        if skip > 0:
                            logger.info(f"Found data at row {skip}, sheet '{sheet_name}' for {filepath}")
                        else:
                            logger.info(f"Loaded sheet '{sheet_name}' from {filepath}")
                        return df

        # If we get here, try the first sheet with skiprows
        df = pd.read_excel(filepath, engine='openpyxl', sheet_name=sheet_names[0], skiprows=2)
        logger.info(f"Using first sheet with skip=2 for {filepath}")
        return df

    except Exception as e:
        logger.error(f"Error reading Excel file {filepath}: {e}")
        raise


def read_csv_file(filepath: str) -> pd.DataFrame:
    """
    Read a CSV file with automatic encoding detection.

    Args:
        filepath: Path to the CSV file

    Returns:
        DataFrame containing the data

    Notes:
        - Automatically detects encoding (UTF-8, Shift-JIS, etc.)
        - Handles different delimiters (comma, semicolon)
    """
    try:
        # Detect encoding
        encoding = detect_csv_encoding(filepath)

        # Try reading with comma delimiter first
        df = pd.read_csv(filepath, encoding=encoding)

        # Check if delimiter is wrong (all data in one column)
        if df.shape[1] == 1 and ';' in str(df.iloc[0, 0]):
            logger.info(f"Detected semicolon delimiter for {filepath}")
            df = pd.read_csv(filepath, encoding=encoding, delimiter=';')

        return df

    except Exception as e:
        logger.error(f"Error reading CSV file {filepath}: {e}")
        raise


def load_single_file(filepath: str) -> Tuple[pd.DataFrame, str]:
    """
    Load a single data file (Excel or CSV).

    Args:
        filepath: Path to the data file

    Returns:
        Tuple of (DataFrame, store_identifier)

    Notes:
        - Automatically detects file type
        - Extracts store identifier from filename
    """
    filepath = Path(filepath)
    filename = filepath.name

    logger.info(f"Loading file: {filename}")

    # Determine file type and read
    if filename.endswith('.xlsx'):
        df = read_excel_file(str(filepath))
    elif filename.endswith('.csv'):
        df = read_csv_file(str(filepath))
    else:
        raise ValueError(f"Unsupported file type: {filename}")

    # Extract store identifier from filename
    # Format: 01_渋谷店_売上_202401.xlsx -> S01
    store_number = filename[:2]
    store_id = f"S{store_number}"

    logger.info(f"Loaded {len(df)} rows from {filename} (Store: {store_id})")

    return df, store_id


def load_all_store_files(data_dir: str) -> List[Tuple[pd.DataFrame, str, str]]:
    """
    Load all store sales files from a directory.

    Args:
        data_dir: Path to directory containing raw data files

    Returns:
        List of tuples (DataFrame, store_id, filename)

    Notes:
        - Loads both Excel (.xlsx) and CSV files
        - Handles encoding automatically
        - Skips non-data files
    """
    data_path = Path(data_dir)
    all_data = []

    # Get all Excel and CSV files
    files = sorted(list(data_path.glob('*.xlsx')) + list(data_path.glob('*.csv')))

    # Filter out files that are clearly not store data
    store_files = [f for f in files if any(str(i).zfill(2) in f.name for i in range(1, 11))]

    logger.info(f"Found {len(store_files)} store data files")

    for filepath in store_files:
        try:
            df, store_id = load_single_file(str(filepath))
            all_data.append((df, store_id, filepath.name))
        except Exception as e:
            logger.warning(f"Failed to load {filepath.name}: {e}")
            # Continue loading other files
            continue

    logger.info(f"Successfully loaded {len(all_data)} out of {len(store_files)} files")

    return all_data


def combine_raw_data(all_data: List[Tuple[pd.DataFrame, str, str]]) -> pd.DataFrame:
    """
    Combine data from all stores into a single DataFrame.

    Args:
        all_data: List of tuples (DataFrame, store_id, filename)

    Returns:
        Combined DataFrame with store_id column added

    Notes:
        - Does NOT standardize columns yet (handled by cleaner.py)
        - Adds store_id as a tracking column
        - Preserves original column names for cleaning phase
    """
    combined_frames = []

    for df, store_id, filename in all_data:
        # Add store_id column
        df_copy = df.copy()
        df_copy['_source_store_id'] = store_id
        df_copy['_source_file'] = filename
        combined_frames.append(df_copy)

    # Concatenate all DataFrames
    combined_df = pd.concat(combined_frames, ignore_index=True, sort=False)

    logger.info(f"Combined data shape: {combined_df.shape}")
    logger.info(f"Total rows: {len(combined_df)}")

    return combined_df


if __name__ == "__main__":
    # Example usage
    data_dir = "/Users/sho/code/project/claudecode-dataanalytics-example/data"

    # Load all files
    all_data = load_all_store_files(data_dir)

    # Combine into single DataFrame
    raw_combined = combine_raw_data(all_data)

    print("\n" + "=" * 80)
    print("RAW DATA LOADING COMPLETE")
    print("=" * 80)
    print(f"Total files loaded: {len(all_data)}")
    print(f"Total rows: {len(raw_combined)}")
    print(f"Total columns: {len(raw_combined.columns)}")
    print(f"\nColumn names found:")
    for col in raw_combined.columns:
        print(f"  - {col}")
