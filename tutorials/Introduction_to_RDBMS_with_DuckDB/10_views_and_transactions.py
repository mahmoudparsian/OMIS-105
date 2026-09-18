import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="10 - Views & Transactions")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 10 · Views & Transactions

    Notebook **10 of 12** · estimated time: **10 minutes**.

    Objectives:

    - Save a reusable query as a `VIEW`, and understand it isn't a
      copy of the data
    - Run a real, hands-on transaction: `BEGIN`, `COMMIT`, `ROLLBACK`
    - See exactly what "Atomicity" (notebook 08's ACID) means when a
      statement fails partway through
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect("ecommerce_database.duckdb")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The demos below insert real rows and create a real view in the
    shared course database, so that everything you see is really
    happening — not a simulation. That also means, unlike a
    throwaway in-memory database, this file will still remember what
    you did the *next* time you open this notebook. So this next
    cell resets anything those demos leave behind, using nothing
    fancier than `DELETE` and `DROP VIEW` — plain SQL you already
    know — so you can re-run this notebook as many times as you like:
    """)
    return


@app.cell
def _(con):
    con.execute("DELETE FROM order_items WHERE order_id = 9001")
    con.execute("DELETE FROM orders WHERE order_id = 9001")
    con.execute("DELETE FROM customers WHERE customer_id IN (501, 502, 503, 600)")
    con.execute("DROP VIEW IF EXISTS customer_order_totals")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `CREATE VIEW` — a saved query, not a saved copy

    We've written this "total spend per customer" query shape more
    than once already (notebook 07). A **view** lets you save it
    under a name and query that name like a table:
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE VIEW customer_order_totals AS
        SELECT c.customer_id, c.first_name, c.last_name,
               count(DISTINCT o.order_id) AS n_orders,
               coalesce(sum(oi.quantity * oi.unit_price), 0) AS total_spend
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        """
    )
    con.sql("SELECT * FROM customer_order_totals ORDER BY total_spend DESC LIMIT 5")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Crucially, a view stores the **query**, not a frozen result. It
    re-runs against live data every time you select from it. Let's
    prove that: insert a brand-new customer with zero orders, and
    query the view again.
    """)
    return


@app.cell
def _(con):
    con.execute(
        "INSERT INTO customers VALUES (600, 'Nova', 'Zed', 'nova.zed@example.com', 'Remote', 'NA', current_date)"
    )
    con.sql("SELECT * FROM customer_order_totals WHERE customer_id = 600")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Customer #600 didn't exist when the view was created, yet it
    shows up immediately with `n_orders = 0` — because
    `customer_order_totals` isn't data, it's a saved `SELECT`
    statement that runs fresh every time. Views are how you give a
    complex, correct query a name once, so everyone downstream
    (other queries, a BI tool, a report) can reuse it without
    retyping or subtly getting the joins wrong.

    ## Transactions — grouping statements into one atomic unit

    Every `INSERT`/`UPDATE`/`DELETE` you've run so far has been its
    own tiny, automatic transaction. A **transaction** lets you group
    *several* statements so that they all succeed together, or none
    of them take effect at all — no in-between state, ever.

    - `BEGIN TRANSACTION` — start grouping statements
    - `COMMIT` — make everything since `BEGIN` permanent
    - `ROLLBACK` — undo everything since `BEGIN`, as if it never ran

    ### Demo 1 — start, then change your mind
    """)
    return


@app.cell
def _(con):
    con.execute("BEGIN TRANSACTION")
    con.execute(
        "INSERT INTO customers VALUES (501, 'Temp', 'Rollback', 'temp501@example.com', 'X', 'XX', current_date)"
    )
    mid_txn_count = con.sql("SELECT count(*) FROM customers WHERE customer_id = 501").fetchone()[0]
    con.execute("ROLLBACK")
    after_rollback_count = con.sql("SELECT count(*) FROM customers WHERE customer_id = 501").fetchone()[0]
    f"Inside the transaction: {mid_txn_count} row. After ROLLBACK: {after_rollback_count} rows."
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The row genuinely existed — queryable, real — for as long as the
    transaction was open. `ROLLBACK` erased it completely, as if the
    `INSERT` had never run. Compare with committing instead:

    ### Demo 2 — start, then make it permanent
    """)
    return


@app.cell
def _(con):
    con.execute("BEGIN TRANSACTION")
    con.execute(
        "INSERT INTO customers VALUES (502, 'Temp', 'Commit', 'temp502@example.com', 'X', 'XX', current_date)"
    )
    con.execute("COMMIT")
    con.sql("SELECT * FROM customers WHERE customer_id = 502")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Demo 3 — what happens when one statement fails mid-transaction

    This is the demo that really shows *why* transactions exist.
    We'll `BEGIN`, successfully insert one valid row, then
    deliberately insert a row that violates a constraint (a
    duplicate primary key, from notebook 08) — and watch what DuckDB
    does next.
    """)
    return


@app.cell
def _(con, mo):
    con.execute("BEGIN TRANSACTION")
    con.execute(
        "INSERT INTO customers VALUES (503, 'Temp', 'PartialWork', 'temp503@example.com', 'X', 'XX', current_date)"
    )
    step1 = "✅ First INSERT succeeded (customer 503 exists, inside the open transaction)."

    try:
        con.execute(
            "INSERT INTO customers VALUES (503, 'Duplicate', 'Id', 'dup503@example.com', 'X', 'XX', current_date)"
        )
        step2 = "This shouldn't happen — duplicate id 503 should fail."
    except Exception as e:
        step2 = f"❌ Second INSERT failed as expected: {type(e).__name__}: {e}"

    try:
        con.sql("SELECT 1").fetchone()
        step3 = "Query succeeded (unexpected)."
    except Exception as e:
        step3 = f"⚠️ Even a harmless SELECT now fails: {type(e).__name__}: {e}"

    mo.md(f"1. {step1}\n2. {step2}\n3. {step3}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    DuckDB doesn't just reject the *one* bad statement and let you
    carry on — the entire transaction is marked **aborted** the
    moment anything inside it fails. Every subsequent statement,
    even a harmless `SELECT`, is refused until you explicitly
    `ROLLBACK`. There is no way to `COMMIT` a partial result out of
    it. Let's clean up:
    """)
    return


@app.cell
def _(con):
    con.execute("ROLLBACK")
    con.sql("SELECT count(*) AS customer_503_exists FROM customers WHERE customer_id = 503")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Zero. Even the *first* `INSERT` — the one that succeeded on its
    own — got undone, because it was part of the same transaction as
    the one that failed. **This is Atomicity** (notebook 08's "A"):
    the group of statements is all-or-nothing. It's exactly the
    behavior you want for something like "insert a new order, then
    insert its line items" — you'd never want a database containing
    an order with zero items just because the second `INSERT` hit a
    typo.

    ## Exercise

    Using a transaction, insert a new order (`order_id = 9001`,
    pick any existing `customer_id` and `employee_id`) together with
    two `order_items` rows for it. Then, on purpose, make one of the
    `order_items` rows invalid (e.g. a `product_id` that doesn't
    exist) so the transaction fails, catch the error, `ROLLBACK`,
    and confirm **none** of it — not even the order — was saved.
    """)
    return


@app.cell
def _(mo):
    ex1 = mo.ui.text_area(
        placeholder=(
            "BEGIN TRANSACTION;\n"
            "INSERT INTO orders VALUES (9001, 1, 4, current_date, 'Nowhere');\n"
            "INSERT INTO order_items VALUES (9001, 1, 2, 10.00);\n"
            "INSERT INTO order_items VALUES (9001, 99999, 1, 5.00);  -- bad product_id"
        ),
        label="10.1 — one statement at a time works best; try them via the button below",
        full_width=True,
        rows=6,
    )
    ex1
    return (ex1,)


@app.cell
def _(mo):
    run_button = mo.ui.run_button(
        label="Run these statements as one transaction"
    )
    run_button
    return (run_button,)


@app.cell
def _(con, ex1, mo, run_button):
    def _execute_all():
        if not run_button.value:
            return mo.md("_Click the button above to run._")
        statements = [s.strip() for s in ex1.value.split(";") if s.strip()]
        log = []
        try:
            for stmt in statements:
                con.execute(stmt)
                log.append(f"✅ ran: `{stmt[:70]}`")
        except Exception as e:
            log.append(f"❌ {type(e).__name__}: {e}")
            con.execute("ROLLBACK")
            log.append("🔄 Rolled back — nothing from this transaction was saved.")
        log.append(
            f"\n\n`order_id = 9001` exists afterwards: "
            f"{con.sql('SELECT count(*) FROM orders WHERE order_id = 9001').fetchone()[0] > 0}"
        )
        return mo.md("\n\n".join(log))

    _execute_all()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "💡 Solution": mo.md(
                "```sql\n"
                "BEGIN TRANSACTION;\n"
                "INSERT INTO orders VALUES (9001, 1, 4, current_date, 'Nowhere');\n"
                "INSERT INTO order_items VALUES (9001, 1, 2, 10.00);\n"
                "INSERT INTO order_items VALUES (9001, 99999, 1, 5.00);\n"
                "```\n\n"
                "The last statement violates the FOREIGN KEY on\n"
                "`order_items.product_id` (there is no product 99999),\n"
                "which aborts the transaction. After `ROLLBACK`, even the\n"
                "order (which inserted fine on its own) is gone — atomicity\n"
                "in action."
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every notebook after this one expects the shared database back in
    its original state — 30 customers, no extra views — so let's leave
    it exactly as we found it, the same way the cleanup cell at the top
    of this notebook did:
    """)
    return


@app.cell
def _(con):
    con.execute("DELETE FROM order_items WHERE order_id = 9001")
    con.execute("DELETE FROM orders WHERE order_id = 9001")
    con.execute("DELETE FROM customers WHERE customer_id IN (501, 502, 503, 600)")
    con.execute("DROP VIEW IF EXISTS customer_order_totals")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - `CREATE VIEW name AS SELECT ...` saves a *query*, not a
      snapshot — it always reflects current data.
    - `BEGIN` / `COMMIT` / `ROLLBACK` group statements into one
      all-or-nothing unit.
    - In DuckDB, one failed statement **aborts the whole
      transaction** — every following statement is refused until you
      `ROLLBACK`, and rolling back undoes everything since `BEGIN`,
      including statements that individually succeeded.

    ➡️ **Next:** `11_duckdb_superpowers.py` — what makes DuckDB
    different from a "normal" RDBMS: querying CSV/Parquet files and
    pandas DataFrames directly with SQL, no loading step required.
    """)
    return


if __name__ == "__main__":
    app.run()
