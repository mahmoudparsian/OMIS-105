"""
Streamlit + DuckDB — Single-Table Aggregation Explorer
=======================================================
One table: employees (payroll data), loaded from **employees.csv**.
No joins — pure focus on aggregation functions and GROUP BY.

Table:
    employees (emp_id, emp_name, department, job_title,
               salary, hire_date, city)

Data file:
    employees.csv  (must be in the same directory as this script)

Tabs:
  1. View Data         — the full table
  2. COUNT             — COUNT(*), COUNT(DISTINCT)
  3. SUM / AVG         — SUM(salary), AVG(salary)
  4. MIN / MAX         — MIN/MAX on salary and hire_date
  5. STRING_AGG / LIST — see what's in each group
  6. HAVING            — filter on aggregated values
  7. Multi-Column GROUP BY — group by two columns at once
  8. SQL Explorer       — free-form practice

Usage:
    pip install streamlit duckdb pandas
    streamlit run app_aggregation_single.py
"""

import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

DB_FILE = "payroll_demo.duckdb"

# CSV file is expected in the same directory as this script
CSV_FILE = Path(__file__).parent / "employees.csv"


def get_connection() -> duckdb.DuckDBPyConnection:
    if "db_conn" not in st.session_state:
        conn = duckdb.connect(DB_FILE)
        _init_table(conn)
        st.session_state.db_conn = conn
    return st.session_state.db_conn


def _init_table(conn: duckdb.DuckDBPyConnection):
    """Create the employees table and load data from CSV if empty."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id      VARCHAR PRIMARY KEY,
            emp_name    VARCHAR NOT NULL,
            department  VARCHAR NOT NULL,
            job_title   VARCHAR NOT NULL,
            salary      DECIMAL(10,2) NOT NULL,
            hire_date   DATE NOT NULL,
            city        VARCHAR NOT NULL
        )
    """)

    if conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0] == 0:
        if not CSV_FILE.exists():
            st.error(
                f"Data file not found: **{CSV_FILE.name}**\n\n"
                f"Please place `employees.csv` in the same folder as this script:\n"
                f"`{CSV_FILE.parent}`"
            )
            st.stop()

        # DuckDB can read CSV directly — no pandas needed for the load
        conn.execute(f"""
            INSERT INTO employees
            SELECT * FROM read_csv_auto('{CSV_FILE}',
                                        header = true,
                                        dateformat = '%Y-%m-%d')
        """)


def reset_table():
    """Drop and reload the table from CSV."""
    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS employees")
    _init_table(conn)


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def run_query(sql: str) -> pd.DataFrame:
    conn = get_connection()
    return conn.execute(sql).fetchdf()


def run_query_safe(sql: str):
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


def get_all_employees() -> pd.DataFrame:
    return run_query("SELECT * FROM employees ORDER BY emp_id")


# ---------------------------------------------------------------------------
# Streamlit App
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Aggregation Explorer (Single Table)", page_icon="📊", layout="wide")

st.title("📊 Single-Table Aggregation Explorer")
st.caption(
    "Powered by **Streamlit** and **DuckDB** — "
    "One table, all the aggregation functions"
)

# Sidebar
with st.sidebar:
    st.header("Schema")
    st.code(
        "employees (\n"
        "  emp_id      VARCHAR PK,\n"
        "  emp_name    VARCHAR,\n"
        "  department  VARCHAR,\n"
        "  job_title   VARCHAR,\n"
        "  salary      DECIMAL(10,2),\n"
        "  hire_date   DATE,\n"
        "  city        VARCHAR\n"
        ")",
        language="sql",
    )
    st.divider()

    emp_count = get_connection().execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    st.metric("Total Employees", emp_count)
    st.divider()

    st.subheader("Aggregation Functions")
    st.code(
        "COUNT(*), COUNT(col)\n"
        "COUNT(DISTINCT col)\n"
        "SUM(col), AVG(col)\n"
        "MIN(col), MAX(col)\n"
        "STRING_AGG(col, sep)\n"
        "LIST(col)\n"
        "ROUND(expr, n)",
        language="sql",
    )
    st.divider()

    st.info(
        "**No JOINs needed!** Everything comes from a single `employees` table, "
        "so you can focus purely on how GROUP BY and aggregation work."
    )
    st.divider()

    if st.button("Reset Table from CSV", type="secondary"):
        reset_table()
        st.success("Table reloaded from employees.csv!")
        st.rerun()

    st.divider()
    st.caption(f"Data source: `{CSV_FILE.name}`")
    st.caption(f"DuckDB file: `{DB_FILE}`")


# Groupable columns
GROUP_COLS = ["department", "city", "job_title"]

# Tabs
tab_data, tab_count, tab_sum_avg, tab_min_max, tab_concat, tab_having, tab_multi, tab_sql = st.tabs([
    "📋 View Data",
    "🔢 COUNT",
    "➕ SUM / AVG",
    "↕️ MIN / MAX",
    "🔗 STRING_AGG / LIST",
    "🚧 HAVING",
    "📐 Multi-Column GROUP BY",
    "🧪 SQL Explorer",
])


# ---- TAB: View Data ---------------------------------------------------------
with tab_data:
    st.subheader("The employees Table")
    st.code("SELECT * FROM employees ORDER BY emp_id;", language="sql")

    df_all = get_all_employees()
    st.dataframe(df_all, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_all)} employee(s)")

    st.divider()
    st.markdown("##### Quick Summary")
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    with summary_col1:
        st.markdown("**Departments**")
        st.dataframe(
            run_query("SELECT department, COUNT(*) AS count FROM employees GROUP BY department ORDER BY department"),
            use_container_width=True, hide_index=True,
        )
    with summary_col2:
        st.markdown("**Cities**")
        st.dataframe(
            run_query("SELECT city, COUNT(*) AS count FROM employees GROUP BY city ORDER BY city"),
            use_container_width=True, hide_index=True,
        )
    with summary_col3:
        st.markdown("**Salary Range**")
        st.dataframe(
            run_query("""
                SELECT
                    MIN(salary) AS min_salary,
                    MAX(salary) AS max_salary,
                    ROUND(AVG(salary), 2) AS avg_salary
                FROM employees
            """),
            use_container_width=True, hide_index=True,
        )


# ---- TAB: COUNT --------------------------------------------------------------
with tab_count:
    st.subheader("COUNT & COUNT(DISTINCT)")

    gc = st.selectbox("GROUP BY column", GROUP_COLS, key="count_gc")

    sql_count = f"""
SELECT
    {gc},
    COUNT(*)                                AS employee_count,
    COUNT(DISTINCT city)                    AS distinct_cities,
    COUNT(DISTINCT job_title)               AS distinct_titles,
    STRING_AGG(emp_name, ', '
               ORDER BY emp_name)           AS employees_in_group
FROM employees
GROUP BY {gc}
ORDER BY employee_count DESC;"""

    st.markdown("##### Raw Table")
    df_raw = get_all_employees()
    st.dataframe(df_raw, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_raw)} row(s)")

    st.divider()

    st.markdown("##### Aggregated Result")
    st.code(sql_count.strip(), language="sql")
    df_agg = run_query(sql_count)
    st.dataframe(df_agg, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_agg)} group(s)")

    st.info(
        "**`employees_in_group`** shows the names that are being counted. "
        "Compare with the raw table above to verify each group!"
    )


# ---- TAB: SUM / AVG ---------------------------------------------------------
with tab_sum_avg:
    st.subheader("SUM & AVG (Salary)")

    gc2 = st.selectbox("GROUP BY column", GROUP_COLS, key="sum_gc")

    sql_sum = f"""
SELECT
    {gc2},
    COUNT(*)                               AS employee_count,
    ROUND(SUM(salary), 2)                   AS total_salary,
    ROUND(AVG(salary), 2)                   AS avg_salary,
    STRING_AGG(
        emp_name || ' ($' || CAST(salary AS VARCHAR) || ')',
        ',  '
        ORDER BY emp_name
    )                                       AS salary_details
FROM employees
GROUP BY {gc2}
ORDER BY total_salary DESC;"""

    st.markdown("##### Raw Table")
    st.dataframe(get_all_employees(), use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("##### Aggregated Result")
    st.code(sql_sum.strip(), language="sql")
    st.dataframe(run_query(sql_sum), use_container_width=True, hide_index=True)

    st.info(
        "**`salary_details`** shows each employee with their salary. "
        "Add them up manually to verify the SUM, then divide by count to check the AVG!"
    )

    # Bonus: show without GROUP BY (whole-table aggregation)
    with st.expander("Aggregation WITHOUT GROUP BY (whole table)"):
        sql_no_group = """
SELECT
    COUNT(*)              AS total_employees,
    ROUND(SUM(salary), 2) AS total_payroll,
    ROUND(AVG(salary), 2) AS avg_salary,
    MIN(salary)            AS lowest_salary,
    MAX(salary)            AS highest_salary
FROM employees;"""
        st.code(sql_no_group.strip(), language="sql")
        st.dataframe(run_query(sql_no_group), use_container_width=True, hide_index=True)
        st.caption(
            "When there is no GROUP BY, the entire table is treated as one group."
        )


# ---- TAB: MIN / MAX ---------------------------------------------------------
with tab_min_max:
    st.subheader("MIN & MAX")

    gc3 = st.selectbox("GROUP BY column", GROUP_COLS, key="minmax_gc")

    sql_minmax = f"""
SELECT
    {gc3},
    COUNT(*)                              AS employee_count,
    MIN(salary)                            AS min_salary,
    MAX(salary)                            AS max_salary,
    MAX(salary) - MIN(salary)              AS salary_range,
    MIN(hire_date)                         AS earliest_hire,
    MAX(hire_date)                         AS latest_hire,
    LIST(salary ORDER BY salary)           AS salaries_sorted,
    STRING_AGG(emp_name, ', '
               ORDER BY salary)            AS names_by_salary_asc
FROM employees
GROUP BY {gc3}
ORDER BY {gc3};"""

    st.markdown("##### Raw Table")
    st.dataframe(get_all_employees(), use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("##### Aggregated Result")
    st.code(sql_minmax.strip(), language="sql")
    st.dataframe(run_query(sql_minmax), use_container_width=True, hide_index=True)

    st.info(
        "**`salaries_sorted`** shows all salaries in ascending order — "
        "the first is MIN, the last is MAX. "
        "**`names_by_salary_asc`** lists employees sorted by salary so you "
        "can see who earns the least and most in each group."
    )


# ---- TAB: STRING_AGG / LIST -------------------------------------------------
with tab_concat:
    st.subheader("STRING_AGG & LIST  (Group Concatenation)")
    st.markdown(
        "These functions **reveal what's inside each group**. "
        "They are your best debugging tool when writing GROUP BY queries."
    )

    gc4 = st.selectbox("GROUP BY column", GROUP_COLS, key="concat_gc")

    sql_concat = f"""
SELECT
    {gc4},
    COUNT(*) AS group_size,

    -- STRING_AGG: comma-separated text
    STRING_AGG(emp_name, ', '
               ORDER BY emp_name)          AS names_csv,

    -- LIST: DuckDB array
    LIST(emp_name ORDER BY emp_name)       AS names_array,

    -- STRING_AGG with salary detail
    STRING_AGG(
        emp_name || ' (' || job_title || ', $' || CAST(salary AS VARCHAR) || ')',
        ',  '
        ORDER BY salary DESC
    )                                       AS full_detail,

    -- LIST of distinct job titles
    LIST(DISTINCT job_title
         ORDER BY job_title)               AS distinct_titles,

    -- LIST of salaries sorted
    LIST(salary ORDER BY salary)           AS salaries

FROM employees
GROUP BY {gc4}
ORDER BY {gc4};"""

    st.markdown("##### Raw Table")
    st.dataframe(get_all_employees(), use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("##### Aggregated Result")
    st.code(sql_concat.strip(), language="sql")
    df_concat = run_query(sql_concat)
    st.dataframe(df_concat, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_concat)} group(s)")

    st.divider()
    st.markdown("##### Function Comparison Across Databases")
    comp = {
        "DuckDB": [
            "STRING_AGG(col, ', ')",
            "STRING_AGG(DISTINCT col, ', ')",
            "LIST(col)",
            "LIST(DISTINCT col)",
        ],
        "MySQL": [
            "GROUP_CONCAT(col SEPARATOR ', ')",
            "GROUP_CONCAT(DISTINCT col SEPARATOR ', ')",
            "JSON_ARRAYAGG(col)",
            "(no direct equivalent)",
        ],
        "PostgreSQL": [
            "STRING_AGG(col, ', ')",
            "STRING_AGG(DISTINCT col, ', ')",
            "ARRAY_AGG(col)",
            "ARRAY_AGG(DISTINCT col)",
        ],
        "Returns": [
            "Comma-separated text",
            "Text (no duplicates)",
            "Array [ ... ]",
            "Array (no duplicates)",
        ],
    }
    st.dataframe(pd.DataFrame(comp), use_container_width=True, hide_index=True)


# ---- TAB: HAVING ------------------------------------------------------------
with tab_having:
    st.subheader("HAVING — Filter on Aggregated Values")
    st.markdown(
        "`WHERE` filters **rows before** grouping.  \n"
        "`HAVING` filters **groups after** aggregation."
    )

    gc5 = st.selectbox("GROUP BY column", GROUP_COLS, key="having_gc")

    hcol1, hcol2, hcol3 = st.columns(3)
    with hcol1:
        having_func = st.selectbox(
            "Aggregate function",
            ["COUNT(*)", "ROUND(AVG(salary), 2)", "SUM(salary)",
             "MAX(salary)", "MIN(salary)", "COUNT(DISTINCT job_title)"],
            key="having_func",
        )
    with hcol2:
        having_op = st.selectbox("Operator", [">", ">=", "=", "<=", "<", "!="], key="having_op")
    with hcol3:
        having_val = st.number_input("Value", value=3, step=1, key="having_val")

    alias = {
        "COUNT(*)": "group_count",
        "ROUND(AVG(salary), 2)": "avg_salary",
        "SUM(salary)": "total_salary",
        "MAX(salary)": "max_salary",
        "MIN(salary)": "min_salary",
        "COUNT(DISTINCT job_title)": "distinct_titles",
    }.get(having_func, "agg_value")

    sql_having = f"""
SELECT
    {gc5},
    {having_func} AS {alias},
    STRING_AGG(emp_name, ', '
               ORDER BY emp_name)          AS employees_in_group,
    STRING_AGG(
        emp_name || ' ($' || CAST(salary AS VARCHAR) || ')',
        ', ' ORDER BY emp_name
    )                                       AS detail
FROM employees
GROUP BY {gc5}
HAVING {having_func} {having_op} {having_val}
ORDER BY {alias} DESC;"""

    sql_all_groups = f"""
SELECT
    {gc5},
    {having_func} AS {alias},
    STRING_AGG(emp_name, ', '
               ORDER BY emp_name)          AS employees_in_group
FROM employees
GROUP BY {gc5}
ORDER BY {alias} DESC;"""

    st.code(sql_having.strip(), language="sql")

    col_all, col_filt = st.columns(2)
    with col_all:
        st.markdown("##### ALL Groups (no HAVING)")
        df_all_g = run_query(sql_all_groups)
        st.dataframe(df_all_g, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_all_g)} group(s)")

    with col_filt:
        st.markdown(f"##### Filtered (HAVING {having_func} {having_op} {having_val})")
        df_filt = run_query(sql_having)
        if len(df_filt) > 0:
            st.dataframe(df_filt, use_container_width=True, hide_index=True)
            st.caption(f"{len(df_filt)} group(s) passed the filter")
        else:
            st.warning("No groups satisfy the HAVING condition. Try adjusting the value.")

    st.divider()
    st.markdown("##### WHERE vs HAVING")
    wvh = {
        "Clause": ["WHERE", "HAVING"],
        "Filters": ["Individual rows", "Aggregated groups"],
        "Executes": ["BEFORE GROUP BY", "AFTER GROUP BY"],
        "Can use aggregates?": ["No", "Yes"],
        "Example": [
            "WHERE salary > 80000",
            "HAVING COUNT(*) > 3",
        ],
    }
    st.dataframe(pd.DataFrame(wvh), use_container_width=True, hide_index=True)

    # Bonus: combine WHERE + HAVING
    with st.expander("Combining WHERE and HAVING"):
        sql_both = f"""
-- First WHERE filters rows, then GROUP BY groups them,
-- then HAVING filters the groups.

SELECT
    department,
    COUNT(*)               AS count_after_where,
    ROUND(AVG(salary), 2)  AS avg_salary,
    STRING_AGG(emp_name || ' ($' || CAST(salary AS VARCHAR) || ')',
               ', ' ORDER BY emp_name) AS detail
FROM employees
WHERE salary > 70000          -- Step 1: keep only rows with salary > 70K
GROUP BY department
HAVING COUNT(*) >= 2          -- Step 2: keep groups with 2+ remaining employees
ORDER BY avg_salary DESC;"""
        st.code(sql_both.strip(), language="sql")
        st.dataframe(run_query(sql_both), use_container_width=True, hide_index=True)
        st.caption(
            "The WHERE removed low-salary employees first, then GROUP BY grouped "
            "the survivors, then HAVING kept only groups with 2+ employees."
        )


# ---- TAB: Multi-Column GROUP BY ---------------------------------------------
with tab_multi:
    st.subheader("GROUP BY Multiple Columns")
    st.markdown(
        "Grouping by **two columns** creates finer-grained groups. "
        "Each unique combination of values becomes its own group."
    )

    mc1, mc2 = st.columns(2)
    with mc1:
        col_a = st.selectbox("First GROUP BY column", GROUP_COLS, index=0, key="multi_a")
    with mc2:
        remaining = [c for c in GROUP_COLS if c != col_a]
        col_b = st.selectbox("Second GROUP BY column", remaining, index=0, key="multi_b")

    sql_multi = f"""
SELECT
    {col_a},
    {col_b},
    COUNT(*)                               AS employee_count,
    ROUND(AVG(salary), 2)                   AS avg_salary,
    ROUND(SUM(salary), 2)                   AS total_salary,
    STRING_AGG(emp_name, ', '
               ORDER BY emp_name)           AS employees_in_group,
    LIST(salary ORDER BY salary)            AS salaries
FROM employees
GROUP BY {col_a}, {col_b}
ORDER BY {col_a}, {col_b};"""

    # Also show single-column group for comparison
    sql_single = f"""
SELECT
    {col_a},
    COUNT(*)                               AS employee_count,
    ROUND(AVG(salary), 2)                   AS avg_salary,
    STRING_AGG(emp_name, ', '
               ORDER BY emp_name)           AS employees_in_group
FROM employees
GROUP BY {col_a}
ORDER BY {col_a};"""

    col_single, col_multi = st.columns(2)
    with col_single:
        st.markdown(f"##### GROUP BY `{col_a}` only")
        st.code(sql_single.strip(), language="sql")
        df_single = run_query(sql_single)
        st.dataframe(df_single, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_single)} group(s)")

    with col_multi:
        st.markdown(f"##### GROUP BY `{col_a}`, `{col_b}`")
        st.code(sql_multi.strip(), language="sql")
        df_multi = run_query(sql_multi)
        st.dataframe(df_multi, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_multi)} group(s)")

    st.info(
        f"**Compare:** Grouping by `{col_a}` alone produced **{len(df_single)}** groups. "
        f"Adding `{col_b}` split them into **{len(df_multi)}** finer groups. "
        "Each unique combination of the two columns is its own group."
    )


# ---- TAB: SQL Explorer -------------------------------------------------------
with tab_sql:
    st.subheader("SQL Explorer")
    st.info("Write any SQL against the **employees** table.")

    examples = {
        "(custom)": "",
        "Department salary summary": (
            "SELECT\n"
            "    department,\n"
            "    COUNT(*) AS headcount,\n"
            "    ROUND(AVG(salary), 2) AS avg_salary,\n"
            "    ROUND(SUM(salary), 2) AS total_payroll,\n"
            "    STRING_AGG(emp_name, ', ' ORDER BY salary DESC) AS by_salary\n"
            "FROM employees\n"
            "GROUP BY department\n"
            "ORDER BY total_payroll DESC;"
        ),
        "Hire year breakdown": (
            "SELECT\n"
            "    EXTRACT(YEAR FROM hire_date) AS hire_year,\n"
            "    COUNT(*) AS hires,\n"
            "    ROUND(AVG(salary), 2) AS avg_salary,\n"
            "    LIST(emp_name ORDER BY emp_name) AS who\n"
            "FROM employees\n"
            "GROUP BY hire_year\n"
            "ORDER BY hire_year;"
        ),
        "Top 5 salaries": (
            "SELECT emp_name, department, job_title, salary\n"
            "FROM employees\n"
            "ORDER BY salary DESC\n"
            "LIMIT 5;"
        ),
        "Departments with avg salary > 90K": (
            "SELECT\n"
            "    department,\n"
            "    COUNT(*) AS headcount,\n"
            "    ROUND(AVG(salary), 2) AS avg_salary,\n"
            "    STRING_AGG(\n"
            "        emp_name || ' ($' || CAST(salary AS VARCHAR) || ')',\n"
            "        ', ' ORDER BY salary DESC\n"
            "    ) AS detail\n"
            "FROM employees\n"
            "GROUP BY department\n"
            "HAVING AVG(salary) > 90000\n"
            "ORDER BY avg_salary DESC;"
        ),
        "City × Department cross-tab": (
            "SELECT\n"
            "    city,\n"
            "    COUNT(*) FILTER (WHERE department = 'Engineering') AS engineering,\n"
            "    COUNT(*) FILTER (WHERE department = 'Marketing') AS marketing,\n"
            "    COUNT(*) FILTER (WHERE department = 'Sales') AS sales,\n"
            "    COUNT(*) FILTER (WHERE department = 'HR') AS hr,\n"
            "    COUNT(*) FILTER (WHERE department = 'Finance') AS finance,\n"
            "    COUNT(*) AS total\n"
            "FROM employees\n"
            "GROUP BY city\n"
            "ORDER BY total DESC;"
        ),
        "Salary quartiles by department": (
            "SELECT\n"
            "    department,\n"
            "    QUANTILE_CONT(salary, 0.25) AS q1,\n"
            "    QUANTILE_CONT(salary, 0.50) AS median,\n"
            "    QUANTILE_CONT(salary, 0.75) AS q3,\n"
            "    ROUND(AVG(salary), 2) AS mean\n"
            "FROM employees\n"
            "GROUP BY department\n"
            "ORDER BY median DESC;"
        ),
        "WHERE + GROUP BY + HAVING": (
            "-- Only employees hired after 2020,\n"
            "-- grouped by department,\n"
            "-- keep groups with 2+ people.\n\n"
            "SELECT\n"
            "    department,\n"
            "    COUNT(*) AS recent_hires,\n"
            "    ROUND(AVG(salary), 2) AS avg_salary,\n"
            "    STRING_AGG(emp_name || ' (' || CAST(hire_date AS VARCHAR) || ')',\n"
            "               ', ' ORDER BY hire_date) AS detail\n"
            "FROM employees\n"
            "WHERE hire_date >= '2021-01-01'\n"
            "GROUP BY department\n"
            "HAVING COUNT(*) >= 2\n"
            "ORDER BY recent_hires DESC;"
        ),
        "Describe table": "DESCRIBE employees;",
    }

    chosen = st.selectbox("Quick examples", examples.keys(), key="sql_ex")
    default_sql = examples[chosen]

    sql_input = st.text_area(
        "Enter your SQL",
        value=default_sql,
        height=200,
        placeholder="SELECT department, COUNT(*) FROM employees GROUP BY department;",
        key="sql_input",
    )

    if st.button("Run Query", type="primary", key="run_sql"):
        if not sql_input.strip():
            st.error("Please enter a SQL statement.")
        else:
            statements = [
                s.strip() for s in sql_input.strip().split(";")
                if s.strip() and not s.strip().startswith("--")
            ]
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
