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
    # Employees & Projects Database (100 Employees)
    ## A Data Story with DuckDB

    This notebook explores a **company database** with **100 employees** across
    5 departments, 12 projects, 250+ work assignments, and 80+ dependents.

    We use **DuckDB** as our SQL engine and load all data from CSV files in `./data2/`.

    **Tables:**

    | Table | Description | Approx Rows |
    |-------|-------------|-------------|
    | `employee` | Employee details, salary, department, avatar | 100 |
    | `department` | Department info with manager | 5 |
    | `project` | Project details and location | 12 |
    | `works_on` | Employee-project hours | 256 |
    | `dependent` | Employee family members | 83 |
    | `dept_locations` | Department office locations | 10 |

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup: Import Libraries & Utility Functions

    All display and plotting functions live in **`display_utils.py`** — keeping this notebook clean and focused on SQL.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import sys, os

    sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))

    from display_utils import (
        show_table, show_sql, show_schema, show_employee_cards,
        plot_bar, plot_pie, plot_donut, plot_grouped_bar,
        plot_scatter, plot_line, plot_heatmap,
        plot_stacked_bar, plot_lollipop, plot_dual_bar
    )

    con = duckdb.connect()

    print("Libraries loaded successfully!")
    print(f"DuckDB version: {duckdb.__version__}")
    return (con, plot_bar, plot_donut, plot_dual_bar, plot_grouped_bar, plot_heatmap, plot_line, plot_lollipop, plot_pie, plot_scatter, plot_stacked_bar, show_employee_cards, show_schema, show_sql, show_table)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Load Data from CSV Files

    Read each CSV from `./data2/` and create DuckDB tables.
    """)
    return


@app.cell
def _(con):
    tables = ['employee', 'department', 'project',
              'works_on', 'dependent', 'dept_locations']

    for t in tables:
        con.execute(f"""
            CREATE TABLE {t} AS
            SELECT * FROM read_csv_auto('./data2/{t}.csv', header=true, nullstr='')
        """)

    print(f"All {len(tables)} tables created from CSV files.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Verify: Tables and Row Counts
    """)
    return


@app.cell
def _(con, show_sql, show_table):
    _sql = """
        SELECT
            table_name,
            estimated_size AS row_count
        FROM duckdb_tables()
        ORDER BY table_name;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Tables in Our Database")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Table Schemas

    Inspect the structure (columns and types) of each table.
    """)
    return


@app.cell
def _(con, show_schema):
    for _t in ['employee', 'department', 'project',
              'works_on', 'dependent', 'dept_locations']:
        show_schema(con, _t)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 1 — All Employees

    Retrieve every employee with key details. We have **100 employees** each with a unique avatar.
    """)
    return


@app.cell
def _(con, show_sql, show_table):
    _sql = """
    SELECT first_name,
           last_name,
           gender,
           salary,
           birth_date,
           dno AS dept_no,
           image_url
    FROM   employee
    ORDER  BY last_name, first_name
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="All Employees (100 rows)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 2 — Employee Avatar Gallery

    Display the first 20 employee avatar cards. Each employee has a unique DiceBear persona image.
    """)
    return


@app.cell
def _(con, show_employee_cards, show_sql):
    _sql = """
    SELECT first_name || ' ' || last_name AS employee_name,
           salary,
           image_url
    FROM   employee
    ORDER  BY last_name
    LIMIT  20
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_employee_cards(_df, detail_cols=['salary'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 3 — Average Salary by Department

    Compare salary statistics across all five departments.
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        SELECT
            d.dept_name,
            COUNT(e.ssn) AS num_employees,
            ROUND(AVG(e.salary)) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary
        FROM employee e
        JOIN department d ON e.dno = d.dept_id
        GROUP BY d.dept_name
        ORDER BY avg_salary DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Salary Statistics by Department")
    plot_bar(_df, 'dept_name', 'avg_salary',
             title='Average Salary by Department',
             xlabel='Department', ylabel='Average Salary ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 4 — Projects per Department

    How are the 12 projects distributed?
    """)
    return


@app.cell
def _(con, plot_donut, show_sql, show_table):
    _sql = """
        SELECT
            d.dept_name,
            COUNT(p.project_id) AS num_projects
        FROM department d
        LEFT
        JOIN project p ON d.dept_id = p.dept_id
        GROUP BY d.dept_name
        ORDER BY num_projects DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Projects per Department")
    plot_donut(_df, 'dept_name', 'num_projects',
               title='Distribution of Projects Across Departments',
               center_text=str(_df['num_projects'].sum()) + '\nProjects')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 5 — Top 15 Employees by Total Hours

    Who logs the most hours across all their projects?
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS employee_name,
            COUNT(w.project_id) AS num_projects,
            SUM(w.hours) AS total_hours
        FROM employee e
        JOIN works_on w ON e.ssn = w.ssn
        GROUP BY e.first_name, e.last_name
        ORDER BY total_hours DESC
        LIMIT 15;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Top 15 Employees by Total Hours")
    plot_bar(_df, 'employee_name', 'total_hours',
             title='Top 15 Employees — Total Hours Worked',
             xlabel='Employee', ylabel='Total Hours', rotation=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 6 — Employees and Their Dependents

    List every employee who has at least one dependent, along with the names and relationships.
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS employee_name,
            COUNT(dep.dependent_name) AS num_dependents,
            STRING_AGG(dep.dependent_name || ' (' || dep.relationship || ')', ', ') AS dependents_list
        FROM employee e
        JOIN dependent dep ON e.ssn = dep.ssn
        GROUP BY e.first_name, e.last_name
        ORDER BY num_dependents DESC
        LIMIT 15;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Top 15 Employees by Number of Dependents")
    plot_bar(_df, 'employee_name', 'num_dependents',
             title='Dependents per Employee (Top 15)',
             xlabel='Employee', ylabel='# Dependents', rotation=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 7 — Gender Distribution

    What is the male-to-female ratio in the company?
    """)
    return


@app.cell
def _(con, plot_pie, show_sql, show_table):
    _sql = """
        SELECT
            CASE gender WHEN 'M' THEN 'Male' WHEN 'F' THEN 'Female' END AS gender_label,
            COUNT(*) AS count
        FROM employee
        GROUP BY gender;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Gender Distribution")
    plot_pie(_df, 'gender_label', 'count',
             title='Employee Gender Distribution')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 8 — Salary vs. Age (Scatter)

    Does age correlate with salary?
    """)
    return


@app.cell
def _(con, plot_scatter, show_sql, show_table):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS employee_name,
            DATE_PART('year', AGE(CURRENT_DATE, e.birth_date)) AS age,
            e.salary
        FROM employee e
        ORDER BY age;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employee Age and Salary", max_rows=15)
    plot_scatter(_df, 'age', 'salary',
                 title='Salary vs. Employee Age (100 Employees)',
                 xlabel='Age (years)', ylabel='Salary ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 9 — Department Managers

    Who manages each department, and what is their salary?
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
    SELECT d.dept_name,
           e.first_name || ' ' || e.last_name AS manager_name,
           e.salary                           AS manager_salary,
           d.mgr_start_date
    FROM   department d
    JOIN   employee   e ON d.mgr_ssn = e.ssn
    ORDER  BY e.salary DESC
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Department Managers")
    plot_bar(_df, 'dept_name', 'manager_salary',
             title='Manager Salary by Department',
             xlabel='Department', ylabel='Salary ($)', horizontal=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 10 — Hours Invested per Project

    Which of the 12 projects consume the most employee hours?
    """)
    return


@app.cell
def _(con, plot_lollipop, show_sql, show_table):
    _sql = """
        SELECT
            p.project_name,
            p.project_location,
            COUNT(w.ssn) AS num_workers,
            SUM(w.hours) AS total_hours,
            ROUND(AVG(w.hours), 1) AS avg_hours_per_worker
        FROM project p
        JOIN works_on w ON p.project_id = w.project_id
        GROUP BY p.project_name, p.project_location
        ORDER BY total_hours DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Hours Invested per Project")
    plot_lollipop(_df, 'project_name', 'total_hours',
                  title='Total Hours Invested per Project',
                  ylabel='Total Hours')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 11 — Supervisor-Subordinate Relationships

    Who reports to whom? (Self-join on the employee table.)
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        SELECT
            s.first_name || ' ' || s.last_name AS supervisor,
            COUNT(e.ssn) AS num_subordinates
        FROM employee e
        JOIN employee s ON e.super_ssn = s.ssn
        GROUP BY s.first_name, s.last_name
        ORDER BY num_subordinates DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Supervisors and Their Subordinate Count")
    plot_bar(_df, 'supervisor', 'num_subordinates',
             title='Number of Subordinates per Supervisor',
             xlabel='Supervisor', ylabel='# Subordinates', rotation=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 12 — Salary Bands

    Categorize all 100 employees into salary ranges using **CASE**.
    """)
    return


@app.cell
def _(con, plot_donut, show_sql, show_table):
    _sql = """
        SELECT CASE WHEN salary < 30000 THEN 'Under $30K' WHEN salary BETWEEN 30000
        AND 39999 THEN '$30K - $39K' WHEN salary BETWEEN 40000
        AND 49999 THEN '$40K - $49K' ELSE '$50K and above' END AS salary_band, COUNT(*) AS num_employees
        FROM employee
        GROUP BY salary_band
        ORDER BY salary_band;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employees by Salary Band")
    plot_donut(_df, 'salary_band', 'num_employees',
               title='Employee Distribution by Salary Band',
               center_text=str(_df['num_employees'].sum()) + '\nTotal')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 13 — Departments and Their Locations

    Which departments operate across multiple office locations?
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        SELECT
            d.dept_name,
            COUNT(dl.dept_location) AS num_locations,
            STRING_AGG(dl.dept_location, ', ') AS locations
        FROM department d
        JOIN dept_locations dl ON d.dept_id = dl.dept_id
        GROUP BY d.dept_name
        ORDER BY num_locations DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Department Locations")
    plot_bar(_df, 'dept_name', 'num_locations',
             title='Number of Locations per Department',
             xlabel='Department', ylabel='Locations')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 14 — Employees on Multiple Projects

    Find employees juggling 3 or more projects at once.
    """)
    return


@app.cell
def _(con, plot_grouped_bar, show_sql, show_table):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS employee_name,
            d.dept_name,
            COUNT(w.project_id) AS num_projects,
            SUM(w.hours) AS total_hours,
            ROUND(SUM(w.hours) / COUNT(w.project_id), 1) AS avg_hrs_per_proj
        FROM employee e
        JOIN works_on w ON e.ssn = w.ssn
        JOIN department d ON e.dno = d.dept_id
        GROUP BY e.first_name, e.last_name, d.dept_name
        HAVING COUNT(w.project_id) >= 3
        ORDER BY num_projects DESC, total_hours DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employees on 3+ Projects")
    plot_grouped_bar(_df.head(12), 'employee_name',
                     ['num_projects', 'avg_hrs_per_proj'],
                     title='Projects & Avg Hours (Top 12 Multi-Taskers)',
                     ylabel='Count / Hours',
                     legend_labels=['# Projects', 'Avg Hrs/Project'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 15 — Cross-Department Collaboration

    Employees working on projects that belong to a *different* department than their own.
    """)
    return


@app.cell
def _(con, show_sql, show_table):
    _sql = """
    SELECT e.first_name || ' ' || e.last_name AS employee_name,
           d1.dept_name                       AS home_dept,
           p.project_name,
           d2.dept_name                       AS project_dept,
           w.hours
    FROM   employee   e
    JOIN   works_on   w  ON e.ssn        = w.ssn
    JOIN   project    p  ON w.project_id = p.project_id
    JOIN   department d1 ON e.dno        = d1.dept_id
    JOIN   department d2 ON p.dept_id    = d2.dept_id
    WHERE  e.dno != p.dept_id
    ORDER  BY employee_name
    LIMIT  20
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Cross-Department Collaboration (first 20)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 16 — Total Payroll by Department

    Each department's headcount and total salary cost.
    """)
    return


@app.cell
def _(con, plot_dual_bar, show_sql, show_table):
    _sql = """
        SELECT
            d.dept_name,
            COUNT(e.ssn) AS num_employees,
            SUM(e.salary) AS total_payroll,
            ROUND(AVG(e.salary)) AS avg_salary,
            MAX(e.salary) - MIN(e.salary) AS salary_spread
        FROM department d
        JOIN employee e ON d.dept_id = e.dno
        GROUP BY d.dept_name
        ORDER BY total_payroll DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Department Payroll Summary")
    plot_dual_bar(_df, 'dept_name', 'total_payroll', 'num_employees',
                  title='Payroll vs. Headcount by Department',
                  y1_label='Total Payroll ($)', y2_label='# Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 17 — Employee-Project Heatmap

    Visualize who works on what and for how many hours (top 25 employees by total hours).
    """)
    return


@app.cell
def _(con, plot_heatmap, show_sql, show_table):
    _sql = """
        WITH top_workers AS (
        SELECT ssn
        FROM works_on
        GROUP BY ssn
        ORDER BY SUM(hours) DESC
        LIMIT 25 )
        SELECT
            e.first_name || ' ' || e.last_name AS employee_name,
            p.project_name,
            w.hours
        FROM employee e
        JOIN works_on w ON e.ssn = w.ssn
        JOIN project p ON w.project_id = p.project_id
        WHERE e.ssn IN (
        SELECT ssn
        FROM top_workers)
        ORDER BY employee_name, p.project_name;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Top 25 Workers — Project Hours Detail", max_rows=20)

    pivot_df = _df.pivot_table(index='employee_name', columns='project_name',
                              values='hours', fill_value=0)
    plot_heatmap(pivot_df,
                 title='Hours Worked: Top 25 Employees x Projects',
                 figsize=(14, 10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 18 — Employees WITHOUT Dependents

    Use a **NOT IN** subquery to find employees with no dependents.
    """)
    return


@app.cell
def _(con, show_sql, show_table):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS employee_name,
            e.salary,
            d.dept_name
        FROM employee e
        JOIN department d ON e.dno = d.dept_id
        WHERE e.ssn NOT IN (
        SELECT ssn
        FROM dependent)
        ORDER BY e.salary DESC
        LIMIT 15;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employees Without Dependents (Top 15 by Salary)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 19 — Work Hours by Project Location

    Aggregate hours across the different project locations.
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        SELECT
            p.project_location AS location,
            COUNT(DISTINCT p.project_id) AS num_projects,
            COUNT(DISTINCT w.ssn) AS num_workers,
            SUM(w.hours) AS total_hours
        FROM project p
        JOIN works_on w ON p.project_id = w.project_id
        GROUP BY p.project_location
        ORDER BY total_hours DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Work Distribution by Location")
    plot_bar(_df, 'location', 'total_hours',
             title='Total Work Hours by Project Location',
             xlabel='Location', ylabel='Total Hours')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 20 — Salary Ranking with Window Functions

    Use **RANK()** to rank employees by salary within each department and company-wide.
    """)
    return


@app.cell
def _(con, show_sql, show_table):
    _sql = """
        SELECT
            d.dept_name,
            e.first_name || ' ' || e.last_name AS employee_name,
            e.salary,
            RANK() OVER (PARTITION BY d.dept_name
        ORDER BY e.salary DESC) AS dept_rank, RANK() OVER (
        ORDER BY e.salary DESC) AS company_rank
        FROM employee e
        JOIN department d ON e.dno = d.dept_id
        ORDER BY d.dept_name, dept_rank;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employee Salary Rankings (Window Functions)", max_rows=25)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 21 — Employees Earning Above Department Average

    A **subquery** to find employees whose salary exceeds their department's average.
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        SELECT
            e.first_name || ' ' || e.last_name AS employee_name,
            d.dept_name,
            e.salary,
            dept_avg.avg_sal AS dept_avg_salary,
            e.salary - dept_avg.avg_sal AS above_avg_by
        FROM employee e
        JOIN department d ON e.dno = d.dept_id
        JOIN (
        SELECT
            dno,
            ROUND(AVG(salary)) AS avg_sal
        FROM employee
        GROUP BY dno) dept_avg ON e.dno = dept_avg.dno
        WHERE e.salary > dept_avg.avg_sal
        ORDER BY above_avg_by DESC
        LIMIT 15;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Top 15 Employees Above Their Dept Average")
    plot_bar(_df, 'employee_name', 'above_avg_by',
             title='How Much Above Department Average? (Top 15)',
             xlabel='Employee', ylabel='$ Above Avg', rotation=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 22 — Running Total of Payroll

    Use a **window function** to compute a cumulative salary total, ordered from lowest to highest.
    """)
    return


@app.cell
def _(con, plot_line, show_sql, show_table):
    _sql = """
        SELECT
            first_name || ' ' || last_name AS employee_name,
            salary,
            SUM(salary) OVER (
        ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW) AS running_total
        FROM employee
        ORDER BY salary;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Running Payroll Total", max_rows=15)
    plot_line(_df, 'employee_name', 'running_total',
              title='Cumulative Payroll (Running Total)',
              xlabel='Employee (by salary)', ylabel='Running Total ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 23 — Department with the Most Dependents

    Join three tables to see which department's employees have the most family dependents.
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        SELECT
            d.dept_name,
            COUNT(DISTINCT e.ssn) AS employees_with_deps,
            COUNT(dep.dependent_name) AS total_dependents
        FROM department d
        JOIN employee e ON d.dept_id = e.dno
        JOIN dependent dep ON e.ssn = dep.ssn
        GROUP BY d.dept_name
        ORDER BY total_dependents DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Dependents by Department")
    plot_bar(_df, 'dept_name', 'total_dependents',
             title='Total Dependents by Department',
             xlabel='Department', ylabel='# Dependents')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 24 — Project Workload Balance (StdDev)

    Use **STDDEV_POP** to measure how evenly hours are distributed among workers per project. Higher = less balanced.
    """)
    return


@app.cell
def _(con, plot_grouped_bar, show_sql, show_table):
    _sql = """
        SELECT
            p.project_name,
            COUNT(w.ssn) AS num_workers,
            SUM(w.hours) AS total_hours,
            ROUND(AVG(w.hours), 1) AS avg_hours,
            ROUND(STDDEV_POP(w.hours), 1) AS stddev_hours
        FROM project p
        JOIN works_on w ON p.project_id = w.project_id
        GROUP BY p.project_name
        HAVING COUNT(w.ssn) >= 3
        ORDER BY stddev_hours DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Project Workload Balance")
    plot_grouped_bar(_df, 'project_name', ['avg_hours', 'stddev_hours'],
                     title='Avg Hours vs. StdDev per Project',
                     ylabel='Hours',
                     legend_labels=['Avg Hours', 'StdDev (Spread)'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 25 — Hours as % of Department Total (CTE)

    Use a **Common Table Expression** to compute each employee's share of their department's total work hours.
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        WITH dept_totals AS (
        SELECT
            e.dno,
            SUM(w.hours) AS dept_total_hours
        FROM employee e
        JOIN works_on w ON e.ssn = w.ssn
        GROUP BY e.dno )
        SELECT
            e.first_name || ' ' || e.last_name AS employee_name,
            d.dept_name,
            SUM(w.hours) AS employee_hours,
            dt.dept_total_hours,
            ROUND(100.0 * SUM(w.hours) / dt.dept_total_hours, 1) AS pct_of_dept
        FROM employee e
        JOIN works_on w ON e.ssn = w.ssn
        JOIN department d ON e.dno = d.dept_id
        JOIN dept_totals dt ON e.dno = dt.dno
        GROUP BY e.first_name, e.last_name, d.dept_name, dt.dept_total_hours
        ORDER BY pct_of_dept DESC
        LIMIT 15;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Top 15 — % Contribution to Department Hours")
    plot_bar(_df, 'employee_name', 'pct_of_dept',
             title='Top 15 by % Contribution to Dept Hours',
             xlabel='Employee', ylabel='% of Department Hours',
             rotation=45, fmt='.1f')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 26 — Gender Pay Comparison by Department

    Compare average salaries by gender within each department.
    """)
    return


@app.cell
def _(con, plot_grouped_bar, show_sql, show_table):
    _sql = """
        SELECT
            d.dept_name,
            CASE e.gender WHEN 'M' THEN 'Male' ELSE 'Female' END AS gender,
            COUNT(*) AS count,
            ROUND(AVG(e.salary)) AS avg_salary
        FROM employee e
        JOIN department d ON e.dno = d.dept_id
        GROUP BY d.dept_name, e.gender
        ORDER BY d.dept_name, gender;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Avg Salary by Gender per Department")

    pivot = _df.pivot_table(index='dept_name', columns='gender',
                           values='avg_salary', fill_value=0).reset_index()
    cols = [c for c in pivot.columns if c != 'dept_name']
    plot_grouped_bar(pivot, 'dept_name', cols,
                     title='Average Salary: Male vs. Female by Department',
                     ylabel='Average Salary ($)',
                     legend_labels=cols)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 27 — UNION: All People in the Database

    Combine employees and dependents into one list using **UNION ALL**.
    """)
    return


@app.cell
def _(con, show_sql, show_table):
    _sql = """
    SELECT first_name || ' ' || last_name AS full_name,
           'Employee'                     AS role,
           gender,
           birth_date
    FROM   employee

    UNION ALL

    SELECT dependent_name                 AS full_name,
           relationship                   AS role,
           gender,
           birth_date
    FROM   dependent
    ORDER  BY full_name
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="All People (Employees + Dependents via UNION)", max_rows=20)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 28 — EXISTS: Departments with Houston Projects

    Use **EXISTS** (a correlated subquery) to find departments that have at least one project in Houston.
    """)
    return


@app.cell
def _(con, show_sql, show_table):
    _sql = """
        SELECT
            d.dept_name,
            d.dept_id
        FROM department d
        WHERE EXISTS (
        SELECT 1
        FROM project p
        WHERE p.dept_id = d.dept_id
        AND p.project_location = 'Houston' )
        ORDER BY d.dept_name;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Departments with Projects in Houston (EXISTS)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 29 — DENSE_RANK: Top 3 Earners per Department

    Use a **CTE + DENSE_RANK** window function to find the top-3 highest-paid employees in each department.
    """)
    return


@app.cell
def _(con, show_sql, show_table):
    _sql = """
        WITH ranked AS (
        SELECT
            d.dept_name,
            e.first_name || ' ' || e.last_name AS employee_name,
            e.salary,
            DENSE_RANK() OVER (PARTITION BY d.dept_name
        ORDER BY e.salary DESC) AS rnk
        FROM employee e
        JOIN department d ON e.dno = d.dept_id )
        SELECT
            dept_name,
            employee_name,
            salary,
            rnk AS RANK
        FROM ranked
        WHERE rnk <= 3
        ORDER BY dept_name, rnk;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Top 3 Earners per Department (DENSE_RANK)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 30 — Salary Percentiles (NTILE)

    Use **NTILE(4)** to divide employees into salary quartiles.
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        SELECT
            CASE quartile WHEN 1 THEN 'Q1 (Bottom 25%)' WHEN 2 THEN 'Q2 (25-50%)' WHEN 3 THEN 'Q3 (50-75%)' WHEN 4 THEN 'Q4 (Top 25%)' END AS quartile_label,
            COUNT(*) AS num_employees,
            MIN(salary) AS min_salary,
            ROUND(AVG(salary)) AS avg_salary,
            MAX(salary) AS max_salary
        FROM (
        SELECT
            salary,
            NTILE(4) OVER (
        ORDER BY salary) AS quartile
        FROM employee ) sub
        GROUP BY quartile
        ORDER BY quartile;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Salary Quartiles (NTILE)")
    plot_bar(_df, 'quartile_label', 'avg_salary',
             title='Average Salary by Quartile',
             xlabel='Quartile', ylabel='Avg Salary ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 31 — Dependent Relationship Breakdown

    Count dependents by relationship type (Spouse, Son, Daughter).
    """)
    return


@app.cell
def _(con, plot_pie, show_sql, show_table):
    _sql = """
        SELECT
            relationship,
            COUNT(*) AS count,
            CASE gender WHEN 'M' THEN 'Male' ELSE 'Female' END AS dep_gender
        FROM dependent
        GROUP BY relationship, gender
        ORDER BY relationship, dep_gender;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Dependent Breakdown by Relationship & Gender")

    agg = _df.groupby('relationship')['count'].sum().reset_index()
    plot_pie(agg, 'relationship', 'count',
             title='Dependent Relationship Distribution')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 32 — Employees with No Project Assignments

    Use a **LEFT JOIN** to find employees who have not been assigned to any project.
    """)
    return


@app.cell
def _(con, show_sql, show_table):
    _sql = """
    SELECT e.first_name || ' ' || e.last_name AS employee_name,
           d.dept_name,
           e.salary
    FROM   employee   e
    LEFT   JOIN works_on w ON e.ssn = w.ssn
    JOIN   department  d ON e.dno = d.dept_id
    WHERE  w.ssn IS NULL
    ORDER  BY e.salary DESC
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employees with No Project Assignments")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 33 — Avg Salary: Employees WITH vs. WITHOUT Dependents

    Do employees with dependents earn more on average?
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        SELECT
            CASE WHEN d.ssn IS NOT NULL THEN 'Has Dependents' ELSE 'No Dependents' END AS category,
            COUNT(DISTINCT e.ssn) AS num_employees,
            ROUND(AVG(e.salary)) AS avg_salary
        FROM employee e
        LEFT
        JOIN (
        SELECT DISTINCT ssn
        FROM dependent) d ON e.ssn = d.ssn
        GROUP BY category;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Salary: Dependents vs. No Dependents")
    plot_bar(_df, 'category', 'avg_salary',
             title='Avg Salary: With vs. Without Dependents',
             xlabel='', ylabel='Average Salary ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 34 — Department Dashboard (Comprehensive Join)

    A single query aggregating employees, projects, payroll, hours, dependents, and locations per department.
    """)
    return


@app.cell
def _(con, plot_stacked_bar, show_sql, show_table):
    _sql = """
        SELECT
            d.dept_name,
            COUNT(DISTINCT e.ssn) AS employees,
            COUNT(DISTINCT p.project_id) AS projects,
            SUM(DISTINCT e.salary) AS total_payroll,
            COALESCE(SUM(w.hours), 0) AS total_project_hours,
            COUNT(DISTINCT dep.dependent_name) AS dependents,
            COUNT(DISTINCT dl.dept_location) AS locations
        FROM department d
        LEFT
        JOIN employee e ON d.dept_id = e.dno
        LEFT
        JOIN project p ON d.dept_id = p.dept_id
        LEFT
        JOIN works_on w ON e.ssn = w.ssn
        AND w.project_id = p.project_id
        LEFT
        JOIN dependent dep ON e.ssn = dep.ssn
        LEFT
        JOIN dept_locations dl ON d.dept_id = dl.dept_id
        GROUP BY d.dept_name
        ORDER BY employees DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Department Dashboard — All Key Metrics")
    plot_stacked_bar(_df, 'dept_name', ['employees', 'projects', 'locations'],
                     title='Department Composition',
                     ylabel='Count',
                     legend_labels=['Employees', 'Projects', 'Locations'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 35 — Salary Histogram (Binned Distribution)

    Bin salaries into $5K ranges to visualize the distribution across 100 employees.
    """)
    return


@app.cell
def _(con, plot_bar, show_sql, show_table):
    _sql = """
        SELECT
            FLOOR(salary / 5000) * 5000 AS bin_start,
            FLOOR(salary / 5000) * 5000 + 4999 AS bin_end,
            '$' || CAST(FLOOR(salary / 5000) * 5 AS INT) || 'K-$' || CAST(FLOOR(salary / 5000) * 5 + 4 AS INT) || 'K' AS salary_range,
            COUNT(*) AS num_employees
        FROM employee
        GROUP BY bin_start, bin_end, salary_range
        ORDER BY bin_start;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Salary Distribution (Histogram Bins)")
    plot_bar(_df, 'salary_range', 'num_employees',
             title='Salary Distribution Across 100 Employees',
             xlabel='Salary Range', ylabel='# Employees',
             color='#3498db')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    We explored the **Employees & Projects** database (100 employees) using **DuckDB** and **SQL**.

    **Dataset:** 100 employees · 5 departments · 12 projects · 256 work assignments · 83 dependents

    **SQL Concepts Covered:**

    | Concept | Queries |
    |---------|---------|
    | Basic SELECT / ORDER BY | Q1, Q2 |
    | JOIN (INNER, LEFT) | Q3–Q6, Q9–Q11, Q13–Q19, Q23, Q32–Q34 |
    | Aggregation (COUNT, SUM, AVG, MIN, MAX) | Q3–Q5, Q10, Q16, Q23, Q30, Q35 |
    | GROUP BY / HAVING | Q3–Q7, Q14, Q24, Q31 |
    | CASE expressions | Q7, Q12, Q33 |
    | Subqueries (scalar, correlated, NOT IN) | Q18, Q21, Q33 |
    | Common Table Expressions (CTE) | Q17, Q25, Q29 |
    | Window Functions (RANK, DENSE_RANK, NTILE, SUM OVER) | Q20, Q22, Q29, Q30 |
    | STDDEV_POP (statistical) | Q24 |
    | EXISTS | Q28 |
    | UNION ALL | Q27 |
    | STRING_AGG | Q6, Q13 |
    | FLOOR / binning | Q35 |
    | Cross-department analysis | Q15, Q34 |

    ---
    *OMIS 105 — Data Stories with SQL & DuckDB*
    """)
    return


@app.cell
def _(con):
    con.close()
    print("DuckDB connection closed. Notebook complete!")
    return


if __name__ == "__main__":
    app.run()
