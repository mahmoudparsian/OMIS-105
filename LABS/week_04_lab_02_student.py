import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 04: SQL Aggregation
    ## Lab 02 — `GROUP BY` and `HAVING` in Depth (Bike Share) · Student

    Work with a single **bike_trips** table (4 stations, August and
    September). Builds on Lab 5 with harder aggregation patterns:
    grouping by two columns, how aggregates treat `NULL`, `HAVING` on an
    aggregate that is not in `SELECT`, counting with `CASE`, and
    grouping by an expression. Run the setup cells first, then write
    your SQL in each question cell (replace `-- YOUR SQL HERE`).

    Same pattern as before: a prediction, a bug, an explain-it, and an
    optional bonus.
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
    """)
    return

@app.cell
def _(bike_trips, mo):
    q1 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. For each `member_type`, show `num_trips` and the average trip length `avg_minutes` rounded to 1 decimal.

    What business story do the two rows tell?
    """)
    return

@app.cell
def _(bike_trips, mo):
    q2 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. Count trips for every `station` + `bike_type` combination. Sort by station, then bike type.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q3 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. Considering **Electric** bikes only, show each station's `electric_trips` and average trip length `avg_minutes` (1 decimal). Sort by station.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q4 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. For each station, show `all_trips` (`COUNT(*)`), `rated_trips` (`COUNT(rating)`), and `avg_rating` (`AVG(rating)`, 2 decimals). Sort by station.

    🔮 **Predict first:** Main St has 6 trips, but 2 of them have a
    `NULL` rating; the other 4 ratings add up to 18. Will Main St's
    `avg_rating` be **18 / 6 = 3.00** or **18 / 4 = 4.50**? And will
    `all_trips` and `rated_trips` be equal?
    """)
    return

@app.cell
def _(bike_trips, mo):
    q5 = mo.sql(
        f"""
        -- Predict: Main St avg_rating = ___
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. Show `station` and `num_trips` for stations whose **longest** trip was more than 45 minutes. (The longest trip itself does not need to be displayed.)
    """)
    return

@app.cell
def _(bike_trips, mo):
    q6 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. 🐞 Debug it

    A classmate wanted the number of trips per station **and** member
    type, and wrote:

    ```sql
    SELECT station, member_type, COUNT(*) AS num_trips
    FROM bike_trips
    GROUP BY station;
    ```

    Run it — DuckDB refuses. Read the error message, then fix the query
    (sort by station, then member type). Why can't SQL show
    `member_type` here?
    """)
    return

@app.cell
def _(bike_trips, mo):
    q7 = mo.sql(
        f"""
        -- Why can't SQL show member_type? (one sentence)
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. Counting with `CASE`: show one row per station with two columns, `member_trips` and `casual_trips`. Sort by station.

    Hint: `SUM(CASE WHEN member_type = 'Member' THEN 1 ELSE 0 END)`
    adds 1 for every Member trip and 0 for every other trip.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q8 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Group by an expression: for each month, show `trip_month` (use `MONTH(trip_date)`), `num_trips`, and `total_minutes`. Sort by month.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q9 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. Run both queries below (one per cell). They give the same counts.

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

    ✍️ **Explain it:** in one sentence, which one should you use, and
    why?
    """)
    return

@app.cell
def _(bike_trips, mo):
    q10 = mo.sql(
        f"""
        -- Explanation:
        -- Query A here
        """
    )
    return

@app.cell
def _(bike_trips, mo):
    q10b = mo.sql(
        f"""
        -- Query B here
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. Which **2** stations have the most total riding time? Show `station` and `total_minutes`.

    Compare with Q1: is the station with the most riding time also the
    busiest?
    """)
    return

@app.cell
def _(bike_trips, mo):
    q11 = mo.sql(
        f"""
        -- YOUR SQL HERE
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional — only if you finish early)

    Looking at **Casual** riders only, which stations have an average
    trip length of **more than 30 minutes**? Show `station`,
    `casual_trips`, and `avg_minutes` (1 decimal), longest average first.

    Combines `WHERE`, `GROUP BY`, `HAVING` on `AVG`, `ROUND`, and
    `ORDER BY` — the full pipeline in one query.
    """)
    return

@app.cell
def _(bike_trips, mo):
    q12 = mo.sql(
        f"""
        -- YOUR SQL HERE (bonus)
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## ✅ Exit Ticket — before you submit
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
