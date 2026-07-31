"""
display_utils.py  –  Helper functions for the Sales Data Exploration notebook.
─────────────────────────────────────────────────────────────────────────────
Keep ALL display / plotting logic here so the notebook stays clean and
students can focus on SQL, not on matplotlib boilerplate.

Usage (inside the notebook):
    from display_utils import show, plot_bar, plot_line, plot_pie, plot_hbar, plot_grouped_bar, plot_stacked_bar
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import textwrap

# ── global style ────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "#f9f9f9",
    "axes.edgecolor":   "#cccccc",
    "axes.grid":        True,
    "grid.alpha":       0.4,
    "grid.linestyle":   "--",
    "font.size":        11,
    "axes.titlesize":   14,
    "axes.titleweight": "bold",
    "axes.labelsize":   12,
    "figure.dpi":       110,
})

# ── colour palette ──────────────────────────────────────────────────────────
COLORS = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52",
    "#8172B3", "#937860", "#DA8BC3", "#8C8C8C",
    "#CCB974", "#64B5CD",
]

# ═══════════════════════════════════════════════════════════════════════════
# 1.  DISPLAY  –  pretty tabulated result set
# ═══════════════════════════════════════════════════════════════════════════

def show(df: pd.DataFrame, max_rows: int = 30, title: str = "") -> None:
    """
    Display a DataFrame as a nicely styled HTML table with row numbers.

    Parameters
    ----------
    df       : pandas DataFrame (typically from duckdb .df())
    max_rows : cap on rows displayed (0 = unlimited)
    title    : optional title rendered above the table
    """
    from IPython.display import display, HTML

    if max_rows and len(df) > max_rows:
        view = df.head(max_rows).copy()
        note = f"<p style='color:#888; font-size:12px;'>Showing {max_rows} of {len(df)} rows</p>"
    else:
        view = df.copy()
        note = ""

    # Row numbers starting at 1
    view.index = range(1, len(view) + 1)
    view.index.name = "#"

    # Build HTML
    html = view.to_html(border=0, classes="styled-table")

    css = """
    <style>
    .styled-table {
        border-collapse: collapse;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
        margin: 10px 0;
    }
    .styled-table thead th {
        background-color: #4C72B0;
        color: white;
        padding: 8px 14px;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid #3a5a8c;
    }
    .styled-table tbody td {
        padding: 6px 14px;
        border-bottom: 1px solid #e8e8e8;
    }
    .styled-table tbody tr:nth-child(even) {
        background-color: #f2f6fa;
    }
    .styled-table tbody tr:hover {
        background-color: #e2eaf4;
    }
    .styled-table th:first-child,
    .styled-table td:first-child {
        color: #888;
        font-size: 11px;
        text-align: right;
        padding-right: 10px;
    }
    </style>
    """
    title_html = f"<h4 style='margin:4px 0 2px 0; color:#333;'>{title}</h4>" if title else ""
    total_html = f"<p style='color:#666; font-size:12px; margin:2px 0;'>Total rows: {len(df)}</p>"
    display(HTML(css + title_html + html + note + total_html))


# ═══════════════════════════════════════════════════════════════════════════
# 2.  PLOTTING helpers
# ═══════════════════════════════════════════════════════════════════════════

def _wrap(labels, width=18):
    """Wrap long tick labels."""
    return [textwrap.fill(str(l), width) for l in labels]


def _annotate_bars(ax, fmt="{:.0f}", fontsize=9, offset=0.01):
    """Place value labels on top of each bar."""
    ymax = ax.get_ylim()[1]
    for bar in ax.patches:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + ymax * offset,
                fmt.format(h),
                ha="center", va="bottom",
                fontsize=fontsize, color="#333",
            )


def _format_currency(ax, axis="y"):
    """Format an axis with $ and comma separators."""
    fmt = mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
    if axis == "y":
        ax.yaxis.set_major_formatter(fmt)
    else:
        ax.xaxis.set_major_formatter(fmt)


# ── bar chart ───────────────────────────────────────────────────────────────

def plot_bar(
    df, x, y, title="", xlabel="", ylabel="",
    color=None, figsize=(10, 5), fmt="{:.0f}",
    currency=False, rotate_x=0, top_n=0,
):
    """Vertical bar chart from a DataFrame."""
    data = df.nlargest(top_n, y) if top_n else df
    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.bar(
        range(len(data)),
        data[y],
        color=color or COLORS[0],
        edgecolor="white", linewidth=0.5,
    )
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(_wrap(data[x].astype(str), 20), rotation=rotate_x, ha="right" if rotate_x else "center")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if currency:
        _format_currency(ax)
    _annotate_bars(ax, fmt=fmt)
    plt.tight_layout()
    plt.show()


# ── horizontal bar chart ────────────────────────────────────────────────────

def plot_hbar(
    df, x, y, title="", xlabel="", ylabel="",
    color=None, figsize=(10, 6), fmt="{:.0f}",
    currency=False, top_n=0,
):
    """Horizontal bar chart – good for long category labels."""
    data = df.nlargest(top_n, y) if top_n else df
    data = data.iloc[::-1]  # reverse so largest is on top
    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(data[x].astype(str), data[y], color=color or COLORS[0], edgecolor="white", linewidth=0.5)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if currency:
        _format_currency(ax, axis="x")
    # value labels
    xmax = ax.get_xlim()[1]
    for i, (val, name) in enumerate(zip(data[y], data[x])):
        ax.text(val + xmax * 0.01, i, fmt.format(val), va="center", fontsize=9, color="#333")
    plt.tight_layout()
    plt.show()


# ── line chart ──────────────────────────────────────────────────────────────

def plot_line(
    df, x, y, title="", xlabel="", ylabel="",
    color=None, figsize=(10, 5), marker="o",
    currency=False, fmt="{:.0f}", annotate=True,
):
    """Line chart with optional data-point annotations."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df[x].astype(str), df[y], marker=marker, color=color or COLORS[0],
            linewidth=2.5, markersize=7)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if currency:
        _format_currency(ax)
    if annotate:
        ymax = ax.get_ylim()[1]
        for xi, yi in zip(df[x].astype(str), df[y]):
            ax.annotate(fmt.format(yi), (xi, yi),
                        textcoords="offset points", xytext=(0, 10),
                        ha="center", fontsize=9, color="#333")
    plt.tight_layout()
    plt.show()


# ── pie chart ───────────────────────────────────────────────────────────────

def plot_pie(
    df, labels_col, values_col, title="",
    figsize=(7, 7), colors=None, startangle=140,
):
    """Pie / donut chart."""
    fig, ax = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax.pie(
        df[values_col],
        labels=df[labels_col],
        autopct="%1.1f%%",
        startangle=startangle,
        colors=colors or COLORS[: len(df)],
        pctdistance=0.78,
        wedgeprops=dict(edgecolor="white", linewidth=1.5),
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_color("white")
        t.set_fontweight("bold")
    ax.set_title(title, pad=16)
    plt.tight_layout()
    plt.show()


# ── grouped bar chart ──────────────────────────────────────────────────────

def plot_grouped_bar(
    df, x, y_cols, title="", xlabel="", ylabel="",
    labels=None, figsize=(11, 5), currency=False,
):
    """Side-by-side grouped bar chart for comparing multiple series."""
    import numpy as np
    cats = df[x].astype(str)
    n = len(y_cols)
    width = 0.8 / n
    positions = np.arange(len(cats))

    fig, ax = plt.subplots(figsize=figsize)
    for i, col in enumerate(y_cols):
        label = labels[i] if labels else col
        ax.bar(positions + i * width, df[col], width,
               label=label, color=COLORS[i % len(COLORS)], edgecolor="white")

    ax.set_xticks(positions + width * (n - 1) / 2)
    ax.set_xticklabels(cats, rotation=0)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if currency:
        _format_currency(ax)
    ax.legend(frameon=True, fancybox=True, shadow=False)
    plt.tight_layout()
    plt.show()


# ── stacked bar chart ─────────────────────────────────────────────────────

def plot_stacked_bar(
    df, x, y_cols, title="", xlabel="", ylabel="",
    labels=None, figsize=(10, 5), currency=False,
):
    """Stacked bar chart."""
    import numpy as np
    cats = df[x].astype(str)
    positions = np.arange(len(cats))
    bottom = np.zeros(len(cats))

    fig, ax = plt.subplots(figsize=figsize)
    for i, col in enumerate(y_cols):
        label = labels[i] if labels else col
        ax.bar(positions, df[col], bottom=bottom,
               label=label, color=COLORS[i % len(COLORS)], edgecolor="white", linewidth=0.5)
        bottom += df[col].values

    ax.set_xticks(positions)
    ax.set_xticklabels(cats)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if currency:
        _format_currency(ax)
    ax.legend(frameon=True, fancybox=True, shadow=False)
    plt.tight_layout()
    plt.show()
