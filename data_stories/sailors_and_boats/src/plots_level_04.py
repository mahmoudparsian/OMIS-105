"""Charts for notebooks/notebook_level_04.py -- the twelve advanced queries.

The notebook writes SQL and calls one function from here per chart; styling
comes from `plots.style()`.

Level 4 is where the charts have to show something the table cannot: how far
every sailor is from "all boats", where a window function's ranks disagree,
and how much of the season is quiet days that appear in no row of `reserves`.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

from plots import (
    BAR_SIZE,
    SEQUENTIAL_BLUE,
    SERIES_1,
    SERIES_2,
    SERIES_3,
    SERIES_4,
    STEM,
    SURFACE,
    TEXT_SECONDARY,
    count_axis,
    style,
    whole_steps,
)


# ---------------------------------------------------------------------------
# Q1 -- how close is anybody to reserving the whole fleet
# ---------------------------------------------------------------------------

def plot_division_progress(df: pd.DataFrame) -> alt.Chart:
    """Bars: boats reserved per sailor, against a line at the size of the fleet.

    Expects columns: sid, sname, boats_reserved, fleet_size, has_them_all.

    Relational division answers "nobody", and a query that returns no rows
    teaches nothing. So the query keeps every sailor and the chart draws the
    target: the gap between the tallest bar and the dashed rule *is* the empty
    answer, made visible.
    """
    d = df.copy()
    d["label"] = d["sname"] + " (" + d["sid"].astype(str) + ")"
    fleet_size = int(d["fleet_size"].iloc[0])

    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE, cornerRadiusEnd=4, color=SERIES_1)
        .encode(
            y=alt.Y("label:N", sort="-x", title=None),
            x=alt.X("boats_reserved:Q", title="different boats reserved",
                    scale=alt.Scale(domain=[0, fleet_size]),
                    axis=count_axis([fleet_size])),
            tooltip=[
                alt.Tooltip("label:N", title="sailor"),
                alt.Tooltip("boats_reserved:Q", title="boats reserved"),
                alt.Tooltip("fleet_size:Q", title="boats in the fleet"),
                alt.Tooltip("has_them_all:N", title="has them all?"),
            ],
        )
    )
    labels = bars.mark_text(align="left", dx=6, fontSize=11).encode(
        text="boats_reserved:Q", color=alt.value(TEXT_SECONDARY)
    )
    target = (
        alt.Chart(pd.DataFrame({"x": [fleet_size]}))
        .mark_rule(strokeDash=[6, 4], strokeWidth=2, color=SERIES_2)
        .encode(x="x:Q")
    )
    target_label = (
        alt.Chart(pd.DataFrame({"x": [fleet_size], "t": [f"all {fleet_size} boats"]}))
        .mark_text(align="right", dx=-8, dy=-8, fontSize=11, color=SERIES_2,
                   baseline="top")
        .encode(x="x:Q", text="t:N")
    )
    return style(
        (bars + labels + target + target_label).properties(height=alt.Step(22)),
        "Distance from 'has reserved every boat'",
        "Dustin leads with 4 of 9 -- the division returns nobody, and this is why",
    )


# ---------------------------------------------------------------------------
# Q4 -- the season accumulating
# ---------------------------------------------------------------------------

def plot_running_total(df: pd.DataFrame) -> alt.Chart:
    """Step line: reservations accumulated across the season.

    Expects columns: day (date), n_reservations, running_total, pct_of_season.

    A running total only ever moves at a booking, and holds flat in between --
    so the line is drawn as steps rather than sloping between points, which
    would imply bookings on days that had none. Points mark the days the total
    actually changed.

    Dates are coerced from `datetime.date` for Vega, as everywhere else.
    """
    d = df.copy()
    d["day"] = pd.to_datetime(d["day"])

    line = (
        alt.Chart(d)
        .mark_line(strokeWidth=2, color=SERIES_1, interpolate="step-after")
        .encode(
            x=alt.X("day:T", title="1998 season",
                    axis=alt.Axis(format="%b %d",
                                  tickCount={"interval": "week", "step": 2})),
            y=alt.Y("running_total:Q", title="reservations so far",
                    scale=alt.Scale(domainMin=0),
                    axis=count_axis(d["running_total"])),
        )
    )
    dots = (
        alt.Chart(d)
        .mark_point(size=80, filled=True, color=SERIES_1,
                    stroke=SURFACE, strokeWidth=2)
        .encode(
            x="day:T",
            y="running_total:Q",
            tooltip=[
                alt.Tooltip("day:T", title="day", format="%Y-%m-%d"),
                alt.Tooltip("n_reservations:Q", title="booked that day"),
                alt.Tooltip("running_total:Q", title="season to date"),
                alt.Tooltip("pct_of_season:Q", title="% of the season",
                            format=".1f"),
            ],
        )
    )
    return style(
        (line + dots).properties(height=280),
        "The season, accumulating",
        "SUM(COUNT(*)) OVER (ORDER BY day) -- an aggregate inside a window",
    )


# ---------------------------------------------------------------------------
# Q5 -- where the three ranking functions disagree
# ---------------------------------------------------------------------------

def plot_rank_functions(df: pd.DataFrame) -> alt.Chart:
    """Grouped bars: ROW_NUMBER, RANK and DENSE_RANK for every sailor.

    Expects columns: sid, sname, n_reservations, as_row_number, as_rank,
    as_dense_rank.

    Three bars per sailor, and for the four sailors who have actually sailed
    they are identical -- the functions only diverge inside a tie. In the
    ten-way tie at zero, ROW_NUMBER fans out to 5..14 while RANK and DENSE_RANK
    hold flat, which is the whole lesson in one shape.

    Every bar is labelled with its value: two of the three hues sit under the
    3:1 contrast floor against the chart surface, so identity never rests on
    colour alone.
    """
    d = df.melt(
        id_vars=["sid", "sname", "n_reservations"],
        value_vars=["as_row_number", "as_rank", "as_dense_rank"],
        var_name="fn",
        value_name="value",
    )
    names = {"as_row_number": "ROW_NUMBER()", "as_rank": "RANK()",
             "as_dense_rank": "DENSE_RANK()"}
    d["fn"] = d["fn"].map(names)
    d["label"] = d["sname"] + " (" + d["sid"].astype(str) + ")"

    order = list(names.values())
    # Sorting a nominal axis by another field needs an aggregate: each sailor
    # has three rows here, so "sort by n_reservations" has to say which of the
    # three to sort on. Without `op` the axis silently falls back to
    # alphabetical, which buries the whole point of the chart.
    y = alt.Y("label:N", title=None,
              sort=alt.EncodingSortField("n_reservations", op="max",
                                         order="descending"))
    y_offset = alt.YOffset("fn:N", sort=order)

    bars = (
        alt.Chart(d)
        .mark_bar(size=7, cornerRadiusEnd=2)
        .encode(
            y=y,
            yOffset=y_offset,
            x=alt.X("value:Q", title="position in the ranking",
                    axis=count_axis(d["value"])),
            color=alt.Color(
                "fn:N", title=None, sort=order,
                scale=alt.Scale(domain=order,
                                range=[SERIES_1, SERIES_2, SERIES_3]),
                # Top-right: the long ROW_NUMBER bars are at the BOTTOM of this
                # chart (the tie), so a bottom-right legend sits on top of them.
                legend=alt.Legend(orient="top-right", symbolType="square"),
            ),
            tooltip=[
                alt.Tooltip("label:N", title="sailor"),
                alt.Tooltip("n_reservations:Q", title="reservations"),
                alt.Tooltip("fn:N", title="function"),
                alt.Tooltip("value:Q", title="value"),
            ],
        )
    )
    # Built from a fresh chart rather than `bars.mark_text(...)`: re-encoding
    # colour on top of an inherited colour encoding leaves the inherited scale
    # in place, and the layered chart renders the same legend twice.
    labels = (
        alt.Chart(d)
        .mark_text(align="left", dx=4, fontSize=9, color=TEXT_SECONDARY)
        .encode(y=y, yOffset=y_offset, x=alt.X("value:Q"), text="value:Q")
    )
    return style(
        (bars + labels).properties(height=alt.Step(11)),
        "ROW_NUMBER vs RANK vs DENSE_RANK",
        "Identical until a tie: ten sailors tie at zero reservations",
    )


# ---------------------------------------------------------------------------
# Q6 -- how long each boat sits idle
# ---------------------------------------------------------------------------

def plot_boat_idle(df: pd.DataFrame) -> alt.Chart:
    """Dots on a stem: the gap in days between one outing and the boat's next.

    Expects columns: boat, day (date), previous_outing, idle_days.

    One dot per *gap*, not per outing -- a boat's first trip of the season has
    no previous row, so `LAG` returns NULL there and the row carries no gap to
    draw. Dropping those rows in the chart is the visual form of the same fact
    the table shows as an empty cell.
    """
    d = df.dropna(subset=["idle_days"]).copy()
    d["idle_days"] = d["idle_days"].astype(int)
    d["day"] = pd.to_datetime(d["day"])
    d["previous_outing"] = pd.to_datetime(d["previous_outing"])
    # See plots_level_03.plot_bottom_sailors: the stem's left end has to be a
    # typed column, not `alt.value(0)`, or the spec renders as an error.
    d["zero"] = 0

    y = alt.Y("boat:N", title=None, sort="ascending")
    tooltip = [
        alt.Tooltip("boat:N", title="boat"),
        alt.Tooltip("previous_outing:T", title="previous outing",
                    format="%Y-%m-%d"),
        alt.Tooltip("day:T", title="next outing", format="%Y-%m-%d"),
        alt.Tooltip("idle_days:Q", title="idle days"),
    ]

    stems = (
        alt.Chart(d)
        .mark_rule(strokeWidth=2, color=STEM)
        .encode(y=y, x=alt.X("zero:Q", title=None), x2=alt.X2("idle_days:Q"))
    )
    dots = (
        alt.Chart(d)
        .mark_circle(size=150, color=SERIES_1, opacity=1,
                     stroke=SURFACE, strokeWidth=2)
        .encode(
            y=y,
            x=alt.X("idle_days:Q", title="days idle between outings",
                    scale=alt.Scale(domainMin=0),
                    axis=count_axis(d["idle_days"])),
            tooltip=tooltip,
        )
    )
    # No per-dot labels: two of boat 102's gaps are 31 and 32 days, and their
    # labels sit on top of each other. The axis and the tooltip both carry the
    # number, and the shape -- every gap around a month -- is the point.
    return style(
        (stems + dots).properties(height=alt.Step(34)),
        "How long each boat waits between outings",
        "One dot per gap -- a first outing has no previous row, so LAG gives NULL",
    )


# ---------------------------------------------------------------------------
# Q7 -- each sailor's share of the season
# ---------------------------------------------------------------------------

def plot_season_share(df: pd.DataFrame) -> alt.Chart:
    """Pie: what fraction of all reservations belongs to each sailor.

    Expects columns: sailor, n_reservations, pct_of_season.

    `SUM(COUNT(*)) OVER ()` computed those percentages in SQL, and they sum to
    100 because every reservation has exactly one sailor -- which is the test a
    pie has to pass. Four slices, each directly labelled with its share.
    """
    d = df.copy()
    # The legend names the sailor, so the slice carries only the numbers --
    # "Dustin (22) · 4 (40%)" is wider than the pie and lands on top of it.
    d["label"] = (d["n_reservations"].astype(str) + " ("
                  + d["pct_of_season"].round(0).astype(int).astype(str) + "%)")

    order = list(d.sort_values("n_reservations", ascending=False)["sailor"])
    palette = [SERIES_1, SERIES_2, SERIES_3, SERIES_4]

    base = alt.Chart(d).encode(
        theta=alt.Theta("n_reservations:Q", stack=True),
        color=alt.Color(
            "sailor:N", title="sailor", sort=order,
            scale=alt.Scale(domain=order, range=palette[:len(order)]),
            legend=alt.Legend(orient="right", symbolType="square"),
        ),
        order=alt.Order("n_reservations:Q", sort="descending"),
        tooltip=[
            alt.Tooltip("sailor:N", title="sailor"),
            alt.Tooltip("n_reservations:Q", title="reservations"),
            alt.Tooltip("pct_of_season:Q", title="share of season", format=".1f"),
        ],
    )
    wedges = base.mark_arc(outerRadius=96, stroke=SURFACE, strokeWidth=2)
    labels = base.mark_text(radius=128, fontSize=11).encode(
        text="label:N", color=alt.value(TEXT_SECONDARY)
    )
    return style(
        (wedges + labels).properties(height=320),
        "Share of the season, by sailor",
        "Only four sailors ever booked anything, so the pie is those four",
    )


# ---------------------------------------------------------------------------
# Q8 -- the PIVOT result as a heatmap
# ---------------------------------------------------------------------------

def plot_month_heatmap(df: pd.DataFrame) -> alt.Chart:
    """Heatmap of the pivoted boat x month table.

    Expects the *pivoted* frame: a `boat` column plus one column per month
    ('1998-09', '1998-10', ...).

    PIVOT produces the shape a person reads -- one row per boat, one column per
    month. Vega wants the opposite: one row per cell. So the frame is melted
    back to long form here, which is the honest division of labour, and the
    reason it is worth seeing both: the wide table is for the reader, the long
    table is for the renderer.
    """
    months = [c for c in df.columns if c != "boat"]
    d = df.melt(id_vars="boat", value_vars=months,
                var_name="month", value_name="n_reservations")
    d["n_reservations"] = d["n_reservations"].fillna(0).astype(int)

    cells = (
        alt.Chart(d)
        .mark_rect(stroke=SURFACE, strokeWidth=2, cornerRadius=3)
        .encode(
            # No grid on either axis. `style()` turns gridlines on for every
            # chart, and on a heatmap they are drawn *over* the cells -- each
            # rectangle ends up with a pale line across it that reads as a
            # border in the wrong place.
            x=alt.X("month:N", title=None, sort=months,
                    axis=alt.Axis(labelAngle=0, grid=False)),
            y=alt.Y("boat:N", title=None, axis=alt.Axis(grid=False)),
            color=alt.Color(
                "n_reservations:Q",
                title="outings",
                # Magnitude is one hue, light to dark -- never a rainbow.
                scale=alt.Scale(range=SEQUENTIAL_BLUE, type="linear"),
                legend=alt.Legend(orient="right", gradientLength=120,
                                  values=whole_steps(d["n_reservations"]),
                                  format="d"),
            ),
            tooltip=[
                alt.Tooltip("boat:N", title="boat"),
                alt.Tooltip("month:N", title="month"),
                alt.Tooltip("n_reservations:Q", title="outings"),
            ],
        )
    )
    # Every cell carries its number, so a reader never has to decode a shade --
    # and the zeros stay legible against the palest step.
    text = cells.mark_text(fontSize=11).encode(
        text="n_reservations:Q",
        # The threshold follows the data, not a fixed number: no boat here goes
        # out twice in a month, so the whole ramp is spent between 0 and 1 and a
        # cell holding 1 is already the darkest step.
        color=alt.condition(alt.datum.n_reservations >= max(1, int(
                                d["n_reservations"].max()) // 2 + 1),
                            alt.value("#ffffff"), alt.value(TEXT_SECONDARY)),
    )
    return style(
        (cells + text).properties(height=alt.Step(34)),
        "Outings per boat per month",
        "The PIVOT result, melted back to one row per cell for the chart",
    )


# ---------------------------------------------------------------------------
# Q9 -- the whole season, quiet days included
# ---------------------------------------------------------------------------

def plot_utilisation(df: pd.DataFrame) -> alt.Chart:
    """Step area: how much of the fleet was out, every day of the season.

    Expects columns: day (date), boats_out, pct_of_fleet.

    This is the chart the calendar spine was built for. Sixty of these
    sixty-nine days appear nowhere in `reserves`, so without the recursive CTE
    the flat stretches would simply not exist and the season would look
    continuously busy. An area rather than a line, because the quantity is a
    count that sits on zero most of the time and the filled shape reads as
    "how much of the time".
    """
    d = df.copy()
    d["day"] = pd.to_datetime(d["day"])

    area = (
        alt.Chart(d)
        .mark_area(interpolate="step-after", line={"color": SERIES_1, "strokeWidth": 2},
                   color=SERIES_1, opacity=0.22)
        .encode(
            x=alt.X("day:T", title="1998 season",
                    axis=alt.Axis(format="%b %d",
                                  tickCount={"interval": "week", "step": 1})),
            y=alt.Y("boats_out:Q", title="boats out",
                    scale=alt.Scale(domainMin=0),
                    axis=count_axis(d["boats_out"])),
            tooltip=[
                alt.Tooltip("day:T", title="day", format="%Y-%m-%d"),
                alt.Tooltip("boats_out:Q", title="boats out"),
                alt.Tooltip("pct_of_fleet:Q", title="% of the fleet", format=".1f"),
            ],
        )
    )
    return style(
        area.properties(height=260),
        "Fleet utilisation across the whole season",
        "69 days in the spine, 9 of them with a booking -- the rest are real zeros",
    )


# ---------------------------------------------------------------------------
# Q11 -- the year, split into days that sailed and days that did not
# ---------------------------------------------------------------------------

def plot_idle_days(df: pd.DataFrame) -> alt.Chart:
    """Stacked bars: each year's observed days, split into booked and idle.

    Expects columns: yr, days_observed, days_with_a_booking, idle_days,
    pct_idle.

    A part-to-whole split, so it stacks: the bar is the year's observed window
    and the segments say how it was spent. This is the one chart in the level
    that stays honest on a single year -- the tutorial season is one bar, and a
    bar that is 87% empty still tells you something. Against the 2024-2026
    database it becomes three.

    The frame arrives wide (one column per count) and Vega wants it long.
    """
    d = df.melt(id_vars=["yr", "days_observed", "pct_idle"],
                value_vars=["days_with_a_booking", "idle_days"],
                var_name="kind", value_name="days")
    d["kind"] = d["kind"].map({"days_with_a_booking": "at least one booking",
                               "idle_days": "nobody sailed"})
    d["yr"] = d["yr"].astype(str)

    order = ["at least one booking", "nobody sailed"]
    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE + 16, cornerRadiusEnd=4,
                  stroke=SURFACE, strokeWidth=2)
        .encode(
            x=alt.X("yr:N", title="year", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("days:Q", title="days",
                    axis=count_axis(df["days_observed"])),
            color=alt.Color(
                "kind:N", title=None, sort=order,
                scale=alt.Scale(domain=order, range=[SERIES_1, SERIES_2]),
                legend=alt.Legend(orient="top", direction="horizontal",
                                  symbolType="square"),
            ),
            order=alt.Order("kind:N"),
            tooltip=[
                alt.Tooltip("yr:N", title="year"),
                alt.Tooltip("kind:N", title="kind of day"),
                alt.Tooltip("days:Q", title="days"),
                alt.Tooltip("days_observed:Q", title="days observed"),
                alt.Tooltip("pct_idle:Q", title="% idle", format=".1f"),
            ],
        )
    )
    # Label position is computed here rather than left to `stack=True`: a
    # stacked text mark lands on the segment BOUNDARY, so the top label is half
    # cut off by the end of the bar. The midpoint of each segment is arithmetic
    # the plotting side can do exactly.
    d = d.sort_values(["yr", "kind"], key=lambda c: c.map(
        {k: i for i, k in enumerate(order)}) if c.name == "kind" else c)
    d["y_mid"] = (d.groupby("yr")["days"].cumsum() - d["days"] / 2)
    labels = (
        alt.Chart(d)
        .mark_text(fontSize=11, color="#ffffff", baseline="middle")
        .encode(x=alt.X("yr:N"), y=alt.Y("y_mid:Q"), text="days:Q")
    )
    return style(
        (bars + labels).properties(height=300),
        "Days that sailed, and days that did not",
        "The bar is the observed season, not the calendar year",
    )


# ---------------------------------------------------------------------------
# Q12 -- the years, ranked
# ---------------------------------------------------------------------------

def plot_year_ranking(df: pd.DataFrame) -> alt.Chart:
    """Horizontal bars: reservations per year, busiest first, labelled with rank.

    Expects columns: yr, n_reservations, n_sailors, n_boats, rank_by_volume,
    pct_of_all_time, change_on_previous_year.

    Against the tutorial database this is a single bar -- one season, rank 1,
    100% -- and Level 2's Q9 says outright that a one-row grouping is a number
    rather than a chart. It is drawn here anyway because this notebook is meant
    to be run against `sailors_and_boats_2.duckdb` as well, where the same cell
    ranks three years and the ranking is the point.
    """
    d = df.copy()
    d["yr"] = d["yr"].astype(str)
    d["label"] = ("#" + d["rank_by_volume"].astype(str) + " · "
                  + d["n_reservations"].astype(str) + " · "
                  + d["pct_of_all_time"].round(0).astype(int).astype(str) + "%")

    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE + 6, cornerRadiusEnd=4, color=SERIES_1)
        .encode(
            y=alt.Y("yr:N", title=None,
                    sort=alt.EncodingSortField("rank_by_volume", op="min",
                                               order="ascending")),
            # Head-room for the label, which sits outside the bar: without it
            # "#1 · 1909 · 38%" runs off the right edge of the longest bar.
            x=alt.X("n_reservations:Q", title="reservations",
                    scale=alt.Scale(domain=[0, d["n_reservations"].max() * 1.25]),
                    axis=count_axis(d["n_reservations"])),
            tooltip=[
                alt.Tooltip("yr:N", title="year"),
                alt.Tooltip("n_reservations:Q", title="reservations"),
                alt.Tooltip("rank_by_volume:Q", title="rank by volume"),
                alt.Tooltip("pct_of_all_time:Q", title="% of all bookings",
                            format=".1f"),
                alt.Tooltip("n_sailors:Q", title="sailors who booked"),
                alt.Tooltip("n_boats:Q", title="boats used"),
            ],
        )
    )
    labels = bars.mark_text(align="left", dx=6, fontSize=11,
                            color=TEXT_SECONDARY).encode(text="label:N")
    return style(
        (bars + labels).properties(height=alt.Step(38)),
        "Years ranked by how much sailing happened",
        "Label is rank · reservations · share of every booking ever made",
    )
