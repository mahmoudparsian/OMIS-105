"""
fk_joins_plot_util.py
=====================
Display and plotting utilities for the FK + JOINs notebook.

Functions
---------
display_table(df, title)         — styled HTML table with row numbers
plot_join_counts(labels, counts) — bar chart comparing join result sizes
plot_salary_by_dept(df)          — horizontal bar chart: avg salary per dept
plot_budget_vs_headcount(df)     — scatter plot: dept budget vs headcount
plot_null_dept_pie(n_assigned, n_null) — pie: employees with/without dept
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from IPython.display import display, HTML

# ── Colour palette ────────────────────────────────────────────────────────────
PALETTE   = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"]
JOIN_COLORS = {
    "INNER JOIN": "#4C72B0",
    "LEFT JOIN":  "#55A868",
    "RIGHT JOIN": "#DD8452",
}


# ── Table display ─────────────────────────────────────────────────────────────

def display_table(df: pd.DataFrame, title: str = "") -> None:
    """Pretty-print a DataFrame as a styled HTML table with row numbers."""
    if df is None or df.empty:
        if title:
            print(f"({title} — empty result set)")
        else:
            print("(empty result set)")
        return

    styled = df.copy()
    styled.index = range(1, len(styled) + 1)
    styled.index.name = "#"

    css = """
    <style>
      .fk-table {
        border-collapse: collapse;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 13px;
        min-width: 400px;
      }
      .fk-table thead tr {
        background-color: #2c5f8a;
        color: #ffffff;
        text-align: left;
      }
      .fk-table th, .fk-table td {
        padding: 7px 14px;
      }
      .fk-table tbody tr {
        border-bottom: 1px solid #dde3ec;
      }
      .fk-table tbody tr:nth-of-type(even) {
        background-color: #f0f4fa;
      }
      .fk-table tbody tr:last-of-type {
        border-bottom: 2px solid #2c5f8a;
      }
      .null-cell { color: #aaa; font-style: italic; }
    </style>
    """

    # Highlight NULL values visually
    # na_rep handles np.nan; replace catches pd.NA which renders as &lt;NA&gt;
    table_html = (
        styled.to_html(border=0, classes="fk-table", na_rep="NULL")
              .replace(">&lt;NA&gt;<", ">NULL<")
              .replace(">NULL<", ' class="null-cell">NULL<')
    )

    heading = (
        f'<h4 style="font-family:sans-serif;margin-bottom:4px;">{title}</h4>'
        if title else ""
    )
    display(HTML(heading + css + table_html))


# ── Join result size comparison ───────────────────────────────────────────────

def plot_join_counts(labels: list, counts: list,
                     title: str = "Rows returned by each JOIN type") -> None:
    """Bar chart comparing how many rows each join type returns."""
    colors = [JOIN_COLORS.get(lbl, PALETTE[i]) for i, lbl in enumerate(labels)]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.bar(labels, counts, color=colors, edgecolor="white", width=0.45)
    for bar, val in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.08,
            str(val),
            ha="center", fontsize=12, fontweight="bold"
        )
    ax.set_ylabel("Row count")
    ax.set_ylim(0, max(counts) * 1.3)
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.show()


# ── Average salary per department ─────────────────────────────────────────────

def plot_salary_by_dept(df: pd.DataFrame,
                        dept_col: str = "dept_name",
                        salary_col: str = "avg_salary",
                        title: str = "Average Salary by Department") -> None:
    """Horizontal bar chart of average salary per department."""
    df = df.dropna(subset=[dept_col, salary_col]).sort_values(salary_col)
    fig, ax = plt.subplots(figsize=(7, 3.5))
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(df))]
    bars = ax.barh(df[dept_col], df[salary_col],
                   color=colors, edgecolor="white", height=0.5)
    for bar, val in zip(bars, df[salary_col]):
        ax.text(
            bar.get_width() + df[salary_col].max() * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"${val:,.0f}",
            va="center", fontsize=10
        )
    ax.set_xlabel("Average Salary ($)")
    ax.set_xlim(0, df[salary_col].max() * 1.20)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.show()


# ── Budget vs headcount scatter ───────────────────────────────────────────────

def plot_budget_vs_headcount(df: pd.DataFrame,
                              dept_col: str = "dept_name",
                              budget_col: str = "budget",
                              count_col: str = "headcount",
                              title: str = "Department Budget vs Headcount") -> None:
    """Scatter plot: each dot is a department; x=headcount, y=budget."""
    df = df.dropna(subset=[dept_col, budget_col, count_col])
    fig, ax = plt.subplots(figsize=(6, 4))
    for i, row in df.iterrows():
        ax.scatter(row[count_col], row[budget_col],
                   s=120, color=PALETTE[i % len(PALETTE)], zorder=3)
        ax.annotate(
            row[dept_col],
            (row[count_col], row[budget_col]),
            textcoords="offset points", xytext=(8, 4),
            fontsize=10
        )
    ax.set_xlabel("Headcount (employees)")
    ax.set_ylabel("Budget ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.show()


# ── NULL dept pie ─────────────────────────────────────────────────────────────

def plot_null_dept_pie(n_assigned: int, n_null: int,
                       title: str = "Employees: Dept Assigned vs Unassigned") -> None:
    """Pie chart showing how many employees have (or lack) a department."""
    labels = ["Dept assigned", "No dept (NULL)"]
    values = [n_assigned, n_null]
    colors = ["#4C72B0", "#cccccc"]
    fig, ax = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct="%1.0f%%",
        colors=colors, startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight("bold")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.show()
