"""
plot_utils.py  –  Reusable plotting functions for Employee Data Exploration.

All functions accept a Pandas DataFrame (typically the result of a DuckDB
query) and produce a clean, presentation-ready Matplotlib figure.

Usage
-----
    from utils import plot_bar, plot_pie, plot_histogram
    plot_bar(df, x="department", y="avg_salary", title="Average Salary by Dept")
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# ── Global style defaults ──────────────────────────────────────────────────
_PALETTE = [
    "#2980B9", "#E74C3C", "#27AE60", "#F39C12", "#8E44AD",
    "#1ABC9C", "#D35400", "#2C3E50", "#C0392B", "#16A085",
    "#7F8C8D", "#2ECC71", "#3498DB", "#9B59B6", "#E67E22",
]
_FIG_BG   = "#FAFAFA"
_FONT     = "Helvetica Neue"

plt.rcParams.update({
    "font.family": _FONT,
    "axes.facecolor": _FIG_BG,
    "figure.facecolor": "#FFFFFF",
    "axes.edgecolor": "#CCCCCC",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.color": "#CCCCCC",
})


def _currency_fmt(x, _):
    """Format axis tick as $120K or $1.2M."""
    if abs(x) >= 1_000_000:
        return f"${x / 1_000_000:.1f}M"
    if abs(x) >= 1_000:
        return f"${x / 1_000:.0f}K"
    return f"${x:,.0f}"


def _number_fmt(x, _):
    """Format axis tick as plain number with commas."""
    return f"{x:,.0f}"


def _add_bar_labels(ax, bars, fmt=",.0f", fontsize=9):
    """Add value labels on top of bars."""
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:{fmt}}",
                ha="center", va="bottom",
                fontsize=fontsize, fontweight="bold",
            )


# ═══════════════════════════════════════════════════════════════════════════
# PUBLIC FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def plot_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    color: str | list | None = None,
    currency: bool = False,
    figsize: tuple = (10, 5),
    rotation: int = 0,
    bar_labels: bool = True,
):
    """Vertical bar chart."""
    fig, ax = plt.subplots(figsize=figsize)
    colors = color if color else _PALETTE[: len(df)]
    bars = ax.bar(df[x].astype(str), df[y], color=colors, edgecolor="white", linewidth=0.5)

    if bar_labels:
        fmt = ",.0f"
        _add_bar_labels(ax, bars, fmt=fmt)

    if currency:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_currency_fmt))
    else:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_number_fmt))

    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel or x, fontsize=11)
    ax.set_ylabel(ylabel or y, fontsize=11)
    ax.tick_params(axis="x", rotation=rotation)
    plt.tight_layout()
    plt.show()


def plot_horizontal_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    color: str | list | None = None,
    currency: bool = False,
    figsize: tuple = (10, 5),
):
    """Horizontal bar chart (good for long category labels)."""
    fig, ax = plt.subplots(figsize=figsize)
    colors = color if color else _PALETTE[: len(df)]
    bars = ax.barh(df[y].astype(str), df[x], color=colors, edgecolor="white", linewidth=0.5)

    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height() / 2.0,
                f" {width:,.0f}", ha="left", va="center", fontsize=9, fontweight="bold")

    if currency:
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(_currency_fmt))

    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel or x, fontsize=11)
    ax.set_ylabel(ylabel or y, fontsize=11)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.show()


def plot_pie(
    df: pd.DataFrame,
    labels: str,
    values: str,
    title: str = "",
    figsize: tuple = (8, 8),
    startangle: int = 140,
):
    """Pie / donut chart with percentage labels."""
    fig, ax = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax.pie(
        df[values],
        labels=df[labels],
        autopct="%1.1f%%",
        startangle=startangle,
        colors=_PALETTE[: len(df)],
        pctdistance=0.78,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_fontweight("bold")
    for t in texts:
        t.set_fontsize(11)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=16)
    plt.tight_layout()
    plt.show()


def plot_grouped_bar(
    df: pd.DataFrame,
    x: str,
    group: str,
    y: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    currency: bool = False,
    figsize: tuple = (12, 6),
):
    """Grouped (side-by-side) bar chart — *df* should be in long form."""
    groups = df[group].unique()
    categories = df[x].unique()
    n_groups = len(groups)
    bar_width = 0.8 / n_groups
    x_pos = np.arange(len(categories))

    fig, ax = plt.subplots(figsize=figsize)
    for i, grp in enumerate(groups):
        subset = df[df[group] == grp].set_index(x).reindex(categories)
        offset = (i - n_groups / 2 + 0.5) * bar_width
        ax.bar(x_pos + offset, subset[y], bar_width,
               label=grp, color=_PALETTE[i % len(_PALETTE)], edgecolor="white")

    ax.set_xticks(x_pos)
    ax.set_xticklabels(categories)
    if currency:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_currency_fmt))
    else:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_number_fmt))
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel or x, fontsize=11)
    ax.set_ylabel(ylabel or y, fontsize=11)
    ax.legend(title=group, frameon=True, fancybox=True, shadow=True)
    plt.tight_layout()
    plt.show()


def plot_histogram(
    df: pd.DataFrame,
    col: str,
    bins: int = 20,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "Frequency",
    currency: bool = False,
    figsize: tuple = (10, 5),
    color: str = "#2980B9",
):
    """Histogram of a numeric column."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.hist(df[col], bins=bins, color=color, edgecolor="white", linewidth=0.8)
    if currency:
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(_currency_fmt))
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel or col, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    plt.tight_layout()
    plt.show()


def plot_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    hue: str | None = None,
    figsize: tuple = (10, 6),
    alpha: float = 0.6,
):
    """Scatter plot, optionally coloured by a categorical column."""
    fig, ax = plt.subplots(figsize=figsize)
    if hue and hue in df.columns:
        for i, cat in enumerate(df[hue].unique()):
            mask = df[hue] == cat
            ax.scatter(df.loc[mask, x], df.loc[mask, y],
                       label=cat, color=_PALETTE[i % len(_PALETTE)],
                       alpha=alpha, s=40, edgecolors="white", linewidth=0.5)
        ax.legend(title=hue, frameon=True, fancybox=True, shadow=True)
    else:
        ax.scatter(df[x], df[y], color=_PALETTE[0], alpha=alpha,
                   s=40, edgecolors="white", linewidth=0.5)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel or x, fontsize=11)
    ax.set_ylabel(ylabel or y, fontsize=11)
    plt.tight_layout()
    plt.show()


def plot_box(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    figsize: tuple = (10, 6),
):
    """Box plot — shows distribution of *y* for each category in *x*."""
    categories = df[x].unique()
    data = [df[df[x] == cat][y].values for cat in categories]

    fig, ax = plt.subplots(figsize=figsize)
    bp = ax.boxplot(data, labels=categories, patch_artist=True, notch=True,
                    boxprops=dict(linewidth=1.2),
                    medianprops=dict(color="#E74C3C", linewidth=2))
    for i, box in enumerate(bp["boxes"]):
        box.set_facecolor(_PALETTE[i % len(_PALETTE)])
        box.set_alpha(0.7)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel or x, fontsize=11)
    ax.set_ylabel(ylabel or y, fontsize=11)
    plt.tight_layout()
    plt.show()


def plot_line(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    marker: str = "o",
    figsize: tuple = (10, 5),
    currency: bool = False,
):
    """Line chart with markers."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df[x].astype(str), df[y], marker=marker, color=_PALETTE[0],
            linewidth=2, markersize=7, markerfacecolor=_PALETTE[1])
    if currency:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_currency_fmt))
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel or x, fontsize=11)
    ax.set_ylabel(ylabel or y, fontsize=11)
    plt.tight_layout()
    plt.show()


def plot_stacked_bar(
    df_pivot: pd.DataFrame,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    currency: bool = False,
    figsize: tuple = (12, 6),
):
    """Stacked bar chart from a pivoted DataFrame (index = x-axis, columns = segments)."""
    fig, ax = plt.subplots(figsize=figsize)
    df_pivot.plot(kind="bar", stacked=True, ax=ax,
                  color=_PALETTE[: len(df_pivot.columns)], edgecolor="white", linewidth=0.5)
    if currency:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_currency_fmt))
    else:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_number_fmt))
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.legend(frameon=True, fancybox=True, shadow=True)
    plt.tight_layout()
    plt.show()


def plot_heatmap(
    df_pivot: pd.DataFrame,
    title: str = "",
    fmt: str = ",.0f",
    figsize: tuple = (10, 6),
    cmap: str = "YlOrRd",
):
    """Simple heatmap from a pivoted DataFrame."""
    fig, ax = plt.subplots(figsize=figsize)
    data = df_pivot.values.astype(float)
    im = ax.imshow(data, cmap=cmap, aspect="auto")

    ax.set_xticks(range(len(df_pivot.columns)))
    ax.set_xticklabels(df_pivot.columns, fontsize=10)
    ax.set_yticks(range(len(df_pivot.index)))
    ax.set_yticklabels(df_pivot.index, fontsize=10)

    # Annotate cells
    for i in range(len(df_pivot.index)):
        for j in range(len(df_pivot.columns)):
            val = data[i, j]
            color = "white" if val > data.mean() else "black"
            ax.text(j, i, f"{val:{fmt}}", ha="center", va="center",
                    fontsize=9, fontweight="bold", color=color)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    fig.colorbar(im, ax=ax, shrink=0.8)
    plt.tight_layout()
    plt.show()
