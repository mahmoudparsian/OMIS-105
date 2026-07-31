"""
util_plot.py  –  Reusable plotting helpers for the Insurance SQL notebooks.
All plotting code lives here so the notebooks stay clean and focused on SQL.

Usage (inside a notebook):
    from util_plot import *
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import textwrap

# ── Global style ────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)
PALETTE = sns.color_palette("muted")
FIG_SMALL  = (8, 4)
FIG_MEDIUM = (10, 5)
FIG_WIDE   = (12, 5)
FIG_TALL   = (8, 6)

def _currency_fmt(ax, axis="y"):
    """Apply $-comma formatting to an axis."""
    fmt = ticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
    if axis in ("y", "both"):
        ax.yaxis.set_major_formatter(fmt)
    if axis in ("x", "both"):
        ax.xaxis.set_major_formatter(fmt)

def _finish(ax, title, xlabel=None, ylabel=None, rotate_x=0, tight=True):
    """Common finishing touches."""
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if rotate_x: plt.xticks(rotation=rotate_x, ha="right")
    if tight: plt.tight_layout()
    plt.show()


# ═══════════════════════════════════════════════════════════════════════════
#  BAR CHARTS
# ═══════════════════════════════════════════════════════════════════════════

def plot_bar(df, x, y, title, xlabel=None, ylabel=None,
             color=None, figsize=FIG_SMALL, horizontal=False,
             currency=False, rotate_x=0, annotate=True, fmt=None):
    """Vertical or horizontal bar chart from a DataFrame."""
    fig, ax = plt.subplots(figsize=figsize)
    c = color or PALETTE[0]
    if horizontal:
        bars = ax.barh(df[x].astype(str), df[y], color=c, edgecolor="white")
        if currency: _currency_fmt(ax, "x")
        if annotate:
            for bar in bars:
                w = bar.get_width()
                label = fmt.format(w) if fmt else (f"${w:,.0f}" if currency else f"{w:,.1f}")
                ax.text(w, bar.get_y() + bar.get_height()/2, f" {label}",
                        va="center", fontsize=9)
    else:
        bars = ax.bar(df[x].astype(str), df[y], color=c, edgecolor="white")
        if currency: _currency_fmt(ax, "y")
        if annotate:
            for bar in bars:
                h = bar.get_height()
                label = fmt.format(h) if fmt else (f"${h:,.0f}" if currency else f"{h:,.1f}")
                ax.text(bar.get_x() + bar.get_width()/2, h, label,
                        ha="center", va="bottom", fontsize=9)
    _finish(ax, title, xlabel, ylabel, rotate_x)


def plot_grouped_bar(df, x, group_col, y, title,
                     xlabel=None, ylabel=None, figsize=FIG_MEDIUM,
                     currency=False, rotate_x=0):
    """Grouped bar chart – one cluster per x-value, coloured by group_col."""
    fig, ax = plt.subplots(figsize=figsize)
    pivot = df.pivot(index=x, columns=group_col, values=y)
    pivot.plot(kind="bar", ax=ax, edgecolor="white", width=0.75)
    if currency: _currency_fmt(ax)
    ax.legend(title=group_col, frameon=True)
    _finish(ax, title, xlabel, ylabel, rotate_x)


# ═══════════════════════════════════════════════════════════════════════════
#  LINE / SCATTER
# ═══════════════════════════════════════════════════════════════════════════

def plot_line(df, x, y, title, xlabel=None, ylabel=None,
              figsize=FIG_MEDIUM, currency=False, marker="o"):
    """Simple line chart."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df[x], df[y], marker=marker, color=PALETTE[0], linewidth=2)
    if currency: _currency_fmt(ax)
    _finish(ax, title, xlabel, ylabel)


def plot_scatter(df, x, y, title, hue=None, xlabel=None, ylabel=None,
                 figsize=FIG_MEDIUM, currency_x=False, currency_y=False,
                 alpha=0.6):
    """Scatter plot, optionally coloured by hue column."""
    fig, ax = plt.subplots(figsize=figsize)
    if hue:
        for i, (name, grp) in enumerate(df.groupby(hue)):
            ax.scatter(grp[x], grp[y], label=name, alpha=alpha,
                       s=40, color=PALETTE[i % len(PALETTE)])
        ax.legend(title=hue, frameon=True)
    else:
        ax.scatter(df[x], df[y], alpha=alpha, s=40, color=PALETTE[0])
    if currency_x: _currency_fmt(ax, "x")
    if currency_y: _currency_fmt(ax, "y")
    _finish(ax, title, xlabel, ylabel)


# ═══════════════════════════════════════════════════════════════════════════
#  DISTRIBUTION PLOTS
# ═══════════════════════════════════════════════════════════════════════════

def plot_histogram(df, col, title, xlabel=None, bins=30,
                   figsize=FIG_SMALL, currency=False, kde=True):
    """Histogram with optional KDE overlay."""
    fig, ax = plt.subplots(figsize=figsize)
    sns.histplot(df[col], bins=bins, kde=kde, ax=ax, color=PALETTE[0],
                 edgecolor="white")
    if currency: _currency_fmt(ax, "x")
    _finish(ax, title, xlabel, ylabel="Count")


def plot_boxplot(df, x, y, title, xlabel=None, ylabel=None,
                 figsize=FIG_MEDIUM, currency=False, order=None):
    """Box plot – distribution of y grouped by x."""
    fig, ax = plt.subplots(figsize=figsize)
    sns.boxplot(data=df, x=x, y=y, ax=ax, palette="muted", order=order)
    if currency: _currency_fmt(ax)
    _finish(ax, title, xlabel, ylabel)


# ═══════════════════════════════════════════════════════════════════════════
#  PIE / DONUT
# ═══════════════════════════════════════════════════════════════════════════

def plot_pie(df, labels_col, values_col, title, figsize=(6, 6),
             startangle=140, donut=False):
    """Pie or donut chart."""
    fig, ax = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax.pie(
        df[values_col], labels=df[labels_col], autopct="%1.1f%%",
        startangle=startangle, colors=PALETTE[:len(df)],
        textprops={"fontsize": 10})
    if donut:
        centre = plt.Circle((0, 0), 0.55, fc="white")
        ax.add_artist(centre)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=14)
    plt.tight_layout()
    plt.show()


# ═══════════════════════════════════════════════════════════════════════════
#  HEATMAP
# ═══════════════════════════════════════════════════════════════════════════

def plot_heatmap(df, title, figsize=FIG_MEDIUM, annot=True, fmt=".2f",
                 cmap="YlOrRd"):
    """Heatmap from a pivot-style DataFrame."""
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(df, annot=annot, fmt=fmt, cmap=cmap, ax=ax,
                linewidths=0.5, linecolor="white")
    _finish(ax, title)


# ═══════════════════════════════════════════════════════════════════════════
#  STACKED BAR
# ═══════════════════════════════════════════════════════════════════════════

def plot_stacked_bar(df, x, columns, title, xlabel=None, ylabel=None,
                     figsize=FIG_MEDIUM, currency=False, rotate_x=0):
    """Stacked bar chart. `columns` is a list of y-column names to stack."""
    fig, ax = plt.subplots(figsize=figsize)
    df.set_index(x)[columns].plot(kind="bar", stacked=True, ax=ax,
                                   edgecolor="white", width=0.75)
    if currency: _currency_fmt(ax)
    ax.legend(frameon=True)
    _finish(ax, title, xlabel, ylabel, rotate_x)


# ═══════════════════════════════════════════════════════════════════════════
#  RANKING / LOLLIPOP
# ═══════════════════════════════════════════════════════════════════════════

def plot_lollipop(df, x, y, title, xlabel=None, ylabel=None,
                  figsize=FIG_MEDIUM, currency=False, color=None):
    """Horizontal lollipop chart – great for rankings."""
    fig, ax = plt.subplots(figsize=figsize)
    c = color or PALETTE[0]
    ax.hlines(y=df[x].astype(str), xmin=0, xmax=df[y],
              color=c, alpha=0.6, linewidth=2)
    ax.plot(df[y], df[x].astype(str), "o", color=c, markersize=8)
    if currency: _currency_fmt(ax, "x")
    _finish(ax, title, xlabel, ylabel)


# ═══════════════════════════════════════════════════════════════════════════
#  MULTI-SERIES LINE
# ═══════════════════════════════════════════════════════════════════════════

def plot_multi_line(df, x, y_cols, title, xlabel=None, ylabel=None,
                    figsize=FIG_MEDIUM, currency=False, marker="o"):
    """Multiple lines on one axis. y_cols is a list of column names."""
    fig, ax = plt.subplots(figsize=figsize)
    for i, col in enumerate(y_cols):
        ax.plot(df[x], df[col], marker=marker, label=col,
                color=PALETTE[i % len(PALETTE)], linewidth=2)
    ax.legend(frameon=True)
    if currency: _currency_fmt(ax)
    _finish(ax, title, xlabel, ylabel)


# ═══════════════════════════════════════════════════════════════════════════
#  DUPLICATE-HIGHLIGHT TABLE (for Notebook 1)
# ═══════════════════════════════════════════════════════════════════════════

def highlight_duplicates(df):
    """Return a styled DataFrame that highlights duplicate rows in red."""
    return df.style.set_properties(**{
        "background-color": "#ffe0e0",
        "border": "1px solid #ccc"
    }).set_caption("Duplicate Rows (highlighted)")
