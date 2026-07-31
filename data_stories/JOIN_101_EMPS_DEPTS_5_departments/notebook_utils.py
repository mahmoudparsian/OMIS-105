"""
notebook_utils.py
=================
Helper utilities for JOIN_101_EMPS_DEPTS Jupyter Notebook.

All display and plotting logic lives here so the notebook
stays clean and focused on SQL learning.

Public API
----------
show_df(df, title)                          — styled table with row numbers
bar_chart(df, x, y, title, ...)             — vertical or horizontal bar chart
pie_chart(df, labels, values, title, ...)   — pie / donut chart
grouped_bar(df, x, y_cols, title, ...)      — side-by-side bars (multi-series)
scatter_chart(df, x, y, title, ...)         — scatter plot
draw_join_venn(join_type)                   — Venn diagram for INNER/LEFT/RIGHT
match_summary_bar(matched, unmatched, ...)  — matched vs unmatched row counts
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from IPython.display import display, HTML
import warnings
warnings.filterwarnings("ignore")

# ── Design tokens ─────────────────────────────────────────────────────────────
PALETTE    = ["#4C72B0", "#DD8452", "#55A868", "#C44E52",
              "#8172B3", "#937860", "#DA8BC3", "#64B5CD"]
BG_COLOR   = "#F7F9FC"
GRID_COLOR = "#E2E8F0"

plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.facecolor":    BG_COLOR,
    "figure.facecolor":  "white",
    "axes.grid":         True,
    "grid.color":        GRID_COLOR,
    "grid.linewidth":    0.7,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

# ── Table display ─────────────────────────────────────────────────────────────

def show_df(rel_or_df, title: str = "", max_rows: int = 60):
    """
    Render a DuckDB relation or Pandas DataFrame as a
    clean, numbered HTML table.

    Parameters
    ----------
    rel_or_df : duckdb relation or pd.DataFrame
    title     : optional heading shown above the table
    max_rows  : cap on rows displayed (default 60)
    """
    if hasattr(rel_or_df, "df"):
        df = rel_or_df.df()
    elif hasattr(rel_or_df, "fetchdf"):
        df = rel_or_df.fetchdf()
    else:
        df = rel_or_df.copy()

    total    = len(df)
    df_show  = df.head(max_rows).copy()
    df_show.index = range(1, len(df_show) + 1)
    df_show.index.name = "#"

    cap = ""
    if title:
        cap = (
            f'<div style="font-size:15px;font-weight:700;color:#1e3a5f;'
            f'margin-bottom:6px;border-left:4px solid #4C72B0;'
            f'padding-left:10px;">📋 {title}</div>'
        )

    styled = (
        df_show.style
        .set_table_styles([
            {"selector": "thead th",
             "props": [("background-color", "#4C72B0"), ("color", "white"),
                       ("font-weight", "bold"), ("font-size", "12px"),
                       ("padding", "7px 13px"), ("text-align", "left")]},
            {"selector": "tbody td",
             "props": [("padding", "5px 13px"), ("font-size", "12px"),
                       ("border-bottom", "1px solid #e4eaf2")]},
            {"selector": "tbody tr:nth-child(even)",
             "props": [("background-color", "#EDF2FB")]},
            {"selector": "tbody tr:hover",
             "props": [("background-color", "#D0E3FF")]},
            {"selector": "th.index_name, td.row_heading",
             "props": [("background-color", "#6C8EBF"), ("color", "white"),
                       ("font-weight", "bold"), ("padding", "5px 10px")]},
        ])
        .format(na_rep="NULL")          # show NULLs explicitly
    )

    display(HTML(cap))
    display(styled)
    if total > max_rows:
        display(HTML(
            f'<div style="font-size:11px;color:#888;margin-top:3px;">'
            f'Showing first {max_rows} of {total} rows.</div>'
        ))


# ── Bar chart ─────────────────────────────────────────────────────────────────

def bar_chart(df, x: str, y: str, title: str = "",
              xlabel: str = "", ylabel: str = "",
              color: str = None, horizontal: bool = False,
              figsize=(9, 4.5)):
    """Vertical or horizontal bar chart with value labels."""
    fig, ax = plt.subplots(figsize=figsize)
    c    = color or PALETTE[0]
    vals = df[y].tolist()
    labs = df[x].astype(str).tolist()

    if horizontal:
        bars = ax.barh(labs, vals, color=c, edgecolor="white", linewidth=0.5)
        ax.set_xlabel(ylabel or y, fontsize=11)
        ax.set_ylabel(xlabel or x, fontsize=11)
        for b in bars:
            w = b.get_width()
            ax.text(w * 1.01, b.get_y() + b.get_height() / 2,
                    f"{w:,.0f}", va="center", ha="left", fontsize=9)
    else:
        bars = ax.bar(labs, vals, color=c, edgecolor="white", linewidth=0.5)
        ax.set_xlabel(xlabel or x, fontsize=11)
        ax.set_ylabel(ylabel or y, fontsize=11)
        plt.xticks(rotation=30, ha="right", fontsize=9)
        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, h * 1.01,
                    f"{h:,.0f}", ha="center", va="bottom", fontsize=9)

    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    plt.tight_layout()
    plt.show()


# ── Pie / donut chart ─────────────────────────────────────────────────────────

def pie_chart(df, labels: str, values: str, title: str = "",
              donut: bool = True, figsize=(7, 5)):
    """Pie or donut chart."""
    fig, ax = plt.subplots(figsize=figsize)
    labs    = df[labels].astype(str).tolist()
    vals    = df[values].tolist()
    colors  = PALETTE[:len(vals)]

    wedges, texts, autotexts = ax.pie(
        vals, labels=labs, colors=colors, autopct="%1.1f%%",
        startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        pctdistance=0.78,
    )
    for t in autotexts:
        t.set_fontsize(9); t.set_color("white"); t.set_fontweight("bold")

    if donut:
        ax.add_patch(plt.Circle((0, 0), 0.52, fc="white"))

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.show()


# ── Grouped bar chart ─────────────────────────────────────────────────────────

def grouped_bar(df, x: str, y_cols: list, title: str = "",
                xlabel: str = "", ylabel: str = "", figsize=(10, 5)):
    """Side-by-side bars for multiple numeric columns."""
    n  = len(df)
    nb = len(y_cols)
    ind   = np.arange(n)
    width = 0.75 / nb

    fig, ax = plt.subplots(figsize=figsize)
    for i, col in enumerate(y_cols):
        offset = (i - nb / 2 + 0.5) * width
        ax.bar(ind + offset, df[col], width,
               label=col, color=PALETTE[i % len(PALETTE)],
               edgecolor="white", linewidth=0.4)

    ax.set_xticks(ind)
    ax.set_xticklabels(df[x].astype(str), rotation=25, ha="right", fontsize=9)
    ax.set_xlabel(xlabel or x, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.show()


# ── Scatter plot ──────────────────────────────────────────────────────────────

def scatter_chart(df, x: str, y: str, title: str = "",
                  color_col: str = None, label_col: str = None,
                  figsize=(9, 5)):
    """Scatter plot, optionally coloured by a categorical column."""
    fig, ax = plt.subplots(figsize=figsize)

    if color_col and color_col in df.columns:
        for i, cat in enumerate(df[color_col].unique()):
            sub = df[df[color_col] == cat]
            ax.scatter(sub[x], sub[y], label=str(cat),
                       color=PALETTE[i % len(PALETTE)],
                       s=90, alpha=0.85, edgecolors="white")
        ax.legend(title=color_col, fontsize=9)
    else:
        ax.scatter(df[x], df[y], color=PALETTE[0], s=90,
                   alpha=0.85, edgecolors="white")

    if label_col and label_col in df.columns:
        for _, row in df.iterrows():
            ax.annotate(str(row[label_col]), (row[x], row[y]),
                        textcoords="offset points", xytext=(5, 3),
                        fontsize=8, color="#444")

    ax.set_xlabel(x, fontsize=11)
    ax.set_ylabel(y, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    plt.tight_layout()
    plt.show()


# ── Join Venn diagram ─────────────────────────────────────────────────────────

def draw_join_venn(join_type: str = "inner"):
    """
    Draw a Venn-style diagram showing which rows survive each JOIN type.

    Parameters
    ----------
    join_type : 'inner' | 'left' | 'right' | 'full'
    """
    jt  = join_type.lower().strip()
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.axis("off"); ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    active = {
        "inner": {"center"},
        "left":  {"left", "center"},
        "right": {"right", "center"},
        "full":  {"left", "center", "right"},
    }.get(jt, {"center"})

    DIM  = "#D5DCE8"
    HI   = "#4C72B0"
    HI2  = "#3a5fa0"

    lc = plt.Circle((3.7, 3), 2.2,
                     color=HI if "left" in active else DIM,
                     alpha=0.55, zorder=1)
    rc = plt.Circle((6.3, 3), 2.2,
                     color=HI if "right" in active else DIM,
                     alpha=0.55, zorder=1)
    ax.add_patch(lc); ax.add_patch(rc)

    if "center" in active:
        cc = plt.Circle((5.0, 3), 1.2,
                         color=HI2, alpha=0.80, zorder=2)
        ax.add_patch(cc)

    ax.text(2.6, 3,   "employees",   ha="center", va="center",
            fontsize=10, fontweight="bold", color="white", zorder=3)
    ax.text(7.4, 3,   "departments", ha="center", va="center",
            fontsize=10, fontweight="bold", color="white", zorder=3)
    ax.text(5.0, 3,   "matched",     ha="center", va="center",
            fontsize=9,  fontweight="bold", color="white", zorder=4)

    captions = {
        "inner": "INNER JOIN  —  only rows where dept_id matches in BOTH tables",
        "left":  "LEFT JOIN   —  ALL employees  +  matching dept info (NULL if no match)",
        "right": "RIGHT JOIN  —  ALL departments  +  matching employees (NULL if no match)",
        "full":  "FULL OUTER JOIN  —  all rows from both tables",
    }
    ax.set_title(captions.get(jt, ""), fontsize=12,
                 fontweight="bold", pad=8, color="#1e3a5f")
    plt.tight_layout()
    plt.show()


# ── Matched / unmatched summary bar ──────────────────────────────────────────

def match_summary_bar(matched: int, unmatched: int,
                      label_matched:   str = "Matched",
                      label_unmatched: str = "Unmatched (NULL)",
                      title: str = "Join Match Summary",
                      figsize=(6, 3)):
    """Two-bar chart: matched rows vs rows with NULLs after a join."""
    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.bar([label_matched, label_unmatched],
                  [matched, unmatched],
                  color=[PALETTE[2], PALETTE[3]],
                  edgecolor="white", width=0.4)
    for b in bars:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h + 0.1,
                str(int(h)), ha="center", va="bottom",
                fontsize=12, fontweight="bold")
    ax.set_ylabel("Number of Rows", fontsize=11)
    ax.set_title(title, fontsize=12, fontweight="bold", pad=8)
    ax.set_ylim(0, max(matched, unmatched) * 1.22)
    plt.tight_layout()
    plt.show()
