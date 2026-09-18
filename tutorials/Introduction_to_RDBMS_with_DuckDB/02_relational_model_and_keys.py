import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="02 - Relational Model & Keys")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 02 · The Relational Model & Keys

    Notebook **2 of 12** · estimated time: **12 minutes**.

    Before writing more SQL, you need the vocabulary. This notebook
    covers what an RDBMS actually *is*, and introduces the schema
    we'll use for the rest of the course.

    By the end you will be able to:

    - Use the terms **relation / tuple / attribute** correctly
    - Define **primary key**, **candidate key**, **composite key**,
      **foreign key**, and **referential integrity**
    - Read the 5-table e-commerce schema this whole course is built on
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## "Relational" vocabulary

    RDBMS = **R**elational **D**ata**b**ase **M**anagement **S**ystem.
    The formal theory (from E. F. Codd, 1970) uses precise terms that
    map onto the everyday words you'd guess:

    | Formal term | Everyday term | Example |
    |---|---|---|
    | **Relation** | Table | `customers` |
    | **Tuple** | Row / record | one specific customer |
    | **Attribute** | Column / field | `email` |
    | **Domain** | The set of legal values for a column | `unit_price` must be a non-negative decimal |
    | **Schema** | The structure (table + column definitions) | `customers(customer_id, first_name, ...)` |
    | **Instance** | The actual data in the tables right now | the 30 rows currently in `customers` |

    A **relational database** is a set of tables, related to each
    other through shared column values — not through pointers,
    nesting, or position. That last part is the whole idea: a row in
    `orders` doesn't *contain* a customer, it just stores a
    `customer_id` value that happens to match a row in `customers`.
    That's a **foreign key**, and it's what the next section is about.

    ## Keys

    - **Primary key (PK)** — one or more columns that uniquely
      identify each row in a table. No two rows may share a primary
      key value, and it can't be `NULL`. Every table should have one.
    - **Candidate key** — *any* column (or column combination) that
      *could* serve as the primary key (unique + non-null). A table
      can have several candidate keys; you pick one to be the PK. In
      `customers`, both `customer_id` and `email` are candidate keys —
      we chose `customer_id` as the PK and kept `email` unique as a
      backup guarantee.
    - **Composite key** — a primary key made of *more than one*
      column. In `order_items`, no single column is unique (the same
      `order_id` appears in several rows, and the same `product_id`
      appears in many orders) — but the *pair* `(order_id,
      product_id)` is unique. That pair is a composite primary key.
    - **Foreign key (FK)** — a column (or columns) in one table that
      must match a primary key value in another table (or be `NULL`,
      if allowed). This is how tables *relate* to each other.
    - **Referential integrity** — the guarantee, enforced by the
      database itself, that every foreign key value actually points
      to a row that exists. DuckDB checks this for you and will
      reject an `INSERT` that would break it — you'll see this happen
      in notebook 08.

    ## This course's schema

    Every notebook from here on uses the same small e-commerce
    database — five tables, built once into a persistent file,
    `ecommerce_database.duckdb`, by running `./create_database.sh`
    (see notebook 03). Because that script always regenerates the same
    seeded data, the file's contents are identical no matter when — or
    how many times — you build it. Here's the shape of it:

    ```
    customers                employees (self-referencing!)
    ├─ customer_id  PK        ├─ employee_id  PK
    ├─ first_name             ├─ first_name
    ├─ last_name              ├─ last_name
    ├─ email        UNIQUE    ├─ title
    ├─ city                   └─ manager_id   FK → employees.employee_id
    ├─ state
    └─ signup_date       products
                         ├─ product_id    PK
    orders               ├─ product_name
    ├─ order_id     PK   ├─ category
    ├─ customer_id  FK → customers.customer_id
    ├─ employee_id  FK → employees.employee_id
    ├─ order_date         ├─ unit_price
    └─ ship_city          └─ in_stock

    order_items
    ├─ order_id     FK → orders.order_id  ┐
    ├─ product_id   FK → products.product_id ├─ PK is the PAIR (composite)
    ├─ quantity                            │
    └─ unit_price                          ┘
    ```

    `orders` sits "between" `customers` and `employees`; `order_items`
    sits between `orders` and `products`. This many-tables-linked-by-keys
    shape — not one giant flat table — is the heart of the relational
    model, and *why* (notebook 09 will show the alternative, and why
    it's worse).

    Let's stop reading about it and look at the real thing. The cell
    below connects to the shared course database and asks DuckDB's own
    system catalog to describe its tables back to us.
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect("ecommerce_database.duckdb", read_only=True)
    con.sql("SHOW TABLES")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Five tables now exist inside `con` — already loaded with sample
    data (notebook 03 covers how). For now we only care about their
    *structure*: DuckDB keeps metadata about every table in **system
    catalog** views — `duckdb_columns()` and `duckdb_constraints()` —
    which you can query with ordinary SQL. Pick a table below to
    inspect it:
    """)
    return


@app.cell
def _(mo):
    table_picker = mo.ui.dropdown(
        options=["customers", "employees", "products", "orders", "order_items"],
        value="order_items",
        label="Inspect table",
    )
    table_picker
    return (table_picker,)


@app.cell
def _(con, mo, table_picker):
    columns_df = con.sql(
        f"""
        SELECT column_name, data_type, is_nullable
        FROM duckdb_columns()
        WHERE table_name = '{table_picker.value}'
        ORDER BY column_index
        """
    ).df()

    constraints_df = con.sql(
        f"""
        SELECT constraint_type, constraint_column_names
        FROM duckdb_constraints()
        WHERE table_name = '{table_picker.value}'
        ORDER BY constraint_type
        """
    ).df()

    mo.vstack(
        [
            mo.md(f"**Columns of `{table_picker.value}`**"),
            columns_df,
            mo.md(f"**Constraints on `{table_picker.value}`**"),
            constraints_df,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice `order_items`: DuckDB reports its `PRIMARY KEY` constraint
    as covering **two** columns, `[order_id, product_id]` — that's the
    composite key from the diagram above, confirmed straight from the
    database itself rather than just prose.

    > ⚠️ **A gotcha to notice now:** the query above builds SQL with an
    > f-string (`f"...WHERE table_name = '{table_picker.value}'..."`).
    > That's fine here because `table_picker` only ever holds one of
    > five values *we* defined. Building SQL by pasting in arbitrary
    > *user-typed* text this way is how **SQL injection**
    > vulnerabilities happen. The fix — parameterized queries — shows
    > up in notebook 04.

    ## Exercise

    Answer these using the diagram and the live inspector above.
    """)
    return


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "customer_id",
            "email",
            "(customer_id, email) together",
        ],
        label="2.1 — What is the PRIMARY KEY of `customers`?",
    )
    q2 = mo.ui.radio(
        options=[
            "It has no foreign keys",
            "manager_id is a foreign key referencing employees.employee_id — the table references itself",
            "employee_id is a foreign key referencing customers.customer_id",
        ],
        label="2.2 — What's special about the foreign key in `employees`?",
    )
    q3 = mo.ui.radio(
        options=[
            "order_id alone",
            "product_id alone",
            "the pair (order_id, product_id)",
        ],
        label="2.3 — What uniquely identifies a row in `order_items`?",
    )
    mo.vstack([q1, q2, q3])
    return q1, q2, q3


@app.cell(hide_code=True)
def _(mo, q1, q2, q3):
    def _check(question, chosen, correct):
        if chosen is None:
            return mo.md(f"_{question}: not answered yet_")
        ok = chosen == correct
        icon = "✅" if ok else "❌"
        return mo.md(f"{icon} **{question}** — you chose: *{chosen}*" + ("" if ok else f"  \n&nbsp;&nbsp;&nbsp;&nbsp;correct answer: *{correct}*"))

    mo.vstack(
        [
            _check("2.1", q1.value, "customer_id"),
            _check(
                "2.2",
                q2.value,
                "manager_id is a foreign key referencing employees.employee_id — the table references itself",
            ),
            _check("2.3", q3.value, "the pair (order_id, product_id)"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recap

    - A relational database is a set of **tables** (relations) linked
      by matching **key** values, not by nesting or position.
    - **Primary key** = uniquely identifies each row. **Foreign key**
      = a pointer to another table's primary key. **Composite key** =
      a primary key spanning more than one column.
    - DuckDB enforces these as real constraints you can query via
      `duckdb_columns()` / `duckdb_constraints()`.

    ➡️ **Next:** `03_creating_tables_and_loading_data.py` — write the
    `CREATE TABLE` statements yourself and load real data in.
    """)
    return


if __name__ == "__main__":
    app.run()
