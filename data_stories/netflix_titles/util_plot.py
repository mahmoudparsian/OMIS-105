"""
util_plot.py — Fallback plotting utilities for Netflix notebooks.

These functions are called ONLY when `altair` is not installed.
Each function accepts a pandas DataFrame and produces a matplotlib figure.

Usage inside a Marimo cell:
    from util_plot import plot_bar_h
    plot_bar_h(df, x="count", y="country", title="Top Countries")
"""

import matplotlib
matplotlib.use("Agg")           # non-interactive backend; Marimo renders the figure
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

# ── Netflix brand colours ──────────────────────────────────────────────────────
RED   = "#e50914"
DARK  = "#221f1f"
MID   = "#b20710"
LIGHT = "#f5f5f1"


def _style_ax(ax, title: str) -> None:
    """Apply clean Netflix-inspired style to an axes object."""
    ax.set_title(title, fontsize=13, fontweight="bold", color=DARK, pad=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.spines["bottom"].set_color("#cccccc")
    ax.tick_params(colors=DARK, labelsize=9)
    ax.set_facecolor(LIGHT)
    ax.figure.patch.set_facecolor("white")


def plot_bar_simple(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = RED,
    figsize: tuple = (9, 4),
) -> plt.Figure:
    """Vertical bar chart."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(df[x].astype(str), df[y], color=color, edgecolor="white", linewidth=0.6)
    ax.set_xlabel(x, fontsize=10)
    ax.set_ylabel(y, fontsize=10)
    _style_ax(ax, title)
    plt.tight_layout()
    plt.show()
    return fig


def plot_bar_h(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = RED,
    figsize: tuple = (9, 6),
) -> plt.Figure:
    """Horizontal bar chart — ideal for long category labels."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(df[y].astype(str), df[x], color=color, edgecolor="white", linewidth=0.6)
    ax.invert_yaxis()            # largest bar at top
    ax.set_xlabel(x, fontsize=10)
    _style_ax(ax, title)
    plt.tight_layout()
    plt.show()
    return fig


def plot_line(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = RED,
    figsize: tuple = (9, 4),
) -> plt.Figure:
    """Simple line chart with filled area."""
    fig, ax = plt.subplots(figsize=figsize)
    xs = df[x].astype(str)
    ys = df[y]
    ax.plot(xs, ys, color=color, linewidth=2, marker="o", markersize=4)
    ax.fill_between(xs, ys, alpha=0.18, color=color)
    ax.set_xlabel(x, fontsize=10)
    ax.set_ylabel(y, fontsize=10)
    plt.xticks(rotation=45, ha="right")
    _style_ax(ax, title)
    plt.tight_layout()
    plt.show()
    return fig


def plot_line_dual(
    df: pd.DataFrame,
    x: str,
    y1: str,
    y2: str,
    title: str = "",
    figsize: tuple = (10, 4),
) -> plt.Figure:
    """Two lines on one axes — e.g. Movies vs TV Shows over time."""
    fig, ax = plt.subplots(figsize=figsize)
    xs = df[x].astype(str)
    ax.plot(xs, df[y1], color=RED,  linewidth=2, marker="o", markersize=4, label=y1)
    ax.plot(xs, df[y2], color=DARK, linewidth=2, marker="s", markersize=4, label=y2)
    ax.fill_between(xs, df[y1], alpha=0.12, color=RED)
    ax.fill_between(xs, df[y2], alpha=0.12, color=DARK)
    ax.legend(fontsize=9)
    ax.set_xlabel(x, fontsize=10)
    plt.xticks(rotation=45, ha="right")
    _style_ax(ax, title)
    plt.tight_layout()
    plt.show()
    return fig


def plot_area(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = RED,
    figsize: tuple = (9, 4),
) -> plt.Figure:
    """Filled area chart — good for cumulative / running totals."""
    fig, ax = plt.subplots(figsize=figsize)
    xs = df[x].astype(str)
    ys = df[y]
    ax.fill_between(xs, ys, color=color, alpha=0.75)
    ax.plot(xs, ys, color=MID, linewidth=1.5)
    ax.set_xlabel(x, fontsize=10)
    ax.set_ylabel(y, fontsize=10)
    plt.xticks(rotation=45, ha="right")
    _style_ax(ax, title)
    plt.tight_layout()
    plt.show()
    return fig


def plot_pie(
    df: pd.DataFrame,
    label: str,
    value: str,
    title: str = "",
    figsize: tuple = (6, 6),
) -> plt.Figure:
    """Donut / pie chart for part-of-whole comparisons."""
    palette = [RED, MID, DARK, "#555555", "#888888"]
    fig, ax = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax.pie(
        df[value],
        labels=df[label],
        autopct="%1.1f%%",
        colors=palette[: len(df)],
        startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        pctdistance=0.82,
    )
    # Draw a white circle in the centre to make it a donut
    centre_circle = plt.Circle((0, 0), 0.60, color="white")
    fig.gca().add_artist(centre_circle)
    for t in autotexts:
        t.set_fontsize(9)
    ax.set_title(title, fontsize=13, fontweight="bold", color=DARK, pad=12)
    plt.tight_layout()
    plt.show()
    return fig
