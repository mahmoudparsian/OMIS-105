import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 04: SQL Aggregation
    ## Lab 02 — `GROUP BY` and `HAVING` in Depth (Bike Share) · Instructor

    Work with a single **bike_trips** table (4 stations, August and
    September). Builds on Lab 5 with harder aggregation patterns:
    grouping by two columns, how aggregates treat `NULL`, `HAVING` on an
    aggregate that is not in `SELECT`, counting with `CASE`, and
    grouping by an expression. Run the setup cells first, then each
    question. Answers are filled in.

    Same template as the v2 labs: Q5 (predict — `NULL` ratings and
    `COUNT`/`AVG`), Q7 (debug — the `GROUP BY` rule), Q10 (explain —
    filter in `WHERE` or `HAVING`?), Q12 (bonus).
    """)
    return

@app.cell
def _():
    import marimo as mo

    return (mo,)

@app.cell
def _(mo):
    bike_trips = mo.sql(
        f"""
        CREATE OR REPLACE TABLE bike_trips AS
        SELECT * FROM (
            VALUES
            (1,  'Main St',    'Member', 'Classic',  12, DATE '2026-08-03', 5),
            (2,  'Main St',    'Casual', 'Electric', 35, DATE '2026-08-03', 4),
            (3,  'Park Ave',   'Member', 'Electric', 18, DATE '2026-08-04', NULL),
            (4,  'University', 'Member', 'Classic',   9, DATE '2026-08-04', 3),
            (5,  'Harbor',     'Casual', 'Classic',  72, DATE '2026-08-05', 5),
            (6,  'Main St',    'Member', 'Electric', 15, DATE '2026-08-05', NULL),
            (7,  'University', 'Casual', 'Electric', 25, DATE '2026-08-06', 4),
            (8,  'Park Ave',   'Casual', 'Classic',  48, DATE '2026-08-06', 2),
            (9,  'University', 'Member', 'Classic',  11, DATE '2026-08-07', 4),
            (10, 'Harbor',     'Casual', 'Electric', 65, DATE '2026-09-01', NULL),
            (11, 'Main St',    'Member', 'Classic',  14, DATE '2026-09-01', 4),
            (12, 'Park Ave',   'Member', 'Electric', 22, DATE '2026-09-02', 5),
            (13, 'University', 'Member', 'Electric', 10, DATE '2026-09-02', NULL),
            (14, 'Harbor',     'Member', 'Classic',  30, DATE '2026-09-03', 3),
            (15, 'Main St',    'Casual', 'Classic',  40, DATE '2026-09-03', NULL),
            (16, 'University', 'Casual', 'Classic',  28, DATE '2026-09-04', 5),
            (17, 'Park Ave',   'Member', 'Classic',  16, DATE '2026-09-04', 4),
            (18, 'Main St',    'Member', 'Electric', 13, DATE '2026-09-05', 5)
        ) AS t(trip_id, station, member_type, bike_type, duration_min, trip_date, rating);
        """
    )
    return (bike_trips,)

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    `rating` is the rider's 1–5 star rating of the trip. It is `NULL`
    when the rider skipped the rating.

    ### Q1. How many trips started at each station? Show `station` and `num_trips`, busiest first.

    Expected: Main St 6, University 5, Park Ave 4, Harbor 3.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q1 = mo.sql(
        f"""
        SELECT station, COUNT(*) AS num_trips
        FROM bike_trips
        GROUP BY station
        ORDER BY num_trips DESC;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. For each `member_type`, show `num_trips` and the average trip length `avg_minutes` rounded to 1 decimal.

    Expected: Casual 7 trips / 44.7 min, Member 11 trips / 15.5 min.

    **Talking point:** a real business insight — members take many
    short commuter trips; casual riders take fewer, much longer
    (leisure) trips. Pricing teams use exactly this `GROUP BY`.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q2 = mo.sql(
        f"""
        SELECT member_type,
               COUNT(*)                   AS num_trips,
               ROUND(AVG(duration_min), 1) AS avg_minutes
        FROM bike_trips
        GROUP BY member_type
        ORDER BY member_type;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. Count trips for every `station` + `bike_type` combination. Sort by station, then bike type.

    Expected: 8 rows — Harbor (Classic 2, Electric 1), Main St (3, 3),
    Park Ave (2, 2), University (3, 2).
    """)
    return

@app.cell
def _(bike_trips, mo):
    q3 = mo.sql(
        f"""
        SELECT station, bike_type, COUNT(*) AS num_trips
        FROM bike_trips
        GROUP BY station, bike_type
        ORDER BY station, bike_type;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. Considering **Electric** bikes only, show each station's `electric_trips` and average trip length `avg_minutes` (1 decimal). Sort by station.

    Expected: Harbor 1 / 65.0, Main St 3 / 21.0, Park Ave 2 / 20.0,
    University 2 / 17.5.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q4 = mo.sql(
        f"""
        SELECT station,
               COUNT(*)                    AS electric_trips,
               ROUND(AVG(duration_min), 1) AS avg_minutes
        FROM bike_trips
        WHERE bike_type = 'Electric'
        GROUP BY station
        ORDER BY station;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. For each station, show `all_trips` (`COUNT(*)`), `rated_trips` (`COUNT(rating)`), and `avg_rating` (`AVG(rating)`, 2 decimals). Sort by station.

    🔮 **Predict first:** Main St has 6 trips, but 2 of them have a
    `NULL` rating; the other 4 ratings add up to 18. Will Main St's
    `avg_rating` be **18 / 6 = 3.00** or **18 / 4 = 4.50**?

    **Answer: 4.50.** Aggregate functions (`COUNT(col)`, `SUM`, `AVG`,
    `MIN`, `MAX`) **skip `NULL`s**. Only `COUNT(*)` counts every row.

    Expected: Harbor 3 / 2 / 4.00, Main St 6 / 4 / 4.50, Park Ave
    4 / 3 / 3.67, University 5 / 4 / 4.00.

    **Talking point:** this is usually what you want ("average of the
    ratings we have"), but the business must know that 5 of 18 trips are
    unrated — a high average from very few ratings can mislead.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q5 = mo.sql(
        f"""
        -- Predict: 4.50 -- AVG skips NULL ratings (18 / 4, not 18 / 6)
        SELECT station,
               COUNT(*)              AS all_trips,
               COUNT(rating)         AS rated_trips,
               ROUND(AVG(rating), 2) AS avg_rating
        FROM bike_trips
        GROUP BY station
        ORDER BY station;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. Show `station` and `num_trips` for stations whose **longest** trip was more than 45 minutes. (The longest trip itself does not need to be displayed.)

    Expected: Harbor 3 (longest 72), Park Ave 4 (longest 48).

    **Talking point:** `HAVING` may use an aggregate (`MAX`) that does
    not appear in `SELECT` — the filter and the displayed columns are
    independent.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q6 = mo.sql(
        f"""
        SELECT station, COUNT(*) AS num_trips
        FROM bike_trips
        GROUP BY station
        HAVING MAX(duration_min) > 45
        ORDER BY station;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. 🐞 Debug it

    Goal: number of trips per station **and** member type. Broken query:

    ```sql
    SELECT station, member_type, COUNT(*) AS num_trips
    FROM bike_trips
    GROUP BY station;
    ```

    DuckDB: `Binder Error: column "member_type" must appear in the GROUP
    BY clause or must be part of an aggregate function.`

    **The bug:** the **GROUP BY rule** — every column in `SELECT` must
    either be in `GROUP BY` or be inside an aggregate. Grouping only by
    station makes one row per station, but each station has *both*
    Member and Casual trips — SQL cannot know which single
    `member_type` to print on that one row.

    **The fix:** `GROUP BY station, member_type`.

    Expected: 8 rows — Harbor (Casual 2, Member 1), Main St (2, 4),
    Park Ave (1, 3), University (2, 3).
    """)
    return

@app.cell
def _(bike_trips, mo):
    q7 = mo.sql(
        f"""
        -- Every non-aggregated SELECT column must be in GROUP BY
        SELECT station, member_type, COUNT(*) AS num_trips
        FROM bike_trips
        GROUP BY station, member_type
        ORDER BY station, member_type;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. Counting with `CASE`: show one row per station with two columns, `member_trips` and `casual_trips`. Sort by station.

    Expected: Harbor 1 / 2, Main St 4 / 2, Park Ave 3 / 1,
    University 3 / 2.

    **Talking point:** compare with Q7 — same numbers, but "wide" (one
    row per station, a column per type) instead of "long" (one row per
    station-and-type). `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` is the
    standard trick for counting only the rows that meet a condition,
    and it reuses `CASE` from week 3.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q8 = mo.sql(
        f"""
        SELECT station,
               SUM(CASE WHEN member_type = 'Member' THEN 1 ELSE 0 END) AS member_trips,
               SUM(CASE WHEN member_type = 'Casual' THEN 1 ELSE 0 END) AS casual_trips
        FROM bike_trips
        GROUP BY station
        ORDER BY station;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Group by an expression: for each month, show `trip_month` (use `MONTH(trip_date)`), `num_trips`, and `total_minutes`. Sort by month.

    Expected: month 8 → 9 trips / 245 min; month 9 → 9 trips / 238 min.

    **Talking point:** you can `GROUP BY` a computed value, not just a
    stored column — every date in August collapses into one group.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q9 = mo.sql(
        f"""
        SELECT MONTH(trip_date)  AS trip_month,
               COUNT(*)          AS num_trips,
               SUM(duration_min) AS total_minutes
        FROM bike_trips
        GROUP BY MONTH(trip_date)
        ORDER BY trip_month;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. Run both queries below. They give the same counts.

    ```sql
    -- Query A
    SELECT station, COUNT(*) AS member_trips
    FROM bike_trips
    WHERE member_type = 'Member'
    GROUP BY station;

    -- Query B
    SELECT station, member_type, COUNT(*) AS member_trips
    FROM bike_trips
    GROUP BY station, member_type
    HAVING member_type = 'Member';
    ```

    Both return Harbor 1, Main St 4, Park Ave 3, University 3.

    ✍️ **Explain it (sample answer):** "Use `WHERE` (Query A): the
    condition is about each individual row, so it should remove the
    Casual rows *before* grouping. Query B builds Casual groups only to
    throw them away, and needs `member_type` added to `GROUP BY` just so
    `HAVING` can see it. Rule of thumb: conditions on columns go in
    `WHERE`; conditions on aggregates go in `HAVING`."
    """)
    return

@app.cell
def _(bike_trips, mo):
    q10 = mo.sql(
        f"""
        -- Prefer WHERE: it's a row condition, so filter before grouping.
        -- HAVING is for conditions on aggregates (COUNT, SUM, AVG, ...).
        SELECT station, COUNT(*) AS member_trips
        FROM bike_trips
        WHERE member_type = 'Member'
        GROUP BY station
        ORDER BY station;
        """
    )
    return

@app.cell
def _(bike_trips, mo):
    q10b = mo.sql(
        f"""
        SELECT station, member_type, COUNT(*) AS member_trips
        FROM bike_trips
        GROUP BY station, member_type
        HAVING member_type = 'Member'
        ORDER BY station;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. Which **2** stations have the most total riding time? Show `station` and `total_minutes`.

    Expected: Harbor 167, Main St 129.

    **Talking point:** Harbor has the *fewest* trips (Q1) but the most
    minutes — `ORDER BY` an aggregate + `LIMIT` answers "top N" questions.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q11 = mo.sql(
        f"""
        SELECT station, SUM(duration_min) AS total_minutes
        FROM bike_trips
        GROUP BY station
        ORDER BY total_minutes DESC
        LIMIT 2;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional)

    Looking at **Casual** riders only, which stations have an average
    trip length of **more than 30 minutes**? Show `station`,
    `casual_trips`, and `avg_minutes` (1 decimal), longest average first.

    Expected: Harbor 2 / 68.5, Park Ave 1 / 48.0, Main St 2 / 37.5
    (University, 26.5, is filtered out).

    Combines `WHERE`, `GROUP BY`, `HAVING` on `AVG`, `ROUND`, and
    `ORDER BY` — the full pipeline in one query.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q12 = mo.sql(
        f"""
        SELECT station,
               COUNT(*)                    AS casual_trips,
               ROUND(AVG(duration_min), 1) AS avg_minutes
        FROM bike_trips
        WHERE member_type = 'Casual'
        GROUP BY station
        HAVING AVG(duration_min) > 30
        ORDER BY avg_minutes DESC;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## ✅ Exit Ticket — before you submit

    (Instructor copy — read a few out loud, anonymously, next class.)
    """)
    return

@app.cell
def _():
    exit_ticket = """
    1. One thing that clicked for you today:


    2. One thing about GROUP BY / HAVING that is still fuzzy or confusing:


    """
    return (exit_ticket,)

if __name__ == "__main__":
    app.run()
