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
    # Employee Data Exploration with DuckDB

    **Course:** OMIS 105 — Data Stories  
    **Dataset:** 1,100 employees across 6 countries  
    **Tool:** DuckDB (in-process SQL engine)  

    This notebook demonstrates SQL querying from basic `SELECT` statements
    through advanced ranking and subquery techniques — all powered by DuckDB.
    Every result is displayed as a formatted table, and meaningful plots are
    included where they add insight.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 — Environment Setup
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Import libraries, load our custom display and plot utilities, and connect to DuckDB.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import sys, os

    # Make our utils package importable
    sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))

    from utils import show, show_query, show_cards, show_table_with_images
    from utils import (
        plot_bar, plot_horizontal_bar, plot_pie, plot_grouped_bar,
        plot_histogram, plot_scatter, plot_box, plot_line,
        plot_stacked_bar, plot_heatmap,
    )

    # Connect to an in-memory DuckDB database
    con = duckdb.connect(database=':memory:')
    print('DuckDB connected successfully!')
    return (con, plot_bar, plot_box, plot_grouped_bar, plot_heatmap, plot_histogram, plot_horizontal_bar, plot_line, plot_pie, plot_scatter, plot_stacked_bar, show, show_cards, show_query, show_table_with_images)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 — Load CSV Data into DuckDB
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read the CSV file and create a permanent DuckDB table called **employees**.
    """)
    return


@app.cell
def _(con, show):
    # Create the employees table from our CSV file
    con.execute("""
        CREATE TABLE employees AS
        SELECT *
        FROM read_csv_auto('data/employees.csv');
    """)

    # Verify the table structure
    _df = con.execute("""
        DESCRIBE employees;
    """).fetchdf()
    show(_df, title='Table Schema: employees')
    return


@app.cell
def _(con, show):
    # Quick sanity check — how many rows?
    _df = con.execute("""
        SELECT COUNT(*) AS total_employees
        FROM employees;
    """).fetchdf()
    show(_df, title='Total Record Count')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3 — Basic Queries (SELECT, WHERE, FROM, LIMIT)

    These queries demonstrate fundamental SQL operations: selecting columns,
    filtering rows, sorting, and limiting output.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q1: First 10 Employees
    Display the first 10 rows to get a feel for the data.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            country
        FROM employees
        LIMIT 10;
    """
    show_query(con, _sql, title='First 10 Employees');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q2: Employees in the AI Department
    Find all employees who work in the AI department.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary,
            country,
            degree
        FROM employees
        WHERE department = 'AI'
        LIMIT 15;
    """
    show_query(con, _sql, title='AI Department — Sample');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q3: High Earners (Salary > $180K)
    Who are the top earners in the company?
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            degree,
            country
        FROM employees
        WHERE salary > 180000
        ORDER BY salary DESC
        LIMIT 15;
    """
    show_query(con, _sql, title='Employees Earning Over $180K');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q4: Female Employees with a PhD
    How many women hold a PhD?
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            country,
            age
        FROM employees
        WHERE gender = 'FEMALE'
        AND degree = 'PHD'
        ORDER BY salary DESC
        LIMIT 15;
    """
    show_query(con, _sql, title='Female PhD Holders — Top 15 by Salary');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q5: Employees from India or China
    Filter employees from two of our largest international offices.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            salary,
            country
        FROM employees
        WHERE country IN ('INDIA', 'CHINA')
        ORDER BY country, emp_name
        LIMIT 15;
    """
    show_query(con, _sql, title='Employees from India & China — Sample');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q6: Employees Hired in the First Quarter of 2015
    Who joined between January and March?
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            hire_date,
            department,
            country
        FROM employees
        WHERE hire_date BETWEEN '2015-01-01'
        AND '2015-03-31'
        ORDER BY hire_date
        LIMIT 15;
    """
    show_query(con, _sql, title='Q1-2015 Hires — Sample');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q7: Employees Earning Between $100K and $130K
    A common mid-range salary band.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary,
            degree,
            department
        FROM employees
        WHERE salary BETWEEN 100000
        AND 130000
        ORDER BY salary DESC
        LIMIT 15;
    """
    show_query(con, _sql, title='Mid-Range Salary Band ($100K–$130K)');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q8: Youngest Employees
    Who are the youngest members of the workforce?
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            age,
            department,
            degree,
            country
        FROM employees
        ORDER BY age ASC
        LIMIT 10;
    """
    show_query(con, _sql, title='10 Youngest Employees');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q9: SALES Employees from USA
    Filter by both department and country.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            salary,
            degree,
            age
        FROM employees
        WHERE department = 'SALES'
        AND country = 'USA'
        ORDER BY salary DESC
        LIMIT 15;
    """
    show_query(con, _sql, title='SALES Team in USA — Top 15 by Salary');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q10: Employees Whose Name Starts with 'J'
    Use the LIKE pattern for text matching.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            department,
            country,
            salary
        FROM employees
        WHERE emp_name LIKE 'J%'
        ORDER BY emp_name
        LIMIT 15;
    """
    show_query(con, _sql, title='Employees Whose Name Starts with J');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 — Aggregation Queries (GROUP BY, HAVING, LIMIT)

    These queries summarize data using aggregate functions and filters on groups.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q11: Employee Count by Department
    How many employees work in each department?
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _sql = """
        SELECT
            department,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY department
        ORDER BY emp_count DESC;
    """
    _df = show_query(con, _sql, title='Employee Count by Department')
    plot_bar(_df, x='department', y='emp_count',
             title='Employee Count by Department',
             ylabel='Number of Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q12: Average Salary by Department
    Which department pays the most on average?
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _sql = """
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC;
    """
    _df = show_query(con, _sql, title='Average Salary by Department')
    plot_bar(_df, x='department', y='avg_salary',
             title='Average Salary by Department',
             ylabel='Average Salary ($)', currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q13: Employee Count by Country
    Geographic distribution of the workforce.
    """)
    return


@app.cell
def _(con, plot_pie, show_query):
    _sql = """
        SELECT
            country,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY country
        ORDER BY emp_count DESC;
    """
    _df = show_query(con, _sql, title='Employee Count by Country')
    plot_pie(_df, labels='country', values='emp_count',
             title='Workforce Distribution by Country')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q14: Average Salary by Degree
    Does a higher degree correlate with higher pay?
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _sql = """
        SELECT
            degree,
            ROUND(AVG(salary), 0) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY degree
        ORDER BY avg_salary DESC;
    """
    _df = show_query(con, _sql, title='Salary Statistics by Degree')
    plot_bar(_df, x='degree', y='avg_salary',
             title='Average Salary by Degree',
             ylabel='Average Salary ($)', currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q15: Gender Distribution by Department
    Examine gender balance across departments.
    """)
    return


@app.cell
def _(con, plot_grouped_bar, show_query):
    _sql = """
        SELECT
            department,
            gender,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY department, gender
        ORDER BY department, gender;
    """
    _df = show_query(con, _sql, title='Gender Distribution by Department')
    plot_grouped_bar(_df, x='department', group='gender', y='emp_count',
                     title='Gender Distribution by Department',
                     ylabel='Number of Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q16: Countries with Average Salary Above $130K
    Use HAVING to filter aggregated results.
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _sql = """
        SELECT
            country,
            ROUND(AVG(salary), 0) AS avg_salary,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY country
        HAVING AVG(salary) > 130000
        ORDER BY avg_salary DESC;
    """
    _df = show_query(con, _sql, title='Countries with Avg Salary > $130K')
    plot_bar(_df, x='country', y='avg_salary',
             title='Countries with Avg Salary > $130K',
             ylabel='Average Salary ($)', currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q17: Departments with More Than 200 Employees
    Which departments are the largest?
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            department,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY department
        HAVING COUNT(*) > 200
        ORDER BY emp_count DESC;
    """
    show_query(con, _sql, title='Departments with > 200 Employees');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q18: Degree Count by Country
    How are degrees distributed geographically?
    """)
    return


@app.cell
def _(con, plot_heatmap, show_query):
    _sql = """
        SELECT
            country,
            degree,
            COUNT(*) AS emp_count
        FROM employees
        GROUP BY country, degree
        ORDER BY country, emp_count DESC;
    """
    _df = show_query(con, _sql, title='Degree Distribution by Country')

    # Pivot for a heatmap
    _pivot = _df.pivot_table(index='country', columns='degree', values='emp_count', fill_value=0)
    plot_heatmap(_pivot, title='Degree × Country Heatmap')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q19: Average Age by Department (departments with avg age > 40)
    Which departments skew older?
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            department,
            ROUND(AVG(age), 1) AS avg_age,
            MIN(age) AS youngest,
            MAX(age) AS oldest
        FROM employees
        GROUP BY department
        HAVING AVG(age) > 40
        ORDER BY avg_age DESC;
    """
    show_query(con, _sql, title='Departments with Average Age > 40');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q20: Hiring Trends by Month (2015)
    When did most people join during 2015?
    """)
    return


@app.cell
def _(con, plot_line, show_query):
    _sql = """
        SELECT EXTRACT(MONTH
        FROM hire_date::DATE) AS hire_month, COUNT(*) AS hires
        FROM employees
        GROUP BY hire_month
        ORDER BY hire_month;
    """
    _df = show_query(con, _sql, title='Monthly Hiring Trend — 2015')
    plot_line(_df, x='hire_month', y='hires',
              title='Monthly Hiring Trend — 2015',
              xlabel='Month', ylabel='Number of Hires')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 — Intermediate Queries (Ranking, Subqueries, CTEs, Window Functions)

    These queries use advanced SQL features: window functions for ranking,
    Common Table Expressions (CTEs), correlated subqueries, and CASE expressions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q21: Rank Employees by Salary Within Each Department
    Use `RANK()` window function to find the salary ranking per department.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_name,
            department,
            salary,
            RANK() OVER (PARTITION BY department
        ORDER BY salary DESC) AS salary_rank
        FROM employees QUALIFY salary_rank <= 3
        ORDER BY department, salary_rank;
    """
    show_query(con, _sql, title='Top 3 Earners per Department (RANK)');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q22: Employees Earning Above Their Department Average
    Use a correlated subquery to compare each employee against their department's mean.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            e.emp_name,
            e.department,
            e.salary,
            e.degree
        FROM employees e
        WHERE e.salary > (
        SELECT AVG(e2.salary)
        FROM employees e2
        WHERE e2.department = e.department )
        ORDER BY e.department, e.salary DESC
        LIMIT 15;
    """
    show_query(con, _sql, title='Employees Earning Above Department Avg — Sample');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q23: Salary Percentile Using NTILE
    Divide employees into 4 salary quartiles.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_name,
            salary,
            department,
            NTILE(4) OVER (
        ORDER BY salary) AS salary_quartile
        FROM employees
        ORDER BY salary DESC
        LIMIT 20;
    """
    show_query(con, _sql, title='Top 20 Employees with Salary Quartile');
    return


@app.cell
def _(con, plot_bar, show_query):
    # Visualize the quartile salary ranges
    sql_q = """
        WITH quartiles AS (
        SELECT
            salary,
            NTILE(4) OVER (
        ORDER BY salary) AS quartile
        FROM employees )
        SELECT
            quartile,
            MIN(salary) AS min_salary,
            ROUND(AVG(salary), 0) AS avg_salary,
            MAX(salary) AS max_salary,
            COUNT(*) AS emp_count
        FROM quartiles
        GROUP BY quartile
        ORDER BY quartile;
    """
    _df = show_query(con, sql_q, title='Salary Quartile Summary')
    plot_bar(_df, x='quartile', y='avg_salary',
             title='Average Salary by Quartile',
             ylabel='Average Salary ($)', currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q24: Department Salary Comparison Using CTE
    Use a Common Table Expression to compute department stats and classify departments.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        WITH dept_stats AS (
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_sal,
            COUNT(*) AS emp_cnt,
            ROUND(AVG(age), 1) AS avg_age
        FROM employees
        GROUP BY department )
        SELECT
            department,
            avg_sal,
            emp_cnt,
            avg_age,
            CASE WHEN avg_sal > 140000 THEN 'High Pay' WHEN avg_sal > 120000 THEN 'Mid Pay' ELSE 'Lower Pay' END AS pay_tier
        FROM dept_stats
        ORDER BY avg_sal DESC;
    """
    show_query(con, _sql, title='Department Pay Tier Classification');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q25: Running Total of Hires by Month
    Use a window function to see cumulative hiring throughout 2015.
    """)
    return


@app.cell
def _(con, plot_line, show_query):
    _sql = """
        WITH monthly AS (
        SELECT EXTRACT(MONTH
        FROM hire_date::DATE) AS mth, COUNT(*) AS hires
        FROM employees
        GROUP BY mth )
        SELECT
            mth,
            hires,
            SUM(hires) OVER (
        ORDER BY mth) AS cumulative_hires
        FROM monthly
        ORDER BY mth;
    """
    _df = show_query(con, _sql, title='Cumulative Hiring Throughout 2015')
    plot_line(_df, x='mth', y='cumulative_hires',
              title='Cumulative Hires Through 2015',
              xlabel='Month', ylabel='Total Hires')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q26: Salary Difference from Department Maximum
    How far is each employee from the top earner in their department?
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_name,
            department,
            salary,
            MAX(salary) OVER (PARTITION BY department) AS dept_max,
            MAX(salary) OVER (PARTITION BY department) - salary AS gap_from_max
        FROM employees
        ORDER BY department, gap_from_max ASC
        LIMIT 15;
    """
    show_query(con, _sql, title='Salary Gap from Department Max — Top Earners');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q27: Country with the Highest PhD Concentration
    Subquery to find which country has the most PhD holders as a percentage.
    """)
    return


@app.cell
def _(con, plot_bar, show_query):
    _sql = """
        WITH country_phd AS (
        SELECT
            country,
            COUNT(*) FILTER (
        WHERE degree = 'PHD') AS phd_count, COUNT(*) AS total, ROUND(100.0 * COUNT(*) FILTER (
        WHERE degree = 'PHD') / COUNT(*), 2) AS phd_pct
        FROM employees
        GROUP BY country )
        SELECT *
        FROM country_phd
        ORDER BY phd_pct DESC;
    """
    _df = show_query(con, _sql, title='PhD Concentration by Country')
    plot_bar(_df, x='country', y='phd_pct',
             title='PhD Holders as % of Country Workforce',
             ylabel='PhD %')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q28: Dense Rank by Age Within Country
    Use DENSE_RANK to rank employees by age within each country.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        SELECT
            emp_name,
            country,
            age,
            salary,
            DENSE_RANK() OVER (PARTITION BY country
        ORDER BY age DESC) AS age_rank
        FROM employees QUALIFY age_rank <= 3
        ORDER BY country, age_rank;
    """
    show_query(con, _sql, title='Top 3 Oldest Employees per Country');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q29: Departments Where Females Out-Earn Males
    Compare average salary by gender per department.
    """)
    return


@app.cell
def _(con, plot_grouped_bar, show_query):
    _sql = """
        WITH gender_avg AS (
        SELECT
            department,
            gender,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department, gender ), pivoted AS (
        SELECT
            department,
            MAX(CASE WHEN gender = 'FEMALE' THEN avg_salary END) AS female_avg,
            MAX(CASE WHEN gender = 'MALE' THEN avg_salary END) AS male_avg
        FROM gender_avg
        GROUP BY department )
        SELECT
            department,
            female_avg,
            male_avg,
            female_avg - male_avg AS diff,
            CASE WHEN female_avg > male_avg THEN 'Female Higher' ELSE 'Male Higher' END AS who_earns_more
        FROM pivoted
        ORDER BY diff DESC;
    """
    _df = show_query(con, _sql, title='Gender Pay Comparison by Department')

    # Grouped bar of female vs male avg salary
    sql_plot = """
        SELECT
            department,
            gender,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department, gender
        ORDER BY department;
    """
    df_plot = con.execute(sql_plot).fetchdf()
    plot_grouped_bar(df_plot, x='department', group='gender', y='avg_salary',
                     title='Average Salary: Female vs Male by Department',
                     ylabel='Average Salary ($)', currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q30: Employees in the Top 10% of Salary
    Use PERCENT_RANK to identify the highest earners across the company.
    """)
    return


@app.cell
def _(con, show_query):
    _sql = """
        WITH ranked AS (
        SELECT
            emp_name,
            department,
            salary,
            degree,
            country,
            ROUND(PERCENT_RANK() OVER (
        ORDER BY salary) * 100, 1) AS salary_percentile
        FROM employees )
        SELECT *
        FROM ranked
        WHERE salary_percentile >= 90
        ORDER BY salary DESC
        LIMIT 20;
    """
    show_query(con, _sql, title='Top 10% Earners');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6 — Bonus: Deep-Dive Queries with Visualizations

    Additional analytical queries paired with meaningful plots.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### B1: Overall Salary Distribution
    A histogram showing how salaries are spread across the company.
    """)
    return


@app.cell
def _(con, plot_histogram):
    df_all = con.execute("""
        SELECT salary
        FROM employees;
    """).fetchdf()
    plot_histogram(df_all, col='salary', bins=25,
                   title='Salary Distribution — All Employees',
                   xlabel='Salary ($)', currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### B2: Salary Spread by Degree (Box Plot)
    Visualize the range and median salary for each degree level.
    """)
    return


@app.cell
def _(con, plot_box):
    df_box = con.execute("""
        SELECT
            degree,
            salary
        FROM employees
        ORDER BY CASE degree WHEN 'BA' THEN 1 WHEN 'BS' THEN 2 WHEN 'MIS' THEN 3 WHEN 'MS' THEN 4 WHEN 'PHD' THEN 5 END;
    """).fetchdf()
    plot_box(df_box, x='degree', y='salary',
             title='Salary Distribution by Degree',
             ylabel='Salary ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### B3: Age vs. Salary (Scatter Plot)
    Does age correlate with salary? Coloured by degree.
    """)
    return


@app.cell
def _(con, plot_scatter):
    df_scatter = con.execute("""
        SELECT
            age,
            salary,
            degree
        FROM employees;
    """).fetchdf()
    plot_scatter(df_scatter, x='age', y='salary', hue='degree',
                 title='Age vs. Salary by Degree',
                 xlabel='Age', ylabel='Salary ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### B4: Degree Mix by Country (Stacked Bar)
    See how the educational profile varies across countries.
    """)
    return


@app.cell
def _(con, plot_stacked_bar):
    _sql = """
        SELECT
            country,
            degree,
            COUNT(*) AS cnt
        FROM employees
        GROUP BY country, degree
        ORDER BY country;
    """
    _df = con.execute(_sql).fetchdf()
    _pivot = _df.pivot_table(index='country', columns='degree', values='cnt', fill_value=0)
    plot_stacked_bar(_pivot,
                     title='Degree Composition by Country',
                     xlabel='Country', ylabel='Number of Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### B5: Average Salary Heatmap — Country × Gender
    A heatmap revealing salary patterns by country and gender.
    """)
    return


@app.cell
def _(con, plot_heatmap):
    _sql = """
        SELECT
            country,
            gender,
            ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY country, gender
        ORDER BY country;
    """
    _df = con.execute(_sql).fetchdf()
    _pivot = _df.pivot_table(index='country', columns='gender', values='avg_salary', fill_value=0)
    plot_heatmap(_pivot, title='Avg Salary: Country × Gender', cmap='Blues')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### B6: Top 10 Highest-Paid Employees
    A horizontal bar chart of the company's biggest earners.
    """)
    return


@app.cell
def _(con, plot_horizontal_bar, show_query):
    _sql = """
        SELECT
            emp_name,
            salary
        FROM employees
        ORDER BY salary DESC
        LIMIT 10;
    """
    _df = show_query(con, _sql, title='Top 10 Highest-Paid Employees')
    plot_horizontal_bar(_df, x='salary', y='emp_name',
                        title='Top 10 Highest-Paid Employees',
                        xlabel='Salary ($)', currency=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7 — Employee Profiles: Rendering Avatars

    Every employee has an `image_url` column pointing to a unique avatar.
    In this section we use custom display functions that render those URLs
    as images — turning dry query results into a visual employee directory.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A1: Employee Table with Avatar Images

    The `show_table_with_images()` function renders the `image_url` column
    as a circular avatar thumbnail right inside the table. Every other
    column displays normally.
    """)
    return


@app.cell
def _(con, show_table_with_images):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            image_url,
            department,
            salary,
            country
        FROM employees
        ORDER BY salary DESC
        LIMIT 10;
    """
    _df = con.execute(_sql).fetchdf()
    show_table_with_images(_df, title='Top 10 Earners — with Avatars')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A2: Employee Profile Cards — Top Earners

    The `show_cards()` function displays each employee as a visual card
    with their avatar, name, and key details. Great for team directories
    and dashboards.
    """)
    return


@app.cell
def _(con, show_cards):
    _sql = """
        SELECT
            emp_name,
            image_url,
            department,
            salary,
            degree,
            country
        FROM employees
        ORDER BY salary DESC
        LIMIT 8;
    """
    _df = con.execute(_sql).fetchdf()
    show_cards(_df, title='Top 8 Highest-Paid Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A3: PhD Holder Directory

    Profile cards for employees who hold a PhD, sorted by salary.
    Notice how each card shows the country and department at a glance.
    """)
    return


@app.cell
def _(con, show_cards):
    _sql = """
        SELECT
            emp_name,
            image_url,
            department,
            salary,
            country,
            age
        FROM employees
        WHERE degree = 'PHD'
        ORDER BY salary DESC
        LIMIT 12;
    """
    _df = con.execute(_sql).fetchdf()
    show_cards(_df, title='PhD Holders — Top 12 by Salary', columns=4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A4: AI Department Roster

    A team roster for the AI department — useful for onboarding docs
    or internal dashboards.
    """)
    return


@app.cell
def _(con, show_cards):
    _sql = """
        SELECT
            emp_name,
            image_url,
            salary,
            degree,
            gender,
            country
        FROM employees
        WHERE department = 'AI'
        ORDER BY emp_name
        LIMIT 12;
    """
    _df = con.execute(_sql).fetchdf()
    show_cards(_df, title='AI Department Team', columns=4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A5: Youngest Employees — Table with Avatars

    A table view showing the 10 youngest employees, with their avatar
    rendered inline alongside age, degree, and department.
    """)
    return


@app.cell
def _(con, show_table_with_images):
    _sql = """
        SELECT
            emp_name,
            image_url,
            age,
            degree,
            department,
            country,
            salary
        FROM employees
        ORDER BY age ASC
        LIMIT 10;
    """
    _df = con.execute(_sql).fetchdf()
    show_table_with_images(_df, title='10 Youngest Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A6: Top Earner in Each Country

    Using a window function to find the highest-paid employee per country,
    then displaying them as profile cards — one card per country.
    """)
    return


@app.cell
def _(con, show_cards):
    _sql = """
        SELECT
            emp_name,
            image_url,
            department,
            salary,
            degree,
            country
        FROM employees QUALIFY RANK() OVER (PARTITION BY country
        ORDER BY salary DESC) = 1
        ORDER BY salary DESC;
    """
    _df = con.execute(_sql).fetchdf()
    show_cards(_df, title='Highest-Paid Employee per Country', columns=3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A7: Random Employee Sample — Full Profile Table

    A random sample of employees with all key columns and their avatar.
    Uses DuckDB's `USING SAMPLE` clause.
    """)
    return


@app.cell
def _(con, show_table_with_images):
    _sql = """
        SELECT
            emp_id,
            emp_name,
            image_url,
            department,
            salary,
            gender,
            degree,
            country,
            age
        FROM employees USING SAMPLE 8;
    """
    _df = con.execute(_sql).fetchdf()
    show_table_with_images(_df, title='Random Sample of 8 Employees')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8 — Cleanup
    """)
    return


@app.cell
def _(con):
    con.close()
    print('DuckDB connection closed. Notebook complete!')
    return


if __name__ == "__main__":
    app.run()
