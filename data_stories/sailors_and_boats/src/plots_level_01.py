"""Charts for notebooks/notebook_level_01.py -- the ten basic queries.

Same rule as src/plots.py: the notebook writes SQL and calls one function from
here per chart, so no plotting code sits inside a notebook. Every function takes
the DataFrame its query returned and gives back an Altair chart; nothing here
runs SQL or touches the database.

Styling comes from `plots.style()` and the palette constants next to it, so all
five chart modules in this project draw the same-looking charts.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from plots import (
    BAR_SIZE,
    BOAT_COLOUR_FILL,
    SERIES_1,
    SURFACE,
    TEXT_SECONDARY,
    count_axis,
    style,
)

# Level 1 is the first chart a student sees, so each one carries a direct
# label: the number is on the mark, not only on the axis.


# ---------------------------------------------------------------------------
# Q7 -- how many boats of each colour
# ---------------------------------------------------------------------------

def plot_boats_per_colour(df: pd.DataFrame) -> alt.Chart:
    """Bars: the size of each colour group in the fleet.

    Expects columns: color, n_boats, boats.

    Painting a "red" bar red is usually lazy, and here it is exactly right --
    the category *is* a colour. Two adjustments keep it honest: 'white' is
    nudged to a warm grey so the bar does not vanish into the surface, and
    every bar is labelled, so red and green (the classic colour-vision
    confusion) are never told apart by hue alone.
    """
    order = [c for c in BOAT_COLOUR_FILL if c in set(df["color"])]

    bars = (
        alt.Chart(df)
        .mark_bar(size=BAR_SIZE, cornerRadiusEnd=4, stroke=SURFACE, strokeWidth=2)
        .encode(
            x=alt.X("color:N", title="boat colour", sort=order,
                    axis=alt.Axis(labelAngle=0)),
            y=alt.Y("n_boats:Q", title="boats in the fleet",
                    axis=count_axis(df["n_boats"])),
            color=alt.Color(
                "color:N",
                sort=order,
                scale=alt.Scale(domain=order,
                                range=[BOAT_COLOUR_FILL[c] for c in order]),
                legend=None,          # the x-axis already names every colour
            ),
            tooltip=[
                alt.Tooltip("color:N", title="colour"),
                alt.Tooltip("n_boats:Q", title="boats"),
                alt.Tooltip("boats:N", title="which"),
            ],
        )
    )
    labels = bars.mark_text(dy=-8, fontSize=11, color=TEXT_SECONDARY).encode(
        text="n_boats:Q", color=alt.value(TEXT_SECONDARY)
    )
    return style(
        (bars + labels).properties(height=260),
        "Boats per colour",
        "Nine hulls, six colours -- the counts a GROUP BY returns",
    )


# ---------------------------------------------------------------------------
# Q9 -- the crew, oldest first
# ---------------------------------------------------------------------------

def plot_crew_by_age(df: pd.DataFrame) -> alt.Chart:
    """Horizontal bars: every sailor's age, tallest first.

    Expects columns: sid, sname, age, rating.

    Horizontal because the labels are names, and names are text. Two sailors
    are called Horatio, so the bar label carries the sid too -- `sname` alone
    would draw two bars that look like a mistake.
    """
    d = df.copy()
    d["label"] = d["sname"] + " (" + d["sid"].astype(str) + ")"

    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE, cornerRadiusEnd=4, color=SERIES_1)
        .encode(
            y=alt.Y("label:N", sort="-x", title=None),
            x=alt.X("age:Q", title="age"),
            tooltip=[
                alt.Tooltip("sname:N", title="sailor"),
                alt.Tooltip("sid:Q", title="sid"),
                alt.Tooltip("age:Q", title="age"),
                alt.Tooltip("rating:Q", title="rating"),
            ],
        )
    )
    labels = bars.mark_text(align="left", dx=6, fontSize=11,
                            color=TEXT_SECONDARY).encode(text="age:Q")
    return style(
        (bars + labels).properties(height=alt.Step(24)),
        "The crew, oldest first",
        "ORDER BY age DESC -- the same rows, arranged so the answer is visible",
    )


# ---------------------------------------------------------------------------
# Q10 -- the season at a glance
# ---------------------------------------------------------------------------

def plot_season_strip(df: pd.DataFrame) -> alt.Chart:
    """One dot per reservation: which boat went out, on which day, held by whom.

    Expects columns: day (date), bid, sid -- the three columns `reserves`
    actually stores, and nothing else.

    The rows the query returned, placed on a time axis -- a `BETWEEN` window is
    a slice of a timeline, so it is worth seeing as one. Gaps between dots are
    days nobody sailed; those days exist in the calendar but not in the table,
    which is the point Level 4 picks up with a calendar spine.

    Every mark is labelled with a bare `sid`, because that is genuinely all
    this table knows. Level 2 joins `sailors` and the numbers turn into names.

    `sailors_db.q` hands back `datetime.date` so tables print YYYY-MM-DD, and
    Vega cannot serialise a `date` -- marimo renders nothing and reports
    "Object of type date is not JSON serializable". Coerce for the chart only.
    """
    d = df.copy()
    d["day"] = pd.to_datetime(d["day"])
    d["boat_label"] = "boat " + d["bid"].astype(str)
    d["sailor_label"] = "sailor " + d["sid"].astype(str)

    dots = (
        alt.Chart(d)
        .mark_circle(size=170, color=SERIES_1, opacity=1,
                     stroke=SURFACE, strokeWidth=2)
        .encode(
            x=alt.X("day:T", title="day",
                    axis=alt.Axis(format="%b %d",
                                  tickCount={"interval": "week", "step": 1})),
            y=alt.Y("boat_label:N", title=None, sort="ascending"),
            tooltip=[
                alt.Tooltip("day:T", title="day", format="%Y-%m-%d"),
                alt.Tooltip("bid:Q", title="bid"),
                alt.Tooltip("sid:Q", title="sid"),
            ],
        )
    )
    names = dots.mark_text(align="center", dy=-13, fontSize=10,
                           color=TEXT_SECONDARY).encode(text="sid:N")
    return style(
        (dots + names).properties(height=alt.Step(30)),
        "The season, boat by boat",
        "One dot per reservation, labelled with the sid -- names need a join",
    )
