"""
freshcart_helpers.py
====================
Helper functions for displaying query results and creating plots.
Import this module in the FreshCart DuckDB notebook to keep cells clean.

Usage in notebook:
    from freshcart_helpers import show, plot_bar, plot_line, plot_pie, plot_hbar
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML

# ─── Global Style Settings ───────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)
plt.rcParams.update({
    "figure.figsize": (9, 5),
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.dpi": 110,
})

# Color palette for consistent styling
COLORS = sns.color_palette("Set2", 10)


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def show(df, title=None, max_rows=50):
    """
    Display a DataFrame as a nicely formatted HTML table with row numbers.

    Parameters
    ----------
    df : pd.DataFrame
        The result set to display.
    title : str, optional
        A title displayed above the table.
    max_rows : int
        Maximum rows to show (default 50).
    """
    if df is None or df.empty:
        print("(No results)")
        return

    display_df = df.head(max_rows).copy()
    display_df.index = range(1, len(display_df) + 1)
    display_df.index.name = "#"

    style = """
    <style>
        .freshcart-table {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            font-size: 12px;
            margin: 8px 0 16px 0;
        }
        .freshcart-table th {
            background-color: #2c3e50;
            color: white;
            padding: 8px 12px;
            text-align: left;
            font-weight: 600;
        }
        .freshcart-table td {
            padding: 6px 12px;
            border-bottom: 1px solid #ecf0f1;
        }
        .freshcart-table tr:nth-child(even) { background-color: #f8f9fa; }
        .freshcart-table tr:hover { background-color: #ebf5fb; }
        .freshcart-title {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            font-size: 14px;
            font-weight: 700;
            color: #2c3e50;
            margin: 12px 0 4px 0;
            padding-bottom: 4px;
            border-bottom: 2px solid #3498db;
            display: inline-block;
        }
    </style>
    """
    html = style
    if title:
        html += f'<div class="freshcart-title">{title}</div>\n'
    html += display_df.to_html(classes="freshcart-table", border=0)

    if len(df) > max_rows:
        html += f'<p style="color:#7f8c8d; font-size:11px;">Showing {max_rows} of {len(df)} rows.</p>'

    display(HTML(html))


# ═══════════════════════════════════════════════════════════════════════════════
# PLOTTING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def plot_bar(df, x, y, title="", xlabel=None, ylabel=None, color=None, rotate_x=0, figsize=None):
    """
    Vertical bar chart from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
    x : str   – column for x-axis categories
    y : str   – column for bar heights
    title : str
    xlabel, ylabel : str
    color : str or list – bar color(s)
    rotate_x : int – rotation angle for x labels
    figsize : tuple
    """
    fig, ax = plt.subplots(figsize=figsize or (9, 5))
    bars = ax.bar(df[x].astype(str), df[y], color=color or COLORS[0], edgecolor="white", width=0.6)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:,.2f}' if isinstance(height, float) else f'{height:,}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, color='#2c3e50')

    ax.set_title(title, fontweight='bold', pad=12)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    if rotate_x:
        plt.xticks(rotation=rotate_x, ha='right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


def plot_hbar(df, label_col, value_col, title="", xlabel=None, color=None, figsize=None):
    """
    Horizontal bar chart – great for ranked lists.
    """
    fig, ax = plt.subplots(figsize=figsize or (9, 5))
    y_pos = range(len(df))
    ax.barh(y_pos, df[value_col], color=color or COLORS[1], edgecolor="white", height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df[label_col].astype(str))
    ax.invert_yaxis()
    ax.set_title(title, fontweight='bold', pad=12)
    ax.set_xlabel(xlabel or value_col)

    # Value labels
    for i, v in enumerate(df[value_col]):
        ax.text(v + max(df[value_col]) * 0.01, i, f'{v:,.2f}' if isinstance(v, float) else f'{v:,}',
                va='center', fontsize=9, color='#2c3e50')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


def plot_line(df, x, y, title="", xlabel=None, ylabel=None, marker='o', figsize=None):
    """
    Line chart – ideal for time series.
    """
    fig, ax = plt.subplots(figsize=figsize or (10, 5))
    ax.plot(df[x].astype(str), df[y], marker=marker, color=COLORS[2],
            linewidth=2, markersize=6, markerfacecolor=COLORS[3])
    ax.fill_between(range(len(df)), df[y], alpha=0.08, color=COLORS[2])
    ax.set_title(title, fontweight='bold', pad=12)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.xticks(rotation=45, ha='right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


def plot_pie(df, labels_col, values_col, title="", figsize=None):
    """
    Pie chart – for share/composition analysis.
    """
    fig, ax = plt.subplots(figsize=figsize or (7, 7))
    wedges, texts, autotexts = ax.pie(
        df[values_col], labels=df[labels_col],
        autopct='%1.1f%%', startangle=140,
        colors=COLORS[:len(df)],
        textprops={'fontsize': 10},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
    )
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    ax.set_title(title, fontweight='bold', pad=16)
    plt.tight_layout()
    plt.show()


def plot_grouped_bar(df, x, columns, title="", xlabel=None, ylabel=None, figsize=None):
    """
    Grouped bar chart – compare multiple measures side by side.
    """
    fig, ax = plt.subplots(figsize=figsize or (10, 5))
    x_vals = range(len(df))
    width = 0.8 / len(columns)

    for i, col in enumerate(columns):
        offset = (i - len(columns) / 2 + 0.5) * width
        bars = ax.bar([xv + offset for xv in x_vals], df[col],
                      width=width, label=col, color=COLORS[i], edgecolor="white")

    ax.set_xticks(x_vals)
    ax.set_xticklabels(df[x].astype(str), rotation=45, ha='right')
    ax.set_title(title, fontweight='bold', pad=12)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or "")
    ax.legend(frameon=True, framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


def plot_scatter(df, x, y, title="", xlabel=None, ylabel=None, hue=None, figsize=None):
    """
    Scatter plot with optional color grouping.
    """
    fig, ax = plt.subplots(figsize=figsize or (9, 5))
    if hue and hue in df.columns:
        for i, grp in enumerate(df[hue].unique()):
            subset = df[df[hue] == grp]
            ax.scatter(subset[x], subset[y], label=grp, color=COLORS[i % len(COLORS)],
                       s=60, alpha=0.75, edgecolors='white', linewidth=0.5)
        ax.legend(frameon=True, framealpha=0.9)
    else:
        ax.scatter(df[x], df[y], color=COLORS[4], s=60, alpha=0.75, edgecolors='white', linewidth=0.5)
    ax.set_title(title, fontweight='bold', pad=12)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()
