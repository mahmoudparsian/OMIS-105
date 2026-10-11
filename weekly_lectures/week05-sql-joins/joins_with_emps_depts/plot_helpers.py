"""
plot_helpers.py
================
Plotting functions for the OMIS 105 Employees/Departments notebook.

Students: You do NOT need to read or modify this file.
          It is imported by notebook.py to keep plotting code
          out of your way so you can focus on SQL.

Every function takes the DataFrame that a SQL cell returns (pandas
or polars — both work) and returns a matplotlib Figure. In Marimo,
make the function call the last line of a cell, and the chart shows.
A NULL label is shown as "(NULL)".

Functions
---------
  plot_threshold_bars(df, labels, values, threshold, title, ...)
        -- vertical bars with a dashed threshold line; bars above it
           are "kept", bars below it are "dropped" (for HAVING)
  plot_bar(df, labels, values, title, ...)
        -- vertical bar chart; zero bars drawn as dashed outlines
  plot_hbar_groups(df, labels, values, groups, title, ...)
        -- horizontal bars, one color per group
  plot_join_map(df, left, right, title, ...)
        -- the rows of a FULL OUTER JOIN as a picture: matched pairs
           joined by a line, unmatched rows highlighted
  plot_hbar(df, labels, values, title, ...)
        -- horizontal bar chart
  plot_pie(df, labels, values, title, ...)
        -- pie chart; each slice shows its count and percent
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# -- Palette ----------------------------------------------------
BLUE = "#3B6EA8"
GREEN = "#4C9A6A"
ORANGE = "#E08E3C"
RED = "#C8553D"
GREY = "#B8BEC6"
TEXT = "#2C3E50"
MUTED = "#8A939D"

GROUP_COLORS = [BLUE, GREEN, "#8E6BB0", "#3E9FA8"]


def _col(df, name):
    """Return one column as a plain Python list (pandas or polars)."""
    return df[name].to_list()


def _labels(df, name):
    """Return a column as text labels; NULL becomes '(NULL)'."""
    return ["(NULL)" if v is None else str(v) for v in _col(df, name)]


def _nums(df, name):
    """Return a numeric column as plain ints/floats. SQL SUM() can come
    back as Decimal, and NULL as None (treated as 0)."""
    out = []
    for v in _col(df, name):
        v = float(v) if v is not None else 0.0
        out.append(int(v) if v.is_integer() else v)
    return out


def _new_figure(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    return fig, ax


def _title(ax, title):
    """Title at the figure's left edge, so long axis labels never
    push it off the page."""
    ax.figure.suptitle(title, x=0.02, ha="left", fontsize=14,
                       fontweight="bold", color=TEXT)


def _style(ax, title, grid_axis="y"):
    """Common look for every chart."""
    _title(ax, title)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(GREY)
    ax.tick_params(colors=TEXT, labelsize=10)
    if grid_axis:
        ax.grid(axis=grid_axis, linestyle="--", alpha=0.35)
        ax.set_axisbelow(True)


# -- Bars with a threshold line (HAVING) ------------------------------
def plot_threshold_bars(df, labels, values, threshold, title, ylabel="",
                        figsize=(8, 4.5)):
    """Bars above `threshold` are blue ('kept'); bars at or below it
    are grey ('dropped'). A dashed line marks the threshold."""
    names = _labels(df, labels)
    nums = _nums(df, values)
    top = max(nums + [threshold])

    fig, ax = _new_figure(figsize)
    for i, num in enumerate(nums):
        kept = num > threshold
        ax.bar(i, num, width=0.6, color=BLUE if kept else GREY)
        ax.text(i, num * 0.92, f"{num:,.0f}", ha="center", va="top",
                fontsize=11, fontweight="bold",
                color="white" if kept else TEXT)
        ax.text(i, num / 2, "kept" if kept else "dropped", ha="center",
                va="center", fontsize=10,
                color="white" if kept else TEXT)
    ax.axhline(threshold, color=RED, linestyle="--", linewidth=1.5)
    low = nums.index(min(nums))
    ax.text(low, threshold + top * 0.03, f"threshold: {threshold:,}",
            ha="center", fontsize=10, color=RED, fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="none", pad=1))
    ax.set_xticks(range(len(names)), names)
    ax.set_ylim(0, top * 1.15)
    ax.set_ylabel(ylabel, fontsize=11, color=TEXT)
    ax.yaxis.set_major_formatter(lambda v, _pos: f"{v:,.0f}")
    _style(ax, title, grid_axis="y")
    fig.tight_layout()
    return fig


# -- Vertical bar chart (zeros shown as outlines) -----------------------
def plot_bar(df, labels, values, title, ylabel="", color=BLUE,
             figsize=(8, 4.5)):
    """A value of 0 is drawn as a dashed outline labeled '0 — none',
    so rows kept by a LEFT JOIN stay visible on the chart."""
    names = _labels(df, labels)
    nums = _nums(df, values)
    top = max(nums) if max(nums) > 0 else 1
    stub = top * 0.04

    fig, ax = _new_figure(figsize)
    for i, num in enumerate(nums):
        if num == 0:
            ax.bar(i, stub, color="white", edgecolor=GREY,
                   linestyle="--", linewidth=1.5, width=0.6)
            ax.text(i, stub + top * 0.02, "0 — none", ha="center",
                    fontsize=10, color=MUTED, style="italic")
        else:
            ax.bar(i, num, color=color, width=0.6)
            ax.text(i, num + top * 0.02, f"{num:,}", ha="center",
                    fontsize=10, color=TEXT, fontweight="bold")
    ax.set_xticks(range(len(names)), names)
    ax.set_ylim(0, top * 1.18)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylabel(ylabel, fontsize=11, color=TEXT)
    _style(ax, title, grid_axis="y")
    fig.tight_layout()
    return fig


# -- Horizontal bars colored by group --------------------------------
def plot_hbar_groups(df, labels, values, groups, title, xlabel="",
                     highlight=None, figsize=(8, 4.5)):
    """One bar per row, top-to-bottom in the DataFrame's row order,
    colored by the value in `groups`. The group named `highlight`
    (optional) is drawn in orange so it stands out."""
    names = _labels(df, labels)
    nums = _nums(df, values)
    group_of = _labels(df, groups)

    palette = {}
    for g in group_of:
        if g not in palette:
            palette[g] = (ORANGE if g == highlight
                          else GROUP_COLORS[len(palette) % len(GROUP_COLORS)])

    fig, ax = _new_figure(figsize)
    bars = ax.barh(names, nums, height=0.6,
                   color=[palette[g] for g in group_of])
    ax.invert_yaxis()
    right = max(nums) * 1.15
    for bar, num in zip(bars, nums):
        ax.text(bar.get_width() + right * 0.01,
                bar.get_y() + bar.get_height() / 2, f"{num:,}",
                va="center", fontsize=10, color=TEXT)
    ax.set_xlim(0, right)
    ax.set_xlabel(xlabel, fontsize=11, color=TEXT)
    ax.xaxis.set_major_formatter(lambda v, _pos: f"{v:,.0f}")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in palette.values()]
    ax.legend(handles, list(palette), frameon=False, loc="upper center",
              ncols=len(palette), bbox_to_anchor=(0.5, -0.15))
    _style(ax, title, grid_axis="x")
    fig.tight_layout()
    return fig


# -- FULL OUTER JOIN as a picture -------------------------------------
def plot_join_map(df, left, right, title, left_title="", right_title="",
                  figsize=(8, 5)):
    """Draw the left-table values in one column and the right-table
    values in another. Each matched row is a line between the two.
    A row with NULL on one side is an unmatched value: it is drawn in
    orange with no line."""
    lefts = _col(df, left)
    rights = _col(df, right)

    left_names, right_names = [], []
    for lv, rv in zip(lefts, rights):
        if lv is not None and lv not in left_names:
            left_names.append(lv)
        if rv is not None and rv not in right_names:
            right_names.append(rv)
    matched_left = {lv for lv, rv in zip(lefts, rights) if rv is not None}
    matched_right = {rv for lv, rv in zip(lefts, rights) if lv is not None}

    rows = max(len(left_names), len(right_names))
    ly = {n: rows - 1 - i * (rows - 1) / max(len(left_names) - 1, 1)
          for i, n in enumerate(left_names)}
    ry = {n: rows - 1 - i * (rows - 1) / max(len(right_names) - 1, 1)
          for i, n in enumerate(right_names)}

    fig, ax = _new_figure(figsize)
    for lv, rv in zip(lefts, rights):
        if lv is not None and rv is not None:
            ax.plot([0, 1], [ly[lv], ry[rv]], color=BLUE, linewidth=1.8,
                    alpha=0.7, zorder=1)

    def _node(x, y, name, matched, ha):
        color = BLUE if matched else ORANGE
        ax.scatter([x], [y], s=140, color=color, zorder=2,
                   edgecolor="white", linewidth=2)
        dx = -0.04 if ha == "right" else 0.04
        label = name if matched else f"{name}  (no match)"
        ax.text(x + dx, y, label, ha=ha, va="center", fontsize=11,
                color=TEXT if matched else ORANGE,
                fontweight="normal" if matched else "bold")

    for n in left_names:
        _node(0, ly[n], n, n in matched_left, "right")
    for n in right_names:
        _node(1, ry[n], n, n in matched_right, "left")

    ax.text(0, rows - 0.3, left_title, ha="center", fontsize=12,
            color=MUTED, fontweight="bold")
    ax.text(1, rows - 0.3, right_title, ha="center", fontsize=12,
            color=MUTED, fontweight="bold")
    ax.set_xlim(-0.9, 1.9)
    ax.set_ylim(-0.6, rows + 0.1)
    ax.axis("off")
    _title(ax, title)
    fig.tight_layout()
    return fig


# -- Horizontal bar chart ---------------------------------------------
def plot_hbar(df, labels, values, title, xlabel="", color=BLUE,
              figsize=(8, 4.5)):
    """Bars are drawn top-to-bottom in the DataFrame's row order."""
    names = _labels(df, labels)
    nums = _nums(df, values)
    right = max(nums) * 1.15

    fig, ax = _new_figure(figsize)
    bars = ax.barh(names, nums, color=color, height=0.6)
    ax.invert_yaxis()
    for bar, num in zip(bars, nums):
        ax.text(bar.get_width() + right * 0.01,
                bar.get_y() + bar.get_height() / 2, f"{num:,}",
                va="center", fontsize=10, color=TEXT, fontweight="bold")
    ax.set_xlim(0, right)
    ax.set_xlabel(xlabel, fontsize=11, color=TEXT)
    _style(ax, title, grid_axis="x")
    fig.tight_layout()
    return fig


# -- Pie chart --------------------------------------------------------
def plot_pie(df, labels, values, title, label_prefix="", highlight=None,
             figsize=(6.5, 5)):
    """One slice per row, in the DataFrame's row order. Each slice shows
    its count and its percent of the total. `label_prefix` is put in
    front of each label (e.g. 'dept '). The slice whose label is
    `highlight` (optional) is drawn in orange and pulled out a little."""
    names = _labels(df, labels)
    nums = _nums(df, values)
    total = sum(nums)

    others = iter(GROUP_COLORS * len(names))
    colors = [ORANGE if n == highlight else next(others) for n in names]
    explode = [0.08 if n == highlight else 0 for n in names]
    shown = [n if n == highlight else f"{label_prefix}{n}" for n in names]

    fig, ax = _new_figure(figsize)
    _wedges, texts, autotexts = ax.pie(
        nums, labels=shown, colors=colors, explode=explode,
        startangle=90, counterclock=False,
        wedgeprops=dict(edgecolor="white", linewidth=2),
        autopct=lambda pct: f"{round(pct * total / 100):,}\n({pct:.0f}%)",
        pctdistance=0.62, labeldistance=1.1)
    for t in texts:
        t.set_fontsize(11)
        t.set_color(TEXT)
    for t in autotexts:
        t.set_fontsize(11)
        t.set_color("white")
        t.set_fontweight("bold")
    ax.axis("equal")
    _title(ax, title)
    fig.tight_layout()
    return fig
