"""
util_plot.py
=============
Decoupled plotting helpers for the `top_500_movies.py` Marimo notebook.

Why a separate module?
----------------------
The notebook keeps each analytical cell focused on ONE idea: a paragraph of
explanation, a *pure SQL* query, and a chart. Stuffing dozens of lines of
matplotlib styling into every cell would bury the SQL. So all the drawing code
lives here instead. Every function:

  * accepts a DataFrame (pandas **or** polars - both are handled),
  * returns a `matplotlib.figure.Figure`, which Marimo renders automatically
    when it is the last expression of a cell,
  * shares one consistent visual theme (see `_PALETTE` / `_style_axis`).

Usage inside a notebook cell:

    import util_plot as up
    up.barh_top(df, label="title", value="customScore", title="Top movies")

Nothing here imports Marimo, so the module can also be unit-tested or reused
from a plain script.
"""

from __future__ import annotations

import matplotlib

# Use a non-interactive backend so the module works headless (CI, scripts,
# notebooks) without trying to open a GUI window.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# --------------------------------------------------------------------------- #
# Shared theme
# --------------------------------------------------------------------------- #
_PALETTE = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
    "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD",
]
_INK = "#2b2b2b"
_GRID = "#d9d9d9"


def _as_pandas(df):
    """Accept pandas or polars; always return a pandas DataFrame."""
    if hasattr(df, "to_pandas"):          # polars.DataFrame
        return df.to_pandas()
    return df


def _new_fig(width=8.5, height=4.8):
    fig, ax = plt.subplots(figsize=(width, height), dpi=120)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    return fig, ax


def _style_axis(ax, title=None, xlabel=None, ylabel=None):
    """Apply the shared minimalist theme to an Axes."""
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=_INK, pad=12)
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=10.5, color=_INK)
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=10.5, color=_INK)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(_GRID)
    ax.tick_params(colors=_INK, labelsize=9.5)
    ax.grid(axis="y", color=_GRID, linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)
    return ax


def _bar_labels(ax, bars, fmt="{:.0f}", horizontal=False, pad=3):
    """Annotate each bar with its value."""
    for b in bars:
        if horizontal:
            val = b.get_width()
            ax.annotate(fmt.format(val),
                        (val, b.get_y() + b.get_height() / 2),
                        xytext=(pad, 0), textcoords="offset points",
                        va="center", ha="left", fontsize=8.5, color=_INK)
        else:
            val = b.get_height()
            ax.annotate(fmt.format(val),
                        (b.get_x() + b.get_width() / 2, val),
                        xytext=(0, pad), textcoords="offset points",
                        va="bottom", ha="center", fontsize=8.5, color=_INK)


# --------------------------------------------------------------------------- #
# Public chart builders
# --------------------------------------------------------------------------- #
def barh_top(df, label, value, title=None, xlabel=None, color=None,
             value_fmt="{:.1f}", max_label_len=34):
    """Horizontal bar chart, largest value on top (great for Top-N rankings)."""
    d = _as_pandas(df).copy()
    d = d[[label, value]].dropna()
    d[label] = d[label].astype(str).str.slice(0, max_label_len)
    d = d.iloc[::-1]                       # so the biggest ends up on top
    fig, ax = _new_fig(height=max(3.2, 0.45 * len(d) + 1.2))
    bars = ax.barh(d[label], d[value], color=color or _PALETTE[0],
                   edgecolor="white", height=0.72)
    _bar_labels(ax, bars, fmt=value_fmt, horizontal=True)
    _style_axis(ax, title=title, xlabel=xlabel if xlabel is not None else value,
                ylabel="")
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=_GRID, linewidth=0.8, alpha=0.7)
    ax.margins(x=0.12)
    fig.tight_layout()
    return fig


def bar(df, x, y, title=None, xlabel=None, ylabel=None, color=None,
        rotate=0, value_fmt="{:.0f}", annotate=True):
    """Vertical bar chart for categorical counts / aggregates."""
    d = _as_pandas(df).copy()
    fig, ax = _new_fig()
    bars = ax.bar(d[x].astype(str), d[y], color=color or _PALETTE[0],
                  edgecolor="white", width=0.72)
    if annotate:
        _bar_labels(ax, bars, fmt=value_fmt)
    _style_axis(ax, title=title,
                xlabel=xlabel if xlabel is not None else x,
                ylabel=ylabel if ylabel is not None else y)
    if rotate:
        plt.setp(ax.get_xticklabels(), rotation=rotate, ha="right")
    ax.margins(y=0.15)
    fig.tight_layout()
    return fig


def line(df, x, ys, title=None, xlabel=None, ylabel=None, labels=None,
         markers=True):
    """Single- or multi-series line chart. `ys` is a column name or list."""
    d = _as_pandas(df).copy()
    if isinstance(ys, str):
        ys = [ys]
    labels = labels or ys
    fig, ax = _new_fig()
    for i, col in enumerate(ys):
        ax.plot(d[x], d[col], color=_PALETTE[i % len(_PALETTE)],
                linewidth=2.2, marker="o" if markers else None,
                markersize=5, label=labels[i])
    _style_axis(ax, title=title,
                xlabel=xlabel if xlabel is not None else x,
                ylabel=ylabel or "")
    if len(ys) > 1:
        ax.legend(frameon=False, fontsize=9.5)
    fig.tight_layout()
    return fig


def grouped_bar(df, x, ys, title=None, xlabel=None, ylabel=None, labels=None,
                value_fmt="{:.0f}", annotate=False):
    """Side-by-side bars for comparing several measures across categories."""
    import numpy as np
    d = _as_pandas(df).copy()
    if isinstance(ys, str):
        ys = [ys]
    labels = labels or ys
    cats = d[x].astype(str).tolist()
    idx = np.arange(len(cats))
    n = len(ys)
    width = 0.8 / n
    fig, ax = _new_fig()
    for i, col in enumerate(ys):
        bars = ax.bar(idx + i * width - 0.4 + width / 2, d[col], width,
                      color=_PALETTE[i % len(_PALETTE)], edgecolor="white",
                      label=labels[i])
        if annotate:
            _bar_labels(ax, bars, fmt=value_fmt)
    ax.set_xticks(idx)
    ax.set_xticklabels(cats)
    _style_axis(ax, title=title,
                xlabel=xlabel if xlabel is not None else x,
                ylabel=ylabel or "")
    ax.legend(frameon=False, fontsize=9.5)
    ax.margins(y=0.15)
    fig.tight_layout()
    return fig


def scatter(df, x, y, title=None, xlabel=None, ylabel=None, color=None,
            size=42, annotate_col=None, max_labels=8):
    """Scatter plot, optionally labelling the most extreme points."""
    d = _as_pandas(df).copy()
    fig, ax = _new_fig()
    ax.scatter(d[x], d[y], s=size, color=color or _PALETTE[0],
               edgecolor="white", alpha=0.85, linewidth=0.6, zorder=3)
    if annotate_col and annotate_col in d.columns:
        top = d.nlargest(max_labels, y)
        for _, row in top.iterrows():
            ax.annotate(str(row[annotate_col])[:24], (row[x], row[y]),
                        xytext=(4, 4), textcoords="offset points",
                        fontsize=8, color=_INK)
    _style_axis(ax, title=title,
                xlabel=xlabel if xlabel is not None else x,
                ylabel=ylabel if ylabel is not None else y)
    ax.grid(axis="both", color=_GRID, linewidth=0.8, alpha=0.6)
    fig.tight_layout()
    return fig


def stacked_bar(df, x, ys, title=None, xlabel=None, ylabel=None, labels=None):
    """Stacked bars - useful for part-to-whole across categories."""
    import numpy as np
    d = _as_pandas(df).copy()
    if isinstance(ys, str):
        ys = [ys]
    labels = labels or ys
    cats = d[x].astype(str).tolist()
    fig, ax = _new_fig()
    bottom = np.zeros(len(cats))
    for i, col in enumerate(ys):
        ax.bar(cats, d[col], bottom=bottom,
               color=_PALETTE[i % len(_PALETTE)], edgecolor="white",
               label=labels[i])
        bottom += d[col].to_numpy()
    _style_axis(ax, title=title,
                xlabel=xlabel if xlabel is not None else x,
                ylabel=ylabel or "")
    ax.legend(frameon=False, fontsize=9.5)
    fig.tight_layout()
    return fig
