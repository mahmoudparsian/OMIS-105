import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from plot_helpers import (
        plot_bar,
        plot_donut,
        plot_hbar,
        plot_join_counts,
        plot_stacked_bar,
    )

    return plot_bar, plot_donut, plot_hbar, plot_join_counts, plot_stacked_bar


@app.cell
def _(mo):
    import duckdb

    # Open the database built by ./create_duckdb_database.sh.
    # read_only=True: queries can read the tables, but nothing in
    # this notebook can change them.
    db_path = mo.notebook_dir() / "authors_books_orders.duckdb"
    if not db_path.exists():
        raise FileNotFoundError(
            f"{db_path} not found. Build it first:  ./create_duckdb_database.sh"
        )
    con = duckdb.connect(database=str(db_path), read_only=True)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Authors / Books / Orders: Learning SQL Joins

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### About This Database

    A small online bookstore with 3 tables:

    | Table | Rows | Columns | Links to |
    |-------|-----:|---------|----------|
    | `authors` | 6  | author_id, name, email, age, country | — |
    | `books`   | 20 | book_id, author_id, title, category, publication_year | `books.author_id` → `authors.author_id` |
    | `orders`  | 80 | order_id, book_id, sale_price, order_date | `orders.book_id` → `books.book_id` |

    So the chain is: **authors → books → orders**. One author writes
    many books. One book can be sold many times.

    On purpose, the data has gaps, the way real data usually does:

    - **2 authors have no books:** Priya Sharma and Omar Haddad.
    - **4 books were never ordered:** B06, B12, B17, B20.
    - Authors do not write the same number of books (8, 6, 4, 2, 0, 0).

    These gaps are why `INNER JOIN`, `LEFT JOIN`, and `RIGHT JOIN`
    give *different* answers here. **Watch the row counts.**

    ### The Plan

    | Part | Queries | Focus |
    |------|---------|-------|
    | 1. Meet the data | V1–V3 | Look at each table |
    | 2. A little aggregation | A1–A3 | COUNT, SUM, AVG, MIN, MAX, GROUP BY |
    | 3. INNER JOIN `A ⋈ B` | J1–J5 | Only rows that match on both sides |
    | 4. LEFT JOIN `A ⟕ B` | J6–J9 | Keep every row from the left table |
    | 5. RIGHT JOIN `A ⟖ B` | J10–J12 | Keep every row from the right table |
    | 6. Finding what is missing | M1–M4 | LEFT/RIGHT JOIN + `IS NULL` |

    ### Read-Only

    The notebook opens `authors_books_orders.duckdb` in **read-only**
    mode. You can run any `SELECT` you like. You cannot break the
    data by accident. If the file is missing, build it first with
    `./create_duckdb_database.sh`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Setup — Confirm the Database Opened

    You should see 6 authors, 20 books, and 80 orders.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT 'authors' AS table_name, COUNT(*) AS row_count FROM authors
        UNION ALL SELECT 'books',  COUNT(*) FROM books
        UNION ALL SELECT 'orders', COUNT(*) FROM orders
        ORDER BY table_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Proof that it is read-only

    The next cell tries to add a new author. DuckDB refuses, because
    we opened the file with `read_only=True`.
    """)
    return


@app.cell
def _(con, mo):
    try:
        con.execute("""
            INSERT INTO authors VALUES
            (7, 'Test Person', 'test@example.com', 30, 'Canada');
        """)
        read_only_result = mo.md("The INSERT worked — the database is **not** read-only.")
    except Exception as err:
        read_only_result = mo.md(f"**Refused, as expected:** `{err}`")
    read_only_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # PART 1 — MEET THE DATA

    Before you join tables, look at each one by itself. Notice the
    **key columns** — they are what the joins will match on.

    ---

    ## V1 — The `authors` table

    > *"Show every author."*

    6 rows. Remember `author_id` 5 and 6 — they will matter later.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT author_id, name, email, age, country
        FROM   authors
        ORDER BY author_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## V2 — The `books` table

    > *"Show every book."*

    20 rows. Each book has an `author_id`. Look at that column:
    you see 1, 2, 3, and 4 — but **never 5 or 6**.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT book_id, author_id, title, category, publication_year
        FROM   books
        ORDER BY book_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## V3 — The `orders` table

    > *"Show every order."*

    80 rows. Each order has a `book_id`. An order does **not** hold the
    book's title or the author's name. To get those, we need a join.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT order_id, book_id, sale_price, order_date
        FROM   orders
        ORDER BY order_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # PART 2 — A LITTLE AGGREGATION

    An **aggregate function** turns many rows into one value:
    `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. Add `GROUP BY` to get one
    value *per group*.

    ---

    ## A1 — Books per category

    > *"How many books do we have in each category? How old and how new are they?"*

    `GROUP BY category` makes one group per category. `COUNT(*)`
    counts the rows in each group.
    """)
    return


@app.cell
def _(con, mo):
    df_categories = mo.sql(
        f"""
        SELECT category,
               COUNT(*)              AS num_books,
               MIN(publication_year) AS oldest,
               MAX(publication_year) AS newest
        FROM   books
        GROUP BY category
        ORDER BY num_books DESC, category;
        """,
        engine=con
    )
    return (df_categories,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Chart — Books per category

    Each slice is one category's share of the 20 books.
    """)
    return


@app.cell
def _(df_categories, plot_donut):
    plot_donut(df_categories, labels="category", values="num_books",
               title="Books per category")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A2 — Sales summary

    > *"How many orders, how much revenue, and what is the average price?"*

    No `GROUP BY` here, so the whole table is **one** group, and we
    get one row back: 80 orders, $2,699 total.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*)                  AS num_orders,
               SUM(sale_price)           AS total_revenue,
               ROUND(AVG(sale_price), 2) AS avg_price,
               MIN(sale_price)           AS lowest_price,
               MAX(sale_price)           AS highest_price
        FROM   orders;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A3 — Top 5 best-selling books

    > *"Which 5 books sold the most copies?"*

    This works, but look at the answer: **B03, B01, B07…** Which books
    are those? Who wrote them? The `orders` table cannot tell us.
    The title is in `books`, and the name is in `authors`.

    That is exactly the problem a **JOIN** solves.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT book_id,
               COUNT(*)        AS copies_sold,
               SUM(sale_price) AS revenue
        FROM   orders
        GROUP BY book_id
        ORDER BY copies_sold DESC, book_id
        LIMIT 5;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # PART 3 — INNER JOIN `A ⋈ B`

    ```sql
    SELECT ...
    FROM   A
    INNER JOIN B ON A.key = B.key;
    ```

    An `INNER JOIN` keeps a row **only when it matches on both sides**.
    Rows with no partner are dropped — silently. (`JOIN` alone means
    `INNER JOIN`.)

    **Table aliases.** `authors AS a` lets us write `a.name` instead of
    `authors.name`. Short, and it says clearly which table a column
    comes from.

    ---

    ## J1 — Every book with its author's name

    > *"List each book with the name of the author who wrote it."*

    **20 rows** — one per book. Now look for Priya Sharma and Omar
    Haddad. They are **gone**: they have no books, so they have nothing
    to match.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT b.book_id,
               b.title,
               b.category,
               a.name AS author
        FROM   authors AS a
        INNER JOIN books AS b ON a.author_id = b.author_id
        ORDER BY b.book_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J2 — Every order with its book title

    > *"For each order, show the title and category of the book sold."*

    **80 rows** — one per order. The 4 books nobody bought (B06, B12,
    B17, B20) do not appear: they have no order to match.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT o.order_id,
               o.order_date,
               b.title,
               b.category,
               o.sale_price
        FROM   orders AS o
        INNER JOIN books AS b ON o.book_id = b.book_id
        ORDER BY o.order_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J3 — Three tables: order + book + author

    > *"For each order, show the book title AND the author's name."*

    You can chain joins. First `orders` joins `books` (on `book_id`),
    then that result joins `authors` (on `author_id`). Each `ON`
    follows one link in the chain **orders → books → authors**.

    Still **80 rows**.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT o.order_id,
               o.order_date,
               b.title,
               a.name AS author,
               o.sale_price
        FROM   orders  AS o
        INNER JOIN books   AS b ON o.book_id   = b.book_id
        INNER JOIN authors AS a ON b.author_id = a.author_id
        ORDER BY o.order_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J4 — Top 5 best-selling books, now with titles

    > *"Which 5 books sold the most copies — and what are they called?"*

    This is A3 again, fixed with a join. **JOIN first, then GROUP BY.**
    Every column in `SELECT` that is not inside an aggregate must be in
    the `GROUP BY`.
    """)
    return


@app.cell
def _(con, mo):
    df_top5 = mo.sql(
        f"""
        SELECT b.book_id,
               b.title,
               a.name            AS author,
               COUNT(*)          AS copies_sold,
               SUM(o.sale_price) AS revenue
        FROM   orders  AS o
        INNER JOIN books   AS b ON o.book_id   = b.book_id
        INNER JOIN authors AS a ON b.author_id = a.author_id
        GROUP BY b.book_id, b.title, a.name
        ORDER BY copies_sold DESC, b.book_id
        LIMIT 5;
        """,
        engine=con
    )
    return (df_top5,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Chart — Top 5 best-selling books

    Titles and authors on a chart: something A3 could not do without a join.
    """)
    return


@app.cell
def _(df_top5, plot_hbar):
    plot_hbar(df_top5, labels="title", values="copies_sold", note="author",
              title="Top 5 best-selling books (copies sold)",
              xlabel="copies sold")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J5 — Revenue per author

    > *"How many copies did each author sell, and how much money did they bring in?"*

    We get **4 rows**. But we have **6 authors**!

    Priya Sharma and Omar Haddad are missing. Their true answer is
    "0 copies, $0" — a real, useful answer — but `INNER JOIN` dropped
    them before `GROUP BY` ever saw them.

    When you need *every* author, even those with no match, you need
    an **outer join**. That is Part 4.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT a.name            AS author,
               COUNT(*)          AS copies_sold,
               SUM(o.sale_price) AS revenue
        FROM   authors AS a
        INNER JOIN books  AS b ON a.author_id = b.author_id
        INNER JOIN orders AS o ON b.book_id   = o.book_id
        GROUP BY a.author_id, a.name
        ORDER BY revenue DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # PART 4 — LEFT JOIN `A ⟕ B`

    ```sql
    SELECT ...
    FROM   A                      -- the LEFT table: keep ALL its rows
    LEFT JOIN B ON A.key = B.key; -- the RIGHT table: keep only matches
    ```

    A `LEFT JOIN` keeps **every row of the left table** (the one after
    `FROM`). When a left row has no match, the right-side columns are
    filled with `NULL`.

    > **Rule of thumb:** put the table you want to *keep complete*
    > right after `FROM`.

    ---

    ## J6 — Every author, with their books (if any)

    > *"List all authors and their books. Include authors with no books."*

    Compare with J1:

    | Query | Rows | Why |
    |-------|-----:|-----|
    | J1 `INNER JOIN` | 20 | only authors with books |
    | J6 `LEFT JOIN`  | **22** | 20 + one row each for Priya and Omar |

    Look at the last two rows: `book_id`, `title`, and `category` are
    empty — those are `NULL`s, meaning "no matching book".
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT a.author_id,
               a.name AS author,
               b.book_id,
               b.title,
               b.category
        FROM   authors AS a
        LEFT JOIN books AS b ON a.author_id = b.author_id
        ORDER BY a.author_id, b.book_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J7 — Books per author: `COUNT(*)` vs `COUNT(column)`

    > *"How many books did each author write? Show all 6 authors."*

    This is the **#1 LEFT JOIN trap**. Look at the two count columns:

    - `COUNT(*)` counts **rows**. Priya's row exists (full of NULLs),
      so she gets **1**. Wrong!
    - `COUNT(b.book_id)` counts **non-NULL values**. Priya's `book_id`
      is NULL, so she gets **0**. Correct.

    > After a `LEFT JOIN`, count a column from the **right** table —
    > never `COUNT(*)`.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT a.author_id,
               a.name           AS author,
               COUNT(*)         AS count_star_WRONG,
               COUNT(b.book_id) AS num_books
        FROM   authors AS a
        LEFT JOIN books AS b ON a.author_id = b.author_id
        GROUP BY a.author_id, a.name
        ORDER BY a.author_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J8 — Revenue per author, all 6 authors (fixes J5)

    > *"Copies sold and revenue for every author — including those with no sales."*

    Two `LEFT JOIN`s in a row: **authors ⟕ books ⟕ orders**. Every
    author survives both joins.

    `SUM` of nothing but NULLs is `NULL`, not 0. `COALESCE(x, 0)`
    means "use `x`, but if it is NULL, use 0 instead". Now Priya and
    Omar show **0 copies, $0** — which is the honest answer.

    > Once you start a chain with `LEFT JOIN`, keep using `LEFT JOIN`.
    > A later `INNER JOIN` would drop the NULL rows again.
    """)
    return


@app.cell
def _(con, mo):
    df_author_revenue = mo.sql(
        f"""
        SELECT a.name                         AS author,
               COUNT(o.order_id)              AS copies_sold,
               COALESCE(SUM(o.sale_price), 0) AS revenue
        FROM   authors AS a
        LEFT JOIN books  AS b ON a.author_id = b.author_id
        LEFT JOIN orders AS o ON b.book_id   = o.book_id
        GROUP BY a.author_id, a.name
        ORDER BY revenue DESC, author;
        """,
        engine=con
    )
    return (df_author_revenue,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Chart — Revenue per author

    All 6 authors appear. The dashed outlines are Priya and Omar —
    the rows that only a `LEFT JOIN` keeps. With J5's `INNER JOIN`,
    they would simply be missing from the chart.
    """)
    return


@app.cell
def _(df_author_revenue, plot_bar):
    plot_bar(df_author_revenue, labels="author", values="revenue",
             title="Revenue per author, 2025", ylabel="revenue",
             money=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J9 — Filter in `ON`, not in `WHERE`

    > *"For every author, how many COMPUTERS books did they write? Show all 6 authors."*

    The category filter goes **inside the `ON`**:
    `ON a.author_id = b.author_id AND b.category = 'COMPUTERS'`.
    The join only matches COMPUTERS books, but every author still
    stays. Lars, Priya, and Omar get **0**.

    **Try it:** move the filter to a `WHERE b.category = 'COMPUTERS'`
    instead. You get only **3 authors**. Why? `WHERE` runs *after* the
    join. The NULL rows have `category = NULL`, which is not
    `'COMPUTERS'`, so `WHERE` throws them away. Your `LEFT JOIN` has
    quietly turned into an `INNER JOIN`.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT a.author_id,
               a.name           AS author,
               COUNT(b.book_id) AS computers_books
        FROM   authors AS a
        LEFT JOIN books AS b
               ON  a.author_id = b.author_id
               AND b.category  = 'COMPUTERS'
        GROUP BY a.author_id, a.name
        ORDER BY a.author_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # PART 5 — RIGHT JOIN `A ⟖ B`

    ```sql
    SELECT ...
    FROM   A
    RIGHT JOIN B ON A.key = B.key; -- keep ALL rows of B
    ```

    A `RIGHT JOIN` is the mirror image of a `LEFT JOIN`: it keeps
    **every row of the right table** (the one after `RIGHT JOIN`).

    These two queries return the same rows:

    ```sql
    FROM A LEFT  JOIN B ON ...
    FROM B RIGHT JOIN A ON ...
    ```

    Most people write `LEFT JOIN` and just swap the table order. But
    you will see `RIGHT JOIN` in other people's code, so you must be
    able to read it.

    ---

    ## J10 — J6 again, written as a RIGHT JOIN

    > *"List all authors and their books. Include authors with no books."*

    Now `books` comes first and `authors` comes after `RIGHT JOIN`.
    `authors` is the table we keep complete. Same **22 rows** as J6.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT a.author_id,
               a.name AS author,
               b.book_id,
               b.title,
               b.category
        FROM   books AS b
        RIGHT JOIN authors AS a ON b.author_id = a.author_id
        ORDER BY a.author_id, b.book_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J11 — Every book with its orders (if any)

    > *"Show every book with each of its orders. Include books nobody bought."*

    `orders RIGHT JOIN books` keeps all 20 books.

    | Query | Rows | Why |
    |-------|-----:|-----|
    | J2 `INNER JOIN` | 80 | only books that were ordered |
    | J11 `RIGHT JOIN` | **84** | 80 + one row each for the 4 unsold books |

    The 4 unsold books show `NULL` in `order_id`, `sale_price`, and
    `order_date`. Scroll to find them, or wait for M2.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT b.book_id,
               b.title,
               o.order_id,
               o.sale_price,
               o.order_date
        FROM   orders AS o
        RIGHT JOIN books AS b ON o.book_id = b.book_id
        ORDER BY b.book_id, o.order_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## J12 — Sold vs. unsold books per category

    > *"In each category, how many books do we have, and how many sold at least once?"*

    `COUNT(DISTINCT ...)` counts **different** values, and skips NULLs:

    - `COUNT(DISTINCT b.book_id)` — every book in the category.
    - `COUNT(DISTINCT o.book_id)` — only books that have an order.
      Unsold books have `o.book_id = NULL`, so they are not counted.

    The difference is the number of unsold books. Every category has
    at least one.
    """)
    return


@app.cell
def _(con, mo):
    df_category_sales = mo.sql(
        f"""
        SELECT b.category,
               COUNT(DISTINCT b.book_id) AS num_books,
               COUNT(DISTINCT o.book_id) AS books_sold,
               COUNT(DISTINCT b.book_id)
                 - COUNT(DISTINCT o.book_id) AS books_unsold,
               COUNT(o.order_id)         AS copies_sold,
               COALESCE(SUM(o.sale_price), 0) AS revenue
        FROM   orders AS o
        RIGHT JOIN books AS b ON o.book_id = b.book_id
        GROUP BY b.category
        ORDER BY b.category;
        """,
        engine=con
    )
    return (df_category_sales,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Chart — Sold vs. unsold books per category

    Green = sold at least once. Red = never sold. The red parts
    exist only because the `RIGHT JOIN` kept the unsold books.
    """)
    return


@app.cell
def _(df_category_sales, plot_stacked_bar):
    plot_stacked_bar(df_category_sales, labels="category",
                     parts=["books_sold", "books_unsold"],
                     part_names=["sold", "never sold"],
                     title="Books per category: sold vs. never sold",
                     ylabel="number of books")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # PART 6 — FINDING WHAT IS MISSING

    Some of the most useful business questions are about what is
    **not** there: customers who never ordered, products that never
    sold, employees with no manager.

    The pattern is always the same:

    ```sql
    SELECT ...
    FROM   keep_table AS k
    LEFT JOIN other_table AS x ON k.key = x.key
    WHERE  x.key IS NULL;   -- no match was found
    ```

    The `LEFT JOIN` creates a NULL row for every unmatched row.
    `WHERE ... IS NULL` keeps **only** those. (This is called an
    **anti-join**.)

    > Use `IS NULL`, never `= NULL`. `NULL = NULL` is not true — it is
    > unknown — so `= NULL` matches nothing.

    ---

    ## M1 — Authors with no books

    > *"Which authors have not published any book?"*

    Answer: **Priya Sharma** and **Omar Haddad**.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT a.author_id,
               a.name,
               a.email,
               a.country
        FROM   authors AS a
        LEFT JOIN books AS b ON a.author_id = b.author_id
        WHERE  b.book_id IS NULL
        ORDER BY a.author_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## M2 — Books that no one has purchased

    > *"Which books have never been ordered?"*

    Same pattern, one step down the chain: keep all `books`, look for
    the ones with no matching `orders` row.

    Answer: **B06, B12, B17, B20**.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT b.book_id,
               b.title,
               b.category,
               b.publication_year
        FROM   books AS b
        LEFT JOIN orders AS o ON b.book_id = o.book_id
        WHERE  o.order_id IS NULL
        ORDER BY b.book_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## M3 — Same question, with a RIGHT JOIN

    > *"Which books have never been ordered?" — written as a RIGHT JOIN.*

    `orders RIGHT JOIN books` keeps all books, exactly like M2.
    Same 4 books. Use whichever form you find easier to read — but
    make sure the table you keep complete is the one with the
    **missing** things in it (here: `books`).
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT b.book_id,
               b.title,
               b.category,
               b.publication_year
        FROM   orders AS o
        RIGHT JOIN books AS b ON o.book_id = b.book_id
        WHERE  o.order_id IS NULL
        ORDER BY b.book_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## M4 — Unsold books, with the author's name

    > *"Which books never sold, and who wrote them?"*

    Mix both join types in one query:

    - `INNER JOIN authors` — every book has an author, so nothing is lost.
    - `LEFT JOIN orders` + `IS NULL` — keep only books with no order.

    Something interesting appears: **each of the 4 published authors
    has exactly one unsold book.**
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT b.book_id,
               b.title,
               b.category,
               a.name AS author
        FROM   books AS b
        INNER JOIN authors AS a ON b.author_id = a.author_id
        LEFT  JOIN orders  AS o ON b.book_id   = o.book_id
        WHERE  o.order_id IS NULL
        ORDER BY b.book_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # SUMMARY — Same Tables, Different Joins, Different Row Counts

    The query below runs every join type on the same pairs of
    tables and counts the rows. This one table is the whole lesson.
    """)
    return


@app.cell
def _(con, mo):
    df_join_counts = mo.sql(
        f"""
        SELECT 'authors INNER JOIN books' AS join_query, 'INNER' AS join_type, COUNT(*) AS num_rows
        FROM   authors AS a INNER JOIN books AS b ON a.author_id = b.author_id
        UNION ALL
        SELECT 'authors LEFT JOIN books', 'LEFT', COUNT(*)
        FROM   authors AS a LEFT JOIN books AS b ON a.author_id = b.author_id
        UNION ALL
        SELECT 'books RIGHT JOIN authors', 'RIGHT', COUNT(*)
        FROM   books AS b RIGHT JOIN authors AS a ON b.author_id = a.author_id
        UNION ALL
        SELECT 'books INNER JOIN orders', 'INNER', COUNT(*)
        FROM   books AS b INNER JOIN orders AS o ON b.book_id = o.book_id
        UNION ALL
        SELECT 'books LEFT JOIN orders', 'LEFT', COUNT(*)
        FROM   books AS b LEFT JOIN orders AS o ON b.book_id = o.book_id
        UNION ALL
        SELECT 'orders RIGHT JOIN books', 'RIGHT', COUNT(*)
        FROM   orders AS o RIGHT JOIN books AS b ON o.book_id = b.book_id;
        """,
        engine=con
    )
    return (df_join_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Chart — Row counts by join type

    Same tables, different joins. The outer joins (green, orange)
    are longer by exactly the number of unmatched rows: 2 authors
    with no books, 4 books with no orders.
    """)
    return


@app.cell
def _(df_join_counts, plot_join_counts):
    plot_join_counts(df_join_counts, labels="join_query", values="num_rows",
                     kinds="join_type", title="Rows returned by each join")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Cheat Sheet

    | Join | Symbol | Keeps | Unmatched rows become |
    |------|:------:|-------|-----------------------|
    | `INNER JOIN` | ⋈ | only rows that match on both sides | dropped |
    | `LEFT JOIN`  | ⟕ | every row of the **left** table (after `FROM`) | NULLs on the right side |
    | `RIGHT JOIN` | ⟖ | every row of the **right** table (after `RIGHT JOIN`) | NULLs on the left side |

    **Five things to remember**

    1. `INNER JOIN` drops unmatched rows **silently**. Always check
       the row count.
    2. After a `LEFT JOIN`, use `COUNT(right_table.column)`, not `COUNT(*)`.
    3. Wrap `SUM` in `COALESCE(..., 0)` when a group might have no rows.
    4. To filter the right table and still keep every left row, put
       the filter in `ON`, not `WHERE`.
    5. "Find what is missing" = `LEFT JOIN` + `WHERE right.key IS NULL`.

    ---

    ### Try It Yourself

    Add a new cell (click **+** below) and write these on your own:

    1. List every author with the **number of different categories**
       they wrote in. Show all 6 authors.
    2. Find the total revenue per **category** with an `INNER JOIN`.
       Why does the answer not change if you use a `LEFT JOIN`?
    3. Find authors who wrote at least one book **but** have one or
       more unsold books. (Hint: start from M4.)
    4. Show every book with its **first order date** (`MIN`).
       Unsold books should still appear, with an empty date.
    5. Which country's authors earned the most revenue?

    ---

    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
