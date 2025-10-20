#!/usr/bin/env python3
"""
Complete EDA Analysis Script for 10-Store Dataset
Generates all metrics, visualizations, and summary tables
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Set visualization parameters
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (10, 6)
sns.set_style('whitegrid')
sns.set_palette('Set2')

def main():
    print("="*80)
    print("MULTI-STORE FASHION RETAIL SALES ANALYSIS - 10 STORES")
    print("January 2024 Complete EDA")
    print("="*80)

    # Define paths
    DATA_DIR = Path('data/processed')
    REPORTS_DIR = Path('reports/assets')
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load data
    print("\n1. Loading data...")
    sales_df = pd.read_csv(DATA_DIR / 'sales_clean.csv', parse_dates=['date'])
    stores_df = pd.read_csv(DATA_DIR / 'stores.csv')
    products_df = pd.read_csv(DATA_DIR / 'products.csv')

    print(f"   Sales transactions: {len(sales_df):,} rows")
    print(f"   Stores: {len(stores_df)} stores")
    print(f"   Product categories: {len(products_df)} categories")

    # Merge sales with store information
    sales_with_stores = sales_df.merge(stores_df, on='store_id', how='left')

    # Calculate key business metrics
    print("\n2. Calculating business metrics...")
    total_revenue = sales_df['sales_amount'].sum()
    total_transactions = len(sales_df)
    avg_transaction_value = sales_df['sales_amount'].mean()
    median_transaction_value = sales_df['sales_amount'].median()
    num_stores_with_sales = sales_df['store_id'].nunique()
    date_range = f"{sales_df['date'].min().strftime('%Y-%m-%d')} to {sales_df['date'].max().strftime('%Y-%m-%d')}"

    print(f"   Total Revenue: ¥{total_revenue:,.0f}")
    print(f"   Total Transactions: {total_transactions:,}")
    print(f"   Average Transaction: ¥{avg_transaction_value:,.0f}")
    print(f"   Active Stores: {num_stores_with_sales}")

    # Store performance analysis
    print("\n3. Analyzing store performance...")
    store_revenue = sales_with_stores.groupby(['store_id', 'store_name_en', 'region']).agg({
        'sales_amount': ['sum', 'mean', 'count']
    }).reset_index()
    store_revenue.columns = ['store_id', 'store_name', 'region', 'total_revenue', 'avg_transaction', 'num_transactions']
    store_revenue = store_revenue.sort_values('total_revenue', ascending=False)
    store_revenue['revenue_share_pct'] = (store_revenue['total_revenue'] / store_revenue['total_revenue'].sum() * 100).round(2)

    # Region performance analysis
    print("\n4. Analyzing regional performance...")
    region_revenue = sales_with_stores.groupby('region').agg({
        'sales_amount': ['sum', 'mean', 'count'],
        'store_id': 'nunique'
    }).reset_index()
    region_revenue.columns = ['region', 'total_revenue', 'avg_transaction', 'num_transactions', 'num_stores']
    region_revenue = region_revenue.sort_values('total_revenue', ascending=False)
    region_revenue['revenue_share_pct'] = (region_revenue['total_revenue'] / region_revenue['total_revenue'].sum() * 100).round(2)

    # Category performance analysis
    print("\n5. Analyzing category performance...")
    category_revenue = sales_df.groupby('product_category').agg({
        'sales_amount': ['sum', 'mean', 'count']
    }).reset_index()
    category_revenue.columns = ['category', 'total_revenue', 'avg_transaction', 'num_transactions']
    category_revenue = category_revenue.sort_values('total_revenue', ascending=False)
    category_revenue['revenue_share_pct'] = (category_revenue['total_revenue'] / category_revenue['total_revenue'].sum() * 100).round(2)

    # Temporal analysis
    print("\n6. Analyzing temporal patterns...")
    daily_revenue = sales_df.groupby('date')['sales_amount'].sum().reset_index()
    daily_revenue.columns = ['date', 'revenue']

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_revenue = sales_df.groupby('day_of_week').agg({
        'sales_amount': ['sum', 'mean', 'count']
    }).reset_index()
    dow_revenue.columns = ['day_of_week', 'total_revenue', 'avg_transaction', 'num_transactions']
    dow_revenue['day_of_week'] = pd.Categorical(dow_revenue['day_of_week'], categories=day_order, ordered=True)
    dow_revenue = dow_revenue.sort_values('day_of_week')

    # Weekend analysis
    weekend_comparison = sales_df.groupby('is_weekend').agg({
        'sales_amount': ['sum', 'mean', 'count']
    }).reset_index()
    weekend_comparison.columns = ['is_weekend', 'total_revenue', 'avg_transaction', 'num_transactions']
    weekend_comparison['period'] = weekend_comparison['is_weekend'].map({True: 'Weekend', False: 'Weekday'})

    weekend_days = sales_df[sales_df['is_weekend']]['date'].dt.date.nunique()
    weekday_days = sales_df[~sales_df['is_weekend']]['date'].dt.date.nunique()
    weekend_comparison['avg_revenue_per_day'] = weekend_comparison.apply(
        lambda row: row['total_revenue'] / (weekend_days if row['is_weekend'] else weekday_days), axis=1
    )

    # Category by store
    category_by_store = sales_with_stores.groupby(['store_name_en', 'product_category'])['sales_amount'].sum().unstack(fill_value=0)

    # Export summary tables
    print("\n7. Exporting summary tables...")
    store_revenue.to_csv('reports/store_performance_summary.csv', index=False)
    region_revenue.to_csv('reports/region_performance_summary.csv', index=False)
    category_revenue.to_csv('reports/category_performance_summary.csv', index=False)
    print("   Summary tables exported to reports/")

    # Generate visualizations
    print("\n8. Generating visualizations...")

    # Visualization 1: Daily Revenue Trend
    print("   Creating daily_revenue_trend.png...")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_revenue['date'], daily_revenue['revenue'], marker='o', linewidth=2, markersize=6, color='#2E86AB')
    ax.axhline(y=daily_revenue['revenue'].mean(), color='red', linestyle='--', linewidth=1.5, label='Average Daily Revenue', alpha=0.7)
    ax.set_title('Daily Revenue Trend - January 2024 (10 Stores)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Revenue (¥)', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000:.0f}K'))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / 'daily_revenue_trend.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Visualization 2: Revenue by Store
    print("   Creating revenue_by_store.png...")
    fig, ax = plt.subplots(figsize=(10, 7))
    colors = sns.color_palette('viridis', len(store_revenue))
    bars = ax.barh(store_revenue['store_name'], store_revenue['total_revenue'], color=colors)
    for i, (bar, revenue, pct) in enumerate(zip(bars, store_revenue['total_revenue'], store_revenue['revenue_share_pct'])):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                f'  ¥{revenue/1000000:.1f}M ({pct}%)',
                va='center', fontsize=9, fontweight='bold')
    ax.set_title('Total Revenue by Store - January 2024 (10 Stores)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Revenue (¥)', fontsize=12)
    ax.set_ylabel('Store', fontsize=12)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / 'revenue_by_store.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Visualization 3: Revenue by Region
    print("   Creating revenue_by_region.png...")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette('Set2', len(region_revenue))
    bars = ax.bar(region_revenue['region'], region_revenue['total_revenue'], color=colors, edgecolor='black', linewidth=1.2)
    for bar, revenue, pct in zip(bars, region_revenue['total_revenue'], region_revenue['revenue_share_pct']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height,
                f'¥{revenue/1000000:.1f}M\n({pct}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.set_title('Total Revenue by Region - January 2024 (10 Stores)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Region', fontsize=12)
    ax.set_ylabel('Revenue (¥)', fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / 'revenue_by_region.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Visualization 4: Revenue by Product Category
    print("   Creating revenue_by_category.png...")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette('pastel', len(category_revenue))
    bars = ax.barh(category_revenue['category'], category_revenue['total_revenue'], color=colors, edgecolor='black', linewidth=1.2)
    for bar, revenue, pct in zip(bars, category_revenue['total_revenue'], category_revenue['revenue_share_pct']):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                f'  ¥{revenue/1000000:.1f}M ({pct}%)',
                va='center', fontsize=10, fontweight='bold')
    ax.set_title('Total Revenue by Product Category - January 2024 (10 Stores)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Revenue (¥)', fontsize=12)
    ax.set_ylabel('Product Category', fontsize=12)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / 'revenue_by_category.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Visualization 5: Revenue by Day of Week
    print("   Creating revenue_by_day_of_week.png...")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#A6CEE3' if day in ['Saturday', 'Sunday'] else '#1F78B4' for day in dow_revenue['day_of_week']]
    bars = ax.bar(dow_revenue['day_of_week'], dow_revenue['total_revenue'], color=colors, edgecolor='black', linewidth=1.2)
    for bar, revenue in zip(bars, dow_revenue['total_revenue']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height,
                f'¥{revenue/1000000:.1f}M',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.set_title('Total Revenue by Day of Week - January 2024 (10 Stores)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Day of Week', fontsize=12)
    ax.set_ylabel('Revenue (¥)', fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax.grid(True, alpha=0.3, axis='y')
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#1F78B4', label='Weekday'),
                       Patch(facecolor='#A6CEE3', label='Weekend')]
    ax.legend(handles=legend_elements, loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / 'revenue_by_day_of_week.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Visualization 6: Weekend vs Weekday Comparison
    print("   Creating weekend_vs_weekday.png...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    colors_1 = ['#2E86AB', '#A23B72']
    bars1 = ax1.bar(weekend_comparison['period'], weekend_comparison['total_revenue'], color=colors_1, edgecolor='black', linewidth=1.2)
    for bar, revenue in zip(bars1, weekend_comparison['total_revenue']):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height,
                 f'¥{revenue/1000000:.1f}M',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax1.set_title('Total Revenue: Weekend vs Weekday', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Revenue (¥)', fontsize=11)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax1.grid(True, alpha=0.3, axis='y')

    bars2 = ax2.bar(weekend_comparison['period'], weekend_comparison['num_transactions'], color=colors_1, edgecolor='black', linewidth=1.2)
    for bar, count in zip(bars2, weekend_comparison['num_transactions']):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height,
                 f'{int(count):,}',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax2.set_title('Transaction Count: Weekend vs Weekday', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Number of Transactions', fontsize=11)
    ax2.grid(True, alpha=0.3, axis='y')

    fig.suptitle('Weekend vs Weekday Performance - January 2024 (10 Stores)', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / 'weekend_vs_weekday.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Visualization 7: Category Mix by Store
    print("   Creating category_mix_by_store.png...")
    fig, ax = plt.subplots(figsize=(12, 8))
    category_by_store_pct = category_by_store.div(category_by_store.sum(axis=1), axis=0) * 100
    category_by_store_pct.plot(kind='barh', stacked=True, ax=ax,
                               colormap='Set3', edgecolor='black', linewidth=0.5)
    ax.set_title('Product Category Mix by Store (% of Store Revenue) - January 2024 (10 Stores)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Percentage of Store Revenue (%)', fontsize=12)
    ax.set_ylabel('Store', fontsize=12)
    ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_xlim(0, 100)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / 'category_mix_by_store.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Visualization 8: Top and Bottom Performers
    print("   Creating top_bottom_stores.png...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    top_stores = store_revenue.head(5)
    colors_top = sns.color_palette('Greens_d', len(top_stores))[::-1]
    bars1 = ax1.barh(top_stores['store_name'], top_stores['total_revenue'], color=colors_top, edgecolor='black', linewidth=1.2)
    for bar, revenue, pct in zip(bars1, top_stores['total_revenue'], top_stores['revenue_share_pct']):
        ax1.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                 f'  ¥{revenue/1000000:.1f}M ({pct}%)',
                 va='center', fontsize=10, fontweight='bold')
    ax1.set_title('Top 5 Performing Stores', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Revenue (¥)', fontsize=11)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax1.grid(True, alpha=0.3, axis='x')
    ax1.invert_yaxis()

    bottom_stores = store_revenue.tail(5)
    colors_bottom = sns.color_palette('Reds_d', len(bottom_stores))
    bars2 = ax2.barh(bottom_stores['store_name'], bottom_stores['total_revenue'], color=colors_bottom, edgecolor='black', linewidth=1.2)
    for bar, revenue, pct in zip(bars2, bottom_stores['total_revenue'], bottom_stores['revenue_share_pct']):
        ax2.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                 f'  ¥{revenue/1000000:.1f}M ({pct}%)',
                 va='center', fontsize=10, fontweight='bold')
    ax2.set_title('Bottom 5 Performing Stores', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Revenue (¥)', fontsize=11)
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.invert_yaxis()

    fig.suptitle('Store Performance Benchmarking - January 2024 (10 Stores)', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / 'top_bottom_stores.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nAll 8 visualizations saved to: {REPORTS_DIR}")
    print("All summary tables saved to: reports/")
    print("\nKey Metrics Summary:")
    print(f"  Total Revenue: ¥{total_revenue:,.0f}")
    print(f"  Total Transactions: {total_transactions:,}")
    print(f"  Active Stores: {num_stores_with_sales}")
    print(f"  Regions Covered: {region_revenue['region'].nunique()}")
    print(f"  Top Store: {store_revenue.iloc[0]['store_name']} (¥{store_revenue.iloc[0]['total_revenue']/1000000:.1f}M)")
    print(f"  Top Region: {region_revenue.iloc[0]['region']} (¥{region_revenue.iloc[0]['total_revenue']/1000000:.1f}M)")
    print(f"  Top Category: {category_revenue.iloc[0]['category']} (¥{category_revenue.iloc[0]['total_revenue']/1000000:.1f}M)")

    # Return key data for report generation
    return {
        'total_revenue': total_revenue,
        'total_transactions': total_transactions,
        'store_revenue': store_revenue,
        'region_revenue': region_revenue,
        'category_revenue': category_revenue,
        'weekend_comparison': weekend_comparison
    }

if __name__ == "__main__":
    main()
