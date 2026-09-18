import marimo

__generated_with = "0.23.10"
app = marimo.App(
    width="medium",
    app_title="03 - Creating Tables & Loading Data",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 03 · Creating Tables & Loading Data

    Notebook **3 of 12** · estimated time: **12 minutes**.

    Objectives:

    - Understand in-memory vs. persistent DuckDB databases
    - Write `CREATE TABLE` statements with real constraints
    - Load data with `INSERT ... VALUES` and `INSERT ... SELECT`
    - Build the shared `con` database this whole course runs on
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## In-memory vs. persistent

    A DuckDB connection points at either:

    - **`:memory:`** — a database that exists only in RAM, and
      vanishes the moment the connection closes. Perfect for
      scratch work, tests, and quick demos like the one below.
    - **A file path**, e.g. `duckdb.connect("shop.duckdb")` — a real
      file on disk that persists between runs, just like a `.sqlite`
      file. You could open it again next week and your tables would
      still be there.

    This course actually uses **both**, for different reasons. The
    shared course database — the one every other notebook queries —
    is file-backed: `ecommerce_database.duckdb`, built once by running
    `./create_database.sh` from a terminal in this folder. Because
    that script always regenerates the same 30 customers, 80 orders,
    etc. from a fixed random seed, the file's contents are identical
    no matter when you build it — you get persistence *and*
    reproducibility. This notebook, though, uses a throwaway
    `:memory:` connection for the hands-on demo below, precisely
    because we *want* it to disappear the moment you're done
    experimenting with it.

    ## `CREATE TABLE`, piece by piece

    Let's build a table by hand before we automate anything. Here's a
    minimal `CREATE TABLE` for a `wishlists` table:

    ```sql
    CREATE TABLE wishlists (
        wishlist_id  INTEGER PRIMARY KEY,       -- unique row identifier
        customer_id  INTEGER NOT NULL,          -- required
        product_name VARCHAR NOT NULL,
        priority     INTEGER DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
        added_on     DATE NOT NULL DEFAULT current_date
    );
    ```

    Reading it constraint by constraint:

    - `PRIMARY KEY` — uniquely identifies each row (notebook 02)
    - `NOT NULL` — this column may never be empty/missing
    - `DEFAULT 3` — if you don't supply a value, DuckDB fills in `3`
    - `CHECK (priority BETWEEN 1 AND 5)` — DuckDB *rejects* any row
      that would violate this — enforced by the database, not by
      application code remembering to validate it
    - `DEFAULT current_date` — a function can be a default too

    Try it yourself below: this is a live SQL editor wired to a fresh,
    empty in-memory database.
    """)
    return


@app.cell
def _():
    import duckdb

    scratch_con = duckdb.connect(database=":memory:")
    return duckdb, scratch_con


@app.cell
def _(mo):
    ddl_editor = mo.ui.text_area(
        value=(
            "CREATE TABLE wishlists (\n"
            "    wishlist_id  INTEGER PRIMARY KEY,\n"
            "    customer_id  INTEGER NOT NULL,\n"
            "    product_name VARCHAR NOT NULL,\n"
            "    priority     INTEGER DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),\n"
            "    added_on     DATE NOT NULL DEFAULT current_date\n"
            ");"
        ),
        label="Run this CREATE TABLE (edit it if you like, then click outside the box)",
        full_width=True,
        rows=8,
    )
    ddl_editor
    return (ddl_editor,)


@app.cell
def _(ddl_editor, mo, scratch_con):
    def _run_ddl():
        try:
            scratch_con.execute("DROP TABLE IF EXISTS wishlists")
            scratch_con.execute(ddl_editor.value)
            scratch_con.execute(
                "INSERT INTO wishlists (wishlist_id, customer_id, product_name) "
                "VALUES (1, 7, 'Mechanical Keyboard')"
            )
            return mo.callout(
                mo.vstack(
                    [
                        mo.md("✅ Table created and one row inserted. Notice `priority` and `added_on` were auto-filled by their `DEFAULT`s:"),
                        scratch_con.sql("SELECT * FROM wishlists").df(),
                    ]
                ),
                kind="success",
            )
        except Exception as e:
            return mo.callout(mo.md(f"**SQL error:** {e}"), kind="danger")

    _run_ddl()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Try breaking it on purpose: change the `INSERT` idea in your head —
    what would happen if you tried to insert `priority = 9`? (You'll
    get a hands-on version of this in notebook 08.)

    ## Building the real course database

    Typing full `CREATE TABLE` statements for all five tables, then
    hand-typing 30+80+192 rows of `INSERT VALUES`, would be tedious
    and this course would be 10 hours long instead of 2. So
    `ecommerce_data.py` does it programmatically — but it's the exact
    same two ideas you just used by hand:

    1. **`CREATE TABLE`** statements (the schema you already explored
       in notebook 02) — see `ecommerce_data.DDL` if you want to read
       the raw SQL.
    2. **Loading rows.** Instead of `INSERT ... VALUES` one row at a
       time, we generate the data as pandas DataFrames, then use
       `con.register(name, df)` to make a DataFrame temporarily
       queryable as if it were a table, followed by:

       ```sql
       INSERT INTO customers SELECT * FROM _customers_df
       ```

       `INSERT ... SELECT` inserts the *result of a query* — here,
       "every row of this DataFrame" — instead of literal values.
       This is the standard way to bulk-load data into a real
       database.

    Let's run that process ourselves against a scratch in-memory
    database and confirm all five tables come out populated:
    """)
    return


@app.cell
def _(duckdb):
    from ecommerce_data import load_data

    con = duckdb.connect(database=":memory:")
    load_data(con)

    con.sql(
        """
        SELECT 'customers' AS table_name, count(*) AS row_count FROM customers
        UNION ALL SELECT 'employees', count(*) FROM employees
        UNION ALL SELECT 'products', count(*) FROM products
        UNION ALL SELECT 'orders', count(*) FROM orders
        UNION ALL SELECT 'order_items', count(*) FROM order_items
        """
    )
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `con` is now fully loaded — and `create_database.sh` runs this
    exact same `load_data()` function, just against a file path
    instead of `:memory:`, to build the persistent
    `ecommerce_database.duckdb` this whole course shares. Every
    notebook from here on starts the same way: `con =
    duckdb.connect("ecommerce_database.duckdb", read_only=True)` —
    the exact same `duckdb.connect(...)` call from notebook 01,
    just pointed at that already-built file (read-only, since those
    notebooks only query it) instead of `:memory:`.

    ## Exercise

    Create a new table, `reviews`, with:

    - `review_id` — integer primary key
    - `product_id` — integer, required, foreign key referencing
      `products(product_id)`
    - `customer_id` — integer, required, foreign key referencing
      `customers(customer_id)`
    - `rating` — integer, required, must be between 1 and 5
    - `comment` — text, optional
    - `review_date` — date, required, defaulting to today

    Then insert **one row** for `customer_id = 1` reviewing
    `product_id = 2` with a rating of `5`.
    """)
    return


@app.cell
def _(mo):
    reviews_editor = mo.ui.text_area(
        placeholder=(
            "CREATE TABLE reviews (\n    ...\n);\n\n"
            "INSERT INTO reviews (...) VALUES (...);"
        ),
        label="Exercise 3.1 — CREATE TABLE reviews + one INSERT",
        full_width=True,
        rows=10,
    )
    reviews_editor
    return (reviews_editor,)


@app.cell
def _(con, mo, reviews_editor):
    def _run_exercise():
        query = reviews_editor.value.strip()
        if not query:
            return mo.md("_Write your SQL above to see results._")
        try:
            con.execute("DROP TABLE IF EXISTS reviews")
            for statement in query.split(";"):
                statement = statement.strip()
                if statement:
                    con.execute(statement)
            return mo.callout(
                mo.vstack(
                    [mo.md("✅ Ran successfully. Current contents of `reviews`:"), con.sql("SELECT * FROM reviews").df()]
                ),
                kind="success",
            )
        except Exception as e:
            return mo.callout(mo.md(f"**SQL error:** {e}"), kind="danger")

    _run_exercise()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "💡 Solution": mo.md(
                """
                ```sql
                CREATE TABLE reviews (
                    review_id    INTEGER PRIMARY KEY,
                    product_id   INTEGER NOT NULL REFERENCES products(product_id),
                    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
                    rating       INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                    comment      VARCHAR,
                    review_date  DATE NOT NULL DEFAULT current_date
                );

                INSERT INTO reviews (review_id, product_id, customer_id, rating)
                VALUES (1, 2, 1, 5);
                ```

                `REFERENCES products(product_id)` inline on the column is
                shorthand for a `FOREIGN KEY` constraint — equivalent to
                writing it as a separate `FOREIGN KEY (product_id)
                REFERENCES products(product_id)` line, which is what
                `ecommerce_data.py` does for the multi-column case in
                `order_items`.
                """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - `:memory:` databases reset every run; file-backed databases
      persist. This course's shared database is file-backed
      (`ecommerce_database.duckdb`), built once by `create_database.sh`
      so every notebook sees the same data without rebuilding it.
    - `CREATE TABLE` defines columns, types, and constraints
      (`PRIMARY KEY`, `NOT NULL`, `CHECK`, `DEFAULT`, `REFERENCES`).
    - `INSERT ... VALUES` adds specific rows; `INSERT ... SELECT`
      bulk-loads the result of a query (including from a registered
      DataFrame).

    ➡️ **Next:** `04_select_where_filter_sort.py` — now that data
    exists, start querying it: `SELECT`, `WHERE`, `ORDER BY`, and more.
    """)
    return


if __name__ == "__main__":
    app.run()
