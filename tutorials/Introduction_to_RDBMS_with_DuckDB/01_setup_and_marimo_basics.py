import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="01 - Setup & Marimo Basics")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 01 · Setup & Marimo Basics

    Welcome! This is notebook **1 of 12** in *Introduction to RDBMS with
    DuckDB*. Estimated time: **10 minutes**.

    By the end of this notebook you will be able to:

    - Explain what makes a marimo notebook different from a Jupyter notebook
    - Run cells, use interactive UI elements, and watch reactivity in action
    - Run your first SQL query against DuckDB, two different ways

    ---

    ## What is marimo?

    Marimo is a **reactive** Python notebook. A regular `.py` file, no
    hidden JSON, that plays nicely with `git diff`. Three things make it
    different from Jupyter:

    1. **It's just Python.** This whole notebook is one file you could
       run with `python 01_setup_and_marimo_basics.py`, `git diff`, or
       import from another script.
    2. **Cells form a dependency graph, not a list.** Jupyter cells run
       in whatever order *you* click them, and can leave stale variables
       behind. Marimo reads each cell's code, figures out which
       variables it *reads* and which it *defines*, and re-runs cells
       automatically, in dependency order, whenever an input changes.
    3. **No hidden state.** If you delete a cell, every variable it
       defined disappears everywhere. What you see is genuinely what
       would run top to bottom.

    This matters for an RDBMS course because we'll be building up a
    shared database connection (`con`) across many cells — reactivity
    means you can never accidentally query a table that no longer
    exists, or a stale copy of one.

    ## How to run this notebook

    You're probably already looking at this rendered as read-only
    output. To actually **edit and run** it yourself, open a terminal
    in this folder and run:

    ```bash
    marimo edit 01_setup_and_marimo_basics.py
    ```

    This opens an editable, interactive version in your browser. Try
    that now, then come back to this file (or follow along in the
    editor directly).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reactivity, live

    Drag the slider below. Notice that the *next* cell — which just
    displays `quantity` and a computed total — updates automatically.
    You never re-ran it yourself; marimo saw that the display cell
    **reads** `quantity`, so it reran that cell for you the moment the
    slider changed.
    """)
    return


@app.cell
def _(mo):
    quantity = mo.ui.slider(start=1, stop=20, value=3, label="Order quantity")
    quantity
    return (quantity,)


@app.cell
def _(mo, quantity):
    unit_price = 24.99
    mo.md(
        f"""
        `quantity` is currently **{quantity.value}**.

        {quantity.value} × ${unit_price} = **${quantity.value * unit_price:,.2f}**
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Under the hood, `quantity` is a cell **output** (the slider widget)
    *and* a Python variable holding a `mo.ui.slider` object; its current
    value lives at `quantity.value`. This "UI element as a variable"
    pattern is how every interactive control in marimo works, and
    we'll lean on it heavily to build interactive SQL query tools later
    in the course.

    ## Your first DuckDB query

    [DuckDB](https://duckdb.org) is an **embedded, in-process
    relational (SQL) database** — think "SQLite for analytics." No
    server to install or manage: `import duckdb` and you have a full
    SQL engine running inside this Python process. That's what makes it
    perfect for learning RDBMS concepts hands-on.

    There are two equally valid ways to run SQL against DuckDB from
    Python / marimo. You'll see both used throughout this course.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Method 1 — the plain DuckDB Python API
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=":memory:")
    result_1 = con.sql("SELECT 42 AS answer, 'hello rdbms' AS message").df()
    result_1
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `con` is a **connection** to an in-memory DuckDB database — a
    completely empty database that lives only in this process's
    memory. `con.sql(...)` runs a query and returns a relation; `.df()`
    materializes it as a pandas DataFrame, which marimo renders as a
    nice interactive table.

    This is the standard way to talk to *any* database from Python
    (DuckDB, Postgres, SQLite, ...) — the exact same pattern works
    outside marimo, in a plain script or a web app.

    ### Method 2 — marimo's native SQL cells

    Marimo also has a **built-in SQL cell type**, backed by DuckDB by
    default, that you can create right inside the editor (right-click a
    cell → "Turn into SQL cell", or use the `+ SQL` button in the UI).
    It looks like this:
    """)
    return


@app.cell
def _(con, mo):
    result_2 = mo.sql(
        f"""
        SELECT 42 AS answer, 'hello again' AS message
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That cell's code is `mo.sql("...", engine=con)` — a normal Python
    call that marimo's editor generates for you automatically when you
    use a SQL cell in the UI. Passing `engine=con` tells it to run
    against *our* connection (instead of marimo's own default
    in-memory database), so it sees the same tables as Method 1.

    **Why two methods?** `con.sql(...)` is the portable, "real Python"
    way — it's what you'd write in a script, a data pipeline, or any
    non-marimo project. `mo.sql(...)` is a marimo-specific convenience:
    inside the interactive editor it gets you SQL syntax highlighting,
    autocomplete on table/column names, and one-click table previews.
    We'll mostly use `con.sql(...).df()` in these notebooks (it reads
    the same whether you're in marimo or not), and call out `mo.sql`
    again when it's especially handy.

    ## Exercise

    Try editing the SQL text below (it's a live `mo.ui.text_area`) and
    watch the result update. Some ideas: change the arithmetic, add
    another column, or try `SELECT current_date`.
    """)
    return


@app.cell
def _(mo):
    exercise_query = mo.ui.text_area(
        value="SELECT 6 * 7 AS the_answer",
        label="Exercise 1.1 — edit this SQL, then click outside the box",
        full_width=True,
        rows=3,
    )
    exercise_query
    return (exercise_query,)


@app.cell
def _(con, exercise_query, mo):
    def _run_exercise():
        query = exercise_query.value.strip()
        if not query:
            return mo.md("_Type a query above to see results._")
        try:
            return con.sql(query).df()
        except Exception as e:
            return mo.callout(mo.md(f"**SQL error:** {e}"), kind="danger")

    _run_exercise()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "💡 Solution / a worked example": mo.md(
                """
                There's no single "right answer" here — any valid SQL
                expression works. A couple of examples:

                ```sql
                SELECT 6 * 7 AS the_answer
                ```

                ```sql
                SELECT current_date AS today, 'DuckDB' AS engine
                ```

                If you see a red error box, read the message — DuckDB's
                error messages are unusually specific and are one of the
                best ways to learn SQL syntax. We'll intentionally trigger
                a few more later in the course (notebook 08).
                """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - Marimo notebooks are reactive `.py` files: cells re-run
      automatically based on a dependency graph, not click order.
    - `mo.ui.*` elements (like `slider` and `text_area`) are Python
      objects whose `.value` drives the rest of the notebook.
    - DuckDB is an embedded SQL engine; `con.sql(query).df()` is the
      workhorse pattern we'll use throughout the course.
    - `mo.sql(query, engine=con)` is marimo's native SQL-cell flavor of
      the same thing.

    ➡️ **Next:** `02_relational_model_and_keys.py` — what actually
    *is* a relational database, and the vocabulary (tables, rows,
    keys) you need before writing real queries.
    """)
    return


if __name__ == "__main__":
    app.run()
