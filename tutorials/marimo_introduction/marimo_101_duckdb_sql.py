import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 🌊 Marimo 101: Your First Steps with Marimo + DuckDB

    * **Course:** OMIS 105 — Introduction to Database Management Systems
    * **Instructor:** Dr. Mahmoud Parsian
    * **Goal:** learn what Marimo is and how to explore data with SQL —
      no notebook experience required.

    ---

    ## What Is Marimo?

    **Marimo** is a tool for writing and running Python and SQL in small,
    connected blocks called **cells**. You are looking at a Marimo
    notebook right now.

    Unlike a Word document, a Marimo notebook is *alive*: cells run code,
    and results (tables, charts, text) appear right below them.

    ## Why Do We Use It in This Course?

    * It runs **SQL** directly, using a fast, built-in database engine
      called **DuckDB**.
    * It **reacts** automatically: change one cell, and every cell that
      depends on it updates — no "Run All" needed.
    * Notebooks are plain **Python files** (`.py`), so they work well
      with git and are easy to share.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## How to Run This Notebook

    1. Open a terminal in the folder that holds this file.
    2. Run:

    ```
    marimo edit marimo_101_duckdb_sql.py
    ```

    3. Your browser opens with the notebook, ready to edit and run.

    **To run a cell:** click the ▷ (play) button on the cell, or press
    **Cmd+Enter** (Mac) / **Ctrl+Enter** (Windows) while your cursor is
    inside it.

    Don't worry about breaking anything — feel free to experiment as you
    go. You can always undo with **Cmd/Ctrl+Shift+Z**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 1. Cells React to Each Other

    A notebook is built from cells. Some hold **Python**, some hold
    **SQL**. When a cell changes, Marimo automatically re-runs every
    cell that depends on it — like a spreadsheet recalculating formulas.

    Let's see this with a small example: a slider controlling a price
    calculation.
    """)
    return


@app.cell
def _(mo):
    quantity = mo.ui.slider(1, 20, value=3, label="How many notebooks?")
    quantity
    return (quantity,)


@app.cell
def _(mo, quantity):
    price_per_item = 4.50
    total = quantity.value * price_per_item

    mo.md(f"""
    If notebooks cost **${price_per_item}** each, and you buy
    **{quantity.value}**, the total is **${total:.2f}**.

    👉 **Try it:** drag the slider above and watch this text update
    automatically — no "Run All" required. That's reactivity!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 2. Meet DuckDB

    **DuckDB** is a database engine that lives inside Python — no server
    to install, no login required. It's fast, free, and perfect for
    learning SQL.

    Marimo has a special kind of cell just for talking to DuckDB: a
    **SQL cell**. Let's connect first.
    """)
    return


@app.cell
def _():
    # Python cell — create an in-memory DuckDB connection
    import duckdb

    con = duckdb.connect(database=":memory:")
    print("DuckDB version:", duckdb.__version__)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3. SQL Cells: `mo.sql()`

    A SQL cell in Marimo looks like a Python cell, but the code inside
    is SQL, wrapped by a call to `mo.sql(...)`. The result appears as a
    table, and any table you `CREATE` becomes available to every cell
    below it — just like a Python variable.

    Let's create a small table for a campus bookstore.
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- SQL cell: define the shape of the table
        CREATE OR REPLACE TABLE products (
            product_id   INTEGER,
            product_name VARCHAR,
            category     VARCHAR,
            price        DECIMAL(6,2),
            in_stock     INTEGER
        );
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    We just told DuckDB: *"Create a table called `products` with five
    columns."* But the table is still empty — let's add data.
    """)
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        -- SQL cell: add rows to the table
        INSERT INTO products (product_id, product_name, category, price, in_stock) VALUES
            (1,  'Spiral Notebook',           'Supplies',    4.50, 120),
            (2,  'Gel Pen (4-pack)',          'Supplies',    6.25,  80),
            (3,  'Laptop Stand',              'Electronics',29.99,  15),
            (4,  'Wireless Mouse',            'Electronics',19.99,  25),
            (5,  'SCU Hoodie',                'Apparel',    45.00,  40),
            (6,  'SCU Cap',                   'Apparel',    18.00,  60),
            (7,  'Scientific Calculator',     'Electronics',24.99,  10),
            (8,  'OMIS 105 Textbook',         'Books',      85.00,  30),
            (9,  'Ceramic Mug',               'Apparel',     9.50,  50),
            (10, 'Noise-Canceling Headphones','Electronics',59.99,   8);
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Now let's **look** at our data. `SELECT * FROM products` means
    *"show me everything in the products table."*
    """)
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        SELECT *
        FROM   products
        ORDER BY product_id;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Asking Questions with SQL

    SQL stands for **Structured Query Language**. It's how you ask a
    database to answer business questions. SQL reads almost like
    English.

    **Question 1:** *"What Electronics do we sell?"*
    """)
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        SELECT product_name,
               price,
               in_stock
        FROM   products
        WHERE  category = 'Electronics';
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Read that out loud: *"Select the product name, price, and stock
    from products where the category is Electronics."* Almost plain
    English!

    ---

    **Question 2:** *"What are our five cheapest items?"*
    """)
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        SELECT product_name,
               category,
               price
        FROM   products
        ORDER BY price ASC
        LIMIT 5;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    **Question 3:** *"How many products, and what's the average price,
    in each category?"*

    `GROUP BY` groups rows together; `COUNT(*)` and `AVG()` summarize
    each group.
    """)
    return


@app.cell
def _(mo, products):
    _df = mo.sql(
        f"""
        SELECT category,
               COUNT(*)         AS num_products,
               ROUND(AVG(price), 2) AS avg_price
        FROM   products
        GROUP BY category
        ORDER BY num_products DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 4. The Best Part: Interactive SQL

    Because Marimo is reactive, you can wire a UI control — like a
    dropdown — directly into a SQL query. Pick a category below, and
    the table updates instantly. No button, no re-run.
    """)
    return


@app.cell
def _(mo):
    category_picker = mo.ui.dropdown(
        options=["Supplies", "Electronics", "Apparel", "Books"],
        value="Electronics",
        label="Choose a category:",
    )
    category_picker
    return (category_picker,)


@app.cell
def _(category_picker, mo, products):
    _df = mo.sql(
        f"""
        SELECT product_name,
               price,
               in_stock
        FROM   products
        WHERE  category = '{category_picker.value}'
        ORDER BY price DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Change the dropdown above and watch the table react — instantly,
    with no button to click. This pattern (a UI element feeding an
    f-string SQL query) is how you'll build interactive dashboards
    later in the course.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 5. Zooming Out: What Is a Database?

    `products` is one **table**. A real database usually has several
    tables that relate to each other — customers, orders, products —
    connected by shared columns (like `product_id`). That's what
    "relational" means.

    ![Relational Database Management System](../../images/rdbms_image.jpg)

    You'll build multi-table databases like this starting in Week 2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Recap: What You Just Learned

    - ✅ A Marimo notebook is made of **cells** that **react** to each other
    - ✅ Python cells run Python; **SQL cells** run SQL against **DuckDB**
    - ✅ `CREATE TABLE`, `INSERT`, and `SELECT` are your first three SQL commands
    - ✅ `WHERE`, `ORDER BY`, and `GROUP BY` filter, sort, and summarize data
    - ✅ UI elements (like dropdowns) can drive SQL queries live

    ## Where to Go Next

    - Edit any SQL cell above and re-run it (Cmd/Ctrl+Enter) — you can't break anything
    - Explore Marimo's own guided tour: `marimo_introduction.py`, in this same folder
    - Run `marimo tutorial sql` in your terminal for Marimo's official SQL tutorial
    - Practice more in `outline-10-weeks/sql_notebooks/`, the notebooks used in class

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
