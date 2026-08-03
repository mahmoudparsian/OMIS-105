"""
mysql101_helpers.py
====================
Helper functions for the MySQL 101 DuckDB Jupyter Notebook.
Provides clean display (tabulated tables with row numbers) and basic
plotting utilities so the notebook cells stay focused on SQL.

Usage in notebook:
    from mysql101_helpers import display_result, plot_bar, plot_hbar, plot_pie, plot_line

Dependencies: pandas, tabulate, matplotlib, seaborn
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from IPython.display import display, HTML

# ─── Global Style Setup ────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)
plt.rcParams.update({
    "figure.figsize": (9, 4.5),
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.dpi": 100,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# Color palette for consistency
COLORS = sns.color_palette("Set2", 12)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DISPLAY FUNCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display_result(df, title=None, max_rows=25):
    """
    Display a DataFrame as a nicely formatted HTML table with row numbers.

    Parameters
    ----------
    df : pd.DataFrame
        The result set to display.
    title : str, optional
        A title/header shown above the table.
    max_rows : int
        Maximum rows to show (default 25).
    """
    if df is None or df.empty:
        print("⚠️  No results returned.")
        return

    total_rows = len(df)
    show_df = df.head(max_rows).copy()
    show_df.index = range(1, len(show_df) + 1)
    show_df.index.name = "#"

    # Build HTML
    html_parts = []
    if title:
        html_parts.append(
            f'<h4 style="color:#2c3e50; margin-bottom:4px; '
            f'border-bottom:2px solid #27ae60; padding-bottom:4px;">{title}</h4>'
        )

    # Style the table
    styled = (
        show_df.style
        .set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#27ae60"),
                ("color", "white"),
                ("padding", "8px 12px"),
                ("text-align", "center"),
                ("font-size", "11px"),
            ]},
            {"selector": "td", "props": [
                ("padding", "6px 12px"),
                ("text-align", "left"),
                ("font-size", "11px"),
            ]},
            {"selector": "tr:nth-child(even)", "props": [
                ("background-color", "#f0fff4"),
            ]},
            {"selector": "tr:hover", "props": [
                ("background-color", "#d4efdf"),
            ]},
            {"selector": "table", "props": [
                ("border-collapse", "collapse"),
                ("margin", "8px 0"),
                ("box-shadow", "0 1px 3px rgba(0,0,0,0.1)"),
            ]},
        ])
        .format(precision=2)
    )
    html_parts.append(styled.to_html())

    if total_rows > max_rows:
        html_parts.append(
            f'<p style="color:#7f8c8d; font-size:11px;">'
            f'Showing {max_rows} of {total_rows} rows.</p>'
        )
    else:
        html_parts.append(
            f'<p style="color:#7f8c8d; font-size:11px;">'
            f'{total_rows} row(s) returned.</p>'
        )

    display(HTML("".join(html_parts)))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PLOTTING FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def plot_bar(df, x, y, title="", xlabel=None, ylabel=None, color=None, rotate_x=0, figsize=None):
    """
    Vertical bar chart with value labels.
    """
    fig, ax = plt.subplots(figsize=figsize or (9, 4.5))
    bars = ax.bar(df[x].astype(str), df[y],
                  color=color or COLORS[:len(df)],
                  edgecolor="white", linewidth=0.8)

    # Value labels on bars
    for bar in bars:
        height = bar.get_height()
        label = f'{height:,.0f}' if height > 10 else f'{height:.1f}'
        ax.text(bar.get_x() + bar.get_width()/2., height,
                label, ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_title(title, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    if rotate_x:
        plt.xticks(rotation=rotate_x, ha="right")
    plt.tight_layout()
    plt.show()


def plot_hbar(df, x, y, title="", xlabel=None, ylabel=None, color=None, figsize=None):
    """
    Horizontal bar chart — useful when category labels are long.
    """
    fig, ax = plt.subplots(figsize=figsize or (9, 4.5))
    bars = ax.barh(df[x].astype(str), df[y],
                   color=color or COLORS[:len(df)],
                   edgecolor="white", linewidth=0.8)

    for bar in bars:
        width = bar.get_width()
        label = f'  {width:,.0f}' if width > 10 else f'  {width:.1f}'
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                label, ha='left', va='center', fontsize=9, fontweight='bold')

    ax.set_title(title, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel or y)
    ax.set_ylabel(ylabel or x)
    plt.tight_layout()
    plt.show()


def plot_pie(df, labels_col, values_col, title="", figsize=None):
    """
    Pie chart with percentage labels.
    """
    fig, ax = plt.subplots(figsize=figsize or (7, 7))
    wedges, texts, autotexts = ax.pie(
        df[values_col],
        labels=df[labels_col],
        autopct="%1.1f%%",
        colors=COLORS[:len(df)],
        startangle=140,
        pctdistance=0.85,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
    )
    for text in autotexts:
        text.set_fontsize(9)
        text.set_fontweight("bold")
    ax.set_title(title, fontweight="bold", pad=16)
    plt.tight_layout()
    plt.show()


def plot_line(df, x, y, title="", xlabel=None, ylabel=None, marker="o", figsize=None):
    """
    Line chart — good for trends.
    """
    fig, ax = plt.subplots(figsize=figsize or (9, 4.5))
    ax.plot(df[x].astype(str), df[y], marker=marker, color=COLORS[0],
            linewidth=2, markersize=6)
    ax.fill_between(range(len(df)), df[y], alpha=0.1, color=COLORS[0])
    ax.set_title(title, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
