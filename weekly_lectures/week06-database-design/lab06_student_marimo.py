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
    # Lab 6: Database Design & Normalization

    ## OMIS 105 — Database Management Systems
    **Week 6 | Estimated time: 75–90 minutes**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Connect to DuckDB and load `orders_denorm` (the denormalized table
    used throughout Parts 1–3), plus the already-normalized `categories`,
    `products`, `customers`, `orders`, and `order_items` (used in Part 5)
    from `./data/`.
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell
def _(con):
    con.execute(
        "CREATE OR REPLACE TABLE orders_denorm AS SELECT * FROM read_csv_auto('./data/orders_denormalized.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE categories AS SELECT * FROM read_csv_auto('./data/categories.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE products AS SELECT * FROM read_csv_auto('./data/products.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv_auto('./data/customers.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE orders AS SELECT * FROM read_csv_auto('./data/orders.csv')"
    )
    con.execute(
        "CREATE OR REPLACE TABLE order_items AS SELECT * FROM read_csv_auto('./data/order_items.csv')"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Functional Dependencies (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** List all functional dependencies you can identify in the
    `orders_denormalized` table. Write a query to verify at least 3 of
    them.

    *(Write your list of FDs here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below with a query that verifies one of your FDs
    con.execute(
        """
        -- Your query here
        SELECT 'Q1: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** What is the candidate key for `orders_denormalized`? Prove it
    with a query that checks uniqueness.

    *(Write your answer here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q2
    con.execute(
        """
        -- Your query here
        SELECT 'Q2: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** Classify each FD as "full," "partial," or "transitive" with
    respect to the candidate key.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Identifying Anomalies (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** Write a query that demonstrates the **redundancy** problem —
    show how many times each customer's information is repeated.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q4
    con.execute(
        """
        -- Your query here
        SELECT 'Q4: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** Describe (in words) how each of the following anomalies
    would occur in this table: update anomaly, insertion anomaly,
    deletion anomaly. Give specific examples.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Normalization (25 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6.** Decompose `orders_denormalized` into **2NF**. Write CREATE
    TABLE statements and INSERT...SELECT queries to populate each new
    table. Verify row counts.
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your 2NF CREATE TABLE statements
    con.execute(
        """
        -- Your CREATE TABLE statements here
        SELECT 'Q6: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    # TODO: replace with a query that verifies your 2NF row counts
    con.execute(
        """
        -- Your query here
        SELECT 'Q6 verify: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** Further decompose your 2NF tables into **3NF**. Show your
    CREATE TABLE statements.
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your 3NF CREATE TABLE statements
    con.execute(
        """
        -- Your CREATE TABLE statements here
        SELECT 'Q7: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8.** Is your 3NF schema also in BCNF? Explain why or why not.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: Design Challenge (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9.** Given the following denormalized table for a library,
    normalize it to 3NF:

    ```
    library_flat(
        loan_id, loan_date, return_date,
        member_id, member_name, member_email, member_phone,
        book_id, book_title, isbn, author_name, author_nationality,
        branch_id, branch_name, branch_city
    )
    ```

    List all FDs, then provide the 3NF decomposition (CREATE TABLE
    statements).

    *(List your FDs here.)*
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your 3NF CREATE TABLE statements for the library schema
    con.execute(
        """
        -- Your CREATE TABLE statements here
        SELECT 'Q9: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** Draw an ER diagram for your normalized library schema.

    *(Describe or attach your ER diagram here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Denormalization Discussion (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q11.** Create a VIEW that presents the denormalized data from your
    normalized ShopSmart tables. Show that it returns the same data as
    the original denormalized table.
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your CREATE VIEW statement
    con.execute(
        """
        -- Your CREATE VIEW here
        SELECT 'Q11: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** Describe two real-world scenarios where denormalization
    would be appropriate. For each, explain what you would denormalize
    and the trade-offs involved.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Submission

    - Submit notebook with all queries, outputs, and written explanations
    - **Total: 75 points**
    """)
    return


if __name__ == "__main__":
    app.run()
