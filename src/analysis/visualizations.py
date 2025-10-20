"""
Reusable visualization functions for retail sales analysis.

This module provides functions to create professional, high-quality charts
for presenting retail sales insights.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, Tuple, List


# Default visualization settings
DEFAULT_DPI = 300
DEFAULT_FIGSIZE = (10, 6)
DEFAULT_COLOR_PALETTE = 'Set2'


def setup_plot_style():
    """
    Configure matplotlib and seaborn with professional styling for reports.

    Example:
        >>> setup_plot_style()
        >>> # Now all subsequent plots will use these settings
    """
    plt.rcParams['figure.dpi'] = DEFAULT_DPI
    plt.rcParams['savefig.dpi'] = DEFAULT_DPI
    plt.rcParams['font.size'] = 10
    plt.rcParams['figure.figsize'] = DEFAULT_FIGSIZE
    sns.set_style('whitegrid')
    sns.set_palette(DEFAULT_COLOR_PALETTE)


def plot_daily_revenue_trend(
    daily_revenue_df: pd.DataFrame,
    save_path: Optional[Path] = None,
    show_average: bool = True
) -> None:
    """
    Create a line chart showing daily revenue trend over time.

    Args:
        daily_revenue_df: DataFrame with columns 'date' and 'revenue'
        save_path: Optional path to save the chart (PNG file)
        show_average: If True, shows average daily revenue as horizontal line

    Example:
        >>> plot_daily_revenue_trend(daily_revenue, save_path=Path('reports/assets/trend.png'))
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        daily_revenue_df['date'],
        daily_revenue_df['revenue'],
        marker='o',
        linewidth=2,
        markersize=6,
        color='#2E86AB'
    )

    if show_average:
        avg_revenue = daily_revenue_df['revenue'].mean()
        ax.axhline(
            y=avg_revenue,
            color='red',
            linestyle='--',
            linewidth=1.5,
            label=f'Average Daily Revenue: ¥{avg_revenue/1000:.0f}K',
            alpha=0.7
        )
        ax.legend()

    ax.set_title('Daily Revenue Trend - January 2024', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Revenue (¥)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000:.0f}K'))

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=DEFAULT_DPI, bbox_inches='tight')

    plt.show()


def plot_revenue_by_store(
    store_revenue_df: pd.DataFrame,
    save_path: Optional[Path] = None,
    show_percentages: bool = True
) -> None:
    """
    Create a horizontal bar chart showing revenue by store.

    Args:
        store_revenue_df: DataFrame with store revenue metrics (from calculate_revenue_by_store)
        save_path: Optional path to save the chart
        show_percentages: If True, shows revenue share percentages on bars

    Example:
        >>> plot_revenue_by_store(store_revenue, save_path=Path('reports/assets/store_revenue.png'))
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = sns.color_palette('viridis', len(store_revenue_df))
    bars = ax.barh(
        store_revenue_df['store_name'],
        store_revenue_df['total_revenue'],
        color=colors
    )

    # Add revenue labels on bars
    for bar, revenue, pct in zip(
        bars,
        store_revenue_df['total_revenue'],
        store_revenue_df['revenue_share_pct']
    ):
        label = f'  ¥{revenue/1000000:.1f}M'
        if show_percentages:
            label += f' ({pct}%)'

        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height()/2,
            label,
            va='center',
            fontsize=9,
            fontweight='bold'
        )

    ax.set_title('Total Revenue by Store - January 2024', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Revenue (¥)', fontsize=12)
    ax.set_ylabel('Store', fontsize=12)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=DEFAULT_DPI, bbox_inches='tight')

    plt.show()


def plot_revenue_by_region(
    region_revenue_df: pd.DataFrame,
    save_path: Optional[Path] = None
) -> None:
    """
    Create a bar chart showing revenue by geographic region.

    Args:
        region_revenue_df: DataFrame with regional revenue metrics
        save_path: Optional path to save the chart

    Example:
        >>> plot_revenue_by_region(region_revenue, save_path=Path('reports/assets/region.png'))
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = sns.color_palette('Set2', len(region_revenue_df))
    bars = ax.bar(
        region_revenue_df['region'],
        region_revenue_df['total_revenue'],
        color=colors,
        edgecolor='black',
        linewidth=1.2
    )

    # Add revenue labels
    for bar, revenue, pct in zip(
        bars,
        region_revenue_df['total_revenue'],
        region_revenue_df['revenue_share_pct']
    ):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f'¥{revenue/1000000:.1f}M\n({pct}%)',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )

    ax.set_title('Total Revenue by Region - January 2024', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Region', fontsize=12)
    ax.set_ylabel('Revenue (¥)', fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax.grid(True, alpha=0.3, axis='y')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=DEFAULT_DPI, bbox_inches='tight')

    plt.show()


def plot_revenue_by_category(
    category_revenue_df: pd.DataFrame,
    save_path: Optional[Path] = None,
    chart_type: str = 'bar'
) -> None:
    """
    Create a chart showing revenue by product category.

    Args:
        category_revenue_df: DataFrame with category revenue metrics
        save_path: Optional path to save the chart
        chart_type: Type of chart - 'bar' or 'pie'

    Example:
        >>> plot_revenue_by_category(category_revenue, chart_type='bar')
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    if chart_type == 'pie':
        colors = sns.color_palette('pastel', len(category_revenue_df))
        wedges, texts, autotexts = ax.pie(
            category_revenue_df['total_revenue'],
            labels=category_revenue_df['category'],
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )

        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')

        ax.set_title('Revenue by Product Category - January 2024', fontsize=14, fontweight='bold', pad=20)

    else:  # bar chart
        colors = sns.color_palette('pastel', len(category_revenue_df))
        bars = ax.barh(
            category_revenue_df['category'],
            category_revenue_df['total_revenue'],
            color=colors,
            edgecolor='black',
            linewidth=1.2
        )

        # Add labels
        for bar, revenue, pct in zip(
            bars,
            category_revenue_df['total_revenue'],
            category_revenue_df['revenue_share_pct']
        ):
            ax.text(
                bar.get_width(),
                bar.get_y() + bar.get_height()/2,
                f'  ¥{revenue/1000000:.1f}M ({pct}%)',
                va='center',
                fontsize=10,
                fontweight='bold'
            )

        ax.set_title('Total Revenue by Product Category - January 2024', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Revenue (¥)', fontsize=12)
        ax.set_ylabel('Product Category', fontsize=12)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
        ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=DEFAULT_DPI, bbox_inches='tight')

    plt.show()


def plot_day_of_week_revenue(
    dow_revenue_df: pd.DataFrame,
    save_path: Optional[Path] = None,
    highlight_weekend: bool = True
) -> None:
    """
    Create a bar chart showing revenue by day of week.

    Args:
        dow_revenue_df: DataFrame with day-of-week revenue metrics
        save_path: Optional path to save the chart
        highlight_weekend: If True, colors weekend bars differently

    Example:
        >>> plot_day_of_week_revenue(dow_revenue, highlight_weekend=True)
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    if highlight_weekend:
        colors = [
            '#A6CEE3' if day in ['Saturday', 'Sunday'] else '#1F78B4'
            for day in dow_revenue_df['day_of_week']
        ]
    else:
        colors = sns.color_palette('Set2', len(dow_revenue_df))

    bars = ax.bar(
        dow_revenue_df['day_of_week'],
        dow_revenue_df['total_revenue'],
        color=colors,
        edgecolor='black',
        linewidth=1.2
    )

    # Add revenue labels
    for bar, revenue in zip(bars, dow_revenue_df['total_revenue']):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f'¥{revenue/1000000:.1f}M',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )

    ax.set_title('Total Revenue by Day of Week - January 2024', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Day of Week', fontsize=12)
    ax.set_ylabel('Revenue (¥)', fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax.grid(True, alpha=0.3, axis='y')

    if highlight_weekend:
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#1F78B4', label='Weekday'),
            Patch(facecolor='#A6CEE3', label='Weekend')
        ]
        ax.legend(handles=legend_elements, loc='upper left')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=DEFAULT_DPI, bbox_inches='tight')

    plt.show()


def plot_weekend_vs_weekday(
    weekend_comparison_df: pd.DataFrame,
    save_path: Optional[Path] = None
) -> None:
    """
    Create a comparison chart showing weekend vs weekday performance.

    Args:
        weekend_comparison_df: DataFrame with weekend vs weekday metrics
        save_path: Optional path to save the chart

    Example:
        >>> plot_weekend_vs_weekday(comparison_df)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    colors = ['#2E86AB', '#A23B72']

    # Revenue comparison
    bars1 = ax1.bar(
        weekend_comparison_df['period'],
        weekend_comparison_df['total_revenue'],
        color=colors,
        edgecolor='black',
        linewidth=1.2
    )

    for bar, revenue in zip(bars1, weekend_comparison_df['total_revenue']):
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f'¥{revenue/1000000:.1f}M',
            ha='center',
            va='bottom',
            fontsize=11,
            fontweight='bold'
        )

    ax1.set_title('Total Revenue: Weekend vs Weekday', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Revenue (¥)', fontsize=11)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax1.grid(True, alpha=0.3, axis='y')

    # Transaction count comparison
    bars2 = ax2.bar(
        weekend_comparison_df['period'],
        weekend_comparison_df['num_transactions'],
        color=colors,
        edgecolor='black',
        linewidth=1.2
    )

    for bar, count in zip(bars2, weekend_comparison_df['num_transactions']):
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f'{int(count):,}',
            ha='center',
            va='bottom',
            fontsize=11,
            fontweight='bold'
        )

    ax2.set_title('Transaction Count: Weekend vs Weekday', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Number of Transactions', fontsize=11)
    ax2.grid(True, alpha=0.3, axis='y')

    fig.suptitle('Weekend vs Weekday Performance - January 2024', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=DEFAULT_DPI, bbox_inches='tight')

    plt.show()


def plot_category_mix_by_store(
    category_mix_df: pd.DataFrame,
    save_path: Optional[Path] = None,
    as_percentage: bool = True
) -> None:
    """
    Create a stacked bar chart showing category mix by store.

    Args:
        category_mix_df: DataFrame with stores as index and categories as columns
        save_path: Optional path to save the chart
        as_percentage: If True, shows percentage; if False, shows absolute values

    Example:
        >>> plot_category_mix_by_store(category_mix, as_percentage=True)
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    if as_percentage:
        plot_data = category_mix_df.div(category_mix_df.sum(axis=1), axis=0) * 100
        xlabel = 'Percentage of Store Revenue (%)'
        xlim = 100
    else:
        plot_data = category_mix_df
        xlabel = 'Revenue (¥)'
        xlim = None

    plot_data.plot(
        kind='barh',
        stacked=True,
        ax=ax,
        colormap='Set3',
        edgecolor='black',
        linewidth=0.5
    )

    ax.set_title(
        'Product Category Mix by Store - January 2024',
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel('Store', fontsize=12)
    ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3, axis='x')

    if xlim:
        ax.set_xlim(0, xlim)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=DEFAULT_DPI, bbox_inches='tight')

    plt.show()


def plot_top_bottom_stores(
    store_revenue_df: pd.DataFrame,
    save_path: Optional[Path] = None,
    num_stores: int = 4
) -> None:
    """
    Create side-by-side comparison of top and bottom performing stores.

    Args:
        store_revenue_df: DataFrame with store revenue metrics
        save_path: Optional path to save the chart
        num_stores: Number of top and bottom stores to display

    Example:
        >>> plot_top_bottom_stores(store_revenue, num_stores=4)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Top stores
    top_stores = store_revenue_df.head(num_stores)
    colors_top = sns.color_palette('Greens_d', len(top_stores))[::-1]
    bars1 = ax1.barh(
        top_stores['store_name'],
        top_stores['total_revenue'],
        color=colors_top,
        edgecolor='black',
        linewidth=1.2
    )

    for bar, revenue, pct in zip(
        bars1,
        top_stores['total_revenue'],
        top_stores['revenue_share_pct']
    ):
        ax1.text(
            bar.get_width(),
            bar.get_y() + bar.get_height()/2,
            f'  ¥{revenue/1000000:.1f}M ({pct}%)',
            va='center',
            fontsize=10,
            fontweight='bold'
        )

    ax1.set_title(f'Top {num_stores} Performing Stores', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Revenue (¥)', fontsize=11)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax1.grid(True, alpha=0.3, axis='x')
    ax1.invert_yaxis()

    # Bottom stores
    bottom_stores = store_revenue_df.tail(num_stores)
    colors_bottom = sns.color_palette('Reds_d', len(bottom_stores))
    bars2 = ax2.barh(
        bottom_stores['store_name'],
        bottom_stores['total_revenue'],
        color=colors_bottom,
        edgecolor='black',
        linewidth=1.2
    )

    for bar, revenue, pct in zip(
        bars2,
        bottom_stores['total_revenue'],
        bottom_stores['revenue_share_pct']
    ):
        ax2.text(
            bar.get_width(),
            bar.get_y() + bar.get_height()/2,
            f'  ¥{revenue/1000000:.1f}M ({pct}%)',
            va='center',
            fontsize=10,
            fontweight='bold'
        )

    ax2.set_title(f'Bottom {num_stores} Performing Stores', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Revenue (¥)', fontsize=11)
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000000:.1f}M'))
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.invert_yaxis()

    fig.suptitle('Store Performance Benchmarking - January 2024', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=DEFAULT_DPI, bbox_inches='tight')

    plt.show()
