"""
plot_helpers.py
================
Plotting functions for the OMIS 105 Students/Courses/Grades notebook.

Students: You do NOT need to read or modify this file.
          It is imported by notebook.py to keep plotting code
          out of your way so you can focus on SQL.

Every function takes the DataFrame that a SQL cell returns (pandas
or polars — both work) and returns a matplotlib Figure. In Marimo,
make the function call the last line of a cell, and the chart shows.

Functions
---------
  plot_hbar(df, labels, values, title, ...)              -- horizontal bar chart
  plot_grades(df, grades, counts, title)                 -- one bar per letter grade,
                                                            A..F colored good -> bad
  plot_line(df, x, y, title, ...)                        -- line chart over time
  plot_bar(df, labels, values, title, ...)               -- vertical bar chart;
                                                            zero bars drawn as outlines
  plot_stacked_bar(df, labels, parts, part_names, title) -- stacked vertical bars
"""

import matplotlib.pyplot as plt

# -- Palette ----------------------------------------------------
BLUE = "#3B6EA8"
GREEN = "#4C9A6A"
ORANGE = "#E08E3C"
RED = "#C8553D"
GREY = "#B8BEC6"
TEXT = "#2C3E50"
MUTED = "#8A939D"

# Letter grades are ordered (good -> bad), so they use a diverging
# scale: two blues, a neutral grey for C, then orange and red.
GRADE_COLORS = {"A": "#2F5F96", "B": "#7FA6D1", "C": "#B8BEC6",
                "D": "#E5A065", "F": "#C8553D"}


def _col(df, name):
    """Return one column as a plain Python list (pandas or polars)."""
    return df[name].to_list()


def _nums(df, name):
    """Return a numeric column as plain ints/floats. SQL SUM() can come
    back as Decimal, and NULL as None (treated as 0)."""
    out = []
    for v in _col(df, name):
        v = float(v) if v is not None else 0.0
        out.append(int(v) if v.is_integer() else v)
    return out


def _fmt(v, decimals):
    return f"{v:,.{decimals}f}" if decimals else f"{v:,.0f}"


def _new_figure(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    return fig, ax


def _style(ax, title, grid_axis="y"):
    """Common look for every chart."""
    ax.set_title(title, fontsize=14, fontweight="bold", color=TEXT,
                 loc="left", pad=14)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(GREY)
    ax.tick_params(colors=TEXT, labelsize=10)
    if grid_axis:
        ax.grid(axis=grid_axis, linestyle="--", alpha=0.35)
        ax.set_axisbelow(True)


# -- Horizontal bar chart ---------------------------------------------
def plot_hbar(df, labels, values, title, xlabel="", note=None, decimals=0,
              xmax=None, color=BLUE, figsize=(8, 4.5)):
    """Bars are drawn top-to-bottom in the DataFrame's row order.
    `note` (optional) is a column whose value is printed after each bar.
    `xmax` (optional) fixes the right end of the axis, e.g. 4.0 for GPA."""
    names = [str(n) for n in _col(df, labels)]
    nums = _nums(df, values)
    notes = _col(df, note) if note else None
    right = xmax if xmax else max(nums) * 1.3

    fig, ax = _new_figure(figsize)
    bars = ax.barh(names, nums, color=color, height=0.6)
    ax.invert_yaxis()
    for i, bar in enumerate(bars):
        text = _fmt(nums[i], decimals)
        if notes:
            text += f"   ({notes[i]})"
        ax.text(bar.get_width() + right * 0.01,
                bar.get_y() + bar.get_height() / 2, text,
                va="center", fontsize=10, color=TEXT)
    ax.set_xlim(0, right * (1.15 if xmax else 1))
    ax.set_xlabel(xlabel, fontsize=11, color=TEXT)
    _style(ax, title, grid_axis="x")
    fig.tight_layout()
    return fig


# -- Letter-grade bar chart -----------------------------------------------
def plot_grades(df, grades, counts, title, figsize=(8, 4.5)):
    """One bar per letter grade, labeled with its count and its share
    of the total."""
    names = [str(g) for g in _col(df, grades)]
    nums = _nums(df, counts)
    total = sum(nums)
    top = max(nums)

    fig, ax = _new_figure(figsize)
    bars = ax.bar(names, nums, width=0.62,
                  color=[GRADE_COLORS.get(n, GREY) for n in names])
    for bar, n in zip(bars, nums):
        x = bar.get_x() + bar.get_width() / 2
        ax.text(x, n + top * 0.02, f"{n:,}", ha="center", fontsize=11,
                color=TEXT, fontweight="bold")
        ax.text(x, n + top * 0.09, f"{n / total:.0%}", ha="center",
                fontsize=10, color=MUTED)
    ax.set_ylim(0, top * 1.2)
    ax.set_ylabel("number of grades", fontsize=11, color=TEXT)
    ax.set_xlabel(f"letter grade  ({total:,} grades in all)", fontsize=11,
                  color=TEXT)
    _style(ax, title, grid_axis="y")
    fig.tight_layout()
    return fig


# -- Line chart over time ---------------------------------------------------
def plot_line(df, x, y, title, ylabel="", color=BLUE, figsize=(8, 4.5)):
    """One line with a labeled marker at every point (few points only,
    e.g. one per year)."""
    xs = [str(v) for v in _col(df, x)]
    ys = _nums(df, y)
    top = max(ys)

    fig, ax = _new_figure(figsize)
    ax.plot(xs, ys, color=color, linewidth=2.2, marker="o", markersize=8,
            markeredgecolor="white", markeredgewidth=2)
    ax.fill_between(xs, ys, color=color, alpha=0.08)
    for xv, yv in zip(xs, ys):
        ax.text(xv, yv + top * 0.04, f"{yv:,}", ha="center", fontsize=10,
                color=TEXT, fontweight="bold")
    ax.set_ylim(0, top * 1.18)
    ax.set_ylabel(ylabel, fontsize=11, color=TEXT)
    _style(ax, title, grid_axis="y")
    fig.tight_layout()
    return fig


# -- Vertical bar chart (zeros shown as outlines) -----------------------
def plot_bar(df, labels, values, title, ylabel="", color=BLUE,
             figsize=(10, 4.5)):
    """A value of 0 is drawn as a dashed outline labeled 'none',
    so rows kept by a LEFT JOIN stay visible on the chart."""
    names = [str(n) for n in _col(df, labels)]
    nums = _nums(df, values)
    top = max(nums) if max(nums) > 0 else 1
    stub = top * 0.04

    fig, ax = _new_figure(figsize)
    for i, num in enumerate(nums):
        if num == 0:
            ax.bar(i, stub, color="white", edgecolor=GREY,
                   linestyle="--", linewidth=1.5, width=0.65)
            ax.text(i, stub + top * 0.02, "none", ha="center",
                    fontsize=9, color=MUTED, style="italic")
        else:
            ax.bar(i, num, color=color, width=0.65)
            ax.text(i, num + top * 0.02, f"{num:,}", ha="center",
                    fontsize=9, color=TEXT, fontweight="bold")
    ax.set_xticks(range(len(names)), names, rotation=45, ha="right")
    ax.set_ylim(0, top * 1.15)
    ax.set_ylabel(ylabel, fontsize=11, color=TEXT)
    _style(ax, title, grid_axis="y")
    fig.tight_layout()
    return fig


# -- Stacked bar chart ----------------------------------------------------
def plot_stacked_bar(df, labels, parts, part_names, title, ylabel="",
                     colors=(BLUE, GREY), figsize=(8, 5)):
    """One bar per row of `labels`, stacked from the columns in `parts`."""
    names = [str(n) for n in _col(df, labels)]
    series = [_nums(df, p) for p in parts]

    fig, ax = _new_figure(figsize)
    bottom = [0] * len(names)
    for values, part_name, color in zip(series, part_names, colors):
        bars = ax.bar(names, values, bottom=bottom, color=color,
                      width=0.55, label=part_name, edgecolor="white",
                      linewidth=2)
        for bar, v in zip(bars, values):
            if v > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_y() + bar.get_height() / 2, str(v),
                        ha="center", va="center",
                        color="white" if color != GREY else TEXT,
                        fontsize=11, fontweight="bold")
        bottom = [b + v for b, v in zip(bottom, values)]
    for i, total in enumerate(bottom):
        ax.text(i, total + max(bottom) * 0.02, f"{total} total",
                ha="center", fontsize=10, color=TEXT)
    ax.set_ylim(0, max(bottom) * 1.18)
    ax.set_ylabel(ylabel, fontsize=11, color=TEXT)
    ax.legend(frameon=False, loc="upper center", ncols=len(parts),
              bbox_to_anchor=(0.5, -0.1))
    _style(ax, title, grid_axis="y")
    fig.tight_layout()
    return fig
