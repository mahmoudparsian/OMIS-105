"""
plot_helpers.py
================
Plotting functions for the OMIS 105 Authors/Books/Orders notebook.

Students: You do NOT need to read or modify this file.
          It is imported by notebook.py to keep plotting code
          out of your way so you can focus on SQL.

Every function takes the DataFrame that a SQL cell returns (polars
or pandas — both work) and returns a matplotlib Figure. In Marimo,
make the function call the last line of a cell, and the chart shows.

Functions
---------
  plot_donut(df, labels, values, title)                  -- donut chart
  plot_hbar(df, labels, values, title, ...)              -- horizontal bar chart
  plot_bar(df, labels, values, title, ...)               -- vertical bar chart;
                                                            zero bars drawn as outlines
  plot_stacked_bar(df, labels, parts, part_names, title) -- stacked vertical bars
  plot_join_counts(df, labels, values, kinds, title)     -- horizontal bars colored
                                                            by join type
"""

import matplotlib.pyplot as plt

# -- Palette ----------------------------------------------------
BLUE = "#3B6EA8"
GREEN = "#4C9A6A"
ORANGE = "#E08E3C"
RED = "#C8553D"
PURPLE = "#7A5BA6"
GREY = "#B8BEC6"
TEXT = "#2C3E50"

CATEGORY_COLORS = {"BUSINESS": BLUE, "COMPUTERS": PURPLE, "SPORT": GREEN}
JOIN_COLORS = {"INNER": BLUE, "LEFT": GREEN, "RIGHT": ORANGE}
FALLBACK = [BLUE, GREEN, ORANGE, PURPLE, RED, GREY]


def _col(df, name):
    """Return one column as a plain Python list (polars or pandas)."""
    return df[name].to_list()


def _nums(df, name):
    """Return a numeric column as plain ints/floats. SQL SUM() can come
    back as Decimal, and NULL as None (treated as 0)."""
    out = []
    for v in _col(df, name):
        v = float(v) if v is not None else 0.0
        out.append(int(v) if v.is_integer() else v)
    return out


def _colors_for(labels):
    """Use the fixed category color when the label is a category."""
    return [CATEGORY_COLORS.get(str(label), FALLBACK[i % len(FALLBACK)])
            for i, label in enumerate(labels)]


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


def _money(value):
    return f"${value:,.0f}"


# -- Donut chart ----------------------------------------------------
def plot_donut(df, labels, values, title, figsize=(6, 5)):
    names = _col(df, labels)
    counts = _nums(df, values)
    total = sum(counts)

    fig, ax = _new_figure(figsize)
    wedges, _texts, autotexts = ax.pie(
        counts,
        labels=[f"{n}\n{c} books" for n, c in zip(names, counts)],
        colors=_colors_for(names),
        autopct="%1.0f%%",
        startangle=90,
        counterclock=False,
        pctdistance=0.78,
        labeldistance=1.12,
        wedgeprops=dict(width=0.42, edgecolor="white", linewidth=3),
        textprops=dict(color=TEXT, fontsize=11),
    )
    for t in autotexts:
        t.set_color("white")
        t.set_fontweight("bold")
    ax.text(0, 0, f"{total}\nbooks", ha="center", va="center",
            fontsize=18, fontweight="bold", color=TEXT)
    ax.set_title(title, fontsize=14, fontweight="bold", color=TEXT, pad=14)
    ax.set_aspect("equal")
    fig.tight_layout()
    return fig


# -- Horizontal bar chart ---------------------------------------------
def plot_hbar(df, labels, values, title, xlabel="", note=None,
              color=BLUE, figsize=(8, 4)):
    """Bars are drawn top-to-bottom in the DataFrame's row order.
    `note` (optional) is a column whose value is printed after each bar."""
    names = [str(n) for n in _col(df, labels)]
    nums = _nums(df, values)
    notes = _col(df, note) if note else None

    fig, ax = _new_figure(figsize)
    bars = ax.barh(names, nums, color=color, height=0.6)
    ax.invert_yaxis()
    for i, bar in enumerate(bars):
        text = f"{nums[i]:,}"
        if notes:
            text += f"   ({notes[i]})"
        ax.text(bar.get_width() + max(nums) * 0.01,
                bar.get_y() + bar.get_height() / 2, text,
                va="center", fontsize=10, color=TEXT)
    ax.set_xlim(0, max(nums) * 1.35)
    ax.set_xlabel(xlabel, fontsize=11, color=TEXT)
    _style(ax, title, grid_axis="x")
    fig.tight_layout()
    return fig


# -- Vertical bar chart (zeros shown as outlines) -----------------------
def plot_bar(df, labels, values, title, ylabel="", money=False,
             color=BLUE, figsize=(8, 4.5)):
    """A value of 0 is drawn as a dashed outline labeled 'none',
    so rows kept by a LEFT JOIN stay visible on the chart."""
    names = [str(n) for n in _col(df, labels)]
    nums = _nums(df, values)
    top = max(nums) if max(nums) > 0 else 1
    stub = top * 0.04

    fig, ax = _new_figure(figsize)
    for i, (name, num) in enumerate(zip(names, nums)):
        if num == 0:
            ax.bar(i, stub, color="white", edgecolor=GREY,
                   linestyle="--", linewidth=1.5, width=0.6)
            ax.text(i, stub + top * 0.02, "none", ha="center",
                    fontsize=10, color="#8A939D", style="italic")
        else:
            ax.bar(i, num, color=color, width=0.6)
            ax.text(i, num + top * 0.02,
                    _money(num) if money else f"{num:,}",
                    ha="center", fontsize=10, color=TEXT,
                    fontweight="bold")
    ax.set_xticks(range(len(names)), names)
    ax.set_ylim(0, top * 1.15)
    ax.set_ylabel(ylabel, fontsize=11, color=TEXT)
    if money:
        ax.yaxis.set_major_formatter(lambda v, _pos: _money(v))
    _style(ax, title, grid_axis="y")
    fig.tight_layout()
    return fig


# -- Stacked bar chart ----------------------------------------------------
def plot_stacked_bar(df, labels, parts, part_names, title, ylabel="",
                     colors=(GREEN, RED), figsize=(7, 5)):
    """One bar per row of `labels`, stacked from the columns in `parts`."""
    names = [str(n) for n in _col(df, labels)]
    series = [_nums(df, p) for p in parts]

    fig, ax = _new_figure(figsize)
    bottom = [0] * len(names)
    for values, part_name, color in zip(series, part_names, colors):
        bars = ax.bar(names, values, bottom=bottom, color=color,
                      width=0.55, label=part_name, edgecolor="white",
                      linewidth=1.5)
        for bar, v in zip(bars, values):
            if v > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_y() + bar.get_height() / 2, str(v),
                        ha="center", va="center", color="white",
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


# -- Join row counts ----------------------------------------------------------
def plot_join_counts(df, labels, values, kinds, title, figsize=(8, 4.5)):
    """Horizontal bars, one per join query, colored by join type
    (INNER / LEFT / RIGHT)."""
    names = _col(df, labels)
    nums = _nums(df, values)
    types = _col(df, kinds)

    fig, ax = _new_figure(figsize)
    bars = ax.barh(names, nums, height=0.6,
                   color=[JOIN_COLORS.get(t, GREY) for t in types])
    ax.invert_yaxis()
    for bar, n in zip(bars, nums):
        ax.text(bar.get_width() + max(nums) * 0.01,
                bar.get_y() + bar.get_height() / 2, f"{n} rows",
                va="center", fontsize=10, color=TEXT, fontweight="bold")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in JOIN_COLORS.values()]
    ax.legend(handles, [f"{k} JOIN" for k in JOIN_COLORS], frameon=False,
              loc="upper center", bbox_to_anchor=(0.5, -0.2),
              ncols=len(JOIN_COLORS))
    ax.set_xlim(0, max(nums) * 1.2)
    ax.set_xlabel("rows returned", fontsize=11, color=TEXT)
    _style(ax, title, grid_axis="x")
    fig.tight_layout()
    return fig
