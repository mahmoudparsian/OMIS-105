"""
plots_02.py — Chart functions for 02_netflix_analysis.py.

Each function:
  - Accepts (con, mo): a DuckDB connection and the marimo module
  - Runs its own focused SQL query
  - Returns a raw Altair Chart object (Marimo renders natively)
    OR mo.as_html(fig) for the matplotlib fallback

Usage inside a Marimo cell:
    import plots_02 as _p
    _w = _p.chart_q1(con, mo)
    _w
    return
"""

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="altair")


# ── Q1 · Movies vs TV Shows ──────────────────────────────────────────────────

def chart_q1(con, mo):
    df = con.execute(
        """
        SELECT type, COUNT(*) AS total
        FROM   netflix
        GROUP BY type
        ORDER BY total DESC
        """
    ).df()
    try:
        import altair as alt
        return (
            alt.Chart(df)
            .mark_bar(cornerRadius=6)
            .encode(
                x=alt.X("type:N", title="Content Type"),
                y=alt.Y("total:Q", title="Count"),
                color=alt.Color("type:N",
                    scale=alt.Scale(range=["#e50914", "#221f1f"])),
                tooltip=["type", "total"],
            )
            .properties(title="Movies vs TV Shows", width=300, height=250)
        )
    except ImportError:
        from util_plot import plot_bar_simple
        fig = plot_bar_simple(df, x="type", y="total", title="Movies vs TV Shows")
        return mo.as_html(fig)


# ── Q2 · Top 10 producing countries ──────────────────────────────────────────

def chart_q2(con, mo):
    df = con.execute(
        """
        SELECT first_country, COUNT(*) AS titles
        FROM   netflix
        WHERE  first_country IS NOT NULL AND first_country <> ''
        GROUP BY first_country
        ORDER BY titles DESC
        LIMIT 10
        """
    ).df()
    try:
        import altair as alt
        return (
            alt.Chart(df)
            .mark_bar(cornerRadius=4)
            .encode(
                x=alt.X("titles:Q", title="Titles"),
                y=alt.Y("first_country:N", sort="-x", title="Country"),
                color=alt.value("#e50914"),
                tooltip=["first_country", "titles"],
            )
            .properties(title="Top 10 Producing Countries", width=400, height=300)
        )
    except ImportError:
        from util_plot import plot_bar_h
        fig = plot_bar_h(df, x="titles", y="first_country",
                         title="Top 10 Producing Countries")
        return mo.as_html(fig)


# ── Q3 · Content added per year ───────────────────────────────────────────────

def chart_q3(con, mo):
    df = con.execute(
        """
        SELECT CAST(year_added AS INTEGER) AS year_added,
               COUNT(*) AS titles_added
        FROM   netflix
        WHERE  year_added IS NOT NULL
        GROUP BY year_added
        ORDER BY year_added
        """
    ).df()
    df["year_str"] = df["year_added"].astype(str)
    try:
        import altair as alt
        return (
            alt.Chart(df)
            .mark_bar(cornerRadius=4, color="#e50914")
            .encode(
                x=alt.X("year_str:N", title="Year"),
                y=alt.Y("titles_added:Q", title="Titles Added"),
                tooltip=["year_str", "titles_added"],
            )
            .properties(title="Titles Added to Netflix Per Year", width=500, height=280)
        )
    except ImportError:
        from util_plot import plot_line
        fig = plot_line(df, x="year_added", y="titles_added",
                        title="Titles Added Per Year")
        return mo.as_html(fig)


# ── Q5 · Audience age groups ──────────────────────────────────────────────────

def chart_q5(con, mo):
    df = con.execute(
        """
        SELECT age_group, COUNT(*) AS titles
        FROM   netflix
        WHERE  age_group <> 'Unknown'
        GROUP BY age_group
        ORDER BY titles DESC
        """
    ).df()
    try:
        import altair as alt
        return (
            alt.Chart(df)
            .mark_arc(innerRadius=50)
            .encode(
                theta=alt.Theta("titles:Q"),
                color=alt.Color("age_group:N",
                    scale=alt.Scale(
                        range=["#e50914", "#b20710", "#831b1b", "#221f1f"])),
                tooltip=["age_group", "titles"],
            )
            .properties(title="Audience Age Group Distribution", width=350, height=300)
        )
    except ImportError:
        from util_plot import plot_pie
        fig = plot_pie(df, label="age_group", value="titles",
                       title="Audience Age Groups")
        return mo.as_html(fig)


# ── Q8 · Content added by month ───────────────────────────────────────────────

def chart_q8(con, mo):
    df = con.execute(
        """
        SELECT CAST(month_added AS INTEGER) AS month_num,
               month_name, COUNT(*) AS titles
        FROM   netflix
        WHERE  month_added IS NOT NULL
        GROUP BY month_num, month_name
        ORDER BY month_num
        """
    ).df()
    # Pad month number so alphabetical sort == chronological sort
    df["month_label"] = df["month_num"].map(
        {1:"01 Jan",2:"02 Feb",3:"03 Mar",4:"04 Apr",5:"05 May",6:"06 Jun",
         7:"07 Jul",8:"08 Aug",9:"09 Sep",10:"10 Oct",11:"11 Nov",12:"12 Dec"}
    )
    try:
        import altair as alt
        return (
            alt.Chart(df)
            .mark_bar(cornerRadius=4, color="#e50914")
            .encode(
                x=alt.X("month_label:N", title="Month"),
                y=alt.Y("titles:Q", title="Titles Added"),
                tooltip=["month_name", "titles"],
            )
            .properties(title="Content Added by Month", width=500, height=280)
        )
    except ImportError:
        from util_plot import plot_bar_simple
        fig = plot_bar_simple(df, x="month_name", y="titles",
                              title="Content Added by Month")
        return mo.as_html(fig)


# ── Q10 · Avg movie runtime by country ───────────────────────────────────────

def chart_q10(con, mo):
    df = con.execute(
        """
        SELECT first_country,
               ROUND(AVG(duration_min), 1) AS avg_runtime_min
        FROM   netflix
        WHERE  type = 'Movie' AND duration_min IS NOT NULL
          AND  first_country IS NOT NULL AND first_country <> ''
        GROUP BY first_country
        HAVING COUNT(*) >= 20
        ORDER BY avg_runtime_min DESC
        LIMIT 15
        """
    ).df()
    try:
        import altair as alt
        return (
            alt.Chart(df)
            .mark_bar(cornerRadius=4, color="#b20710")
            .encode(
                x=alt.X("avg_runtime_min:Q", title="Avg Runtime (min)"),
                y=alt.Y("first_country:N", sort="-x", title="Country"),
                tooltip=["first_country", "avg_runtime_min"],
            )
            .properties(title="Avg Movie Runtime by Country (≥20 movies)",
                        width=450, height=340)
        )
    except ImportError:
        from util_plot import plot_bar_h
        fig = plot_bar_h(df, x="avg_runtime_min", y="first_country",
                         title="Avg Movie Runtime by Country")
        return mo.as_html(fig)


# ── Q11 · Top 20 genres ───────────────────────────────────────────────────────

def chart_q11(con, mo):
    df = con.execute(
        """
        SELECT TRIM(genre) AS genre, COUNT(*) AS appearances
        FROM (
            SELECT UNNEST(STRING_SPLIT(listed_in, ',')) AS genre
            FROM netflix WHERE listed_in IS NOT NULL
        ) sub
        GROUP BY genre ORDER BY appearances DESC LIMIT 20
        """
    ).df()
    try:
        import altair as alt
        return (
            alt.Chart(df)
            .mark_bar(cornerRadius=4, color="#e50914")
            .encode(
                x=alt.X("appearances:Q", title="Appearances"),
                y=alt.Y("genre:N", sort="-x", title="Genre"),
                tooltip=["genre", "appearances"],
            )
            .properties(title="Top 20 Netflix Genres", width=450, height=480)
        )
    except ImportError:
        from util_plot import plot_bar_h
        fig = plot_bar_h(df, x="appearances", y="genre",
                         title="Top 20 Netflix Genres")
        return mo.as_html(fig)


# ── Q14 · Movies vs TV Shows per year ────────────────────────────────────────

def chart_q14(con, mo):
    df = con.execute(
        """
        SELECT CAST(year_added AS INTEGER) AS year_added,
               COUNT(CASE WHEN type='Movie'   THEN 1 END) AS movies,
               COUNT(CASE WHEN type='TV Show' THEN 1 END) AS tv_shows
        FROM netflix WHERE year_added IS NOT NULL
        GROUP BY year_added ORDER BY year_added
        """
    ).df()
    df["year_str"] = df["year_added"].astype(str)
    try:
        import altair as alt
        df_long = df.melt("year_str", var_name="content_type", value_name="count")
        return (
            alt.Chart(df_long)
            .mark_bar(cornerRadius=2)
            .encode(
                x=alt.X("year_str:N", title="Year"),
                y=alt.Y("count:Q", title="Titles"),
                color=alt.Color("content_type:N",
                    scale=alt.Scale(domain=["movies", "tv_shows"],
                                    range=["#e50914", "#221f1f"])),
                tooltip=["year_str", "content_type", "count"],
            )
            .properties(title="Movies vs TV Shows Added Per Year",
                        width=500, height=280)
        )
    except ImportError:
        from util_plot import plot_line_dual
        fig = plot_line_dual(df, x="year_added", y1="movies", y2="tv_shows",
                             title="Movies vs TV Shows Per Year")
        return mo.as_html(fig)


# ── Q17 · Running total ──────────────────────────────────────────────────────

def chart_q17(con, mo):
    df = con.execute(
        """
        WITH yearly AS (
            SELECT CAST(year_added AS INTEGER) AS year_added,
                   COUNT(*) AS titles_added
            FROM netflix WHERE year_added IS NOT NULL
            GROUP BY year_added
        )
        SELECT year_added,
               SUM(titles_added) OVER (ORDER BY year_added) AS cumulative_total
        FROM yearly ORDER BY year_added
        """
    ).df()
    df["year_str"] = df["year_added"].astype(str)
    try:
        import altair as alt
        return (
            alt.Chart(df)
            .mark_bar(cornerRadius=4, color="#e50914")
            .encode(
                x=alt.X("year_str:N", title="Year"),
                y=alt.Y("cumulative_total:Q", title="Total Titles on Platform"),
                tooltip=["year_str", "cumulative_total"],
            )
            .properties(title="Netflix Catalogue Growth (Cumulative)",
                        width=500, height=300)
        )
    except ImportError:
        from util_plot import plot_area
        fig = plot_area(df, x="year_added", y="cumulative_total",
                        title="Netflix Catalogue Growth (Cumulative)")
        return mo.as_html(fig)


# ── Q19 · Year-over-year growth ──────────────────────────────────────────────

def chart_q19(con, mo):
    df = con.execute(
        """
        WITH yearly AS (
            SELECT CAST(year_added AS INTEGER) AS year_added,
                   COUNT(*) AS titles
            FROM netflix WHERE year_added IS NOT NULL
            GROUP BY year_added
        ),
        with_lag AS (
            SELECT year_added, titles,
                   LAG(titles) OVER (ORDER BY year_added) AS prev
            FROM yearly
        )
        SELECT year_added,
               ROUND((titles - prev) * 100.0 / NULLIF(prev, 0), 1) AS yoy_growth_pct
        FROM with_lag
        WHERE prev IS NOT NULL
        ORDER BY year_added
        """
    ).df()
    df["year_str"] = df["year_added"].astype(str)
    try:
        import altair as alt
        return (
            alt.Chart(df)
            .mark_bar(cornerRadius=4, color="#e50914")
            .encode(
                x=alt.X("year_str:N", title="Year"),
                y=alt.Y("yoy_growth_pct:Q", title="YoY Growth (%)"),
                tooltip=["year_str", "yoy_growth_pct"],
            )
            .properties(title="Year-over-Year Content Growth Rate (%)",
                        width=500, height=280)
        )
    except ImportError:
        from util_plot import plot_bar_simple
        fig = plot_bar_simple(df, x="year_added", y="yoy_growth_pct",
                              title="YoY Growth Rate (%)")
        return mo.as_html(fig)
