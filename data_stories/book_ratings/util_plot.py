"""
util_plot.py
------------
Reusable plotting helpers for the OMIS 105 "Book Ratings" data-story notebooks.

All plotting code lives here so the notebooks stay focused on SQL.
Every function takes a pandas DataFrame (typically the result of a DuckDB query)
and returns a matplotlib Figure so cells can display or save it.

Usage in a notebook:
    import util_plot as up
    df = con.execute("SELECT ...").df()
    up.bar(df, x="title", y="average_rating", title="...")
"""

from __future__ import annotations
import textwrap
import matplotlib.pyplot as plt

# A clean, consistent default style for every chart in the project.
plt.rcParams.update({
    "figure.figsize": (9, 5),
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 11,
})

_PALETTE = "#4C72B0"
_PALETTE2 = "#DD8452"


def _wrap(labels, width=22):
    """Wrap long category labels so they don't overlap."""
    return ["\n".join(textwrap.wrap(str(l), width)) for l in labels]


def bar(df, x, y, title="", xlabel=None, ylabel=None, color=_PALETTE,
        rotate=0, value_labels=False):
    """Vertical bar chart of df[y] against df[x]."""
    fig, ax = plt.subplots()
    ax.bar(df[x].astype(str), df[y], color=color)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel if xlabel is not None else x)
    ax.set_ylabel(ylabel if ylabel is not None else y)
    if rotate:
        plt.setp(ax.get_xticklabels(), rotation=rotate, ha="right")
    if value_labels:
        for i, v in enumerate(df[y]):
            ax.text(i, v, f"{v:,.2f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    return fig


def barh(df, x, y, title="", xlabel=None, ylabel=None, color=_PALETTE,
         value_fmt="{:,.0f}", wrap=38):
    """Horizontal bar chart - ideal for Top-N rankings.

    df[y] is the category (e.g. book title), df[x] is the measure.
    The largest value is drawn at the top.

    The figure height grows with the number of bars and the category labels
    are wrapped (but not too aggressively) so long titles never collide.
    """
    d = df.iloc[::-1]  # reverse so the biggest bar ends up on top
    labels = _wrap(d[y], width=wrap)

    # Height scales with bar count AND how many wrapped lines each label needs.
    n = len(d)
    extra_lines = sum(lbl.count("\n") for lbl in labels)
    height = max(3.0, 0.55 * n + 0.18 * extra_lines + 1.2)

    fig, ax = plt.subplots(figsize=(9, height))
    bars = ax.barh(range(n), d[x], color=color)
    ax.set_yticks(range(n))
    ax.set_yticklabels(labels, fontsize=9)
    ax.margins(x=0.12)  # leave room for value labels on the right
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel if xlabel is not None else x)
    ax.set_ylabel(ylabel if ylabel is not None else y)
    ax.bar_label(bars, labels=[value_fmt.format(v) for v in d[x]],
                 padding=3, fontsize=9)
    fig.tight_layout()
    return fig


def hist(series, bins=30, title="", xlabel="", ylabel="Count", color=_PALETTE):
    """Histogram of a numeric series (e.g. distribution of average ratings)."""
    fig, ax = plt.subplots()
    ax.hist(series.dropna(), bins=bins, color=color, edgecolor="white")
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig


def line(df, x, y, title="", xlabel=None, ylabel=None, color=_PALETTE,
         marker="o"):
    """Line chart - useful for trends over a continuous axis (e.g. by year)."""
    fig, ax = plt.subplots()
    ax.plot(df[x], df[y], marker=marker, color=color)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel if xlabel is not None else x)
    ax.set_ylabel(ylabel if ylabel is not None else y)
    fig.tight_layout()
    return fig


def scatter(df, x, y, title="", xlabel=None, ylabel=None, color=_PALETTE,
            alpha=0.5, logx=False):
    """Scatter plot - useful for relationships (e.g. ratings_count vs rating)."""
    fig, ax = plt.subplots()
    ax.scatter(df[x], df[y], color=color, alpha=alpha, s=18)
    if logx:
        ax.set_xscale("log")
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel if xlabel is not None else x)
    ax.set_ylabel(ylabel if ylabel is not None else y)
    fig.tight_layout()
    return fig


def grouped_bar(df, x, y, title="", xlabel=None, ylabel=None, rotate=0):
    """Two-series comparison: df must have columns [x, y] already aggregated.

    Thin wrapper kept for readability in the notebooks; identical to bar()
    but uses the secondary palette colour.
    """
    return bar(df, x, y, title=title, xlabel=xlabel, ylabel=ylabel,
               color=_PALETTE2, rotate=rotate)
