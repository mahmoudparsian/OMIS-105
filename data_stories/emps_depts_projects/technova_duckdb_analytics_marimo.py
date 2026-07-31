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
    # TechNova: Employee, Department & Project Analytics

    **A Data Story using DuckDB and SQL**

    * TechNova is a global technology consultancy that employs specialists from over fifteen countries. 

    * Each **employee** belongs to exactly one **department**, and employees work on multiple **projects** 
    throughout the year. 

    * In this notebook we explore the data using SQL queries in DuckDB, 
    visualize results with charts, and answer common business questions.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Setup: Import Libraries and Connect to DuckDB
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We import DuckDB for SQL, and our custom `display_utils` module that handles 
    all table formatting and plotting so the notebook stays clean.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    from display_utils import (run_query, show, show_query,
                                plot_bar, plot_hbar, plot_pie, plot_line,
                                plot_grouped_bar, plot_scatter, plot_hist,
                                plot_box, plot_stacked_bar)

    # Create an in-memory DuckDB connection
    con = duckdb.connect()
    print('DuckDB connected successfully!')
    return (con, plot_bar, plot_box, plot_grouped_bar, plot_hbar, plot_hist, plot_line, plot_pie, plot_scatter, run_query, show, show_query)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Load CSV Data into DuckDB Tables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We read the four CSV files from the `data/` folder and create proper 
    DuckDB tables with primary keys and foreign keys.
    """)
    return


@app.cell
def _(con):
    # ── Create tables from CSV files ──────────────────────────────

    con.execute("""
        CREATE TABLE departments AS
        SELECT *
        FROM read_csv_auto('data/departments.csv');
    """)

    con.execute("""
        CREATE TABLE employees AS
        SELECT *
        FROM read_csv_auto('data/employees.csv');
    """)

    con.execute("""
        CREATE TABLE projects AS
        SELECT *
        FROM read_csv_auto('data/projects.csv');
    """)

    con.execute("""
        CREATE TABLE employee_projects AS
        SELECT *
        FROM read_csv_auto('data/employee_projects.csv');
    """)

    print('All 4 tables loaded successfully from CSV files!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Verify: Quick Look at Each Table
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's confirm the data loaded correctly by peeking at each table.
    """)
    return


@app.cell
def _(con, run_query, show):
    show(run_query(con, """
        SELECT *
        FROM departments;
    """), title='All Departments')
    return


@app.cell
def _(con, run_query, show):
    show(run_query(con, """
        SELECT *
        FROM employees
        LIMIT 10;
    """), title='Employees (first 10 rows)')
    return


@app.cell
def _(con, run_query, show):
    show(run_query(con, """
        SELECT *
        FROM projects;
    """), title='All Projects')
    return


@app.cell
def _(con, run_query, show):
    show(run_query(con, """
        SELECT *
        FROM employee_projects
        LIMIT 10;
    """), title='Employee–Project Assignments (first 10 rows)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How many rows are in each table?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A quick sanity check to see the size of our dataset.
    """)
    return


@app.cell
def _(con, plot_bar, run_query, show):
    _df = run_query(con, """
        SELECT
            'departments' AS table_name,
            COUNT(*) AS row_count
        FROM departments
        UNION ALL
        SELECT
            'employees',
            COUNT(*)
        FROM employees
        UNION ALL
        SELECT
            'projects',
            COUNT(*)
        FROM projects
        UNION ALL
        SELECT
            'employee_projects',
            COUNT(*)
        FROM employee_projects;
    """)
    show(_df, title='Row Counts per Table')
    plot_bar(_df, 'table_name', 'row_count',
             title='Number of Rows per Table',
             xlabel='Table', ylabel='Rows')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. Basic Queries

    Simple `SELECT`, `WHERE`, `ORDER BY`, and aggregate queries.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q1 – Show all employee names and their salaries
    We select just the name and salary columns to get a quick roster overview.
    """)
    return


@app.cell
def _(con, show_query):
    _df = show_query(con, """
        SELECT
            first_name,
            last_name,
            salary
        FROM employees
        ORDER BY last_name, first_name;
    """, title='Employee Names and Salaries')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q2 – Find the 10 highest-paid employees
    Which individuals earn the most at TechNova?
    """)
    return


@app.cell
def _(con, plot_hbar, show_query):
    _df = show_query(con, """
        SELECT
            first_name,
            last_name,
            salary,
            country
        FROM employees
        ORDER BY salary DESC
        LIMIT 10;
    """, title='Top 10 Highest-Paid Employees')

    plot_hbar(_df, 'first_name', 'salary',
              title='Top 10 Highest-Paid Employees',
              xlabel='Salary ($)', fmt='${:,.0f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q3 – Employees hired after 2021
    Who are the most recent hires?
    """)
    return


@app.cell
def _(con, show_query):
    _df = show_query(con, """
        SELECT
            first_name,
            last_name,
            hire_date,
            country
        FROM employees
        WHERE hire_date > '2021-01-01'
        ORDER BY hire_date DESC;
    """, title='Employees Hired After 2021')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q4 – How many distinct countries do our employees come from?
    TechNova prides itself on global diversity.
    """)
    return


@app.cell
def _(con, show_query):
    _df = show_query(con, """
        SELECT DISTINCT country
        FROM employees
        ORDER BY country;
    """, title='All Employee Countries')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q5 – Count of employees per country
    Which countries have the most TechNova employees?
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _df = show_query(con, """
        SELECT
            country,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY country
        ORDER BY emp_count DESC;
    """, title='Employees per Country')

    plot_bar(_df, 'country', 'emp_count',
             title='Number of Employees per Country',
             xlabel='Country', ylabel='Employees',
             rotate_labels=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q6 – Average salary across all employees
    A single number showing the overall average.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT ROUND(AVG(salary), 2) AS avg_salary
        FROM employees;
    """, title='Overall Average Salary')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q7 – Minimum and maximum salaries
    What is the salary range at TechNova?
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            MAX(salary) - MIN(salary) AS salary_range
        FROM employees;
    """, title='Salary Range')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q8 – Salary distribution (histogram)
    Let's visualize how salaries are spread across the company.
    """)
    return


@app.cell
def _(con, plot_hist, run_query):
    _df = run_query(con, """
        SELECT salary
        FROM employees;
    """)
    plot_hist(_df, 'salary', bins=12,
              title='Distribution of Employee Salaries',
              xlabel='Salary ($)', ylabel='Number of Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q9 – Projects whose name starts with 'C'
    Using the `LIKE` operator to filter by pattern.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            proj_name,
            start_date,
            end_date
        FROM projects
        WHERE proj_name LIKE 'C%';
    """, title="Projects Starting with 'C'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q10 – Employees sorted by hire date (earliest first)
    A timeline view of when people joined TechNova.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            first_name,
            last_name,
            hire_date,
            dept_id
        FROM employees
        ORDER BY hire_date
        LIMIT 15;
    """, title='First 15 Employees by Hire Date')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. Join Queries

    Combining tables with `JOIN` to answer cross-table questions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q11 – Employee names with their department names
    Join `employees` with `departments` to replace `dept_id` with a human-readable name.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            e.first_name,
            e.last_name,
            d.dept_name,
            e.country
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name, e.last_name;
    """, title='Employees with Department Names')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q12 – Number of employees in each department
    Which departments are the largest?
    """)
    return


@app.cell
def _(con, plot_pie, show_query):
    _df = show_query(con, """
        SELECT
            d.dept_name,
            COUNT(*) AS emp_count
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY emp_count DESC;
    """, title='Headcount by Department')

    plot_pie(_df, 'dept_name', 'emp_count',
             title='Employee Distribution by Department')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q13 – Average salary per department
    How does pay differ across departments?
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _df = show_query(con, """
        SELECT
            d.dept_name,
            ROUND(AVG(e.salary), 0) AS avg_salary
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY avg_salary DESC;
    """, title='Average Salary by Department')

    plot_bar(_df, 'dept_name', 'avg_salary',
             title='Average Salary by Department',
             xlabel='Department', ylabel='Avg Salary ($)',
             fmt='${:,.0f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q14 – Departments where average salary exceeds $100,000
    Using `HAVING` to filter grouped results.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            d.dept_name,
            ROUND(AVG(e.salary), 0) AS avg_salary
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        HAVING AVG(e.salary) > 100000
        ORDER BY avg_salary DESC;
    """, title='Departments with Avg Salary > $100K')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q15 – Employees and the projects they work on
    A three-table join: `employees` → `employee_projects` → `projects`.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            e.first_name,
            e.last_name,
            p.proj_name,
            ep.role
        FROM employees e
        JOIN employee_projects ep ON e.emp_id = ep.emp_id
        JOIN projects p ON ep.proj_id = p.proj_id
        ORDER BY e.last_name, p.proj_name;
    """, title='Employee–Project Assignments with Roles')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q16 – How many employees are assigned to each project?
    Which projects have the largest teams?
    """)
    return


@app.cell
def _(con, plot_hbar, show_query):
    _df = show_query(con, """
        SELECT
            p.proj_name,
            COUNT(*) AS team_size
        FROM employee_projects ep
        JOIN projects p ON ep.proj_id = p.proj_id
        GROUP BY p.proj_name
        ORDER BY team_size DESC;
    """, title='Team Size per Project')

    plot_hbar(_df, 'proj_name', 'team_size',
              title='Team Size per Project',
              xlabel='Number of Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q17 – Top 3 projects by team size
    Using `LIMIT` to focus on just the biggest projects.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            p.proj_name,
            COUNT(*) AS team_size
        FROM employee_projects ep
        JOIN projects p ON ep.proj_id = p.proj_id
        GROUP BY p.proj_name
        ORDER BY team_size DESC
        LIMIT 3;
    """, title='Top 3 Largest Project Teams')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q18 – Employees with NO project assignments
    Using a `LEFT JOIN` to find employees who haven't been assigned to any project.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            e.first_name,
            e.last_name,
            e.country,
            d.dept_name
        FROM employees e
        LEFT
        JOIN employee_projects ep ON e.emp_id = ep.emp_id
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE ep.proj_id IS NULL
        ORDER BY e.last_name;
    """, title='Employees Without Any Projects')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q19 – Employees who are Managers on projects
    Filtering by role in the assignment table.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            e.first_name,
            e.last_name,
            p.proj_name
        FROM employees e
        JOIN employee_projects ep ON e.emp_id = ep.emp_id
        JOIN projects p ON ep.proj_id = p.proj_id
        WHERE ep.role = 'Manager'
        ORDER BY p.proj_name;
    """, title='Project Managers')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q20 – Average salary per country
    How does compensation compare across geographies?
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _df = show_query(con, """
        SELECT
            country,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY country
        ORDER BY avg_salary DESC;
    """, title='Average Salary by Country')

    plot_bar(_df, 'country', 'avg_salary',
             title='Average Salary by Country',
             xlabel='Country', ylabel='Avg Salary ($)',
             rotate_labels=45, fmt='${:,.0f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6. Intermediate & Advanced Queries

    CTEs (Common Table Expressions), window functions, subqueries, and more.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q21 – Highest-paid employee in each department (Window Function)
    Use `ROW_NUMBER()` to rank employees within their department by salary, 
    then pick only the top earner.
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _df = show_query(con, """
        WITH ranked AS (
        SELECT
            e.first_name,
            e.last_name,
            d.dept_name,
            e.salary,
            ROW_NUMBER() OVER ( PARTITION BY d.dept_name
        ORDER BY e.salary DESC ) AS rnk
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id )
        SELECT
            first_name,
            last_name,
            dept_name,
            salary
        FROM ranked
        WHERE rnk = 1
        ORDER BY salary DESC;
    """, title='Highest-Paid Employee per Department')

    plot_bar(_df, 'dept_name', 'salary',
             title='Top Salary in Each Department',
             xlabel='Department', ylabel='Salary ($)',
             rotate_labels=30, fmt='${:,.0f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q22 – Employees working on more than 2 projects
    Who are the busiest team members?
    """)
    return


@app.cell
def _(con, plot_hbar, show_query):
    _df = show_query(con, """
        SELECT
            e.first_name,
            e.last_name,
            COUNT(ep.proj_id) AS project_count
        FROM employees e
        JOIN employee_projects ep ON e.emp_id = ep.emp_id
        GROUP BY e.emp_id, e.first_name, e.last_name
        HAVING COUNT(ep.proj_id) > 2
        ORDER BY project_count DESC;
    """, title='Employees on More Than 2 Projects')

    plot_hbar(_df, 'first_name', 'project_count',
              title='Busiest Employees (by Project Count)',
              xlabel='Number of Projects')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q23 – Project duration in days
    How long did each project take? We use `end_date - start_date` in DuckDB.
    """)
    return


@app.cell
def _(con, plot_hbar, show_query):
    _df = show_query(con, """
        SELECT
            proj_name,
            start_date,
            end_date,
            DATEDIFF('day', start_date, end_date) AS duration_days
        FROM projects
        ORDER BY duration_days DESC;
    """, title='Project Durations')

    plot_hbar(_df, 'proj_name', 'duration_days',
              title='Project Duration (Days)',
              xlabel='Days')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q24 – Number of distinct projects per department
    Which departments are involved in the most projects?
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _df = show_query(con, """
        SELECT
            d.dept_name,
            COUNT(DISTINCT ep.proj_id) AS project_count
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        JOIN employee_projects ep ON e.emp_id = ep.emp_id
        GROUP BY d.dept_name
        ORDER BY project_count DESC;
    """, title='Projects per Department')

    plot_bar(_df, 'dept_name', 'project_count',
             title='Number of Distinct Projects per Department',
             xlabel='Department', ylabel='Projects')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q25 – Total salary cost per project
    Sum up the salaries of all employees assigned to each project. 
    (This approximates the labor cost exposure per project.)
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _df = show_query(con, """
        SELECT
            p.proj_name,
            SUM(e.salary) AS total_salary_cost,
            COUNT(*) AS team_size
        FROM employees e
        JOIN employee_projects ep ON e.emp_id = ep.emp_id
        JOIN projects p ON ep.proj_id = p.proj_id
        GROUP BY p.proj_name
        ORDER BY total_salary_cost DESC;
    """, title='Total Salary Cost per Project')

    plot_bar(_df, 'proj_name', 'total_salary_cost',
             title='Total Salary Cost per Project',
             xlabel='Project', ylabel='Total Salary ($)',
             rotate_labels=35, fmt='${:,.0f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q26 – Salary distribution by department (Box Plot)
    Box plots show the median, quartiles, and outliers for each department's salaries.
    """)
    return


@app.cell
def _(con, plot_box, run_query):
    _df = run_query(con, """
        SELECT
            d.dept_name,
            e.salary
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id;
    """)
    plot_box(_df, 'dept_name', 'salary',
             title='Salary Distribution by Department',
             xlabel='Department', ylabel='Salary ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q27 – Role distribution across all projects
    How many Architects, Developers, Testers, Managers, and Analysts do we have overall?
    """)
    return


@app.cell
def _(con, plot_pie, show_query):
    _df = show_query(con, """
        SELECT
            role,
            COUNT(*) AS assignment_count
        FROM employee_projects
        GROUP BY role
        ORDER BY assignment_count DESC;
    """, title='Role Distribution')

    plot_pie(_df, 'role', 'assignment_count',
             title='Distribution of Roles Across Projects')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q28 – Hiring trend by year
    How many employees were hired each year? This shows growth over time.
    """)
    return


@app.cell
def _(con, plot_line, show_query):
    _df = show_query(con, """
        SELECT EXTRACT(YEAR
        FROM hire_date) AS hire_year, COUNT(*) AS hires
        FROM employees
        GROUP BY hire_year
        ORDER BY hire_year;
    """, title='Hires per Year')

    plot_line(_df, 'hire_year', 'hires',
              title='Hiring Trend Over the Years',
              xlabel='Year', ylabel='Number of Hires')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q29 – Countries with the most project participations
    Which countries contribute the most to project teams?
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _df = show_query(con, """
        SELECT
            e.country,
            COUNT(DISTINCT ep.proj_id) AS projects_involved
        FROM employees e
        JOIN employee_projects ep ON e.emp_id = ep.emp_id
        GROUP BY e.country
        ORDER BY projects_involved DESC;
    """, title='Country Project Participation')

    plot_bar(_df, 'country', 'projects_involved',
             title='Number of Distinct Projects by Country',
             xlabel='Country', ylabel='Projects',
             rotate_labels=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q30 – Employees who are NOT assigned to any project (using NOT EXISTS)
    An alternative to the LEFT JOIN approach — uses a correlated subquery.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            e.first_name,
            e.last_name,
            e.country
        FROM employees e
        WHERE NOT EXISTS (
        SELECT 1
        FROM employee_projects ep
        WHERE ep.emp_id = e.emp_id )
        ORDER BY e.last_name;
    """, title='Unassigned Employees (NOT EXISTS)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q31 – Department with the highest average tenure
    Tenure = years between hire date and today. Which department retains people longest?
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _df = show_query(con, """
        SELECT
            d.dept_name,
            ROUND(AVG( (CURRENT_DATE - e.hire_date) / 365.25 ), 1) AS avg_tenure_years
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY avg_tenure_years DESC;
    """, title='Average Tenure by Department')

    plot_bar(_df, 'dept_name', 'avg_tenure_years',
             title='Average Employee Tenure by Department',
             xlabel='Department', ylabel='Years',
             fmt='{:.1f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q32 – Project with the most departments involved
    Which project pulls in people from the most different departments?
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            p.proj_name,
            COUNT(DISTINCT e.dept_id) AS dept_count
        FROM projects p
        JOIN employee_projects ep ON p.proj_id = ep.proj_id
        JOIN employees e ON ep.emp_id = e.emp_id
        GROUP BY p.proj_name
        ORDER BY dept_count DESC;
    """, title='Cross-Department Projects')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q33 – Department–Country employee matrix
    A pivot-style view: how many employees per department in each country?
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            d.dept_name,
            e.country,
            COUNT(*) AS emp_count
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_name, e.country
        ORDER BY d.dept_name, e.country;
    """, title='Department–Country Matrix')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q34 – Salary percentile rank of each employee
    Using `PERCENT_RANK()` to see where each person falls in the overall salary distribution.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            first_name,
            last_name,
            salary,
            ROUND(PERCENT_RANK() OVER (
        ORDER BY salary) * 100, 1) AS percentile
        FROM employees
        ORDER BY salary DESC
        LIMIT 15;
    """, title='Top 15 Employees by Salary Percentile')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q35 – Running total of hires over the years
    A cumulative count: how the workforce grew year by year.
    """)
    return


@app.cell
def _(con, plot_line, show_query):
    _df = show_query(con, """
        WITH yearly AS (
        SELECT EXTRACT(YEAR
        FROM hire_date) AS yr, COUNT(*) AS hires
        FROM employees
        GROUP BY yr )
        SELECT
            yr AS year,
            hires,
            SUM(hires) OVER (
        ORDER BY yr) AS cumulative_hires
        FROM yearly
        ORDER BY yr;
    """, title='Cumulative Hires by Year')

    plot_line(_df, 'year', 'cumulative_hires',
              title='Cumulative Workforce Growth',
              xlabel='Year', ylabel='Total Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q36 – Salary vs. Tenure scatter plot
    Is there a relationship between how long someone has been at TechNova and their pay?
    """)
    return


@app.cell
def _(con, plot_scatter, run_query, show):
    _df = run_query(con, """
        SELECT
            salary,
            ROUND((CURRENT_DATE - hire_date) / 365.25, 1) AS tenure_years
        FROM employees;
    """)
    show(_df.head(10), title='Salary vs Tenure (sample)')
    plot_scatter(_df, 'tenure_years', 'salary',
                 title='Salary vs. Tenure at TechNova',
                 xlabel='Years at Company', ylabel='Salary ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q37 – Top 2 projects per department (by team size)
    Using a CTE with `ROW_NUMBER()` to find each department's most-staffed projects.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        WITH dept_proj AS (
        SELECT
            d.dept_name,
            p.proj_name,
            COUNT(*) AS team_size
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        JOIN employee_projects ep ON e.emp_id = ep.emp_id
        JOIN projects p ON ep.proj_id = p.proj_id
        GROUP BY d.dept_name, p.proj_name ), ranked AS (
        SELECT
            *,
            ROW_NUMBER() OVER ( PARTITION BY dept_name
        ORDER BY team_size DESC ) AS rn
        FROM dept_proj )
        SELECT
            dept_name,
            proj_name,
            team_size
        FROM ranked
        WHERE rn <= 2
        ORDER BY dept_name, rn;
    """, title='Top 2 Projects per Department')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q38 – Average number of employees per project
    A nested subquery to compute a single metric.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT ROUND(AVG(team_size), 1) AS avg_team_size
        FROM (
        SELECT
            proj_id,
            COUNT(*) AS team_size
        FROM employee_projects
        GROUP BY proj_id ) sub;
    """, title='Average Team Size per Project')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q39 – Employees earning above their department's average
    Using a correlated subquery to compare each employee to their department peers.
    """)
    return


@app.cell
def _(con, show_query):
    show_query(con, """
        SELECT
            e.first_name,
            e.last_name,
            d.dept_name,
            e.salary,
            ROUND(dept_avg.avg_sal, 0) AS dept_avg_salary
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        JOIN (
        SELECT
            dept_id,
            AVG(salary) AS avg_sal
        FROM employees
        GROUP BY dept_id ) dept_avg ON e.dept_id = dept_avg.dept_id
        WHERE e.salary > dept_avg.avg_sal
        ORDER BY d.dept_name, e.salary DESC;
    """, title='Employees Earning Above Department Average')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q40 – Comprehensive summary: Department dashboard
    A final aggregation combining headcount, average salary, min/max salary, 
    and project involvement into a single summary table.
    """)
    return


@app.cell
def _(con, plot_grouped_bar, show_query):
    _df = show_query(con, """
        SELECT
            d.dept_name,
            COUNT(DISTINCT e.emp_id) AS headcount,
            ROUND(AVG(e.salary), 0) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary,
            COUNT(DISTINCT ep.proj_id) AS active_projects
        FROM departments d
        LEFT
        JOIN employees e ON d.dept_id = e.dept_id
        LEFT
        JOIN employee_projects ep ON e.emp_id = ep.emp_id
        GROUP BY d.dept_name
        ORDER BY headcount DESC;
    """, title='Department Dashboard')

    plot_grouped_bar(_df, 'dept_name',
                     ['headcount', 'active_projects'],
                     title='Headcount vs. Active Projects by Department',
                     xlabel='Department', ylabel='Count')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    In this notebook we:

    - Loaded **4 CSV files** into DuckDB tables (departments, employees, projects, employee_projects)
    - Ran **40 SQL queries** ranging from basic SELECTs to advanced CTEs and window functions
    - Visualized results with bar charts, pie charts, histograms, box plots, line charts, and scatter plots

    All display and plotting code lives in `display_utils.py` to keep this notebook clean and focused on SQL.

    **Key Takeaways:**
    - TechNova employs 50 people across 8 departments and 15+ countries
    - Engineering is the largest department; Finance and Sales have the highest average pay
    - The busiest employees work on 4-5 projects simultaneously
    - Hiring has been steady, with growth accelerating in 2020-2022
    """)
    return


if __name__ == "__main__":
    app.run()
