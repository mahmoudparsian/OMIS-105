"""
Streamlit + DuckDB — Aggregation & GROUP BY Explorer
=====================================================
An e-commerce schema (customers, products, orders) designed to teach:

  - COUNT, COUNT(DISTINCT)
  - SUM, AVG
  - MIN, MAX
  - STRING_AGG / LIST / GROUP_CONCAT  (see *what* is aggregated per key)
  - GROUP BY with multiple columns
  - HAVING (filter on aggregated values)
  - SQL Explorer for free-form practice

Every aggregation tab shows the RAW rows alongside the aggregated result
so students can manually verify what each group contains.

Usage:
    pip install streamlit duckdb pandas
    streamlit run app_aggregation.py
"""

import streamlit as st
import duckdb
import pandas as pd

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

DB_FILE = "aggregation_demo.duckdb"


def get_connection() -> duckdb.DuckDBPyConnection:
    if "db_conn" not in st.session_state:
        conn = duckdb.connect(DB_FILE)
        _init_tables(conn)
        st.session_state.db_conn = conn
    return st.session_state.db_conn


def _init_tables(conn: duckdb.DuckDBPyConnection):
    """Create and seed the e-commerce tables."""

    # ---- customers ----------------------------------------------------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id   VARCHAR PRIMARY KEY,
            customer_name VARCHAR NOT NULL,
            city          VARCHAR NOT NULL,
            country       VARCHAR NOT NULL
        )
    """)
    if conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 0:
        conn.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", [
            ("C1", "Alice",   "New York",  "USA"),
            ("C2", "Bob",     "Toronto",   "Canada"),
            ("C3", "Charlie", "New York",  "USA"),
            ("C4", "Diana",   "Berlin",    "Germany"),
            ("C5", "Eve",     "Vancouver", "Canada"),
            ("C6", "Frank",   "Chicago",   "USA"),
        ])

    # ---- products -----------------------------------------------------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id   VARCHAR PRIMARY KEY,
            product_name VARCHAR NOT NULL,
            category     VARCHAR NOT NULL,
            price        DECIMAL(10,2) NOT NULL
        )
    """)
    if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        conn.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", [
            ("P1", "Laptop",      "Electronics", 999.99),
            ("P2", "Mouse",       "Electronics",  29.99),
            ("P3", "Keyboard",    "Electronics",  79.99),
            ("P4", "Desk Chair",  "Furniture",   249.99),
            ("P5", "Standing Desk","Furniture",  549.99),
            ("P6", "Notebook",    "Stationery",    4.99),
            ("P7", "Pen Set",     "Stationery",   12.99),
            ("P8", "Monitor",     "Electronics", 399.99),
        ])

    # ---- orders -------------------------------------------------------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id    VARCHAR PRIMARY KEY,
            customer_id VARCHAR NOT NULL,
            product_id  VARCHAR NOT NULL,
            quantity    INTEGER NOT NULL,
            order_date  DATE NOT NULL
        )
    """)
    if conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
        conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", [
            # Alice: 4 orders across categories
            ("O01", "C1", "P1", 1, "2025-01-05"),
            ("O02", "C1", "P2", 2, "2025-01-05"),
            ("O03", "C1", "P6", 5, "2025-02-10"),
            ("O04", "C1", "P4", 1, "2025-03-15"),
            # Bob: 3 orders
            ("O05", "C2", "P1", 1, "2025-01-10"),
            ("O06", "C2", "P3", 1, "2025-01-10"),
            ("O07", "C2", "P5", 1, "2025-02-20"),
            # Charlie: 3 orders (same city as Alice — good for city grouping)
            ("O08", "C3", "P2", 3, "2025-01-15"),
            ("O09", "C3", "P8", 2, "2025-02-25"),
            ("O10", "C3", "P7", 4, "2025-03-01"),
            # Diana: 2 orders
            ("O11", "C4", "P1", 1, "2025-02-05"),
            ("O12", "C4", "P6", 10, "2025-02-05"),
            # Eve: 3 orders
            ("O13", "C5", "P4", 2, "2025-01-20"),
            ("O14", "C5", "P5", 1, "2025-03-10"),
            ("O15", "C5", "P2", 1, "2025-03-10"),
            # Frank: 2 orders
            ("O16", "C6", "P8", 1, "2025-01-25"),
            ("O17", "C6", "P3", 2, "2025-02-15"),
        ])


def reset_tables():
    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS orders")
    conn.execute("DROP TABLE IF EXISTS products")
    conn.execute("DROP TABLE IF EXISTS customers")
    _init_tables(conn)


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def run_query(sql: str) -> pd.DataFrame:
    conn = get_connection()
    return conn.execute(sql).fetchdf()


def run_query_safe(sql: str):
    """Run SQL, return (df, None) on success or (None, error_str) on failure."""
    try:
        conn = get_connection()
        result = conn.execute(sql)
        try:
            cols = [d[0] for d in result.description]
            rows = result.fetchall()
            return pd.DataFrame(rows, columns=cols), None
        except Exception:
            return None, None
    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------------------------
# The "detail" view: join orders with customers & products for a flat view
# ---------------------------------------------------------------------------

DETAIL_SQL = """
    SELECT
        o.order_id,
        c.customer_name,
        c.city,
        c.country,
        p.product_name,
        p.category,
        p.price,
        o.quantity,
        ROUND(p.price * o.quantity, 2) AS line_total,
        o.order_date
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products  p ON o.product_id  = p.product_id
    ORDER BY o.order_id
"""


def get_detail_df() -> pd.DataFrame:
    return run_query(DETAIL_SQL)


# ---------------------------------------------------------------------------
# Streamlit App
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Aggregation Explorer", page_icon="📊", layout="wide")

st.title("📊 Aggregation & GROUP BY Explorer")
st.caption(
    "Powered by **Streamlit** and **DuckDB** — "
    "See exactly what each GROUP BY aggregates"
)

# Sidebar
with st.sidebar:
    st.header("Schema")
    st.markdown(
        "**customers** (customer_id, customer_name, city, country)\n\n"
        "**products** (product_id, product_name, category, price)\n\n"
        "**orders** (order_id, customer_id, product_id, quantity, order_date)"
    )
    st.divider()

    st.subheader("DuckDB Aggregation Functions")
    st.code(
        "COUNT(*), COUNT(DISTINCT col)\n"
        "SUM(col), AVG(col)\n"
        "MIN(col), MAX(col)\n"
        "STRING_AGG(col, ', ')\n"
        "LIST(col)\n"
        "ROUND(expr, n)",
        language="sql",
    )
    st.divider()

    st.subheader("Key Insight")
    st.info(
        "**STRING_AGG** and **LIST** let you *see* which values "
        "are being collapsed into each group. Use them to verify "
        "that COUNT, SUM, and AVG are computing what you expect."
    )
    st.divider()

    if st.button("Reset All Tables", type="secondary"):
        reset_tables()
        st.success("Tables reset to original data!")
        st.rerun()

    st.caption(f"DuckDB file: `{DB_FILE}`")


# Tabs
tab_data, tab_count, tab_sum_avg, tab_min_max, tab_concat, tab_having, tab_sql = st.tabs([
    "📋 View Data",
    "🔢 COUNT",
    "➕ SUM / AVG",
    "↕️ MIN / MAX",
    "🔗 STRING_AGG / LIST",
    "🚧 HAVING",
    "🧪 SQL Explorer",
])


# ---- TAB: View Data ---------------------------------------------------------
with tab_data:
    st.subheader("Raw Tables")

    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("##### customers")
        st.dataframe(run_query("SELECT * FROM customers ORDER BY customer_id"),
                     use_container_width=True, hide_index=True)
    with t2:
        st.markdown("##### products")
        st.dataframe(run_query("SELECT * FROM products ORDER BY product_id"),
                     use_container_width=True, hide_index=True)
    with t3:
        st.markdown("##### orders")
        st.dataframe(run_query("SELECT * FROM orders ORDER BY order_id"),
                     use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("##### Joined Detail View (orders + customers + products)")
    st.info("This flat view joins all three tables — it is the starting point for most aggregation queries below.")
    st.code(DETAIL_SQL.strip(), language="sql")
    df_detail = get_detail_df()
    st.dataframe(df_detail, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_detail)} order line(s)")


# ---- TAB: COUNT --------------------------------------------------------------
with tab_count:
    st.subheader("COUNT & COUNT(DISTINCT)")

    group_col = st.selectbox(
        "GROUP BY column",
        ["customer_name", "country", "city", "category", "product_name", "order_date"],
        key="count_group",
    )

    # Build the query — include STRING_AGG so students see what's in each group
    if group_col in ("customer_name", "country", "city"):
        # Grouping by a customer-level attribute
        sql_count = f"""
SELECT
    {group_col},
    COUNT(*)                           AS total_orders,
    COUNT(DISTINCT product_name)       AS distinct_products,
    STRING_AGG(product_name, ', '
               ORDER BY product_name)  AS products_in_group
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
GROUP BY {group_col}
ORDER BY total_orders DESC;"""
    elif group_col == "order_date":
        sql_count = f"""
SELECT
    order_date,
    COUNT(*)                           AS total_orders,
    COUNT(DISTINCT customer_name)      AS distinct_customers,
    STRING_AGG(customer_name, ', '
               ORDER BY customer_name) AS customers_in_group,
    STRING_AGG(product_name, ', '
               ORDER BY product_name)  AS products_in_group
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
GROUP BY order_date
ORDER BY order_date;"""
    else:
        # Grouping by a product-level attribute
        sql_count = f"""
SELECT
    {group_col},
    COUNT(*)                           AS total_orders,
    COUNT(DISTINCT customer_name)      AS distinct_customers,
    STRING_AGG(customer_name, ', '
               ORDER BY customer_name) AS customers_in_group
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
GROUP BY {group_col}
ORDER BY total_orders DESC;"""

    col_raw, col_agg = st.columns(2)
    with col_raw:
        st.markdown("##### Raw Detail Rows")
        df_raw = get_detail_df()
        # Highlight the GROUP BY column
        st.dataframe(df_raw, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_raw)} row(s)")
    with col_agg:
        st.markdown("##### Aggregated Result")
        st.code(sql_count.strip(), language="sql")
        df_agg = run_query(sql_count)
        st.dataframe(df_agg, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_agg)} group(s)")

    st.info(
        "**Notice:** The `STRING_AGG` column shows *exactly* which values are "
        "being counted in each group. Compare it to the raw rows on the left!"
    )


# ---- TAB: SUM / AVG ---------------------------------------------------------
with tab_sum_avg:
    st.subheader("SUM & AVG")

    group_col2 = st.selectbox(
        "GROUP BY column",
        ["customer_name", "country", "city", "category"],
        key="sum_group",
    )

    sql_sum = f"""
SELECT
    {group_col2},
    COUNT(*)                              AS order_count,
    SUM(quantity)                          AS total_qty,
    ROUND(SUM(price * quantity), 2)        AS total_spent,
    ROUND(AVG(price * quantity), 2)        AS avg_line_total,
    STRING_AGG(
        product_name || ' (qty ' || quantity || ' = $'
            || ROUND(price * quantity, 2) || ')',
        ',  '
        ORDER BY product_name
    )                                      AS line_details
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
GROUP BY {group_col2}
ORDER BY total_spent DESC;"""

    col_r, col_a = st.columns(2)
    with col_r:
        st.markdown("##### Raw Detail Rows")
        st.dataframe(get_detail_df(), use_container_width=True, hide_index=True)
    with col_a:
        st.markdown("##### Aggregated Result")
        st.code(sql_sum.strip(), language="sql")
        st.dataframe(run_query(sql_sum), use_container_width=True, hide_index=True)

    st.info(
        "**`line_details`** shows each product with its quantity and dollar amount, "
        "so you can manually add them up and verify the SUM and AVG."
    )


# ---- TAB: MIN / MAX ---------------------------------------------------------
with tab_min_max:
    st.subheader("MIN & MAX")

    group_col3 = st.selectbox(
        "GROUP BY column",
        ["customer_name", "country", "category"],
        key="minmax_group",
    )

    sql_minmax = f"""
SELECT
    {group_col3},
    COUNT(*)                              AS order_count,
    MIN(price)                             AS min_price,
    MAX(price)                             AS max_price,
    MIN(order_date)                        AS first_order,
    MAX(order_date)                        AS last_order,
    LIST(DISTINCT product_name
         ORDER BY product_name)            AS products_list,
    LIST(price ORDER BY price)             AS prices_list
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
GROUP BY {group_col3}
ORDER BY {group_col3};"""

    col_r2, col_a2 = st.columns(2)
    with col_r2:
        st.markdown("##### Raw Detail Rows")
        st.dataframe(get_detail_df(), use_container_width=True, hide_index=True)
    with col_a2:
        st.markdown("##### Aggregated Result")
        st.code(sql_minmax.strip(), language="sql")
        st.dataframe(run_query(sql_minmax), use_container_width=True, hide_index=True)

    st.info(
        "**`prices_list`** shows all prices in sorted order — "
        "the first element is the MIN and the last is the MAX. "
        "**`products_list`** uses `LIST(DISTINCT ...)` to deduplicate."
    )


# ---- TAB: STRING_AGG / LIST -------------------------------------------------
with tab_concat:
    st.subheader("STRING_AGG & LIST  (Group Concatenation)")
    st.markdown(
        "These functions let you **see** what is inside each group. "
        "In other databases these are called `GROUP_CONCAT` (MySQL) "
        "or `ARRAY_AGG` (PostgreSQL). DuckDB supports both `STRING_AGG` "
        "(returns text) and `LIST` (returns an array)."
    )

    group_col4 = st.selectbox(
        "GROUP BY column",
        ["customer_name", "country", "city", "category", "order_date"],
        key="concat_group",
    )

    sql_concat = f"""
SELECT
    {group_col4},
    COUNT(*) AS order_count,

    -- STRING_AGG: comma-separated text
    STRING_AGG(product_name, ', '
               ORDER BY product_name)     AS products_csv,

    -- STRING_AGG with DISTINCT
    STRING_AGG(DISTINCT product_name, ', '
               ORDER BY product_name)     AS distinct_products_csv,

    -- LIST: DuckDB array
    LIST(product_name
         ORDER BY product_name)           AS products_array,

    -- LIST with DISTINCT
    LIST(DISTINCT product_name
         ORDER BY product_name)           AS distinct_products_array,

    -- Concatenate multiple columns for richer detail
    STRING_AGG(
        product_name || ' ($' || ROUND(price * quantity, 2) || ')',
        ',  '
        ORDER BY product_name
    )                                      AS detailed_breakdown

FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
GROUP BY {group_col4}
ORDER BY {group_col4};"""

    st.code(sql_concat.strip(), language="sql")

    col_r3, col_a3 = st.columns([1, 2])
    with col_r3:
        st.markdown("##### Raw Detail Rows")
        st.dataframe(get_detail_df(), use_container_width=True, hide_index=True)
    with col_a3:
        st.markdown("##### Aggregated Result")
        df_concat = run_query(sql_concat)
        st.dataframe(df_concat, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_concat)} group(s)")

    st.divider()
    st.markdown("##### Function Comparison")
    comp_data = {
        "Function": [
            "STRING_AGG(col, ', ')",
            "STRING_AGG(DISTINCT col, ', ')",
            "LIST(col)",
            "LIST(DISTINCT col)",
            "GROUP_CONCAT(col, ', ')",
            "ARRAY_AGG(col)",
        ],
        "Returns": [
            "Comma-separated text",
            "Comma-separated text (no duplicates)",
            "DuckDB array [ ... ]",
            "DuckDB array (no duplicates)",
            "Same as STRING_AGG (MySQL compat)",
            "Same as LIST (PostgreSQL compat)",
        ],
        "DuckDB Support": ["Yes", "Yes", "Yes", "Yes", "Yes", "Yes"],
    }
    st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)


# ---- TAB: HAVING ------------------------------------------------------------
with tab_having:
    st.subheader("HAVING — Filter on Aggregated Values")
    st.markdown(
        "`WHERE` filters **rows** *before* grouping. "
        "`HAVING` filters **groups** *after* aggregation. "
        "This is one of the most important distinctions in SQL!"
    )

    group_col5 = st.selectbox(
        "GROUP BY column",
        ["customer_name", "country", "city", "category"],
        key="having_group",
    )

    hcol1, hcol2, hcol3 = st.columns(3)
    with hcol1:
        having_func = st.selectbox(
            "Aggregate function",
            ["COUNT(*)", "SUM(quantity)", "ROUND(SUM(price * quantity), 2)",
             "AVG(price)", "COUNT(DISTINCT product_name)"],
            key="having_func",
        )
    with hcol2:
        having_op = st.selectbox("Operator", [">", ">=", "=", "<=", "<", "!="], key="having_op")
    with hcol3:
        having_val = st.number_input("Value", value=2, step=1, key="having_val")

    # Friendly alias for the function
    func_alias = {
        "COUNT(*)": "group_count",
        "SUM(quantity)": "total_qty",
        "ROUND(SUM(price * quantity), 2)": "total_spent",
        "AVG(price)": "avg_price",
        "COUNT(DISTINCT product_name)": "distinct_products",
    }.get(having_func, "agg_value")

    sql_having = f"""
SELECT
    {group_col5},
    {having_func} AS {func_alias},
    STRING_AGG(product_name, ', '
               ORDER BY product_name)  AS products_in_group,
    STRING_AGG(
        product_name || ' (qty ' || quantity || ')',
        ', '
        ORDER BY product_name
    )                                   AS detail
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
GROUP BY {group_col5}
HAVING {having_func} {having_op} {having_val}
ORDER BY {func_alias} DESC;"""

    # Also show the WITHOUT HAVING version for comparison
    sql_no_having = f"""
SELECT
    {group_col5},
    {having_func} AS {func_alias},
    STRING_AGG(product_name, ', '
               ORDER BY product_name)  AS products_in_group
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
GROUP BY {group_col5}
ORDER BY {func_alias} DESC;"""

    st.code(sql_having.strip(), language="sql")

    col_all, col_filtered = st.columns(2)
    with col_all:
        st.markdown("##### ALL Groups (without HAVING)")
        df_all = run_query(sql_no_having)
        st.dataframe(df_all, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_all)} group(s)")

    with col_filtered:
        st.markdown(f"##### Filtered Groups (HAVING {having_func} {having_op} {having_val})")
        df_having = run_query(sql_having)
        if len(df_having) > 0:
            st.dataframe(df_having, use_container_width=True, hide_index=True)
            st.caption(f"{len(df_having)} group(s) passed the HAVING filter")
        else:
            st.warning("No groups satisfy the HAVING condition. Try adjusting the value.")

    st.divider()
    st.markdown("##### WHERE vs HAVING — Side by Side")
    where_vs_having = {
        "": ["WHERE", "HAVING"],
        "Filters": ["Individual rows", "Aggregated groups"],
        "Runs": ["BEFORE GROUP BY", "AFTER GROUP BY"],
        "Can use aggregates?": ["No", "Yes"],
        "Example": [
            f"WHERE price > 50",
            f"HAVING COUNT(*) > 2",
        ],
    }
    st.dataframe(pd.DataFrame(where_vs_having), use_container_width=True, hide_index=True)


# ---- TAB: SQL Explorer -------------------------------------------------------
with tab_sql:
    st.subheader("SQL Explorer")
    st.info(
        "Write any SQL against **customers**, **products**, and **orders**. "
        "Try combining aggregation functions with GROUP BY and HAVING!"
    )

    examples = {
        "(custom)": "",
        "Revenue by customer": (
            "SELECT\n"
            "    c.customer_name,\n"
            "    COUNT(*) AS orders,\n"
            "    ROUND(SUM(p.price * o.quantity), 2) AS total_spent,\n"
            "    STRING_AGG(p.product_name, ', ' ORDER BY p.product_name) AS products\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.customer_id\n"
            "JOIN products  p ON o.product_id  = p.product_id\n"
            "GROUP BY c.customer_name\n"
            "ORDER BY total_spent DESC;"
        ),
        "Revenue by category": (
            "SELECT\n"
            "    p.category,\n"
            "    COUNT(*) AS order_lines,\n"
            "    SUM(o.quantity) AS total_units,\n"
            "    ROUND(SUM(p.price * o.quantity), 2) AS total_revenue,\n"
            "    LIST(DISTINCT p.product_name ORDER BY p.product_name) AS products\n"
            "FROM orders o\n"
            "JOIN products p ON o.product_id = p.product_id\n"
            "GROUP BY p.category\n"
            "ORDER BY total_revenue DESC;"
        ),
        "Monthly summary": (
            "SELECT\n"
            "    STRFTIME(o.order_date, '%Y-%m') AS month,\n"
            "    COUNT(*) AS orders,\n"
            "    COUNT(DISTINCT o.customer_id) AS unique_customers,\n"
            "    ROUND(SUM(p.price * o.quantity), 2) AS revenue,\n"
            "    STRING_AGG(DISTINCT c.customer_name, ', '\n"
            "               ORDER BY c.customer_name) AS customers\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.customer_id\n"
            "JOIN products  p ON o.product_id  = p.product_id\n"
            "GROUP BY month\n"
            "ORDER BY month;"
        ),
        "Customers who spent > $500": (
            "SELECT\n"
            "    c.customer_name,\n"
            "    c.country,\n"
            "    ROUND(SUM(p.price * o.quantity), 2) AS total_spent,\n"
            "    STRING_AGG(\n"
            "        p.product_name || ' ($' || ROUND(p.price * o.quantity, 2) || ')',\n"
            "        ',  ' ORDER BY p.product_name\n"
            "    ) AS breakdown\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.customer_id\n"
            "JOIN products  p ON o.product_id  = p.product_id\n"
            "GROUP BY c.customer_name, c.country\n"
            "HAVING SUM(p.price * o.quantity) > 500\n"
            "ORDER BY total_spent DESC;"
        ),
        "Country with most distinct products ordered": (
            "SELECT\n"
            "    c.country,\n"
            "    COUNT(DISTINCT p.product_id) AS distinct_products,\n"
            "    LIST(DISTINCT p.product_name ORDER BY p.product_name) AS product_list\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.customer_id\n"
            "JOIN products  p ON o.product_id  = p.product_id\n"
            "GROUP BY c.country\n"
            "ORDER BY distinct_products DESC;"
        ),
        "Products never ordered": (
            "SELECT p.*\n"
            "FROM products p\n"
            "LEFT JOIN orders o ON p.product_id = o.product_id\n"
            "WHERE o.order_id IS NULL;"
        ),
        "CROSS-TAB: customer × category spending": (
            "SELECT\n"
            "    c.customer_name,\n"
            "    ROUND(SUM(CASE WHEN p.category = 'Electronics' THEN p.price * o.quantity ELSE 0 END), 2) AS electronics,\n"
            "    ROUND(SUM(CASE WHEN p.category = 'Furniture'   THEN p.price * o.quantity ELSE 0 END), 2) AS furniture,\n"
            "    ROUND(SUM(CASE WHEN p.category = 'Stationery'  THEN p.price * o.quantity ELSE 0 END), 2) AS stationery,\n"
            "    ROUND(SUM(p.price * o.quantity), 2) AS grand_total\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.customer_id\n"
            "JOIN products  p ON o.product_id  = p.product_id\n"
            "GROUP BY c.customer_name\n"
            "ORDER BY grand_total DESC;"
        ),
        "Describe tables": (
            "DESCRIBE customers;\n"
            "-- Also try: DESCRIBE products;\n"
            "-- Also try: DESCRIBE orders;"
        ),
    }

    chosen = st.selectbox("Quick examples", examples.keys(), key="sql_ex")
    default_sql = examples[chosen]

    sql_input = st.text_area(
        "Enter your SQL",
        value=default_sql,
        height=200,
        placeholder="SELECT category, COUNT(*) FROM products GROUP BY category;",
        key="sql_input",
    )

    if st.button("Run Query", type="primary", key="run_sql"):
        if not sql_input.strip():
            st.error("Please enter a SQL statement.")
        else:
            # Support multiple statements separated by semicolons
            statements = [s.strip() for s in sql_input.strip().split(";") if s.strip() and not s.strip().startswith("--")]
            for i, stmt in enumerate(statements):
                if len(statements) > 1:
                    st.markdown(f"**Statement {i+1}:**")
                    st.code(stmt + ";", language="sql")
                df, err = run_query_safe(stmt)
                if err:
                    st.error(f"SQL Error: {err}")
                elif df is not None:
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.caption(f"Returned {len(df)} row(s)")
                else:
                    st.success("Statement executed successfully.")


# Footer
st.divider()
st.caption(
    "Built with [Streamlit](https://streamlit.io) • "
    "Data stored in [DuckDB](https://duckdb.org) • "
    "Designed for introductory DBMS courses"
)
