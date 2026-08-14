"""
crud_helpers.py
===============
Utility functions for the CRUD DuckDB Jupyter Notebook.

Students: You do NOT need to read or understand this file.
          It is imported at the top of the notebook to keep
          all display, tabulation, and plotting code out of
          your way so you can focus on SQL and CRUD concepts.

Helper functions used in the notebook
--------------------------------------
  run(con, sql, title)      -- SELECT: prints SQL, shows table, returns None
  query(con, sql, title)    -- SELECT for plots: same but returns DataFrame
  execute_sql(con, sql)     -- INSERT/UPDATE/DELETE: prints SQL, executes it
  section(label)            -- prints a section divider banner
"""

import textwrap
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from IPython.display import display, HTML
import duckdb

try:
    import sqlglot
    _SQLGLOT_AVAILABLE = True
except ImportError:
    _SQLGLOT_AVAILABLE = False

# ── Colour palette ───────────────────────────────────────────────────
PALETTE = {
    "SALES":    "#4C72B0",
    "BUSINESS": "#55A868",
    "AI":       "#C44E52",
    "MALE":     "#4878CF",
    "FEMALE":   "#E58606",
    "default":  "#8172B2",
}
BAR_COLORS = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#E58606",
              "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]


# ── SQL pretty-printer ───────────────────────────────────────────────
def _format_sql(sql: str) -> str:
    if _SQLGLOT_AVAILABLE:
        try:
            return sqlglot.transpile(sql, read="duckdb", write="duckdb", pretty=True)[0]
        except Exception:
            pass
    return textwrap.dedent(sql).strip()


def print_sql(sql: str) -> None:
    formatted = _format_sql(sql)
    lines  = formatted.splitlines()
    width  = max((len(ln) for ln in lines), default=20) + 4
    width  = max(width, 40)
    border = "═" * width
    print(f"\n╔{border}╗")
    print(f"║{'  SQL Statement':<{width}}║")
    print(f"╠{border}╣")
    for ln in lines:
        padded = f"  {ln}"
        print(f"║{padded:<{width}}║")
    print(f"╚{border}╝\n")


# ── Result-set tabulator ─────────────────────────────────────────────
def show_table(df: pd.DataFrame, title: str = "Result Set",
               max_rows: int = 50) -> None:
    if df is None or df.empty:
        display(HTML(f"<p><i>No rows returned for: <b>{title}</b></i></p>"))
        return
    df_show = df.head(max_rows).copy()
    # Render image_url as <img> tag if the column exists
    if 'image_url' in df_show.columns:
        df_show['image_url'] = df_show['image_url'].apply(
            lambda u: f'<img src="{u}" width="32" height="32" '
                      f'style="border-radius:50%">'
            if pd.notna(u) and u else ''
        )
    df_show.insert(0, "#", range(1, len(df_show) + 1))
    styled = (
        df_show.style
        .set_caption(title)
        .set_table_styles([
            {"selector": "caption",
             "props": [("font-size", "15px"), ("font-weight", "bold"),
                       ("color", "#2c3e50"), ("padding", "8px 0"),
                       ("text-align", "left")]},
            {"selector": "thead th",
             "props": [("background-color", "#2c3e50"), ("color", "white"),
                       ("padding", "8px 12px"), ("text-align", "center")]},
            {"selector": "tbody td",
             "props": [("padding", "6px 12px"), ("text-align", "center")]},
            {"selector": "tbody tr:nth-child(even)",
             "props": [("background-color", "#f2f6fc")]},
            {"selector": "tbody tr:hover",
             "props": [("background-color", "#d6eaf8")]},
            {"selector": "",
             "props": [("border-collapse", "collapse"),
                       ("font-family", "monospace"), ("font-size", "13px")]},
        ])
        .hide(axis="index")
    )
    # If image_url column has <img> tags, render as HTML
    if 'image_url' in df_show.columns:
        html_str = styled.to_html()
        # Unescape the <img> tags so they render properly
        html_str = html_str.replace('&lt;img ', '<img ')
        html_str = html_str.replace('&gt;', '>')
        html_str = html_str.replace('&quot;', '"')
        html_str = html_str.replace('&#x27;', "'")
        display(HTML(html_str))
    else:
        display(styled)


# ── run: display only, returns None ─────────────────────────────────
def run(con: duckdb.DuckDBPyConnection, sql: str,
        title: str = "Result Set") -> None:
    """
    Pretty-print SQL, execute it, show the result table exactly once.
    Returns None — Jupyter has nothing to auto-display a second time.
    Use this for all SELECT cells in the notebook.
    """
    print_sql(sql)
    df = con.execute(sql).df()
    show_table(df, title=title)


# ── query: same as run but returns the DataFrame for plotting ────────
def query(con: duckdb.DuckDBPyConnection, sql: str,
          title: str = "Result Set") -> pd.DataFrame:
    """
    Pretty-print SQL, execute it, show the result table, AND return
    the DataFrame so it can be passed to a plot function.
    Always assign the result:  df = query(con, sql, title)
    Make sure the plot call follows on the next line — never leave
    query() as the last expression in a cell.
    """
    print_sql(sql)
    df = con.execute(sql).df()
    show_table(df, title=title)
    return df


# ── execute_sql: INSERT / UPDATE / DELETE ────────────────────────────
def execute_sql(con: duckdb.DuckDBPyConnection, sql: str) -> None:
    """
    Pretty-print SQL and execute it.  No result set is returned.
    Use this for INSERT, UPDATE, DELETE, CREATE, DROP.
    """
    print_sql(sql)
    con.execute(sql)


# ── Section header ───────────────────────────────────────────────────
def section(label: str) -> None:
    print(f"\n{'━'*60}")
    print(f"  {label}")
    print(f"{'━'*60}\n")


# ── Plot helpers ─────────────────────────────────────────────────────
def plot_hbar(df, x_col, y_col, title, xlabel="", color_col=None,
              figsize=(8, 4)):
    fig, ax = plt.subplots(figsize=figsize)
    colors = ([PALETTE.get(v, PALETTE["default"]) for v in df[color_col]]
              if color_col else BAR_COLORS[:len(df)])
    bars = ax.barh(df[y_col].astype(str), df[x_col], color=colors,
                   edgecolor="white", linewidth=0.8)
    ax.bar_label(bars, fmt=_smart_fmt(df[x_col]), padding=4,
                 fontsize=10, color="#2c3e50")
    ax.set_title(title, fontsize=14, fontweight="bold", color="#2c3e50", pad=10)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(
        lambda v, _: f"${v:,.0f}" if "salary" in xlabel.lower() else f"{v:,.0f}"))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()


def plot_vbar(df, x_col, y_col, title, ylabel="", color_col=None,
              figsize=(8, 4)):
    fig, ax = plt.subplots(figsize=figsize)
    colors = ([PALETTE.get(v, PALETTE["default"]) for v in df[color_col]]
              if color_col else BAR_COLORS[:len(df)])
    bars = ax.bar(df[x_col].astype(str), df[y_col], color=colors,
                  edgecolor="white", linewidth=0.8)
    ax.bar_label(bars, fmt=_smart_fmt(df[y_col]), padding=4,
                 fontsize=10, color="#2c3e50")
    ax.set_title(title, fontsize=14, fontweight="bold", color="#2c3e50", pad=10)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda v, _: f"${v:,.0f}" if "salary" in ylabel.lower() else f"{v:,.0f}"))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()


def plot_pie(df, label_col, value_col, title, figsize=(6, 6)):
    colors = [PALETTE.get(v, BAR_COLORS[i % len(BAR_COLORS)])
              for i, v in enumerate(df[label_col])]
    fig, ax = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax.pie(
        df[value_col], labels=df[label_col], autopct="%1.1f%%",
        startangle=90, colors=colors, pctdistance=0.78,
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    )
    for t in autotexts:
        t.set_fontsize(11); t.set_fontweight("bold"); t.set_color("white")
    ax.set_title(title, fontsize=14, fontweight="bold", color="#2c3e50", pad=12)
    plt.tight_layout()
    plt.show()


def plot_salary_range(df, dept_col, min_col, max_col, title, figsize=(9, 5)):
    import numpy as np
    depts = df[dept_col].tolist()
    x, w = np.arange(len(depts)), 0.35
    fig, ax = plt.subplots(figsize=figsize)
    b1 = ax.bar(x - w/2, df[min_col], w, label="Min Salary",
                color="#4C72B0", edgecolor="white")
    b2 = ax.bar(x + w/2, df[max_col], w, label="Max Salary",
                color="#C44E52", edgecolor="white")
    ax.bar_label(b1, fmt="$%,.0f", padding=3, fontsize=9)
    ax.bar_label(b2, fmt="$%,.0f", padding=3, fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(depts, fontsize=11)
    ax.set_title(title, fontsize=14, fontweight="bold", color="#2c3e50", pad=10)
    ax.set_ylabel("Salary (USD)", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.legend(fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()


def _smart_fmt(series):
    if pd.api.types.is_float_dtype(series):
        return "%.1f%%"
    if series.max() > 999:
        return lambda v, _=None: f"${v:,.0f}"
    return "%d"
