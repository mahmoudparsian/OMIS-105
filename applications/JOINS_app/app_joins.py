"""
Streamlit + DuckDB — SQL Joins Explorer
========================================
A teaching app dedicated to INNER, LEFT, RIGHT, and FULL OUTER JOINs.

Two tables:
  - employees (left table)  : emp_id, emp_name, dept_id
  - projects  (right table) : project_id, project_name, dept_id

Pre-seeded so that dept_id = 10 has 2 employees and 3 projects,
producing 2 × 3 = 6 rows on an INNER JOIN — a vivid demonstration
of the Cartesian-product behavior of joins on duplicate keys.

Usage:
    pip install streamlit duckdb pandas
    streamlit run app_joins.py
"""

import streamlit as st
import duckdb
import pandas as pd

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

DB_FILE = "joins_demo.duckdb"


def get_connection() -> duckdb.DuckDBPyConnection:
    if "db_conn" not in st.session_state:
        conn = duckdb.connect(DB_FILE)
        _init_tables(conn)
        st.session_state.db_conn = conn
    return st.session_state.db_conn


def _init_tables(conn: duckdb.DuckDBPyConnection):
    """Create and seed tables if they don't exist yet."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id    VARCHAR PRIMARY KEY,
            emp_name  VARCHAR NOT NULL,
            dept_id   INTEGER NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id   VARCHAR PRIMARY KEY,
            project_name VARCHAR NOT NULL,
            dept_id      INTEGER NOT NULL
        )
    """)

    # Seed only if tables are empty (first run)
    emp_count = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    if emp_count == 0:
        conn.executemany(
            "INSERT INTO employees VALUES (?, ?, ?)",
            [
                # dept_id 10: TWO employees  (the "1, 1" on the left)
                ("E1", "Alice",   10),
                ("E2", "Bob",     10),
                # dept_id 20: one employee
                ("E3", "Charlie", 20),
                # dept_id 30: one employee — NO matching projects (LEFT-only)
                ("E4", "Diana",   30),
            ],
        )

    prj_count = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    if prj_count == 0:
        conn.executemany(
            "INSERT INTO projects VALUES (?, ?, ?)",
            [
                # dept_id 10: THREE projects (the "1, 1, 1" on the right)
                ("P1", "Alpha",   10),
                ("P2", "Beta",    10),
                ("P3", "Gamma",   10),
                # dept_id 20: one project
                ("P4", "Delta",   20),
                # dept_id 40: one project — NO matching employees (RIGHT-only)
                ("P5", "Epsilon", 40),
            ],
        )


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def fetch_employees():
    conn = get_connection()
    return conn.execute("SELECT * FROM employees ORDER BY emp_id").fetchdf()


def fetch_projects():
    conn = get_connection()
    return conn.execute("SELECT * FROM projects ORDER BY project_id").fetchdf()


def run_join(join_type: str) -> pd.DataFrame:
    """Run a join and return the result as a DataFrame."""
    conn = get_connection()
    sql = f"""
        SELECT
            e.emp_id,
            e.emp_name,
            e.dept_id  AS emp_dept_id,
            p.project_id,
            p.project_name,
            p.dept_id  AS prj_dept_id
        FROM employees e
        {join_type} JOIN projects p
            ON e.dept_id = p.dept_id
        ORDER BY
            COALESCE(e.dept_id, p.dept_id),
            e.emp_id,
            p.project_id
    """
    return conn.execute(sql).fetchdf()


def get_join_sql(join_type: str) -> str:
    """Return the SQL string for display."""
    return (
        f"SELECT\n"
        f"    e.emp_id,\n"
        f"    e.emp_name,\n"
        f"    e.dept_id  AS emp_dept_id,\n"
        f"    p.project_id,\n"
        f"    p.project_name,\n"
        f"    p.dept_id  AS prj_dept_id\n"
        f"FROM employees e\n"
        f"{join_type} JOIN projects p\n"
        f"    ON e.dept_id = p.dept_id\n"
        f"ORDER BY\n"
        f"    COALESCE(e.dept_id, p.dept_id),\n"
        f"    e.emp_id, p.project_id;"
    )


def add_employee(emp_id: str, emp_name: str, dept_id: int):
    conn = get_connection()
    conn.execute("INSERT INTO employees VALUES (?, ?, ?)", [emp_id, emp_name, dept_id])


def delete_employee(emp_id: str):
    conn = get_connection()
    conn.execute("DELETE FROM employees WHERE emp_id = ?", [emp_id])


def add_project(project_id: str, project_name: str, dept_id: int):
    conn = get_connection()
    conn.execute("INSERT INTO projects VALUES (?, ?, ?)", [project_id, project_name, dept_id])


def delete_project(project_id: str):
    conn = get_connection()
    conn.execute("DELETE FROM projects WHERE project_id = ?", [project_id])


def reset_tables():
    """Drop and re-create both tables with original seed data."""
    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS employees")
    conn.execute("DROP TABLE IF EXISTS projects")
    _init_tables(conn)


# ---------------------------------------------------------------------------
# Row-count multiplier explanation
# ---------------------------------------------------------------------------

def build_multiplier_table(join_type: str, df_left: pd.DataFrame, df_right: pd.DataFrame):
    """
    For each dept_id, show:
      Left count × Right count = Expected rows in join result.
    This makes the Cartesian-product behavior crystal clear.
    """
    left_counts = df_left.groupby("dept_id").size().reset_index(name="left_count")
    right_counts = df_right.groupby("dept_id").size().reset_index(name="right_count")

    # All dept_ids that appear in either table
    all_depts = pd.DataFrame(
        {"dept_id": sorted(set(left_counts["dept_id"]) | set(right_counts["dept_id"]))}
    )
    merged = all_depts.merge(left_counts, on="dept_id", how="left").merge(
        right_counts, on="dept_id", how="left"
    )
    merged["left_count"] = merged["left_count"].fillna(0).astype(int)
    merged["right_count"] = merged["right_count"].fillna(0).astype(int)

    jt = join_type.upper()
    rows = []
    for _, r in merged.iterrows():
        lc = r["left_count"]
        rc = r["right_count"]
        dept = int(r["dept_id"])

        if jt == "INNER":
            produced = lc * rc
        elif jt == "LEFT":
            produced = lc * rc if rc > 0 else lc  # unmatched left rows appear once with NULLs
        elif jt == "RIGHT":
            produced = lc * rc if lc > 0 else rc  # unmatched right rows appear once with NULLs
        else:  # FULL OUTER
            if lc > 0 and rc > 0:
                produced = lc * rc
            elif lc > 0:
                produced = lc
            else:
                produced = rc

        if jt == "INNER":
            explanation = f"{lc} × {rc} = {produced}"
        elif jt == "LEFT":
            if rc > 0:
                explanation = f"{lc} × {rc} = {produced}"
            else:
                explanation = f"{lc} left row(s), 0 right → {produced} row(s) with NULLs on right"
        elif jt == "RIGHT":
            if lc > 0:
                explanation = f"{lc} × {rc} = {produced}"
            else:
                explanation = f"0 left, {rc} right row(s) → {produced} row(s) with NULLs on left"
        else:
            if lc > 0 and rc > 0:
                explanation = f"{lc} × {rc} = {produced}"
            elif lc > 0:
                explanation = f"{lc} left row(s), 0 right → {produced} row(s) with NULLs on right"
            else:
                explanation = f"0 left, {rc} right row(s) → {produced} row(s) with NULLs on left"

        rows.append({
            "dept_id": dept,
            "Left Count": int(lc),
            "Right Count": int(rc),
            "Rows Produced": int(produced),
            "Explanation": explanation,
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Venn diagram (pure SVG)
# ---------------------------------------------------------------------------

def venn_svg(join_type: str) -> str:
    """Return an SVG Venn diagram highlighting the relevant region.

    The diagram uses three independently-colored regions:
      - left-only  (left circle minus overlap)
      - right-only (right circle minus overlap)
      - overlap    (intersection of both circles)

    Each join type turns regions on (green) or off (grey).
    """
    jt = join_type.upper()

    GREEN = "#4CAF50"
    DARK_GREEN = "#388E3C"
    GREY = "#E0E0E0"
    STROKE = "#333333"

    # Decide which regions are "on"
    if jt == "INNER":
        left_only_fill = GREY
        right_only_fill = GREY
        overlap_fill = GREEN
        desc = "Only matching rows from BOTH tables"
    elif jt == "LEFT":
        left_only_fill = GREEN
        right_only_fill = GREY
        overlap_fill = DARK_GREEN
        desc = "ALL rows from LEFT table + matching rows from right"
    elif jt == "RIGHT":
        left_only_fill = GREY
        right_only_fill = GREEN
        overlap_fill = DARK_GREEN
        desc = "ALL rows from RIGHT table + matching rows from left"
    else:  # FULL OUTER
        left_only_fill = GREEN
        right_only_fill = GREEN
        overlap_fill = DARK_GREEN
        desc = "ALL rows from BOTH tables"

    # Use unique clip-path IDs per join type to avoid SVG ID collisions
    # when multiple Venn diagrams are on the same page.
    tag = jt.replace(" ", "").lower()

    svg = f"""
    <svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" style="max-width:400px;">
      <defs>
        <clipPath id="clip-left-{tag}">
          <circle cx="130" cy="100" r="75"/>
        </clipPath>
        <clipPath id="clip-right-{tag}">
          <circle cx="230" cy="100" r="75"/>
        </clipPath>
      </defs>

      <!-- 1. Draw both full circles in their "only" color -->
      <circle cx="130" cy="100" r="75" fill="{left_only_fill}" stroke="none" opacity="0.8"/>
      <circle cx="230" cy="100" r="75" fill="{right_only_fill}" stroke="none" opacity="0.8"/>

      <!-- 2. Paint the overlap region (left circle clipped to right area) -->
      <g clip-path="url(#clip-right-{tag})">
        <circle cx="130" cy="100" r="75" fill="{overlap_fill}" opacity="0.9"/>
      </g>

      <!-- 3. Strokes on top so they are always clean -->
      <circle cx="130" cy="100" r="75" fill="none" stroke="{STROKE}" stroke-width="2"/>
      <circle cx="230" cy="100" r="75" fill="none" stroke="{STROKE}" stroke-width="2"/>

      <!-- Labels -->
      <text x="95" y="100" text-anchor="middle" font-size="14" font-weight="bold"
            fill="#333" font-family="sans-serif">Left</text>
      <text x="95" y="118" text-anchor="middle" font-size="11"
            fill="#555" font-family="sans-serif">(employees)</text>
      <text x="265" y="100" text-anchor="middle" font-size="14" font-weight="bold"
            fill="#333" font-family="sans-serif">Right</text>
      <text x="265" y="118" text-anchor="middle" font-size="11"
            fill="#555" font-family="sans-serif">(projects)</text>

      <!-- Description -->
      <text x="180" y="192" text-anchor="middle" font-size="12"
            fill="#333" font-family="sans-serif">{desc}</text>
    </svg>
    """
    return svg


# ---------------------------------------------------------------------------
# Reusable: render a join tab
# ---------------------------------------------------------------------------

def render_join_tab(join_type: str, join_label: str):
    """Render the full UI for one join type."""
    st.subheader(f"{join_label}")

    # Venn diagram
    st.markdown(venn_svg(join_type), unsafe_allow_html=True)
    st.write("")

    # Three-column layout: Left | Right | Result
    col_left, col_right = st.columns(2)

    df_emp = fetch_employees()
    df_prj = fetch_projects()

    with col_left:
        st.markdown("##### Left Table: `employees`")
        st.dataframe(df_emp, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_emp)} row(s)")

    with col_right:
        st.markdown("##### Right Table: `projects`")
        st.dataframe(df_prj, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_prj)} row(s)")

    st.divider()

    # The SQL
    st.markdown("##### SQL Query")
    st.code(get_join_sql(join_type), language="sql")

    # The join result
    st.markdown("##### Join Result")
    df_result = run_join(join_type)
    if len(df_result) > 0:
        # Add a 1-based row number as the first column
        df_result.insert(0, "Row #", range(1, len(df_result) + 1))

        # Convert all columns to object (string) dtype so we can safely
        # replace NaN/None with the literal text "NULL" for display.
        df_display = df_result.astype(object).fillna("NULL")

        # Highlight NULL cells: bright yellow background with bold dark text
        def highlight_nulls(val):
            if val == "NULL":
                return "background-color: #FFF9C4; color: #F57F17; font-weight: bold;"
            return ""

        styled = df_display.style.applymap(highlight_nulls)
        st.dataframe(styled, use_container_width=True, hide_index=True)
        st.caption(f"**{len(df_result)} row(s)** produced by {join_label}")
    else:
        st.info("Join produced 0 rows.")

    # Row-count multiplier breakdown
    st.markdown("##### Row-Count Breakdown (why this many rows?)")
    mult_df = build_multiplier_table(join_type, df_emp, df_prj)
    st.dataframe(mult_df, use_container_width=True, hide_index=True)

    total = mult_df["Rows Produced"].sum()
    st.success(f"**Total rows = {total}**  (sum of all dept_id contributions)")


# ---------------------------------------------------------------------------
# Streamlit App
# ---------------------------------------------------------------------------

st.set_page_config(page_title="SQL Joins Explorer", page_icon="🔗", layout="wide")

st.title("🔗 SQL Joins Explorer")
st.caption(
    "Powered by **Streamlit** and **DuckDB** — "
    "See exactly how INNER, LEFT, RIGHT, and FULL OUTER JOINs work"
)

# Sidebar
with st.sidebar:
    st.header("About This App")
    st.markdown(
        "Two tables are joined on **`dept_id`**:\n\n"
        "- **employees** (left table)\n"
        "- **projects** (right table)\n\n"
        "The seed data is designed so that "
        "`dept_id = 10` has **2 employees** and **3 projects**, "
        "producing **2 × 3 = 6 rows** in an INNER JOIN."
    )
    st.divider()

    st.subheader("Quick Reference")
    st.markdown(
        "| Join | Keeps |\n"
        "|------|-------|\n"
        "| INNER | Only matching rows |\n"
        "| LEFT | All left + matches |\n"
        "| RIGHT | All right + matches |\n"
        "| FULL OUTER | Everything |\n"
    )
    st.divider()

    st.subheader("Key Insight")
    st.info(
        "When a join key appears **M** times in the left table "
        "and **N** times in the right table, the join produces "
        "**M × N** rows for that key."
    )
    st.divider()

    if st.button("Reset Tables to Original Data", type="secondary"):
        reset_tables()
        st.success("Tables reset!")
        st.rerun()

    st.divider()
    st.caption(f"DuckDB file: `{DB_FILE}`")


# Main tabs
tab_data, tab_inner, tab_left, tab_right, tab_full, tab_sql = st.tabs([
    "📊 Manage Data",
    "⚡ INNER JOIN",
    "⬅️ LEFT JOIN",
    "➡️ RIGHT JOIN",
    "↔️ FULL OUTER JOIN",
    "🧪 SQL Explorer",
])

# ---- TAB: Manage Data -------------------------------------------------------
with tab_data:
    st.subheader("Manage the Left and Right Tables")
    st.markdown(
        "Add or remove rows to see how the join results change. "
        "Try adding more employees or projects with `dept_id = 10` to watch the "
        "Cartesian product grow!"
    )

    data_col1, data_col2 = st.columns(2)

    # --- Left table: employees ---
    with data_col1:
        st.markdown("##### Left Table: `employees`")
        df_emp = fetch_employees()
        st.dataframe(df_emp, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_emp)} row(s)")

        with st.expander("Add an Employee"):
            with st.form("add_emp", clear_on_submit=True):
                ae_col1, ae_col2, ae_col3 = st.columns(3)
                with ae_col1:
                    new_emp_id = st.text_input("emp_id", placeholder="E5")
                with ae_col2:
                    new_emp_name = st.text_input("emp_name", placeholder="Eve")
                with ae_col3:
                    new_emp_dept = st.number_input("dept_id", min_value=1, value=10, step=1)
                if st.form_submit_button("Add Employee", type="primary"):
                    if not new_emp_id.strip() or not new_emp_name.strip():
                        st.error("emp_id and emp_name are required.")
                    else:
                        try:
                            add_employee(new_emp_id.strip(), new_emp_name.strip(), int(new_emp_dept))
                            st.success(f"Added employee `{new_emp_id.strip()}`")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

        with st.expander("Delete an Employee"):
            if len(df_emp) > 0:
                emp_to_delete = st.selectbox(
                    "Select employee",
                    df_emp.apply(
                        lambda r: f"{r['emp_id']}  —  {r['emp_name']}  (dept {r['dept_id']})",
                        axis=1,
                    ).tolist(),
                    index=None,
                    placeholder="Choose…",
                    key="del_emp_select",
                )
                if emp_to_delete and st.button("Delete", key="del_emp_btn"):
                    eid = emp_to_delete.split("  —")[0].strip()
                    delete_employee(eid)
                    st.success(f"Deleted `{eid}`")
                    st.rerun()
            else:
                st.info("No employees to delete.")

    # --- Right table: projects ---
    with data_col2:
        st.markdown("##### Right Table: `projects`")
        df_prj = fetch_projects()
        st.dataframe(df_prj, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_prj)} row(s)")

        with st.expander("Add a Project"):
            with st.form("add_prj", clear_on_submit=True):
                ap_col1, ap_col2, ap_col3 = st.columns(3)
                with ap_col1:
                    new_prj_id = st.text_input("project_id", placeholder="P6")
                with ap_col2:
                    new_prj_name = st.text_input("project_name", placeholder="Zeta")
                with ap_col3:
                    new_prj_dept = st.number_input("dept_id", min_value=1, value=10, step=1, key="prj_dept")
                if st.form_submit_button("Add Project", type="primary"):
                    if not new_prj_id.strip() or not new_prj_name.strip():
                        st.error("project_id and project_name are required.")
                    else:
                        try:
                            add_project(new_prj_id.strip(), new_prj_name.strip(), int(new_prj_dept))
                            st.success(f"Added project `{new_prj_id.strip()}`")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

        with st.expander("Delete a Project"):
            if len(df_prj) > 0:
                prj_to_delete = st.selectbox(
                    "Select project",
                    df_prj.apply(
                        lambda r: f"{r['project_id']}  —  {r['project_name']}  (dept {r['dept_id']})",
                        axis=1,
                    ).tolist(),
                    index=None,
                    placeholder="Choose…",
                    key="del_prj_select",
                )
                if prj_to_delete and st.button("Delete", key="del_prj_btn"):
                    pid = prj_to_delete.split("  —")[0].strip()
                    delete_project(pid)
                    st.success(f"Deleted `{pid}`")
                    st.rerun()
            else:
                st.info("No projects to delete.")

    # Summary of dept_id distribution
    st.divider()
    st.markdown("##### dept_id Distribution (key used for joining)")
    dist_col1, dist_col2 = st.columns(2)
    with dist_col1:
        emp_dist = df_emp.groupby("dept_id").size().reset_index(name="employee_count")
        st.dataframe(emp_dist, use_container_width=True, hide_index=True)
    with dist_col2:
        prj_dist = df_prj.groupby("dept_id").size().reset_index(name="project_count")
        st.dataframe(prj_dist, use_container_width=True, hide_index=True)

# ---- TAB: INNER JOIN --------------------------------------------------------
with tab_inner:
    render_join_tab("INNER", "INNER JOIN")

# ---- TAB: LEFT JOIN ---------------------------------------------------------
with tab_left:
    render_join_tab("LEFT", "LEFT JOIN")

# ---- TAB: RIGHT JOIN --------------------------------------------------------
with tab_right:
    render_join_tab("RIGHT", "RIGHT JOIN")

# ---- TAB: FULL OUTER JOIN ---------------------------------------------------
with tab_full:
    render_join_tab("FULL OUTER", "FULL OUTER JOIN")

# ---- TAB: SQL Explorer ------------------------------------------------------
with tab_sql:
    st.subheader("SQL Explorer")
    st.info(
        "Write any SQL against the `employees` and `projects` tables. "
        "Try your own JOIN variations, subqueries, or aggregations!"
    )

    example_queries = {
        "(custom)": "",
        "INNER JOIN": get_join_sql("INNER"),
        "LEFT JOIN": get_join_sql("LEFT"),
        "RIGHT JOIN": get_join_sql("RIGHT"),
        "FULL OUTER JOIN": get_join_sql("FULL OUTER"),
        "CROSS JOIN (Cartesian product)":
            "SELECT\n"
            "    e.emp_id, e.emp_name,\n"
            "    p.project_id, p.project_name\n"
            "FROM employees e\n"
            "CROSS JOIN projects p\n"
            "ORDER BY e.emp_id, p.project_id;",
        "Count per dept_id (employees)":
            "SELECT dept_id, COUNT(*) AS emp_count\n"
            "FROM employees\n"
            "GROUP BY dept_id\n"
            "ORDER BY dept_id;",
        "Count per dept_id (projects)":
            "SELECT dept_id, COUNT(*) AS prj_count\n"
            "FROM projects\n"
            "GROUP BY dept_id\n"
            "ORDER BY dept_id;",
        "Join multiplier per dept_id":
            "SELECT\n"
            "    COALESCE(e.dept_id, p.dept_id) AS dept_id,\n"
            "    COUNT(DISTINCT e.emp_id) AS emp_count,\n"
            "    COUNT(DISTINCT p.project_id) AS prj_count,\n"
            "    COUNT(*) AS join_rows\n"
            "FROM employees e\n"
            "INNER JOIN projects p ON e.dept_id = p.dept_id\n"
            "GROUP BY COALESCE(e.dept_id, p.dept_id)\n"
            "ORDER BY dept_id;",
        "Self-join: employees in same dept":
            "SELECT\n"
            "    a.emp_name AS employee_1,\n"
            "    b.emp_name AS employee_2,\n"
            "    a.dept_id\n"
            "FROM employees a\n"
            "JOIN employees b\n"
            "    ON a.dept_id = b.dept_id\n"
            "    AND a.emp_id < b.emp_id\n"
            "ORDER BY a.dept_id;",
        "Describe employees": "DESCRIBE employees;",
        "Describe projects": "DESCRIBE projects;",
    }

    chosen = st.selectbox("Quick examples", example_queries.keys(), key="sql_ex")
    default_sql = example_queries[chosen]

    sql_input = st.text_area(
        "Enter your SQL",
        value=default_sql,
        height=180,
        placeholder="SELECT * FROM employees e INNER JOIN projects p ON e.dept_id = p.dept_id;",
        key="sql_input",
    )

    if st.button("Run Query", type="primary", key="run_sql"):
        if not sql_input.strip():
            st.error("Please enter a SQL statement.")
        else:
            try:
                conn = get_connection()
                result = conn.execute(sql_input.strip())
                try:
                    columns = [desc[0] for desc in result.description]
                    rows = result.fetchall()
                    df_sql = pd.DataFrame(rows, columns=columns)
                    st.dataframe(df_sql, use_container_width=True, hide_index=True)
                    st.caption(f"Returned {len(df_sql)} row(s)")
                except Exception:
                    st.success("Statement executed successfully (no rows returned).")
            except Exception as e:
                st.error(f"SQL Error: {e}")


# Footer
st.divider()
st.caption(
    "Built with [Streamlit](https://streamlit.io) • "
    "Data stored in [DuckDB](https://duckdb.org) • "
    "Designed for introductory DBMS courses"
)
