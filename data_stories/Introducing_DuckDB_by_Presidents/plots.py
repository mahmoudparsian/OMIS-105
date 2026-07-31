"""
plots.py — Visualization helpers for the DuckDB notebook.

All functions accept a pandas DataFrame (from duckdb_relation.df())
and return a matplotlib Figure so the notebook can display them inline.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


# ── colour palette ────────────────────────────────────────────────────────────
PARTY_COLORS = {
    "Democratic": "#2166ac",
    "Republican": "#d6604d",
    "Whig": "#4dac26",
    "Federalist": "#8073ac",
    "Democratic-Republican": "#f1a340",
    "Unaffiliated": "#969696",
    "National Union": "#b2df8a",
}

DEFAULT_COLOR = "#5e9cc9"


def _party_color(party_name: str) -> str:
    return PARTY_COLORS.get(party_name, DEFAULT_COLOR)


# ── 1. Bar chart: number of presidents per party ──────────────────────────────
def plot_presidents_per_party(df) -> plt.Figure:
    """
    Parameters
    ----------
    df : DataFrame with columns [party_name, president_count]
    """
    df = df.sort_values("president_count", ascending=True)
    colors = [_party_color(p) for p in df["party_name"]]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(df["party_name"], df["president_count"], color=colors, edgecolor="white")
    ax.bar_label(bars, padding=4, fontsize=9)
    ax.set_xlabel("Number of Presidents", fontsize=11)
    ax.set_title("US Presidents by Political Party", fontsize=13, fontweight="bold")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


# ── 2. Histogram: days in office distribution ─────────────────────────────────
def plot_days_in_office_distribution(df) -> plt.Figure:
    """
    Parameters
    ----------
    df : DataFrame with columns [name, days_in_office]
    """
    days = df["days_in_office"].dropna()

    fig, ax = plt.subplots(figsize=(9, 5))
    n, bins, patches = ax.hist(days, bins=15, color=DEFAULT_COLOR, edgecolor="white", linewidth=0.8)

    # colour bars by rough quartile
    q25, q75 = np.percentile(days, [25, 75])
    for patch, left in zip(patches, bins[:-1]):
        if left < q25:
            patch.set_facecolor("#aec7e8")
        elif left > q75:
            patch.set_facecolor("#1f77b4")

    ax.axvline(days.mean(), color="crimson", linestyle="--", linewidth=1.4, label=f"Mean: {days.mean():.0f} days")
    ax.axvline(days.median(), color="darkorange", linestyle=":", linewidth=1.4, label=f"Median: {days.median():.0f} days")
    ax.legend(fontsize=9)
    ax.set_xlabel("Days in Office", fontsize=11)
    ax.set_ylabel("Number of Presidents", fontsize=11)
    ax.set_title("Distribution of Presidential Term Lengths", fontsize=13, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


# ── 3. Timeline: term start years over history ───────────────────────────────
def plot_term_timeline(df) -> plt.Figure:
    """
    Parameters
    ----------
    df : DataFrame with columns [sequence, last_name, term_start_year, party_name]
    """
    colors = [_party_color(p) for p in df["party_name"]]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.scatter(df["term_start_year"], df["sequence"], c=colors, s=60, zorder=3)

    # annotate a few notable presidents
    notable = {1: "Washington", 16: "Lincoln", 32: "FDR", 44: "Obama", 45: "Trump"}
    for _, row in df.iterrows():
        if row["sequence"] in notable:
            ax.annotate(
                row["last_name"],
                (row["term_start_year"], row["sequence"]),
                textcoords="offset points",
                xytext=(0, 7),
                ha="center",
                fontsize=7.5,
                color="dimgray",
            )

    # legend for parties present
    seen = {}
    for name, color in zip(df["party_name"], colors):
        if name not in seen:
            seen[name] = color
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=8, label=n)
               for n, c in seen.items()]
    ax.legend(handles=handles, fontsize=8, loc="upper left", framealpha=0.7)

    ax.set_xlabel("Year Term Started", fontsize=11)
    ax.set_ylabel("Presidency #", fontsize=11)
    ax.set_title("Presidential Terms Over US History", fontsize=13, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


# ── 4. Stacked bar: avg term length per party ────────────────────────────────
def plot_avg_term_by_party(df) -> plt.Figure:
    """
    Parameters
    ----------
    df : DataFrame with columns [party_name, avg_days, president_count]
    """
    df = df.sort_values("avg_days", ascending=False)
    colors = [_party_color(p) for p in df["party_name"]]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(df["party_name"], df["avg_days"], color=colors, edgecolor="white")
    ax.bar_label(bars, labels=[f"{v:.0f}d" for v in df["avg_days"]], padding=3, fontsize=8)

    ax.axhline(1461, color="gray", linestyle="--", linewidth=1, label="1 term (≈1461 days)")
    ax.axhline(2922, color="gray", linestyle=":",  linewidth=1, label="2 terms (≈2922 days)")
    ax.legend(fontsize=8)
    ax.set_ylabel("Avg Days in Office", fontsize=11)
    ax.set_title("Average Presidential Term Length by Party", fontsize=13, fontweight="bold")
    ax.tick_params(axis="x", rotation=30)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


# ── 5. Scatter: sequence vs days in office (coloured by century) ─────────────
def plot_sequence_vs_days(df) -> plt.Figure:
    """
    Parameters
    ----------
    df : DataFrame with columns [sequence, last_name, days_in_office, term_start_year]
    """
    def century_color(year):
        if year < 1800: return "#fdae61"
        if year < 1900: return "#abd9e9"
        if year < 2000: return "#2c7bb6"
        return "#d7191c"

    colors = [century_color(y) for y in df["term_start_year"]]

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.scatter(df["sequence"], df["days_in_office"], c=colors, s=70, edgecolors="white", linewidths=0.5, zorder=3)

    # trend line
    z = np.polyfit(df["sequence"], df["days_in_office"], 1)
    p = np.poly1d(z)
    xs = np.linspace(df["sequence"].min(), df["sequence"].max(), 200)
    ax.plot(xs, p(xs), color="gray", linestyle="--", linewidth=1.2, label="Trend")

    legend_items = [
        plt.Line2D([0],[0], marker="o", color="w", markerfacecolor=c, markersize=8, label=l)
        for c, l in [("#fdae61","1700s"), ("#abd9e9","1800s"), ("#2c7bb6","1900s"), ("#d7191c","2000s")]
    ]
    legend_items.append(plt.Line2D([0],[0], color="gray", linestyle="--", label="Trend"))
    ax.legend(handles=legend_items, fontsize=8)

    ax.set_xlabel("Presidency #", fontsize=11)
    ax.set_ylabel("Days in Office", fontsize=11)
    ax.set_title("Days in Office vs Presidential Sequence", fontsize=13, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig
