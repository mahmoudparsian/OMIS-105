import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from pathlib import Path

    import duckdb

    DATA_DIR = Path(__file__).parent / "data"
    con = duckdb.connect(database=":memory:")
    con.execute(f"""
        CREATE OR REPLACE TABLE sales_reps AS SELECT * FROM read_csv('{DATA_DIR}/sales_reps.csv')
    """)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 9 — Ranking Functions, Session 1: `ROW_NUMBER` and `RANK`

    **OMIS 105 — Introduction to Database Management Systems**

    This notebook follows `ranking_slides_1.md`. Run the cells from top to bottom.
    The setup cell loads `data/sales_reps.csv` — 12 sales reps on 3 teams
    (`sales` in thousands of dollars). Watch the **ties**: Ava and Fay (95), Ben and
    Chloe (88), Gus and Hal (60).
    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The data
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT rep_id, rep_name, team, sales
        FROM sales_reps
        ORDER BY rep_id
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `GROUP BY` gives one row per team — but no names
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT team, MAX(sales) AS top_sales
        FROM sales_reps
        GROUP BY team
        ORDER BY team
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `ROW_NUMBER()` — number the rows

    `rep_name` is the **tie-breaker**: without it, Ava and Fay could swap numbers 4 and 5.
    (`LIMIT 8` only shortens the output — it is not part of the ranking.)
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT rep_name, team, sales,
               ROW_NUMBER() OVER (ORDER BY sales DESC, rep_name) AS rn
        FROM sales_reps
        ORDER BY rn
        LIMIT 8
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `RANK()` — ties share a rank, then a gap

    Ava and Fay are both 4, so the next rep (Ben) is 6.
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT rep_name, team, sales,
               RANK() OVER (ORDER BY sales DESC) AS rnk
        FROM sales_reps
        ORDER BY rnk, rep_name
        LIMIT 8
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Side by side
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT rep_name, sales,
               ROW_NUMBER() OVER (ORDER BY sales DESC, rep_name) AS rn,
               RANK()       OVER (ORDER BY sales DESC)           AS rnk
        FROM sales_reps
        ORDER BY rn
        LIMIT 8
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `PARTITION BY` — restart at 1 for each team
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT team, rep_name, sales,
               ROW_NUMBER() OVER (PARTITION BY team
                                  ORDER BY sales DESC, rep_name) AS rn
        FROM sales_reps
        ORDER BY team, rn
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⚠️ `WHERE` cannot see `rn`

    This cell is **meant to fail** — read the error message.
    """)
    return


@app.cell
def _(con):
    try:
        con.execute("""
        SELECT rep_name, sales,
               ROW_NUMBER() OVER (ORDER BY sales DESC, rep_name) AS rn
        FROM sales_reps
        WHERE rn = 1
        """).fetchdf()
    except Exception as e:
        print("Error:", str(e).splitlines()[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Rank in a subquery, filter outside: the top rep per team
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT team, rep_name, sales
        FROM (
            SELECT team, rep_name, sales,
                   ROW_NUMBER() OVER (PARTITION BY team
                                      ORDER BY sales DESC, rep_name) AS rn
            FROM sales_reps
        ) AS ranked
        WHERE rn = 1
        ORDER BY team
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Top 2 per team with `ROW_NUMBER` — exactly 2 rows per team
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT team, rep_name, sales, rn
        FROM (
            SELECT team, rep_name, sales,
                   ROW_NUMBER() OVER (PARTITION BY team
                                      ORDER BY sales DESC, rep_name) AS rn
            FROM sales_reps
        ) AS ranked
        WHERE rn <= 2
        ORDER BY team, rn
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Top 2 per team with `RANK` — East keeps both Ben and Chloe (7 rows)
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT team, rep_name, sales, rnk
        FROM (
            SELECT team, rep_name, sales,
                   RANK() OVER (PARTITION BY team ORDER BY sales DESC) AS rnk
            FROM sales_reps
        ) AS ranked
        WHERE rnk <= 2
        ORDER BY team, rnk, rep_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⚠️ Why not just `ORDER BY … LIMIT`? Puzzle 1: the top 4 reps

    `LIMIT 4` counts **rows**. Ava and Fay tie at 95 for 4th place — only one of them fits.
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT rep_name, team, sales
        FROM sales_reps
        ORDER BY sales DESC
        LIMIT 4
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ✅ With `RANK() … WHERE rnk <= 4` both reps tied for 4th are kept (5 rows).
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT rep_name, team, sales, rnk
        FROM (
            SELECT rep_name, team, sales,
                   RANK() OVER (ORDER BY sales DESC) AS rnk
            FROM sales_reps
        ) AS ranked
        WHERE rnk <= 4
        ORDER BY rnk, rep_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Puzzle 2: the top rep in each team — `LIMIT 3`?

    3 teams, 3 rows… but `LIMIT` never restarts per team: two Central reps, no East rep.
    The fix is `PARTITION BY team` + `WHERE rn = 1` (the cell above: Ivy, Ava, Eli).
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT rep_name, team, sales
        FROM sales_reps
        ORDER BY sales DESC
        LIMIT 3
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Puzzle 3: the lowest sales — `LIMIT 1` shows Gus only, but Hal also has 60
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT rep_name, team, sales
        FROM sales_reps
        ORDER BY sales
        LIMIT 1
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ✅ `RANK() OVER (ORDER BY sales)` finds the tie for you: Gus **and** Hal.
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT rep_name, team, sales
        FROM (
            SELECT rep_name, team, sales,
                   RANK() OVER (ORDER BY sales) AS rnk
            FROM sales_reps
        ) AS ranked
        WHERE rnk = 1
        ORDER BY rep_name
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⚠️ Forgetting `PARTITION BY` — only 1 row
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
        SELECT team, rep_name, sales
        FROM (
            SELECT team, rep_name, sales,
                   ROW_NUMBER() OVER (ORDER BY sales DESC, rep_name) AS rn
            FROM sales_reps
        ) AS ranked
        WHERE rn = 1
    """).fetchdf()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Your turn

    1. Rank the reps **within each team** with `RANK()`. Which team has two reps with the same rank?
    2. Show the **bottom** rep of each team (lowest `sales`). What do you change?
    3. In the West team, Gus and Hal tie at 60. What does `ROW_NUMBER` give them, and what does `RANK` give them?
    4. A manager asks for "the top 2 reps overall". Compare `ORDER BY sales DESC LIMIT 2` with `RANK() … <= 2`. Do they agree? Would they still agree for the top 4?
    """)
    return


if __name__ == "__main__":
    app.run()
