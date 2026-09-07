"""
Streamlit + DuckDB Customer Management Application (Extended)
=============================================================
Full CRUD + sorting/filtering + raw SQL explorer.

Tabs:
  1. Create Customer   — INSERT INTO
  2. View All          — SELECT with ORDER BY / WHERE filters
  3. Search by Email   — SELECT … WHERE LIKE (partial match)
  4. Update Customer   — UPDATE … SET … WHERE
  5. Delete Customer   — DELETE FROM … WHERE
  6. SQL Explorer      — Free-form SQL for learning

Usage:
    pip install streamlit duckdb pandas
    streamlit run app_with_update.py
"""

import streamlit as st
import duckdb
import uuid
import pandas as pd
import re
from datetime import datetime


# ---------------------------------------------------------------------------
# SQL formatter (no external dependency)
# ---------------------------------------------------------------------------

_CLAUSE_KEYWORDS = re.compile(
    r'\b(SELECT|FROM|WHERE|GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|OFFSET'
    r'|LEFT\s+JOIN|RIGHT\s+JOIN|INNER\s+JOIN|FULL\s+JOIN|JOIN'
    r'|UNION\s+ALL|UNION|INTERSECT|EXCEPT|ON|SET|UPDATE|INSERT\s+INTO'
    r'|DELETE\s+FROM|VALUES|DESCRIBE|SHOW)\b',
    re.IGNORECASE,
)

_ALL_KEYWORDS = re.compile(
    r'\b(SELECT|DISTINCT|AS|FROM|WHERE|AND|OR|NOT|IN|EXISTS|BETWEEN|LIKE'
    r'|IS\s+NULL|IS\s+NOT\s+NULL|NULL|TRUE|FALSE|CASE|WHEN|THEN|ELSE|END'
    r'|GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|OFFSET|ASC|DESC|ON|SET|UPDATE'
    r'|INSERT\s+INTO|DELETE\s+FROM|VALUES|INTO|JOIN|LEFT|RIGHT|INNER|FULL'
    r'|OUTER|CROSS|UNION|ALL|INTERSECT|EXCEPT|WITH|CREATE|TABLE|DROP'
    r'|ALTER|INDEX|VIEW|IF|EXISTS|COUNT|SUM|AVG|MIN|MAX|CAST|COALESCE'
    r'|LOWER|UPPER|TRIM|LENGTH|SUBSTRING|REPLACE|NOW|DATE|DESCRIBE|SHOW)\b',
    re.IGNORECASE,
)


def format_sql(sql: str) -> str:
    """Uppercase keywords and add a newline+indent before each major clause."""
    # Uppercase all SQL keywords
    def _upper(m):
        return re.sub(r'\s+', ' ', m.group(0).upper())
    sql = _ALL_KEYWORDS.sub(_upper, sql)

    # Newline before each clause keyword
    sql = _CLAUSE_KEYWORDS.sub(lambda m: '\n' + re.sub(r'\s+', ' ', m.group(0).upper()), sql)

    # Clean up: strip leading/trailing whitespace per line, collapse blank lines
    lines = [ln.rstrip() for ln in sql.splitlines()]
    lines = [ln for ln in lines if ln.strip()]

    # Indent lines that are not clause starters
    formatted = []
    for line in lines:
        stripped = line.lstrip()
        if _CLAUSE_KEYWORDS.match(stripped):
            formatted.append(stripped)
        else:
            formatted.append('    ' + stripped)

    return '\n'.join(formatted).strip()

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

DB_FILE = "customers.duckdb"


def get_connection() -> duckdb.DuckDBPyConnection:
    """Return a DuckDB connection stored in Streamlit session state."""
    if "db_conn" not in st.session_state:
        conn = duckdb.connect(DB_FILE)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id    VARCHAR PRIMARY KEY,
                customer_name  VARCHAR NOT NULL,
                gender         VARCHAR NOT NULL,
                country        VARCHAR NOT NULL,
                customer_email VARCHAR NOT NULL,
                date_created   TIMESTAMP NOT NULL
            )
        """)
        st.session_state.db_conn = conn
    return st.session_state.db_conn


def insert_customer(name: str, gender: str, country: str, email: str) -> str:
    conn = get_connection()
    customer_id = str(uuid.uuid4())[:8].upper()
    now = datetime.now()
    conn.execute(
        """
        INSERT INTO customers
            (customer_id, customer_name, gender, country, customer_email, date_created)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [customer_id, name, gender, country, email, now],
    )
    return customer_id


def fetch_all_customers():
    conn = get_connection()
    return conn.execute(
        "SELECT * FROM customers ORDER BY date_created DESC"
    ).fetchall()


def fetch_customers_sorted_filtered(
    sort_col: str, sort_dir: str,
    filter_gender: str | None, filter_country: str | None
):
    """Fetch customers with optional ORDER BY and WHERE filters."""
    conn = get_connection()

    col_map = {
        "Customer ID": "customer_id",
        "Name": "customer_name",
        "Gender": "gender",
        "Country": "country",
        "Email": "customer_email",
        "Date Created": "date_created",
    }
    db_col = col_map.get(sort_col, "date_created")

    conditions = []
    params = []
    if filter_gender and filter_gender != "All":
        conditions.append("gender = ?")
        params.append(filter_gender)
    if filter_country and filter_country != "All":
        conditions.append("country = ?")
        params.append(filter_country)

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    sql = f"""
        SELECT * FROM customers
        {where_clause}
        ORDER BY {db_col} {sort_dir}
    """
    return conn.execute(sql, params).fetchall()


def search_customers_by_email(email_fragment: str):
    conn = get_connection()
    return conn.execute(
        """
        SELECT * FROM customers
        WHERE LOWER(customer_email) LIKE LOWER(?)
        ORDER BY date_created DESC
        """,
        [f"%{email_fragment}%"],
    ).fetchall()


def update_customer(customer_id: str, name: str, gender: str, country: str, email: str):
    """Update a customer's fields (except ID and date_created)."""
    conn = get_connection()
    conn.execute(
        """
        UPDATE customers
        SET customer_name  = ?,
            gender         = ?,
            country        = ?,
            customer_email = ?
        WHERE customer_id  = ?
        """,
        [name, gender, country, email, customer_id],
    )


def delete_customer(customer_id: str) -> int:
    conn = get_connection()
    before = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    conn.execute("DELETE FROM customers WHERE customer_id = ?", [customer_id])
    after = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    return before - after


def get_customer_count() -> int:
    conn = get_connection()
    return conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]


def run_sql(sql: str):
    """Execute arbitrary SQL. Returns (columns, rows) for SELECT or row count for DML."""
    conn = get_connection()
    result = conn.execute(sql)
    # If the statement returns rows, fetch them
    try:
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        return columns, rows
    except Exception:
        return None, None


# ---------------------------------------------------------------------------
# UI Constants
# ---------------------------------------------------------------------------

COLUMN_NAMES = [
    "Customer ID",
    "Name",
    "Gender",
    "Country",
    "Email",
    "Date Created",
]

GENDERS = ["MALE", "FEMALE"]
COUNTRIES = ["USA", "CANADA", "MEXICO", "GERMANY"]

# ---------------------------------------------------------------------------
# Streamlit App
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Customer Manager", page_icon="🗃️", layout="wide")

st.title("🗃️ Customer Management System")
st.caption("Powered by **Streamlit** and **DuckDB** — Full CRUD + SQL Explorer")

# Sidebar — quick stats
with st.sidebar:
    st.header("Database Info")
    st.metric("Total Customers", get_customer_count())
    st.divider()
    st.subheader("SQL Cheat Sheet")
    st.code("SELECT * FROM customers;", language="sql")
    st.code("SELECT * FROM customers\nWHERE country = 'USA';", language="sql")
    st.code("SELECT gender, COUNT(*)\nFROM customers\nGROUP BY gender;", language="sql")
    st.code("SELECT country, COUNT(*) AS cnt\nFROM customers\nGROUP BY country\nORDER BY cnt DESC;", language="sql")
    st.divider()
    st.info(f"DuckDB file: `{DB_FILE}`")

# Tabs for each operation
tab_create, tab_view, tab_search, tab_update, tab_delete, tab_sql = st.tabs([
    "➕ Create",
    "📋 View All",
    "🔍 Search",
    "✏️ Update",
    "🗑️ Delete",
    "🧪 SQL Explorer",
])

# ---- TAB 1: Create Customer ------------------------------------------------
with tab_create:
    st.subheader("Create a New Customer")
    st.info("**SQL equivalent:** `INSERT INTO customers (...) VALUES (...)`")

    with st.form("create_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Customer Name *", placeholder="e.g. Jane Doe")
            gender = st.selectbox("Gender *", GENDERS)
        with col2:
            email = st.text_input("Email *", placeholder="e.g. jane@example.com")
            country = st.selectbox("Country *", COUNTRIES)

        submitted = st.form_submit_button("Create Customer", type="primary")

        if submitted:
            if not name.strip():
                st.error("Customer name is required.")
            elif not email.strip():
                st.error("Email is required.")
            else:
                cid = insert_customer(name.strip(), gender, country, email.strip())
                st.success(f"Customer created!  **ID:** `{cid}`")
                st.balloons()

# ---- TAB 2: View All Customers (with sorting & filtering) ------------------
with tab_view:
    st.subheader("All Customers")
    st.info("**SQL equivalent:** `SELECT * FROM customers [WHERE ...] ORDER BY ...`")

    # --- Filter & sort controls ---
    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns(4)
    with ctrl_col1:
        sort_column = st.selectbox("Sort by", COLUMN_NAMES, index=5, key="view_sort_col")
    with ctrl_col2:
        sort_direction = st.radio(
            "Direction", ["ASC", "DESC"], index=1, horizontal=True, key="view_sort_dir"
        )
    with ctrl_col3:
        filter_gender = st.selectbox("Filter Gender", ["All"] + GENDERS, key="view_fg")
    with ctrl_col4:
        filter_country = st.selectbox("Filter Country", ["All"] + COUNTRIES, key="view_fc")

    rows = fetch_customers_sorted_filtered(sort_column, sort_direction, filter_gender, filter_country)
    if rows:
        df = pd.DataFrame(rows, columns=COLUMN_NAMES)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Showing {len(df)} customer(s)")

        # Show the generated SQL for educational purposes
        with st.expander("Show generated SQL"):
            parts = ["SELECT * FROM customers"]
            wheres = []
            if filter_gender != "All":
                wheres.append(f"gender = '{filter_gender}'")
            if filter_country != "All":
                wheres.append(f"country = '{filter_country}'")
            if wheres:
                parts.append("WHERE " + " AND ".join(wheres))
            col_map = {
                "Customer ID": "customer_id", "Name": "customer_name",
                "Gender": "gender", "Country": "country",
                "Email": "customer_email", "Date Created": "date_created",
            }
            parts.append(f"ORDER BY {col_map.get(sort_column, 'date_created')} {sort_direction}")
            st.code("\n".join(parts) + ";", language="sql")
    else:
        st.info("No customers match the current filters.")

# ---- TAB 3: Search by Email ------------------------------------------------
with tab_search:
    st.subheader("Search Customers by Email")
    st.info("**SQL equivalent:** `SELECT * FROM customers WHERE LOWER(customer_email) LIKE LOWER('%...%')`")

    email_query = st.text_input(
        "Enter email or part of email",
        placeholder="e.g. @gmail.com",
        key="search_email",
    )

    if email_query.strip():
        results = search_customers_by_email(email_query.strip())
        if results:
            df_search = pd.DataFrame(results, columns=COLUMN_NAMES)
            st.dataframe(df_search, use_container_width=True, hide_index=True)
            st.caption(f"Found {len(df_search)} matching customer(s)")
        else:
            st.warning("No customers found matching that email fragment.")
    else:
        st.caption("Type an email fragment above to search.")

# ---- TAB 4: Update Customer ------------------------------------------------
with tab_update:
    st.subheader("Update an Existing Customer")
    st.info("**SQL equivalent:** `UPDATE customers SET ... WHERE customer_id = '...'`")

    all_customers = fetch_all_customers()
    if all_customers:
        # Build lookup: display label -> full row
        customer_lookup = {
            f"{row[0]}  —  {row[1]}  ({row[4]})": row for row in all_customers
        }

        selected_label = st.selectbox(
            "Select a customer to update",
            customer_lookup.keys(),
            index=None,
            placeholder="Choose a customer…",
            key="update_select",
        )

        if selected_label:
            row = customer_lookup[selected_label]
            cid, cur_name, cur_gender, cur_country, cur_email, cur_date = row

            st.divider()
            st.caption(f"Editing customer **{cid}** (created {cur_date})")

            with st.form("update_form"):
                ucol1, ucol2 = st.columns(2)
                with ucol1:
                    new_name = st.text_input("Customer Name", value=cur_name)
                    new_gender = st.selectbox(
                        "Gender", GENDERS,
                        index=GENDERS.index(cur_gender) if cur_gender in GENDERS else 0,
                    )
                with ucol2:
                    new_email = st.text_input("Email", value=cur_email)
                    new_country = st.selectbox(
                        "Country", COUNTRIES,
                        index=COUNTRIES.index(cur_country) if cur_country in COUNTRIES else 0,
                    )

                update_submitted = st.form_submit_button("Save Changes", type="primary")

                if update_submitted:
                    if not new_name.strip():
                        st.error("Customer name cannot be empty.")
                    elif not new_email.strip():
                        st.error("Email cannot be empty.")
                    else:
                        update_customer(cid, new_name.strip(), new_gender, new_country, new_email.strip())
                        st.success(f"Customer `{cid}` updated successfully!")

                        # Show the SQL that ran
                        with st.expander("Show generated SQL"):
                            st.code(
                                f"UPDATE customers\n"
                                f"SET customer_name  = '{new_name.strip()}',\n"
                                f"    gender         = '{new_gender}',\n"
                                f"    country        = '{new_country}',\n"
                                f"    customer_email = '{new_email.strip()}'\n"
                                f"WHERE customer_id  = '{cid}';",
                                language="sql",
                            )
    else:
        st.info("No customers yet. Create one first!")

# ---- TAB 5: Delete Customer ------------------------------------------------
with tab_delete:
    st.subheader("Delete a Customer")
    st.info("**SQL equivalent:** `DELETE FROM customers WHERE customer_id = '...'`")

    all_for_delete = fetch_all_customers()
    if all_for_delete:
        options = {
            f"{row[0]}  —  {row[1]}  ({row[4]})": row[0] for row in all_for_delete
        }

        selected = st.selectbox(
            "Select a customer to delete",
            options.keys(),
            index=None,
            placeholder="Choose a customer…",
            key="delete_select",
        )

        if selected:
            cid_to_delete = options[selected]
            st.warning(f"You are about to delete customer **{cid_to_delete}**.")

            if st.button("Confirm Delete", type="primary"):
                removed = delete_customer(cid_to_delete)
                if removed:
                    st.success(f"Customer `{cid_to_delete}` deleted.")
                    st.rerun()
                else:
                    st.error("Customer not found — may have been already deleted.")
    else:
        st.info("No customers to delete.")

# ---- TAB 6: SQL Explorer ---------------------------------------------------
with tab_sql:
    st.subheader("SQL Explorer")
    st.info(
        "Type any SQL query below and run it against the DuckDB database. "
        "Great for practicing SELECT, aggregate functions, JOINs, and more!"
    )

    # Pre-loaded example queries students can try
    example_queries = {
        "(custom)": "",
        "Select all customers": "SELECT * FROM customers;",
        "Count by gender": "SELECT gender, COUNT(*) AS total\nFROM customers\nGROUP BY gender;",
        "Count by country": "SELECT country, COUNT(*) AS total\nFROM customers\nGROUP BY country\nORDER BY total DESC;",
        "Customers created today": f"SELECT * FROM customers\nWHERE CAST(date_created AS DATE) = '{datetime.now():%Y-%m-%d}';",
        "Distinct countries": "SELECT DISTINCT country FROM customers ORDER BY country;",
        "Latest 5 customers": "SELECT * FROM customers\nORDER BY date_created DESC\nLIMIT 5;",
        "Describe table": "DESCRIBE customers;",
    }

    # Apply deferred format (must happen BEFORE the text_area widget is instantiated)
    if st.session_state.pop("_do_format", False):
        st.session_state["sql_input"] = format_sql(st.session_state.get("sql_input", ""))

    def _load_example():
        raw = example_queries[st.session_state["sql_example"]]
        st.session_state["sql_input"] = format_sql(raw) if raw else ""

    chosen_example = st.selectbox(
        "Quick examples", example_queries.keys(), key="sql_example", on_change=_load_example
    )

    default_sql = format_sql(example_queries[chosen_example]) if example_queries[chosen_example] else ""
    # Split into two columns: editor on left, highlighted preview on right
    edit_col, preview_col = st.columns(2)

    with edit_col:
        st.markdown("**✏️ Editor**")
        sql_input = st.text_area(
            "Enter your SQL",
            value=default_sql,
            height=220,
            placeholder="SELECT * FROM customers WHERE country = 'USA';",
            key="sql_input",
            label_visibility="collapsed",
        )
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            if st.button("▶ Run Query", type="primary", key="run_sql"):
                pass  # handled below
        with btn_col2:
            if st.button("✨ Format SQL", key="fmt_sql"):
                st.session_state["_do_format"] = True
                st.rerun()

    with preview_col:
        st.markdown("**🎨 Highlighted Preview**")
        if sql_input.strip():
            st.code(sql_input, language="sql")
        else:
            st.caption("Start typing SQL on the left to see a highlighted preview here.")

    if st.session_state.get("run_sql"):
        if not sql_input.strip():
            st.error("Please enter a SQL statement.")
        else:
            try:
                columns, rows = run_sql(sql_input.strip())
                if columns is not None:
                    df_sql = pd.DataFrame(rows, columns=columns)
                    st.dataframe(df_sql, use_container_width=True, hide_index=True)
                    st.caption(f"Returned {len(df_sql)} row(s)")
                else:
                    st.success("Statement executed successfully (no rows returned).")
            except Exception as e:
                st.error(f"SQL Error: {e}")

# Footer
st.divider()
st.caption(
    "Built with [Streamlit](https://streamlit.io) • "
    "Data stored in [DuckDB](https://duckdb.org) • "
    f"Session started at {datetime.now():%Y-%m-%d %H:%M}"
)
