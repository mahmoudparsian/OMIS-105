import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 9: Capstone Project Specification & Starter Template

    ## OMIS 105 — Database Management Systems
    **Week 9 | Due: Week 10 (presentation)**

    ---

    ## Overview

    Design, implement, and present a **complete relational database
    system** for a real-world domain of your choosing. This project
    integrates all concepts from Weeks 1–8.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Deliverables

    | # | Deliverable | Weight | Format |
    |---|-------------|--------|--------|
    | 1 | ER Diagram | 15% | Image or ASCII in notebook |
    | 2 | Normalized Schema (CREATE TABLE) | 15% | SQL in notebook |
    | 3 | Sample Data | 10% | CSV files or INSERT statements |
    | 4 | 10 SQL Queries | 25% | SQL in notebook with output |
    | 5 | Transaction Demo | 10% | Python function in notebook |
    | 6 | Views (2+) and Indexes (3+) | 10% | SQL in notebook |
    | 7 | Presentation | 15% | 5–8 minutes, live demo |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Requirements

    **Database Design**
    - Minimum **5 tables**
    - At least one **1:M** relationship
    - At least one **M:M** relationship (with junction table)
    - Schema must be in **3NF** (document your normalization check)
    - Use appropriate **constraints**: PK, FK, NOT NULL, CHECK, UNIQUE, DEFAULT

    **Sample Data**
    - At least **20 rows** per main entity table
    - Data must be **meaningful and realistic** (not "test1", "test2")
    - Include variety: different statuses, date ranges, edge cases

    **SQL Queries (10 total)** — each must include a comment explaining
    its **business purpose**, the **SQL code**, and the **output**:

    | Category | Minimum Count |
    |----------|--------------|
    | Basic SELECT with WHERE, ORDER BY | 2 |
    | JOINs (INNER, LEFT, multi-table) | 3 |
    | GROUP BY with HAVING or CASE | 2 |
    | Window functions or CTEs | 2 |
    | Transaction (Python function) | 1 |

    **Views and Indexes**
    - At least **2 views** with justification
    - At least **3 indexes** with justification (explain which queries
      they help)

    **Transaction**
    - Must be a **multi-step** operation (3+ SQL statements)
    - Must include **error handling** (try/except with ROLLBACK)
    - Must demonstrate both **success** and **failure** cases
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Suggested Domains

    | Domain | Key Entities |
    |--------|-------------|
    | Restaurant Management | Menus, Items, Orders, Tables, Staff, Reservations |
    | Fitness Gym | Members, Classes, Trainers, Rooms, Bookings, Payments |
    | Music Streaming | Artists, Albums, Songs, Users, Playlists, Listening History |
    | Hospital/Clinic | Patients, Doctors, Appointments, Prescriptions, Departments |
    | Library System | Books, Authors, Members, Loans, Fines, Branches |
    | Airline Booking | Flights, Passengers, Bookings, Aircraft, Airports, Crew |
    | Hotel Management | Rooms, Guests, Reservations, Services, Invoices |
    | Online Learning | Courses, Students, Instructors, Enrollments, Assignments, Grades |

    You may also propose your own domain — clear it with the instructor
    first.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Starter Template

    Fill in each section below with your own domain. Every code cell
    below is written to run cleanly even before you touch it — any SQL
    that still contains a literal `...` placeholder, or that fails
    because something it depends on hasn't been built yet, prints a TODO
    notice and is skipped instead of crashing the notebook. Replace the
    placeholders bit by bit, re-running as you go.

    **Your Name:**
    **Domain:**
    **Date:**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Requirements Analysis

    **Purpose of this database:**
    (Describe what your database will manage)

    **Target users:**
    (Who will use this system?)

    **Key questions the database should answer:**
    1.
    2.
    3.
    4.
    5.

    **Business rules:**
    1.
    2.
    3.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: ER Diagram

    Draw your ER diagram below (or attach an image). Include:
    - All entities with attributes
    - Primary keys
    - Relationships with cardinality (1:1, 1:M, M:M)
    - Junction tables for M:M relationships

    ```
    (Paste your ASCII ER diagram here, or describe it)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Schema Design (CREATE TABLE)
    """)
    return


@app.cell
def _():
    import duckdb
    import re as _re
    import pandas as _pd

    def _has_placeholder(_sql):
        # `...` is a fill-in placeholder unless it only appears inside comments
        _s = _re.sub(r"--[^\n]*", "", _sql)
        _s = _re.sub(r"/\*.*?\*/", "", _s, flags=_re.DOTALL)
        return "..." in _s

    class _Skipped:
        # stand-in result for an un-filled (placeholder) query
        def show(self, *a, **k):
            print("   (query not run yet — fill in the `...` first)")
        def fetchone(self, *a, **k):
            return None
        def fetchall(self, *a, **k):
            return []
        def df(self, *a, **k):
            return _pd.DataFrame()
        def fetchdf(self, *a, **k):
            return _pd.DataFrame()

    class _TemplateConn:
        """Wraps DuckDB so unfinished (`...`) queries are skipped with a TODO
        message instead of raising a parser error — lets the template run
        end-to-end before every blank is filled in."""
        def __init__(self, _c):
            self._c = _c
        def execute(self, _sql, *a, **k):
            if isinstance(_sql, str) and _has_placeholder(_sql):
                print("⏳ TODO: complete this query (it still contains `...`).")
                return _Skipped()
            try:
                return self._c.execute(_sql, *a, **k)
            except Exception as _e:
                print(f"   (query skipped — depends on something not built yet: {_e})")
                return _Skipped()
        def sql(self, _sql, *a, **k):
            return self.execute(_sql, *a, **k)
        def __getattr__(self, _name):
            return getattr(self._c, _name)

    con = _TemplateConn(duckdb.connect(database=":memory:"))

    # ── Table 1: (your main entity) ──
    con.execute("""
        CREATE OR REPLACE TABLE your_table_1 (
            id  INTEGER PRIMARY KEY
            -- Add your columns here -- Use appropriate data types -- Add constraints (NOT NULL, CHECK, UNIQUE, REFERENCES)
        )
    """)

    # ── Table 2: ──
    con.execute("""
        CREATE OR REPLACE TABLE your_table_2 (
            id INTEGER PRIMARY KEY -- ...
        )
    """)

    # ── Table 3: ──
    # ...

    # ── Table 4: ──
    # ...

    # ── Table 5 (junction table for M:M): ──
    # ...

    return (con,)


@app.cell
def _(con):
    # Verify: minimum 5 tables, one M:M junction table among them
    con.execute("SHOW TABLES").fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Normalization Check

    **1NF**: (Are all values atomic? Any repeating groups?)

    **2NF**: (Any partial dependencies? Only relevant for composite keys.)

    **3NF**: (Any transitive dependencies?)

    **Intentional denormalization** (if any, justify):
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5: Load Sample Data

    At least 20 rows per main entity table, realistic and varied.
    """)
    return


@app.cell
def _(con):
    # Option A: Insert directly
    con.execute("""
        INSERT INTO your_table_1
        VALUES
            (1, ...),
            (2, ...),
            (3, ...)
    """)

    # Option B: Load from CSV
    # con.execute("INSERT INTO your_table_1 SELECT * FROM read_csv_auto('your_data.csv')")

    # Verify data loaded
    for table in ['your_table_1']:  # Add all your tables
        cnt = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        print(f"{table}: {cnt[0] if cnt else 0} rows")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6: SQL Queries (10 Required)

    ### Query 1: Basic SELECT with filtering
    """)
    return


@app.cell
def _(con):
    # Q1: (describe what this query does)
    con.execute("""
        SELECT ...
        FROM ...
        WHERE ...
        ORDER BY ...
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 2: Basic SELECT with filtering
    """)
    return


@app.cell
def _(con):
    # Q2: (describe)
    con.execute("""
        SELECT ...
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 3: INNER JOIN (multi-table)
    """)
    return


@app.cell
def _(con):
    # Q3: (describe)
    con.execute("""
        SELECT ...
        FROM ...
        INNER JOIN ... ON ...
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 4: LEFT JOIN
    """)
    return


@app.cell
def _(con):
    # Q4: (describe)
    con.execute("""
        SELECT ...
        FROM ...
        LEFT JOIN ... ON ...
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 5: 3+ Table JOIN
    """)
    return


@app.cell
def _(con):
    # Q5: (describe)
    con.execute("""
        SELECT ...
        FROM ...
        JOIN ... ON ...
        JOIN ... ON ...
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 6: GROUP BY with HAVING
    """)
    return


@app.cell
def _(con):
    # Q6: (describe)
    con.execute("""
        SELECT
            ...,
            COUNT(*),
            ...
        FROM ...
        GROUP BY ...
        HAVING ...
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 7: Aggregation with CASE
    """)
    return


@app.cell
def _(con):
    # Q7: (describe)
    con.execute("""
        SELECT
            CASE WHEN ... THEN ... END AS ...,
            COUNT(*)
        FROM ...
        GROUP BY ...
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 8: Window Function
    """)
    return


@app.cell
def _(con):
    # Q8: (describe)
    con.execute("""
        SELECT
            ...,
            ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) AS ...
        FROM ...
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 9: CTE (Common Table Expression)
    """)
    return


@app.cell
def _(con):
    # Q9: (describe)
    con.execute("""
        WITH cte_name AS (
            SELECT ...
        )
        SELECT ...
        FROM cte_name
        JOIN ...
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query 10: Complex analytical query
    """)
    return


@app.cell
def _(con):
    # Q10: (describe — combine multiple techniques)
    con.execute("""
        ...
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 7: Views (at least 2)
    """)
    return


@app.cell
def _(con):
    # View 1: (describe purpose)
    con.execute("""
        CREATE OR REPLACE VIEW your_view_1 AS
        SELECT ...
    """)
    con.execute("SELECT * FROM your_view_1 LIMIT 10").fetchdf()
    return


@app.cell
def _(con):
    # View 2: (describe purpose)
    con.execute("""
        CREATE OR REPLACE VIEW your_view_2 AS
        SELECT ...
    """)
    con.execute("SELECT * FROM your_view_2 LIMIT 10").fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 8: Indexes (at least 3)
    """)
    return


@app.cell
def _(con):
    # Index 1: (explain why this column needs an index)
    con.execute("CREATE INDEX idx_1 ON your_table(column)")

    # Index 2:
    con.execute("CREATE INDEX idx_2 ON your_table(column)")

    # Index 3:
    con.execute("CREATE INDEX idx_3 ON your_table(column1, column2)")
    return


@app.cell
def _(con):
    # Verify
    con.execute("SELECT * FROM duckdb_indexes()").fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 9: Transaction Demo

    Must be a **multi-step** operation (3+ SQL statements), include
    **error handling** (try/except with ROLLBACK), and demonstrate both
    a **success** and a **failure** case.

    > This cell is shown as text, not run directly — it references
    placeholder table/column names (`...`) that would raise a Python
    `NameError`, not a SQL error, so the placeholder-skipping mechanism
    above can't catch it. Copy this into a real code cell once your
    schema exists and fill in the details.

    ```python
    # Implement a meaningful transaction for your domain
    def your_transaction(con, ...):
        try:
            con.execute("BEGIN")

            # Step 1: ...
            # Step 2: ...
            # Step 3: ...

            con.execute("COMMIT")
            print("Transaction committed")
            return True
        except Exception as e:
            con.execute("ROLLBACK")
            print(f"Transaction rolled back: {e}")
            return False

    # Test: successful case
    your_transaction(con, ...)

    # Test: failure case (triggers rollback)
    your_transaction(con, ...)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 10: Lessons Learned

    1. **What was the hardest part?**

    2. **What would you do differently?**

    3. **What did you learn about database design?**

    4. **How does this connect to real-world applications?**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Presentation Guide (5–8 minutes)

    1. **Introduction** (1 min): What is your domain? What problem does
       your database solve?
    2. **ER Diagram** (1 min): Walk through your entities and
       relationships
    3. **Schema Highlights** (1 min): Key tables, interesting
       constraints
    4. **Live Demo** (3–4 min): Run 3–4 of your best queries
    5. **Transaction Demo** (1 min): Show success and failure cases
    6. **Reflection** (30 sec): What did you learn? What would you do
       differently?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Grading Rubric

    | Criterion | Excellent (A: 90–100%) | Good (B: 80–89%) | Adequate (C: 70–79%) | Needs Work (<70%) |
    |-----------|----------------------|------------------|---------------------|-------------------|
    | **Design** | 5+ tables, proper keys, FK, 3NF verified, M:M present | 5 tables, minor normalization issues | <5 tables or not normalized | Major design flaws |
    | **Data** | 20+ rows, realistic, varied, edge cases | 20 rows, mostly realistic | <20 rows or unrealistic data | Minimal or missing data |
    | **Queries** | 10 diverse, complex, well-documented | 10 queries, some basic | <10 or mostly simple | Few or non-functional |
    | **Transaction** | Multi-step, error handling, both cases shown | Basic transaction works | Only COMMIT, no error handling | No transaction |
    | **Views/Indexes** | Justified, useful, demonstrate understanding | Present but minimal justification | Only 1 of each | Missing |
    | **Presentation** | Clear, organized, live demo, within time | Adequate, mostly clear | Disorganized or over time | Confusing or missing |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Submission

    - Upload your notebook with all code and outputs
    - Include any **CSV data files**
    - Include your **ER diagram** (image or in notebook)
    - Be prepared to **present live** in Week 10
    - **Total: 100 points** (this project counts as your Week 9/10 grade)

    **Good luck and have fun!**
    """)
    return


if __name__ == "__main__":
    app.run()
