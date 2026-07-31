"""
Streamlit + DuckDB Customer Management Application
===================================================
Demonstrates full CRUD interaction between Streamlit and DuckDB:
  - Create new customers (auto-generated ID and timestamp)
  - View all customers
  - Delete a customer by ID
  - Search customers by email (partial match)

Usage:
    pip install streamlit duckdb
    streamlit run app.py
"""

import streamlit as st
import duckdb
import uuid
from datetime import datetime

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

DB_FILE = "customers.duckdb"


def get_connection() -> duckdb.DuckDBPyConnection:
    """Return a DuckDB connection stored in Streamlit session state so it
    persists across reruns but stays scoped to the session."""
    if "db_conn" not in st.session_state:
        conn = duckdb.connect(DB_FILE)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id   VARCHAR PRIMARY KEY,
                customer_name VARCHAR NOT NULL,
                gender        VARCHAR NOT NULL,
                country       VARCHAR NOT NULL,
                customer_email VARCHAR NOT NULL,
                date_created  TIMESTAMP NOT NULL
            )
        """)
        st.session_state.db_conn = conn
    return st.session_state.db_conn


def insert_customer(name: str, gender: str, country: str, email: str) -> str:
    """Insert a new customer and return the generated customer_id."""
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
    """Return all customers as a list of tuples."""
    conn = get_connection()
    return conn.execute(
        "SELECT * FROM customers ORDER BY date_created DESC"
    ).fetchall()


def delete_customer(customer_id: str) -> int:
    """Delete a customer by ID. Returns the number of rows removed."""
    conn = get_connection()
    before = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    conn.execute("DELETE FROM customers WHERE customer_id = ?", [customer_id])
    after = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    return before - after


def search_customers_by_email(email_fragment: str):
    """Return customers whose email contains the given fragment (case-insensitive)."""
    conn = get_connection()
    return conn.execute(
        """
        SELECT * FROM customers
        WHERE LOWER(customer_email) LIKE LOWER(?)
        ORDER BY date_created DESC
        """,
        [f"%{email_fragment}%"],
    ).fetchall()


def get_customer_count() -> int:
    conn = get_connection()
    return conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]


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
st.caption("Powered by **Streamlit** and **DuckDB**")

# Sidebar — quick stats
with st.sidebar:
    st.header("Database Info")
    st.metric("Total Customers", get_customer_count())
    st.divider()
    st.info(f"DuckDB file: `{DB_FILE}`")

# Tabs for each operation
tab_create, tab_view, tab_search, tab_delete = st.tabs(
    ["➕ Create Customer", "📋 View All", "🔍 Search by Email", "🗑️ Delete Customer"]
)

# ---- TAB 1: Create Customer ------------------------------------------------
with tab_create:
    st.subheader("Create a New Customer")

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
            # Basic validation
            if not name.strip():
                st.error("Customer name is required.")
            elif not email.strip():
                st.error("Email is required.")
            else:
                cid = insert_customer(name.strip(), gender, country, email.strip())
                st.success(f"Customer created successfully!  **ID:** `{cid}`")
                st.balloons()

# ---- TAB 2: View All Customers ---------------------------------------------
with tab_view:
    st.subheader("All Customers")

    rows = fetch_all_customers()
    if rows:
        # Build a simple dataframe-style display
        import pandas as pd

        df = pd.DataFrame(rows, columns=COLUMN_NAMES)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Showing {len(df)} customer(s)")
    else:
        st.info("No customers yet. Head over to the **Create Customer** tab to add one.")

# ---- TAB 3: Search by Email ------------------------------------------------
with tab_search:
    st.subheader("Search Customers by Email")

    email_query = st.text_input(
        "Enter email or part of email",
        placeholder="e.g. @gmail.com",
        key="search_email",
    )

    if email_query.strip():
        results = search_customers_by_email(email_query.strip())
        if results:
            import pandas as pd

            df_search = pd.DataFrame(results, columns=COLUMN_NAMES)
            st.dataframe(df_search, use_container_width=True, hide_index=True)
            st.caption(f"Found {len(df_search)} matching customer(s)")
        else:
            st.warning("No customers found matching that email fragment.")
    else:
        st.caption("Type an email fragment above to search.")

# ---- TAB 4: Delete Customer ------------------------------------------------
with tab_delete:
    st.subheader("Delete a Customer")

    all_customers = fetch_all_customers()
    if all_customers:
        # Build a lookup dict: display string -> customer_id
        options = {
            f"{row[0]}  —  {row[1]}  ({row[4]})": row[0] for row in all_customers
        }

        selected = st.selectbox(
            "Select a customer to delete",
            options.keys(),
            index=None,
            placeholder="Choose a customer…",
        )

        if selected:
            cid_to_delete = options[selected]

            # Show the customer details before confirming
            st.warning(f"You are about to delete customer **{cid_to_delete}** ({selected}).")

            if st.button("Confirm Delete", type="primary"):
                removed = delete_customer(cid_to_delete)
                if removed:
                    st.success(f"Customer `{cid_to_delete}` deleted successfully.")
                    st.rerun()
                else:
                    st.error("Customer not found — they may have already been deleted.")
    else:
        st.info("No customers to delete.")

# Footer
st.divider()
st.caption(
    "Built with [Streamlit](https://streamlit.io) • "
    "Data stored in [DuckDB](https://duckdb.org) • "
    f"Session started at {datetime.now():%Y-%m-%d %H:%M}"
)
