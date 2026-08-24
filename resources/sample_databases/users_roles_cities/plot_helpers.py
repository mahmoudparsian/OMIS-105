"""
plot_helpers.py
================
Simple plotting functions for the OMIS 105 Users/Roles/Cities DuckDB
notebook.

Students: You do NOT need to read or modify this file.
          It is imported by the notebook to keep plotting code
          out of your way so you can focus on SQL. (This is why
          the assignment calls for "plotting code outside of Marimo".)

Functions
---------
  plot_bar(df, x, y, title)            -- vertical bar chart
  plot_hbar(df, x, y, title)           -- horizontal bar chart
  plot_pie(df, labels, values, title)  -- pie / donut chart
"""

import matplotlib.pyplot as plt

# -- Colour palette ---------------------------------------------
COLORS = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#E58606",
          "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]


def _apply_style(ax, title, grid_axis="y"):
    """Common styling for all charts."""
    ax.set_title(title, fontsize=14, fontweight="bold",
                 color="#2c3e50", pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis=grid_axis, linestyle="--", alpha=0.4)


# -- Vertical bar chart -------------------------------------------
def plot_bar(df, x, y, title, ylabel="", figsize=(7, 4), color=None):
    fig, ax = plt.subplots(figsize=figsize)
    colors = color if color else COLORS[:len(df)]
    bars = ax.bar(df[x].astype(str), df[y], color=colors,
                  edgecolor="white", linewidth=0.8)
    ax.bar_label(bars, fmt=lambda v: f"{v:,.0f}", padding=4,
                 fontsize=9, color="#2c3e50")
    ax.set_ylabel(ylabel, fontsize=11)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    _apply_style(ax, title, grid_axis="y")
    plt.tight_layout()
    plt.show()


# -- Horizontal bar chart ------------------------------------------
def plot_hbar(df, x, y, title, xlabel="", figsize=(7, 4), color=None):
    fig, ax = plt.subplots(figsize=figsize)
    colors = color if color else COLORS[:len(df)]
    bars = ax.barh(df[y].astype(str), df[x], color=colors,
                   edgecolor="white", linewidth=0.8)
    ax.bar_label(bars, fmt=lambda v: f"{v:,.0f}", padding=4,
                 fontsize=9, color="#2c3e50")
    ax.set_xlabel(xlabel, fontsize=11)
    ax.invert_yaxis()
    _apply_style(ax, title, grid_axis="x")
    plt.tight_layout()
    plt.show()


# -- Pie / donut chart -----------------------------------------------
def plot_pie(df, labels, values, title, figsize=(5.5, 5)):
    colors = COLORS[:len(df)]
    fig, ax = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax.pie(
        df[values], labels=df[labels], autopct="%1.1f%%",
        startangle=90, colors=colors, pctdistance=0.78,
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    )
    for t in autotexts:
        t.set_fontsize(11)
        t.set_fontweight("bold")
        t.set_color("white")
    ax.set_title(title, fontsize=14, fontweight="bold",
                 color="#2c3e50", pad=12)
    plt.tight_layout()
    plt.show()
