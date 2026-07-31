"""
notebook_utils.py
=================
Helper utilities for JOIN_101_EMPS_DEPTS Jupyter Notebook.

Provides clean display and plotting functions so the notebook
stays focused on SQL learning — no tangled visualization code.

Functions
---------
show_df(df, title)          : Display a DuckDB result as a styled table with row numbers
bar_chart(df, x, y, title)  : Horizontal or vertical bar chart
pie_chart(df, labels, values, title) : Pie / donut chart
scatter_chart(df, x, y, title, color_col) : Scatter plot
grouped_bar(df, x, y_cols, title) : Grouped bar chart for multi-series data
salary_hist(df, col, title) : Histogram for salary distribution
highlight_join(left_col, right_col, match_col, df, title) : Visual join result highlighter
"""

import matplotlib
matplotlib.use("Agg")          # safe for all environments
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from IPython.display import display, HTML
import warnings
warnings.filterwarnings("ignore")

# ── Palette ──────────────────────────────────────────────────────────────────
PALETTE   = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
             "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]
BG_COLOR  = "#F8F9FA"
GRID_COLOR = "#E0E0E0"
FONT      = "DejaVu Sans"

plt.rcParams.update({
    "font.family":       FONT,
    "axes.facecolor":    BG_COLOR,
    "figure.facecolor":  "white",
    "axes.grid":         True,
    "grid.color":        GRID_COLOR,
    "grid.linewidth":    0.8,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

# ── Table Display ─────────────────────────────────────────────────────────────

def show_df(rel_or_df, title: str = "", max_rows: int = 50):
    """
    Display a DuckDB relation or Pandas DataFrame as a clean HTML table
    with row numbers.

    Parameters
    ----------
    rel_or_df : duckdb.DuckDBPyRelation | pd.DataFrame
    title     : Optional caption shown above the table
    max_rows  : Truncate display to this many rows (default 50)
    """
    # Convert DuckDB relation to DataFrame if needed
    if hasattr(rel_or_df, "df"):
        df = rel_or_df.df()
    elif hasattr(rel_or_df, "fetchdf"):
        df = rel_or_df.fetchdf()
    else:
        df = rel_or_df.copy()

    total = len(df)
    df_show = df.head(max_rows).copy()
    df_show.index = range(1, len(df_show) + 1)
    df_show.index.name = "#"

    caption_html = ""
    if title:
        caption_html = (
            f'<div style="font-size:15px;font-weight:700;color:#2c3e50;'
            f'margin-bottom:6px;padding:4px 0 2px 2px;'
            f'border-left:4px solid #4C72B0;padding-left:10px;">'
            f'📋 {title}</div>'
        )

    styled = (
        df_show.style
        .set_table_styles([
            {"selector": "thead th",
             "props": [("background-color", "#4C72B0"),
                       ("color", "white"),
                       ("font-weight", "bold"),
                       ("font-size", "12px"),
                       ("padding", "8px 12px"),
                       ("text-align", "left")]},
            {"selector": "tbody td",
             "props": [("padding", "6px 12px"),
                       ("font-size", "12px"),
                       ("border-bottom", "1px solid #e0e0e0")]},
            {"selector": "tbody tr:nth-child(even)",
             "props": [("background-color", "#EEF2F7")]},
            {"selector": "tbody tr:hover",
             "props": [("background-color", "#D6E4F7")]},
            {"selector": "th.index_name, td.row_heading",
             "props": [("background-color", "#6C8EBF"),
                       ("color", "white"),
                       ("font-weight", "bold"),
                       ("padding", "6px 10px")]},
        ])
        .format(na_rep="—")
    )

    footer = ""
    if total > max_rows:
        footer = (
            f'<div style="font-size:11px;color:#888;margin-top:4px;">'
            f'Showing first {max_rows} of {total} rows.</div>'
        )

    display(HTML(caption_html))
    display(styled)
    if footer:
        display(HTML(footer))


# ── Bar Chart ─────────────────────────────────────────────────────────────────

def bar_chart(df, x: str, y: str, title: str = "",
              xlabel: str = "", ylabel: str = "",
              color: str = None, horizontal: bool = False,
              figsize=(10, 5)):
    """Vertical or horizontal bar chart from a DataFrame."""
    fig, ax = plt.subplots(figsize=figsize)
    col  = color or PALETTE[0]
    vals = df[y].tolist()
    labs = df[x].astype(str).tolist()

    if horizontal:
        bars = ax.barh(labs, vals, color=col, edgecolor="white", linewidth=0.6)
        ax.set_xlabel(ylabel or y, fontsize=11)
        ax.set_ylabel(xlabel or x, fontsize=11)
        for bar in bars:
            w = bar.get_width()
            ax.text(w * 1.01, bar.get_y() + bar.get_height() / 2,
                    f"{w:,.0f}", va="center", ha="left", fontsize=9, color="#333")
    else:
        bars = ax.bar(labs, vals, color=col, edgecolor="white", linewidth=0.6)
        ax.set_xlabel(xlabel or x, fontsize=11)
        ax.set_ylabel(ylabel or y, fontsize=11)
        plt.xticks(rotation=35, ha="right", fontsize=9)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h * 1.01,
                    f"{h:,.0f}", ha="center", va="bottom", fontsize=9, color="#333")

    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.show()


# ── Pie / Donut Chart ─────────────────────────────────────────────────────────

def pie_chart(df, labels: str, values: str, title: str = "",
              donut: bool = True, figsize=(8, 6)):
    """Pie or donut chart."""
    fig, ax = plt.subplots(figsize=figsize)
    labs = df[labels].astype(str).tolist()
    vals = df[values].tolist()
    colors = PALETTE[:len(vals)]

    wedges, texts, autotexts = ax.pie(
        vals, labels=labs, colors=colors,
        autopct="%1.1f%%", startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        pctdistance=0.80
    )
    for t in autotexts:
        t.set_fontsize(9)
        t.set_color("white")
        t.set_fontweight("bold")

    if donut:
        centre = plt.Circle((0, 0), 0.55, fc="white")
        ax.add_patch(centre)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    plt.tight_layout()
    plt.show()


# ── Grouped Bar Chart ─────────────────────────────────────────────────────────

def grouped_bar(df, x: str, y_cols: list, title: str = "",
                xlabel: str = "", ylabel: str = "", figsize=(11, 5)):
    """Grouped bar chart for comparing multiple numeric columns side-by-side."""
    n_groups = len(df)
    n_bars   = len(y_cols)
    ind      = np.arange(n_groups)
    width    = 0.8 / n_bars

    fig, ax = plt.subplots(figsize=figsize)
    for i, col in enumerate(y_cols):
        offset = (i - n_bars / 2 + 0.5) * width
        bars = ax.bar(ind + offset, df[col], width,
                      label=col, color=PALETTE[i % len(PALETTE)],
                      edgecolor="white", linewidth=0.5)

    ax.set_xticks(ind)
    ax.set_xticklabels(df[x].astype(str), rotation=30, ha="right", fontsize=9)
    ax.set_xlabel(xlabel or x, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.show()


# ── Scatter Plot ──────────────────────────────────────────────────────────────

def scatter_chart(df, x: str, y: str, title: str = "",
                  color_col: str = None, label_col: str = None,
                  figsize=(10, 6)):
    """Scatter plot, optionally coloured by a categorical column."""
    fig, ax = plt.subplots(figsize=figsize)

    if color_col and color_col in df.columns:
        categories = df[color_col].unique()
        for i, cat in enumerate(categories):
            sub = df[df[color_col] == cat]
            ax.scatter(sub[x], sub[y], label=str(cat),
                       color=PALETTE[i % len(PALETTE)], s=80, alpha=0.8, edgecolors="white")
        ax.legend(title=color_col, fontsize=9)
    else:
        ax.scatter(df[x], df[y], color=PALETTE[0], s=80, alpha=0.8, edgecolors="white")

    if label_col and label_col in df.columns:
        for _, row in df.iterrows():
            ax.annotate(str(row[label_col]), (row[x], row[y]),
                        textcoords="offset points", xytext=(5, 3),
                        fontsize=7, color="#444")

    ax.set_xlabel(x, fontsize=11)
    ax.set_ylabel(y, fontsize=11)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.show()


# ── Salary Histogram ──────────────────────────────────────────────────────────

def salary_hist(df, col: str = "salary", title: str = "Salary Distribution",
                bins: int = 10, figsize=(10, 5)):
    """Histogram for a numeric column (e.g. salary)."""
    fig, ax = plt.subplots(figsize=figsize)
    vals = df[col].dropna()
    ax.hist(vals, bins=bins, color=PALETTE[0], edgecolor="white", linewidth=0.7)
    ax.axvline(vals.mean(), color=PALETTE[3], linewidth=1.8,
               linestyle="--", label=f"Mean: ${vals.mean():,.0f}")
    ax.axvline(vals.median(), color=PALETTE[2], linewidth=1.8,
               linestyle=":", label=f"Median: ${vals.median():,.0f}")
    ax.set_xlabel(col.replace("_", " ").title(), fontsize=11)
    ax.set_ylabel("Number of Employees", fontsize=11)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.show()


# ── Join Venn Diagram ─────────────────────────────────────────────────────────

def draw_join_venn(join_type: str = "inner"):
    """
    Draw a simple Venn-style diagram illustrating which rows are kept
    for INNER, LEFT, RIGHT, or FULL OUTER joins.

    Parameters
    ----------
    join_type : str  — 'inner' | 'left' | 'right' | 'full'
    """
    join_type = join_type.lower().strip()
    fig, ax   = plt.subplots(figsize=(7, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    highlight = {
        "inner": ("center",),
        "left":  ("left", "center"),
        "right": ("right", "center"),
        "full":  ("left", "center", "right"),
    }.get(join_type, ("center",))

    region_colors = {
        "left":   "#4C72B0" if "left"   in highlight else "#D0D8E8",
        "center": "#4C72B0" if "center" in highlight else "#D0D8E8",
        "right":  "#4C72B0" if "right"  in highlight else "#D0D8E8",
    }
    alpha = 0.55

    # Left circle
    left_c = plt.Circle((3.8, 3), 2.1, color=region_colors["left"],
                         alpha=alpha, zorder=1)
    # Right circle
    right_c = plt.Circle((6.2, 3), 2.1, color=region_colors["right"],
                          alpha=alpha, zorder=1)
    ax.add_patch(left_c)
    ax.add_patch(right_c)

    # Intersection overlay
    if "center" in highlight:
        from matplotlib.patches import Wedge
        # Use a clipping polygon approximation
        cx = plt.Circle((5.0, 3), 1.25, color="#4C72B0", alpha=0.75, zorder=2)
        ax.add_patch(cx)

    # Labels
    ax.text(2.5, 3, "Employees", ha="center", va="center",
            fontsize=11, fontweight="bold", color="white", zorder=3)
    ax.text(7.5, 3, "Departments", ha="center", va="center",
            fontsize=11, fontweight="bold", color="white", zorder=3)
    ax.text(5.0, 3, "Match", ha="center", va="center",
            fontsize=10, fontweight="bold", color="white", zorder=4)

    titles = {
        "inner": "INNER JOIN — only matching rows from both tables",
        "left":  "LEFT JOIN — all Employees + matches from Departments",
        "right": "RIGHT JOIN — all Departments + matches from Employees",
        "full":  "FULL OUTER JOIN — all rows from both tables",
    }
    ax.set_title(titles.get(join_type, ""), fontsize=13,
                 fontweight="bold", pad=8, color="#2c3e50")
    plt.tight_layout()
    plt.show()


# ── Null / Match Summary Bar ──────────────────────────────────────────────────

def match_summary_bar(matched: int, unmatched: int,
                      label_matched: str = "Matched",
                      label_unmatched: str = "Unmatched",
                      title: str = "Join Match Summary",
                      figsize=(7, 3)):
    """
    Simple two-bar chart showing matched vs unmatched row counts after a join.
    Helpful for visualising LEFT / RIGHT join NULL rows.
    """
    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.bar([label_matched, label_unmatched],
                  [matched, unmatched],
                  color=[PALETTE[2], PALETTE[3]],
                  edgecolor="white", linewidth=0.7, width=0.45)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.3,
                str(int(h)), ha="center", va="bottom",
                fontsize=12, fontweight="bold", color="#333")
    ax.set_ylabel("Number of Rows", fontsize=11)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.set_ylim(0, max(matched, unmatched) * 1.18)
    plt.tight_layout()
    plt.show()
