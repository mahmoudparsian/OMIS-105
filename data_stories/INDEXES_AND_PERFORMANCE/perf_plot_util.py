"""
perf_plot_util.py — display + plotting helpers for the Week 7 indexing notebook.

All presentation code lives here so the notebook itself stays SQL + explanation.

Exports
-------
    display_table(df, caption)      pretty-print a result set
    time_query(con, sql, reps)      median wall-clock time of a query, in ms
    plot_index_comparison(rows)     grouped bars: no-index vs indexed, per table size
    plot_speedup(rows)              how the speedup changes as the table grows
    plot_projection_cost(labels, ms) why column selection matters in a columnar DB

Colours come from a colour-vision-validated palette: the adjacent pairs clear the
CVD separation threshold, so the charts stay readable in greyscale and for
colourblind viewers.
"""

import statistics
import time

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

SLOW = "#eb6834"   # orange — the "before" bar
FAST = "#2a78d6"   # blue   — the "after" bar
ACCENT = "#1baf7a"  # aqua

plt.rcParams.update({
    "figure.figsize": (9, 5),
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK_SECONDARY,
    "axes.titlecolor": INK,
    "axes.titlesize": 13,
    "axes.titleweight": "600",
    "axes.titlelocation": "left",
    "axes.titlepad": 14,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": GRIDLINE,
    "grid.linewidth": 0.8,
    "text.color": INK,
    "xtick.color": INK_MUTED,
    "ytick.color": INK_MUTED,
    "legend.frameon": False,
})


# ── Display ──────────────────────────────────────────────────────────────────

def display_table(df, caption=""):
    """Print a DataFrame with a caption, the way the other OMIS-105 stories do."""
    if caption:
        print(f"\n{caption}")
        print("-" * max(len(caption), 40))
    print(df.to_string(index=False))
    print()
    return df


# ── Measurement ──────────────────────────────────────────────────────────────

def time_query(con, sql, reps=25):
    """
    Median wall-clock time of `sql`, in milliseconds.

    The median is used rather than the mean because one unlucky run — a garbage
    collection pause, another process waking up — would drag a mean around and
    invent a difference that is not really there. The first execution is thrown
    away so we are not also measuring one-off parsing and planning.
    """
    con.execute(sql).fetchall()                      # warm-up, discarded
    samples = []
    for _ in range(reps):
        start = time.perf_counter()
        con.execute(sql).fetchall()
        samples.append((time.perf_counter() - start) * 1000)
    return statistics.median(samples)


# ── Charts ───────────────────────────────────────────────────────────────────

def _style(ax, title, xlabel=None, ylabel=None):
    ax.set_title(title, color=INK)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, labelpad=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, labelpad=10)
    ax.grid(axis="y")
    ax.grid(axis="x", visible=False)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    return ax


def _label(ax, bars, values, fmt="{:.2f}"):
    span = max(values) if values else 1
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + span * 0.02,
                fmt.format(v), ha="center", va="bottom",
                fontsize=9, color=INK_SECONDARY)


def plot_index_comparison(rows):
    """
    Grouped bars comparing query time before and after CREATE INDEX.

    `rows` is a list of (n_rows, ms_without_index, ms_with_index).
    """
    labels = [f"{n:,}" for n, _, _ in rows]
    before = [b for _, b, _ in rows]
    after = [a for _, _, a in rows]
    x = range(len(rows))
    w = 0.38

    fig, ax = plt.subplots()
    b1 = ax.bar([i - w / 2 - 0.01 for i in x], before, width=w,
                color=SLOW, label="No index")
    b2 = ax.bar([i + w / 2 + 0.01 for i in x], after, width=w,
                color=FAST, label="With index")

    _style(ax, "Same query, same data — with and without an index",
           xlabel="Rows in table", ylabel="Query time (ms, median)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(before + after) * 1.18)
    _label(ax, b1, before)
    _label(ax, b2, after)
    ax.legend(loc="upper left")

    fig.tight_layout()
    return fig


def plot_speedup(rows):
    """Line showing how the index speedup changes with table size."""
    labels = [f"{n:,}" for n, _, _ in rows]
    speedup = [b / a if a else 1 for _, b, a in rows]

    fig, ax = plt.subplots()
    ax.plot(range(len(rows)), speedup, marker="o", markersize=9,
            linewidth=2, color=FAST)
    ax.axhline(1.0, color=BASELINE, linewidth=1.5, linestyle="--")
    ax.text(0, 1.0, "  no benefit", va="bottom", ha="left",
            fontsize=9, color=INK_MUTED)

    for i, s in enumerate(speedup):
        ax.annotate(f"{s:.1f}x", (i, s), textcoords="offset points",
                    xytext=(0, 11), ha="center",
                    fontsize=9, color=INK_SECONDARY)

    _style(ax, "The index helps more as the table grows — but not dramatically",
           xlabel="Rows in table", ylabel="Speedup (x times faster)")
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(speedup) * 1.35)

    fig.tight_layout()
    return fig


def plot_projection_cost(labels, times):
    """
    Bars showing the cost of reading columns you do not need.

    In a columnar database this is often a bigger lever than an index, which is
    the main point of the Week 7 notebook.
    """
    colors = [SLOW] + [FAST] * (len(labels) - 1)

    fig, ax = plt.subplots()
    bars = ax.bar(labels, times, width=0.6, color=colors)

    _style(ax, "Reading fewer columns is the columnar database's real speed-up",
           ylabel="Query time (ms, median)")
    ax.set_ylim(0, max(times) * 1.18)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:.0f}"))
    _label(ax, bars, times)

    fig.tight_layout()
    return fig
