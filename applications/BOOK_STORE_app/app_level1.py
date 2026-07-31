"""
app_level1.py — University Bookstore · Level 1: Explore & Query
OMIS-105: Introduction to DBMS · Santa Clara University

Concepts covered:
    SELECT, FROM, WHERE, ORDER BY, LIMIT, BETWEEN, comparison operators

Run:
    pip install streamlit duckdb pandas
    streamlit run app_level1.py
"""

import os
import duckdb
import pandas as pd
import streamlit as st

# ── Config ────────────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "bookstore.duckdb")

st.set_page_config(
    page_title="Bookstore · Level 1",
    page_icon="📚",
    layout="wide",
)

# ── DB helper ─────────────────────────────────────────────────────────────────

@st.cache_resource
def get_conn():
    return duckdb.connect(DB_PATH, read_only=True)

def run(sql: str) -> pd.DataFrame:
    return get_conn().execute(sql).df()

# ── Sidebar navigation ────────────────────────────────────────────────────────

st.sidebar.title("📚 University Bookstore")
st.sidebar.caption("OMIS-105 · Level 1: Explore & Query")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🔍 Table Explorer", "🛠️ Query Builder"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
**Level 1 Concepts**
- `SELECT` — choose columns
- `FROM` — choose a table
- `WHERE` — filter rows
- `ORDER BY` — sort results
- `LIMIT` — cap the result set
- `BETWEEN` — range filters
"""
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 · HOME
# ─────────────────────────────────────────────────────────────────────────────

if page == "🏠 Home":
    st.title("📚 University Bookstore Database")
    st.subheader("OMIS-105 · Level 1: Explore & Query")

    st.markdown(
        """
Welcome to the **University Bookstore** — a relational database that tracks
students, courses, books, and purchases across two semesters at Santa Clara University.

In Level 1 you will explore the five tables and run guided queries using
`SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, and `BETWEEN`.
No joins yet — each query touches exactly one table.
        """
    )

    st.markdown("---")
    st.subheader("📊 Dataset Snapshot")

    tables = ["students", "courses", "books", "course_books", "purchases"]
    descriptions = {
        "students":     "The buyers — name, major, year, GPA",
        "courses":      "Demand drivers — department, credits, semester",
        "books":        "Inventory — title, author, price, category",
        "course_books": "Which books belong to which course (required / optional)",
        "purchases":    "Every transaction — who bought what, when, and for how much",
    }

    cols = st.columns(5)
    for col, table in zip(cols, tables):
        n = run(f"SELECT COUNT(*) AS n FROM {table}").iloc[0]["n"]
        col.metric(label=table, value=f"{n} rows", help=descriptions[table])

    st.markdown("---")
    st.subheader("🗂️ Table Descriptions")

    for table, desc in descriptions.items():
        with st.expander(f"`{table}` — {desc}"):
            df = run(f"SELECT * FROM {table} LIMIT 5")
            st.dataframe(df, use_container_width=True)
            st.caption(f"Showing first 5 rows of `{table}`.")

    st.markdown("---")
    st.subheader("💡 The Story So Far")
    col1, col2, col3 = st.columns(3)

    rev = run("""
        SELECT c.department, ROUND(SUM(p.total_amount),2) AS revenue
        FROM purchases p JOIN courses c ON p.course_id = c.course_id
        GROUP BY c.department ORDER BY revenue DESC LIMIT 1
    """)
    top_dept = rev.iloc[0]["department"]
    top_rev  = rev.iloc[0]["revenue"]
    col1.metric("Top Department (Revenue)", top_dept, f"${top_rev:,.2f}")

    top_book = run("""
        SELECT b.title, COUNT(*) AS times_bought
        FROM purchases p JOIN books b ON p.book_id = b.book_id
        GROUP BY b.title ORDER BY times_bought DESC LIMIT 1
    """)
    col2.metric("Most Purchased Book",
                top_book.iloc[0]["title"][:30] + "…",
                f"{top_book.iloc[0]['times_bought']} purchases")

    total = run("SELECT ROUND(SUM(total_amount),2) AS t FROM purchases").iloc[0]["t"]
    col3.metric("Total Revenue", f"${total:,.2f}", "across 2 semesters")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 · TABLE EXPLORER
# ─────────────────────────────────────────────────────────────────────────────

elif page == "🔍 Table Explorer":
    st.title("🔍 Table Explorer")
    st.markdown("Pick any table, choose which columns to display, and see the SQL that ran.")

    table = st.selectbox(
        "Table",
        ["students", "courses", "books", "course_books", "purchases"],
    )

    # Get column names
    cols_df = run(f"DESCRIBE {table}")
    all_cols = cols_df["column_name"].tolist()

    selected_cols = st.multiselect(
        "Columns to show  (leave empty = all)",
        options=all_cols,
        default=[],
    )

    table_count = int(run(f"SELECT COUNT(*) AS n FROM {table}").iloc[0]["n"])
    limit = st.slider(
        "Row limit  (0 = no limit — return all rows)",
        min_value=0, max_value=table_count,
        value=min(20, table_count), step=1,
    )

    col_clause = ", ".join(selected_cols) if selected_cols else "*"
    apply_limit = limit > 0
    limit_clause = f"\nLIMIT  {limit}" if apply_limit else ""
    sql = f"SELECT {col_clause}\nFROM   {table}{limit_clause};"

    st.markdown("---")
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("Results")
        df = run(sql.rstrip(";"))
        st.dataframe(df, use_container_width=True)
        st.caption(
            f"{len(df)} rows returned — **all {table_count} rows** (no LIMIT applied)."
            if not apply_limit else
            f"{len(df)} of {table_count} rows returned."
        )

    with col_right:
        st.subheader("SQL")
        st.code(sql, language="sql")
        limit_explanation = (
            "- _(no `LIMIT` clause)_ — all rows in the table are returned"
            if not apply_limit else
            f"- `LIMIT {limit}` — return at most {limit} rows; "
            f"remaining {table_count - limit} rows are not fetched"
        )
        st.markdown(
            f"""
**What this does:**
- `SELECT {col_clause}` — retrieve {'all columns' if col_clause == '*' else 'the selected columns'}
- `FROM {table}` — from the `{table}` table
{limit_explanation}
            """
        )

    st.markdown("---")
    st.subheader("📋 Column Reference")
    st.dataframe(
        cols_df[["column_name", "column_type", "null"]].rename(
            columns={"column_name": "Column", "column_type": "Type", "null": "Nullable"}
        ),
        use_container_width=True,
        hide_index=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 · QUERY BUILDER
# ─────────────────────────────────────────────────────────────────────────────

elif page == "🛠️ Query Builder":
    st.title("🛠️ Query Builder")
    st.markdown(
        "Build queries using the controls below. The SQL updates live — "
        "watch how each setting changes the query before running it."
    )

    query_choice = st.selectbox(
        "Choose a query template",
        [
            "1 · Books by category",
            "2 · Students by major",
            "3 · Top N most expensive books",
            "4 · Books in a price range",
            "5 · Students with GPA above a threshold",
            "6 · Purchases in a date range",
        ],
    )

    st.markdown("---")

    # ── Template 1: Books by category ────────────────────────────────────────
    if query_choice.startswith("1"):
        st.subheader("📖 Books by Category")

        categories = run("SELECT DISTINCT category FROM books ORDER BY category")["category"].tolist()
        cat = st.selectbox("Category", categories)
        sort_col = st.selectbox("Sort by", ["price", "title", "author"])
        sort_dir = st.radio("Order", ["ASC", "DESC"], horizontal=True)

        sql = (
            f"SELECT title, author, price, publisher\n"
            f"FROM   books\n"
            f"WHERE  category = '{cat}'\n"
            f"ORDER BY {sort_col} {sort_dir};"
        )

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql.rstrip(";"))
            st.dataframe(df, use_container_width=True)
            st.caption(f"{len(df)} books in the '{cat}' category.")
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                f"""
**Key clause:** `WHERE category = '{cat}'`

`WHERE` filters rows *before* they are returned.
Only rows where the `category` column exactly equals
`'{cat}'` are included in the result.
                """
            )

    # ── Template 2: Students by major ────────────────────────────────────────
    elif query_choice.startswith("2"):
        st.subheader("🎓 Students by Major")

        majors = run("SELECT DISTINCT major FROM students ORDER BY major")["major"].tolist()
        major = st.selectbox("Major", majors)
        sort_col = st.selectbox("Sort by", ["name", "year", "gpa"])
        sort_dir = st.radio("Order", ["ASC", "DESC"], horizontal=True)

        sql = (
            f"SELECT name, email, year, gpa\n"
            f"FROM   students\n"
            f"WHERE  major = '{major}'\n"
            f"ORDER BY {sort_col} {sort_dir};"
        )

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql.rstrip(";"))
            st.dataframe(df, use_container_width=True)
            st.caption(f"{len(df)} students in '{major}'.")
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                f"""
**Key clause:** `WHERE major = '{major}'`

String comparisons in SQL use single quotes.
`ORDER BY {sort_col} {sort_dir}` sorts the result
{'A→Z / lowest first' if sort_dir == 'ASC' else 'Z→A / highest first'}.
                """
            )

    # ── Template 3: Top N most expensive books ────────────────────────────────
    elif query_choice.startswith("3"):
        st.subheader("💰 Top N Most Expensive Books")

        n = st.slider("How many books?", 1, 20, 5)
        cat_options = ["All categories"] + run(
            "SELECT DISTINCT category FROM books ORDER BY category"
        )["category"].tolist()
        cat_filter = st.selectbox("Category filter", cat_options)

        where_clause = "" if cat_filter == "All categories" else f"\nWHERE  category = '{cat_filter}'"
        sql = (
            f"SELECT title, author, category, price\n"
            f"FROM   books"
            f"{where_clause}\n"
            f"ORDER BY price DESC\n"
            f"LIMIT  {n};"
        )

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql.rstrip(";"))
            st.dataframe(df, use_container_width=True)
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                f"""
**Key clauses:**
- `ORDER BY price DESC` — sort highest price first
- `LIMIT {n}` — keep only the top {n} rows

`LIMIT` always applies *after* sorting, so you get
the true top {n} — not just the first {n} stored rows.
                """
            )

    # ── Template 4: Books in a price range ───────────────────────────────────
    elif query_choice.startswith("4"):
        st.subheader("🏷️ Books in a Price Range")

        min_p, max_p = st.slider(
            "Price range ($)", min_value=0, max_value=250, value=(20, 100), step=5
        )

        sql = (
            f"SELECT title, author, category, price\n"
            f"FROM   books\n"
            f"WHERE  price BETWEEN {min_p} AND {max_p}\n"
            f"ORDER BY price ASC;"
        )

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql.rstrip(";"))
            st.dataframe(df, use_container_width=True)
            st.caption(f"{len(df)} books priced between ${min_p} and ${max_p}.")
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                f"""
**Key clause:** `BETWEEN {min_p} AND {max_p}`

`BETWEEN` is inclusive on both ends. It is shorthand for:
```sql
WHERE price >= {min_p}
  AND price <= {max_p}
```
Both forms produce identical results.
                """
            )

    # ── Template 5: Students by GPA threshold ────────────────────────────────
    elif query_choice.startswith("5"):
        st.subheader("⭐ Students Above a GPA Threshold")

        threshold = st.slider("Minimum GPA", min_value=2.0, max_value=4.0, value=3.5, step=0.05)
        sort_dir = st.radio("Sort GPA", ["DESC (highest first)", "ASC (lowest first)"])
        order = "DESC" if sort_dir.startswith("DESC") else "ASC"

        sql = (
            f"SELECT name, major, year, gpa\n"
            f"FROM   students\n"
            f"WHERE  gpa >= {threshold}\n"
            f"ORDER BY gpa {order};"
        )

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql.rstrip(";"))
            st.dataframe(df, use_container_width=True)
            st.caption(f"{len(df)} students with GPA ≥ {threshold}.")
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                f"""
**Key clause:** `WHERE gpa >= {threshold}`

Numeric comparisons use `=`, `!=`, `<`, `<=`, `>`, `>=`.
No quotes around numbers — only around string values.

Try lowering the threshold toward 3.0 and watch
how the result set grows.
                """
            )

    # ── Template 6: Purchases in a date range ────────────────────────────────
    elif query_choice.startswith("6"):
        st.subheader("📅 Purchases in a Date Range")

        import datetime
        start = st.date_input("Start date", value=datetime.date(2025, 8, 26))
        end   = st.date_input("End date",   value=datetime.date(2025, 12, 31))

        sql = (
            f"SELECT purchase_id, student_id, book_id,\n"
            f"       purchase_date, quantity, total_amount\n"
            f"FROM   purchases\n"
            f"WHERE  purchase_date BETWEEN '{start}' AND '{end}'\n"
            f"ORDER BY purchase_date ASC;"
        )

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql.rstrip(";"))
            st.dataframe(df, use_container_width=True)
            total = df["total_amount"].sum()
            st.caption(f"{len(df)} purchases · total ${total:,.2f}")
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                f"""
**Key clause:** `BETWEEN '{start}' AND '{end}'`

Date literals are written as strings in `'YYYY-MM-DD'`
format. DuckDB (like most RDBMS engines) compares them
chronologically when the column type is `DATE`.

Try switching the range to Spring 2026
(`2026-01-01` → `2026-06-30`) and compare the totals.
                """
            )

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption("OMIS-105 · Santa Clara University · Leavey School of Business · Level 1 of 3")
