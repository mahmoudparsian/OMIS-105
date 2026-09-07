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
    return DATA_DIR, con


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # OMIS 105 — Week NN Review: TOPIC

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    One or two sentences on what this week is about, framed as a business
    question rather than a list of syntax.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | First idea | `KEYWORD`, `KEYWORD` |
    | Second idea | `KEYWORD` |

    ### How to Use

    Run the cells from top to bottom. Every database cell takes `con`, the
    DuckDB connection created in the setup cell. Read the markdown between
    queries — it explains the *why*, not just the *how*.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Setup — Build the Database

    Delete whichever half of this section you do not need.

    **Option A — load a CSV.** Put the file in this folder's `data/`
    directory. `DATA_DIR` is resolved from the notebook's own location, so
    the folder works no matter where Marimo is launched from.

    **Option B — create the data inline.** Use `CREATE OR REPLACE TABLE ...
    AS SELECT * FROM (VALUES ...)`. No CSV, no file paths, runs anywhere.

    Whichever you choose, **build every table this notebook queries**. A week
    folder must run on its own.
    """)
    return


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE orders AS
        SELECT * FROM read_csv_auto('{DATA_DIR}/orders_data.csv');
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT 'orders_data.csv loaded!' AS status,
               COUNT(*)                  AS total_rows
        FROM   orders;
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE customers AS
        SELECT * FROM (VALUES
            (1, 'Alice', 'San Jose',    'Gold'),
            (2, 'Bob',   'Santa Clara', 'Silver'),
            (3, 'Carol', 'Cupertino',   'Gold')
        ) AS t(customer_id, customer_name, city, tier);
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM customers ORDER BY customer_id;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1.1 — First Concept

    > *Business question: "..."*

    Explain the idea in two or three short sentences before showing the SQL.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT customer_name,
               city,
               tier
        FROM   customers
        WHERE  tier = 'Gold'
        ORDER BY customer_name;
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week NN Summary

    | Concept | What It Solves |
    |---------|---------------|
    | `KEYWORD` | The business problem it answers |

    ### Looking Ahead

    One sentence connecting this week to the next.
    """)
    return


if __name__ == "__main__":
    app.run()
