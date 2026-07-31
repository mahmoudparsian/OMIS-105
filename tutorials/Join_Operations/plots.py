"""
plots.py
--------
Beautiful, reusable plotting functions for the SQL JOINs tutorial.
All plots use the same navy/red-pink design palette as display_tables.py.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import numpy as np

# ── Design tokens ─────────────────────────────────────────────────────────────
C_BG       = "#1a1a2e"
C_PANEL    = "#16213e"
C_ACCENT   = "#0f3460"
C_GRID     = "#2a2a4a"
C_HIGHLIGHT= "#e94560"
C_AMBER    = "#f5a623"
C_MINT     = "#26c485"
C_LAVENDER = "#9b5de5"
C_SKY      = "#00bbf9"
C_TEXT     = "#eaeaea"
C_MUTED    = "#a0a4b8"

PALETTE = [C_HIGHLIGHT, C_SKY, C_MINT, C_AMBER, C_LAVENDER,
           "#ff6b6b","#4ecdc4","#ffe66d","#a8dadc","#f9c74f"]

def _setup_ax(ax, title="", xlabel="", ylabel="", grid_axis="y"):
    ax.set_facecolor(C_PANEL)
    ax.tick_params(colors=C_MUTED, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(C_GRID)
    if grid_axis:
        ax.grid(axis=grid_axis, color=C_GRID, linewidth=0.7, linestyle="--", alpha=0.6)
        ax.set_axisbelow(True)
    if title:
        ax.set_title(title, color=C_TEXT, fontsize=13, fontweight="bold", pad=10)
    if xlabel:
        ax.set_xlabel(xlabel, color=C_MUTED, fontsize=10, labelpad=6)
    if ylabel:
        ax.set_ylabel(ylabel, color=C_MUTED, fontsize=10, labelpad=6)


def _fig(w=11, h=5.5):
    fig = plt.figure(figsize=(w, h), facecolor=C_BG)
    return fig


def _finalize(fig, caption=""):
    if caption:
        fig.text(0.5, 0.01, caption, ha="center", color=C_MUTED,
                 fontsize=9, fontstyle="italic")
    plt.tight_layout(rect=[0,0.03,1,1] if caption else [0,0,1,1])
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# 1.  Horizontal Bar Chart
# ─────────────────────────────────────────────────────────────────────────────
def plot_hbar(df: pd.DataFrame, x_col: str, y_col: str,
              title="", xlabel="", ylabel="", caption="",
              color=None, top_n=None, annotate=True):
    """Horizontal bar chart — great for categorical comparisons."""
    data = df.copy()
    if top_n:
        data = data.nlargest(top_n, x_col)
    data = data.sort_values(x_col)

    fig = _fig(10, max(4, 0.55 * len(data)))
    ax  = fig.add_subplot(111)
    ax.set_facecolor(C_PANEL)

    colors = [color or C_HIGHLIGHT] * len(data)
    # gradient effect: lightest bar is slightly muted
    for i, (val, label) in enumerate(zip(data[x_col], data[y_col])):
        alpha = 0.55 + 0.45 * (i / max(len(data)-1,1))
        ax.barh(str(label), val, color=colors[i], alpha=alpha,
                height=0.65, edgecolor="none")
        if annotate:
            fmt = f"{val:,.0f}" if isinstance(val, (int,float)) else str(val)
            ax.text(val * 1.01, i, fmt, va="center",
                    color=C_TEXT, fontsize=9, fontweight="600")

    _setup_ax(ax, title, xlabel or x_col, ylabel or y_col, grid_axis="x")
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels([str(v) for v in data[y_col]], color=C_TEXT, fontsize=10)
    _finalize(fig, caption)


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Vertical Bar Chart
# ─────────────────────────────────────────────────────────────────────────────
def plot_bar(df: pd.DataFrame, x_col: str, y_col: str,
             title="", xlabel="", ylabel="", caption="",
             color=None, annotate=True, rotate=30):
    """Vertical bar chart with value labels."""
    fig = _fig()
    ax  = fig.add_subplot(111)

    xs = range(len(df))
    clr = color or C_HIGHLIGHT
    bars = ax.bar(xs, df[y_col], color=clr, edgecolor="none",
                  width=0.65, zorder=3)

    # value annotations
    if annotate:
        for bar, val in zip(bars, df[y_col]):
            fmt = f"{val:,.0f}" if isinstance(val,(int,float)) else str(val)
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.01,
                    fmt, ha="center", va="bottom",
                    color=C_TEXT, fontsize=9, fontweight="600")

    ax.set_xticks(xs)
    ax.set_xticklabels([str(v) for v in df[x_col]],
                       rotation=rotate, ha="right", color=C_TEXT, fontsize=9)
    _setup_ax(ax, title, xlabel or x_col, ylabel or y_col)
    _finalize(fig, caption)


# ─────────────────────────────────────────────────────────────────────────────
# 3.  Grouped Bar Chart
# ─────────────────────────────────────────────────────────────────────────────
def plot_grouped_bar(df: pd.DataFrame, x_col: str, group_col: str, y_col: str,
                     title="", xlabel="", ylabel="", caption=""):
    """Side-by-side bars grouped by a categorical column."""
    groups  = df[group_col].unique()
    xs      = df[x_col].unique()
    n_g     = len(groups)
    width   = 0.75 / n_g

    fig = _fig(max(10, len(xs)*1.2), 5.5)
    ax  = fig.add_subplot(111)

    for i, grp in enumerate(groups):
        sub = df[df[group_col]==grp].set_index(x_col)[y_col]
        positions = [j + (i - n_g/2 + 0.5)*width for j in range(len(xs))]
        vals = [sub.get(x, 0) for x in xs]
        ax.bar(positions, vals, width=width*0.92,
               color=PALETTE[i % len(PALETTE)], label=str(grp),
               edgecolor="none", zorder=3)

    ax.set_xticks(range(len(xs)))
    ax.set_xticklabels([str(x) for x in xs],
                       rotation=30, ha="right", color=C_TEXT, fontsize=9)
    ax.legend(framealpha=0.15, labelcolor=C_TEXT, facecolor=C_PANEL,
              edgecolor=C_GRID, fontsize=9)
    _setup_ax(ax, title, xlabel or x_col, ylabel or y_col)
    _finalize(fig, caption)


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Pie / Donut Chart
# ─────────────────────────────────────────────────────────────────────────────
def plot_donut(df: pd.DataFrame, label_col: str, value_col: str,
               title="", caption="", show_pct=True):
    """Donut chart for proportion breakdown."""
    fig = _fig(8, 5.5)
    ax  = fig.add_subplot(111)
    ax.set_facecolor(C_BG)

    wedge_props = {"linewidth": 2, "edgecolor": C_BG}
    labels = df[label_col].astype(str)
    values = df[value_col]
    colors = PALETTE[:len(df)]

    wedges, texts, autotexts = ax.pie(
        values, labels=None, colors=colors,
        autopct="%1.1f%%" if show_pct else None,
        pctdistance=0.78, startangle=140,
        wedgeprops={**wedge_props, "width": 0.52},
        textprops={"color": C_TEXT, "fontsize": 10},
    )
    for at in autotexts:
        at.set(color=C_BG, fontsize=9, fontweight="bold")

    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(0.98,0.5),
              framealpha=0.1, labelcolor=C_TEXT, facecolor=C_PANEL,
              edgecolor=C_GRID, fontsize=9)
    if title:
        ax.set_title(title, color=C_TEXT, fontsize=13, fontweight="bold")
    _finalize(fig, caption)


# ─────────────────────────────────────────────────────────────────────────────
# 5.  Heat-map / Matrix
# ─────────────────────────────────────────────────────────────────────────────
def plot_heatmap(df: pd.DataFrame, row_col: str, col_col: str, val_col: str,
                 title="", caption="", fmt="{:.0f}", cmap_name="navy_red"):
    """Matrix heatmap — good for cross-tabulation results."""
    pivot = df.pivot_table(index=row_col, columns=col_col,
                           values=val_col, aggfunc="sum", fill_value=0)

    cmap = LinearSegmentedColormap.from_list(
        "custom", [C_ACCENT, C_HIGHLIGHT], N=256)

    fig = _fig(max(8, pivot.shape[1]*1.4), max(4, pivot.shape[0]*0.7))
    ax  = fig.add_subplot(111)
    im  = ax.imshow(pivot.values, aspect="auto", cmap=cmap, vmin=0)

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_yticks(range(len(pivot.index)))
    ax.set_xticklabels(pivot.columns, color=C_TEXT, rotation=35, ha="right", fontsize=9)
    ax.set_yticklabels(pivot.index,   color=C_TEXT, fontsize=9)
    ax.set_facecolor(C_PANEL)
    for spine in ax.spines.values(): spine.set_visible(False)

    for r in range(pivot.shape[0]):
        for c in range(pivot.shape[1]):
            val = pivot.iloc[r,c]
            ax.text(c, r, fmt.format(val),
                    ha="center", va="center",
                    color=C_TEXT if val > pivot.values.max()*0.5 else C_MUTED,
                    fontsize=9, fontweight="600")

    cbar = fig.colorbar(im, ax=ax, pad=0.02)
    cbar.ax.tick_params(colors=C_MUTED, labelsize=8)

    if title:
        ax.set_title(title, color=C_TEXT, fontsize=13, fontweight="bold", pad=10)
    _finalize(fig, caption)


# ─────────────────────────────────────────────────────────────────────────────
# 6.  Box-plot / Distribution
# ─────────────────────────────────────────────────────────────────────────────
def plot_boxplot(df: pd.DataFrame, group_col: str, value_col: str,
                 title="", xlabel="", ylabel="", caption=""):
    """Box plots per group — great for salary distributions."""
    groups = [g for g, sub in df.groupby(group_col)]
    data   = [sub[value_col].dropna().values
               for _, sub in df.groupby(group_col)]

    fig = _fig(max(8, len(groups)*1.2), 5.5)
    ax  = fig.add_subplot(111)

    bp = ax.boxplot(data, patch_artist=True, notch=False,
                    medianprops={"color": C_AMBER, "linewidth": 2.5},
                    whiskerprops={"color": C_MUTED},
                    capprops={"color": C_MUTED},
                    flierprops={"marker":"o","color":C_HIGHLIGHT,
                                "alpha":0.5,"markersize":4})

    for patch, clr in zip(bp["boxes"], PALETTE):
        patch.set_facecolor(clr)
        patch.set_alpha(0.75)

    ax.set_xticks(range(1, len(groups)+1))
    ax.set_xticklabels([str(g) for g in groups],
                       rotation=30, ha="right", color=C_TEXT, fontsize=9)
    _setup_ax(ax, title, xlabel or group_col, ylabel or value_col)
    _finalize(fig, caption)


# ─────────────────────────────────────────────────────────────────────────────
# 7.  Stacked Bar Chart
# ─────────────────────────────────────────────────────────────────────────────
def plot_stacked_bar(df: pd.DataFrame, x_col: str, stack_col: str, y_col: str,
                     title="", xlabel="", ylabel="", caption=""):
    """Stacked bars — great for composition within groups."""
    pivot = df.pivot_table(index=x_col, columns=stack_col,
                           values=y_col, aggfunc="sum", fill_value=0)

    fig = _fig(max(9, len(pivot)*0.9), 5.5)
    ax  = fig.add_subplot(111)

    bottom = np.zeros(len(pivot))
    for i, col in enumerate(pivot.columns):
        vals = pivot[col].values
        ax.bar(range(len(pivot)), vals, bottom=bottom,
               color=PALETTE[i % len(PALETTE)], label=str(col),
               edgecolor="none", width=0.7, zorder=3)
        bottom += vals

    ax.set_xticks(range(len(pivot)))
    ax.set_xticklabels([str(v) for v in pivot.index],
                       rotation=30, ha="right", color=C_TEXT, fontsize=9)
    ax.legend(framealpha=0.15, labelcolor=C_TEXT, facecolor=C_PANEL,
              edgecolor=C_GRID, fontsize=9, bbox_to_anchor=(1.01,1), loc="upper left")
    _setup_ax(ax, title, xlabel or x_col, ylabel or y_col)
    _finalize(fig, caption)


# ─────────────────────────────────────────────────────────────────────────────
# 8.  Scatter Plot
# ─────────────────────────────────────────────────────────────────────────────
def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str,
                 color_col: str = None, size_col: str = None,
                 title="", xlabel="", ylabel="", caption=""):
    """Scatter with optional color/size encoding."""
    fig = _fig()
    ax  = fig.add_subplot(111)

    if color_col and color_col in df.columns:
        cats = df[color_col].unique()
        for i, cat in enumerate(cats):
            sub = df[df[color_col]==cat]
            sz  = sub[size_col]*0.3 if size_col and size_col in df.columns else 50
            ax.scatter(sub[x_col], sub[y_col], label=str(cat),
                       color=PALETTE[i % len(PALETTE)], s=sz,
                       alpha=0.75, edgecolors="none", zorder=3)
        ax.legend(framealpha=0.15, labelcolor=C_TEXT, facecolor=C_PANEL,
                  edgecolor=C_GRID, fontsize=9)
    else:
        sz = df[size_col]*0.3 if size_col and size_col in df.columns else 50
        ax.scatter(df[x_col], df[y_col], color=C_HIGHLIGHT,
                   s=sz, alpha=0.75, edgecolors="none", zorder=3)

    _setup_ax(ax, title, xlabel or x_col, ylabel or y_col, grid_axis="both")
    _finalize(fig, caption)


# ─────────────────────────────────────────────────────────────────────────────
# 9.  Venn Diagram (simplified as overlapping circles for JOIN illustration)
# ─────────────────────────────────────────────────────────────────────────────
def plot_join_venn(join_type: str, left_count: int, right_count: int,
                   match_count: int, title=""):
    """
    Visual Venn-diagram explanation of a JOIN type.
    join_type: 'INNER', 'LEFT', 'RIGHT', 'FULL OUTER'
    """
    fig, ax = plt.subplots(figsize=(7,4), facecolor=C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0,7); ax.set_ylim(0,4); ax.set_aspect("equal")
    ax.axis("off")

    highlight_left  = join_type in ("LEFT",  "FULL OUTER")
    highlight_right = join_type in ("RIGHT", "FULL OUTER")
    highlight_mid   = join_type in ("INNER", "LEFT", "RIGHT", "FULL OUTER")

    # Left circle
    lc = mpatches.Circle((2.8,2), 1.5,
                          facecolor=C_SKY if (highlight_left or highlight_mid) else C_ACCENT,
                          edgecolor=C_TEXT, linewidth=2, alpha=0.55, zorder=2)
    # Right circle
    rc = mpatches.Circle((4.2,2), 1.5,
                          facecolor=C_HIGHLIGHT if (highlight_right or highlight_mid) else C_ACCENT,
                          edgecolor=C_TEXT, linewidth=2, alpha=0.55, zorder=2)
    ax.add_patch(lc); ax.add_patch(rc)

    ax.text(2.1, 2, "employees", ha="center", va="center",
            color=C_TEXT, fontsize=10, fontweight="700", zorder=4)
    ax.text(4.9, 2, "departments", ha="center", va="center",
            color=C_TEXT, fontsize=10, fontweight="700", zorder=4)
    ax.text(3.5, 2, f"{match_count:,}\nmatched", ha="center", va="center",
            color=C_TEXT, fontsize=9, fontweight="700", zorder=5)

    ax.text(3.5, 3.7, f"{join_type} JOIN",
            ha="center", va="top", color=C_TEXT,
            fontsize=14, fontweight="800")

    info = (f"Left: {left_count:,}  |  Right: {right_count:,}  |  "
            f"Matched: {match_count:,}")
    ax.text(3.5, 0.2, info, ha="center", color=C_MUTED, fontsize=9)

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# 10.  Line / Trend Chart
# ─────────────────────────────────────────────────────────────────────────────
def plot_line(df: pd.DataFrame, x_col: str, y_col: str,
              group_col: str = None,
              title="", xlabel="", ylabel="", caption=""):
    """Line chart — ideal for time-series or ordered data."""
    fig = _fig()
    ax  = fig.add_subplot(111)

    if group_col and group_col in df.columns:
        for i, (grp, sub) in enumerate(df.groupby(group_col)):
            sub_sorted = sub.sort_values(x_col)
            ax.plot(sub_sorted[x_col], sub_sorted[y_col],
                    label=str(grp), color=PALETTE[i % len(PALETTE)],
                    linewidth=2.2, marker="o", markersize=5)
        ax.legend(framealpha=0.15, labelcolor=C_TEXT, facecolor=C_PANEL,
                  edgecolor=C_GRID, fontsize=9)
    else:
        sorted_df = df.sort_values(x_col)
        ax.plot(sorted_df[x_col], sorted_df[y_col],
                color=C_HIGHLIGHT, linewidth=2.5, marker="o", markersize=5)
        ax.fill_between(range(len(sorted_df)), sorted_df[y_col],
                        color=C_HIGHLIGHT, alpha=0.12)
        ax.set_xticks(range(len(sorted_df)))
        ax.set_xticklabels(sorted_df[x_col].astype(str),
                           rotation=30, ha="right", color=C_TEXT, fontsize=9)

    _setup_ax(ax, title, xlabel or x_col, ylabel or y_col, grid_axis="both")
    _finalize(fig, caption)
