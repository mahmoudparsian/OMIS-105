import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Setup Verification

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Quarter:** Fall 2026
    **Author:** Dr. Mahmoud Parsian

    ---

    If you can read this, **Marimo is working!**

    This notebook verifies that Python, DuckDB, Pandas, and Marimo
    are all installed correctly, then runs a real SQL query to prove
    everything works end-to-end.

    Works on **macOS**, **Windows**, and **Linux**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Part 1 — Environment Checks
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Check 1 — Python
    """)
    return


@app.cell
def _():
    import sys

    version = sys.version.split()[0]
    major, minor = sys.version_info.major, sys.version_info.minor

    if major >= 3 and minor >= 10:
        print(f"  [+] PASS  Python {version}")
    else:
        print(f"  [X] FAIL  Need Python 3.10+, you have {version}")
        print(f"            Download from https://www.python.org/downloads/")
    return (sys,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Check 2 — DuckDB
    """)
    return


@app.cell
def _():
    import duckdb as _duckdb

    _result = _duckdb.query("SELECT 42 AS answer").fetchone()
    assert _result[0] == 42
    print(f"  [+] PASS  DuckDB {_duckdb.__version__}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Check 3 — Pandas
    """)
    return


@app.cell
def _():
    import pandas as _pd

    print(f"  [+] PASS  Pandas {_pd.__version__}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Check 4 — Marimo
    """)
    return


@app.cell
def _(mo):
    print(f"  [+] PASS  Marimo {mo.__version__}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Check 5 — Platform Info
    """)
    return


@app.cell
def _(sys):
    import platform

    print(f"  OS:          {platform.system()} {platform.release()}")
    print(f"  Machine:     {platform.machine()}")
    print(f"  Python path: {sys.executable}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Part 2 — SQL Verification

    The real test: create a table, insert data, and query it —
    using the same `con.execute()` pattern you will use throughout the course.
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect()

    con.execute("""
        CREATE OR REPLACE TABLE test_students (
            student_id INTEGER,
            name       VARCHAR,
            major      VARCHAR,
            gpa        DECIMAL(3,2)
        )
    """)

    con.execute("""
        INSERT INTO test_students VALUES
            (1, 'Alice', 'Computer Science', 3.80),
            (2, 'Bob',   'Business',         3.20),
            (3, 'Carol', 'Mathematics',      3.95)
    """)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### SELECT * — all rows
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute("""
        SELECT * FROM test_students ORDER BY student_id
    """).df()
    mo.ui.table(_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### SELECT with WHERE — filtered rows
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute("""
        SELECT name, gpa
        FROM   test_students
        WHERE  gpa > 3.5
        ORDER BY gpa DESC
    """).df()
    mo.ui.table(_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### SELECT with COUNT — aggregate query
    """)
    return


@app.cell
def _(con, mo):
    _df = con.execute("""
        SELECT COUNT(*) AS total_students,
               ROUND(AVG(gpa), 2) AS avg_gpa,
               MIN(gpa) AS min_gpa,
               MAX(gpa) AS max_gpa
        FROM   test_students
    """).df()
    mo.ui.table(_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## You're All Set!

    If you can see Alice, Bob, and Carol in the tables above —
    **congratulations!** Python, DuckDB, Pandas, and Marimo are all working.

    **You are ready for OMIS 105. See you in class!**

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
