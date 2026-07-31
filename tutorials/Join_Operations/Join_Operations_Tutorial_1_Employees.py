import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🔗 SQL JOIN Operations — Interactive DuckDB Tutorial

    > **Learning goal:** Master `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`, and more through 20 hands-on exercises using a realistic employee dataset.

    **Dataset:**
    | Table | Rows | Description |
    |-------|------|-------------|
    | `employees` | *(see Cell 0)* | Employees with salary, education, country, dept |
    | `departments` | 7 | 5 active + 2 unused (AI, IT) |
    | `countries` | 10 | Reference table with population |

    > 💡 **Tip:** Run cells top-to-bottom. Each cell has: a plain-English explanation → formatted SQL → beautiful result table → chart.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Setup: load DuckDB and helper modules 
    """)
    return


@app.cell
def _():
    # ── Setup: load DuckDB and helper modules ─────────────────────────
    import duckdb
    import pandas as pd
    import sys, os

    # Make sure helper modules are found
    sys.path.insert(0, os.path.dirname(os.path.abspath(".")))

    from display_tables import render_table, render_sql, render_section_header, render_summary_card
    from plots import (plot_hbar, plot_bar, plot_donut, plot_heatmap,
                       plot_boxplot, plot_stacked_bar, plot_scatter,
                       plot_join_venn, plot_line, plot_grouped_bar)
    return (duckdb, plot_bar, plot_donut, plot_grouped_bar, plot_hbar, plot_heatmap, plot_join_venn, plot_line, plot_scatter, plot_stacked_bar, render_section_header, render_sql, render_summary_card, render_table)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Read CSV Files and Create Database Tables
    """)
    return


@app.cell
def _(duckdb):
    # Create an in-memory DuckDB database and load the CSVs
    con = duckdb.connect()

    con.execute("""
        CREATE TABLE departments AS
        SELECT *
        FROM read_csv_auto('./data/departments.csv', header=True);
    """)
    con.execute("""
        CREATE TABLE countries AS
        SELECT *
        FROM read_csv_auto('./data/countries.csv', header=True);
    """)
    con.execute("""
        CREATE TABLE employees AS
        SELECT *
        FROM read_csv_auto('./data/employees.csv', header=True);
    """)

    print("✅  Tables loaded successfully!")
    print(f"   employees  : {con.execute('SELECT COUNT(*) FROM employees').fetchone()[0]:,} rows")
    print(f"   departments: {con.execute('SELECT COUNT(*) FROM departments').fetchone()[0]:,} rows")
    print(f"   countries  : {con.execute('SELECT COUNT(*) FROM countries').fetchone()[0]:,} rows")
    return (con,)


@app.cell
def _(con, plot_donut, render_section_header, render_sql, render_summary_card, render_table):
    render_section_header(1, "Dataset Overview", "A quick look at all three tables", "")

    from IPython.display import display, HTML
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>
      Before joining tables, let's understand what data we have.
      We preview the first rows of each table and basic statistics.
    </div>
    """))

    # Employees sample
    render_sql("SELECT emp_id, emp_name, salary, dept_id, country_code, gender, education, hire_date\nFROM employees LIMIT 8", "employees table sample")
    df_emp = con.execute("""
        SELECT
            emp_id,
            emp_name,
            salary,
            dept_id,
            country_code,
            gender,
            education,
            hire_date
        FROM employees
        LIMIT 8;
    """).df()
    render_table(df_emp, "employees (first 8 rows)", "👥")

    # Departments
    render_sql("""
        SELECT *
        FROM departments;
    """, "departments table (all 7 rows)")
    df_dept = con.execute("SELECT * FROM departments").df()
    render_table(df_dept, "departments (all 7 rows)", "🏢")

    # Countries
    render_sql("""
        SELECT *
        FROM countries;
    """, "countries table (all 10 rows)")
    df_ctry = con.execute("SELECT * FROM countries").df()
    render_table(df_ctry, "countries (all 10 rows)", "🌍")

    # Summary stats — pulled live from the tables, never hardcoded
    n_emp      = con.execute("""
        SELECT COUNT(*)
        FROM employees;
    """).fetchone()[0]
    n_secret   = con.execute("""
        SELECT COUNT(*)
        FROM employees
        WHERE dept_id = 'TOP-SECRET';
    """).fetchone()[0]
    n_active_d = con.execute("""
        SELECT COUNT(DISTINCT dept_id)
        FROM employees
        WHERE dept_id != 'TOP-SECRET';
    """).fetchone()[0]
    n_unused_d = con.execute("""
        SELECT COUNT(*)
        FROM departments d
        LEFT
        JOIN employees e ON d.dept_id = e.dept_id
        WHERE e.emp_id IS NULL;
    """).fetchone()[0]
    n_countries = con.execute("""
        SELECT COUNT(*)
        FROM countries;
    """).fetchone()[0]
    stats = {
        "Total Employees": n_emp,
        "Active Depts":    n_active_d,
        "Unused Depts":    n_unused_d,
        "Countries":       n_countries,
        "TOP-SECRET":      n_secret,
    }
    render_summary_card(stats, "Dataset Quick Facts", "📊")

    # Education breakdown chart
    df_edu = con.execute("""
        SELECT
            education,
            COUNT(*) AS cnt
        FROM employees
        GROUP BY education
        ORDER BY cnt DESC;
    """).df()
    n_phd = con.execute("""
        SELECT COUNT(*)
        FROM employees
        WHERE education='PHD';
    """).fetchone()[0]
    n_law = con.execute("""
        SELECT COUNT(*)
        FROM employees
        WHERE education='LAW';
    """).fetchone()[0]
    plot_donut(df_edu, "education", "cnt",
               title=f"Education Distribution across {n_emp:,} Employees",
               caption=f"Only {n_phd} PhD holders and {n_law} LAW graduates")

    return (HTML, display)


@app.cell
def _(HTML, con, display, plot_hbar, plot_join_venn, render_section_header, render_sql, render_table):
    render_section_header(2, "INNER JOIN: Employees ↔ Departments", "Only employees whose dept_id exists in the departments table", "INNER JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>We want to see each employee's department name and location. An INNER JOIN keeps ONLY the rows that have a matching key in BOTH tables. The 10 employees with dept_id = 'TOP-SECRET' are silently dropped because TOP-SECRET is not in the departments table.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
    SELECT
        e.emp_id,
        e.emp_name,
        e.salary,
        e.gender,
        d.dept_name,
        d.dept_location
    FROM employees  AS e
    INNER JOIN departments AS d
        ON e.dept_id = d.dept_id
    LIMIT 20
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "INNER JOIN: Employees ↔ Departments", "🔗")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_dept_cnt = con.execute("""
        SELECT
            d.dept_name,
            COUNT(*) AS num_employees
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY num_employees DESC;
    """).df()
    plot_hbar(df_dept_cnt, "num_employees", "dept_name",
              title="Employees per Department (INNER JOIN)",
              xlabel="Number of Employees", ylabel="Department",
              caption="10 TOP-SECRET employees are excluded — they have no matching dept row",
              color="#e94560")
    _n_emp   = con.execute("""
        SELECT COUNT(*)
        FROM employees;
    """).fetchone()[0]
    _n_inner = con.execute("""
        SELECT COUNT(*)
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id;
    """).fetchone()[0]
    plot_join_venn("INNER", _n_emp, 7, _n_inner,
                   title="INNER JOIN: only rows that match in BOTH tables")

    return


@app.cell
def _(HTML, con, display, plot_join_venn, render_section_header, render_sql, render_table):
    render_section_header(3, "LEFT JOIN: Find Orphan Employees", "Detect employees whose dept_id has no matching department", "LEFT JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>A LEFT JOIN keeps ALL rows from the left table (employees) and fills NULLs for columns from the right table (departments) when there is no match. This is perfect for finding data quality problems — here we find the 10 employees assigned to the mysterious 'TOP-SECRET' department.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
    SELECT
        e.emp_id,
        e.emp_name,
        e.dept_id            AS emp_dept_id,
        d.dept_id            AS dept_table_id,
        d.dept_name,
        d.dept_location
    FROM employees  AS e
    LEFT JOIN departments AS d
        ON e.dept_id = d.dept_id
    WHERE d.dept_id IS NULL          -- only the unmatched employees
    ORDER BY e.emp_id
    LIMIT 20
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "LEFT JOIN: Find Orphan Employees", "⬅️")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_orphans = con.execute("""
        SELECT
            e.dept_id AS dept_assigned,
            COUNT(*) AS employee_count
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE d.dept_id IS NULL
        GROUP BY e.dept_id;
    """).df()
    display(HTML('''<div style="background:#2d1b00;border:1px solid #f5a623;border-radius:8px;
    padding:12px 18px;color:#f5a623;font-size:13px;margin:12px 0;">
    ⚠️  <b>10 employees have dept_id = \'TOP-SECRET\'</b> — not in the departments table.
    A LEFT JOIN exposes them (with NULLs for department columns).
    An INNER JOIN would silently hide them!
    </div>'''))
    _n_emp = con.execute("""
        SELECT COUNT(*)
        FROM employees;
    """).fetchone()[0]
    _n_matched = con.execute("""
        SELECT COUNT(*)
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id;
    """).fetchone()[0]
    plot_join_venn("LEFT", _n_emp, 7, _n_matched)

    return


@app.cell
def _(HTML, con, display, plot_hbar, plot_join_venn, render_section_header, render_sql, render_table):
    render_section_header(4, "RIGHT JOIN: Find Unused Departments", "Which departments exist in the dept table but have zero employees?", "RIGHT JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>A RIGHT JOIN keeps ALL rows from the right table (departments) and fills NULLs for employee columns when there is no match. This reveals the AI and IT departments that have no employees assigned. In practice, LEFT JOIN is more common — a RIGHT JOIN is a LEFT JOIN with the tables swapped.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        SELECT
            d.dept_id,
            d.dept_name,
            d.dept_location,
            d.dept_manager,
            COUNT(e.emp_id) AS num_employees
        FROM employees AS e
        RIGHT
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY d.dept_id, d.dept_name, d.dept_location, d.dept_manager
        ORDER BY num_employees ASC;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "RIGHT JOIN: Find Unused Departments", "➡️")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_all_depts = con.execute("""
        SELECT
            d.dept_name,
            COUNT(e.emp_id) AS num_employees,
            CASE WHEN COUNT(e.emp_id) = 0 THEN 'Unused' ELSE 'Active' END AS status
        FROM employees e
        RIGHT
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY num_employees;
    """).df()
    plot_hbar(df_all_depts, "num_employees", "dept_name",
              title="All Departments — Employee Count (RIGHT JOIN)",
              xlabel="Number of Employees",
              caption="AI and IT show 0 employees — RIGHT JOIN reveals unused departments",
              color="#9b5de5")
    _n_emp = con.execute("""
        SELECT COUNT(*)
        FROM employees;
    """).fetchone()[0]
    plot_join_venn("RIGHT", _n_emp, 7, 5)

    return


@app.cell
def _(HTML, con, display, plot_bar, render_section_header, render_sql, render_table):
    render_section_header(5, "INNER JOIN: Employees ↔ Countries", "Headcount and average salary per country", "INNER JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>We join employees with countries to see where our workforce is located. We compute the headcount, average salary, and even a salary-to-population ratio per country. INNER JOIN is used because every employee has a valid country code.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        SELECT
            c.country_name,
            c.population,
            COUNT(e.emp_id) AS num_employees,
            ROUND(AVG(e.salary), 0) AS avg_salary,
            ROUND(AVG(e.salary) / c.population * 1000000, 4) AS salary_per_million_pop
        FROM employees AS e
        INNER
        JOIN countries AS c ON e.country_code = c.country_code
        GROUP BY c.country_name, c.population
        ORDER BY num_employees DESC;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "INNER JOIN: Employees ↔ Countries", "🌍")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_ctry_sal = con.execute("""
        SELECT
            c.country_name,
            COUNT(e.emp_id) AS num_employees,
            ROUND(AVG(e.salary),0) AS avg_salary
        FROM employees e
        INNER
        JOIN countries c ON e.country_code = c.country_code
        GROUP BY c.country_name
        ORDER BY num_employees DESC;
    """).df()
    plot_bar(df_ctry_sal, "country_name", "num_employees",
             title="Employee Count by Country",
             xlabel="Country", ylabel="Employees",
             caption="USA (500), India (400), China (300) dominate the headcount",
             color="#00bbf9", rotate=30)

    return


@app.cell
def _(HTML, con, display, plot_heatmap, render_section_header, render_sql, render_table):
    render_section_header(6, "3-Table INNER JOIN", "Joining employees, departments, AND countries in one query", "INNER JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>We can chain as many JOINs as we need. Here we join all three tables at once: each row shows the employee, their department name (from departments), and their country name (from countries). The result is a rich, denormalized view ready for analysis.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
    SELECT
        e.emp_id,
        e.emp_name,
        e.salary,
        e.education,
        d.dept_name,
        c.country_name
    FROM employees    AS e
    INNER JOIN departments AS d ON e.dept_id      = d.dept_id
    INNER JOIN countries   AS c ON e.country_code = c.country_code
    ORDER BY e.salary DESC
    LIMIT 15
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "3-Table INNER JOIN", "🔗🔗")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_3t = con.execute("""
        SELECT
            d.dept_name,
            c.country_name,
            COUNT(*) AS cnt
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        INNER
        JOIN countries c ON e.country_code = c.country_code
        GROUP BY d.dept_name, c.country_name
        ORDER BY cnt DESC
        LIMIT 20;
    """).df()
    plot_heatmap(df_3t, "dept_name", "country_name", "cnt",
                 title="Employees per Dept × Country (3-Table INNER JOIN)",
                 caption="Chaining two INNER JOINs lets us cross-analyse three tables at once")

    return


@app.cell
def _(HTML, con, display, plot_hbar, render_section_header, render_sql, render_table):
    render_section_header(7, "LEFT JOIN: Salary Stats per Department", "Drive from departments table so ALL 7 depts appear, even empty ones", "LEFT JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>When we drive from the departments table and LEFT JOIN employees, ALL 7 departments appear in the result — even AI and IT which have zero employees. AVG(salary) returns NULL for those empty departments. Compare this to Cell 2 where INNER JOIN excluded unused departments.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        SELECT
            d.dept_name,
            d.dept_location,
            COUNT(e.emp_id) AS headcount,
            ROUND(AVG(e.salary), 0) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary
        FROM departments AS d
        LEFT
        JOIN employees AS e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name, d.dept_location
        ORDER BY headcount DESC;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "LEFT JOIN: Salary Stats per Department", "📊")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_sal = con.execute("""
        SELECT
            d.dept_name,
            ROUND(AVG(e.salary),0) AS avg_salary,
            COUNT(e.emp_id) AS headcount
        FROM departments d
        LEFT
        JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
        ORDER BY avg_salary DESC;
    """).df()
    plot_hbar(df_sal, "avg_salary", "dept_name",
              title="Average Salary per Department (LEFT JOIN from departments)",
              xlabel="Average Salary ($)", ylabel="Department",
              caption="AI and IT show NULL avg salary — they have no employees")

    return


@app.cell
def _(HTML, con, display, plot_bar, render_section_header, render_sql, render_table):
    render_section_header(8, "Anti-Join: Departments With NO Employees", "LEFT JOIN + WHERE right.key IS NULL = Anti-Join pattern", "LEFT JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>The Anti-Join pattern is one of the most useful SQL tricks: LEFT JOIN a table, then filter WHERE the right side's key IS NULL. You get only the rows from the left table that have NO match in the right table. Here we find departments that have never had an employee assigned.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
    SELECT
        d.dept_id,
        d.dept_name,
        d.dept_manager,
        d.created_date
    FROM departments AS d
    LEFT JOIN employees  AS e ON d.dept_id = e.dept_id
    WHERE e.emp_id IS NULL          -- the anti-join condition
    ORDER BY d.dept_name
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "Anti-Join: Departments With NO Employees", "🚫")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_anti = con.execute("""
        SELECT
            d.dept_name,
            CASE WHEN e.emp_id IS NULL THEN 'No Employees (Anti-Join Match)' ELSE 'Has Employees' END AS status,
            COUNT(d.dept_id) AS count
        FROM departments d
        LEFT
        JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name, (e.emp_id IS NULL)
        ORDER BY status DESC;
    """).df()
    plot_bar(df_anti, "dept_name", "count",
             title="LEFT JOIN Anti-Join: Departments With Zero Employees",
             xlabel="Department", ylabel="Count",
             caption="WHERE e.emp_id IS NULL turns a LEFT JOIN into an anti-join",
             color="#9b5de5", rotate=30)

    return


@app.cell
def _(HTML, con, display, plot_hbar, render_section_header, render_sql, render_table):
    render_section_header(9, "Salary Analysis by Education × Department", "How does education level affect pay across departments?", "INNER JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>We join employees with departments then GROUP BY education and department to see how advanced degrees correlate with higher salaries. Only employees with a valid dept_id appear (INNER JOIN), so the 10 TOP-SECRET employees are excluded from this analysis.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        SELECT
            e.education,
            d.dept_name,
            COUNT(*) AS headcount,
            ROUND(AVG(e.salary), 0) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY e.education, d.dept_name
        ORDER BY e.education, avg_salary DESC;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "Salary Analysis by Education × Department", "🎓")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_edu_dept = con.execute("""
        SELECT
            e.education,
            ROUND(AVG(e.salary),0) AS avg_salary,
            COUNT(*) AS headcount
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY e.education
        ORDER BY avg_salary DESC;
    """).df()
    plot_hbar(df_edu_dept, "avg_salary", "education",
              title="Average Salary by Education Level (INNER JOIN)",
              xlabel="Average Salary ($)", ylabel="Education",
              caption="PHD and LAW holders command the highest salaries",
              color="#26c485")

    return


@app.cell
def _(HTML, con, display, plot_stacked_bar, render_section_header, render_sql, render_table):
    render_section_header(10, "Gender Distribution Across Departments", "Window function + INNER JOIN to compute % within each department", "INNER JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>We join employees to departments and use a window function (SUM(...) OVER PARTITION BY dept_name) to compute what percentage of each department is MALE, FEMALE, or UNKNOWN. This shows that INNER JOIN combined with GROUP BY and window functions gives powerful analytics in a single query.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        SELECT
            d.dept_name,
            e.gender,
            COUNT(*) AS headcount,
            ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY d.dept_name), 1) AS pct_of_dept
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name, e.gender
        ORDER BY d.dept_name, headcount DESC;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "Gender Distribution Across Departments", "⚧️")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_gender = con.execute("""
        SELECT
            d.dept_name,
            e.gender,
            COUNT(*) AS headcount
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name, e.gender
        ORDER BY d.dept_name, headcount DESC;
    """).df()
    plot_stacked_bar(df_gender, "dept_name", "gender", "headcount",
                     title="Gender Distribution per Department (Stacked)",
                     xlabel="Department", ylabel="Headcount",
                     caption="INNER JOIN + GROUP BY + window function for percentages")

    return


@app.cell
def _(HTML, con, display, plot_bar, render_section_header, render_sql, render_table):
    render_section_header(11, "Self-Join: PHD Colleagues in the Same Department", "Joining a table to ITSELF to find pairs of employees sharing education + dept", "INNER JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>A self-join is when we join a table to itself using two aliases (e1, e2). Here we find every pair of PHD employees who work in the same department. The condition e1.emp_id < e2.emp_id prevents duplicate pairs and self-matches. This pattern is useful for org-chart, mentorship, or colleague-pair queries.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
    SELECT
        e1.emp_name   AS employee_1,
        e2.emp_name   AS employee_2,
        e1.education,
        d.dept_name
    FROM employees    AS e1
    INNER JOIN employees    AS e2
        ON  e1.dept_id   = e2.dept_id
        AND e1.education = e2.education
        AND e1.emp_id    < e2.emp_id   -- avoid duplicates and self-rows
    INNER JOIN departments AS d ON e1.dept_id = d.dept_id
    WHERE e1.education = 'PHD'
    LIMIT 15
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "Self-Join: PHD Colleagues in the Same Department", "👥👥")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_phd_pairs = con.execute("""
        SELECT
            d.dept_name,
            COUNT(*) AS phd_pairs
        FROM employees e1
        INNER
        JOIN employees e2 ON e1.dept_id = e2.dept_id
        AND e1.education = e2.education
        AND e1.emp_id < e2.emp_id
        INNER
        JOIN departments d ON e1.dept_id = d.dept_id
        WHERE e1.education = 'PHD'
        GROUP BY d.dept_name
        ORDER BY phd_pairs DESC;
    """).df()
    plot_bar(df_phd_pairs, "dept_name", "phd_pairs",
             title="PHD Colleague Pairs per Department (Self-Join)",
             xlabel="Department", ylabel="PHD Pairs",
             caption="A self-join joins a table to itself — great for peer / hierarchy analysis",
             color="#f5a623", rotate=30)

    return


@app.cell
def _(HTML, con, display, plot_scatter, render_section_header, render_sql, render_table):
    render_section_header(12, "LEFT JOIN: Country Population vs Employee Count", "All 10 countries appear; compare representation to actual population", "LEFT JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>We drive from the countries table (LEFT side) and LEFT JOIN employees. All 10 countries appear even if a country has zero employees. We compute each country's share of the total workforce and compare it to the country's actual world population to see who is over- or under-represented.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        SELECT
            c.country_name,
            c.population,
            COUNT(e.emp_id) AS num_employees,
            ROUND(COUNT(e.emp_id) * 100.0 / SUM(COUNT(e.emp_id)) OVER (), 2) AS pct_of_workforce
        FROM countries AS c
        LEFT
        JOIN employees AS e ON c.country_code = e.country_code
        GROUP BY c.country_name, c.population
        ORDER BY num_employees DESC;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "LEFT JOIN: Country Population vs Employee Count", "🌐")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_pop = con.execute("""
        SELECT
            c.country_name,
            c.population,
            COUNT(e.emp_id) AS num_employees
        FROM countries c
        LEFT
        JOIN employees e ON c.country_code = e.country_code
        GROUP BY c.country_name, c.population
        ORDER BY num_employees DESC;
    """).df()
    plot_scatter(df_pop, "population", "num_employees",
                 title="Population vs Employee Count per Country (LEFT JOIN)",
                 xlabel="Country Population", ylabel="Employees in Dataset",
                 caption="India is highly over-represented; Japan and Australia under-represented")

    return


@app.cell
def _(HTML, con, display, plot_donut, plot_join_venn, render_section_header, render_sql, render_table):
    render_section_header(13, "FULL OUTER JOIN: See ALL Unmatched Rows", "Captures orphan employees AND empty departments in one query", "FULL JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>A FULL OUTER JOIN combines LEFT JOIN + RIGHT JOIN: it returns every row from both tables, filling NULL where there is no match. Here we filter to only the unmatched rows to see: (1) the 10 employees with dept_id=TOP-SECRET, and (2) the AI and IT departments that have no employees.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
    -- DuckDB supports FULL OUTER JOIN natively
    SELECT
        e.emp_id,
        e.emp_name,
        e.dept_id            AS emp_dept_id,
        d.dept_id            AS dept_table_id,
        d.dept_name,
        CASE
            WHEN d.dept_id IS NULL THEN '⚠️  No matching dept'
            WHEN e.emp_id  IS NULL THEN '🏢  Dept has no employees'
            ELSE '✅  Matched'
        END                  AS join_status
    FROM employees   AS e
    FULL OUTER JOIN departments AS d
        ON e.dept_id = d.dept_id
    WHERE d.dept_id IS NULL
       OR e.emp_id  IS NULL
    ORDER BY join_status, e.emp_id
    LIMIT 20
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "FULL OUTER JOIN: See ALL Unmatched Rows", "🔀")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_full = con.execute("""
        SELECT
            CASE WHEN d.dept_id IS NULL THEN 'Employee: no dept (TOP-SECRET)' WHEN e.emp_id IS NULL THEN 'Dept: no employees (AI/IT)' ELSE 'Matched' END AS status,
            COUNT(*) AS cnt
        FROM employees e
        FULL OUTER
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY status
        ORDER BY cnt DESC;
    """).df()
    plot_donut(df_full, "status", "cnt",
               title="FULL OUTER JOIN: Match Status",
               caption="FULL OUTER JOIN = LEFT JOIN ∪ RIGHT JOIN (all unmatched rows from BOTH sides)")
    _n_emp = con.execute("""
        SELECT COUNT(*)
        FROM employees;
    """).fetchone()[0]
    _n_matched = con.execute("""
        SELECT COUNT(*)
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id;
    """).fetchone()[0]
    plot_join_venn("FULL OUTER", _n_emp, 7, _n_matched)

    return


@app.cell
def _(HTML, con, display, plot_bar, render_section_header, render_sql, render_table):
    render_section_header(14, "INNER JOIN + HAVING: Filter After Aggregation", "Which departments have an average salary above $75,000?", "INNER JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>WHERE filters rows before grouping; HAVING filters groups after aggregation. Here we JOIN employees to departments, GROUP BY department, and then use HAVING to keep only departments where the average salary exceeds $75,000. This is a common pattern for finding high-performing segments.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        SELECT
            d.dept_name,
            COUNT(e.emp_id) AS headcount,
            ROUND(AVG(e.salary), 0) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary,
            ROUND(SUM(e.salary), 0) AS total_payroll
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        HAVING AVG(e.salary) > 75000
        ORDER BY avg_salary DESC;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "INNER JOIN + HAVING: Filter After Aggregation", "💰")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_payroll = con.execute("""
        SELECT
            d.dept_name,
            ROUND(AVG(e.salary),0) AS avg_salary,
            ROUND(SUM(e.salary)/1000000.0,2) AS total_payroll_M
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        HAVING AVG(e.salary) > 75000
        ORDER BY avg_salary DESC;
    """).df()
    plot_bar(df_payroll, "dept_name", "avg_salary",
             title="High-Earning Departments (AVG Salary > $75K) — HAVING Clause",
             xlabel="Department", ylabel="Average Salary ($)",
             caption="HAVING filters AFTER GROUP BY; WHERE filters BEFORE aggregation",
             color="#26c485", rotate=30)

    return


@app.cell
def _(HTML, con, display, plot_hbar, render_section_header, render_sql, render_table):
    render_section_header(15, "JOIN + Subquery: Above-Average Earners per Department", "Join the main table to a pre-aggregated subquery", "INNER JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>We can JOIN to a subquery (an inline derived table). First we compute the average salary per department in a subquery (dept_avg). Then we join it to employees and departments to find employees who earn more than their own department's average. This pattern avoids complex correlated subqueries and is very efficient.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        SELECT
            e.emp_name,
            e.salary,
            d.dept_name,
            dept_avg.avg_salary AS dept_avg_salary,
            ROUND(e.salary - dept_avg.avg_salary, 0) AS salary_above_avg
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        INNER
        JOIN (
        SELECT
            dept_id,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY dept_id ) AS dept_avg ON e.dept_id = dept_avg.dept_id
        WHERE e.salary > dept_avg.avg_salary
        ORDER BY salary_above_avg DESC
        LIMIT 20;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "JOIN + Subquery: Above-Average Earners per Department", "⬆️💲")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_above = con.execute("""
        SELECT
            d.dept_name,
            COUNT(*) AS above_avg_count,
            ROUND(AVG(e.salary - dept_avg.avg_salary),0) AS mean_excess
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        INNER
        JOIN (
        SELECT
            dept_id,
            AVG(salary) AS avg_salary
        FROM employees
        GROUP BY dept_id ) dept_avg ON e.dept_id = dept_avg.dept_id
        WHERE e.salary > dept_avg.avg_salary
        GROUP BY d.dept_name
        ORDER BY mean_excess DESC;
    """).df()
    plot_hbar(df_above, "mean_excess", "dept_name",
              title="Mean Salary Excess vs Dept Average (JOIN + Subquery)",
              xlabel="Mean $ above dept average", ylabel="Department",
              caption="Joining to a subquery is a powerful pattern for relative comparisons",
              color="#f5a623")

    return


@app.cell
def _(HTML, con, display, plot_hbar, render_section_header, render_sql, render_table):
    render_section_header(16, "CTE + JOIN: Employee Tenure Analysis", "Using WITH (Common Table Expressions) to organise a multi-step JOIN", "INNER JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>CTEs (WITH clauses) let us define named intermediate result sets that can then be joined like regular tables. Here we compute each employee's years at the company in the first CTE, average tenure per department in a second CTE, then join both CTEs to departments to produce a clean summary. CTEs make long queries readable and debuggable.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        WITH tenure AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            salary,
            hire_date,
            DATEDIFF('year', CAST(hire_date AS DATE), CURRENT_DATE) AS years_at_company
        FROM employees ), dept_tenure AS (
        SELECT
            dept_id,
            ROUND(AVG(years_at_company), 1) AS avg_tenure_yrs
        FROM tenure
        GROUP BY dept_id )
        SELECT
            d.dept_name,
            dt.avg_tenure_yrs,
            COUNT(t.emp_id) AS headcount,
            ROUND(AVG(t.salary), 0) AS avg_salary
        FROM tenure AS t
        INNER
        JOIN dept_tenure AS dt ON t.dept_id = dt.dept_id
        INNER
        JOIN departments AS d ON t.dept_id = d.dept_id
        GROUP BY d.dept_name, dt.avg_tenure_yrs
        ORDER BY avg_tenure_yrs DESC;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "CTE + JOIN: Employee Tenure Analysis", "📅")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_tenure = con.execute("""
        WITH tenure AS (
        SELECT
            dept_id,
            DATEDIFF('year', CAST(hire_date AS DATE), CURRENT_DATE) AS yrs
        FROM employees )
        SELECT
            d.dept_name,
            ROUND(AVG(t.yrs),1) AS avg_tenure
        FROM tenure t
        INNER
        JOIN departments d ON t.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY avg_tenure DESC;
    """).df()
    plot_hbar(df_tenure, "avg_tenure", "dept_name",
              title="Average Employee Tenure by Department (CTE + JOIN)",
              xlabel="Average Years at Company", ylabel="Department",
              caption="CTEs (WITH clause) make complex JOINs readable and reusable",
              color="#00bbf9")

    return


@app.cell
def _(HTML, con, display, plot_stacked_bar, render_section_header, render_sql, render_table):
    render_section_header(17, "JOIN + CASE: Salary Band Classification by Country", "Create computed salary bands and cross-tabulate with country", "INNER JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>The CASE WHEN expression lets us create computed classification columns on the fly inside any query — including one with a JOIN. Here we bucket every employee's salary into four bands, then cross-tabulate by country to see the salary distribution in each geographic region.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        SELECT
            c.country_name,
            CASE WHEN e.salary < 60000 THEN '1. < $60K' WHEN e.salary < 90000 THEN '2. $60K–$90K' WHEN e.salary < 120000 THEN '3. $90K–$120K' ELSE '4. $120K+' END AS salary_band,
            COUNT(*) AS headcount,
            ROUND(AVG(e.salary), 0) AS avg_in_band
        FROM employees AS e
        INNER
        JOIN countries AS c ON e.country_code = c.country_code
        GROUP BY c.country_name, salary_band
        ORDER BY c.country_name, salary_band;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "JOIN + CASE: Salary Band Classification by Country", "🏷️")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_bands = con.execute("""
        SELECT
            c.country_name,
            CASE WHEN e.salary < 60000 THEN '< $60K' WHEN e.salary < 90000 THEN '$60K-$90K' WHEN e.salary < 120000 THEN '$90K-$120K' ELSE '$120K+' END AS salary_band,
            COUNT(*) AS headcount
        FROM employees e
        INNER
        JOIN countries c ON e.country_code = c.country_code
        WHERE c.country_name IN ('United States','India','China','Canada','Germany')
        GROUP BY c.country_name, salary_band
        ORDER BY c.country_name, salary_band;
    """).df()
    plot_stacked_bar(df_bands, "country_name", "salary_band", "headcount",
                     title="Salary Band Distribution by Country (JOIN + CASE)",
                     xlabel="Country", ylabel="Headcount",
                     caption="CASE WHEN inside a JOIN query creates computed classification columns")

    return


@app.cell
def _(HTML, con, display, plot_grouped_bar, render_section_header, render_sql, render_table):
    render_section_header(18, "LEFT JOIN: PHD & LAW Graduates — Full Enrichment", "Enrich elite employees with department AND country info; preserve TOP-SECRET", "LEFT JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>We want a full profile for every PHD or LAW employee. Using LEFT JOIN (instead of INNER JOIN) ensures that the 10 TOP-SECRET employees still appear in the result — with NULL for dept_name. Chaining two LEFT JOINs gives us country info too. This is the safest JOIN when you don't want to accidentally lose rows.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        SELECT
            e.emp_id,
            e.emp_name,
            e.salary,
            e.education,
            d.dept_name,
            d.dept_manager,
            d.dept_location,
            c.country_name
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.dept_id = d.dept_id
        LEFT
        JOIN countries AS c ON e.country_code = c.country_code
        WHERE e.education IN ('PHD', 'LAW')
        ORDER BY e.salary DESC
        LIMIT 20;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "LEFT JOIN: PHD & LAW Graduates — Full Enrichment", "🎓💼")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_elite = con.execute("""
        SELECT
            d.dept_name,
            e.education,
            COUNT(*) AS cnt,
            ROUND(AVG(e.salary),0) AS avg_salary
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE e.education IN ('PHD','LAW')
        GROUP BY d.dept_name, e.education
        ORDER BY avg_salary DESC;
    """).df()
    plot_grouped_bar(df_elite, "dept_name", "education", "cnt",
                     title="PHD & LAW Graduates per Department (LEFT JOIN)",
                     xlabel="Department", ylabel="Headcount",
                     caption="LEFT JOIN preserves TOP-SECRET employees (dept_name shows NULL)")

    return


@app.cell
def _(HTML, con, display, plot_line, render_section_header, render_sql, render_table):
    render_section_header(19, "INNER JOIN + Date Functions: Hiring Trend Over Time", "Analyse annual hiring patterns and starting salaries by department", "INNER JOIN")

    # ── Plain English ─────────────────────────────────────────────────────────────
    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>Date functions like EXTRACT() and DATEDIFF() work seamlessly inside JOIN queries. Here we extract the hire year from the hire_date column, join to departments, and GROUP BY year + department to track how many employees were hired each year and at what starting salary. This is a classic time-series reporting query.
    </div>
    """))

    # ── SQL ───────────────────────────────────────────────────────────────────────
    _sql = """
        SELECT EXTRACT(YEAR
        FROM CAST(e.hire_date AS DATE)) AS hire_year, d.dept_name, COUNT(*) AS new_hires, ROUND(AVG(e.salary), 0) AS avg_starting_salary
        FROM employees AS e
        INNER
        JOIN departments AS d ON e.dept_id = d.dept_id
        WHERE EXTRACT(YEAR
        FROM CAST(e.hire_date AS DATE)) >= 2010
        GROUP BY hire_year, d.dept_name
        ORDER BY hire_year, d.dept_name;
    """
    render_sql(_sql, "DuckDB SQL")

    # ── Execute ───────────────────────────────────────────────────────────────────
    _df = con.execute(_sql).df()
    render_table(_df, "INNER JOIN + Date Functions: Hiring Trend Over Time", "📈")

    # ── Plot ──────────────────────────────────────────────────────────────────────
    df_trend = con.execute("""
        SELECT EXTRACT(YEAR
        FROM CAST(hire_date AS DATE)) AS hire_year, COUNT(*) AS new_hires
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE EXTRACT(YEAR
        FROM CAST(hire_date AS DATE)) >= 2010
        GROUP BY hire_year
        ORDER BY hire_year;
    """).df()
    df_trend["hire_year"] = df_trend["hire_year"].astype(int)
    plot_line(df_trend, "hire_year", "new_hires",
              title="Annual New Hires Trend (INNER JOIN + Date Extraction)",
              xlabel="Year", ylabel="New Hires",
              caption="EXTRACT() on dates enables time-series analysis in JOIN queries")

    return


@app.cell
def _(HTML, con, display, plot_hbar, render_section_header, render_sql, render_table):
    render_section_header(20, "JOIN Summary Dashboard", 
                          "Complete overview combining all three tables with all JOIN types", "")


    display(HTML("""
    <div style="background:#0d2137;border-left:4px solid #f5a623;border-radius:0 8px 8px 0;
                padding:12px 18px;margin:8px 0 16px 0;font-family:system-ui;color:#eaeaea;font-size:13px;">
      <b style="color:#f5a623;">💬 What are we doing?</b><br>
      A final comprehensive query that brings everything together: salary statistics per 
      department and country, degree of matching, and data quality flags.
      This shows how a production analytics query combines multiple JOIN types.
    </div>
    """))

    # ── Final comprehensive SQL ───────────────────────────────────────────────────
    sql_final = """
        SELECT
            COALESCE(d.dept_name, '⚠️ NO DEPARTMENT') AS department,
            COALESCE(c.country_name, '⚠️ NO COUNTRY') AS country,
            COUNT(e.emp_id) AS headcount,
            ROUND(AVG(e.salary), 0) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary,
            COUNT(CASE WHEN e.education = 'PHD' THEN 1 END) AS phd_count,
            COUNT(CASE WHEN e.education = 'LAW' THEN 1 END) AS law_count,
            COUNT(CASE WHEN e.gender = 'FEMALE' THEN 1 END) AS female_count
        FROM employees AS e
        LEFT
        JOIN departments AS d ON e.dept_id = d.dept_id
        LEFT
        JOIN countries AS c ON e.country_code = c.country_code
        GROUP BY d.dept_name, c.country_name
        HAVING COUNT(e.emp_id) > 30
        ORDER BY avg_salary DESC
        LIMIT 20;
    """
    render_sql(sql_final, "Comprehensive Multi-JOIN Analytics Query")
    df_final = con.execute(sql_final).df()
    render_table(df_final, "Multi-Table JOIN Dashboard", "🏆", max_rows=30)

    # ── Top-10 highest avg salary combos ─────────────────────────────────────────
    df_top = con.execute("""
        SELECT
            COALESCE(d.dept_name,'NO DEPT') AS dept,
            COALESCE(c.country_name,'NO COUNTRY') AS country,
            COUNT(*) AS headcount,
            ROUND(AVG(e.salary),0) AS avg_salary
        FROM employees e
        LEFT
        JOIN departments d ON e.dept_id = d.dept_id
        LEFT
        JOIN countries c ON e.country_code = c.country_code
        GROUP BY d.dept_name, c.country_name
        HAVING COUNT(*) > 20
        ORDER BY avg_salary DESC
        LIMIT 10;
    """).df()
    df_top["label"] = df_top["dept"] + " / " + df_top["country"]
    plot_hbar(df_top, "avg_salary", "label",
              title="Top 10 Dept×Country Combos by Average Salary",
              xlabel="Average Salary ($)", ylabel="Dept / Country",
              caption="Final dashboard: LEFT JOIN across all 3 tables with HAVING and COALESCE",
              color="#e94560")

    # ── JOIN cheat-sheet ──────────────────────────────────────────────────────────
    display(HTML("""
    <div style="margin:24px 0;border-radius:14px;overflow:hidden;
                box-shadow:0 4px 24px rgba(0,0,0,0.10);border:1px solid #e2e8f0;
                font-family:system-ui,sans-serif;">

      <!-- Header bar -->
      <div style="background:#1e293b;padding:16px 22px;display:flex;align-items:center;gap:12px;">
        <span style="font-size:22px;">📚</span>
        <span style="color:#f8fafc;font-size:17px;font-weight:800;letter-spacing:0.3px;">SQL JOIN Cheat Sheet</span>
        <span style="margin-left:auto;background:#f8fafc;color:#1e293b;border-radius:20px;
                     padding:3px 12px;font-size:11px;font-weight:700;letter-spacing:0.8px;">6 JOIN TYPES</span>
      </div>

      <table style="width:100%;border-collapse:collapse;">
        <thead>
          <tr style="background:#f1f5f9;">
            <th style="padding:10px 14px;text-align:left;color:#475569;font-size:11px;
                       letter-spacing:1px;text-transform:uppercase;
                       border-bottom:2px solid #cbd5e1;white-space:nowrap;">JOIN Type</th>
            <th style="padding:10px 14px;text-align:left;color:#475569;font-size:11px;
                       letter-spacing:1px;text-transform:uppercase;
                       border-bottom:2px solid #cbd5e1;">Keeps</th>
            <th style="padding:10px 14px;text-align:left;color:#475569;font-size:11px;
                       letter-spacing:1px;text-transform:uppercase;
                       border-bottom:2px solid #cbd5e1;">Use When</th>
            <th style="padding:10px 14px;text-align:left;color:#475569;font-size:11px;
                       letter-spacing:1px;text-transform:uppercase;
                       border-bottom:2px solid #cbd5e1;white-space:nowrap;">Cell #</th>
          </tr>
        </thead>
        <tbody>

          <tr style="background:#ffffff;">
            <td style="padding:12px 14px;border-bottom:1px solid #e2e8f0;">
              <span style="display:inline-block;background:#dc2626;color:#fff;
                           border-radius:6px;padding:4px 11px;font-family:monospace;
                           font-size:12px;font-weight:800;">INNER JOIN</span>
            </td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;border-bottom:1px solid #e2e8f0;">Only matched rows from both tables</td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;border-bottom:1px solid #e2e8f0;">You want clean, fully matched data only</td>
            <td style="padding:12px 14px;font-family:monospace;font-size:12px;color:#7c3aed;font-weight:700;border-bottom:1px solid #e2e8f0;white-space:nowrap;">2, 5, 6, 9–12, 14–16, 17, 19</td>
          </tr>

          <tr style="background:#f8fafc;">
            <td style="padding:12px 14px;border-bottom:1px solid #e2e8f0;">
              <span style="display:inline-block;background:#16a34a;color:#fff;
                           border-radius:6px;padding:4px 11px;font-family:monospace;
                           font-size:12px;font-weight:800;">LEFT JOIN</span>
            </td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;border-bottom:1px solid #e2e8f0;">All left rows + matching right rows (NULL if no match)</td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;border-bottom:1px solid #e2e8f0;">Keep every left-table row; fill NULL for unmatched right</td>
            <td style="padding:12px 14px;font-family:monospace;font-size:12px;color:#7c3aed;font-weight:700;border-bottom:1px solid #e2e8f0;white-space:nowrap;">3, 7, 8, 12, 18, 20</td>
          </tr>

          <tr style="background:#ffffff;">
            <td style="padding:12px 14px;border-bottom:1px solid #e2e8f0;">
              <span style="display:inline-block;background:#7c3aed;color:#fff;
                           border-radius:6px;padding:4px 11px;font-family:monospace;
                           font-size:12px;font-weight:800;">RIGHT JOIN</span>
            </td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;border-bottom:1px solid #e2e8f0;">Matching left rows + all right rows (NULL if no match)</td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;border-bottom:1px solid #e2e8f0;">Keep every right-table row; flip of LEFT JOIN</td>
            <td style="padding:12px 14px;font-family:monospace;font-size:12px;color:#7c3aed;font-weight:700;border-bottom:1px solid #e2e8f0;white-space:nowrap;">4</td>
          </tr>

          <tr style="background:#f8fafc;">
            <td style="padding:12px 14px;border-bottom:1px solid #e2e8f0;">
              <span style="display:inline-block;background:#b45309;color:#fff;
                           border-radius:6px;padding:4px 11px;font-family:monospace;
                           font-size:12px;font-weight:800;">FULL OUTER JOIN</span>
            </td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;border-bottom:1px solid #e2e8f0;">Every row from both tables; NULL where no match on either side</td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;border-bottom:1px solid #e2e8f0;">See all unmatched rows from both tables at once</td>
            <td style="padding:12px 14px;font-family:monospace;font-size:12px;color:#7c3aed;font-weight:700;border-bottom:1px solid #e2e8f0;white-space:nowrap;">13</td>
          </tr>

          <tr style="background:#ffffff;">
            <td style="padding:12px 14px;border-bottom:1px solid #e2e8f0;">
              <span style="display:inline-block;background:#0369a1;color:#fff;
                           border-radius:6px;padding:4px 11px;font-family:monospace;
                           font-size:12px;font-weight:800;">ANTI-JOIN</span>
            </td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;border-bottom:1px solid #e2e8f0;">Only left rows that have <em>no</em> match in the right table</td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;border-bottom:1px solid #e2e8f0;">Find orphans / missing references (LEFT JOIN + WHERE IS NULL)</td>
            <td style="padding:12px 14px;font-family:monospace;font-size:12px;color:#7c3aed;font-weight:700;border-bottom:1px solid #e2e8f0;white-space:nowrap;">8</td>
          </tr>

          <tr style="background:#f8fafc;">
            <td style="padding:12px 14px;">
              <span style="display:inline-block;background:#374151;color:#fff;
                           border-radius:6px;padding:4px 11px;font-family:monospace;
                           font-size:12px;font-weight:800;">SELF-JOIN</span>
            </td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;">Pairs or hierarchies within the same table</td>
            <td style="padding:12px 14px;color:#1e293b;font-size:13px;">Org-charts, peer comparisons, consecutive-row analysis</td>
            <td style="padding:12px 14px;font-family:monospace;font-size:12px;color:#7c3aed;font-weight:700;white-space:nowrap;">11</td>
          </tr>

        </tbody>
      </table>
    </div>
    """))

    return


if __name__ == "__main__":
    app.run()
