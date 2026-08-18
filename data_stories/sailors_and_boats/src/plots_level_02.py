"""Charts for notebooks/notebook_level_02.py -- the ten intermediate queries.

As everywhere in this project, the notebook writes SQL and calls one function
from here per chart. Styling comes from `plots.style()` so every chart in the
project looks like part of one set.

Level 2 is where two categories start appearing in a single chart (voted /
too young, booked / never booked). Wherever that happens the rule is the same:
a legend is present *and* the bars carry direct labels, so nothing is
identified by colour alone.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from plots import (
    BAR_SIZE,
    SERIES_1,
    SERIES_2,
    SURFACE,
    TEXT_SECONDARY,
    count_axis,
    style,
)


# ---------------------------------------------------------------------------
# Q1 -- who sails at all
# ---------------------------------------------------------------------------

def plot_who_sails(df: pd.DataFrame) -> alt.Chart:
    """Pie: the crew split into those who have booked a boat and those who haven't.

    Expects columns: status, n_sailors, who.

    A pie is defensible here for the same reason it rarely is elsewhere: two
    slices, and they are parts of one whole -- every sailor is in exactly one
    of them, so the circle really is the crew.
    """
    d = df.copy()
    # Share of the crew, worked out here rather than in SQL: a window function
    # is a Level 4 idea, and the query this chart belongs to is the second one
    # a student meets. The slice label carries the count and the percentage,
    # the legend carries the name -- spelling the status out on the slice too
    # makes the label wider than the pie.
    d["pct"] = (100 * d["n_sailors"] / d["n_sailors"].sum()).round(0).astype(int)
    d["label"] = d["n_sailors"].astype(str) + " (" + d["pct"].astype(str) + "%)"

    order = ["has reserved a boat", "never reserved a boat"]
    base = alt.Chart(d).encode(
        theta=alt.Theta("n_sailors:Q", stack=True),
        color=alt.Color(
            "status:N",
            title=None,
            sort=order,
            scale=alt.Scale(domain=order, range=[SERIES_1, SERIES_2]),
            legend=alt.Legend(orient="right", symbolType="square"),
        ),
        order=alt.Order("n_sailors:Q", sort="descending"),
        tooltip=[
            alt.Tooltip("status:N", title="status"),
            alt.Tooltip("n_sailors:Q", title="sailors"),
            alt.Tooltip("pct:Q", title="share of the crew", format=".0f"),
            alt.Tooltip("who:N", title="who"),
        ],
    )
    wedges = base.mark_arc(outerRadius=98, stroke=SURFACE, strokeWidth=2)
    # `color=alt.value(...)` overrides the inherited encoding: without it each
    # label would be drawn in its own slice's fill.
    labels = base.mark_text(radius=120, fontSize=12).encode(
        text="label:N", color=alt.value(TEXT_SECONDARY)
    )
    return style(
        (wedges + labels).properties(height=300),
        "Who has ever reserved a boat?",
        "Ten of the fourteen sailors are in the database but not in reserves",
    )


# ---------------------------------------------------------------------------
# Q3 -- sailors with two or more boats
# ---------------------------------------------------------------------------

def plot_boats_per_sailor(df: pd.DataFrame) -> alt.Chart:
    """Horizontal bars: how many *different* boats each sailor has taken out.

    Expects columns: sid, sname, n_boats, n_reservations.

    Only the sailors the HAVING clause kept are in the frame, so the chart is
    the answer rather than a picture the answer was cut from.
    """
    d = df.copy()
    d["label"] = d["sname"] + " (" + d["sid"].astype(str) + ")"

    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE, cornerRadiusEnd=4, color=SERIES_1)
        .encode(
            y=alt.Y("label:N", sort="-x", title=None),
            x=alt.X("n_boats:Q", title="different boats reserved",
                    axis=count_axis(d["n_boats"])),
            tooltip=[
                alt.Tooltip("sname:N", title="sailor"),
                alt.Tooltip("sid:Q", title="sid"),
                alt.Tooltip("n_boats:Q", title="different boats"),
                alt.Tooltip("n_reservations:Q", title="reservations"),
            ],
        )
    )
    labels = bars.mark_text(align="left", dx=6, fontSize=11,
                            color=TEXT_SECONDARY).encode(text="n_boats:Q")
    return style(
        (bars + labels).properties(height=alt.Step(30)),
        "Sailors who have reserved at least two boats",
        "COUNT(DISTINCT bid) -- the same boat twice does not count twice",
    )


# ---------------------------------------------------------------------------
# Q5 -- the rating distribution, with the top rating picked out
# ---------------------------------------------------------------------------

def plot_rating_distribution(df: pd.DataFrame) -> alt.Chart:
    """Bars: how many sailors hold each rating, with the maximum highlighted.

    Expects columns: rating, n_sailors, who, is_top_rating.

    The highlight is what makes this the answer to "who is rated highest?" --
    and the bar being two units tall is what makes the tie visible. A query
    written as `ORDER BY rating DESC LIMIT 1` would have hidden it.
    """
    d = df.copy()
    d["highlight"] = d["is_top_rating"].map(
        {True: "the highest rating", False: "everyone else"}
    )

    order = ["the highest rating", "everyone else"]
    # The y encoding is spelled out once and reused by every layer. Layering a
    # text mark that inherits `y` without its axis lets Vega-Lite resolve the
    # shared axis from the wrong layer, and "sailors" picks up half-unit ticks.
    x = alt.X("rating:O", title="rating (1 = novice, 10 = expert)",
              axis=alt.Axis(labelAngle=0))
    y = alt.Y("n_sailors:Q", title="sailors",
              axis=count_axis(d["n_sailors"]))

    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE, cornerRadiusEnd=4)
        .encode(
            x=x,
            y=y,
            color=alt.Color(
                "highlight:N",
                title=None,
                sort=order,
                scale=alt.Scale(domain=order, range=[SERIES_2, SERIES_1]),
                # Above the plot area, not inside it: at "top-left" the legend
                # text crosses the bar at rating 3.
                legend=alt.Legend(orient="top", direction="horizontal",
                                  symbolType="square"),
            ),
            tooltip=[
                alt.Tooltip("rating:O", title="rating"),
                alt.Tooltip("n_sailors:Q", title="sailors"),
                alt.Tooltip("who:N", title="who"),
            ],
        )
    )
    counts = (
        alt.Chart(d)
        .mark_text(dy=-8, fontSize=11, color=TEXT_SECONDARY)
        .encode(x=x, y=y, text="n_sailors:Q")
    )
    # Names only on the bar that answers the question. Labelling all nine bars
    # collides at ratings 7 and 8, and the other names are in the tooltip and
    # the table anyway.
    winners = (
        alt.Chart(d[d["is_top_rating"]])
        .mark_text(dy=-24, dx=10, align="right", fontSize=11,
                   color=SERIES_2, fontWeight="bold")
        .encode(x=x, y=y, text="who:N")
    )
    return style(
        (bars + counts + winners).properties(height=300),
        "Sailors at each rating, and who is rated highest",
        "Two sailors tie at 10 -- the answer is a group, not a row",
    )


# ---------------------------------------------------------------------------
# Q8 -- old enough to vote, by rating
# ---------------------------------------------------------------------------

def plot_voting_by_rating(df: pd.DataFrame) -> alt.Chart:
    """Stacked bars: eligible and ineligible voters at each rating level.

    Expects columns: rating, n_sailors, n_can_vote, n_too_young.

    Two counts that sum to the group total, so they stack: the bar height is
    still "sailors at this rating" and the split says how many can vote. The
    frame arrives wide (one column per count) and Vega wants it long, so it is
    reshaped here -- reshaping for a chart is presentation, and belongs on this
    side of the line.
    """
    d = df.melt(
        id_vars=["rating", "n_sailors"],
        value_vars=["n_can_vote", "n_too_young"],
        var_name="group",
        value_name="sailors",
    )
    d["group"] = d["group"].map(
        {"n_can_vote": "old enough to vote", "n_too_young": "under 18"}
    )
    d = d[d["sailors"] > 0]

    order = ["old enough to vote", "under 18"]
    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE, cornerRadiusEnd=4, stroke=SURFACE, strokeWidth=2)
        .encode(
            x=alt.X("rating:O", title="rating",
                    axis=alt.Axis(labelAngle=0)),
            y=alt.Y("sailors:Q", title="sailors",
                    axis=count_axis(df["n_sailors"])),
            color=alt.Color(
                "group:N",
                title=None,
                sort=order,
                scale=alt.Scale(domain=order, range=[SERIES_1, SERIES_2]),
                legend=alt.Legend(orient="top", direction="horizontal",
                                  symbolType="square"),
            ),
            order=alt.Order("group:N"),
            tooltip=[
                alt.Tooltip("rating:O", title="rating"),
                alt.Tooltip("group:N", title="group"),
                alt.Tooltip("sailors:Q", title="sailors"),
                alt.Tooltip("n_sailors:Q", title="sailors at this rating"),
            ],
        )
    )
    return style(
        bars.properties(height=300),
        "Sailors old enough to vote, by rating level",
        "One sailor is under 18 -- Zorba, rated 10, aged 16",
    )


# ---------------------------------------------------------------------------
# Q10 -- bookings per boat, including the boats with none
# ---------------------------------------------------------------------------

def plot_bookings_per_boat(df: pd.DataFrame) -> alt.Chart:
    """Horizontal bars: every hull, with the never-booked ones picked out.

    Expects columns: bid, bname, color, n_reservations, never_reserved.

    The zeros are the finding, so they are drawn -- a bar of length zero is
    still a labelled row on the axis. This is what the LEFT JOIN bought; an
    INNER JOIN would have deleted five boats from the chart.
    """
    d = df.copy()
    d["label"] = d["bid"].astype(str) + "  " + d["bname"] + " (" + d["color"] + ")"
    d["status"] = d["never_reserved"].map(
        {True: "never reserved", False: "has been reserved"}
    )

    order = ["has been reserved", "never reserved"]
    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE, cornerRadiusEnd=4)
        .encode(
            y=alt.Y("label:N", sort=alt.SortField("n_reservations", "descending"),
                    title=None),
            x=alt.X("n_reservations:Q", title="reservations",
                    axis=count_axis(d["n_reservations"])),
            color=alt.Color(
                "status:N",
                title=None,
                sort=order,
                scale=alt.Scale(domain=order, range=[SERIES_1, SERIES_2]),
                legend=alt.Legend(orient="bottom-right", symbolType="square"),
            ),
            tooltip=[
                alt.Tooltip("label:N", title="boat"),
                alt.Tooltip("n_reservations:Q", title="reservations"),
                alt.Tooltip("status:N", title="status"),
            ],
        )
    )
    labels = bars.mark_text(align="left", dx=6, fontSize=11).encode(
        text="n_reservations:Q", color=alt.value(TEXT_SECONDARY)
    )
    # A bar of length zero is nothing at all, which would leave "never
    # reserved" in the legend with no mark to point at. The dot sits on the
    # axis and says "this row exists, and its value is none".
    zeros = (
        alt.Chart(d[d["never_reserved"]])
        .mark_circle(size=90, color=SERIES_2, opacity=1)
        .encode(y=alt.Y("label:N", sort=alt.SortField("n_reservations", "descending"),
                        title=None),
                x=alt.X("n_reservations:Q"))
    )
    return style(
        (bars + zeros + labels).properties(height=alt.Step(26)),
        "Reservations per boat -- zeros included",
        "Five hulls have never left the dock; an INNER JOIN would hide them",
    )
