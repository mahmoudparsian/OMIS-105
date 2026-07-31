"""
plot_utils.py
=============
Utility functions for creating beautiful plots from
DuckDB query result DataFrames in Jupyter Notebooks.

Usage in notebook:
    from plot_utils import plot_bar, plot_horizontal_bar, plot_pie,
                           plot_line, plot_scatter, plot_grouped_bar,
                           plot_histogram, plot_stacked_bar
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


# ─── Global Style Settings ───────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 100,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Color palette (professional, colorblind-friendly)
COLORS = [
    '#2196F3', '#FF9800', '#4CAF50', '#E91E63', '#9C27B0',
    '#00BCD4', '#FF5722', '#607D8B', '#8BC34A', '#FFC107',
    '#3F51B5', '#795548', '#009688', '#CDDC39', '#F44336',
]


def _get_colors(n):
    """Return n colors from the palette, cycling if needed."""
    return [COLORS[i % len(COLORS)] for i in range(n)]


def plot_bar(df, x_col, y_col, title="", xlabel="", ylabel="",
             figsize=(10, 5), rotate_labels=45, color=None, show_values=True):
    """
    Vertical bar chart.

    Parameters
    ----------
    df : pandas.DataFrame
    x_col : str - column for x-axis categories
    y_col : str - column for y-axis values
    title, xlabel, ylabel : str
    figsize : tuple
    rotate_labels : int - rotation angle for x labels
    color : str or None - single color; if None uses palette
    show_values : bool - show values on top of bars
    """
    fig, ax = plt.subplots(figsize=figsize)
    colors = color if color else _get_colors(len(df))
    bars = ax.bar(df[x_col].astype(str), df[y_col], color=colors,
                  edgecolor='white', linewidth=0.8)

    if show_values:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:,.0f}' if isinstance(height, (int, float)) else str(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 4), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, color='#333')

    ax.set_title(title, pad=15)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=rotate_labels)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()


def plot_horizontal_bar(df, label_col, value_col, title="", xlabel="",
                        ylabel="", figsize=(10, 6), color=None, show_values=True):
    """
    Horizontal bar chart (great for ranked data).
    """
    fig, ax = plt.subplots(figsize=figsize)
    colors = color if color else _get_colors(len(df))
    y_pos = range(len(df))
    bars = ax.barh(y_pos, df[value_col], color=colors,
                   edgecolor='white', linewidth=0.8)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(df[label_col].astype(str))

    if show_values:
        for bar in bars:
            width = bar.get_width()
            ax.annotate(f'{width:,.0f}',
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(5, 0), textcoords="offset points",
                        ha='left', va='center', fontsize=9, color='#333')

    ax.set_title(title, pad=15)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()


def plot_pie(df, label_col, value_col, title="", figsize=(8, 8),
             show_pct=True, explode_top=False):
    """
    Pie chart with percentages.
    """
    fig, ax = plt.subplots(figsize=figsize)
    colors = _get_colors(len(df))
    explode = None
    if explode_top:
        explode = [0.05] + [0] * (len(df) - 1)

    wedges, texts, autotexts = ax.pie(
        df[value_col], labels=df[label_col], colors=colors,
        autopct='%1.1f%%' if show_pct else '',
        startangle=90, explode=explode,
        shadow=False, textprops={'fontsize': 10}
    )
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax.set_title(title, pad=20, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_line(df, x_col, y_col, title="", xlabel="", ylabel="",
              figsize=(10, 5), marker='o', color=None):
    """
    Line chart (good for trends over time).
    """
    fig, ax = plt.subplots(figsize=figsize)
    c = color if color else COLORS[0]
    ax.plot(df[x_col].astype(str), df[y_col], marker=marker,
            color=c, linewidth=2, markersize=6, markerfacecolor='white',
            markeredgecolor=c, markeredgewidth=2)

    ax.set_title(title, pad=15)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=45)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.grid(alpha=0.3, linestyle='--')
    ax.fill_between(range(len(df)), df[y_col], alpha=0.1, color=c)
    plt.tight_layout()
    plt.show()


def plot_scatter(df, x_col, y_col, title="", xlabel="", ylabel="",
                 figsize=(10, 6), color=None, label_col=None):
    """
    Scatter plot with optional labels.
    """
    fig, ax = plt.subplots(figsize=figsize)
    c = color if color else COLORS[0]
    ax.scatter(df[x_col], df[y_col], color=c, s=80, alpha=0.7,
               edgecolors='white', linewidth=0.5)

    if label_col:
        for _, row in df.iterrows():
            ax.annotate(row[label_col], (row[x_col], row[y_col]),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=8, alpha=0.8)

    ax.set_title(title, pad=15)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()


def plot_grouped_bar(df, group_col, category_col, value_col, title="",
                     xlabel="", ylabel="", figsize=(12, 6)):
    """
    Grouped bar chart for comparing categories across groups.
    """
    fig, ax = plt.subplots(figsize=figsize)
    categories = df[category_col].unique()
    groups = df[group_col].unique()
    n_groups = len(groups)
    bar_width = 0.8 / len(categories)

    for i, cat in enumerate(categories):
        subset = df[df[category_col] == cat]
        positions = np.arange(n_groups) + i * bar_width
        values = []
        for g in groups:
            v = subset[subset[group_col] == g][value_col]
            values.append(v.values[0] if len(v) > 0 else 0)
        ax.bar(positions, values, bar_width, label=cat,
               color=COLORS[i % len(COLORS)], edgecolor='white', linewidth=0.5)

    ax.set_xticks(np.arange(n_groups) + bar_width * (len(categories) - 1) / 2)
    ax.set_xticklabels(groups, rotation=45, ha='right')
    ax.set_title(title, pad=15)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(title=category_col, bbox_to_anchor=(1.02, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()


def plot_histogram(df, col, title="", xlabel="", ylabel="Frequency",
                   figsize=(10, 5), bins=15, color=None):
    """
    Histogram for distribution analysis.
    """
    fig, ax = plt.subplots(figsize=figsize)
    c = color if color else COLORS[0]
    ax.hist(df[col], bins=bins, color=c, edgecolor='white',
            linewidth=0.8, alpha=0.85)

    ax.set_title(title, pad=15)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()


def plot_stacked_bar(df, x_col, columns, title="", xlabel="", ylabel="",
                     figsize=(12, 6)):
    """
    Stacked bar chart.

    Parameters
    ----------
    df : DataFrame with x_col and numeric columns to stack
    columns : list of column names to stack
    """
    fig, ax = plt.subplots(figsize=figsize)
    bottom = np.zeros(len(df))

    for i, col in enumerate(columns):
        ax.bar(df[x_col].astype(str), df[col], bottom=bottom,
               label=col, color=COLORS[i % len(COLORS)],
               edgecolor='white', linewidth=0.5)
        bottom += df[col].values

    ax.set_title(title, pad=15)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=45)
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()
