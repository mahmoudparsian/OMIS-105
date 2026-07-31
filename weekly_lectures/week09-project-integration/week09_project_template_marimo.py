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
    # Week 9: Capstone Project — Starter Template
    ## OMIS 105: Database Management Systems

    Use this notebook as your project template. Fill in each section with your own domain.

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
    ## Step 3: Schema Design (CREATE OR REPLACE TABLE)
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
            if isinstance(_sql, str) and _has_placeholder(_sql):
                print("⏳ TODO: complete this query (it still contains `...`).")
                return _Skipped()
            try:
                return self._c.sql(_sql, *a, **k)
            except Exception as _e:
                print(f"   (query skipped — depends on something not built yet: {_e})")
                return _Skipped()
        def __getattr__(self, _name):
            return getattr(self._c, _name)

    con = _TemplateConn(duckdb.connect())

    # ── Table 1: (your main entity) ──
    con.sql("""
        CREATE OR REPLACE TABLE your_table_1 (
            id  INTEGER PRIMARY KEY,
            -- Add your columns here -- Use appropriate data types -- Add constraints (NOT NULL, CHECK, UNIQUE, REFERENCES)
        );
    """)

    # ── Table 2: ──
    con.sql("""
        CREATE OR REPLACE TABLE your_table_2 (
            id INTEGER PRIMARY KEY -- ...
        );
    """)

    # ── Table 3: ──
    # ...

    # ── Table 4: ──
    # ...

    # ── Table 5 (junction table for M:M): ──
    # ...

    # Verify
    con.sql("SHOW TABLES").show()
    return (con,)


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
            (3, ...);
    """)

    # Option B: Load from CSV
    # con.sql("INSERT INTO your_table_1 SELECT * FROM read_csv_auto('your_data.csv')")

    # Verify data loaded
    for table in ['your_table_1']:  # Add all your tables
        cnt = con.sql(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {cnt} rows")
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
    con.sql("""
        SELECT ...
        FROM ...
        WHERE ...
        ORDER BY ...;
    """).show()
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
    con.sql("""
        SELECT ...
    """).show()
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
    con.sql("""
        SELECT ...
        FROM ...
        INNER
        JOIN ... ON ...;
    """).show()
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
    con.sql("""
        SELECT ...
        FROM ...
        LEFT
        JOIN ... ON ...;
    """).show()
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
    con.sql("""
        SELECT ...
        FROM ...
        JOIN ... ON ...
        JOIN ... ON ...;
    """).show()
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
    con.sql("""
        SELECT
            ...,
            COUNT(*),
            ...
        FROM ...
        GROUP BY ...
        HAVING ...;
    """).show()
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
    con.sql("""
        SELECT
            CASE WHEN ... THEN ... END AS ...,
            COUNT(*)
        FROM ...
        GROUP BY ...;
    """).show()
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
    con.sql("""
        SELECT
            ...,
            ROW_NUMBER() OVER (PARTITION BY ...
        ORDER BY ...) AS ...
        FROM ...;
    """).show()
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
    con.sql("""
        WITH cte_name AS (
        SELECT ... )
        SELECT ...
        FROM cte_name
        JOIN ...;
    """).show()
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
    con.sql("""
        ...
    """).show()
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
    con.sql("""
        CREATE VIEW your_view_1 AS
        SELECT ...;
    """)
    con.sql("""
        SELECT *
        FROM your_view_1
        LIMIT 10;
    """).show()
    return


@app.cell
def _(con):
    # View 2: (describe purpose)
    con.sql("""
        CREATE VIEW your_view_2 AS
        SELECT ...;
    """)
    con.sql("""
        SELECT *
        FROM your_view_2
        LIMIT 10;
    """).show()
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
    con.sql("""
        CREATE INDEX idx_1 ON your_table(column);
    """)

    # Index 2:
    con.sql("""
        CREATE INDEX idx_2 ON your_table(column);
    """)

    # Index 3:
    con.sql("""
        CREATE INDEX idx_3 ON your_table(column1, column2);
    """)

    # Verify
    con.sql("""
        SELECT *
        FROM duckdb_indexes();
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 9: Transaction Demo
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    > ⚠️ *Non-executable cell (converted to display only):*

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


if __name__ == "__main__":
    app.run()
