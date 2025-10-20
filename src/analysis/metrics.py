"""
Reusable metrics calculation functions for retail sales analysis.

This module provides functions to calculate key performance indicators (KPIs)
and business metrics from sales transaction data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional


def calculate_revenue_by_store(
    sales_df: pd.DataFrame,
    stores_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate revenue metrics aggregated by store.

    Args:
        sales_df: DataFrame with sales transactions
        stores_df: DataFrame with store metadata

    Returns:
        DataFrame with columns: store_id, store_name, region, total_revenue,
        avg_transaction, num_transactions, revenue_share_pct

    Example:
        >>> store_metrics = calculate_revenue_by_store(sales_df, stores_df)
        >>> print(store_metrics.head())
    """
    # Merge sales with store information
    sales_with_stores = sales_df.merge(stores_df, on='store_id', how='left')

    # Aggregate by store
    store_revenue = sales_with_stores.groupby(
        ['store_id', 'store_name_en', 'region']
    ).agg({
        'sales_amount': ['sum', 'mean', 'count']
    }).reset_index()

    store_revenue.columns = [
        'store_id', 'store_name', 'region',
        'total_revenue', 'avg_transaction', 'num_transactions'
    ]

    # Calculate revenue share percentage
    store_revenue['revenue_share_pct'] = (
        store_revenue['total_revenue'] / store_revenue['total_revenue'].sum() * 100
    ).round(2)

    # Sort by revenue descending
    store_revenue = store_revenue.sort_values('total_revenue', ascending=False)

    return store_revenue


def calculate_revenue_by_region(
    sales_df: pd.DataFrame,
    stores_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate revenue metrics aggregated by geographic region.

    Args:
        sales_df: DataFrame with sales transactions
        stores_df: DataFrame with store metadata

    Returns:
        DataFrame with regional revenue metrics including total_revenue,
        avg_transaction, num_transactions, num_stores, revenue_share_pct

    Example:
        >>> region_metrics = calculate_revenue_by_region(sales_df, stores_df)
    """
    # Merge sales with store information
    sales_with_stores = sales_df.merge(stores_df, on='store_id', how='left')

    # Aggregate by region
    region_revenue = sales_with_stores.groupby('region').agg({
        'sales_amount': ['sum', 'mean', 'count'],
        'store_id': 'nunique'
    }).reset_index()

    region_revenue.columns = [
        'region', 'total_revenue', 'avg_transaction',
        'num_transactions', 'num_stores'
    ]

    # Calculate revenue share percentage
    region_revenue['revenue_share_pct'] = (
        region_revenue['total_revenue'] / region_revenue['total_revenue'].sum() * 100
    ).round(2)

    # Sort by revenue descending
    region_revenue = region_revenue.sort_values('total_revenue', ascending=False)

    return region_revenue


def calculate_revenue_by_category(
    sales_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate revenue metrics aggregated by product category.

    Args:
        sales_df: DataFrame with sales transactions

    Returns:
        DataFrame with category revenue metrics including total_revenue,
        avg_transaction, num_transactions, revenue_share_pct

    Example:
        >>> category_metrics = calculate_revenue_by_category(sales_df)
    """
    # Aggregate by category
    category_revenue = sales_df.groupby('product_category').agg({
        'sales_amount': ['sum', 'mean', 'count']
    }).reset_index()

    category_revenue.columns = [
        'category', 'total_revenue', 'avg_transaction', 'num_transactions'
    ]

    # Calculate revenue share percentage
    category_revenue['revenue_share_pct'] = (
        category_revenue['total_revenue'] / category_revenue['total_revenue'].sum() * 100
    ).round(2)

    # Sort by revenue descending
    category_revenue = category_revenue.sort_values('total_revenue', ascending=False)

    return category_revenue


def calculate_daily_revenue(
    sales_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate daily revenue aggregated by date.

    Args:
        sales_df: DataFrame with sales transactions containing 'date' column

    Returns:
        DataFrame with columns: date, revenue

    Example:
        >>> daily_rev = calculate_daily_revenue(sales_df)
    """
    daily_revenue = sales_df.groupby('date')['sales_amount'].sum().reset_index()
    daily_revenue.columns = ['date', 'revenue']

    return daily_revenue


def calculate_day_of_week_metrics(
    sales_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate revenue metrics by day of week.

    Args:
        sales_df: DataFrame with sales transactions

    Returns:
        DataFrame with day_of_week, total_revenue, avg_transaction, num_transactions
        sorted by standard week order (Monday-Sunday)

    Example:
        >>> dow_metrics = calculate_day_of_week_metrics(sales_df)
    """
    # Define proper day order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Aggregate by day of week
    dow_revenue = sales_df.groupby('day_of_week').agg({
        'sales_amount': ['sum', 'mean', 'count']
    }).reset_index()

    dow_revenue.columns = [
        'day_of_week', 'total_revenue', 'avg_transaction', 'num_transactions'
    ]

    # Sort by day order
    dow_revenue['day_of_week'] = pd.Categorical(
        dow_revenue['day_of_week'],
        categories=day_order,
        ordered=True
    )
    dow_revenue = dow_revenue.sort_values('day_of_week')

    return dow_revenue


def calculate_weekend_vs_weekday(
    sales_df: pd.DataFrame
) -> Tuple[pd.DataFrame, float]:
    """
    Compare weekend vs weekday performance metrics.

    Args:
        sales_df: DataFrame with sales transactions containing 'is_weekend' column

    Returns:
        Tuple of (comparison DataFrame, weekend_lift_percentage)

        comparison DataFrame includes: period (Weekend/Weekday), total_revenue,
        avg_transaction, num_transactions, avg_revenue_per_day

    Example:
        >>> comparison, lift = calculate_weekend_vs_weekday(sales_df)
        >>> print(f"Weekend lift: {lift:.1f}%")
    """
    # Aggregate by weekend flag
    weekend_comparison = sales_df.groupby('is_weekend').agg({
        'sales_amount': ['sum', 'mean', 'count']
    }).reset_index()

    weekend_comparison.columns = [
        'is_weekend', 'total_revenue', 'avg_transaction', 'num_transactions'
    ]

    # Add period label
    weekend_comparison['period'] = weekend_comparison['is_weekend'].map({
        True: 'Weekend',
        False: 'Weekday'
    })

    # Calculate average per day
    weekend_days = sales_df[sales_df['is_weekend']]['date'].dt.date.nunique()
    weekday_days = sales_df[~sales_df['is_weekend']]['date'].dt.date.nunique()

    weekend_comparison['avg_revenue_per_day'] = weekend_comparison.apply(
        lambda row: row['total_revenue'] / (weekend_days if row['is_weekend'] else weekday_days),
        axis=1
    )

    # Calculate weekend lift
    weekend_avg = weekend_comparison[weekend_comparison['is_weekend']]['avg_revenue_per_day'].values[0]
    weekday_avg = weekend_comparison[~weekend_comparison['is_weekend']]['avg_revenue_per_day'].values[0]
    weekend_lift = ((weekend_avg - weekday_avg) / weekday_avg * 100)

    return weekend_comparison, weekend_lift


def calculate_key_metrics(
    sales_df: pd.DataFrame
) -> Dict[str, float]:
    """
    Calculate overall key performance indicators for the entire dataset.

    Args:
        sales_df: DataFrame with sales transactions

    Returns:
        Dictionary with key metrics: total_revenue, total_transactions,
        avg_transaction_value, median_transaction_value, num_stores, num_days

    Example:
        >>> kpis = calculate_key_metrics(sales_df)
        >>> print(f"Total Revenue: ¥{kpis['total_revenue']:,.0f}")
    """
    kpis = {
        'total_revenue': sales_df['sales_amount'].sum(),
        'total_transactions': len(sales_df),
        'avg_transaction_value': sales_df['sales_amount'].mean(),
        'median_transaction_value': sales_df['sales_amount'].median(),
        'num_stores': sales_df['store_id'].nunique(),
        'num_days': sales_df['date'].dt.date.nunique(),
        'date_range_start': sales_df['date'].min(),
        'date_range_end': sales_df['date'].max()
    }

    return kpis


def calculate_category_mix_by_store(
    sales_df: pd.DataFrame,
    stores_df: pd.DataFrame,
    percentage: bool = False
) -> pd.DataFrame:
    """
    Calculate product category revenue breakdown for each store.

    Args:
        sales_df: DataFrame with sales transactions
        stores_df: DataFrame with store metadata
        percentage: If True, returns percentage of store revenue;
                   if False, returns absolute revenue

    Returns:
        DataFrame with stores as rows and categories as columns,
        values are revenue (or percentage of store total)

    Example:
        >>> mix = calculate_category_mix_by_store(sales_df, stores_df, percentage=True)
    """
    # Merge with store info
    sales_with_stores = sales_df.merge(stores_df, on='store_id', how='left')

    # Pivot to get category x store matrix
    category_by_store = sales_with_stores.pivot_table(
        values='sales_amount',
        index='store_name_en',
        columns='product_category',
        aggfunc='sum',
        fill_value=0
    )

    if percentage:
        # Convert to percentage of store total
        category_by_store = category_by_store.div(
            category_by_store.sum(axis=1),
            axis=0
        ) * 100

    return category_by_store


def calculate_performance_gap(
    store_revenue_df: pd.DataFrame
) -> Tuple[Dict[str, any], float]:
    """
    Calculate performance gap between top and bottom performing stores.

    Args:
        store_revenue_df: DataFrame with store revenue metrics (from calculate_revenue_by_store)

    Returns:
        Tuple of (performance_summary dict, gap_percentage)

        performance_summary includes top_store, bottom_store, and their metrics

    Example:
        >>> gap_info, gap_pct = calculate_performance_gap(store_revenue)
        >>> print(f"Performance gap: {gap_pct:.1f}%")
    """
    # Ensure sorted by revenue
    sorted_df = store_revenue_df.sort_values('total_revenue', ascending=False)

    top_store = sorted_df.iloc[0]
    bottom_store = sorted_df.iloc[-1]

    performance_summary = {
        'top_store_name': top_store['store_name'],
        'top_store_revenue': top_store['total_revenue'],
        'top_store_share': top_store['revenue_share_pct'],
        'bottom_store_name': bottom_store['store_name'],
        'bottom_store_revenue': bottom_store['total_revenue'],
        'bottom_store_share': bottom_store['revenue_share_pct']
    }

    # Calculate gap percentage
    gap_percentage = (
        (top_store['total_revenue'] - bottom_store['total_revenue'])
        / bottom_store['total_revenue']
        * 100
    )

    return performance_summary, gap_percentage


def calculate_revenue_per_customer(
    sales_df: pd.DataFrame,
    groupby_column: Optional[str] = None
) -> pd.DataFrame:
    """
    Calculate revenue per customer metric.

    Args:
        sales_df: DataFrame with sales transactions
        groupby_column: Optional column to group by (e.g., 'store_id', 'product_category')

    Returns:
        DataFrame with revenue per customer metrics

    Note:
        This function assumes sales_amount represents per-transaction revenue
        and customer_count is available (though may have missing values)

    Example:
        >>> rpc = calculate_revenue_per_customer(sales_df, groupby_column='store_id')
    """
    if groupby_column:
        # Group by specified column
        metrics = sales_df.groupby(groupby_column).agg({
            'sales_amount': ['sum', 'mean'],
            'transaction_id': 'count'
        }).reset_index()

        metrics.columns = [
            groupby_column, 'total_revenue',
            'avg_transaction', 'num_transactions'
        ]
    else:
        # Overall metrics
        metrics = pd.DataFrame({
            'total_revenue': [sales_df['sales_amount'].sum()],
            'avg_transaction': [sales_df['sales_amount'].mean()],
            'num_transactions': [len(sales_df)]
        })

    return metrics
