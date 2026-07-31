"""
app_level2.py — University Bookstore · Level 2: Relationships & Joins
OMIS-105: Introduction to DBMS · Santa Clara University

Concepts covered:
    INNER JOIN, LEFT JOIN, GROUP BY, aggregate functions
    (SUM, COUNT, AVG, MAX, MIN), HAVING, multi-table queries

Run:
    pip install streamlit duckdb pandas
    streamlit run app_level2.py
"""

import os
import duckdb
import pandas as pd
import streamlit as st

# ── Config ────────────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "bookstore.duckdb")

st.set_page_config(
    page_title="Bookstore · Level 2",
    page_icon="🔗",
    layout="wide",
)

# ── DB helper ─────────────────────────────────────────────────────────────────

@st.cache_resource
def get_conn():
    return duckdb.connect(DB_PATH, read_only=True)

def run(sql: str) -> pd.DataFrame:
    return get_conn().execute(sql).df()

# ── Sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.title("📚 University Bookstore")
st.sidebar.caption("OMIS-105 · Level 2: Relationships & Joins")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🔗 Join Explorer", "📊 Aggregation Builder"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
**Level 2 Concepts**
- `JOIN` — combine rows across tables
- `INNER JOIN` — only matching rows
- `LEFT JOIN` — all left rows, NULLs if no match
- `GROUP BY` — group rows by a column
- `SUM / COUNT / AVG / MAX / MIN` — aggregate functions
- `HAVING` — filter *after* aggregation
"""
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 · HOME
# ─────────────────────────────────────────────────────────────────────────────

if page == "🏠 Home":
    st.title("🔗 Level 2: Relationships & Joins")
    st.subheader("OMIS-105 · Multi-table queries")

    st.markdown(
        """
In Level 1 every query touched a single table. The results had **IDs** where you
wanted **names** — `student_id = 3` instead of *"Carla Rivera"*.

**Level 2 fixes that.** A `JOIN` links two tables on a shared key, so you can
ask questions that span the whole database: *"Which department generated the most
revenue?"* or *"Which books did Computer Science students buy?"*
        """
    )

    st.markdown("---")
    st.subheader("📊 Multi-table Metrics")

    col1, col2, col3 = st.columns(3)

    # Revenue by top department (requires JOIN)
    top_dept = run("""
        SELECT c.department, ROUND(SUM(p.total_amount), 2) AS revenue
        FROM   purchases p
        JOIN   courses c ON p.course_id = c.course_id
        GROUP  BY c.department
        ORDER  BY revenue DESC
        LIMIT  1
    """)
    col1.metric(
        "Top Department",
        top_dept.iloc[0]["department"],
        f"${top_dept.iloc[0]['revenue']:,.2f} revenue",
    )

    # Most purchased book by title (requires JOIN)
    top_book = run("""
        SELECT b.title, COUNT(*) AS n
        FROM   purchases p
        JOIN   books b ON p.book_id = b.book_id
        GROUP  BY b.title
        ORDER  BY n DESC
        LIMIT  1
    """)
    col2.metric(
        "Most Purchased Book",
        top_book.iloc[0]["title"][:28] + "…",
        f"{top_book.iloc[0]['n']} purchases",
    )

    # Average spend per student (requires JOIN)
    avg_spend = run("""
        SELECT ROUND(AVG(total), 2) AS avg_spend
        FROM (
            SELECT student_id, SUM(total_amount) AS total
            FROM   purchases
            GROUP  BY student_id
        )
    """)
    col3.metric("Avg Spend per Student", f"${avg_spend.iloc[0]['avg_spend']:,.2f}")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("💰 Revenue by Department")
        dept_rev = run("""
            SELECT c.department,
                   COUNT(*)                    AS purchases,
                   ROUND(SUM(p.total_amount),2) AS revenue
            FROM   purchases p
            JOIN   courses c ON p.course_id = c.course_id
            GROUP  BY c.department
            ORDER  BY revenue DESC
        """)
        st.dataframe(dept_rev, use_container_width=True, hide_index=True)
        with st.expander("Show SQL"):
            st.code("""
SELECT c.department,
       COUNT(*)                     AS purchases,
       ROUND(SUM(p.total_amount),2) AS revenue
FROM   purchases p
JOIN   courses c ON p.course_id = c.course_id
GROUP  BY c.department
ORDER  BY revenue DESC;
            """, language="sql")

    with col_b:
        st.subheader("🎓 Spend by Student")
        student_spend = run("""
            SELECT s.name, s.major,
                   COUNT(*)                     AS purchases,
                   ROUND(SUM(p.total_amount),2)  AS total_spent
            FROM   purchases p
            JOIN   students s ON p.student_id = s.student_id
            GROUP  BY s.name, s.major
            ORDER  BY total_spent DESC
        """)
        st.dataframe(student_spend, use_container_width=True, hide_index=True)
        with st.expander("Show SQL"):
            st.code("""
SELECT s.name, s.major,
       COUNT(*)                     AS purchases,
       ROUND(SUM(p.total_amount),2) AS total_spent
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.name, s.major
ORDER  BY total_spent DESC;
            """, language="sql")

    st.markdown("---")
    st.subheader("📚 Required vs Optional — Revenue Comparison")
    req_comp = run("""
        SELECT CASE WHEN cb.required THEN 'Required' ELSE 'Optional' END AS book_type,
               COUNT(*)                     AS purchases,
               ROUND(SUM(p.total_amount),2)  AS revenue,
               ROUND(AVG(p.total_amount),2)  AS avg_per_purchase
        FROM   purchases p
        JOIN   course_books cb
               ON p.book_id = cb.book_id AND p.course_id = cb.course_id
        GROUP  BY cb.required
        ORDER  BY revenue DESC
    """)
    st.dataframe(req_comp, use_container_width=True, hide_index=True)
    st.caption(
        "Required books generate more revenue per purchase because they tend to be "
        "expensive textbooks. This query joins purchases to course_books on two columns."
    )
    with st.expander("Show SQL"):
        st.code("""
SELECT CASE WHEN cb.required THEN 'Required' ELSE 'Optional' END AS book_type,
       COUNT(*)                     AS purchases,
       ROUND(SUM(p.total_amount),2) AS revenue,
       ROUND(AVG(p.total_amount),2) AS avg_per_purchase
FROM   purchases p
JOIN   course_books cb
       ON p.book_id = cb.book_id AND p.course_id = cb.course_id
GROUP  BY cb.required
ORDER  BY revenue DESC;
        """, language="sql")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 · JOIN EXPLORER
# ─────────────────────────────────────────────────────────────────────────────

elif page == "🔗 Join Explorer":
    st.title("🔗 Join Explorer")
    st.markdown(
        "See what happens when you link two tables — and how `INNER JOIN` and "
        "`LEFT JOIN` produce different results."
    )

    # ── Join pair picker ──────────────────────────────────────────────────────
    JOIN_PAIRS = {
        "purchases ↔ students  (who made each purchase?)": {
            "left":  "purchases p",
            "right": "students s",
            "on":    "p.student_id = s.student_id",
            "cols":  "p.purchase_id, p.purchase_date, p.total_amount,\n       s.name, s.major, s.year",
            "left_label":  "purchases",
            "right_label": "students",
            "insight": (
                "Every purchase has a `student_id` that points to a student. "
                "The JOIN replaces that ID with the student's name and major. "
                "Since every `student_id` in `purchases` exists in `students`, "
                "INNER and LEFT JOIN return the same rows here."
            ),
        },
        "purchases ↔ books  (what was bought?)": {
            "left":  "purchases p",
            "right": "books b",
            "on":    "p.book_id = b.book_id",
            "cols":  "p.purchase_id, p.purchase_date, p.total_amount,\n       b.title, b.category, b.price",
            "left_label":  "purchases",
            "right_label": "books",
            "insight": (
                "Linking purchases to books replaces `book_id` with a human-readable title. "
                "With LEFT JOIN, books that were never purchased would appear with NULL purchase columns — "
                "useful for finding unsold inventory."
            ),
        },
        "purchases ↔ courses  (which course drove each purchase?)": {
            "left":  "purchases p",
            "right": "courses c",
            "on":    "p.course_id = c.course_id",
            "cols":  "p.purchase_id, p.purchase_date, p.total_amount,\n       c.course_name, c.department, c.semester",
            "left_label":  "purchases",
            "right_label": "courses",
            "insight": (
                "Some purchases have a NULL `course_id` (the student bought the book out of personal interest). "
                "INNER JOIN drops those rows. LEFT JOIN keeps them, with NULL in the course columns. "
                "Watch the row counts change when you switch join types!"
            ),
        },
        "books ↔ course_books  (is each book assigned to a course?)": {
            "left":  "books b",
            "right": "course_books cb",
            "on":    "b.book_id = cb.book_id",
            "cols":  "b.book_id, b.title, b.price,\n       cb.course_id, cb.required, cb.edition",
            "left_label":  "books",
            "right_label": "course_books",
            "insight": (
                "Not every book in the catalog is assigned to a course. "
                "INNER JOIN shows only books that appear in at least one course. "
                "LEFT JOIN shows all books — unassigned ones get NULL in the course_books columns."
            ),
        },
        "courses ↔ course_books  (what books does each course require?)": {
            "left":  "courses c",
            "right": "course_books cb",
            "on":    "c.course_id = cb.course_id",
            "cols":  "c.course_name, c.department, c.semester,\n       cb.book_id, cb.required, cb.edition",
            "left_label":  "courses",
            "right_label": "course_books",
            "insight": (
                "Each course can have multiple books. The result has one row per "
                "(course, book) combination — that is the nature of a one-to-many relationship."
            ),
        },
    }

    pair_label = st.selectbox("Table pair", list(JOIN_PAIRS.keys()))
    pair = JOIN_PAIRS[pair_label]

    join_type = st.radio("Join type", ["INNER JOIN", "LEFT JOIN"], horizontal=True)

    # Get the total row count for this join so the slider max is accurate
    count_sql = (
        f"SELECT COUNT(*) AS n\n"
        f"FROM   {pair['left']}\n"
        f"{join_type} {pair['right']}\n"
        f"       ON {pair['on']}"
    )
    join_count = int(run(count_sql).iloc[0]["n"])

    limit = st.slider(
        "Row limit  (0 = no limit — return all rows)",
        min_value=0, max_value=join_count,
        value=min(20, join_count), step=1,
    )

    apply_limit = limit > 0
    limit_clause = f"\nLIMIT  {limit}" if apply_limit else ""

    sql = (
        f"SELECT {pair['cols']}\n"
        f"FROM   {pair['left']}\n"
        f"{join_type} {pair['right']}\n"
        f"       ON {pair['on']}"
        f"{limit_clause};"
    )

    st.markdown("---")
    col1, col2 = st.columns([3, 2])

    with col1:
        df = run(sql.rstrip(";"))
        null_rows = df.isnull().any(axis=1).sum()
        st.subheader(f"Results  ·  {len(df)} rows")
        if not apply_limit:
            st.success(f"All {join_count} rows returned — no LIMIT applied.")
        elif null_rows > 0:
            st.info(f"⚠️ {null_rows} row(s) contain NULL values — the right table had no match.")
        st.dataframe(df, use_container_width=True)

    with col2:
        st.subheader("SQL")
        st.code(sql, language="sql")

        st.markdown("**What this join does:**")
        st.markdown(pair["insight"])

        st.markdown("---")
        st.markdown(
            f"""
**`INNER JOIN`** — keeps only rows where the `ON` condition matches in *both* tables.
Unmatched rows are silently dropped.

**`LEFT JOIN`** — keeps *all* rows from `{pair['left_label']}` (the left table).
If there is no match in `{pair['right_label']}`, the right-side columns are `NULL`.
            """
        )

    # ── Side-by-side comparison ───────────────────────────────────────────────
    st.markdown("---")
    st.subheader("⚖️ INNER vs LEFT — Side by Side")

    inner_sql = sql.replace("LEFT JOIN", "INNER JOIN")
    left_sql  = sql.replace("INNER JOIN", "LEFT JOIN")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**INNER JOIN**")
        df_inner = run(inner_sql.rstrip(";"))
        st.dataframe(df_inner, use_container_width=True)
        st.caption(f"{len(df_inner)} rows")
    with c2:
        st.markdown("**LEFT JOIN**")
        df_left = run(left_sql.rstrip(";"))
        null_count = df_left.isnull().any(axis=1).sum()
        st.dataframe(df_left, use_container_width=True)
        st.caption(f"{len(df_left)} rows  ·  {null_count} with NULLs")

    diff = len(df_left) - len(df_inner)
    if diff > 0:
        st.warning(
            f"LEFT JOIN returns **{diff} more row(s)** than INNER JOIN. "
            f"Those extra rows have no matching record in the right table."
        )
    else:
        st.success(
            "Both join types return the same number of rows — "
            "every left-table row has a match in the right table."
        )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 · AGGREGATION BUILDER
# ─────────────────────────────────────────────────────────────────────────────

elif page == "📊 Aggregation Builder":
    st.title("📊 Aggregation Builder")
    st.markdown(
        "Group rows by a column and compute an aggregate (SUM, COUNT, AVG, MAX, MIN). "
        "Then use `HAVING` to filter the groups — like `WHERE`, but for aggregated results."
    )

    # ── Query templates ───────────────────────────────────────────────────────
    AGG_TEMPLATES = {
        "Revenue by department": {
            "base_sql": """\
SELECT c.department                  AS group_col,
       {agg}(p.total_amount)         AS result
FROM   purchases p
JOIN   courses c ON p.course_id = c.course_id
GROUP  BY c.department""",
            "having_col": "result",
            "order_col":  "result",
            "agg_choices": ["SUM", "AVG", "MAX", "MIN", "COUNT"],
            "having_label": "Revenue threshold ($)",
            "having_min": 0, "having_max": 3000, "having_default": 0,
            "insight": "Joins purchases to courses so we can group by department.",
        },
        "Spend by student": {
            "base_sql": """\
SELECT s.name                        AS group_col,
       {agg}(p.total_amount)         AS result
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.name""",
            "having_col": "result",
            "order_col":  "result",
            "agg_choices": ["SUM", "AVG", "MAX", "MIN", "COUNT"],
            "having_label": "Spend threshold ($)",
            "having_min": 0, "having_max": 1500, "having_default": 0,
            "insight": "Shows how much each individual student spent in total.",
        },
        "Purchases per book": {
            "base_sql": """\
SELECT b.title                       AS group_col,
       {agg}(p.quantity)             AS result
FROM   purchases p
JOIN   books b ON p.book_id = b.book_id
GROUP  BY b.title""",
            "having_col": "result",
            "order_col":  "result",
            "agg_choices": ["COUNT", "SUM", "AVG", "MAX", "MIN"],
            "having_label": "Minimum purchases",
            "having_min": 0, "having_max": 10, "having_default": 0,
            "insight": "Links purchases to books so we can count by title.",
        },
        "Average book price by category": {
            "base_sql": """\
SELECT b.category                    AS group_col,
       {agg}(b.price)                AS result
FROM   books b
GROUP  BY b.category""",
            "having_col": "result",
            "order_col":  "result",
            "agg_choices": ["AVG", "MAX", "MIN", "SUM", "COUNT"],
            "having_label": "Price threshold ($)",
            "having_min": 0, "having_max": 200, "having_default": 0,
            "insight": "Single-table aggregation — no join needed.",
        },
        "Number of books per course": {
            "base_sql": """\
SELECT c.course_name                 AS group_col,
       {agg}(cb.book_id)             AS result
FROM   course_books cb
JOIN   courses c ON cb.course_id = c.course_id
GROUP  BY c.course_name""",
            "having_col": "result",
            "order_col":  "result",
            "agg_choices": ["COUNT", "SUM", "AVG", "MAX", "MIN"],
            "having_label": "Minimum books per course",
            "having_min": 0, "having_max": 5, "having_default": 0,
            "insight": "Counts how many books (required + optional) each course has.",
        },
        "Spend by major": {
            "base_sql": """\
SELECT s.major                       AS group_col,
       {agg}(p.total_amount)         AS result
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.major""",
            "having_col": "result",
            "order_col":  "result",
            "agg_choices": ["SUM", "AVG", "COUNT", "MAX", "MIN"],
            "having_label": "Spend threshold ($)",
            "having_min": 0, "having_max": 2500, "having_default": 0,
            "insight": "Aggregates by student major — a two-step GROUP BY across a join.",
        },
    }

    template_name = st.selectbox("Query template", list(AGG_TEMPLATES.keys()))
    tmpl = AGG_TEMPLATES[template_name]

    col_ctrl, col_ctrl2 = st.columns(2)
    with col_ctrl:
        agg_fn = st.selectbox("Aggregate function", tmpl["agg_choices"])
    with col_ctrl2:
        sort_dir = st.radio("Sort result", ["DESC (highest first)", "ASC (lowest first)"],
                            horizontal=True)
    order = "DESC" if sort_dir.startswith("DESC") else "ASC"

    # HAVING controls
    use_having = st.checkbox("Add HAVING filter")
    having_clause = ""
    having_val = 0
    if use_having:
        having_val = st.slider(
            tmpl["having_label"],
            min_value=float(tmpl["having_min"]),
            max_value=float(tmpl["having_max"]),
            value=float(tmpl["having_default"]) if tmpl["having_default"] else float(tmpl["having_min"]),
            step=float((tmpl["having_max"] - tmpl["having_min"]) / 50) or 1.0,
        )
        having_clause = f"\nHAVING {tmpl['having_col']} > {having_val:.2f}"

    base = tmpl["base_sql"].format(agg=agg_fn)
    sql = f"{base}{having_clause}\nORDER  BY {tmpl['order_col']} {order};"

    st.markdown("---")
    col1, col2 = st.columns([3, 2])

    with col1:
        df = run(sql.rstrip(";"))
        # Rename for display
        group_name = template_name.split(" by ")[-1].strip().title()
        df.columns = [group_name, agg_fn]
        if agg_fn in ("SUM", "AVG", "MAX", "MIN"):
            df[agg_fn] = df[agg_fn].round(2)
        st.subheader(f"Results  ·  {len(df)} groups")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("SQL")
        st.code(sql, language="sql")

        st.markdown("**What this does:**")
        st.markdown(
            f"""
- `{agg_fn}(...)` — computes the {agg_fn.lower()} of the target column
- `GROUP BY` — collapses all rows with the same group value into one result row
- {f'`HAVING result > {having_val:.2f}` — keeps only groups where {agg_fn} exceeds {having_val:.2f}' if use_having else '*(no HAVING filter applied)*'}

_{tmpl["insight"]}_
            """
        )

        if use_having:
            st.markdown("---")
            st.markdown(
                """
**`WHERE` vs `HAVING`:**

`WHERE` filters individual rows *before* grouping.
`HAVING` filters groups *after* aggregation.

You cannot write `WHERE SUM(...) > x` — the aggregation
hasn't happened yet at that point. Use `HAVING` instead.
                """
            )

    # ── Concept illustration: WHERE vs HAVING ────────────────────────────────
    st.markdown("---")
    st.subheader("💡 WHERE vs HAVING — Illustrated")
    st.markdown(
        "The same question answered two ways. "
        "Note which clause filters rows and which filters groups."
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Using WHERE (filters rows before grouping)**")
        st.code("""
-- Students in Computer Science only,
-- then total their spending
SELECT s.name,
       SUM(p.total_amount) AS total_spent
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
WHERE  s.major = 'Computer Science'
GROUP  BY s.name
ORDER  BY total_spent DESC;
        """, language="sql")
        df_where = run("""
            SELECT s.name,
                   ROUND(SUM(p.total_amount),2) AS total_spent
            FROM   purchases p
            JOIN   students s ON p.student_id = s.student_id
            WHERE  s.major = 'Computer Science'
            GROUP  BY s.name
            ORDER  BY total_spent DESC
        """)
        st.dataframe(df_where, use_container_width=True, hide_index=True)

    with c2:
        st.markdown("**Using HAVING (filters groups after aggregation)**")
        st.code("""
-- All students grouped,
-- then keep only big spenders (> $500)
SELECT s.name,
       SUM(p.total_amount) AS total_spent
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.name
HAVING SUM(p.total_amount) > 500
ORDER  BY total_spent DESC;
        """, language="sql")
        df_having = run("""
            SELECT s.name,
                   ROUND(SUM(p.total_amount),2) AS total_spent
            FROM   purchases p
            JOIN   students s ON p.student_id = s.student_id
            GROUP  BY s.name
            HAVING SUM(p.total_amount) > 500
            ORDER  BY total_spent DESC
        """)
        st.dataframe(df_having, use_container_width=True, hide_index=True)

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption("OMIS-105 · Santa Clara University · Leavey School of Business · Level 2 of 3")
