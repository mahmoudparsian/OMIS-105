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
    # Lab 2: Relational Thinking — Keys, Relationships, and Schema Design

    ## OMIS 105 — Database Management Systems
    **Week 2 | Estimated time: 60–90 minutes**

    ---

    ## Objectives

    - Identify primary keys, foreign keys, and candidate keys
    - Understand and classify table relationships (1:1, 1:M, M:M)
    - Create tables with proper constraints in DuckDB
    - Draw an ER diagram for a given scenario
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Connect to DuckDB and load `categories`, `products`, and `customers`
    from `./data/`. Each id column is cast to `INTEGER` and given a
    `PRIMARY KEY` — `read_csv_auto` infers `BIGINT` and adds no
    constraints, and Part 3's `REFERENCES` clauses need a same-typed
    primary/unique key on the referenced column to bind.
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
        "CREATE OR REPLACE TABLE categories AS SELECT * FROM read_csv_auto('./data/categories.csv')"
    )
    con.execute("ALTER TABLE categories ALTER COLUMN category_id TYPE INTEGER")
    con.execute("ALTER TABLE categories ADD PRIMARY KEY (category_id)")

    con.execute(
        "CREATE OR REPLACE TABLE products AS SELECT * FROM read_csv_auto('./data/products.csv')"
    )
    con.execute("ALTER TABLE products ALTER COLUMN product_id TYPE INTEGER")
    con.execute("ALTER TABLE products ADD PRIMARY KEY (product_id)")

    con.execute(
        "CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv_auto('./data/customers.csv')"
    )
    con.execute("ALTER TABLE customers ALTER COLUMN customer_id TYPE INTEGER")
    con.execute("ALTER TABLE customers ADD PRIMARY KEY (customer_id)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Key Identification (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q1.** (5 pts) For each table below, identify the primary key and
    explain why it qualifies:
    - categories
    - products
    - customers

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** (3 pts) Which column in the `products` table is a foreign key?
    What table does it reference?

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q3.** (4 pts) Is `email` in the `customers` table a candidate key?
    Write a query to prove your answer.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q3
    con.execute(
        """
        -- Your query here
        SELECT 'Q3: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** (3 pts) Give an example of when you would use a composite
    primary key. Describe the table and its columns.

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Relationship Analysis (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q5.** (6 pts) Classify each relationship and explain your reasoning:
    - categories → products
    - customers → orders (imagine an orders table)
    - products ↔ suppliers

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q6.** (4 pts) For the categories → products relationship, write a
    query that shows how many products belong to each category.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q6
    con.execute(
        """
        -- Your query here
        SELECT 'Q6: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q7.** (5 pts) If we add a `reviews` table where customers can review
    products, what type of relationship exists between:
    - customers and reviews?
    - products and reviews?
    - customers and products (through reviews)?

    *(Write your answer here.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Schema Creation (20 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q8.** (8 pts) Write a `CREATE TABLE` statement for an `orders` table
    with:
    - `order_id` as primary key
    - `customer_id` as foreign key referencing customers
    - `order_date` (DATE, not null)
    - `status` (VARCHAR, must be one of: 'processing', 'shipped',
      'completed', 'cancelled')
    - `total_amount` (DECIMAL, must be positive)
    """)
    return


@app.cell
def _(con):
    # TODO: replace the statement below to answer Q8
    con.execute(
        """
        -- Your CREATE TABLE here
        CREATE OR REPLACE TABLE orders_todo AS SELECT 'Q8: replace this statement' AS todo
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9.** (7 pts) Write a `CREATE TABLE` for an `order_items` junction
    table with:
    - `order_id` (FK to orders)
    - `product_id` (FK to products)
    - `quantity` (integer, must be > 0)
    - `unit_price` (decimal)
    - Composite primary key of (order_id, product_id)
    """)
    return


@app.cell
def _(con):
    # TODO: replace the statement below to answer Q9
    con.execute(
        """
        -- Your CREATE TABLE here
        CREATE OR REPLACE TABLE order_items_todo AS SELECT 'Q9: replace this statement' AS todo
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** (5 pts) Insert 3 sample rows into your `orders` table and 5
    sample rows into `order_items`. Verify with `SELECT` queries.
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your INSERT statements for orders and order_items
    print("Q10: add your INSERT statements here")
    return


@app.cell
def _(con):
    # TODO: verify with a SELECT
    con.execute(
        """
        -- Your query here
        SELECT 'Q10: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: Referential Integrity (10 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q11.** (5 pts) Try inserting an order with a `customer_id` that does
    not exist in the `customers` table. What happens? Explain the result.
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your INSERT attempt, then explain the result above
    print("Q11: try your INSERT here")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q12.** (5 pts) Write a query that checks if there are any products
    with a `category_id` that does not exist in the `categories` table.
    """)
    return


@app.cell
def _(con):
    # TODO: replace the query below to answer Q12
    con.execute(
        """
        -- Your query here
        SELECT 'Q12: replace this query' AS todo
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: ER Diagram (15 points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q13.** (15 pts) Draw an ER diagram (on paper or using text/ASCII art)
    for a **University Registration System** with the following entities:
    - Students (student_id, name, email, major)
    - Courses (course_id, title, credits, department)
    - Enrollments (student_id, course_id, semester, grade)
    - Instructors (instructor_id, name, department)

    Include:
    - Primary keys for each table
    - Foreign keys showing relationships
    - Cardinality labels (1:1, 1:M, or M:M)

    *(Draw your diagram here — ASCII art or attach a photo/scan with your
    submission.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 6: Challenge (5 bonus points)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q14.** Design a schema (CREATE TABLE statements) for a simple
    **music streaming service** with at least 4 tables. Include at least
    one M:M relationship with a junction table. Draw the ER diagram.
    """)
    return


@app.cell
def _(con):
    # TODO: replace with your CREATE TABLE statements for the music schema
    print("Q14 (bonus): add your CREATE TABLE statements here")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Submission

    - Submit your notebook with all queries, outputs, and ER diagrams
    - For diagram questions, include a photo/scan of hand-drawn diagrams
      or ASCII art

    **Total: 75 points (+ 5 bonus)**
    """)
    return


if __name__ == "__main__":
    app.run()
