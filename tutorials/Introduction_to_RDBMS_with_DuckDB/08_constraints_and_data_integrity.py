import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="08 - Constraints & Data Integrity")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 08 · Constraints & Data Integrity

    Notebook **8 of 12** · estimated time: **10 minutes**.

    Notebook 03 introduced `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`,
    `UNIQUE`, and `CHECK` as syntax. This notebook is about *why they
    matter*: they're the database actively refusing to store bad
    data, on your behalf, every single time — not just a suggestion
    that application code has to remember to enforce.

    Objectives:

    - Deliberately trigger each kind of constraint violation and read
      DuckDB's error
    - Understand what "referential integrity" prevents in practice
    - Meet **ACID**, the four guarantees a real RDBMS gives you
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
    ## Why constraints matter: the alternative

    Without database constraints, "don't let quantity go negative"
    or "every order needs a real customer" has to be enforced
    entirely by every single piece of application code that ever
    writes to the database — a Python script here, a web form there,
    a one-off data-fix script six months from now. Miss *one* of
    those, even once, and the database now contains bad data
    forever, silently. Constraints move that responsibility into the
    database itself, where it can't be forgotten or bypassed.

    ## Watch DuckDB refuse bad data

    Pick a violation to attempt. Each one is a real `INSERT` against
    our actual `customers` / `orders` / `order_items` tables:
    """)
    return


@app.cell
def _(con, mo):
    violation_picker = mo.ui.dropdown(
        options=[
            "Duplicate PRIMARY KEY",
            "FOREIGN KEY to a customer that doesn't exist",
            "NOT NULL — missing a required column",
            "UNIQUE — duplicate email",
            "CHECK — a negative quantity",
        ],
        value="Duplicate PRIMARY KEY",
        label="Try to insert data that violates...",
    )

    existing_email = con.sql("SELECT email FROM customers LIMIT 1").fetchone()[0]

    statements = {
        "Duplicate PRIMARY KEY": (
            "INSERT INTO customers VALUES "
            "(1, 'Test', 'User', 'new-unique-email@example.com', 'X', 'XX', '2024-01-01')",
            "customer_id 1 already exists — a PRIMARY KEY can never repeat.",
        ),
        "FOREIGN KEY to a customer that doesn't exist": (
            "INSERT INTO orders VALUES (99999, 88888, 4, '2024-01-01', 'Nowhere')",
            "There is no customer_id 88888 — the FOREIGN KEY constraint on orders.customer_id blocks it.",
        ),
        "NOT NULL — missing a required column": (
            "INSERT INTO customers VALUES "
            "(9001, NULL, 'User', 'nullname@example.com', 'X', 'XX', '2024-01-01')",
            "first_name is declared NOT NULL in the schema.",
        ),
        "UNIQUE — duplicate email": (
            f"INSERT INTO customers VALUES (9002, 'Test', 'User', '{existing_email}', 'X', 'XX', '2024-01-01')",
            "That email already belongs to another customer, and email is UNIQUE.",
        ),
        "CHECK — a negative quantity": (
            "INSERT INTO order_items VALUES (1, 9, -5, 10.00)",
            "order_items.quantity has CHECK (quantity > 0).",
        ),
    }
    return statements, violation_picker


@app.cell
def _(mo, statements, violation_picker):
    mo.vstack(
        [
            violation_picker,
            mo.md(f"```sql\n{statements[violation_picker.value][0]}\n```"),
        ]
    )
    return


@app.cell
def _(con, mo, statements, violation_picker):
    def _attempt():
        sql, why = statements[violation_picker.value]
        try:
            con.execute(sql)
            return mo.callout(
                mo.md("No error — this shouldn't happen for any option here. If it does, the demo data changed."),
                kind="warn",
            )
        except Exception as e:
            return mo.callout(
                mo.md(f"**Blocked, as expected.**\n\nWhy: {why}\n\n**DuckDB's error:**\n```\n{e}\n```"),
                kind="danger",
            )

    _attempt()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every one of those `INSERT`s was individually valid *SQL syntax*
    — the problem was always about the *data*, caught at the moment
    it tried to enter the table. This is referential and domain
    integrity working exactly as designed. (And because each failed
    statement is rejected as a whole, `con`'s tables are unchanged —
    try re-running any option above and you'll get the identical
    error again, not a "now it's a duplicate of my own earlier
    attempt" error.)

    ## ACID — the four guarantees

    Constraints are how a real RDBMS keeps data *valid*. **ACID** is
    the broader set of guarantees about how it keeps data *correct*
    even under concurrent access, crashes, and multi-step updates:

    | Guarantee | Means |
    |---|---|
    | **Atomicity** | A multi-statement transaction either fully happens or fully doesn't — no half-finished updates left behind if something fails partway through |
    | **Consistency** | Every transaction leaves the database satisfying all its constraints — this notebook's whole topic |
    | **Isolation** | Two transactions running at the same time don't see each other's half-finished work |
    | **Durability** | Once a transaction commits, it survives — even a crash or power loss right after |

    You've spent this whole notebook on the "C." The next notebook
    (10) puts your hands on the "A" and "I" directly, with real
    `BEGIN` / `COMMIT` / `ROLLBACK` transactions.

    ## Exercise

    Write an `INSERT` into `order_items` that fails **specifically**
    because of the `CHECK` constraint on `unit_price` (it must be
    `>= 0`) — not any of the other constraints on that table. Confirm
    you get exactly one error, and read which constraint it names.
    """)
    return


@app.cell
def _(mo):
    ex1 = mo.ui.text_area(placeholder="INSERT INTO order_items VALUES (...)", label="8.1", full_width=True, rows=3)
    ex1
    return (ex1,)


@app.cell
def _(con, ex1, mo):
    def _run_exercise():
        stmt = ex1.value.strip()
        if not stmt:
            return mo.md("_Write an INSERT statement above._")
        try:
            con.execute(stmt)
            return mo.callout(mo.md("No error was raised — that INSERT succeeded. Adjust the values so it violates the `unit_price >= 0` CHECK."), kind="warn")
        except Exception as e:
            return mo.callout(mo.md(f"**Error (as intended):**\n```\n{e}\n```"), kind="danger")

    _run_exercise()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "💡 Solution": mo.md(
                "```sql\n"
                "INSERT INTO order_items VALUES (1, 9, 2, -10.00)\n"
                "```\n\n"
                "`product_id = 9` was chosen because it isn't already in\n"
                "order 1's items — otherwise you'd trip the composite\n"
                "PRIMARY KEY constraint instead of (or in addition to) the\n"
                "CHECK constraint you're aiming for. Any unused product_id\n"
                "for that order, with a negative unit_price, works."
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, and `CHECK`
      are enforced by DuckDB itself, on every write, unconditionally.
    - A rejected `INSERT` changes nothing — constraint violations
      fail atomically, not partially.
    - **ACID** (Atomicity, Consistency, Isolation, Durability) is the
      full set of correctness guarantees a real RDBMS provides.

    ➡️ **Next:** `09_normalization.py` — why the data is split into
    five linked tables instead of one big spreadsheet-style table,
    and what goes wrong if you don't.
    """)
    return


if __name__ == "__main__":
    app.run()
