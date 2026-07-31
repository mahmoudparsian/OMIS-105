import marimo

__generated_with = "0.23.10"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SQL WHERE Clause Builder
    # Learn Filtering with Interactive Widgets
    ---

    * **Course:** OMIS 105 — Database Management
    * **Environment:** DuckDB (in-memory) + Marimo UI Widgets

    ---

    ### What You Will Learn

    The `WHERE` clause is how you **filter rows** in SQL.
    This notebook lets you build WHERE clauses visually —
    pick a column, choose an operator, enter a value,
    and watch the SQL query run in real time.

    ### Operator Reference

    | Operator | Meaning | Example |
    |----------|---------|---------|
    | `=` | Equals | `WHERE price = 29.99` |
    | `!=` | Not equals | `WHERE category != 'Books'` |
    | `>` | Greater than | `WHERE price > 50` |
    | `<` | Less than | `WHERE stock < 50` |
    | `>=` | Greater or equal | `WHERE rating >= 4.0` |
    | `<=` | Less or equal | `WHERE price <= 100` |
    | `LIKE` | Pattern match | `WHERE product_name LIKE '%phone%'` |
    | `IN` | In a list | `WHERE category IN ('Books', 'Home')` |
    | `BETWEEN` | In a range | `WHERE price BETWEEN 20 AND 80` |

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Setup — Create Our Product Database
    ---
    """)
    return


@app.cell(hide_code=True)
def _():
    import duckdb
    from where_builder import query_with_where, query_with_two_conditions

    con = duckdb.connect()

    con.execute("""
    CREATE TABLE products (
        product_id    INT PRIMARY KEY,
        product_name  VARCHAR(50),
        category      VARCHAR(20),
        price         DECIMAL(8,2),
        stock         INT,
        rating        DECIMAL(3,1)
    );

    INSERT INTO products VALUES
        (1,  'Laptop',        'Electronics', 999.99, 25,  4.5),
        (2,  'Headphones',    'Electronics',  79.99, 150, 4.2),
        (3,  'T-Shirt',       'Clothing',     24.99, 200, 3.8),
        (4,  'Running Shoes', 'Clothing',     89.99, 75,  4.6),
        (5,  'Python Book',   'Books',        39.99, 60,  4.9),
        (6,  'SQL Guide',     'Books',        34.99, 45,  4.7),
        (7,  'Coffee Maker',  'Home',        149.99, 30,  4.1),
        (8,  'Desk Lamp',     'Home',         29.99, 90,  3.5),
        (9,  'Smartphone',    'Electronics', 699.99, 50,  4.4),
        (10, 'Backpack',      'Clothing',     49.99, 120, 4.0),
        (11, 'Cookbook',       'Books',        22.99, 80,  4.3),
        (12, 'Blender',       'Home',         69.99, 40,  3.9);
    """)

    print("Product database created: 12 products, 4 categories")
    print("DuckDB version:", duckdb.__version__)
    return con, query_with_two_conditions, query_with_where


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Our Dataset: 12 Products

    Here is the complete `products` table. The WHERE clause builder
    below will let you filter this data using any column and operator.
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _df = con.execute("""
    SELECT *
    FROM products
    ORDER BY product_id;
    """).df()

    mo.ui.table(_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Section 1: Build Your Own WHERE Clause

    Use the three controls below to build a SQL WHERE clause.
    Pick a **column**, choose an **operator**, and type a **value**.
    The query runs automatically!

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    col_picker = mo.ui.dropdown(
        options=["product_name", "category", "price", "stock", "rating"],
        value="price",
        label="1. Pick a Column",
    )

    op_picker = mo.ui.dropdown(
        options=["=", "!=", ">", "<", ">=", "<=", "LIKE", "IN", "BETWEEN"],
        value=">=",
        label="2. Pick an Operator",
    )

    val_input = mo.ui.text(
        value="50",
        label="3. Enter a Value",
    )

    mo.hstack([col_picker, op_picker, val_input], justify="start", gap=1)
    return col_picker, op_picker, val_input


@app.cell(hide_code=True)
def _(mo, op_picker):
    _hints = {
        "=":       "Enter a single value. Text: `Electronics` | Number: `29.99`",
        "!=":      "Enter a value to exclude. Example: `Books` or `0`",
        ">":       "Enter a number. Example: `50` (finds values greater than 50)",
        "<":       "Enter a number. Example: `100` (finds values less than 100)",
        ">=":      "Enter a number. Example: `4.0` (finds 4.0 and above)",
        "<=":      "Enter a number. Example: `50` (finds 50 and below)",
        "LIKE":    "Use `%` as wildcard. Example: `%phone%` (contains phone) or `S%` (starts with S)",
        "IN":      "Comma-separated list. Example: `Books, Home` or `29.99, 39.99`",
        "BETWEEN": "Two values with comma. Example: `20, 80` (between 20 and 80)",
    }

    _hint = _hints.get(op_picker.value, "")
    mo.md(f"**Hint:** {_hint}")
    return


@app.cell(hide_code=True)
def _(col_picker, con, mo, op_picker, query_with_where, val_input):
    _md, _df = query_with_where(con, col_picker.value, op_picker.value, val_input.value)
    _table = mo.ui.table(_df) if _df is not None else mo.md("")
    mo.vstack([mo.md(_md), _table])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Section 2: Quick Examples

    Not sure what to try? Pick a pre-built example below.
    Each one demonstrates a different operator.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    example_picker = mo.ui.dropdown(
        options=[
            "Price over $50",
            "Electronics only",
            "Name contains 'Book'",
            "Rating 4.5 and above",
            "Books or Home categories",
            "Price between $20 and $80",
            "Low stock (under 50)",
            "Not Clothing",
            "Name starts with S",
        ],
        value="Price over $50",
        label="Pick an example query",
    )
    example_picker
    return (example_picker,)


@app.cell(hide_code=True)
def _(con, example_picker, mo):
    _examples = {
        "Price over $50":
            "SELECT * FROM products WHERE price > 50 ORDER BY price DESC",
        "Electronics only":
            "SELECT * FROM products WHERE category = 'Electronics' ORDER BY product_id",
        "Name contains 'Book'":
            "SELECT * FROM products WHERE product_name LIKE '%Book%' ORDER BY product_id",
        "Rating 4.5 and above":
            "SELECT * FROM products WHERE rating >= 4.5 ORDER BY rating DESC",
        "Books or Home categories":
            "SELECT * FROM products WHERE category IN ('Books', 'Home') ORDER BY category, product_name",
        "Price between $20 and $80":
            "SELECT * FROM products WHERE price BETWEEN 20 AND 80 ORDER BY price",
        "Low stock (under 50)":
            "SELECT * FROM products WHERE stock < 50 ORDER BY stock",
        "Not Clothing":
            "SELECT * FROM products WHERE category != 'Clothing' ORDER BY product_id",
        "Name starts with S":
            "SELECT * FROM products WHERE product_name LIKE 'S%' ORDER BY product_id",
    }

    _sql = _examples.get(example_picker.value, "SELECT * FROM products")
    _df = con.execute(_sql).df()

    mo.vstack([
        mo.md(f"""
    **{example_picker.value}**
    ```sql
    {_sql};
    ```
    **Result:** {len(_df)} product(s)
        """),
        mo.ui.table(_df),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Section 3: Two-Condition Filter (AND / OR)

    Real queries often combine **two or more conditions**.
    Use `AND` when **both** must be true. Use `OR` when
    **either** can be true.

    Build a two-condition WHERE clause below!

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    col_a = mo.ui.dropdown(
        options=["product_name", "category", "price", "stock", "rating"],
        value="category",
        label="Column",
    )
    op_a = mo.ui.dropdown(
        options=["=", "!=", ">", "<", ">=", "<=", "LIKE"],
        value="=",
        label="Operator",
    )
    val_a = mo.ui.text(value="Electronics", label="Value")

    connector = mo.ui.radio(
        options=["AND", "OR"],
        value="AND",
        label="Combine with:",
    )

    col_b = mo.ui.dropdown(
        options=["product_name", "category", "price", "stock", "rating"],
        value="price",
        label="Column",
    )
    op_b = mo.ui.dropdown(
        options=["=", "!=", ">", "<", ">=", "<=", "LIKE"],
        value="<",
        label="Operator",
    )
    val_b = mo.ui.text(value="500", label="Value")

    mo.vstack([
        mo.md("**Condition 1:**"),
        mo.hstack([col_a, op_a, val_a], justify="start", gap=1),
        mo.hstack([mo.md(""), connector], justify="start"),
        mo.md("**Condition 2:**"),
        mo.hstack([col_b, op_b, val_b], justify="start", gap=1),
    ])
    return col_a, col_b, connector, op_a, op_b, val_a, val_b


@app.cell(hide_code=True)
def _(
    col_a,
    col_b,
    con,
    connector,
    mo,
    op_a,
    op_b,
    query_with_two_conditions,
    val_a,
    val_b,
):
    _md, _df = query_with_two_conditions(
        con,
        col_a.value, op_a.value, val_a.value,
        col_b.value, op_b.value, val_b.value,
        logic=connector.value,
    )
    _table = mo.ui.table(_df) if _df is not None else mo.md("")
    mo.vstack([mo.md(_md), _table])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Section 4: Challenge — Try It Yourself!

    Use the WHERE Clause Builder (Section 1) or the Two-Condition
    Filter (Section 3) to answer these questions:

    1. **Which products cost less than $30?**

    2. **Which products have a rating of 4.5 or higher?**

    3. **Find all products with "Book" in the name** (hint: use LIKE with %)

    4. **Which Electronics products cost less than $100?** (hint: use AND)

    5. **Which products are in the Books or Home category?** (hint: use IN)

    6. **Find products priced between $25 and $75** (hint: use BETWEEN)

    7. **Which non-Clothing products have more than 50 in stock?** (hint: use AND with !=)

    Scroll up and try each one!

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    ### Operators You Learned

    | Operator | What It Does | When to Use It |
    |----------|-------------|----------------|
    | `=` | Exact match | Find a specific value |
    | `!=` | Exclude a value | Remove unwanted rows |
    | `>` `<` `>=` `<=` | Compare numbers | Price ranges, age limits |
    | `LIKE` | Pattern matching | Search by partial name |
    | `IN` | Match a list | Multiple categories at once |
    | `BETWEEN` | Range of values | Price ranges, date ranges |
    | `AND` | Both conditions true | Narrow results (stricter) |
    | `OR` | Either condition true | Widen results (broader) |

    ### Key Takeaway

    The WHERE clause is the **most important filtering tool** in SQL.
    Every business question that says "show me only..." or "find all..."
    translates to a WHERE clause. The widgets in this notebook work
    exactly like the filter panels in business tools like Tableau,
    Power BI, and Salesforce — they all generate SQL behind the scenes!

    ---
    *Notebook by Professor M. Parsian — Santa Clara University*
    """)
    return


@app.cell(hide_code=True)
def _():
    print("SQL WHERE Clause Builder — complete!")
    return


if __name__ == "__main__":
    app.run()
