"""
display_utils.py
================
Utility functions for displaying query results and creating plots.
Used by the Employees & Projects DuckDB notebook.

All plotting and display logic lives here so the notebook
stays clean and focused on SQL.

Author : OMIS 105
Date   : 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from IPython.display import display, HTML, Markdown

# ─────────────────────────────────────────────────────────
# DISPLAY / TABULATION FUNCTIONS
# ─────────────────────────────────────────────────────────

def show_table(df, title=None, max_rows=50):
    """
    Display a DataFrame as a nicely formatted HTML table
    with row numbers and a title.
    """
    if title:
        display(Markdown(f"### {title}"))

    styled_df = df.head(max_rows).copy()
    styled_df.index = range(1, len(styled_df) + 1)
    styled_df.index.name = '#'

    style = (
        styled_df.style
        .set_table_styles([
            {'selector': 'th', 'props': [
                ('background-color', '#2c3e50'),
                ('color', 'white'),
                ('font-weight', 'bold'),
                ('text-align', 'center'),
                ('padding', '8px 12px'),
                ('border', '1px solid #34495e')
            ]},
            {'selector': 'td', 'props': [
                ('padding', '6px 12px'),
                ('border', '1px solid #bdc3c7'),
                ('text-align', 'left')
            ]},
            {'selector': 'tr:nth-child(even)', 'props': [
                ('background-color', '#f8f9fa')
            ]},
            {'selector': 'tr:hover', 'props': [
                ('background-color', '#e8f4fd')
            ]},
            {'selector': 'table', 'props': [
                ('border-collapse', 'collapse'),
                ('font-family', 'Segoe UI, Arial, sans-serif'),
                ('font-size', '13px'),
                ('margin', '10px 0'),
                ('box-shadow', '0 2px 4px rgba(0,0,0,0.1)')
            ]},
            {'selector': 'caption', 'props': [
                ('font-size', '14px'),
                ('font-weight', 'bold'),
                ('margin-bottom', '8px')
            ]}
        ])
        .format(precision=2, na_rep='NULL')
    )

    display(style)

    row_count = len(df)
    if row_count > max_rows:
        display(HTML(f"<p style='color:#7f8c8d; font-size:12px;'>"
                     f"Showing {max_rows} of {row_count} rows</p>"))
    else:
        display(HTML(f"<p style='color:#7f8c8d; font-size:12px;'>"
                     f"({row_count} row{'s' if row_count != 1 else ''})</p>"))


def show_sql(sql_text):
    """Display SQL code in a formatted code block."""
    display(Markdown(f"```sql\n{sql_text.strip()}\n```"))


def show_schema(con, table_name):
    """
    Display the schema (column names & types) for a DuckDB table.
    """
    df = con.execute(f"DESCRIBE {table_name}").fetchdf()
    df = df[['column_name', 'column_type', 'null']]
    df.columns = ['Column', 'Type', 'Nullable']
    show_table(df, title=f"Schema: {table_name}")


# ─────────────────────────────────────────────────────────
# AVATAR / IMAGE DISPLAY
# ─────────────────────────────────────────────────────────

def show_employee_cards(df, name_col='employee_name', url_col='image_url',
                        detail_cols=None, cards_per_row=4):
    """
    Display employee avatar cards in a responsive grid.
    Each card shows the avatar image, name, and optional details.

    Parameters
    ----------
    df : DataFrame with at least name_col and url_col
    detail_cols : list of column names to show under the name
    cards_per_row : int
    """
    if detail_cols is None:
        detail_cols = []

    html = "<div style='display:flex; flex-wrap:wrap; gap:16px; margin:12px 0;'>"
    for _, row in df.iterrows():
        details = "".join(
            f"<div style='font-size:11px;color:#7f8c8d;'>{col}: {row[col]}</div>"
            for col in detail_cols if col in row.index
        )
        html += f"""
        <div style='border:1px solid #ddd; border-radius:10px; padding:14px;
                    width:160px; text-align:center; background:#fafafa;
                    box-shadow:0 1px 3px rgba(0,0,0,0.08);'>
            <img src='{row[url_col]}' width='72' height='72'
                 style='border-radius:50%; border:2px solid #3498db; margin-bottom:8px;'/>
            <div style='font-weight:600; font-size:13px; color:#2c3e50;'>
                {row[name_col]}
            </div>
            {details}
        </div>"""
    html += "</div>"
    display(HTML(html))


# ─────────────────────────────────────────────────────────
# PLOTTING FUNCTIONS
# ─────────────────────────────────────────────────────────

# A consistent color palette for all plots
COLORS = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#f39c12',
          '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b',
          '#8e44ad', '#d35400', '#27ae60', '#2980b9', '#f1c40f',
          '#7f8c8d', '#d4ac0d', '#2471a3', '#a93226', '#117a65']


def _setup_style():
    """Apply a clean plot style."""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 12,
        'figure.facecolor': 'white',
        'axes.facecolor': '#fafafa',
        'grid.alpha': 0.3
    })


def plot_bar(df, x_col, y_col, title="", xlabel="", ylabel="",
             horizontal=False, figsize=(10, 5), color=None,
             show_values=True, rotation=0, fmt=','):
    """
    Create a bar chart from a DataFrame.
    """
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    colors = color if color else COLORS[:len(df)]

    if horizontal:
        bars = ax.barh(df[x_col].astype(str), df[y_col],
                       color=colors, edgecolor='white', linewidth=0.5)
        ax.set_xlabel(ylabel or y_col)
        ax.set_ylabel(xlabel or x_col)
        if show_values:
            for bar in bars:
                w = bar.get_width()
                ax.text(w + max(df[y_col]) * 0.01,
                        bar.get_y() + bar.get_height() / 2,
                        f'{w:{fmt}}', va='center', fontsize=10, color='#2c3e50')
    else:
        bars = ax.bar(df[x_col].astype(str), df[y_col],
                      color=colors, edgecolor='white', linewidth=0.5)
        ax.set_xlabel(xlabel or x_col)
        ax.set_ylabel(ylabel or y_col)
        if show_values:
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2,
                        h + max(df[y_col]) * 0.01,
                        f'{h:{fmt}}', ha='center', va='bottom',
                        fontsize=10, color='#2c3e50')
        plt.xticks(rotation=rotation)

    ax.set_title(title, pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


def plot_pie(df, labels_col, values_col, title="", figsize=(7, 7)):
    """Create a pie chart from a DataFrame."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax.pie(
        df[values_col], labels=df[labels_col],
        autopct='%1.1f%%', startangle=90,
        colors=COLORS[:len(df)],
        textprops={'fontsize': 11},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight('bold')
    ax.set_title(title, pad=20, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_donut(df, labels_col, values_col, title="",
               figsize=(7, 7), center_text=""):
    """Create a donut chart (pie with a hole) from a DataFrame."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax.pie(
        df[values_col], labels=df[labels_col],
        autopct='%1.1f%%', startangle=90,
        colors=COLORS[:len(df)],
        textprops={'fontsize': 11},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'width': 0.45},
        pctdistance=0.76
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight('bold')
    if center_text:
        ax.text(0, 0, center_text, ha='center', va='center',
                fontsize=16, fontweight='bold', color='#2c3e50')
    ax.set_title(title, pad=20, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_grouped_bar(df, x_col, y_cols, title="", xlabel="", ylabel="",
                     figsize=(10, 5), legend_labels=None):
    """Create a grouped bar chart with multiple value columns."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    x = np.arange(len(df))
    width = 0.8 / len(y_cols)

    for i, col in enumerate(y_cols):
        offset = (i - len(y_cols) / 2 + 0.5) * width
        label = legend_labels[i] if legend_labels else col
        ax.bar(x + offset, df[col], width, label=label,
               color=COLORS[i], edgecolor='white', linewidth=0.5)

    ax.set_xlabel(xlabel or x_col)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(df[x_col].astype(str), rotation=30, ha='right')
    ax.legend(framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


def plot_scatter(df, x_col, y_col, title="", xlabel="", ylabel="",
                 label_col=None, figsize=(10, 6)):
    """Create a scatter plot from a DataFrame."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(df[x_col], df[y_col], c=COLORS[0], s=100,
               edgecolors='white', linewidth=1.5, alpha=0.8, zorder=5)
    if label_col:
        for _, row in df.iterrows():
            ax.annotate(row[label_col], (row[x_col], row[y_col]),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=9, color='#2c3e50')
    ax.set_xlabel(xlabel or x_col)
    ax.set_ylabel(ylabel or y_col)
    ax.set_title(title, pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


def plot_line(df, x_col, y_col, title="", xlabel="", ylabel="",
              figsize=(10, 5), marker='o'):
    """Create a line chart from a DataFrame."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df[x_col].astype(str), df[y_col], marker=marker,
            color=COLORS[0], linewidth=2.5, markersize=8,
            markerfacecolor='white', markeredgewidth=2,
            markeredgecolor=COLORS[0])
    ax.fill_between(range(len(df)), df[y_col], alpha=0.1, color=COLORS[0])
    ax.set_xlabel(xlabel or x_col)
    ax.set_ylabel(ylabel or y_col)
    ax.set_title(title, pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


def plot_heatmap(df, title="", figsize=(12, 8), fmt=".1f", cmap="YlOrRd"):
    """Create a heatmap from a pivot-style DataFrame."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(df.values, cmap=cmap, aspect='auto')

    ax.set_xticks(range(len(df.columns)))
    ax.set_yticks(range(len(df.index)))
    ax.set_xticklabels(df.columns, rotation=45, ha='right')
    ax.set_yticklabels(df.index)

    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            val = df.values[i, j]
            if not np.isnan(val) and val != 0:
                vmax = df.values[~np.isnan(df.values)].max()
                ax.text(j, i, format(val, fmt), ha='center', va='center',
                        color='white' if val > vmax * 0.6 else 'black',
                        fontsize=9, fontweight='bold')

    plt.colorbar(im, ax=ax, shrink=0.8, label='Hours')
    ax.set_title(title, pad=15)
    plt.tight_layout()
    plt.show()


def plot_stacked_bar(df, x_col, y_cols, title="", xlabel="", ylabel="",
                     figsize=(10, 5), legend_labels=None):
    """Create a stacked bar chart."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    bottom = np.zeros(len(df))
    for i, col in enumerate(y_cols):
        label = legend_labels[i] if legend_labels else col
        ax.bar(df[x_col].astype(str), df[col], bottom=bottom,
               label=label, color=COLORS[i], edgecolor='white', linewidth=0.5)
        bottom += df[col].values

    ax.set_xlabel(xlabel or x_col)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=15)
    ax.legend(framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


def plot_lollipop(df, x_col, y_col, title="", xlabel="", ylabel="",
                  figsize=(10, 6), color=None):
    """
    Create a lollipop chart — a clean alternative to bar charts
    when you have many categories.
    """
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    c = color or COLORS[1]
    y_pos = range(len(df))

    ax.hlines(y=y_pos, xmin=0, xmax=df[y_col], color=c, alpha=0.5, linewidth=2)
    ax.plot(df[y_col], y_pos, 'o', color=c, markersize=10)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(df[x_col].astype(str))
    ax.set_xlabel(ylabel or y_col)
    ax.set_title(title, pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.show()


def plot_dual_bar(df, x_col, y1_col, y2_col, title="",
                  xlabel="", y1_label="", y2_label="",
                  figsize=(10, 5)):
    """
    Create a dual-axis bar + line chart for comparing two
    metrics on different scales.
    """
    _setup_style()
    fig, ax1 = plt.subplots(figsize=figsize)
    x = np.arange(len(df))

    bars = ax1.bar(x, df[y1_col], color=COLORS[0], alpha=0.7,
                   edgecolor='white', label=y1_label or y1_col)
    ax1.set_ylabel(y1_label or y1_col, color=COLORS[0])
    ax1.tick_params(axis='y', labelcolor=COLORS[0])

    ax2 = ax1.twinx()
    ax2.plot(x, df[y2_col], color=COLORS[3], marker='D', linewidth=2.5,
             markersize=7, label=y2_label or y2_col)
    ax2.set_ylabel(y2_label or y2_col, color=COLORS[3])
    ax2.tick_params(axis='y', labelcolor=COLORS[3])

    ax1.set_xticks(x)
    ax1.set_xticklabels(df[x_col].astype(str), rotation=30, ha='right')
    ax1.set_title(title, pad=15)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left',
               framealpha=0.9)

    ax1.spines['top'].set_visible(False)
    plt.tight_layout()
    plt.show()
