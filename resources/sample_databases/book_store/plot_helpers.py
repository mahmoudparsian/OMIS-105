"""
plot_helpers.py
===============
Decoupled plotting functions for the Bookstore DuckDB portfolio notebook.
Each function takes a DataFrame (or Series) and returns a matplotlib Figure
so the notebook cells stay focused on SQL + results.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ── Style defaults ───────────────────────────────────────────────────
plt.rcParams.update({
    "figure.figsize": (10, 5),
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.dpi": 110,
})

PALETTE = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
    "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD",
]


# ── Generic helpers ──────────────────────────────────────────────────

def bar_chart(df, x, y, title, xlabel=None, ylabel=None,
              horizontal=False, color=None, top_n=None, figsize=None):
    """Generic bar (or horizontal bar) chart."""
    if top_n:
        df = df.head(top_n)
    fig, ax = plt.subplots(figsize=figsize or (10, 5))
    c = color or PALETTE[0]
    if horizontal:
        ax.barh(df[x].astype(str), df[y], color=c)
        ax.set_xlabel(ylabel or y)
        ax.set_ylabel(xlabel or x)
        ax.invert_yaxis()
    else:
        ax.bar(df[x].astype(str), df[y], color=c)
        ax.set_xlabel(xlabel or x)
        ax.set_ylabel(ylabel or y)
        plt.xticks(rotation=45, ha="right")
    ax.set_title(title)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    plt.tight_layout()
    return fig


def pie_chart(df, labels_col, values_col, title, figsize=None):
    """Pie / donut chart."""
    fig, ax = plt.subplots(figsize=figsize or (8, 8))
    wedges, texts, autotexts = ax.pie(
        df[values_col], labels=df[labels_col], autopct="%1.1f%%",
        colors=PALETTE[: len(df)], startangle=140,
        wedgeprops=dict(width=0.55),
    )
    for t in autotexts:
        t.set_fontsize(9)
    ax.set_title(title, fontsize=14)
    plt.tight_layout()
    return fig


def line_chart(df, x, y, title, xlabel=None, ylabel=None,
               marker="o", figsize=None):
    """Simple line chart."""
    fig, ax = plt.subplots(figsize=figsize or (10, 5))
    ax.plot(df[x].astype(str), df[y], marker=marker, color=PALETTE[0], linewidth=2)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.set_title(title)
    plt.xticks(rotation=45, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    plt.tight_layout()
    return fig


def grouped_bar_chart(df, x, groups, title, xlabel=None, ylabel=None, figsize=None):
    """Side-by-side grouped bar chart.  `groups` is a list of column names."""
    fig, ax = plt.subplots(figsize=figsize or (12, 5))
    x_vals = np.arange(len(df))
    width = 0.8 / len(groups)
    for i, g in enumerate(groups):
        ax.bar(x_vals + i * width, df[g], width, label=g, color=PALETTE[i % len(PALETTE)])
    ax.set_xticks(x_vals + width * (len(groups) - 1) / 2)
    ax.set_xticklabels(df[x].astype(str), rotation=45, ha="right")
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or "")
    ax.set_title(title)
    ax.legend()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    plt.tight_layout()
    return fig


def stacked_bar_chart(df_pivot, title, xlabel=None, ylabel=None, figsize=None):
    """Stacked bar chart from a pivoted DataFrame (index=x, columns=stack groups)."""
    fig, ax = plt.subplots(figsize=figsize or (12, 6))
    df_pivot.plot(kind="bar", stacked=True, ax=ax, color=PALETTE[: df_pivot.shape[1]])
    ax.set_xlabel(xlabel or "")
    ax.set_ylabel(ylabel or "")
    ax.set_title(title)
    plt.xticks(rotation=45, ha="right")
    ax.legend(title=df_pivot.columns.name, bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    plt.tight_layout()
    return fig


def histogram(series, bins=30, title="", xlabel="", ylabel="Count", figsize=None):
    """Histogram of a single series."""
    fig, ax = plt.subplots(figsize=figsize or (10, 5))
    ax.hist(series, bins=bins, color=PALETTE[0], edgecolor="white", alpha=0.85)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.tight_layout()
    return fig


def scatter_plot(df, x, y, title, xlabel=None, ylabel=None, figsize=None):
    """Scatter plot."""
    fig, ax = plt.subplots(figsize=figsize or (10, 6))
    ax.scatter(df[x], df[y], alpha=0.5, color=PALETTE[0], edgecolors="white", s=50)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.set_title(title)
    plt.tight_layout()
    return fig


def heatmap(df_pivot, title, xlabel=None, ylabel=None, fmt=".0f", figsize=None):
    """Simple heatmap from a pivoted DataFrame."""
    fig, ax = plt.subplots(figsize=figsize or (12, 6))
    im = ax.imshow(df_pivot.values, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(df_pivot.columns)))
    ax.set_xticklabels(df_pivot.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(df_pivot.index)))
    ax.set_yticklabels(df_pivot.index)
    # Annotate cells
    for i in range(len(df_pivot.index)):
        for j in range(len(df_pivot.columns)):
            val = df_pivot.values[i, j]
            ax.text(j, i, f"{val:{fmt}}", ha="center", va="center",
                    color="white" if val > df_pivot.values.max() * 0.6 else "black",
                    fontsize=8)
    ax.set_xlabel(xlabel or "")
    ax.set_ylabel(ylabel or "")
    ax.set_title(title)
    fig.colorbar(im, ax=ax, shrink=0.8)
    plt.tight_layout()
    return fig


def multi_line_chart(df, x, y_cols, title, xlabel=None, ylabel=None, figsize=None):
    """Multiple lines on one chart."""
    fig, ax = plt.subplots(figsize=figsize or (12, 5))
    for i, col in enumerate(y_cols):
        ax.plot(df[x].astype(str), df[col], marker="o", label=col,
                color=PALETTE[i % len(PALETTE)], linewidth=2)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or "")
    ax.set_title(title)
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    plt.tight_layout()
    return fig
