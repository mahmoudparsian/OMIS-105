"""
world_plots.py
--------------
Reusable plotting functions for the World database Jupyter notebook.
All matplotlib/seaborn logic lives here, keeping the notebook clean.

Usage (from notebook):
    from world_plots import *
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import textwrap

# ── Global style ─────────────────────────────────────────────────────────────

PALETTE = [
    "#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974",
    "#64B5CD", "#E5AE38", "#6D904F", "#8B8B8B", "#D65F5F",
]

def _apply_style():
    """Set a clean, consistent plot style."""
    plt.rcParams.update({
        "figure.facecolor":  "white",
        "axes.facecolor":    "white",
        "axes.edgecolor":    "#333333",
        "axes.labelcolor":   "#333333",
        "xtick.color":       "#333333",
        "ytick.color":       "#333333",
        "font.size":         11,
        "axes.titlesize":    13,
        "axes.labelsize":    11,
        "figure.dpi":        110,
        "axes.grid":         True,
        "grid.alpha":        0.3,
        "grid.color":        "#cccccc",
    })

_apply_style()


# ── Helper utilities ─────────────────────────────────────────────────────────

def _wrap_labels(labels, width=14):
    """Wrap long tick-labels across multiple lines."""
    return [textwrap.fill(str(l), width) for l in labels]


def _fmt_millions(x, _):
    if x >= 1_000_000:
        return f"{x / 1_000_000:.1f}M"
    if x >= 1_000:
        return f"{x / 1_000:.0f}K"
    return f"{x:.0f}"


# ── Bar chart ────────────────────────────────────────────────────────────────

def plot_bar(df, x, y, title="", xlabel="", ylabel="",
             horizontal=False, color=None, figsize=(10, 5), top_n=None,
             fmt_y_millions=False, rotate_labels=0):
    """General-purpose bar chart from a DataFrame."""
    data = df.head(top_n) if top_n else df
    fig, ax = plt.subplots(figsize=figsize)
    c = color or PALETTE[0]

    if horizontal:
        ax.barh(data[x].astype(str), data[y], color=c, edgecolor="white")
        ax.set_xlabel(ylabel or y)
        ax.set_ylabel(xlabel or x)
        ax.invert_yaxis()
        if fmt_y_millions:
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_millions))
    else:
        bars = ax.bar(data[x].astype(str), data[y], color=c, edgecolor="white")
        ax.set_xlabel(xlabel or x)
        ax.set_ylabel(ylabel or y)
        if fmt_y_millions:
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_millions))
        if rotate_labels:
            plt.xticks(rotation=rotate_labels, ha="right")

    ax.set_title(title, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.show()


# ── Horizontal grouped / stacked bar ────────────────────────────────────────

def plot_grouped_bar(df, category, values, labels=None,
                     title="", xlabel="", figsize=(10, 6)):
    """Side-by-side bars for comparing two or more metrics."""
    import numpy as np
    cats = df[category].astype(str)
    n = len(values)
    x = np.arange(len(cats))
    width = 0.8 / n

    fig, ax = plt.subplots(figsize=figsize)
    for i, v in enumerate(values):
        lbl = labels[i] if labels else v
        ax.bar(x + i * width, df[v], width, label=lbl, color=PALETTE[i % len(PALETTE)])

    ax.set_xticks(x + width * (n - 1) / 2)
    ax.set_xticklabels(_wrap_labels(cats), fontsize=9)
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontweight="bold", pad=12)
    ax.legend()
    plt.tight_layout()
    plt.show()


# ── Pie / donut chart ───────────────────────────────────────────────────────

def plot_pie(df, labels_col, values_col, title="", figsize=(7, 7), top_n=8):
    """Pie chart; groups everything past top_n into 'Other'."""
    data = df.sort_values(values_col, ascending=False)
    if len(data) > top_n:
        top   = data.head(top_n)
        other = pd.DataFrame({
            labels_col: ["Other"],
            values_col: [data.iloc[top_n:][values_col].sum()],
        })
        data = pd.concat([top, other], ignore_index=True)

    fig, ax = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax.pie(
        data[values_col], labels=data[labels_col],
        autopct="%1.1f%%", colors=PALETTE, startangle=140,
        pctdistance=0.8, textprops={"fontsize": 10},
    )
    ax.set_title(title, fontweight="bold", pad=16)
    plt.tight_layout()
    plt.show()


# ── Scatter plot ─────────────────────────────────────────────────────────────

def plot_scatter(df, x, y, title="", xlabel="", ylabel="",
                 hue=None, size=None, figsize=(10, 6),
                 fmt_x_millions=False, fmt_y_millions=False,
                 annotate_col=None, annotate_top_n=5):
    """Scatter with optional colour grouping and annotations."""
    fig, ax = plt.subplots(figsize=figsize)

    if hue and hue in df.columns:
        groups = df[hue].unique()
        for i, g in enumerate(groups):
            sub = df[df[hue] == g]
            ax.scatter(sub[x], sub[y], label=g,
                       color=PALETTE[i % len(PALETTE)], alpha=0.7, s=50)
        ax.legend(fontsize=9, loc="best")
    else:
        ax.scatter(df[x], df[y], color=PALETTE[0], alpha=0.7, s=50)

    if annotate_col and annotate_col in df.columns:
        top = df.nlargest(annotate_top_n, y)
        for _, row in top.iterrows():
            ax.annotate(row[annotate_col], (row[x], row[y]),
                        fontsize=8, alpha=0.8,
                        xytext=(5, 5), textcoords="offset points")

    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.set_title(title, fontweight="bold", pad=12)
    if fmt_x_millions:
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_millions))
    if fmt_y_millions:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_millions))
    plt.tight_layout()
    plt.show()


# ── Line chart ───────────────────────────────────────────────────────────────

def plot_line(df, x, y, title="", xlabel="", ylabel="",
              figsize=(10, 5), marker="o"):
    """Simple line chart."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df[x], df[y], marker=marker, color=PALETTE[0], linewidth=2)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.set_title(title, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.show()


# ── Heatmap-style table ─────────────────────────────────────────────────────

def plot_heatmap(df, index_col, columns, values, title="", figsize=(10, 6)):
    """Pivot + colour-coded heatmap."""
    import numpy as np
    pivot = df.pivot_table(index=index_col, columns=columns, values=values,
                           aggfunc="sum", fill_value=0)
    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(pivot.values, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(_wrap_labels(pivot.columns, 12), fontsize=9)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)
    plt.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title(title, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.show()


# ── Stacked bar ──────────────────────────────────────────────────────────────

def plot_stacked_bar(df, x, y_cols, labels=None, title="",
                     xlabel="", ylabel="", figsize=(10, 6)):
    """Stacked bar chart from multiple value columns."""
    fig, ax = plt.subplots(figsize=figsize)
    bottom = None
    for i, col in enumerate(y_cols):
        lbl = labels[i] if labels else col
        ax.bar(df[x].astype(str), df[col], label=lbl,
               bottom=bottom, color=PALETTE[i % len(PALETTE)])
        bottom = df[col] if bottom is None else bottom + df[col]
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight="bold", pad=12)
    ax.legend(fontsize=9)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# ── Box plot ─────────────────────────────────────────────────────────────────

def plot_box(df, x, y, title="", xlabel="", ylabel="", figsize=(10, 5)):
    """Box-and-whisker by category."""
    groups = df[x].unique()
    data = [df[df[x] == g][y].dropna().values for g in groups]

    fig, ax = plt.subplots(figsize=figsize)
    bp = ax.boxplot(data, patch_artist=True, labels=_wrap_labels(groups))
    for patch, color in zip(bp["boxes"], PALETTE):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.set_title(title, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.show()
