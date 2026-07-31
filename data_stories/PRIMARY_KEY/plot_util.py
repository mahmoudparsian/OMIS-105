"""
plot_util.py
============
Utility functions for the Primary Key data story notebook.

Provides:
  - display_table()   : pretty-print a DataFrame with row numbers
  - plot_bar()        : generic horizontal/vertical bar chart
  - plot_salary_range(): min/max salary comparison per group
  - plot_gender_pie() : pie chart for gender distribution
  - plot_dept_bar()   : bar chart for department distribution
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from IPython.display import display, HTML


# ── colour palette ──────────────────────────────────────────────────────────
PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2",
           "#937860", "#DA8BC3", "#8C8C8C"]

GENDER_COLORS = {"MALE": "#4C72B0", "FEMALE": "#DD8452", "FMALE": "#DD8452"}


# ── table display ────────────────────────────────────────────────────────────

def display_table(df: pd.DataFrame, title: str = "") -> None:
    """
    Display a pandas DataFrame as a styled HTML table with row numbers.

    Parameters
    ----------
    df    : DataFrame to display
    title : optional heading shown above the table
    """
    if df is None or df.empty:
        print("(empty result set)")
        return

    styled = df.copy()
    styled.index = range(1, len(styled) + 1)
    styled.index.name = "#"

    html_parts = []
    if title:
        html_parts.append(
            f'<h4 style="font-family:sans-serif;margin-bottom:4px;">{title}</h4>'
        )

    table_html = styled.to_html(
        border=0,
        classes="styled-table",
    )

    css = """
    <style>
      .styled-table {
        border-collapse: collapse;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 13px;
        min-width: 420px;
      }
      .styled-table thead tr {
        background-color: #4C72B0;
        color: #ffffff;
        text-align: left;
      }
      .styled-table th, .styled-table td {
        padding: 8px 14px;
      }
      .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
      }
      .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f6fb;
      }
      .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #4C72B0;
      }
    </style>
    """

    html_parts.append(css + table_html)
    display(HTML("".join(html_parts)))


# ── generic bar chart ────────────────────────────────────────────────────────

def plot_bar(
    labels,
    values,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    color: str = "#4C72B0",
    horizontal: bool = False,
    figsize=(8, 4),
    value_fmt: str = "{:.0f}",
) -> None:
    """
    Draw a simple bar (or horizontal bar) chart.

    Parameters
    ----------
    labels      : sequence of category labels
    values      : sequence of numeric values
    title       : chart title
    xlabel/ylabel: axis labels
    color       : bar fill colour
    horizontal  : if True draw a horizontal bar chart
    figsize     : (width, height) in inches
    value_fmt   : format string for bar labels
    """
    fig, ax = plt.subplots(figsize=figsize)
    labels = list(labels)
    values = list(values)

    if horizontal:
        bars = ax.barh(labels, values, color=color, edgecolor="white", height=0.55)
        ax.set_xlabel(xlabel or "Value")
        ax.set_ylabel(ylabel or "")
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_width() + max(values) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                value_fmt.format(val),
                va="center",
                fontsize=10,
            )
        ax.set_xlim(0, max(values) * 1.18)
    else:
        bars = ax.bar(labels, values, color=color, edgecolor="white", width=0.55)
        ax.set_xlabel(xlabel or "")
        ax.set_ylabel(ylabel or "Value")
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(values) * 0.01,
                value_fmt.format(val),
                ha="center",
                fontsize=10,
            )
        ax.set_ylim(0, max(values) * 1.18)

    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.show()


# ── gender pie chart ─────────────────────────────────────────────────────────

def plot_gender_pie(labels, percentages, title: str = "Gender Distribution") -> None:
    """
    Pie chart for gender (or any two-category) distribution.

    Parameters
    ----------
    labels      : e.g. ['MALE', 'FEMALE']
    percentages : corresponding numeric values (need not sum to 100)
    title       : chart title
    """
    colors = [GENDER_COLORS.get(lbl, PALETTE[i]) for i, lbl in enumerate(labels)]
    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        percentages,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    for autotext in autotexts:
        autotext.set_fontsize(11)
        autotext.set_fontweight("bold")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=14)
    plt.tight_layout()
    plt.show()


# ── salary range chart ────────────────────────────────────────────────────────

def plot_salary_range(
    groups,
    min_salaries,
    max_salaries,
    title: str = "Salary Range by Group",
    group_label: str = "Group",
    figsize=(9, 5),
) -> None:
    """
    Grouped bar chart showing min and max salary side-by-side for each group.

    Parameters
    ----------
    groups        : category labels (e.g. department names)
    min_salaries  : min salary per group
    max_salaries  : max salary per group
    title         : chart title
    group_label   : x-axis label
    figsize       : figure size
    """
    import numpy as np

    groups = list(groups)
    min_salaries = list(min_salaries)
    max_salaries = list(max_salaries)

    x = range(len(groups))
    width = 0.35

    fig, ax = plt.subplots(figsize=figsize)
    bars_min = ax.bar(
        [i - width / 2 for i in x], min_salaries, width,
        label="Min Salary", color="#4C72B0", edgecolor="white"
    )
    bars_max = ax.bar(
        [i + width / 2 for i in x], max_salaries, width,
        label="Max Salary", color="#DD8452", edgecolor="white"
    )

    def _label_bars(bars):
        for bar in bars:
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + max(max_salaries) * 0.01,
                f"${h:,.0f}",
                ha="center", va="bottom", fontsize=9
            )

    _label_bars(bars_min)
    _label_bars(bars_max)

    ax.set_xticks(list(x))
    ax.set_xticklabels(groups)
    ax.set_xlabel(group_label)
    ax.set_ylabel("Salary ($)")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_ylim(0, max(max_salaries) * 1.20)
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.show()


# ── department distribution bar chart ─────────────────────────────────────────

def plot_dept_bar(
    departments,
    percentages,
    title: str = "Employee Distribution by Department",
    figsize=(7, 4),
) -> None:
    """
    Coloured bar chart for department headcount percentages.

    Parameters
    ----------
    departments : department name labels
    percentages : percentage values
    title       : chart title
    figsize     : figure size
    """
    departments = list(departments)
    percentages = list(percentages)
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(departments))]

    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.bar(departments, percentages, color=colors, edgecolor="white", width=0.5)

    for bar, pct in zip(bars, percentages):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(percentages) * 0.01,
            f"{pct:.1f}%",
            ha="center", fontsize=11, fontweight="bold"
        )

    ax.set_ylabel("% of Employees")
    ax.set_ylim(0, max(percentages) * 1.25)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.show()
