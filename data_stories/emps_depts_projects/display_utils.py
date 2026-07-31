"""
display_utils.py  –  Helper functions for the TechNova DuckDB Notebook
=====================================================================
This module keeps ALL display and plotting code OUT of the notebook
so that students see only:
    1. A plain-English explanation
    2. The SQL query
    3. A clean function call that shows the result

Usage inside the notebook:
    from display_utils import run_query, show, plot_bar, plot_hbar, ...
"""

import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import textwrap, warnings
from IPython.display import display, HTML, Markdown

# ── Suppress noisy warnings in student notebooks ────────────────────
warnings.filterwarnings("ignore", category=UserWarning)

# ── Global style settings ───────────────────────────────────────────
FONT = "Segoe UI"
plt.rcParams.update({
    "figure.figsize":    (10, 5),
    "figure.dpi":        110,
    "axes.titlesize":    14,
    "axes.titleweight":  "bold",
    "axes.labelsize":    11,
    "xtick.labelsize":   10,
    "ytick.labelsize":   10,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
})

# ── A nice color palette ────────────────────────────────────────────
COLORS = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52",
    "#8172B3", "#937860", "#DA8BC3", "#8C8C8C",
    "#CCB974", "#64B5CD", "#4C72B0", "#DD8452",
]

# =====================================================================
#  CORE HELPERS
# =====================================================================

def run_query(con: duckdb.DuckDBPyConnection, sql: str) -> pd.DataFrame:
    """Execute a SQL query and return a pandas DataFrame."""
    return con.execute(sql).fetchdf()


def show(df: pd.DataFrame, title: str = "", max_rows: int = 60) -> None:
    """
    Display a DataFrame as a beautifully formatted HTML table
    with row numbers, zebra striping, and a title.
    """
    if title:
        display(Markdown(f"**Result: {title}**"))

    styled_df = df.head(max_rows).copy()
    styled_df.index = range(1, len(styled_df) + 1)
    styled_df.index.name = "#"

    # Build HTML table with clean styling
    html = styled_df.to_html(
        classes="result-table",
        border=0,
        justify="left",
    )

    css = """
    <style>
    .result-table {
        border-collapse: collapse;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        margin: 8px 0 16px 0;
        width: auto;
    }
    .result-table th {
        background-color: #2C3E50;
        color: white;
        padding: 8px 14px;
        text-align: left;
        font-weight: 600;
        border: 1px solid #2C3E50;
    }
    .result-table td {
        padding: 6px 14px;
        border: 1px solid #ddd;
    }
    .result-table tr:nth-child(even) {
        background-color: #F7F9FC;
    }
    .result-table tr:nth-child(odd) {
        background-color: #FFFFFF;
    }
    .result-table tr:hover {
        background-color: #EBF0F7;
    }
    </style>
    """
    display(HTML(css + html))

    if len(df) > max_rows:
        display(HTML(
            f'<p style="color:#888; font-size:12px;">'
            f'Showing {max_rows} of {len(df)} rows.</p>'
        ))


def show_query(con, sql: str, title: str = "", max_rows: int = 60):
    """Run a query, display the result table, and return the DataFrame."""
    df = run_query(con, sql)
    show(df, title=title, max_rows=max_rows)
    return df


# =====================================================================
#  PLOTTING HELPERS
# =====================================================================

def _apply_common(ax, title, xlabel, ylabel):
    """Apply common formatting to any axes object."""
    if title:
        ax.set_title(title, pad=12)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()


def plot_bar(df, x, y, title="", xlabel="", ylabel="",
             color=None, figsize=None, rotate_labels=0,
             show_values=True, fmt="{:.0f}"):
    """
    Vertical bar chart.

    Parameters
    ----------
    df       : DataFrame with the data
    x, y     : column names for the x-axis (categories) and y-axis (values)
    title    : chart title
    show_values : annotate each bar with its value
    fmt      : format string for value annotations
    """
    fig, ax = plt.subplots(figsize=figsize or (max(6, len(df)*0.8), 5))
    colors = color or COLORS[:len(df)]
    bars = ax.bar(df[x].astype(str), df[y], color=colors, edgecolor="white", width=0.6)

    if show_values:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h,
                    fmt.format(h), ha="center", va="bottom",
                    fontsize=9, fontweight="bold")

    if rotate_labels:
        plt.xticks(rotation=rotate_labels, ha="right")

    _apply_common(ax, title, xlabel, ylabel)
    plt.show()


def plot_hbar(df, label_col, value_col, title="", xlabel="",
              ylabel="", color=None, figsize=None, show_values=True,
              fmt="{:.0f}"):
    """
    Horizontal bar chart – great for long category names.
    """
    fig, ax = plt.subplots(figsize=figsize or (8, max(4, len(df)*0.45)))
    colors = color or COLORS[:len(df)]
    bars = ax.barh(df[label_col].astype(str), df[value_col],
                   color=colors, edgecolor="white", height=0.6)

    if show_values:
        for bar in bars:
            w = bar.get_width()
            ax.text(w, bar.get_y() + bar.get_height()/2,
                    "  " + fmt.format(w), ha="left", va="center",
                    fontsize=9, fontweight="bold")

    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    if title:
        ax.set_title(title, pad=12)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    plt.tight_layout()
    plt.show()


def plot_pie(df, labels_col, values_col, title="", figsize=None):
    """Pie chart with percentage labels."""
    fig, ax = plt.subplots(figsize=figsize or (7, 7))
    wedges, texts, autotexts = ax.pie(
        df[values_col], labels=df[labels_col],
        autopct="%1.1f%%", startangle=140,
        colors=COLORS[:len(df)],
        textprops={"fontsize": 10},
        pctdistance=0.8,
    )
    for t in autotexts:
        t.set_fontweight("bold")
    if title:
        ax.set_title(title, pad=16, fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_line(df, x, y, title="", xlabel="", ylabel="",
              marker="o", color=None, figsize=None):
    """Line chart – good for time-series or trend data."""
    fig, ax = plt.subplots(figsize=figsize or (10, 5))
    ax.plot(df[x].astype(str), df[y], marker=marker,
            color=color or COLORS[0], linewidth=2, markersize=6)
    ax.fill_between(range(len(df)), df[y], alpha=0.08, color=COLORS[0])
    _apply_common(ax, title, xlabel, ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.show()


def plot_grouped_bar(df, x, groups, title="", xlabel="", ylabel="",
                     figsize=None):
    """
    Grouped (side-by-side) bar chart.

    Parameters
    ----------
    df     : DataFrame
    x      : column for x-axis labels
    groups : list of column names, one bar per group
    """
    import numpy as np
    fig, ax = plt.subplots(figsize=figsize or (max(8, len(df)*1.2), 5))
    n = len(groups)
    width = 0.7 / n
    positions = np.arange(len(df))

    for i, col in enumerate(groups):
        offset = (i - n/2 + 0.5) * width
        ax.bar(positions + offset, df[col], width=width,
               label=col, color=COLORS[i % len(COLORS)], edgecolor="white")

    ax.set_xticks(positions)
    ax.set_xticklabels(df[x].astype(str), rotation=30, ha="right")
    ax.legend(frameon=False)
    _apply_common(ax, title, xlabel, ylabel)
    plt.show()


def plot_scatter(df, x, y, title="", xlabel="", ylabel="",
                 color=None, figsize=None, size=60):
    """Scatter plot."""
    fig, ax = plt.subplots(figsize=figsize or (8, 5))
    ax.scatter(df[x], df[y], s=size, color=color or COLORS[0],
               alpha=0.7, edgecolors="white", linewidth=0.5)
    _apply_common(ax, title, xlabel, ylabel)
    plt.show()


def plot_hist(df, col, bins=15, title="", xlabel="", ylabel="Frequency",
              color=None, figsize=None):
    """Histogram."""
    fig, ax = plt.subplots(figsize=figsize or (8, 5))
    ax.hist(df[col], bins=bins, color=color or COLORS[0],
            edgecolor="white", alpha=0.85)
    _apply_common(ax, title, xlabel, ylabel)
    plt.show()


def plot_box(df, x, y, title="", xlabel="", ylabel="", figsize=None):
    """
    Box plot – shows salary distribution by category.
    Uses matplotlib only (no seaborn dependency).
    """
    fig, ax = plt.subplots(figsize=figsize or (10, 5))
    categories = df[x].unique()
    data_groups = [df[df[x] == cat][y].values for cat in categories]

    bp = ax.boxplot(data_groups, patch_artist=True, labels=categories,
                    widths=0.5, medianprops=dict(color="black", linewidth=1.5))
    for patch, color in zip(bp["boxes"], COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)

    _apply_common(ax, title, xlabel, ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.show()


def plot_stacked_bar(df, x, columns, title="", xlabel="", ylabel="",
                     figsize=None):
    """Stacked bar chart."""
    fig, ax = plt.subplots(figsize=figsize or (max(8, len(df)*0.9), 5))
    bottom = pd.Series([0]*len(df), dtype=float)
    for i, col in enumerate(columns):
        ax.bar(df[x].astype(str), df[col], bottom=bottom,
               label=col, color=COLORS[i % len(COLORS)], edgecolor="white")
        bottom += df[col]
    ax.legend(frameon=False, loc="upper right")
    _apply_common(ax, title, xlabel, ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.show()
