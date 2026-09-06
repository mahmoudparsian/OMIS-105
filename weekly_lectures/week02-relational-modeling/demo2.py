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
    # 🚀 DuckDB ELITE Tutorial (OMIS 105)

    This notebook is a **flagship teaching asset**.

    Each section includes:

    1. 🧠 Business Question (Natural Language)
    2. ✍️ Student Attempt (empty)
    3. 💻 SQL Solution
    4. 📊 Result
    5. 🔍 Insight

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🔧 Setup
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
        f"""
        CREATE OR REPLACE TABLE sales AS
        SELECT * FROM (VALUES
            ('USA',    'Laptop',   5,  999.99),
            ('USA',    'Phone',   12,  699.99),
            ('USA',    'Tablet',   8,  449.99),
            ('Canada', 'Laptop',   3,  999.99),
            ('Canada', 'Phone',    7,  699.99),
            ('Canada', 'Tablet',   4,  449.99),
            ('UK',     'Laptop',   6,  999.99),
            ('UK',     'Phone',    9,  699.99),
            ('UK',     'Tablet',   2,  449.99),
            ('Mexico', 'Laptop',   2,  999.99),
            ('Mexico', 'Phone',    5,  699.99),
            ('Mexico', 'Tablet',   3,  449.99)
        ) AS t(country, product, quantity, price)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1️⃣ Show all data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🧠 Business Question
    Display all rows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✍️ Student Attempt
    _Write your SQL here_
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 💻 SQL Solution
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM sales
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Insight
    This is the full dataset view.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2️⃣ Filter USA
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🧠 Business Question
    Show all USA sales
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✍️ Student Attempt
    _Write your SQL here_
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 💻 SQL Solution
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM sales WHERE country='USA'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Insight
    WHERE filters rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3️⃣ Sort
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🧠 Business Question
    Show highest price first
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✍️ Student Attempt
    _Write your SQL here_
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 💻 SQL Solution
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM sales ORDER BY price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Insight
    ORDER BY sorts results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4️⃣ Top N
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🧠 Business Question
    Show top 3 rows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✍️ Student Attempt
    _Write your SQL here_
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 💻 SQL Solution
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM sales ORDER BY price DESC LIMIT 3
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Insight
    LIMIT applies globally.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5️⃣ Revenue
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🧠 Business Question
    Compute revenue per row
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✍️ Student Attempt
    _Write your SQL here_
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 💻 SQL Solution
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *, quantity*price AS revenue FROM sales
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Insight
    Derived columns add business meaning.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6️⃣ Aggregation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🧠 Business Question
    Revenue per country
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✍️ Student Attempt
    _Write your SQL here_
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 💻 SQL Solution
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT country, SUM(quantity*price) AS revenue
            FROM sales
            GROUP BY country
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Insight
    GROUP BY summarizes data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7️⃣ HAVING
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🧠 Business Question
    Countries with revenue > 2000
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✍️ Student Attempt
    _Write your SQL here_
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 💻 SQL Solution
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT country, SUM(quantity*price) AS revenue
            FROM sales
            GROUP BY country
            HAVING SUM(quantity*price) > 2000
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Insight
    HAVING filters aggregated results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8️⃣ Ranking
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🧠 Business Question
    Rank rows by revenue
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✍️ Student Attempt
    _Write your SQL here_
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 💻 SQL Solution
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT *, quantity*price AS revenue,
            RANK() OVER (ORDER BY quantity*price DESC) AS rnk
            FROM sales
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Insight
    RANK assigns positions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9️⃣ Top per country
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🧠 Business Question
    Top product per country
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✍️ Student Attempt
    _Write your SQL here_
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 💻 SQL Solution
    """)
    return


@app.cell
def _(r, con):
    con.execute(
        f"""
        WITH r AS (
            SELECT country, product, quantity*price AS revenue,
            RANK() OVER (PARTITION BY country ORDER BY quantity*price DESC) AS rnk
            FROM sales
            )
            SELECT * FROM r WHERE rnk=1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔍 Insight
    RANK enables per-group top-N.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧠 Final Challenge

    Write queries for:

    1. Top 2 products per country
    2. Country with lowest revenue
    3. Total units sold per product

    ---

    # 🎯 Takeaway

    - LIMIT = global
    - RANK = flexible
    - GROUP BY = summarize
    - SQL = answering questions
    """)
    return


if __name__ == "__main__":
    app.run()
