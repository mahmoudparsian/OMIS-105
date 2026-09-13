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
    # Lab 2: Relational Thinking — INSTRUCTOR SOLUTIONS

    ## OMIS 105 — Database Management Systems
    **Week 2 | Answer Key**

    ---
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
    **Q1.** (5 pts) Primary keys:
    - `categories`: `category_id` — unique integer identifying each category
    - `products`: `product_id` — unique integer identifying each product
    - `customers`: `customer_id` — unique integer identifying each customer

    All are surrogate keys (auto-assigned integers with no business meaning).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q2.** (3 pts) `category_id` in `products` is a foreign key referencing
    `categories(category_id)`.
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
    con.execute(
        """
        SELECT email, COUNT(*) AS cnt
        FROM customers
        GROUP BY email
        HAVING COUNT(*) > 1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Returns 0 rows → every email is unique → email qualifies as a candidate key.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q4.** (3 pts) Give an example of when you would use a composite
    primary key. Describe the table and its columns.

    > Example: `order_items(order_id, product_id)` — neither column is
    unique alone (an order can have multiple items, a product can appear
    in multiple orders), but together they uniquely identify each line item.
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

    > - categories → products: **1:M** (one category has many products,
      each product belongs to one category)
    > - customers → orders: **1:M** (one customer can place many orders,
      each order belongs to one customer)
    > - products ↔ suppliers: **M:M** (one product can have multiple
      suppliers, one supplier can supply multiple products)
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
    con.execute(
        """
        SELECT c.category_name, COUNT(*) AS product_count
        FROM categories c, products p
        WHERE c.category_id = p.category_id
        GROUP BY c.category_name
        ORDER BY product_count DESC
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

    > - customers → reviews: **1:M** (one customer writes many reviews)
    > - products → reviews: **1:M** (one product can have many reviews)
    > - customers ↔ products (through reviews): effectively **M:M** — a
      customer can review many products, a product can be reviewed by many
      customers. The reviews table acts as a junction table with additional
      attributes (rating, text).
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
    with a primary key, a foreign key to `customers`, a not-null date, a
    `CHECK` on `status`, and a `CHECK` that `total_amount` is positive.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE OR REPLACE TABLE orders (
            order_id     INTEGER PRIMARY KEY,
            customer_id  INTEGER REFERENCES customers(customer_id),
            order_date   DATE NOT NULL,
            status       VARCHAR CHECK (status IN ('processing','shipped','completed','cancelled')),
            total_amount DECIMAL(10,2) CHECK (total_amount > 0)
        )
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Grading note**: Award full credit if all 5 constraints are present
    (PK, FK, NOT NULL, CHECK on status, CHECK on amount).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q9.** (7 pts) Write a `CREATE TABLE` for an `order_items` junction
    table with a composite primary key of `(order_id, product_id)`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE OR REPLACE TABLE order_items (
            order_id   INTEGER REFERENCES orders(order_id),
            product_id INTEGER REFERENCES products(product_id),
            quantity   INTEGER CHECK (quantity > 0),
            unit_price DECIMAL(10,2),
            PRIMARY KEY (order_id, product_id)
        )
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Q10.** (5 pts) Insert 3 sample rows into `orders` and 5 sample rows
    into `order_items`. Verify with `SELECT` queries.
    """)
    return


@app.cell
def _(con):
    con.execute("INSERT INTO orders VALUES (1, 1, '2024-06-01', 'completed', 150.00)")
    con.execute("INSERT INTO orders VALUES (2, 2, '2024-06-02', 'shipped', 75.50)")
    con.execute("INSERT INTO orders VALUES (3, 1, '2024-06-03', 'processing', 200.00)")

    con.execute("INSERT INTO order_items VALUES (1, 1, 1, 150.00)")
    con.execute("INSERT INTO order_items VALUES (2, 3, 2, 25.00)")
    con.execute("INSERT INTO order_items VALUES (2, 5, 1, 25.50)")
    con.execute("INSERT INTO order_items VALUES (3, 2, 1, 120.00)")
    con.execute("INSERT INTO order_items VALUES (3, 7, 2, 40.00)")
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM orders").fetchdf()
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM order_items").fetchdf()
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
    not exist in the `customers` table. What happens?
    """)
    return


@app.cell
def _(con):
    try:
        con.execute(
            "INSERT INTO orders VALUES (99, 9999, '2024-01-01', 'processing', 50.00)"
        )
        print("INSERT succeeded — this DuckDB build did not enforce the FK constraint.")
    except Exception as e:
        print(f"INSERT failed — DuckDB enforced the foreign key:\n{e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Note**: whether this raises depends on the DuckDB version and
    whether the referenced column has a primary/unique key (ours does, so
    it is enforced here — a `Constraint Error`). If it ever succeeds
    instead, explain that in a production DBMS this would fail. The
    concept — referential integrity — is what matters, not which error
    message appears.
    """)
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
    con.execute(
        """
        SELECT p.product_id, p.product_name, p.category_id
        FROM products p
        WHERE p.category_id NOT IN (SELECT category_id FROM categories)
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Should return 0 rows (data integrity holds).
    """)
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
    **Q13.** (15 pts) Draw an ER diagram for a **University Registration
    System**: students, courses, enrollments, instructors.

    ```
    ┌─────────────┐         ┌──────────────┐
    │ instructors │         │   students   │
    │─────────────│         │──────────────│
    │PK inst_id   │──┐      │PK student_id │──┐
    │ name        │  │      │ name         │  │
    │ department  │  │      │ email        │  │
    └─────────────┘  │      │ major        │  │
                     │      └──────────────┘  │
                ┌────┴────┐             ┌─────┴──────┐
                │ courses │             │enrollments │
                │─────────│             │────────────│
                │PK c_id  │─────────────│FK c_id     │
                │ title   │             │FK s_id     │
                │ credits │             │ semester   │
                │ dept    │             │ grade      │
                │FK inst  │             │PK(s_id,c_id│
                └─────────┘             │  ,semester)│
                                        └────────────┘
    ```

    **Relationships**:
    - instructors → courses: 1:M
    - students ↔ courses (through enrollments): M:M
    - The enrollments table is the junction table with composite PK

    **Grading**: 5 pts for correct entities/attributes, 5 pts for correct
    relationships, 5 pts for correct cardinality.
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
    **Q14.** Design a schema for a simple **music streaming service** with
    at least 4 tables and at least one M:M relationship with a junction
    table.
    """)
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE OR REPLACE TABLE artists (
            artist_id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            genre VARCHAR
        )
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE albums (
            album_id INTEGER PRIMARY KEY,
            title VARCHAR NOT NULL,
            artist_id INTEGER REFERENCES artists(artist_id),
            release_year INTEGER
        )
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE songs (
            song_id INTEGER PRIMARY KEY,
            title VARCHAR NOT NULL,
            album_id INTEGER REFERENCES albums(album_id),
            duration_seconds INTEGER
        )
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE users (
            user_id INTEGER PRIMARY KEY,
            username VARCHAR UNIQUE NOT NULL,
            email VARCHAR UNIQUE
        )
        """
    )
    # M:M -- users can have many playlists, playlists have many songs
    con.execute(
        """
        CREATE OR REPLACE TABLE playlists (
            playlist_id INTEGER PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            name VARCHAR
        )
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE playlist_songs (
            playlist_id INTEGER REFERENCES playlists(playlist_id),
            song_id INTEGER REFERENCES songs(song_id),
            position INTEGER,
            PRIMARY KEY (playlist_id, song_id)
        )
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Grading Rubric

    | Part | Points |
    |------|--------|
    | Part 1: Key Identification | 15 |
    | Part 2: Relationship Analysis | 15 |
    | Part 3: Schema Creation | 20 |
    | Part 4: Referential Integrity | 10 |
    | Part 5: ER Diagram | 15 |
    | **Subtotal** | **75** |
    | Part 6: Challenge | 5 |
    | **Maximum** | **80** |
    """)
    return


if __name__ == "__main__":
    app.run()
