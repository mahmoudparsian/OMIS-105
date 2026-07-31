# -*- coding: utf-8 -*-
"""
plot_util.py
------------
All plotting code for the movies-database Marimo notebooks lives here, kept
deliberately decoupled from the notebooks so the notebook cells stay focused
on PURE SQL.

Every function accepts the dataframe returned by `mo.sql(...)` - which is a
Polars DataFrame when `polars` is installed, otherwise a Pandas DataFrame -
and returns a Matplotlib `Figure`.  Marimo renders a returned Figure inline,
so a notebook plot cell is simply:

    import plot_util
    plot_util.barh(my_result, cat="title", val="revenue", title="...")

Column access uses `df[col].to_list()`, which works identically for Polars and
Pandas Series, so no DataFrame library is hard-required here.
"""
from __future__ import annotations

import warnings

import matplotlib

matplotlib.use("Agg")  # headless backend; marimo still renders the Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Many movie titles are non-Latin (e.g. 七人の侍, 올드보이).  Prefer a font that
# can render CJK glyphs when one is available on the system (common on macOS),
# and silence the harmless "glyph missing from font" warnings otherwise.
plt.rcParams["font.sans-serif"] = [
    "Arial Unicode MS", "Hiragino Sans", "PingFang SC", "Heiti TC",
    "Noto Sans CJK SC", "Noto Sans CJK JP", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
warnings.filterwarnings("ignore", message="Glyph .* missing from font")

# ----------------------------------------------------------------------------
# House style
# ----------------------------------------------------------------------------
_ACCENT = "#4C72B0"
_ACCENT2 = "#DD8452"
_GRID = "#DDDDDD"


def _apply_style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="both", color=_GRID, linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)


def _col(df, name):
    """Return a plain Python list for a column of a Polars or Pandas frame."""
    series = df[name]
    if hasattr(series, "to_list"):      # Polars Series and Pandas Series both have this
        return series.to_list()
    return list(series)


def _floats(values):
    out = []
    for v in values:
        try:
            out.append(float(v))
        except (TypeError, ValueError):
            out.append(float("nan"))
    return out


def _human(num):
    """Compact human-readable number: 1_200_000 -> '1.2M'."""
    try:
        n = float(num)
    except (TypeError, ValueError):
        return str(num)
    for unit, div in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(n) >= div:
            return f"{n / div:.1f}{unit}"
    return f"{n:.0f}"


def _maybe_money_formatter(ax, axis, values):
    """Use compact K/M/B tick labels when the magnitudes are large."""
    big = any(abs(v) >= 1000 for v in values if v == v)  # skip NaN
    if big:
        fmt = FuncFormatter(lambda x, _pos: _human(x))
        (ax.xaxis if axis == "x" else ax.yaxis).set_major_formatter(fmt)


# ----------------------------------------------------------------------------
# Public chart helpers
# ----------------------------------------------------------------------------
def barh(df, cat, val, title="", xlabel="", ylabel="", color=_ACCENT, **_):
    """Horizontal bar chart - ideal for long category labels (movie titles)."""
    cats = [str(c) for c in _col(df, cat)]
    vals = _floats(_col(df, val))
    # show the largest at the top
    pairs = list(zip(cats, vals))[::-1]
    cats = [p[0] for p in pairs]
    vals = [p[1] for p in pairs]

    height = max(2.5, 0.45 * len(cats) + 1.2)
    fig, ax = plt.subplots(figsize=(9, height))
    bars = ax.barh(cats, vals, color=color)
    _apply_style(ax)
    _maybe_money_formatter(ax, "x", vals)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel or val)
    if ylabel:
        ax.set_ylabel(ylabel)
    # value labels at the end of each bar
    for b, v in zip(bars, vals):
        ax.annotate(_human(v), xy=(b.get_width(), b.get_y() + b.get_height() / 2),
                    xytext=(4, 0), textcoords="offset points",
                    va="center", ha="left", fontsize=8, color="#333333")
    fig.tight_layout()
    return fig


def bar(df, cat, val, title="", xlabel="", ylabel="", rotate=0, color=_ACCENT, **_):
    """Vertical bar chart - good for a modest number of categories."""
    cats = [str(c) for c in _col(df, cat)]
    vals = _floats(_col(df, val))

    width = max(6, 0.55 * len(cats) + 2)
    fig, ax = plt.subplots(figsize=(min(width, 14), 5))
    bars = ax.bar(cats, vals, color=color)
    _apply_style(ax)
    _maybe_money_formatter(ax, "y", vals)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel or val)
    if rotate:
        plt.setp(ax.get_xticklabels(), rotation=rotate, ha="right")
    for b, v in zip(bars, vals):
        ax.annotate(_human(v), xy=(b.get_x() + b.get_width() / 2, b.get_height()),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, color="#333333")
    fig.tight_layout()
    return fig


def line(df, x, y, title="", xlabel="", ylabel="", color=_ACCENT, **_):
    """Line chart - for time series and cumulative/over-time trends."""
    xs = _floats(_col(df, x))
    ys = _floats(_col(df, y))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(xs, ys, color=color, linewidth=2, marker="o", markersize=3)
    ax.fill_between(xs, ys, color=color, alpha=0.08)
    _apply_style(ax)
    _maybe_money_formatter(ax, "y", ys)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    fig.tight_layout()
    return fig


# Dispatch table used by the generated notebooks.
KIND = {"barh": barh, "bar": bar, "line": line}


def plot(df, spec):
    """Generic entry point: `spec` is the plot dict from query_specs."""
    kind = spec["kind"]
    kwargs = {k: v for k, v in spec.items() if k != "kind"}
    return KIND[kind](df, **kwargs)
