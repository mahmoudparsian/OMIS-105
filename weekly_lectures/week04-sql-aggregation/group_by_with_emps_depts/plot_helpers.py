"""
plot_helpers.py
================
Plotting functions for the OMIS 105 notebook
"Learning GROUP BY with Employees & Departments" (notebook.py).

Students: You do NOT need to read or modify this file.
          It is imported by notebook.py to keep plotting code
          out of your way so you can focus on SQL.

Every function takes the DataFrame that a SQL cell returns (pandas
or polars — both work) and returns a matplotlib Figure. In Marimo,
make the function call the last line of a cell, and the chart shows.
A NULL label is shown as "(NULL)".

Colors follow the thing, not its position: department 10 is always
blue, "Engineer" is always blue, and so on, in every chart.

Functions
---------
  plot_group_map(df, item, group, title, ...)
        -- the idea of GROUP BY as a picture: every row on the left,
           one box per group on the right, a line from each row to
           its group
  plot_pie(df, labels, values, title, ...)
        -- donut chart; each slice shows its value and percent
  plot_range(df, labels, low, mid, high, title, ...)
        -- one line per group from MIN to MAX, with a dot at AVG
  plot_hbar(df, labels, values, title, ...)
        -- horizontal bar chart
  plot_before_after(df_all, df_kept, labels, before, after, title, ...)
        -- two bars per group: all rows vs. rows kept by WHERE
  plot_threshold_bars(df, labels, values, threshold, title, ...)
        -- bars with a dashed line; groups above it are "kept",
           groups below it are "dropped" (for HAVING)
  plot_stacked_bars(df, x, stack, values, title, ...)
        -- one bar per x value, split into colored pieces by `stack`
           (for GROUP BY on two columns)
  plot_heatmap(df, row_label, columns, title, ...)
        -- a table of numbers drawn as shaded cells (for a pivot)
  plot_bar(df, labels, values, title, ...)
        -- vertical bar chart; zero bars drawn as dashed outlines
"""

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import MaxNLocator

# -- Palette ----------------------------------------------------
# Categorical slots, in fixed order (validated for color-blind
# readers when used next to each other).
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
YELLOW = "#eda100"
SERIES = [BLUE, ORANGE, AQUA, YELLOW]

RED = "#c8553d"        # threshold lines only
GREY = "#c4c8cd"       # "dropped" / "filtered out"
GRID = "#e3e5e8"
TEXT = "#1f2933"
MUTED = "#6b7480"
SURFACE = "#ffffff"

# Fixed color for each entity, so a group keeps its color everywhere.
ENTITY_COLORS = {
    "10": BLUE, "Engineering": BLUE,
    "20": ORANGE, "Marketing": ORANGE,
    "30": AQUA, "Sales": AQUA,
    "40": YELLOW, "Finance": YELLOW,
    "50": "#8b6fd0", "IT": "#8b6fd0",
    "Engineer": BLUE,
    "Marketer": ORANGE,
    "Salesperson": AQUA,
    "VP": YELLOW,
}


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
        out.append(int(v) if v.is_integer() else round(v, 2))
    return out


def _colors(names):
    """The fixed color of each name; unknown names take the next
    free slot, in order."""
    out, spare = [], iter(SERIES * 4)
    for n in names:
        out.append(ENTITY_COLORS.get(n) or next(spare))
    return out


def _money(v):
    """70000 -> '$70K', 105714.29 -> '$105.7K'."""
    k = v / 1000
    return f"${k:,.0f}K" if float(k).is_integer() else f"${k:,.1f}K"


def _new_figure(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    return fig, ax


def _title(ax, title, subtitle=""):
    """Title (and an optional muted subtitle) at the figure's left
    edge, so long axis labels never push it off the page."""
    fig = ax.figure
    fig.suptitle(title, x=0.02, y=0.98, ha="left", va="top",
                 fontsize=14, fontweight="bold", color=TEXT)
    if subtitle:
        fig.text(0.02, 0.905, subtitle, ha="left", va="top",
                 fontsize=10.5, color=MUTED)


def _finish(fig, subtitle):
    fig.tight_layout(rect=(0, 0, 1, 0.86 if subtitle else 0.92))
    return fig


def _style(ax, grid_axis="y"):
    """Common look: no box, light dashed grid behind the data."""
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(GREY)
    ax.tick_params(colors=TEXT, labelsize=10.5, length=0)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, linestyle="--", linewidth=0.8)
        ax.set_axisbelow(True)


def _money_axis(axis):
    axis.set_major_formatter(lambda v, _pos: _money(v) if v else "0")


# -- GROUP BY as a picture --------------------------------------------
def plot_group_map(df, item, group, title, subtitle="", value=None,
                   group_prefix="", figsize=(8.5, 6.5)):
    """Every row of `df` is a dot on the left, labeled by `item`
    (plus `value`, if given). Every distinct value of `group` is a box
    on the right. A line runs from each row to its group, so you can
    see many rows collapse into one row per group."""
    items = _labels(df, item)
    groups = _labels(df, group)
    values = _nums(df, value) if value else None

    names = []
    for g in groups:
        if g not in names:
            names.append(g)
    members = {g: [i for i, x in enumerate(groups) if x == g] for g in names}
    colors = dict(zip(names, _colors(names)))

    n = len(items)
    row_y = {i: n - 1 - i for i in range(n)}
    # each group box sits at the middle of its own rows
    group_y = {g: sum(row_y[i] for i in members[g]) / len(members[g])
               for g in names}

    fig, ax = _new_figure(figsize)
    for i, g in enumerate(groups):
        ax.plot([0, 1], [row_y[i], group_y[g]], color=colors[g],
                linewidth=1.6, alpha=0.55, zorder=1)
        ax.scatter([0], [row_y[i]], s=70, color=colors[g], zorder=2,
                   edgecolor=SURFACE, linewidth=2)
        label = items[i]
        if values:
            label = f"{label}   {_money(values[i])}"
        ax.text(-0.05, row_y[i], label, ha="right", va="center",
                fontsize=10.5, color=TEXT)

    for g in names:
        y = group_y[g]
        box = FancyBboxPatch((1.02, y - 0.42), 0.9, 0.84,
                             boxstyle="round,pad=0.02,rounding_size=0.12",
                             facecolor=colors[g], edgecolor=SURFACE,
                             linewidth=2, zorder=2)
        ax.add_patch(box)
        ax.text(1.47, y, f"{group_prefix}{g}", ha="center", va="center",
                fontsize=11, color="white", fontweight="bold", zorder=3)
        count = len(members[g])
        ax.text(1.98, y, f"{count} row{'s' if count != 1 else ''} → 1 row",
                ha="left", va="center", fontsize=10.5, color=MUTED)

    ax.text(-0.05, n - 0.1, f"{n} rows (before)", ha="right",
            fontsize=11.5, color=MUTED, fontweight="bold")
    ax.text(1.47, n - 0.1, f"{len(names)} groups (after)", ha="center",
            fontsize=11.5, color=MUTED, fontweight="bold")
    ax.set_xlim(-1.25, 2.85)
    ax.set_ylim(-0.8, n + 0.4)
    ax.axis("off")
    _title(ax, title, subtitle)
    return _finish(fig, subtitle)


# -- Donut chart ------------------------------------------------------
def plot_pie(df, labels, values, title, subtitle="", label_prefix="",
             money=False, center_text="", figsize=(7, 5.2)):
    """One slice per row, in the DataFrame's row order. Each slice
    shows its value and its percent of the total. `label_prefix` is put
    in front of each label (e.g. 'dept '). `center_text` is written in
    the hole (e.g. '13 employees')."""
    names = _labels(df, labels)
    nums = _nums(df, values)
    total = sum(nums)

    def _fmt(pct):
        v = pct * total / 100
        shown = _money(v) if money else f"{round(v):,}"
        return f"{shown}\n{pct:.0f}%"

    fig, ax = _new_figure(figsize)
    _wedges, texts, autotexts = ax.pie(
        nums, labels=[f"{label_prefix}{n}" for n in names],
        colors=_colors(names), startangle=90, counterclock=False,
        wedgeprops=dict(edgecolor=SURFACE, linewidth=2.5, width=0.45),
        autopct=_fmt, pctdistance=0.775, labeldistance=1.08)
    for t in texts:
        t.set_fontsize(11.5)
        t.set_color(TEXT)
        t.set_fontweight("bold")
    for t in autotexts:
        t.set_fontsize(10)
        t.set_color("white")
        t.set_fontweight("bold")
    if center_text:
        ax.text(0, 0, center_text, ha="center", va="center", fontsize=13,
                color=TEXT, fontweight="bold")
    ax.axis("equal")
    _title(ax, title, subtitle)
    return _finish(fig, subtitle)


# -- MIN / AVG / MAX range --------------------------------------------
def plot_range(df, labels, low, mid, high, title, subtitle="",
               label_prefix="", figsize=(8.5, 4.2)):
    """One horizontal line per group from `low` (MIN) to `high` (MAX),
    with a large dot at `mid` (AVG). A group with one value is a dot."""
    names = _labels(df, labels)
    lows, mids, highs = _nums(df, low), _nums(df, mid), _nums(df, high)
    colors = _colors(names)

    fig, ax = _new_figure(figsize)
    for i, (lo, md, hi, c) in enumerate(zip(lows, mids, highs, colors)):
        ax.plot([lo, hi], [i, i], color=c, linewidth=5,
                solid_capstyle="round", alpha=0.35, zorder=1)
        ax.scatter([lo, hi], [i, i], s=60, color=c, zorder=2,
                   edgecolor=SURFACE, linewidth=2)
        ax.scatter([md], [i], s=190, color=c, zorder=3, marker="D",
                   edgecolor=SURFACE, linewidth=2)
        ax.text(lo, i - 0.3, f"MIN {_money(lo)}", ha="center", va="top",
                fontsize=9.5, color=MUTED)
        ax.text(hi, i - 0.3, f"MAX {_money(hi)}", ha="center", va="top",
                fontsize=9.5, color=MUTED)
        ax.text(md, i + 0.26, f"AVG {_money(md)}", ha="center",
                va="bottom", fontsize=10, color=TEXT, fontweight="bold")
    ax.set_yticks(range(len(names)), [f"{label_prefix}{n}" for n in names])
    ax.invert_yaxis()
    span = max(highs) - min(lows)
    ax.set_xlim(min(lows) - span * 0.12, max(highs) + span * 0.12)
    ax.set_ylim(len(names) - 0.4, -0.75)
    _money_axis(ax.xaxis)
    ax.set_xlabel("salary", fontsize=11, color=TEXT)
    _style(ax, grid_axis="x")
    _title(ax, title, subtitle)
    return _finish(fig, subtitle)


# -- Horizontal bar chart ---------------------------------------------
def plot_hbar(df, labels, values, title, subtitle="", xlabel="",
              money=False, reference=None, reference_label="",
              figsize=(8.5, 4.2)):
    """Bars top-to-bottom in the DataFrame's row order, each in its
    entity's color. `reference` (optional) draws a dashed vertical line,
    e.g. the company-wide average."""
    names = _labels(df, labels)
    nums = _nums(df, values)
    right = max(nums + [reference or 0]) * 1.18

    fig, ax = _new_figure(figsize)
    bars = ax.barh(names, nums, color=_colors(names), height=0.62,
                   edgecolor=SURFACE, linewidth=2)
    ax.invert_yaxis()
    for bar, num in zip(bars, nums):
        ax.text(bar.get_width() + right * 0.01,
                bar.get_y() + bar.get_height() / 2,
                _money(num) if money else f"{num:,}",
                va="center", fontsize=10.5, color=TEXT, fontweight="bold")
    if reference is not None:
        ax.axvline(reference, color=MUTED, linestyle="--", linewidth=1.3)
        ax.text(reference, -0.62, f"{reference_label}: {_money(reference)}",
                ha="center", va="center", fontsize=10, color=MUTED,
                bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.5))
        ax.set_ylim(len(names) - 0.5, -0.85)
    ax.set_xlim(0, right)
    if money:
        _money_axis(ax.xaxis)
    else:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel(xlabel, fontsize=11, color=TEXT)
    _style(ax, grid_axis="x")
    _title(ax, title, subtitle)
    return _finish(fig, subtitle)


# -- WHERE: all rows vs. kept rows ------------------------------------
def plot_before_after(df_all, df_kept, labels, before, after, title,
                      subtitle="", before_label="all rows",
                      after_label="kept by WHERE", label_prefix="",
                      figsize=(8.5, 4.5)):
    """Two bars per group: a dashed outline bar for `before` (taken from
    `df_all`, the count of every row) and a solid bar for `after` (taken
    from `df_kept`, the count of the rows that passed WHERE). A group
    missing from `df_kept` lost all its rows: its solid bar is 0."""
    names = _labels(df_all, labels)
    befores = _nums(df_all, before)
    kept = dict(zip(_labels(df_kept, labels), _nums(df_kept, after)))
    afters = [kept.get(n, 0) for n in names]
    colors = _colors(names)
    top = max(befores) * 1.2

    fig, ax = _new_figure(figsize)
    w = 0.36
    for i, (b, a, c) in enumerate(zip(befores, afters, colors)):
        ax.bar(i - w / 2 - 0.02, b, width=w, color="white", edgecolor=c,
               linewidth=1.8, linestyle="--")
        ax.text(i - w / 2 - 0.02, b + top * 0.02, f"{b}", ha="center",
                fontsize=10.5, color=MUTED)
        ax.bar(i + w / 2 + 0.02, a, width=w, color=c)
        ax.text(i + w / 2 + 0.02, a + top * 0.02, f"{a}", ha="center",
                fontsize=11, color=TEXT, fontweight="bold")
    ax.set_xticks(range(len(names)), [f"{label_prefix}{n}" for n in names])
    ax.set_ylim(0, top)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylabel("employees", fontsize=11, color=TEXT)
    handles = [plt.Rectangle((0, 0), 1, 1, facecolor="white",
                             edgecolor=MUTED, linestyle="--"),
               plt.Rectangle((0, 0), 1, 1, color=MUTED)]
    ax.legend(handles, [before_label, after_label], frameon=False,
              loc="upper right", fontsize=10)
    _style(ax, grid_axis="y")
    _title(ax, title, subtitle)
    return _finish(fig, subtitle)


# -- Bars with a threshold line (HAVING) ------------------------------
def plot_threshold_bars(df, labels, values, threshold, title, subtitle="",
                        ylabel="", money=False, figsize=(8.5, 4.5)):
    """Bars above `threshold` keep their color ('kept'); bars at or
    below it are grey ('dropped'). A dashed line marks the threshold."""
    names = _labels(df, labels)
    nums = _nums(df, values)
    colors = _colors(names)
    top = max(nums + [threshold])
    fmt = _money if money else (lambda v: f"{v:,}")

    fig, ax = _new_figure(figsize)
    for i, (num, c) in enumerate(zip(nums, colors)):
        kept = num > threshold
        ink = "white" if kept else TEXT
        ax.bar(i, num, width=0.6, color=c if kept else GREY)
        ax.text(i, num / 2, fmt(num), ha="center", va="center",
                fontsize=12, fontweight="bold", color=ink)
        ax.text(i, top * 0.06, "kept" if kept else "dropped", ha="center",
                va="bottom", fontsize=10.5, fontweight="bold", color=ink)
    ax.axhline(threshold, color=RED, linestyle="--", linewidth=1.5,
               zorder=3)
    ax.text(len(names) - 0.6, threshold + top * 0.02,
            f"HAVING … > {fmt(threshold)}", ha="center", va="bottom",
            fontsize=10, color=RED, fontweight="bold",
            bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.5))
    ax.set_xlim(-0.5, len(names) - 0.1)
    ax.set_xticks(range(len(names)), names)
    ax.set_ylim(0, top * 1.08)
    ax.set_ylabel(ylabel, fontsize=11, color=TEXT)
    if money:
        _money_axis(ax.yaxis)
    _style(ax, grid_axis="y")
    _title(ax, title, subtitle)
    return _finish(fig, subtitle)


# -- Stacked bars (GROUP BY two columns) ------------------------------
def plot_stacked_bars(df, x, stack, values, title, subtitle="", ylabel="",
                      label_prefix="", figsize=(8.5, 4.8)):
    """`df` has one row per (x, stack) pair — exactly what
    GROUP BY x, stack returns. Draws one bar per x value, split into
    one colored piece per stack value."""
    xs, stacks, nums = _labels(df, x), _labels(df, stack), _nums(df, values)
    x_names = list(dict.fromkeys(xs))
    s_names = sorted(dict.fromkeys(stacks))
    colors = dict(zip(s_names, _colors(s_names)))
    cell = {(a, b): v for a, b, v in zip(xs, stacks, nums)}

    fig, ax = _new_figure(figsize)
    bottoms = [0] * len(x_names)
    for s in s_names:
        heights = [cell.get((a, s), 0) for a in x_names]
        ax.bar(range(len(x_names)), heights, bottom=bottoms, width=0.58,
               color=colors[s], edgecolor=SURFACE, linewidth=2, label=s)
        for i, h in enumerate(heights):
            if h:
                ax.text(i, bottoms[i] + h / 2, f"{s}: {h}", ha="center",
                        va="center", fontsize=9.5, color="white",
                        fontweight="bold")
        bottoms = [b + h for b, h in zip(bottoms, heights)]
    for i, total in enumerate(bottoms):
        ax.text(i, total + max(bottoms) * 0.02, f"total {total}",
                ha="center", fontsize=10.5, color=TEXT, fontweight="bold")
    ax.set_xticks(range(len(x_names)),
                  [f"{label_prefix}{n}" for n in x_names])
    ax.set_ylim(0, max(bottoms) * 1.15)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylabel(ylabel, fontsize=11, color=TEXT)
    ax.legend(frameon=False, loc="upper right", fontsize=10)
    _style(ax, grid_axis="y")
    _title(ax, title, subtitle)
    return _finish(fig, subtitle)


# -- Heatmap (pivot table) --------------------------------------------
def plot_heatmap(df, row_label, columns, title, subtitle="",
                 label_prefix="", money=True, figsize=(8.5, 3.8)):
    """Draw the numeric `columns` of `df` as a grid of shaded cells,
    one row per row of `df`. Darker = bigger. A 0 or NULL cell is
    left white and shows '—'."""
    rows = _labels(df, row_label)
    grid = [_nums(df, c) for c in columns]          # one list per column
    data = [[grid[j][i] for j in range(len(columns))]
            for i in range(len(rows))]
    top = max(max(r) for r in data) or 1
    cmap = LinearSegmentedColormap.from_list("blues",
                                             ["#eaf2fc", "#2a78d6", "#123f75"])

    fig, ax = _new_figure(figsize)
    for i, r in enumerate(data):
        for j, v in enumerate(r):
            shade = cmap(v / top) if v else SURFACE
            ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=shade,
                                       edgecolor=SURFACE, linewidth=3))
            if v:
                text = _money(v) if money else f"{v:,}"
                ink = "white" if v / top > 0.45 else TEXT
            else:
                text, ink = "—", MUTED
            ax.text(j + 0.5, i + 0.5, text, ha="center", va="center",
                    fontsize=11, color=ink, fontweight="bold")
    ax.set_xlim(0, len(columns))
    ax.set_ylim(len(rows), 0)
    ax.set_xticks([j + 0.5 for j in range(len(columns))], columns)
    ax.set_yticks([i + 0.5 for i in range(len(rows))],
                  [f"{label_prefix}{n}" for n in rows])
    ax.xaxis.tick_top()
    ax.tick_params(colors=TEXT, labelsize=10.5, length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    _title(ax, title, subtitle)
    return _finish(fig, subtitle)


# -- Vertical bar chart (zeros shown as outlines) ---------------------
def plot_bar(df, labels, values, title, subtitle="", ylabel="",
             figsize=(8.5, 4.5)):
    """Each bar in its entity's color. A value of 0 is drawn as a
    dashed outline labeled '0 — none', so rows kept by a LEFT JOIN
    stay visible on the chart."""
    names = _labels(df, labels)
    nums = _nums(df, values)
    colors = _colors(names)
    top = max(nums) if max(nums) > 0 else 1
    stub = top * 0.04

    fig, ax = _new_figure(figsize)
    for i, (num, c) in enumerate(zip(nums, colors)):
        if num == 0:
            ax.bar(i, stub, color="white", edgecolor=MUTED,
                   linestyle="--", linewidth=1.5, width=0.6)
            ax.text(i, stub + top * 0.02, "0 — none", ha="center",
                    fontsize=10.5, color=MUTED, style="italic")
        else:
            ax.bar(i, num, color=c, width=0.6)
            ax.text(i, num + top * 0.02, f"{num:,}", ha="center",
                    fontsize=11, color=TEXT, fontweight="bold")
    ax.set_xticks(range(len(names)), names)
    ax.set_ylim(0, top * 1.18)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylabel(ylabel, fontsize=11, color=TEXT)
    _style(ax, grid_axis="y")
    _title(ax, title, subtitle)
    return _finish(fig, subtitle)
