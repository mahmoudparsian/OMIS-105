import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ⚡ Indexes & Query Performance
    ### A Hands-On Tutorial with DuckDB — Week 7

    ---

    ## What You Will Learn

    | Topic | Description |
    |---|---|
    | **What an index is** | A lookup structure the database keeps *beside* your table |
    | **`CREATE INDEX`** | How to build one, and on which column |
    | **Measuring honestly** | Timing a query properly instead of guessing |
    | **`EXPLAIN`** | Reading the plan the database chose |
    | **Why the gain is small here** | DuckDB is *columnar* — and that changes everything |
    | **What actually makes it fast** | Column pruning and zone maps beat indexes in DuckDB |
    | **When an index does pay** | Selective lookups, and enforcing `PRIMARY KEY` |

    ---

    ## The idea, in one picture

    An index is the same thing as the index at the back of a textbook.

    ```
    WITHOUT an index                    WITH an index
    ─────────────────                   ──────────────
    Want "transactions"?                Want "transactions"?
    Open page 1.                        Flip to the back.
    Not there. Page 2.                  "transactions ....... 412"
    Not there. Page 3.                  Go straight to page 412.
    ... 400 more pages ...
                                        A few lookups.
    Read the whole book.
    ```

    The database calls the slow version a **sequential scan** and the fast version
    an **index scan**.

    ---

    ## An honest warning before we start

    Your instructor's teaching notes say students often *expect a dramatic speed
    difference and do not see one*. That is not a mistake in your code — and this
    notebook will show you exactly why it happens.

    **We are going to measure real numbers, and some of them will be
    disappointing.** That disappointment is the lesson.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 0 · Setup
    """)
    return


@app.cell
def _():
    import os
    import sys

    import duckdb
    import pandas as pd

    sys.path.insert(0, os.path.dirname(os.path.abspath("__file__")))
    from perf_plot_util import (
        display_table,
        plot_index_comparison,
        plot_projection_cost,
        plot_speedup,
        time_query,
    )

    # In-memory database — fresh every run, so this notebook is fully idempotent.
    con = duckdb.connect(database=":memory:")
    print("✅  DuckDB connected  |  version:", duckdb.__version__)
    return (
        con,
        display_table,
        pd,
        plot_index_comparison,
        plot_projection_cost,
        plot_speedup,
        time_query,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1 · Build a small table — the way the lab does

    We start where the Week 7 lab starts: a small `sales` table. `range(1000)`
    generates the rows for us, so nothing has to be typed by hand.

    The `price` column is deliberately spread out so that any single price matches
    only a handful of rows. A filter that matches *most* of the table can never
    benefit from an index — the database would have to read everything anyway.
    """)
    return


@app.cell
def _(con, display_table):
    _sql = """
        CREATE OR REPLACE TABLE sales AS
        SELECT
            i                          AS sale_id,
            (i * 7919) % 100000        AS price,
            'product_' || ((i * 31) % 500) AS product,
            (i % 12) + 1               AS month
        FROM range(1000) t(i);
    """
    print("SQL:\n", _sql)
    con.execute(_sql)

    _df = con.execute("SELECT * FROM sales ORDER BY sale_id LIMIT 5;").df()
    display_table(_df, "First 5 rows of sales (1,000 rows total)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2 · Time the query *without* an index

    The lab asks us to "query without index", then "query again" after creating
    one. To compare them we need a number, not a feeling.

    `time_query()` in `perf_plot_util.py` runs the query 25 times and reports the
    **median**. Two details matter:

    - The **first** run is thrown away. It includes parsing and planning the query,
      which happens once and would exaggerate the "before" number.
    - The **median** is used, not the average. One unlucky run — the operating
      system pausing us, another program waking up — would drag an average around
      and invent a difference that is not real.

    Measuring badly is the most common way to "prove" something false about
    performance.
    """)
    return


@app.cell
def _(con, time_query):
    _query = "SELECT * FROM sales WHERE price = 79190;"
    print("SQL:\n", _query)

    _small_before = time_query(con, _query)
    print(f"1,000 rows, no index : {_small_before:.4f} ms")
    print("\nHow many rows come back?")
    print(con.execute("SELECT COUNT(*) AS matches FROM sales WHERE price = 79190").df()
          .to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3 · Create the index and measure again

    ```sql
    CREATE INDEX idx_price ON sales(price);
    ```

    DuckDB builds an **ART index** (an adaptive radix tree) on the `price` column.
    It is a separate structure that maps each price to the rows holding it.
    """)
    return


@app.cell
def _(con, time_query):
    _query = "SELECT * FROM sales WHERE price = 79190;"

    _before = time_query(con, _query)
    con.execute("CREATE INDEX idx_price ON sales(price);")
    _after = time_query(con, _query)

    print(f"1,000 rows, no index   : {_before:.4f} ms")
    print(f"1,000 rows, with index : {_after:.4f} ms")
    print(f"Speedup                : {_before / _after:.2f}x")
    print("\n👉 On 1,000 rows there is essentially nothing to gain.")
    print("   Scanning 1,000 rows is already almost free.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **This is the moment the teaching notes warn about.** The index made no
    meaningful difference, and a student could reasonably conclude that indexes do
    not work.

    The real explanation is simpler: **1,000 rows is too small for the question to
    matter.** Reading all thousand takes microseconds. You cannot save time that
    was never being spent.

    So let us make the table big enough for the question to be fair.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 · Scale it up — 10 thousand to 2 million rows

    We now rebuild the same table at four sizes and repeat the identical
    experiment: time the query, create the index, time it again.

    This takes a few seconds to run. Nothing about the query changes — only the
    number of rows underneath it.
    """)
    return


@app.cell
def _(con, display_table, pd, time_query):
    _query = "SELECT * FROM sales_scaled WHERE price = 79190;"
    _results = []

    for _n in (10_000, 100_000, 500_000, 2_000_000):
        con.execute(f"""
            CREATE OR REPLACE TABLE sales_scaled AS
            SELECT i                              AS sale_id,
                   (i * 7919) % 100000            AS price,
                   'product_' || ((i * 31) % 500) AS product,
                   (i % 12) + 1                   AS month
            FROM range({_n}) t(i);
        """)
        _no_index = time_query(con, _query)
        con.execute("CREATE INDEX idx_scaled_price ON sales_scaled(price);")
        _with_index = time_query(con, _query)
        _results.append((_n, _no_index, _with_index))

    timing_rows = _results
    _df = pd.DataFrame(
        [(f"{n:,}", round(b, 4), round(a, 4), round(b / a, 2)) for n, b, a in _results],
        columns=["rows", "no_index_ms", "with_index_ms", "speedup"],
    )
    display_table(_df, "Point-lookup timing as the table grows")
    return (timing_rows,)


@app.cell
def _(plot_index_comparison, timing_rows):
    plot_index_comparison(timing_rows)
    return


@app.cell
def _(plot_speedup, timing_rows):
    plot_speedup(timing_rows)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 · So why is the speedup still so modest?

    Two million rows, a perfectly selective filter, an index built exactly on the
    filtered column — and the query is only around **1.5 to 2 times** faster. In a
    traditional database like PostgreSQL or MySQL this same experiment can show a
    *hundred-fold* difference.

    The reason is that **DuckDB is a columnar database**, and it is extremely good
    at the thing an index is supposed to rescue you from.

    ### Reason 1 — it only reads the column you asked about

    ```
    ROW STORE (PostgreSQL, MySQL)      COLUMN STORE (DuckDB)
    ─────────────────────────────      ─────────────────────
    row 1: [id|price|product|month]    id:      [1][2][3][4]...
    row 2: [id|price|product|month]    price:   [7919][15838]...   ← reads only this
    row 3: [id|price|product|month]    product: [p_31][p_62]...
                                       month:   [2][3][4]...
    To check price it must walk
    over id, product and month too.    To check price it reads price. Nothing else.
    ```

    ### Reason 2 — zone maps skip most of the data already

    DuckDB stores rows in groups and remembers the **minimum and maximum** value in
    each group. Searching for `price = 79190`, it checks each group's min/max and
    skips any group that cannot possibly contain it — without reading a single
    value inside. That is most of the benefit an index would have given you, and
    you get it for free with no `CREATE INDEX` at all.

    ### Reason 3 — the scan itself is vectorised

    DuckDB compares values in batches of ~2,048 at a time using your CPU's parallel
    instructions, across multiple cores. A "full scan" here is nothing like reading
    rows one at a time.

    > **The honest summary:** in DuckDB, a sequential scan is already so fast that
    > an index has much less to save. Indexes are not useless — but they are not the
    > main performance lever, and reaching for one first is usually the wrong move.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6 · Reading the plan with `EXPLAIN`

    `EXPLAIN` shows the strategy the database chose *without running the query*.
    It is how you check what is actually happening instead of guessing.

    Look for the node type — `SEQ_SCAN` means it decided to scan.
    """)
    return


@app.cell
def _(con):
    _sql = "EXPLAIN SELECT * FROM sales_scaled WHERE price = 79190;"
    print("SQL:\n", _sql)
    print(con.execute(_sql).fetchall()[0][1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice two things in that plan:

    1. **`Filters: price=79190` appears inside the scan node.** The filter was
       *pushed down* into the scan rather than applied afterwards, so rows are
       discarded as early as possible.
    2. **It still says `SEQ_SCAN`,** even though our index exists. DuckDB uses an
       index scan only when it estimates the result is a very small fraction of the
       table, and it often decides its own scan is the better bet. The optimiser is
       allowed to ignore your index — and here it usually should.

    `EXPLAIN ANALYZE` goes further: it *runs* the query and reports real timings
    per operator.
    """)
    return


@app.cell
def _(con):
    _sql = "EXPLAIN ANALYZE SELECT COUNT(*) FROM sales_scaled WHERE price = 79190;"
    print("SQL:\n", _sql)
    _plan = con.execute(_sql).fetchall()[0][1]
    print("\n".join(_plan.splitlines()[:14]))
    print("...")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7 · What *does* make a big difference here

    If indexes are not the main lever in a columnar database, what is? Two things,
    and you already have both.

    ### Stop asking for columns you do not need

    `SELECT *` forces DuckDB to read and assemble every column. Naming only the
    columns you actually want lets it skip the rest entirely — this is called
    **projection pushdown**, and on a wide table it is worth more than any index.
    """)
    return


@app.cell
def _(con, display_table, pd, time_query):
    con.execute("""
        CREATE OR REPLACE TABLE wide_sales AS
        SELECT i                                            AS sale_id,
               (i % 1000)                                   AS price,
               i * 1.5                                      AS amount,
               'customer note padding text number ' || i    AS note1,
               'shipping address padding text '     || i    AS note2,
               'internal comment padding text '     || i    AS note3
        FROM range(1000000) t(i);
    """)

    _q_all = "SELECT * FROM wide_sales WHERE price = 7;"
    _q_two = "SELECT sale_id, amount FROM wide_sales WHERE price = 7;"

    _t_all = time_query(con, _q_all, reps=8)
    _t_two = time_query(con, _q_two, reps=8)

    projection_labels = ["SELECT *\n(6 columns)", "SELECT sale_id, amount\n(2 columns)"]
    projection_times = [_t_all, _t_two]

    _df = pd.DataFrame({
        "query": ["SELECT *", "SELECT sale_id, amount"],
        "ms": [round(_t_all, 3), round(_t_two, 3)],
    })
    display_table(_df, "Same rows, same filter — only the column list changed")
    print(f"Naming your columns was {_t_all / _t_two:.1f}x faster here.")
    return projection_labels, projection_times


@app.cell
def _(plot_projection_cost, projection_labels, projection_times):
    plot_projection_cost(projection_labels, projection_times)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filter on something the zone maps can use

    A filter on a column whose values are **stored in order** lets DuckDB skip
    whole blocks using min/max. Our `sale_id` is generated in order, so filtering
    on it is dramatically cheaper than filtering on a scattered column — with no
    index involved at all.
    """)
    return


@app.cell
def _(con, display_table, pd, time_query):
    _q_scattered = "SELECT COUNT(*) FROM wide_sales WHERE price = 7;"
    _q_ordered = "SELECT COUNT(*) FROM wide_sales WHERE sale_id < 1000;"

    _t_scattered = time_query(con, _q_scattered, reps=15)
    _t_ordered = time_query(con, _q_ordered, reps=15)

    _df = pd.DataFrame({
        "filter": ["price = 7  (scattered values)", "sale_id < 1000  (ordered values)"],
        "ms": [round(_t_scattered, 4), round(_t_ordered, 4)],
    })
    display_table(_df, "Zone maps: an ordered column can skip whole blocks")
    print(f"The ordered filter was {_t_scattered / _t_ordered:.1f}x faster — no index used.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8 · When an index *is* worth creating

    Indexes are not pointless in DuckDB. They earn their place in three situations.

    | Situation | Why the index helps |
    |---|---|
    | **Very selective lookup on text** | String comparison is expensive per row; the index avoids doing it a million times |
    | **`PRIMARY KEY` / `UNIQUE`** | DuckDB builds an index automatically to check uniqueness on every insert |
    | **Frequent point lookups in an application** | A dashboard hitting the same `WHERE id = ?` thousands of times |

    Below is the text case — the one where a manually created index genuinely pays.
    """)
    return


@app.cell
def _(con, display_table, pd, time_query):
    con.execute("""
        CREATE OR REPLACE TABLE customers AS
        SELECT i                        AS customer_id,
               'CUST-' || (i * 7919 % 1000000) AS customer_ref
        FROM range(1000000) t(i);
    """)
    _q = "SELECT * FROM customers WHERE customer_ref = 'CUST-123456';"

    _before = time_query(con, _q, reps=12)
    con.execute("CREATE INDEX idx_ref ON customers(customer_ref);")
    _after = time_query(con, _q, reps=12)

    _df = pd.DataFrame({
        "state": ["no index", "with index"],
        "ms": [round(_before, 4), round(_after, 4)],
    })
    display_table(_df, "Text point-lookup on 1,000,000 rows")
    print(f"Speedup: {_before / _after:.1f}x — the best result in this notebook.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 9 · The costs nobody mentions

    An index is not free. You are trading one resource for another.

    | Cost | What it means |
    |---|---|
    | **Disk / memory** | The index is a second copy of that column's data |
    | **Slower writes** | Every `INSERT`, `UPDATE` and `DELETE` must update the index too |
    | **Maintenance** | An index on a column nobody filters on is pure overhead |

    So the rule is not "add indexes to make things fast". It is:

    > **Measure first. Index the column you actually filter on. Measure again.
    > Keep the index only if the numbers justify it.**

    That loop — measure, change one thing, measure again — is the entire skill.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 10 · Summary

    | Question | Answer |
    |---|---|
    | What is an index? | A lookup structure beside the table, like a book's index |
    | How do I create one? | `CREATE INDEX idx_name ON table(column);` |
    | Did it help on 1,000 rows? | No — there was no time to save |
    | Did it help on 2,000,000 rows? | A little: roughly 1.5–2x |
    | Why so little? | DuckDB is columnar: it reads one column, skips blocks with zone maps, and scans in vectorised batches |
    | What helped more? | Selecting fewer columns, and filtering on an ordered column |
    | When is an index clearly worth it? | Selective text lookups, and `PRIMARY KEY` / `UNIQUE` enforcement |
    | What is the real skill? | Measuring properly — median, warm-up run, one change at a time |

    ### The sentence to remember

    > **An index removes work the database would otherwise do. If it was not doing
    > much work, an index cannot save you much.**

    ---

    ## Exercises

    1. **Selectivity.** Re-run the Section 4 experiment but filter with
       `WHERE price < 90000`, which matches most of the table. Does the index help
       at all? Explain why in one sentence.
    2. **Wrong column.** Create an index on `month` and then time a query filtering
       on `price`. What happens, and why?
    3. **Write cost.** Time inserting 100,000 rows into `sales_scaled` before and
       after creating an index. Which direction did the index move that number?
    4. **Read a plan.** Run `EXPLAIN` on a query joining two tables. Identify the
       scan nodes and the join node.
    5. **Challenge (the lab's question).** In your own words, explain to someone
       who has never used a database why creating an index did *not* make the small
       table faster. Do not use the words "index" or "scan".
    """)
    return


if __name__ == "__main__":
    app.run()
