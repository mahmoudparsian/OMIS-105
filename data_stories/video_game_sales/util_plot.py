"""
util_plot.py
============
Decoupled plotting helpers for the Video Game Sales data-story notebooks.

Why a separate file?
--------------------
Keeping plotting code out of the notebooks means each notebook cell can stay
focused on *one* idea: the SQL query and its result. The figures are produced
by calling a single, well-named helper here. This keeps the teaching notebooks
clean, makes the charts reusable, and lets us restyle every plot in one place.

Every helper:
  * accepts a pandas DataFrame (typically the result of a DuckDB query),
  * returns the matplotlib Axes (so the caller can tweak further if needed),
  * uses a consistent, readable style.

Usage
-----
    import util_plot as up
    df = con.sql("SELECT ...").df()
    up.bar(df, x="platform", y="total_sales", title="Sales by platform")
"""

from __future__ import annotations

import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Shared style
# ---------------------------------------------------------------------------
PALETTE = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
    "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD",
]


def _new_ax(figsize=(9, 5)):
    """Create a figure/axes with the house style applied."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    return ax


def _finish(ax, title=None, xlabel=None, ylabel=None, rotate=0):
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=11)
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=11)
    if rotate:
        for label in ax.get_xticklabels():
            label.set_rotation(rotate)
            label.set_ha("right")
    plt.tight_layout()
    return ax


# ---------------------------------------------------------------------------
# Chart helpers
# ---------------------------------------------------------------------------
def bar(df, x, y, title=None, xlabel=None, ylabel=None, color=None, rotate=30,
        horizontal=False):
    """Vertical (or horizontal) bar chart from two DataFrame columns."""
    ax = _new_ax()
    color = color or PALETTE[0]
    if horizontal:
        ax.barh(df[x].astype(str), df[y], color=color)
        ax.invert_yaxis()  # largest on top
        return _finish(ax, title, ylabel if ylabel is not None else y,
                       xlabel if xlabel is not None else x)
    ax.bar(df[x].astype(str), df[y], color=color)
    return _finish(ax, title,
                   xlabel if xlabel is not None else x,
                   ylabel if ylabel is not None else y, rotate=rotate)


def grouped_bar(df, x, y_cols, title=None, xlabel=None, ylabel=None, rotate=30):
    """Grouped bar chart: one cluster of bars per row in ``df``."""
    import numpy as np
    ax = _new_ax(figsize=(10, 5.5))
    cats = df[x].astype(str).tolist()
    idx = np.arange(len(cats))
    n = len(y_cols)
    width = 0.8 / n
    for i, col in enumerate(y_cols):
        ax.bar(idx + i * width, df[col], width=width,
               label=col, color=PALETTE[i % len(PALETTE)])
    ax.set_xticks(idx + width * (n - 1) / 2)
    ax.set_xticklabels(cats)
    ax.legend(frameon=False)
    return _finish(ax, title,
                   xlabel if xlabel is not None else x,
                   ylabel if ylabel is not None else "value", rotate=rotate)


def line(df, x, y, title=None, xlabel=None, ylabel=None, marker="o", color=None):
    """Line chart, e.g. a metric over time."""
    ax = _new_ax()
    ax.plot(df[x], df[y], marker=marker, color=color or PALETTE[0])
    return _finish(ax, title,
                   xlabel if xlabel is not None else x,
                   ylabel if ylabel is not None else y)


def hist(series, bins=30, title=None, xlabel=None, ylabel="count", color=None):
    """Histogram of a single numeric series."""
    ax = _new_ax()
    ax.hist(series.dropna(), bins=bins, color=color or PALETTE[2],
            edgecolor="white")
    return _finish(ax, title, xlabel, ylabel)


def area(df, x, y, title=None, xlabel=None, ylabel=None, color=None):
    """Filled area chart, e.g. a cumulative running total over an ordering."""
    ax = _new_ax()
    ax.plot(df[x], df[y], color=color or PALETTE[3])
    ax.fill_between(df[x], df[y], color=color or PALETTE[3], alpha=0.25)
    return _finish(ax, title,
                   xlabel if xlabel is not None else x,
                   ylabel if ylabel is not None else y)


def pie(df, labels, values, title=None):
    """Pie chart for a small number of categories (e.g. regional split)."""
    ax = _new_ax(figsize=(6.5, 6.5))
    ax.pie(df[values], labels=df[labels].astype(str), autopct="%1.1f%%",
           colors=PALETTE, startangle=90, counterclock=False,
           wedgeprops=dict(edgecolor="white"))
    ax.axis("equal")
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    return ax
