"""Charts for notebooks/notebook_level_03.py -- the ten intermediate+ queries.

The notebook writes SQL and calls one function from here per chart; styling
comes from `plots.style()`.

Level 3 is where a chart stops illustrating the answer and starts *being* the
argument. The top-three and bottom-three charts draw the whole crew rather than
the three rows a `LIMIT` would have kept, because the interesting part -- a
ten-way tie at the bottom -- is exactly what `LIMIT` throws away.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from plots import (
    BAR_SIZE,
    BOAT_COLOUR_FILL,
    SERIES_1,
    SERIES_2,
    STEM,
    SURFACE,
    TEXT_SECONDARY,
    count_axis,
    style,
)


def _sailor_label(df: pd.DataFrame) -> pd.Series:
    """'Horatio (64)' -- two sailors share the name Horatio, so sid disambiguates."""
    return df["sname"] + " (" + df["sid"].astype(str) + ")"


# ---------------------------------------------------------------------------
# Q3 -- the busiest three sailors, against everybody else
# ---------------------------------------------------------------------------

def plot_top_sailors(df: pd.DataFrame) -> alt.Chart:
    """Horizontal bars: reservations per sailor, top three highlighted.

    Expects columns: sid, sname, n_reservations, n_boats, rank_from_top,
    in_top_3.

    Drawing all fourteen sailors is the point: `LIMIT 3` answers the question
    but shows nothing about the gap between third place and fourth. Here the
    highlight is the answer and the rest of the bars are the context it came
    from.
    """
    d = df.copy()
    d["label"] = _sailor_label(d)
    d["band"] = d["in_top_3"].map({True: "top three", False: "the rest of the crew"})

    order = ["top three", "the rest of the crew"]
    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE, cornerRadiusEnd=4)
        .encode(
            y=alt.Y("label:N", sort="-x", title=None),
            x=alt.X("n_reservations:Q", title="reservations",
                    axis=count_axis(d["n_reservations"])),
            color=alt.Color(
                "band:N", title=None, sort=order,
                scale=alt.Scale(domain=order, range=[SERIES_2, SERIES_1]),
                legend=alt.Legend(orient="bottom-right", symbolType="square"),
            ),
            tooltip=[
                alt.Tooltip("label:N", title="sailor"),
                alt.Tooltip("n_reservations:Q", title="reservations"),
                alt.Tooltip("n_boats:Q", title="different boats"),
                alt.Tooltip("rank_from_top:Q", title="rank"),
            ],
        )
    )
    labels = bars.mark_text(align="left", dx=6, fontSize=11).encode(
        text="n_reservations:Q", color=alt.value(TEXT_SECONDARY)
    )
    return style(
        (bars + labels).properties(height=alt.Step(22)),
        "Top three sailors by reservations",
        "RANK() keeps the whole crew in view; LIMIT 3 would have kept three rows",
    )


# ---------------------------------------------------------------------------
# Q4 -- the quiet end, where the ties are
# ---------------------------------------------------------------------------

def plot_bottom_sailors(df: pd.DataFrame) -> alt.Chart:
    """Lollipops: reservations per sailor, fewest first, bottom band highlighted.

    Expects columns: sid, sname, n_reservations, rank_from_bottom, in_bottom_3.

    A dot on a stem rather than a bar, because most of the values are zero and
    a zero-length bar is invisible -- the dot still lands on the axis and says
    "none". Ten sailors tie at zero, which is why `LIMIT 3` cannot answer this
    question honestly: it would return three of the ten, chosen by nothing.
    """
    d = df.copy()
    d["label"] = _sailor_label(d)
    d["band"] = d["in_bottom_3"].map(
        {True: "bottom three ranks", False: "everyone else"}
    )
    # A real column of zeros for the stem's left end. `x=alt.value(0)` next to
    # an `x2` looks equivalent and serialises happily, but Vega-Lite rejects the
    # spec at render time ("Cannot read properties of undefined") because the
    # channel carries no type -- a failure that only appears in a browser.
    d["zero"] = 0

    order = ["bottom three ranks", "everyone else"]
    y = alt.Y("label:N", sort=alt.SortField("n_reservations", "ascending"), title=None)
    colour = alt.Color(
        "band:N", title=None, sort=order,
        scale=alt.Scale(domain=order, range=[SERIES_2, SERIES_1]),
        # Top-right: the bottom of this chart is where the long bars are.
        legend=alt.Legend(orient="top-right", symbolType="circle"),
    )
    tooltip = [
        alt.Tooltip("label:N", title="sailor"),
        alt.Tooltip("n_reservations:Q", title="reservations"),
        alt.Tooltip("rank_from_bottom:Q", title="rank from the bottom"),
    ]

    stems = (
        alt.Chart(d)
        .mark_rule(strokeWidth=2, color=STEM)
        .encode(y=y, x=alt.X("zero:Q", title=None), x2=alt.X2("n_reservations:Q"))
    )
    dots = (
        alt.Chart(d)
        .mark_circle(size=140, opacity=1, stroke=SURFACE, strokeWidth=2)
        .encode(
            y=y,
            x=alt.X("n_reservations:Q", title="reservations",
                    axis=count_axis(d["n_reservations"]),
                    scale=alt.Scale(domainMin=0)),
            color=colour,
            tooltip=tooltip,
        )
    )
    labels = dots.mark_text(align="left", dx=12, fontSize=11).encode(
        text="rank_from_bottom:Q", color=alt.value(TEXT_SECONDARY)
    )
    return style(
        (stems + dots + labels).properties(height=alt.Step(22)),
        "The quiet end of the crew",
        "The number beside each dot is DENSE_RANK -- ten sailors share rank 1",
    )


# ---------------------------------------------------------------------------
# Q5 -- what colours does each sailor take out
# ---------------------------------------------------------------------------

def plot_colour_mix(df: pd.DataFrame) -> alt.Chart:
    """Stacked bars: each sailor's reservations, split by boat colour.

    Expects columns: sid, sailor, color, n_reservations.

    The stack is honest here because the segments sum to something real -- one
    sailor's whole season. Segments are separated by a 2px surface-coloured
    stroke so adjacent colours never touch, and the tooltip names the colour,
    because red and green are the pair colour-blind readers cannot separate.
    """
    order = [c for c in BOAT_COLOUR_FILL if c in set(df["color"])]

    bars = (
        alt.Chart(df)
        .mark_bar(size=BAR_SIZE + 6, cornerRadiusEnd=4,
                  stroke=SURFACE, strokeWidth=2)
        .encode(
            # Each sailor has one row per colour, so sorting by `sid` needs an
            # aggregate to say which of those rows to sort on. Without `op` the
            # axis quietly falls back to alphabetical order.
            y=alt.Y("sailor:N", title=None,
                    sort=alt.EncodingSortField("sid", op="min",
                                               order="ascending")),
            # The bars are stacked, so the axis has to reach the tallest
            # *total*, not the largest single segment.
            x=alt.X("n_reservations:Q", title="reservations",
                    axis=count_axis(
                        df.groupby("sailor")["n_reservations"].sum())),
            color=alt.Color(
                "color:N", title="boat colour", sort=order,
                scale=alt.Scale(domain=order,
                                range=[BOAT_COLOUR_FILL[c] for c in order]),
                legend=alt.Legend(orient="right", symbolType="square"),
            ),
            order=alt.Order("color:N"),
            tooltip=[
                alt.Tooltip("sailor:N", title="sailor"),
                alt.Tooltip("color:N", title="boat colour"),
                alt.Tooltip("n_reservations:Q", title="reservations"),
            ],
        )
    )
    return style(
        bars.properties(height=alt.Step(34)),
        "What each sailor takes out, by boat colour",
        "Grouped by sid, not by name -- the two Horatios are different sailors",
    )


# ---------------------------------------------------------------------------
# Q6 -- each boat's season, first outing to last
# ---------------------------------------------------------------------------

def plot_boat_seasons(df: pd.DataFrame) -> alt.Chart:
    """Range bars: the span between each boat's first and last outing.

    Expects columns: bid, boat, color, n_reservations, first_out, last_out,
    span_days.

    MIN and MAX of a date column are two ends of a line, so they are drawn as
    one: the bar *is* `max(day) - min(day)`. What the chart cannot show is how
    many outings happened inside the span -- that is what the endpoint dots and
    the tooltip are for, and it is why `span_days` alone is a poor measure of a
    busy boat.

    Dates arrive as `datetime.date` and Vega cannot serialise those, so they
    are coerced here (see plots.plot_reservations_by_month for the full story).
    """
    d = df.copy()
    d["first_out"] = pd.to_datetime(d["first_out"])
    d["last_out"] = pd.to_datetime(d["last_out"])

    y = alt.Y("boat:N", title=None, sort=alt.SortField("first_out", "ascending"))
    x = alt.X("first_out:T", title="1998 season",
              axis=alt.Axis(format="%b %d",
                            tickCount={"interval": "week", "step": 2}))
    tooltip = [
        alt.Tooltip("boat:N", title="boat"),
        alt.Tooltip("color:N", title="colour"),
        alt.Tooltip("first_out:T", title="first outing", format="%Y-%m-%d"),
        alt.Tooltip("last_out:T", title="last outing", format="%Y-%m-%d"),
        alt.Tooltip("span_days:Q", title="days between"),
        alt.Tooltip("n_reservations:Q", title="outings"),
    ]

    spans = (
        alt.Chart(d)
        .mark_bar(size=10, cornerRadius=5, color=SERIES_1)
        .encode(y=y, x=x, x2=alt.X2("last_out:T"), tooltip=tooltip)
    )
    ends = (
        alt.Chart(d)
        .mark_point(size=70, filled=True, color=SERIES_1,
                    stroke=SURFACE, strokeWidth=2)
        .encode(y=y, x=alt.X("last_out:T"), tooltip=tooltip)
    )
    labels = (
        alt.Chart(d)
        .mark_text(align="left", dx=10, fontSize=11, color=TEXT_SECONDARY)
        .encode(y=y, x=alt.X("last_out:T"),
                text=alt.Text("span_days:Q", format=".0f"))
    )
    return style(
        (spans + ends + labels).properties(height=alt.Step(34)),
        "Each boat's season, first outing to last",
        "The number is span_days; a long bar can still hold only two outings",
    )


# ---------------------------------------------------------------------------
# Q7 -- how much of the fleet was out each day
# ---------------------------------------------------------------------------

def plot_busiest_days(df: pd.DataFrame) -> alt.Chart:
    """Bars: boats out per day, busiest first in the tooltip but chronological on screen.

    Expects columns: day (date), boats_out, pct_of_fleet, who.

    The query sorts by `boats_out DESC` to answer "which day was busiest"; the
    chart puts the days back in date order, because a time axis that is sorted
    by value stops being a time axis. Same rows, two orders, each right for its
    medium.

    Only days that appear in `reserves` are here -- the quiet days are missing,
    and Level 4 builds the calendar spine that puts them back.
    """
    d = df.copy()
    d["day"] = pd.to_datetime(d["day"])

    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE, cornerRadiusEnd=4, color=SERIES_1)
        .encode(
            x=alt.X("day:O", title="day",
                    # Ordinal axis: Vega-Lite reads `format` as a *number*
                    # format unless formatType says otherwise, and an unusable
                    # format string renders the chart blank.
                    axis=alt.Axis(labelAngle=-45, format="%Y-%m-%d",
                                  formatType="time")),
            y=alt.Y("boats_out:Q", title="boats out",
                    axis=count_axis(d["boats_out"])),
            tooltip=[
                alt.Tooltip("day:T", title="day", format="%Y-%m-%d"),
                alt.Tooltip("boats_out:Q", title="boats out"),
                alt.Tooltip("pct_of_fleet:Q", title="% of the fleet", format=".1f"),
                alt.Tooltip("who:N", title="who was out"),
            ],
        )
    )
    labels = bars.mark_text(dy=-8, fontSize=11, color=TEXT_SECONDARY).encode(
        text="boats_out:Q"
    )
    return style(
        (bars + labels).properties(height=260),
        "Boats out per booked day",
        "Only one day ever had two boats out at once: 1998-09-08",
    )


# ---------------------------------------------------------------------------
# Q8 -- the crew in age bands
# ---------------------------------------------------------------------------

def plot_age_bands(df: pd.DataFrame) -> alt.Chart:
    """Bars: how many sailors fall in each CASE band, labelled with average rating.

    Expects columns: age_band, n_sailors, avg_rating, avg_age, band_floor.

    Bands are ordered by `band_floor`, not alphabetically -- '25 to 39' sorts
    before 'under 25' as text, which would put the bands in nonsense order.
    The average rating rides as a label rather than a second axis: two measures
    on one chart never means two y-scales.
    """
    d = df.copy()
    d["rating_label"] = "avg rating " + d["avg_rating"].round(1).astype(str)

    x_sort = list(d.sort_values("band_floor")["age_band"])
    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE + 10, cornerRadiusEnd=4, color=SERIES_1)
        .encode(
            x=alt.X("age_band:N", title="age band", sort=x_sort,
                    axis=alt.Axis(labelAngle=0)),
            y=alt.Y("n_sailors:Q", title="sailors",
                    axis=count_axis(d["n_sailors"])),
            tooltip=[
                alt.Tooltip("age_band:N", title="band"),
                alt.Tooltip("n_sailors:Q", title="sailors"),
                alt.Tooltip("avg_age:Q", title="average age", format=".1f"),
                alt.Tooltip("avg_rating:Q", title="average rating", format=".2f"),
            ],
        )
    )
    counts = bars.mark_text(dy=-22, fontSize=12, color=TEXT_SECONDARY).encode(
        text="n_sailors:Q"
    )
    ratings = bars.mark_text(dy=-8, fontSize=10, color=TEXT_SECONDARY).encode(
        text="rating_label:N"
    )
    return style(
        (bars + counts + ratings).properties(height=290),
        "The crew, in age bands",
        "Bands come from CASE, and are ordered by where each band starts",
    )
