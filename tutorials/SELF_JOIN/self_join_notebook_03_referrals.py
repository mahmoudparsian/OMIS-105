import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb

    # One tiny table, built in memory. Re-running is safe
    # because of CREATE OR REPLACE.
    con = duckdb.connect(database=":memory:")

    con.execute("""
        CREATE OR REPLACE TABLE customers (
            cust_id     INTEGER PRIMARY KEY,
            name        VARCHAR,
            city        VARCHAR,
            join_date   DATE,
            total_spent INTEGER,
            referred_by INTEGER
        )
    """)
    con.execute("""
        INSERT INTO customers VALUES
            (1, 'Maria', 'San Jose',    DATE '2024-01-15', 1200, NULL),
            (2, 'Kevin', 'Santa Clara', DATE '2024-02-03',  450, 1),
            (3, 'Priya', 'San Jose',    DATE '2024-02-20', 1800, 1),
            (4, 'Tom',   'Oakland',     DATE '2024-03-11',  300, 2),
            (5, 'Lina',  'Santa Clara', DATE '2024-03-29',  950, 2),
            (6, 'Omar',  'San Jose',    DATE '2024-04-05',  700, 3),
            (7, 'Sofia', 'Oakland',     DATE '2024-05-17',  150, NULL),
            (8, 'Ben',   'Santa Clara', DATE '2024-06-02',  600, 5)
    """)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 🤝 Self Join — Customer Referrals

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### The Story: Bronco Outfitters 🛍️

    **Bronco Outfitters** is a small online store. It gives a reward
    when a customer invites a friend.

    All 8 customers live in **one table**, `customers`. The
    `referred_by` column holds the `cust_id` of the customer who
    invited them. So the person who invited you is **also a row in
    the same table**. If someone found the store on their own, their
    `referred_by` is `NULL`.

    The marketing manager asks:

    > **"Which customers bring in the most friends — and are those
    > friends good customers?"**

    To answer, we put two rows of the same table side by side.
    That is a **self join**.

    This notebook is the referral example from Section 6 of
    [`self_joins_guide.md`](self_joins_guide.md), as live queries.
    It works best after notebook 01 or 02.

    ### The Plan

    | Part | Queries | What happens |
    |------|---------|--------------|
    | 1. Meet the data | Q1–Q2 | The table and its referral tree. |
    | 2. Two roles | — | `c` = the customer, `r` = the referrer. |
    | 3. Who invited whom? | Q3–Q4 | `INNER JOIN`, then `LEFT JOIN` + `COALESCE`. |
    | 4. Count the referrals | Q5 | `GROUP BY`, and the `COUNT(*)` trap. |
    | 5. Compare a row to its partner | Q6 | Friends who spent more than the person who invited them. |
    | 6. Pairs from one table | Q7–Q8 | Customers in the same city, and the `<` trick. |
    | 7. Two steps up | Q9 | The referral chain: three copies of one table. |
    | 8. Explore | — | Pick a customer, see the friends they invited. |
    | 9. Practice | — | 4 exercises with solutions. |

    The table is tiny on purpose: you can check every answer by eye.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 1 — Meet the Data

    ### Q1. The `customers` table

    Look at the `referred_by` column. Kevin's `referred_by` is `1`.
    Who has `cust_id = 1`? Maria. So **Maria invited Kevin**.

    Maria and Sofia found the store on their own, so their
    `referred_by` is `NULL`.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT cust_id,
               name,
               city,
               join_date,
               total_spent,
               referred_by
        FROM customers
        ORDER BY cust_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. The same data as a referral tree

    Each arrow goes from a customer to a friend they invited.
    Maria and Sofia start their own trees, because nobody invited them.

    **Fun fact:** the arrows are drawn from the result of a self
    join — the query you will write in Q3.
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _nodes = con.execute("""
        SELECT cust_id, name, city, total_spent
        FROM customers
        ORDER BY cust_id
    """).fetchall()
    _edges = con.execute("""
        SELECT r.cust_id, c.cust_id
        FROM customers AS c
        INNER JOIN customers AS r
            ON c.referred_by = r.cust_id
        ORDER BY r.cust_id, c.cust_id
    """).fetchall()

    _ids = {_name: _id for _id, _name, _city, _spent in _nodes}

    def referral_tree(customers=(), referrers=(), color="#BBF7D0", border="#15803D"):
        # Fill each customer's box, outline each referrer's box (dashed),
        # and thicken the arrow between each pair.
        customers, referrers = list(customers), list(referrers)
        _pairs = {(_ids[r], _ids[c]) for c, r in zip(customers, referrers)}
        _lines = ["graph TD"]
        for _id, _name, _city, _spent in _nodes:
            _lines.append(f'    C{_id}["<b>{_name}</b><br/>{_city}<br/>spent {_spent:,}"]')
        for _i, (_r, _c) in enumerate(_edges):
            _lines.append(f"    C{_r} --> C{_c}")
            if (_r, _c) in _pairs:
                _lines.append(f"    linkStyle {_i} stroke:{border},stroke-width:4px")
        _lines.append(f"    classDef cust fill:{color},stroke:{border},stroke-width:3px,color:#111")
        _lines.append(f"    classDef ref fill:#FFFFFF,stroke:{border},stroke-width:3px,stroke-dasharray:6 4,color:#111")
        if customers:
            _lines.append("    class " + ",".join(f"C{_ids[c]}" for c in customers) + " cust")
        _ref_only = [r for r in dict.fromkeys(referrers) if r not in customers]
        if _ref_only:
            _lines.append("    class " + ",".join(f"C{_ids[r]}" for r in _ref_only) + " ref")
        return mo.mermaid("\n".join(_lines))

    referral_tree()
    return (referral_tree,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 2 — Two Roles

    We use the **same table twice** and give each copy an alias.
    Each alias plays a **role**:

    | Alias | Role | Read it as |
    |-------|------|------------|
    | `c` | the **customer** | "the person we are talking about" |
    | `r` | the **referrer** | "the person who invited `c`" |

    The `ON` rule connects the two roles:

    ```sql
    ON c.referred_by = r.cust_id
    ```

    Read it out loud: *"the customer's `referred_by` must equal the
    referrer's `cust_id`."*

    ```
       c  (customer copy)                      r  (referrer copy)
    ┌────┬───────┬─────────────┐          ┌────┬───────┐
    │ id │ name  │ referred_by │          │ id │ name  │
    ├────┼───────┼─────────────┤          ├────┼───────┤
    │  2 │ Kevin │       1 ────┼────────▶ │  1 │ Maria │
    │  8 │ Ben   │       5 ────┼────────▶ │  5 │ Lina  │
    │  7 │ Sofia │    NULL     │   ✗      │    │       │
    └────┴───────┴─────────────┘          └────┴───────┘
    ```

    **Always put the alias in front of every column** (`c.name`,
    `r.name`). Every column exists in both copies, so a bare `name`
    is ambiguous, and DuckDB stops with an error.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 3 — Who Invited Whom?

    ### Q3. Each customer next to the person who invited them

    `c` gives us the customer's name. `r` gives us the referrer's name.

    **Predict first:** there are 8 customers. How many rows will
    `INNER JOIN` return?

    **Expected: 6 rows.** Maria and Sofia are missing — their
    `referred_by` is `NULL`, and `NULL` never matches anything.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT c.name AS customer,
               r.name AS referred_by
        FROM customers AS c
        INNER JOIN customers AS r
            ON c.referred_by = r.cust_id
        ORDER BY c.cust_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. Every customer, with a friendly label

    `LEFT JOIN` keeps **every row of the left copy** (`c`), even when
    nobody invited them. `COALESCE(a, b)` returns `b` when `a` is
    `NULL`, so we can print a label instead of `NULL`.

    **Expected: 8 rows.** Maria and Sofia say *"Signed up on their own"*.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT c.name AS customer,
               c.join_date,
               COALESCE(r.name, 'Signed up on their own') AS referred_by
        FROM customers AS c
        LEFT JOIN customers AS r
            ON c.referred_by = r.cust_id
        ORDER BY c.cust_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 4 — Count the Referrals

    ### Q5. Who invited the most friends?

    Now the referrer `r` goes on the **left**: we start from every
    customer and look for the friends they invited (`c`).
    `LEFT JOIN` keeps customers who invited nobody.

    Two counts, side by side:

    * `COUNT(c.cust_id)` counts only **real** friends. ✅
    * `COUNT(*)` counts **rows** — and a customer who invited nobody
      still has one row (full of `NULL`s), so it says **1**. ❌

    **Expected: 8 rows.** Maria and Kevin invited 2 friends each;
    Priya and Lina invited 1; Tom, Omar, Sofia, and Ben invited 0.
    Maria's friends spent 450 + 1,800 = 2,250. Look at the
    `wrong_count` column: Tom shows 1, but he invited nobody.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT r.name AS customer,
               COUNT(c.cust_id)                AS referrals,
               COUNT(*)                        AS wrong_count,
               COALESCE(SUM(c.total_spent), 0) AS spent_by_referrals,
               STRING_AGG(c.name, ', ' ORDER BY c.name) AS friends
        FROM customers AS r
        LEFT JOIN customers AS c
            ON c.referred_by = r.cust_id
        GROUP BY r.cust_id, r.name
        ORDER BY referrals DESC, r.cust_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 5 — Compare a Row to Its Partner

    After the join, each result row holds **two people**: `c` and `r`.
    Now you can compare their columns.

    > `ON` decides **which rows belong together**.
    > `WHERE` decides **which of those pairs to keep**.

    ### Q6. Friends who spent more than the person who invited them

    These are the store's "best" invitations.

    **Expected: 2 rows.** Priya spent 1,800 (Maria: 1,200).
    Lina spent 950 (Kevin: 450).
    """)
    return


@app.cell
def _(con, mo):
    q6_df = mo.sql(
        f"""
        SELECT c.name        AS customer,
               c.total_spent AS customer_spent,
               r.name        AS referred_by,
               r.total_spent AS referrer_spent,
               c.total_spent - r.total_spent AS difference
        FROM customers AS c
        INNER JOIN customers AS r
            ON c.referred_by = r.cust_id
        WHERE c.total_spent > r.total_spent
        ORDER BY difference DESC;
        """,
        engine=con
    )
    return (q6_df,)


@app.cell(hide_code=True)
def _(mo, q6_df, referral_tree):
    mo.vstack([
        mo.md("""
    **Q6 on the referral tree.** 🟩 A **green** box spent more than
    the person who invited them. The **dashed** box is that referrer,
    and the **thick arrow** is the self-join match between them.
        """),
        referral_tree(q6_df["customer"], q6_df["referred_by"]),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 6 — Pairs From One Table

    A self join can match rows on **any** column they share — not
    only `referred_by`. Here we pair up customers who live in the
    same city.

    Both aliases play the **same role**, so we call them `a` and `b`
    (not `c` and `r`).

    ### Q7. Which customers live in the same city?

    ```sql
    ON a.city = b.city              -- same city
    AND a.cust_id < b.cust_id       -- the "<" trick
    ```

    **Expected: 7 pairs.** San Jose and Santa Clara have 3 customers
    each, so 3 pairs each. Oakland has 2 customers, so 1 pair.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT a.name AS customer_1,
               b.name AS customer_2,
               a.city
        FROM customers AS a
        INNER JOIN customers AS b
            ON a.city = b.city
           AND a.cust_id < b.cust_id
        ORDER BY a.city, a.cust_id, b.cust_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. Why the `<` trick? Count the pairs three ways

    | Extra condition | What goes wrong |
    |-----------------|-----------------|
    | *(none)* | Every customer is paired **with themselves** (Tom–Tom). |
    | `a.cust_id <> b.cust_id` | No self-pairs, but every pair appears **twice** (Tom–Sofia **and** Sofia–Tom). |
    | `a.cust_id < b.cust_id` | Each pair appears **once**. ✅ |

    **Expected:** 22, then 14, then 7.
    (22 = 14 two-way pairs + 8 self-pairs. 14 ÷ 2 = 7.)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            (SELECT COUNT(*)
             FROM customers AS a
             INNER JOIN customers AS b
                 ON a.city = b.city) AS no_extra_rule,
            (SELECT COUNT(*)
             FROM customers AS a
             INNER JOIN customers AS b
                 ON a.city = b.city
                AND a.cust_id <> b.cust_id) AS with_not_equal,
            (SELECT COUNT(*)
             FROM customers AS a
             INNER JOIN customers AS b
                 ON a.city = b.city
                AND a.cust_id < b.cust_id) AS with_less_than;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 7 — Two Steps Up the Chain 🪜

    ### Q9. Who invited the person who invited you?

    Use the same table **three times**. Each copy gets its own alias
    and its own role:

    | Alias | Role |
    |-------|------|
    | `c` | the customer |
    | `r` | the person who invited them |
    | `rr` | the person who invited `r` |

    Each `JOIN` climbs **one step** up the referral tree.

    **Expected: 4 rows** — Tom, Lina, Omar, and Ben. Kevin and Priya
    are missing: Maria invited them, and nobody invited Maria.
    Maria and Sofia are missing too: nobody invited them.

    **Try it:** change both `INNER JOIN`s to `LEFT JOIN`. You should
    get all 8 customers, with `NULL` where a step is missing.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT c.name  AS customer,
               r.name  AS referred_by,
               rr.name AS referrers_referrer
        FROM customers AS c
        INNER JOIN customers AS r
            ON c.referred_by = r.cust_id
        INNER JOIN customers AS rr
            ON r.referred_by = rr.cust_id
        ORDER BY c.cust_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 8 — Explore: Pick a Customer 🎛️

    Choose a customer. The query below re-runs by itself and shows
    the friends they invited. This is the same self join as Q3 —
    only the `WHERE` filter changes.
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _referrers = [r[0] for r in con.execute("""
        SELECT DISTINCT r.name, r.cust_id
        FROM customers AS c
        INNER JOIN customers AS r
            ON c.referred_by = r.cust_id
        ORDER BY r.cust_id
    """).fetchall()]
    referrer_picker = mo.ui.dropdown(
        options=_referrers, value="Kevin", label="Referrer (`r`):"
    )
    referrer_picker
    return (referrer_picker,)


@app.cell
def _(con, mo, referrer_picker):
    _df = mo.sql(
        f"""
        SELECT r.name AS referrer,
               c.name AS friend,
               c.city,
               c.join_date,
               c.total_spent
        FROM customers AS c
        INNER JOIN customers AS r
            ON c.referred_by = r.cust_id
        WHERE r.name = '{referrer_picker.value}'
        ORDER BY c.total_spent DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 9 — Try It Yourself ✍️

    Write each query in a new cell, then open the solution to check.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Exercise 1 — Who lives in a different city than the person who invited them?": mo.md("""
    ```sql
    SELECT c.name, c.city, r.name AS referred_by, r.city AS referrer_city
    FROM customers AS c
    INNER JOIN customers AS r
        ON c.referred_by = r.cust_id
    WHERE c.city <> r.city
    ORDER BY c.cust_id;
    ```
    2 rows: Kevin (Santa Clara; Maria lives in San Jose) and Tom
    (Oakland; Kevin lives in Santa Clara).
        """),
        "Exercise 2 — Who invited nobody? (Hint: LEFT JOIN + IS NULL)": mo.md("""
    ```sql
    SELECT r.name
    FROM customers AS r
    LEFT JOIN customers AS c
        ON c.referred_by = r.cust_id
    WHERE c.cust_id IS NULL
    ORDER BY r.cust_id;
    ```
    4 rows: Tom, Omar, Sofia, Ben.
        """),
        "Exercise 3 — How many days after their referrer did each friend join?": mo.md("""
    ```sql
    SELECT c.name,
           r.name AS referred_by,
           DATE_DIFF('day', r.join_date, c.join_date) AS days_later
    FROM customers AS c
    INNER JOIN customers AS r
        ON c.referred_by = r.cust_id
    ORDER BY days_later;
    ```
    6 rows. Kevin joined fastest (19 days after Maria). Ben was the
    slowest (65 days after Lina).
        """),
        "Exercise 4 — Who spent more than the person two steps up their chain?": mo.md("""
    ```sql
    SELECT c.name, c.total_spent,
           rr.name AS referrers_referrer, rr.total_spent AS rr_spent
    FROM customers AS c
    INNER JOIN customers AS r
        ON c.referred_by = r.cust_id
    INNER JOIN customers AS rr
        ON r.referred_by = rr.cust_id
    WHERE c.total_spent > rr.total_spent;
    ```
    1 row: Ben spent 600. Lina invited him, and Kevin invited Lina.
    Kevin spent only 450.
        """),
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ### Same Patterns, New Table

    | Pattern | Employees (notebooks 01–02) | Customers (this notebook) |
    |---------|-----------------------------|---------------------------|
    | Row → its parent | `e.manager_id = m.emp_id` | `c.referred_by = r.cust_id` |
    | Keep rows with no parent | `LEFT JOIN` + `COALESCE` | `LEFT JOIN` + `COALESCE` |
    | Count the children | `COUNT(e.emp_id)` | `COUNT(c.cust_id)` |
    | Compare a row to its parent | `e.salary > m.salary` | `c.total_spent > r.total_spent` |
    | Pairs of peers | same `manager_id` + `<` | same `city` + `<` |
    | Two steps up | `e → m → g` | `c → r → rr` |

    ### Key Takeaway

    > Any table where one row **points to another row** of the same
    > table is ready for a self join. Give each copy an alias that
    > names its **role**, write the `ON` rule that connects the roles,
    > and everything you know about joins works exactly as before.

    **Further reading:**
    [DuckDB joins](https://duckdb.org/docs/lts/sql/query_syntax/from) ·
    [Marimo SQL cells](https://docs.marimo.io/guides/working_with_data/sql/)

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
