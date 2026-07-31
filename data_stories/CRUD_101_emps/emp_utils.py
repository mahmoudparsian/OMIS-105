"""
emp_utils.py
============
Helper utilities for the CRUD_101_emps Jupyter Notebook.
All display, tabulation, and plotting functions live here so that
the notebook stays clean and students can focus on SQL.

Usage inside the notebook:
    from emp_utils import show, plot_bar, plot_pie, plot_hist, plot_scatter, show_avatars
"""

import textwrap
import warnings
import matplotlib
matplotlib.use("Agg")          # headless-safe; Jupyter will still render inline
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
import pandas as pd
import io, base64, urllib.request
from IPython.display import display, HTML, Markdown

warnings.filterwarnings("ignore")

# ── colour palette used across all plots ────────────────────────────────────
PALETTE   = ["#4C9BE8", "#F4845F", "#54C6A4", "#F7C948", "#A78BFA", "#FB7185"]
BG_COLOR  = "#F8FAFC"
GRID_CLR  = "#E2E8F0"
TITLE_CLR = "#1E293B"
TEXT_CLR  = "#475569"

# ── pretty-print a DuckDB relation or pandas DataFrame ──────────────────────
def show(result, title: str = "", max_rows: int = 50) -> None:
    """
    Render a DuckDB query result (or DataFrame) as a styled HTML table
    with row numbers, a title banner, and zebra-stripe rows.

    Parameters
    ----------
    result  : duckdb.DuckDBPyRelation | pandas.DataFrame
    title   : optional heading shown above the table
    max_rows: maximum rows to display (default 50)
    """
    # Convert duckdb relation → DataFrame if needed
    if hasattr(result, "df"):
        df = result.df()
    elif isinstance(result, pd.DataFrame):
        df = result
    else:
        df = pd.DataFrame(result)

    df = df.head(max_rows).reset_index(drop=True)
    n_rows, n_cols = df.shape

    # ── build styled HTML ──────────────────────────────────────────────────
    css = """
    <style>
      .crud-table-wrap { font-family: 'Segoe UI', Arial, sans-serif;
                         font-size: 13px; margin: 8px 0 20px 0; }
      .crud-title      { background: #1E293B; color: #F1F5F9;
                         padding: 8px 14px; border-radius: 6px 6px 0 0;
                         font-weight: 700; font-size: 14px; letter-spacing:.4px; }
      .crud-meta       { color: #94A3B8; font-size: 11px;
                         padding: 4px 14px 6px; background:#F8FAFC; }
      .crud-tbl        { border-collapse: collapse; width: 100%;
                         background: #ffffff; }
      .crud-tbl th     { background: #334155; color: #F1F5F9;
                         padding: 7px 12px; text-align: left;
                         font-size: 12px; font-weight: 600; }
      .crud-tbl td     { padding: 6px 12px; border-bottom: 1px solid #E2E8F0;
                         color: #334155; vertical-align: middle; }
      .crud-tbl tr:nth-child(even) td { background: #F1F5F9; }
      .crud-tbl tr:hover td  { background: #DBEAFE !important; }
      .row-num         { color: #94A3B8; font-size: 11px; }
      .crud-footer     { background:#F8FAFC; border-top:2px solid #334155;
                         padding: 4px 14px; color:#64748B; font-size:11px;
                         border-radius: 0 0 6px 6px; }
    </style>
    """

    title_html = ""
    if title:
        title_html = f'<div class="crud-title">📋 {title}</div>'

    meta_html  = f'<div class="crud-meta">{n_rows} row(s) · {n_cols} column(s)</div>'

    # Header row
    th_row = "<tr><th class='row-num'>#</th>"
    for col in df.columns:
        th_row += f"<th>{col}</th>"
    th_row += "</tr>"

    # Data rows
    td_rows = ""
    for i, row in df.iterrows():
        td_rows += "<tr>"
        td_rows += f"<td class='row-num'>{i+1}</td>"
        for val in row:
            td_rows += f"<td>{val}</td>"
        td_rows += "</tr>"

    footer_html = f'<div class="crud-footer">✔ Showing {n_rows} of {len(df)} row(s)</div>'

    html = (css + '<div class="crud-table-wrap">'
            + title_html + meta_html
            + f'<table class="crud-tbl">{th_row}{td_rows}</table>'
            + footer_html + "</div>")
    display(HTML(html))


# ── section header helper ────────────────────────────────────────────────────
def section(label: str, emoji: str = "🔷") -> None:
    """Print a styled section banner."""
    display(HTML(f"""
    <div style="background:linear-gradient(90deg,#1E293B,#334155);
                color:#F1F5F9; padding:10px 18px; border-radius:8px;
                font-family:'Segoe UI',Arial,sans-serif;
                font-size:15px; font-weight:700; margin:18px 0 6px 0;
                letter-spacing:.5px;">
        {emoji} {label}
    </div>"""))


def note(text: str) -> None:
    """Print a styled info note."""
    display(HTML(f"""
    <div style="background:#EFF6FF; border-left:4px solid #3B82F6;
                padding:8px 14px; border-radius:0 6px 6px 0;
                font-family:'Segoe UI',Arial,sans-serif; font-size:13px;
                color:#1E40AF; margin:6px 0 10px 0;">
        ℹ️ {text}
    </div>"""))


def definition(term: str, desc: str) -> None:
    """Print a styled term-definition block."""
    display(HTML(f"""
    <div style="background:#F0FDF4; border-left:4px solid #22C55E;
                padding:8px 14px; border-radius:0 6px 6px 0;
                font-family:'Segoe UI',Arial,sans-serif; font-size:13px;
                color:#166534; margin:6px 0 10px 0;">
        <b>📖 {term}:</b> {desc}
    </div>"""))


def sql_box(query: str) -> None:
    """Render a SQL query in a syntax-highlighted-style code box."""
    # minimal keyword highlighting
    keywords = ["SELECT","FROM","WHERE","INSERT","INTO","VALUES","UPDATE","SET",
                "DELETE","CREATE","TABLE","DROP","ALTER","GROUP BY","ORDER BY",
                "HAVING","LIMIT","JOIN","ON","AND","OR","NOT","AS","DISTINCT",
                "COUNT","SUM","AVG","MIN","MAX","RANK","OVER","PARTITION BY",
                "WITH","CASE","WHEN","THEN","ELSE","END","IF EXISTS",
                "PRIMARY KEY","RETURNING"]
    highlighted = query
    for kw in sorted(keywords, key=len, reverse=True):
        highlighted = highlighted.replace(
            kw,
            f'<span style="color:#7C3AED;font-weight:700">{kw}</span>'
        )
        highlighted = highlighted.replace(kw.lower(), f'<span style="color:#7C3AED;font-weight:700">{kw}</span>')  # noqa

    display(HTML(f"""
    <div style="background:#1E293B; color:#E2E8F0;
                font-family:'Courier New',monospace; font-size:12.5px;
                padding:14px 18px; border-radius:8px;
                margin:6px 0 10px 0; white-space:pre-wrap;
                line-height:1.7; border:1px solid #334155;">
{highlighted}
    </div>"""))


# ── PLOT HELPERS ─────────────────────────────────────────────────────────────

def _base_fig(figsize=(9, 4.5), title="", xlabel="", ylabel=""):
    fig, ax = plt.subplots(figsize=figsize, facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.grid(axis="y", color=GRID_CLR, linewidth=0.8, zorder=0)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.spines["bottom"].set_color(GRID_CLR)
    ax.tick_params(colors=TEXT_CLR, labelsize=10)
    if title:  ax.set_title(title, color=TITLE_CLR, fontsize=13, fontweight="bold", pad=12)
    if xlabel: ax.set_xlabel(xlabel, color=TEXT_CLR, fontsize=10)
    if ylabel: ax.set_ylabel(ylabel, color=TEXT_CLR, fontsize=10)
    return fig, ax


def plot_bar(result, x_col: str, y_col: str,
             title: str = "", xlabel: str = "", ylabel: str = "",
             color: str = None, horizontal: bool = False) -> None:
    """Bar chart from a DuckDB result or DataFrame."""
    df = result.df() if hasattr(result, "df") else result
    fig, ax = _base_fig(title=title,
                        xlabel=xlabel or (y_col if horizontal else x_col),
                        ylabel=ylabel or (x_col if horizontal else y_col))
    colors = [color or PALETTE[i % len(PALETTE)] for i in range(len(df))]
    if horizontal:
        bars = ax.barh(df[x_col].astype(str), df[y_col], color=colors, zorder=3, height=0.6)
        for bar in bars:
            w = bar.get_width()
            ax.text(w * 1.01, bar.get_y() + bar.get_height()/2,
                    f"{w:,.0f}", va="center", fontsize=9, color=TEXT_CLR)
        ax.grid(axis="x", color=GRID_CLR); ax.grid(axis="y", visible=False)
    else:
        bars = ax.bar(df[x_col].astype(str), df[y_col], color=colors, zorder=3, width=0.6)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h * 1.01,
                    f"{h:,.0f}", ha="center", fontsize=9, color=TEXT_CLR)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()


def plot_pie(result, label_col: str, value_col: str, title: str = "") -> None:
    """Pie / donut chart."""
    df = result.df() if hasattr(result, "df") else result
    fig, ax = plt.subplots(figsize=(6, 5), facecolor=BG_COLOR)
    wedges, texts, autotexts = ax.pie(
        df[value_col], labels=df[label_col],
        colors=PALETTE[:len(df)],
        autopct="%1.1f%%", startangle=140,
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
        pctdistance=0.75)
    for at in autotexts:
        at.set_fontsize(10); at.set_color("white"); at.set_fontweight("bold")
    if title:
        ax.set_title(title, color=TITLE_CLR, fontsize=13, fontweight="bold")
    plt.tight_layout(); plt.show()


def plot_hist(result, col: str, title: str = "", bins: int = 8,
              xlabel: str = "", color: str = None) -> None:
    """Histogram for a numeric column."""
    df = result.df() if hasattr(result, "df") else result
    fig, ax = _base_fig(title=title, xlabel=xlabel or col, ylabel="Count")
    ax.hist(df[col].dropna(), bins=bins,
            color=color or PALETTE[0], edgecolor="white", linewidth=0.8, zorder=3)
    plt.tight_layout(); plt.show()


def plot_scatter(result, x_col: str, y_col: str,
                 hue_col: str = None, title: str = "") -> None:
    """Scatter plot, optionally coloured by a categorical column."""
    df = result.df() if hasattr(result, "df") else result
    fig, ax = _base_fig(figsize=(8, 5), title=title,
                        xlabel=x_col, ylabel=y_col)
    if hue_col:
        cats = df[hue_col].unique()
        cmap = {c: PALETTE[i % len(PALETTE)] for i, c in enumerate(cats)}
        for cat in cats:
            sub = df[df[hue_col] == cat]
            ax.scatter(sub[x_col], sub[y_col], color=cmap[cat],
                       label=cat, s=90, edgecolor="white", linewidth=0.6, zorder=3)
        ax.legend(title=hue_col, fontsize=9, title_fontsize=9)
    else:
        ax.scatter(df[x_col], df[y_col],
                   color=PALETTE[0], s=90, edgecolor="white", zorder=3)
    plt.tight_layout(); plt.show()


def plot_grouped_bar(result, x_col: str, y_col: str, group_col: str,
                     title: str = "", ylabel: str = "") -> None:
    """Grouped bar chart."""
    df = result.df() if hasattr(result, "df") else result
    pivot = df.pivot(index=x_col, columns=group_col, values=y_col)
    fig, ax = _base_fig(figsize=(10, 5), title=title,
                        xlabel=x_col, ylabel=ylabel or y_col)
    pivot.plot(kind="bar", ax=ax, color=PALETTE[:pivot.shape[1]],
               edgecolor="white", width=0.7, zorder=3)
    ax.legend(fontsize=9); plt.xticks(rotation=20, ha="right")
    plt.tight_layout(); plt.show()


def plot_box(result, x_col: str, y_col: str, title: str = "") -> None:
    """Box plot of a numeric column grouped by a categorical column."""
    df = result.df() if hasattr(result, "df") else result
    fig, ax = _base_fig(figsize=(9, 5), title=title,
                        xlabel=x_col, ylabel=y_col)
    groups = [df[df[x_col] == g][y_col].dropna().values
              for g in df[x_col].unique()]
    bp = ax.boxplot(groups, labels=df[x_col].unique(), patch_artist=True, notch=False)
    for i, patch in enumerate(bp["boxes"]):
        patch.set_facecolor(PALETTE[i % len(PALETTE)])
        patch.set_alpha(0.8)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout(); plt.show()


def plot_line(result, x_col: str, y_col: str,
              title: str = "", xlabel: str = "", ylabel: str = "") -> None:
    """Line chart."""
    df = result.df() if hasattr(result, "df") else result
    fig, ax = _base_fig(title=title,
                        xlabel=xlabel or x_col,
                        ylabel=ylabel or y_col)
    ax.plot(df[x_col].astype(str), df[y_col],
            color=PALETTE[0], linewidth=2.5, marker="o",
            markersize=7, markerfacecolor="white",
            markeredgewidth=2, zorder=3)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout(); plt.show()


def show_avatars(result, name_col: str = "emp_name",
                 url_col: str = "image_url",
                 dept_col: str = None,
                 salary_col: str = None) -> None:
    """
    Display employee avatar images in a grid with name / department / salary labels.
    Falls back to a coloured placeholder circle if the URL is unreachable.
    """
    df = result.df() if hasattr(result, "df") else result
    n = len(df)
    cols = min(n, 5)
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols,
                             figsize=(cols * 2.4, rows * 3),
                             facecolor=BG_COLOR)
    axes = (axes.flatten() if n > 1 else [axes])

    for i, (_, row) in enumerate(df.iterrows()):
        ax = axes[i]
        ax.set_facecolor(BG_COLOR)
        ax.axis("off")

        # Try to fetch the SVG/image; fall back to circle placeholder
        try:
            with urllib.request.urlopen(row[url_col], timeout=4) as resp:
                data = resp.read()
            img_arr = mpimg.imread(io.BytesIO(data), format="png")
            ax.imshow(img_arr)
        except Exception:
            circle = plt.Circle((0.5, 0.55), 0.32,
                                 color=PALETTE[i % len(PALETTE)],
                                 transform=ax.transAxes)
            ax.add_patch(circle)
            initials = "".join(p[0] for p in row[name_col].split()[:2])
            ax.text(0.5, 0.55, initials, transform=ax.transAxes,
                    ha="center", va="center",
                    fontsize=18, fontweight="bold", color="white")

        # Name label
        ax.set_title(row[name_col], fontsize=9, fontweight="bold",
                     color=TITLE_CLR, pad=3)

        # Optional sub-labels
        sub = ""
        if dept_col and dept_col in row.index:
            sub += f"🏢 {row[dept_col]}"
        if salary_col and salary_col in row.index:
            sub += f"\n💰 ${row[salary_col]:,}"
        if sub:
            ax.text(0.5, -0.04, sub, transform=ax.transAxes,
                    ha="center", va="top", fontsize=7.5, color=TEXT_CLR,
                    multialignment="center")

    # Hide unused axes
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.suptitle("Employee Avatars", fontsize=13, fontweight="bold",
                 color=TITLE_CLR, y=1.01)
    plt.tight_layout()
    plt.show()


def show_before_after(con, sql_before: str, sql_after: str,
                      transform_desc: str = "") -> None:
    """
    Helper to display BEFORE → transformation note → AFTER tables side-by-side.
    con  : an open duckdb.connect() connection
    """
    before = con.execute(sql_before).df()
    if transform_desc:
        display(HTML(f"""
        <div style="background:#FEF3C7; border-left:4px solid #F59E0B;
                    padding:8px 14px; border-radius:0 6px 6px 0;
                    font-family:'Segoe UI',Arial,sans-serif;
                    font-size:13px; color:#92400E; margin:6px 0 10px 0;">
            🔄 <b>Transformation:</b> {transform_desc}
        </div>"""))
    after = con.execute(sql_after).df()
    show(before, title="BEFORE")
    show(after,  title="AFTER")
