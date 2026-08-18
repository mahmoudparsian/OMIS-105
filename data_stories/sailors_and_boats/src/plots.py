"""All plotting code for the Sailors & Boats notebook lives here.

The assignment requires the plotting code to sit *outside* the notebook, so the
notebook's job is limited to writing SQL and calling one function per chart.
Every function takes the DataFrame a query returned and gives back an Altair
chart -- no function here runs SQL or touches the database.

Colour policy (see the data-viz palette these values come from):
  * one measure, one series  -> a single blue, no legend; the title names it
  * continuous magnitude     -> the single-hue blue sequential ramp, light->dark
  * never a rainbow, never a second y-axis
Marks are thin, grids recessive, and every chart carries a hover tooltip.
"""

from __future__ import annotations

import altair as alt
import pandas as pd

# --- palette ----------------------------------------------------------------
SERIES_1 = "#2a78d6"   # categorical slot 1 -- the default single series
SERIES_2 = "#eb6834"   # categorical slot 2 -- only when a second series exists
# Slots 3 and 4 exist for the level notebooks (three ranking functions, four
# sailors in a pie) and are taken in this fixed order, never cycled. The four
# together pass the palette checks -- lightness band, chroma floor, colour-vision
# separation -- but slots 3 and 4 sit under 3:1 against the surface, so any chart
# using them must label its marks directly rather than relying on hue.
SERIES_3 = "#1baf7a"   # categorical slot 3 -- aqua
SERIES_4 = "#eda100"   # categorical slot 4 -- yellow
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e6e5e1"
# Lollipop stems: heavier than the grid so the line to the axis reads, lighter
# than any mark so it never competes with the dot carrying the value.
STEM = "#d0cfc9"
SURFACE = "#fcfcfb"

# Blue sequential ramp, light -> dark, for continuous magnitude.
SEQUENTIAL_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

CHART_WIDTH = 620
BAR_SIZE = 18


def whole_steps(values) -> list[int]:
    """Explicit tick values for an axis that counts things.

    `alt.Axis(tickMinStep=1)` is the documented way to keep an axis on whole
    numbers, and it is enough on a single-layer chart. It is *not* enough on a
    layered one: the layers share a scale, Vega-Lite may resolve the axis from
    whichever layer it likes, and a text layer that inherited the encoding
    without the axis produces half-steps -- a "sailors" axis reading
    0, 0.5, 1, 1.5, 2, which `format='d'` then renders as 0, 1, 1, 2, 2.

    Explicit values cannot be resolved away. Ticks stay at most nine apart so a
    long axis does not turn into a solid row of labels.
    """
    top = int(max(values)) if len(values) else 0
    # A "nice" step, not just top/9: ticks at 0, 213, 426 are arithmetically
    # correct and unreadable. Take the smallest familiar step that keeps the
    # axis under ten labels.
    for step in (1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 5000):
        if top // step <= 9:
            break
    return list(range(0, top + 1, step))


def count_axis(values, **kwargs) -> alt.Axis:
    """An axis for a column that counts things: whole-number ticks, no decimals.

    `format='d'` matters as much as the tick values -- Vega formats an axis
    from its scale, so ticks at [0, 1, 2] still render as "0.0, 1.0, 2.0" on a
    quantitative scale unless the format says otherwise.
    """
    return alt.Axis(values=whole_steps(values), format="d", **kwargs)


def style(chart: alt.Chart, title: str, subtitle: str = "") -> alt.Chart:
    """Shared styling: recessive axes, readable title, generous padding.

    Public on purpose: the four level notebooks have their own chart modules
    (`plots_level_01.py` ... `plots_level_04.py`) and every one of them calls
    this, so all 29 charts in the project share one look.
    """
    return (
        chart.properties(
            width=CHART_WIDTH,
            title=alt.TitleParams(
                text=title,
                subtitle=subtitle or None,
                anchor="start",
                fontSize=15,
                subtitleFontSize=12,
                color=TEXT_PRIMARY,
                subtitleColor=TEXT_SECONDARY,
                offset=12,
            ),
        )
        .configure_view(strokeWidth=0, fill=SURFACE)
        .configure_axis(
            grid=True,
            gridColor=GRID,
            gridWidth=1,
            domain=False,
            tickColor=GRID,
            labelColor=TEXT_SECONDARY,
            titleColor=TEXT_SECONDARY,
            labelFontSize=11,
            titleFontSize=11,
            titlePadding=8,
        )
        .configure_legend(
            labelColor=TEXT_SECONDARY,
            titleColor=TEXT_SECONDARY,
            labelFontSize=11,
            titleFontSize=11,
        )
    )


# ---------------------------------------------------------------------------
# Plot 1 -- reservations per boat
# ---------------------------------------------------------------------------

def plot_reservations_per_boat(df: pd.DataFrame) -> alt.Chart:
    """Horizontal bars: how many times each boat was booked.

    Expects columns: bid, bname, color, n_reservations.
    Horizontal because the labels are text ('102 Interlake / red'); sorted by
    value so the ranking is the shape of the chart. Boats with zero
    reservations stay on the axis -- their absence is the finding.
    """
    d = df.copy()
    d["label"] = d["bid"].astype(str) + "  " + d["bname"] + " (" + d["color"] + ")"

    bars = (
        alt.Chart(d)
        .mark_bar(size=BAR_SIZE, cornerRadiusEnd=4, color=SERIES_1)
        .encode(
            y=alt.Y("label:N", sort="-x", title=None),
            x=alt.X("n_reservations:Q", title="reservations",
                    axis=alt.Axis(tickMinStep=1)),
            tooltip=[
                alt.Tooltip("label:N", title="boat"),
                alt.Tooltip("n_reservations:Q", title="reservations"),
            ],
        )
    )
    labels = bars.mark_text(align="left", dx=6, fontSize=11, color=TEXT_SECONDARY).encode(
        text="n_reservations:Q"
    )
    return style(
        (bars + labels).properties(height=alt.Step(26)),
        "Reservations per boat",
        "Boats at zero have never been booked",
    )


# ---------------------------------------------------------------------------
# Plot 2 -- average age by rating level
# ---------------------------------------------------------------------------

def plot_avg_age_by_rating(df: pd.DataFrame) -> alt.Chart:
    """Vertical bars: average sailor age at each rating level.

    Expects columns: rating, avg_age, n_sailors.
    Rating is an ordered discrete scale, so it stays on the x-axis in its
    natural order rather than being sorted by value.
    """
    bars = (
        alt.Chart(df)
        .mark_bar(size=BAR_SIZE, cornerRadiusEnd=4, color=SERIES_1)
        .encode(
            x=alt.X("rating:O", title="rating (1 = novice, 10 = expert)"),
            y=alt.Y("avg_age:Q", title="average age"),
            tooltip=[
                alt.Tooltip("rating:O", title="rating"),
                alt.Tooltip("avg_age:Q", title="average age", format=".1f"),
                alt.Tooltip("n_sailors:Q", title="sailors"),
            ],
        )
    )
    labels = bars.mark_text(dy=-8, fontSize=11, color=TEXT_SECONDARY).encode(
        text=alt.Text("avg_age:Q", format=".1f")
    )
    return style(
        (bars + labels).properties(height=280),
        "Average age by rating level",
        "Unrated sailors are excluded -- AVG ignores NULL",
    )


# ---------------------------------------------------------------------------
# Plot 3 -- reservations over time
# ---------------------------------------------------------------------------

def plot_reservations_by_month(df: pd.DataFrame) -> alt.Chart:
    """Line + points: booking volume month by month.

    Expects columns: month_start (date), n_reservations.
    A line, because months are ordered and continuous -- the slope between
    points is meaningful. Points are drawn so single months stay visible.

    `sailors_db.q` hands back real `datetime.date` objects so tables print
    YYYY-MM-DD, but Vega serialises the frame to JSON and cannot encode a
    `date`. Marimo surfaces that as "Object of type date is not JSON
    serializable" and renders nothing; Streamlit's path happens to tolerate it,
    so this only breaks in the notebook. Coerce back to datetime for the chart.
    """
    d = df.copy()
    d["month_start"] = pd.to_datetime(d["month_start"])

    line = (
        alt.Chart(d)
        .mark_line(strokeWidth=2, color=SERIES_1, point=alt.OverlayMarkDef(
            size=90, fill=SERIES_1, stroke=SURFACE, strokeWidth=2))
        .encode(
            x=alt.X("month_start:T", title="month",
                    axis=alt.Axis(format="%b %Y",
                                  # One tick per month: the default fits ticks to
                                  # the pixel width and lands them mid-month, which
                                  # "%b %Y" then renders as duplicate labels.
                                  tickCount={"interval": "month", "step": 1})),
            y=alt.Y("n_reservations:Q", title="reservations",
                    scale=alt.Scale(domainMin=0), axis=alt.Axis(tickMinStep=1)),
            tooltip=[
                alt.Tooltip("month_start:T", title="month", format="%B %Y"),
                alt.Tooltip("n_reservations:Q", title="reservations"),
            ],
        )
    )
    return style(line.properties(height=280),
                 "Reservations by month",
                 "The 1998 sailing season in the tutorial data")


# ---------------------------------------------------------------------------
# Plot 4 -- fleet calendar heatmap
# ---------------------------------------------------------------------------

def plot_fleet_calendar(df: pd.DataFrame) -> alt.Chart:
    """Heatmap of boat x day, one cell per reservation.

    Expects columns: day (date), boat_label, sname, sid.
    This is the picture of PRIMARY KEY (bid, day): every cell is either empty
    or holds exactly one sailor. A second sailor in one cell is impossible,
    which is precisely what the assignment asked the schema to guarantee.

    As in plot_reservations_by_month, the `day` column arrives as
    `datetime.date` (so tables print YYYY-MM-DD) and Vega cannot serialise
    that -- coerce back to datetime for the chart only.
    """
    d = df.copy()
    d["day"] = pd.to_datetime(d["day"])

    cells = (
        alt.Chart(d)
        .mark_rect(stroke=SURFACE, strokeWidth=2, cornerRadius=3)
        .encode(
            x=alt.X("day:O", title="day",
                    # `day` is ordinal here (one column per booked date, no gaps).
                    # On an ordinal axis Vega-Lite treats `format` as a NUMBER
                    # format, so a time pattern needs formatType="time" or it
                    # raises "invalid format" and the chart renders blank.
                    axis=alt.Axis(labelAngle=-45, format="%Y-%m-%d",
                                  formatType="time")),
            y=alt.Y("boat_label:N", title=None),
            color=alt.Color(
                "sid:N",
                title="held by",
                # Every cell carries the sailor's name in white, so each step
                # must be dark enough to read it -- the pale end of the ramp
                # would render the label invisible. Identity comes from the
                # label, not the hue; the colour only groups a sailor's cells
                # at a glance, which is why four near steps are enough.
                scale=alt.Scale(range=["#256abf", "#1c5cab", "#184f95", "#0d366b"]),
                legend=alt.Legend(orient="right", symbolType="square"),
            ),
            tooltip=[
                alt.Tooltip("day:T", title="day", format="%Y-%m-%d"),
                alt.Tooltip("boat_label:N", title="boat"),
                alt.Tooltip("sname:N", title="sailor"),
                alt.Tooltip("sid:N", title="sid"),
            ],
        )
    )
    # Direct label inside each cell, so identity is never colour alone.
    text = cells.mark_text(fontSize=10, color="#ffffff").encode(
        text="sname:N", color=alt.value("#ffffff")
    )
    return style(
        (cells + text).properties(height=alt.Step(24)),
        "Fleet calendar -- who has which boat, and when",
        "One cell can hold at most one sailor: that is PRIMARY KEY (bid, day)",
    )


# ---------------------------------------------------------------------------
# Plot 5 -- age vs rating, sized by activity
# ---------------------------------------------------------------------------

def plot_age_vs_rating(df: pd.DataFrame) -> alt.Chart:
    """Scatter of every sailor: age against rating, shaded by booking count.

    Expects columns: sid, sname, rating, age, n_reservations.
    Magnitude rides a single-hue sequential ramp rather than a categorical
    palette, because "number of reservations" is a continuous quantity.
    """
    points = (
        alt.Chart(df)
        .mark_circle(size=170, stroke=SURFACE, strokeWidth=2, opacity=1)
        .encode(
            x=alt.X("rating:Q", title="rating",
                    scale=alt.Scale(domain=[0, 11]), axis=alt.Axis(tickMinStep=1)),
            y=alt.Y("age:Q", title="age", scale=alt.Scale(zero=False, nice=True)),
            color=alt.Color(
                "n_reservations:Q",
                title="reservations",
                scale=alt.Scale(range=SEQUENTIAL_BLUE, type="linear"),
                legend=alt.Legend(orient="right", gradientLength=140),
            ),
            tooltip=[
                alt.Tooltip("sname:N", title="sailor"),
                alt.Tooltip("sid:Q", title="sid"),
                alt.Tooltip("rating:Q", title="rating"),
                alt.Tooltip("age:Q", title="age"),
                alt.Tooltip("n_reservations:Q", title="reservations"),
            ],
        )
    )
    labels = points.mark_text(align="left", dx=10, fontSize=10,
                              color=TEXT_SECONDARY).encode(text="sname:N")
    return style((points + labels).properties(height=320),
                 "Sailors: age vs rating, shaded by how much they sail",
                 "Unrated sailors (rating IS NULL) drop out of this view")


# ---------------------------------------------------------------------------
# Plot 6 -- share of bookings by boat colour (pie)
# ---------------------------------------------------------------------------

# Boat colours drawn as themselves. This is the unusual case where mapping the
# mark to the literal hue is right rather than lazy: the category *is* a colour,
# so a blue slice for "blue" is self-documenting. Two adjustments keep it
# legible -- 'white' is nudged to a light warm grey so the slice does not vanish
# into the surface, and every slice carries a direct label, so identity never
# depends on hue alone (red and green are the classic colour-vision confusion).
BOAT_COLOUR_FILL = {
    "red":    "#c94a5a",
    "green":  "#2f9e63",
    "blue":   "#3179c9",
    "yellow": "#dfa920",
    "white":  "#dedbd2",
    "black":  "#33322e",
}


def plot_bookings_by_colour(df: pd.DataFrame) -> alt.Chart:
    """Pie: what share of all bookings goes to each boat colour.

    Expects columns: color, n_reservations, pct.

    A pie is the right form here and rarely elsewhere: the slices are parts of
    one whole (every reservation is on exactly one boat, which has exactly one
    colour, so the counts sum to every booking ever made) and there are only a
    handful of them. For comparing magnitudes across many categories a bar
    chart wins every time -- see plot_reservations_per_boat.
    """
    d = df.copy()
    d["label"] = (d["color"] + " · " + d["n_reservations"].astype(str)
                  + " (" + d["pct"].round(0).astype(int).astype(str) + "%)")

    order = [c for c in BOAT_COLOUR_FILL if c in set(d["color"])]

    base = alt.Chart(d).encode(
        theta=alt.Theta("n_reservations:Q", stack=True),
        color=alt.Color(
            "color:N",
            title="boat colour",
            sort=order,
            scale=alt.Scale(domain=order, range=[BOAT_COLOUR_FILL[c] for c in order]),
            legend=alt.Legend(orient="right", symbolType="square"),
        ),
        order=alt.Order("n_reservations:Q", sort="descending"),
        tooltip=[
            alt.Tooltip("color:N", title="colour"),
            alt.Tooltip("n_reservations:Q", title="bookings"),
            alt.Tooltip("pct:Q", title="share of bookings", format=".1f"),
        ],
    )

    # 2px surface-coloured gap between slices, per the mark spec.
    wedges = base.mark_arc(outerRadius=98, stroke=SURFACE, strokeWidth=2)
    # Labels sit outside the pie in text ink. The `color=alt.value(...)` is
    # doing real work: `base` carries a colour *encoding*, and an encoding beats
    # a mark property, so without the override each label inherits its slice's
    # fill -- which renders the "white" label invisible against the surface.
    # Radii are kept modest so the widest label still fits inside the chart.
    labels = base.mark_text(radius=122, fontSize=11).encode(
        text="label:N",
        color=alt.value(TEXT_SECONDARY),
    )

    return style((wedges + labels).properties(height=320),
                 "Share of bookings by boat colour",
                 "Every reservation is on exactly one boat, so the slices are a whole")
