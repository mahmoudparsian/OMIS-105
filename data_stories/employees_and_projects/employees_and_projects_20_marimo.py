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
    # Employees & Projects Database
    ## A Data Story with DuckDB

    This notebook explores a **company database** containing information about
    employees, departments, projects, work assignments, and dependents.

    We use **DuckDB** as our SQL engine and load all data from CSV files in the `./data/` folder.

    **Tables:**

    | Table | Description |
    |-------|-------------|
    | `employee` | Employee details (name, salary, department, avatar) |
    | `department` | Department info with manager |
    | `project` | Project details and location |
    | `works_on` | Employee-project assignments with hours |
    | `dependent` | Employee dependents (family members) |
    | `dept_locations` | Department office locations |

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup: Import Libraries & Utility Functions
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import sys, os

    # Add current directory so we can import our utility module
    sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))

    from display_utils import (
        show_table, show_sql, show_schema, show_employee_cards,
        plot_bar, plot_pie, plot_donut, plot_grouped_bar,
        plot_scatter, plot_line, plot_heatmap,
        plot_stacked_bar, plot_lollipop, plot_dual_bar
    )

    # Create an in-memory DuckDB connection
    con = duckdb.connect()

    print("Libraries loaded successfully!")
    print(f"DuckDB version: {duckdb.__version__}")
    return (
        con,
        plot_bar,
        plot_donut,
        plot_dual_bar,
        plot_grouped_bar,
        plot_heatmap,
        plot_line,
        plot_lollipop,
        plot_pie,
        plot_scatter,
        plot_stacked_bar,
        show_employee_cards,
        show_schema,
        show_sql,
        show_table,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Load Data from CSV Files

    We read each CSV file from the `./data/` folder and create DuckDB tables.
    """)
    return


@app.cell
def _(con):
    # ─── Create tables from CSV files ───
    tables = ['employee', 'department', 'project',
              'works_on', 'dependent', 'dept_locations']

    for t in tables:
        con.execute(f"""
            CREATE TABLE {t} AS
            SELECT * FROM read_csv_auto('./data/{t}.csv', header=true, nullstr='')
        """)

    print(f"All {len(tables)} tables created successfully from CSV files.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Verify: Tables and Row Counts

    Let's confirm all tables loaded correctly.
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

    Inspect the structure of each table.
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

    Retrieve every employee with their key details and unique avatar.
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
           dno        AS dept_no,
           image_url
    FROM   employee
    ORDER  BY last_name, first_name
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="All Employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 2 — Employee Avatar Gallery

    Each employee has a unique avatar image. Let's display them as cards.
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

    Which departments pay the most on average?
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

    How are projects distributed across departments?
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
               center_text=f"{_df['num_projects'].sum()}\nProjects")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 5 — Total Hours Worked per Employee

    Who are the hardest workers across all projects?
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
        ORDER BY total_hours DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Total Hours Worked per Employee")
    plot_bar(_df, 'employee_name', 'total_hours',
             title='Total Hours Worked by Employee',
             xlabel='Employee', ylabel='Total Hours', rotation=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 6 — Employees and Their Dependents

    Which employees have dependents, and who are they?
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
        ORDER BY num_dependents DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employees with Dependents")
    plot_bar(_df, 'employee_name', 'num_dependents',
             title='Number of Dependents per Employee',
             xlabel='Employee', ylabel='Dependents', rotation=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 7 — Gender Distribution

    What is the gender breakdown across the company?
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

    Is there a relationship between employee age and salary?
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
    show_table(_df, title="Employee Age and Salary")
    plot_scatter(_df, 'age', 'salary',
                 title='Salary vs. Employee Age',
                 xlabel='Age (years)', ylabel='Salary ($)',
                 label_col='employee_name')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 9 — Department Managers

    Who manages each department and what are they paid?
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

    Which projects consume the most employee hours?
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

    Who reports to whom in the organization?
    """)
    return


@app.cell
def _(con, show_sql, show_table):
    _sql = """
    SELECT s.first_name || ' ' || s.last_name AS supervisor,
           e.first_name || ' ' || e.last_name AS subordinate,
           e.salary                           AS subordinate_salary,
           d.dept_name
    FROM   employee   e
    JOIN   employee   s ON e.super_ssn = s.ssn
    JOIN   department d ON e.dno = d.dept_id
    ORDER  BY supervisor, subordinate
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Supervisor → Subordinate Relationships")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 12 — Salary Bands

    Categorize employees into salary ranges.
    """)
    return


@app.cell
def _(con, plot_donut, show_sql, show_table):
    _sql = """
        SELECT CASE WHEN salary < 30000 THEN 'Under $30K' WHEN salary BETWEEN 30000
        AND 39999 THEN '$30K–$39K' WHEN salary BETWEEN 40000
        AND 49999 THEN '$40K–$49K' ELSE '$50K and above' END AS salary_band, COUNT(*) AS num_employees
        FROM employee
        GROUP BY salary_band
        ORDER BY salary_band;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employees by Salary Band")
    plot_donut(_df, 'salary_band', 'num_employees',
               title='Employee Distribution by Salary Band',
               center_text=f"{_df['num_employees'].sum()}\nTotal")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 13 — Departments and Their Locations

    Which departments operate across multiple locations?
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

    Identify employees juggling the most projects simultaneously.
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
        HAVING COUNT(w.project_id) >= 2
        ORDER BY num_projects DESC, total_hours DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employees on Multiple Projects")
    plot_grouped_bar(_df, 'employee_name',
                     ['num_projects', 'avg_hrs_per_proj'],
                     title='Projects & Avg Hours per Employee',
                     ylabel='Count / Hours',
                     legend_labels=['# Projects', 'Avg Hrs/Project'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 15 — Cross-Department Collaboration

    Which employees work on projects belonging to a different department?
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
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Cross-Department Collaboration")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 16 — Total Payroll by Department

    What is each department's total salary cost?
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

    Visualize which employees work on which projects and for how many hours.
    """)
    return


@app.cell
def _(con, plot_heatmap, show_sql, show_table):
    _sql = """
    SELECT e.first_name || ' ' || e.last_name AS employee_name,
           p.project_name,
           w.hours
    FROM   employee e
    JOIN   works_on  w ON e.ssn        = w.ssn
    JOIN   project   p ON w.project_id = p.project_id
    ORDER  BY employee_name, p.project_name
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employee-Project Work Hours")

    pivot_df = _df.pivot_table(index='employee_name', columns='project_name',
                              values='hours', fill_value=0)
    plot_heatmap(pivot_df,
                 title='Hours Worked: Employees × Projects',
                 figsize=(14, 10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 18 — Employees WITHOUT Dependents

    Which employees have no listed dependents?
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
        ORDER BY e.last_name;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employees Without Dependents")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 19 — Work Distribution by Location

    How are project hours distributed across geographic locations?
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

    Rank employees by salary within each department **and** company-wide.
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
    show_table(_df, title="Employee Salary Rankings (Window Functions)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 21 — Employees Earning Above Department Average (Subquery)

    Find employees whose salary exceeds their department's average — a classic **correlated subquery**.
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
        ORDER BY above_avg_by DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employees Earning Above Their Department Average")
    plot_bar(_df, 'employee_name', 'above_avg_by',
             title='How Much Above Department Average?',
             xlabel='Employee', ylabel='$ Above Avg', rotation=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 22 — Running Total of Payroll (Window Function)

    Compute a **running total** of salary ordered by salary ascending — useful for budget analysis.
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
    show_table(_df, title="Running Payroll Total (lowest to highest)")
    plot_line(_df, 'employee_name', 'running_total',
              title='Cumulative Payroll (Running Total)',
              xlabel='Employee', ylabel='Running Total ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 23 — Department with the Most Dependents

    Which department's employees have the most family dependents overall?
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
    ## Query 24 — Project Workload Balance

    Measure how evenly hours are spread across workers on each project
    using **standard deviation** — higher means less balanced.
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
        HAVING COUNT(w.ssn) >= 2
        ORDER BY stddev_hours DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Project Workload Balance (StdDev Analysis)")
    plot_grouped_bar(_df, 'project_name', ['avg_hours', 'stddev_hours'],
                     title='Avg Hours vs. Spread (StdDev) per Project',
                     ylabel='Hours',
                     legend_labels=['Avg Hours', 'StdDev'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 25 — Hours Contribution as % of Department (CTE)

    What percentage of their department's total hours does each employee contribute?
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
        ORDER BY d.dept_name, pct_of_dept DESC;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Employee Hours — % of Department Total")
    plot_bar(_df.head(10), 'employee_name', 'pct_of_dept',
             title='Top 10 Employees by % Contribution to Dept Hours',
             xlabel='Employee', ylabel='% of Department Hours',
             rotation=45, fmt='.1f')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 26 — Gender Pay Gap Analysis

    Compare average salary by gender within each department.
    """)
    return


@app.cell
def _(con, plot_grouped_bar, show_sql, show_table):
    _sql = """
        SELECT
            d.dept_name,
            CASE e.gender WHEN 'M' THEN 'Male' ELSE 'Female' END AS gender,
            COUNT(*) AS COUNT,
            ROUND(AVG(e.salary)) AS avg_salary
        FROM employee e
        JOIN department d ON e.dno = d.dept_id
        GROUP BY d.dept_name, e.gender
        ORDER BY d.dept_name, gender;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Average Salary by Gender per Department")

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

    Combine employees and dependents into a single list using **UNION**.
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
    show_table(_df, title="All People (Employees + Dependents via UNION)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 28 — EXISTS: Departments That Have Projects in Houston

    Use **EXISTS** to find departments with at least one project located in Houston.
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
    ## Query 29 — DENSE_RANK: Top Earners per Department

    Use **DENSE_RANK** to find the top-2 earners in each department.
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
        WHERE rnk <= 2
        ORDER BY dept_name, rnk;
    """
    show_sql(_sql)
    _df = con.execute(_sql).fetchdf()
    show_table(_df, title="Top 2 Earners per Department (DENSE_RANK)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Query 30 — Comprehensive Dashboard: Department Overview

    A single query that summarises each department with multiple metrics.
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
    ## Summary

    In this notebook we explored the **Employees & Projects** database using **DuckDB** and **SQL**.

    **Dataset:** 20 employees · 5 departments · 12 projects · 40 work assignments · 16 dependents

    **SQL Concepts Covered:**

    | Concept | Queries |
    |---------|---------|
    | Basic SELECT / ORDER BY | Q1, Q2 |
    | JOIN (INNER, LEFT) | Q3–Q6, Q9–Q11, Q13–Q19 |
    | Aggregation (COUNT, SUM, AVG, MIN, MAX) | Q3–Q5, Q10, Q16 |
    | GROUP BY / HAVING | Q3–Q7, Q14, Q24 |
    | CASE expressions | Q7, Q12 |
    | Subqueries (scalar & correlated) | Q18, Q21 |
    | Common Table Expressions (CTE) | Q25, Q29 |
    | Window Functions (RANK, DENSE_RANK, SUM OVER) | Q20, Q22, Q29 |
    | Standard Deviation (STDDEV_POP) | Q24 |
    | EXISTS | Q28 |
    | UNION ALL | Q27 |
    | STRING_AGG | Q6, Q13 |
    | Cross-department analysis | Q15, Q30 |

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
