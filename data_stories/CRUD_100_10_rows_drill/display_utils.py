"""
display_utils.py
================
Utility functions for displaying DuckDB query results
and creating beautiful plots.

Keep this module OUTSIDE the notebook so that students
see clean SQL cells without plotting / display clutter.

Usage inside a notebook cell:
    from display_utils import show, plot_bar, plot_pie, ...
"""

import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import textwrap

# ── colour palette (colour-blind friendly) ──────────────────────────
COLORS = [
    "#4E79A7", "#F28E2B", "#E15759", "#76B7B2",
    "#59A14F", "#EDC948", "#B07AA1", "#FF9DA7",
    "#9C755F", "#BAB0AC",
]
MALE_COLOR   = "#4E79A7"
FEMALE_COLOR = "#E15759"

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "#F9F9F9",
    "axes.grid":        True,
    "grid.alpha":       0.3,
    "font.size":        11,
    "axes.titlesize":   14,
    "axes.labelsize":   12,
})


# =====================================================================
# 1.  DISPLAY helpers
# =====================================================================

def show(sql, title=None, row_numbers=True):
    """
    Execute *sql* on DuckDB's default connection (shared with %%dql)
    and display the result as a nicely formatted table with row numbers.

    Parameters
    ----------
    sql  : str   – the SQL statement
    title: str   – optional heading printed above the table
    row_numbers : bool – if True, prepend a '#' column (1-based)

    Returns
    -------
    pd.DataFrame – the result set (so callers can chain with plots)
    """
    df = duckdb.sql(sql).fetchdf()
    if title:
        print(f"\n{'─'*60}")
        print(f"  {title}")
        print(f"{'─'*60}")
    if row_numbers:
        df_display = df.copy()
        df_display.insert(0, "#", range(1, len(df_display) + 1))
    else:
        df_display = df
    from IPython.display import display as ipd
    ipd(df_display.style
        .set_properties(**{
            "text-align": "left",
            "border": "1px solid #ddd",
            "padding": "6px 10px",
        })
        .set_table_styles([
            {"selector": "th",
             "props": [("background-color", "#4E79A7"),
                       ("color", "white"),
                       ("text-align", "left"),
                       ("padding", "6px 10px")]},
            {"selector": "tr:nth-child(even)",
             "props": [("background-color", "#f2f2f2")]},
        ])
        .hide(axis="index")
    )
    return df


def show_before_after(sql_transform, table="employees",
                      before_title="BEFORE", after_title="AFTER",
                      transform_title="SQL Transformation"):
    """
    1. Show the table BEFORE
    2. Pretty-print the transformation SQL
    3. Execute the transformation
    4. Show the table AFTER

    Uses DuckDB's default connection (shared with %%dql).
    """
    # ── before ──
    show(f"SELECT * FROM {table} ORDER BY emp_id",
         title=before_title)

    # ── SQL ──
    print(f"\n{'━'*60}")
    print(f"  {transform_title}")
    print(f"{'━'*60}")
    _pretty_sql(sql_transform)

    # ── execute ──
    duckdb.execute(sql_transform)

    # ── after ──
    show(f"SELECT * FROM {table} ORDER BY emp_id",
         title=after_title)


def _pretty_sql(sql):
    """Print SQL in a highlighted box."""
    from IPython.display import display, Markdown
    display(Markdown(f"```sql\n{textwrap.dedent(sql).strip()}\n```"))


def pretty_sql(sql):
    """Public version – print formatted SQL in a code block."""
    _pretty_sql(sql)


def show_with_images(sql, title=None, img_col="image_url",
                     img_size=50):
    """
    Execute *sql* and display the result as an HTML table that
    renders the *img_col* column as inline avatar images.

    Parameters
    ----------
    sql      : str  – SQL query (must include *img_col*)
    title    : str  – optional heading
    img_col  : str  – column name containing the image URL
    img_size : int  – avatar width/height in pixels
    """
    from IPython.display import display, HTML

    df = duckdb.sql(sql).fetchdf()

    if title:
        print(f"\n{'─'*60}")
        print(f"  {title}")
        print(f"{'─'*60}")

    # ── build HTML table ──
    cols = list(df.columns)
    header = "".join(
        f'<th style="background:#4E79A7;color:#fff;padding:8px 12px;'
        f'text-align:left;">{c}</th>'
        for c in ["#"] + cols
    )

    rows_html = []
    for idx, row in df.iterrows():
        bg = "#f2f2f2" if idx % 2 == 0 else "#ffffff"
        cells = [
            f'<td style="padding:6px 10px;border:1px solid #ddd;'
            f'background:{bg};">{idx + 1}</td>'
        ]
        for c in cols:
            val = row[c]
            if c == img_col:
                cell_content = (
                    f'<img src="{val}" '
                    f'width="{img_size}" height="{img_size}" '
                    f'style="border-radius:50%;vertical-align:middle;" />'
                )
            else:
                # Format salary with $ and commas if numeric
                if isinstance(val, (int, float)) and c.lower() in (
                        "salary", "avg_salary", "min_salary", "max_salary",
                        "total_salary"):
                    cell_content = f"${val:,.0f}"
                else:
                    cell_content = str(val)
            cells.append(
                f'<td style="padding:6px 10px;border:1px solid #ddd;'
                f'background:{bg};">{cell_content}</td>'
            )
        rows_html.append(f'<tr>{"".join(cells)}</tr>')

    html = (
        f'<table style="border-collapse:collapse;font-size:13px;'
        f'font-family:sans-serif;">'
        f'<thead><tr>{header}</tr></thead>'
        f'<tbody>{"".join(rows_html)}</tbody></table>'
    )
    display(HTML(html))
    return df


# =====================================================================
# 2.  PLOT helpers
# =====================================================================

def plot_bar(df, x, y, title="", xlabel="", ylabel="",
             color=None, horizontal=False, figsize=(8, 4),
             fmt="${:,.0f}", annotate=True, rotation=0):
    """Generic bar chart from a DataFrame."""
    fig, ax = plt.subplots(figsize=figsize)
    colors = color if color else COLORS[:len(df)]
    if horizontal:
        bars = ax.barh(df[x].astype(str), df[y], color=colors)
        ax.set_xlabel(ylabel or y)
        ax.set_ylabel(xlabel or x)
        if annotate:
            for bar in bars:
                w = bar.get_width()
                ax.text(w + max(df[y])*0.01, bar.get_y() + bar.get_height()/2,
                        fmt.format(w), va="center", fontsize=10)
    else:
        bars = ax.bar(df[x].astype(str), df[y], color=colors)
        ax.set_xlabel(xlabel or x)
        ax.set_ylabel(ylabel or y)
        if annotate:
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, h + max(df[y])*0.01,
                        fmt.format(h), ha="center", fontsize=10)
    ax.set_title(title, fontweight="bold")
    plt.xticks(rotation=rotation)
    plt.tight_layout()
    plt.show()


def plot_pie(df, labels_col, values_col, title="",
             figsize=(6, 6), colors=None, startangle=140):
    """Generic pie chart from a DataFrame."""
    fig, ax = plt.subplots(figsize=figsize)
    c = colors if colors else COLORS[:len(df)]
    wedges, texts, autotexts = ax.pie(
        df[values_col], labels=df[labels_col],
        autopct="%1.1f%%", startangle=startangle,
        colors=c, textprops={"fontsize": 12},
    )
    for t in autotexts:
        t.set_fontweight("bold")
    ax.set_title(title, fontweight="bold", fontsize=14)
    plt.tight_layout()
    plt.show()


def plot_grouped_bar(df, group_col, x_col, y_col, title="",
                     xlabel="", ylabel="", figsize=(10, 5),
                     fmt="${:,.0f}"):
    """Grouped bar chart – one cluster per x_col value, bars per group_col."""
    import numpy as np
    groups = df[group_col].unique()
    x_vals = df[x_col].unique()
    n = len(groups)
    width = 0.8 / n
    fig, ax = plt.subplots(figsize=figsize)
    x_pos = np.arange(len(x_vals))

    for i, g in enumerate(groups):
        subset = df[df[group_col] == g]
        vals = [subset.loc[subset[x_col] == xv, y_col].values[0]
                if xv in subset[x_col].values else 0 for xv in x_vals]
        bars = ax.bar(x_pos + i * width, vals, width,
                      label=g, color=COLORS[i % len(COLORS)])
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x() + bar.get_width()/2, h,
                        fmt.format(h), ha="center", va="bottom",
                        fontsize=8)

    ax.set_xticks(x_pos + width * (n - 1) / 2)
    ax.set_xticklabels(x_vals)
    ax.set_xlabel(xlabel or x_col)
    ax.set_ylabel(ylabel or y_col)
    ax.set_title(title, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_salary_range(df, title="Salary Range by Department",
                      figsize=(9, 5)):
    """
    Expects columns: department, min_salary, max_salary, avg_salary.
    Draws a range (lollipop) chart.
    """
    fig, ax = plt.subplots(figsize=figsize)
    depts = df["department"].values
    y_pos = range(len(depts))

    for i, (dept, lo, hi, avg) in enumerate(
            zip(depts, df["min_salary"], df["max_salary"], df["avg_salary"])):
        ax.plot([lo, hi], [i, i], color=COLORS[i % len(COLORS)],
                linewidth=4, solid_capstyle="round")
        ax.scatter([lo, hi], [i, i], color=COLORS[i % len(COLORS)],
                   s=80, zorder=5)
        ax.scatter([avg], [i], color="black", s=60, zorder=6, marker="D")
        ax.text(hi + 2000, i, f"${hi:,.0f}", va="center", fontsize=9)
        ax.text(lo - 2000, i, f"${lo:,.0f}", va="center",
                ha="right", fontsize=9)

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(depts)
    ax.set_xlabel("Salary ($)")
    ax.set_title(title, fontweight="bold")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    plt.tight_layout()
    plt.show()


def plot_gender_salary(df, title="Average Salary by Gender",
                       figsize=(6, 4)):
    """Bar chart comparing avg salary by gender."""
    fig, ax = plt.subplots(figsize=figsize)
    colors = [MALE_COLOR if g == "MALE" else FEMALE_COLOR
              for g in df["gender"]]
    bars = ax.bar(df["gender"], df["avg_salary"], color=colors)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 500,
                f"${h:,.0f}", ha="center", fontweight="bold")
    ax.set_title(title, fontweight="bold")
    ax.set_ylabel("Average Salary ($)")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    plt.tight_layout()
    plt.show()


def plot_horizontal_salary(df, name_col="emp_name", salary_col="salary",
                           title="Employee Salaries", figsize=(8, 5)):
    """Horizontal bar chart of individual salaries."""
    fig, ax = plt.subplots(figsize=figsize)
    df_sorted = df.sort_values(salary_col)
    colors = [COLORS[i % len(COLORS)] for i in range(len(df_sorted))]
    bars = ax.barh(df_sorted[name_col], df_sorted[salary_col], color=colors)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1000, bar.get_y() + bar.get_height()/2,
                f"${w:,.0f}", va="center", fontsize=9)
    ax.set_xlabel("Salary ($)")
    ax.set_title(title, fontweight="bold")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    plt.tight_layout()
    plt.show()
