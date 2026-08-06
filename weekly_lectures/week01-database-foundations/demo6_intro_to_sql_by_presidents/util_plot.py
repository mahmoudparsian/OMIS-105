"""
util_plot.py
============

All plotting logic for the *Introducing DuckDB by Presidents* notebook lives
here, fully decoupled from the notebook itself.  The notebook stays focused on
SQL; this module owns everything about how the results *look*.

Design goals
------------
* One consistent visual theme (seaborn whitegrid + a tuned matplotlib rcParams).
* Real, recognisable political-party colours so every chart reads at a glance.
* Every function takes a tidy ``pandas.DataFrame`` (exactly what
  ``con.execute(sql).df()`` returns in DuckDB) and returns a
  ``matplotlib.figure.Figure`` so the notebook can ``plt.show()`` or save it.
* No global state leaks: each function builds its own ``fig, ax``.

Usage from the notebook
-----------------------
    import util_plot as up
    fig = up.plot_presidents_per_party(party_counts_df)

Author: built for OMIS 105, Santa Clara University.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

# --------------------------------------------------------------------------- #
#  Theme & palette
# --------------------------------------------------------------------------- #

#: Recognisable colours for each U.S. political party in the data set.
PARTY_COLORS = {
    "Democratic":           "#2E5A9C",   # blue
    "Democratic-Republican": "#6BAED6",  # light blue
    "Republican":           "#C8312B",   # red
    "Whig":                 "#E0A22B",   # gold
    "Federalist":           "#3F7A3F",   # green
    "National Union":       "#7B5EA7",   # purple
    "Unaffiliated":         "#7F7F7F",   # grey
}

#: Fallback colour for any party not in the map above.
_DEFAULT_COLOR = "#4C4C4C"

#: A single accent colour for charts that are not party-segmented.
ACCENT = "#2E5A9C"


def set_theme() -> None:
    """Apply the shared visual theme.

    Call this once near the top of the notebook (the plotting functions also
    call it defensively, so charts look right even if you forget).
    """
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update(
        {
            "figure.dpi": 110,
            "savefig.dpi": 110,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.titlesize": 15,
            "axes.titleweight": "bold",
            "axes.titlepad": 14,
            "axes.labelsize": 11.5,
            "axes.labelweight": "medium",
            "axes.edgecolor": "#444444",
            "axes.linewidth": 0.9,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.frameon": False,
            "font.family": "sans-serif",
        }
    )


def _colors_for(party_names) -> list[str]:
    """Map an iterable of party names to their brand colours."""
    return [PARTY_COLORS.get(name, _DEFAULT_COLOR) for name in party_names]


def _style_axes(ax) -> None:
    """Strip chart-junk: drop the top/right spines, lighten the grid."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="both", alpha=0.35, linewidth=0.7)


# --------------------------------------------------------------------------- #
#  4.x query visualisations
# --------------------------------------------------------------------------- #

def plot_presidents_per_party(df: pd.DataFrame,
                              party_col: str = "party_name",
                              count_col: str = "president_count"):
    """Horizontal bar chart: how many presidents each party produced.

    Parameters
    ----------
    df : DataFrame with one row per party.
    party_col, count_col : column names to read.
    """
    set_theme()
    data = df.sort_values(count_col, ascending=True)

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    bars = ax.barh(
        data[party_col], data[count_col],
        color=_colors_for(data[party_col]), edgecolor="white", linewidth=0.8,
    )
    ax.bar_label(bars, padding=4, fontsize=10, fontweight="bold",
                 color="#222222")

    ax.set_title("Presidents per Political Party")
    ax.set_xlabel("Number of presidents")
    ax.set_ylabel("")
    ax.margins(x=0.12)
    _style_axes(ax)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    return fig


def plot_term_length_distribution(df: pd.DataFrame,
                                  days_col: str = "term_days"):
    """Histogram + rug of every president's term length (in years).

    Converts days to years on the fly so the x-axis is human-readable.
    """
    set_theme()
    years = df[days_col] / 365.25

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    sns.histplot(years, bins=12, kde=True, color=ACCENT,
                 edgecolor="white", alpha=0.85, ax=ax)
    sns.rugplot(years, color="#C8312B", height=0.05, ax=ax)

    mean_years = years.mean()
    ax.axvline(mean_years, color="#C8312B", linestyle="--", linewidth=1.6,
               label=f"mean = {mean_years:.1f} yrs")

    ax.set_title("Distribution of Presidential Term Lengths")
    ax.set_xlabel("Years in office")
    ax.set_ylabel("Number of presidents")
    ax.legend(loc="upper right")
    _style_axes(ax)
    fig.tight_layout()
    return fig


def plot_term_timeline(df: pd.DataFrame,
                       start_col: str = "term_start",
                       end_col: str = "term_end",
                       name_col: str = "full_name",
                       party_col: str = "party_name",
                       seq_col: str = "sequence"):
    """Gantt-style timeline: one horizontal bar per presidency, party-coloured.

    Expects ``start_col``/``end_col`` to be parseable as datetimes.
    """
    set_theme()
    data = df.copy()
    data[start_col] = pd.to_datetime(data[start_col])
    data[end_col] = pd.to_datetime(data[end_col])
    data = data.sort_values(seq_col, ascending=False)  # #1 at top

    starts = data[start_col].map(lambda d: d.toordinal())
    widths = (data[end_col] - data[start_col]).dt.days
    y = range(len(data))

    fig, ax = plt.subplots(figsize=(9.5, 12))
    ax.barh(list(y), widths, left=starts,
            color=_colors_for(data[party_col]),
            edgecolor="white", linewidth=0.6)

    ax.set_yticks(list(y))
    ax.set_yticklabels(
        [f"{int(s):>2}. {n}" for s, n in zip(data[seq_col], data[name_col])],
        fontsize=8.5,
    )

    # Convert ordinal x-axis back to year labels.
    def _ord_to_year(x, _pos):
        try:
            return pd.Timestamp.fromordinal(int(x)).year
        except (ValueError, OverflowError):
            return ""
    ax.xaxis.set_major_locator(mticker.MultipleLocator(20 * 365.25))
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_ord_to_year))

    # Legend from the party colour map (only parties actually present).
    present = list(dict.fromkeys(data[party_col]))
    handles = [plt.Rectangle((0, 0), 1, 1,
               color=PARTY_COLORS.get(p, _DEFAULT_COLOR)) for p in present]
    ax.legend(handles, present, title="Party", loc="lower right",
              fontsize=9, title_fontsize=10)

    ax.set_title("Timeline of U.S. Presidencies")
    ax.set_xlabel("Year")
    ax.set_ylabel("")
    ax.margins(y=0.01)
    _style_axes(ax)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    return fig


def plot_avg_term_by_party(df: pd.DataFrame,
                           party_col: str = "party_name",
                           avg_days_col: str = "avg_days",
                           count_col: str = "president_count"):
    """Bar chart of average term length (years) per party.

    Annotates each bar with the number of presidents behind the average.
    """
    set_theme()
    data = df.copy()
    data["avg_years"] = data[avg_days_col] / 365.25
    data = data.sort_values("avg_years", ascending=False)

    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    bars = ax.bar(
        data[party_col], data["avg_years"],
        color=_colors_for(data[party_col]), edgecolor="white", linewidth=0.8,
    )
    for bar, n in zip(bars, data[count_col]):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                f"{bar.get_height():.1f} yr\n(n={int(n)})",
                ha="center", va="bottom", fontsize=9, color="#222222")

    ax.set_title("Average Term Length by Party")
    ax.set_xlabel("")
    ax.set_ylabel("Average years in office")
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data[party_col], rotation=25, ha="right")
    ax.margins(y=0.18)
    _style_axes(ax)
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    return fig


def plot_top_n_longest(df: pd.DataFrame,
                       name_col: str = "president",
                       days_col: str = "days_in_office",
                       party_col: str | None = "party_name"):
    """Horizontal bar chart of the Top-N longest-serving presidents.

    If ``party_col`` is present the bars are party-coloured; otherwise a single
    accent colour is used.
    """
    set_theme()
    data = df.sort_values(days_col, ascending=True)
    years = data[days_col] / 365.25

    if party_col and party_col in data.columns:
        colors = _colors_for(data[party_col])
    else:
        colors = ACCENT

    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    bars = ax.barh(data[name_col], years, color=colors,
                   edgecolor="white", linewidth=0.8)
    ax.bar_label(bars, labels=[f"{v:.1f} yr" for v in years],
                 padding=4, fontsize=9.5, fontweight="bold", color="#222222")

    ax.set_title(f"Top {len(data)} Longest-Serving Presidents")
    ax.set_xlabel("Years in office")
    ax.set_ylabel("")
    ax.margins(x=0.14)
    _style_axes(ax)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    return fig


def plot_cumulative_days(df: pd.DataFrame,
                         seq_col: str = "sequence",
                         cum_col: str = "cumulative_days",
                         name_col: str | None = "last_name"):
    """Area + line chart of cumulative days in office across the sequence."""
    set_theme()
    data = df.sort_values(seq_col)
    cum_years = data[cum_col] / 365.25

    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    ax.fill_between(data[seq_col], cum_years, color=ACCENT, alpha=0.18)
    ax.plot(data[seq_col], cum_years, color=ACCENT, linewidth=2.2,
            marker="o", markersize=3.5)

    ax.set_title("Cumulative Years Served Across the Presidency")
    ax.set_xlabel("President sequence number")
    ax.set_ylabel("Cumulative years in office")
    _style_axes(ax)
    fig.tight_layout()
    return fig


def plot_presidents_per_century(df: pd.DataFrame,
                                century_col: str = "century",
                                count_col: str = "presidents",
                                avg_days_col: str | None = "avg_days_in_office"):
    """Bar chart of presidents per century, optionally annotated with avg term."""
    set_theme()
    data = df.sort_values(century_col)

    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    bars = ax.bar(data[century_col], data[count_col],
                  color=ACCENT, edgecolor="white", linewidth=0.8)

    if avg_days_col and avg_days_col in data.columns:
        for bar, d in zip(bars, data[avg_days_col]):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.1,
                    f"{int(bar.get_height())}\navg {d/365.25:.1f} yr",
                    ha="center", va="bottom", fontsize=9, color="#222222")
    else:
        ax.bar_label(bars, padding=3, fontweight="bold")

    ax.set_title("Presidents per Century")
    ax.set_xlabel("")
    ax.set_ylabel("Number of presidents")
    ax.margins(y=0.18)
    _style_axes(ax)
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    return fig


def plot_term_vs_sequence(df: pd.DataFrame,
                          seq_col: str = "sequence",
                          days_col: str = "term_days",
                          party_col: str = "party_name"):
    """Scatter of term length (years) vs. sequence, coloured by party.

    A light LOWESS-free rolling mean shows the long-run trend without adding a
    statsmodels dependency.
    """
    set_theme()
    data = df.copy()
    data["years"] = data[days_col] / 365.25
    data = data.sort_values(seq_col)

    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    for party, grp in data.groupby(party_col):
        ax.scatter(grp[seq_col], grp["years"], s=70,
                   color=PARTY_COLORS.get(party, _DEFAULT_COLOR),
                   edgecolor="white", linewidth=0.8, label=party, zorder=3)

    trend = data["years"].rolling(window=5, center=True, min_periods=1).mean()
    ax.plot(data[seq_col], trend, color="#333333", linewidth=1.6,
            linestyle="--", alpha=0.7, label="5-term rolling mean", zorder=2)

    ax.set_title("Term Length Across History")
    ax.set_xlabel("President sequence number")
    ax.set_ylabel("Years in office")
    ax.legend(fontsize=8.5, ncol=2, loc="upper right")
    _style_axes(ax)
    fig.tight_layout()
    return fig
