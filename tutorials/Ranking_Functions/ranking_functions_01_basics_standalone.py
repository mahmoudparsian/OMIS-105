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
    # Master Flagship Tutorial: DuckDB Ranking Functions

    **Goal:** learn `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()` from zero, using DuckDB and a realistic 1000-row employees CSV.

    Every learning SQL cell includes a natural-language question, simple concept explanation, SQL using `WITH`, and a styled result table.
    """)
    return


@app.cell
def _():
    # Setup: imports and display options
    import duckdb
    import pandas as pd
    from IPython.display import display, HTML

    pd.set_option('display.max_columns', 50)
    pd.set_option('display.width', 120)

    CSV_PATH = './data/employees_1000.csv'
    con = duckdb.connect(database=':memory:')
    return (HTML, con, display)


@app.cell
def _(HTML, df, display):
    # Rendering helper: keep all styling code outside the SQL learning cells.
    def show(df, max_rows=20, caption=None):
        # Render a DataFrame as a high-quality teaching table.
        if df is None:
            return
        display_df = df.head(max_rows).copy()
        row_count = len(df)
        shown_count = len(display_df)
        caption_text = caption or f"Showing {shown_count:,} of {row_count:,} rows"

        styler = (
            display_df.style
            .set_caption(caption_text)
            .set_table_styles([
                {'selector': 'caption', 'props': [
                    ('caption-side', 'top'),
                    ('font-size', '15px'),
                    ('font-weight', '700'),
                    ('color', '#0f172a'),
                    ('padding', '8px 0')
                ]},
                {'selector': 'th', 'props': [
                    ('background-color', '#0f172a'),
                    ('color', 'white'),
                    ('font-weight', '700'),
                    ('text-align', 'left'),
                    ('padding', '8px'),
                    ('border', '1px solid #334155')
                ]},
                {'selector': 'td', 'props': [
                    ('padding', '7px 8px'),
                    ('border', '1px solid #e2e8f0')
                ]},
                {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#f8fafc')]},
                {'selector': 'tr:nth-child(odd)', 'props': [('background-color', '#ffffff')]},
                {'selector': 'tr:hover', 'props': [('background-color', '#dbeafe')]},
                {'selector': 'table', 'props': [
                    ('border-collapse', 'collapse'),
                    ('font-family', 'Arial, sans-serif'),
                    ('font-size', '13px'),
                    ('width', '100%')
                ]},
            ])
            .format(precision=2)
        )
        display(styler)
        display(HTML(f"<div style='font-family:Arial; color:#475569; margin:4px 0 18px 0;'>Total rows returned by SQL: <b>{row_count:,}</b></div>"))
    return (show,)


@app.cell
def _(con, show):
    # Load the CSV into DuckDB.
    # The table is read from employees_1000.csv, which is included with this notebook.
    con.execute("""
        DROP TABLE IF EXISTS employees;
    """)
    con.execute("""
        CREATE TABLE employees AS
        SELECT
            emp_id,
            emp_name,
            dept_id,
            country,
            gender,
            salary,
            degree,
            performance,
            CAST(hire_date AS DATE) AS hire_date
        FROM read_csv_auto('./data/employees_1000.csv', header=True);
    """)

    summary = con.execute("""
        WITH row_check AS (
        SELECT
            COUNT(*) AS total_rows,
            MIN(hire_date) AS earliest_hire_date,
            MAX(hire_date) AS latest_hire_date,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees )
        SELECT *
        FROM row_check;
    """).df()
    show(summary, caption='Dataset loaded into DuckDB')
    return


@app.cell
def _(con, show):
    # Basic 1 of 10 — inspect the employee table
    # Natural-language question:
    # What does the employee table look like?
    #
    # Concept in simple English:
    # Before ranking, inspect the columns and sample rows. Ranking functions always operate on rows that already exist in a result set.

    _SQL_QUERY = """
        WITH sample_employees AS (
        SELECT *
        FROM employees
        ORDER BY emp_id
        LIMIT 10 )
        SELECT *
        FROM sample_employees;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Basic 1 of 10 — inspect the employee table')
    return (_df,)


@app.cell
def _(con, show):
    # Basic 2 of 10 — verify department distribution
    # Natural-language question:
    # How many employees are in each department?
    #
    # Concept in simple English:
    # A ranking function can rank within the whole table or within groups. Departments will become our main ranking groups later.

    _SQL_QUERY = """
        WITH dept_counts AS (
        SELECT
            dept_id,
            COUNT(*) AS employees
        FROM employees
        GROUP BY dept_id )
        SELECT *
        FROM dept_counts
        ORDER BY employees DESC, dept_id;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Basic 2 of 10 — verify department distribution')
    return (_df,)


@app.cell
def _(con, show):
    # Basic 3 of 10 — verify country distribution
    # Natural-language question:
    # How many employees are in each country?
    #
    # Concept in simple English:
    # Partitioned ranking means ranking separately inside a category. Country is another useful partition column.

    _SQL_QUERY = """
        WITH country_counts AS (
        SELECT
            country,
            COUNT(*) AS employees
        FROM employees
        GROUP BY country )
        SELECT *
        FROM country_counts
        ORDER BY employees DESC, country;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Basic 3 of 10 — verify country distribution')
    return (_df,)


@app.cell
def _(con, show):
    # Basic 4 of 10 — understand sorted order before ranking
    # Natural-language question:
    # Who are the 10 highest-paid employees?
    #
    # Concept in simple English:
    # Ranking depends on `ORDER BY`. Before using ranking functions, students should understand the sorted order that the rank will follow.

    _SQL_QUERY = """
        WITH sorted_employees AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            country,
            degree,
            salary
        FROM employees
        ORDER BY salary DESC, emp_id
        LIMIT 10 )
        SELECT *
        FROM sorted_employees;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Basic 4 of 10 — understand sorted order before ranking')
    return (_df,)


@app.cell
def _(con, show):
    # Basic 5 of 10 — first ROW_NUMBER
    # Natural-language question:
    # Assign a unique position to employees by salary.
    #
    # Concept in simple English:
    # `ROW_NUMBER()` gives every row a unique number. Even if two people have the same salary, one gets the next row number.

    _SQL_QUERY = """
        WITH ranked_employees AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            degree,
            salary,
            ROW_NUMBER() OVER (
        ORDER BY salary DESC, emp_id) AS salary_row_number
        FROM employees )
        SELECT *
        FROM ranked_employees
        ORDER BY salary_row_number
        LIMIT 15;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Basic 5 of 10 — first ROW_NUMBER')
    return (_df,)


@app.cell
def _(con, show):
    # Basic 6 of 10 — ROW_NUMBER inside each department
    # Natural-language question:
    # Assign a salary position inside each department.
    #
    # Concept in simple English:
    # `PARTITION BY dept_id` restarts the row numbers for every department. This is one of the most important ranking patterns.

    _SQL_QUERY = """
        WITH dept_ranked AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            degree,
            salary,
            ROW_NUMBER() OVER ( PARTITION BY dept_id
        ORDER BY salary DESC, emp_id ) AS dept_salary_row_number
        FROM employees )
        SELECT *
        FROM dept_ranked
        WHERE dept_id IN ('AI', 'SALES')
        ORDER BY dept_id, dept_salary_row_number
        LIMIT 20;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Basic 6 of 10 — ROW_NUMBER inside each department')
    return (_df,)


@app.cell
def _(con, show):
    # Basic 7 of 10 — first RANK
    # Natural-language question:
    # Rank employees by salary and allow ties.
    #
    # Concept in simple English:
    # `RANK()` gives tied rows the same rank. After a tie, it skips rank numbers. Example: 1, 2, 2, 4.

    _SQL_QUERY = """
        WITH salary_ranked AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            degree,
            salary,
            RANK() OVER (
        ORDER BY salary DESC) AS salary_rank
        FROM employees )
        SELECT *
        FROM salary_ranked
        ORDER BY salary_rank, emp_id
        LIMIT 20;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Basic 7 of 10 — first RANK')
    return (_df,)


@app.cell
def _(con, show):
    # Basic 8 of 10 — first DENSE_RANK
    # Natural-language question:
    # Rank employees by salary without gaps after ties.
    #
    # Concept in simple English:
    # `DENSE_RANK()` also gives tied rows the same rank, but it does not skip rank numbers. Example: 1, 2, 2, 3.

    _SQL_QUERY = """
        WITH salary_dense_ranked AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            degree,
            salary,
            DENSE_RANK() OVER (
        ORDER BY salary DESC) AS salary_dense_rank
        FROM employees )
        SELECT *
        FROM salary_dense_ranked
        ORDER BY salary_dense_rank, emp_id
        LIMIT 20;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Basic 8 of 10 — first DENSE_RANK')
    return (_df,)


@app.cell
def _(con, show):
    # Basic 9 of 10 — compare all three ranking functions
    # Natural-language question:
    # How are ROW_NUMBER, RANK, and DENSE_RANK different?
    #
    # Concept in simple English:
    # This cell shows the three functions side by side. The difference appears clearly when salary ties exist.

    _SQL_QUERY = """
        WITH comparison AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            degree,
            salary,
            ROW_NUMBER() OVER (
        ORDER BY salary DESC, emp_id) AS row_number_value, RANK() OVER (
        ORDER BY salary DESC) AS rank_value, DENSE_RANK() OVER (
        ORDER BY salary DESC) AS dense_rank_value
        FROM employees )
        SELECT *
        FROM comparison
        ORDER BY salary DESC, emp_id
        LIMIT 25;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Basic 9 of 10 — compare all three ranking functions')
    return (_df,)


@app.cell
def _(con, show):
    # Basic 10 of 10 — top 3 employees by department
    # Natural-language question:
    # Who are the top 3 highest-paid employees in each department?
    #
    # Concept in simple English:
    # This is a classic `WITH` pattern: first rank rows in a CTE, then filter the rank in the outer query.

    _SQL_QUERY = """
        WITH dept_ranked AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            degree,
            salary,
            ROW_NUMBER() OVER ( PARTITION BY dept_id
        ORDER BY salary DESC, emp_id ) AS dept_position
        FROM employees )
        SELECT *
        FROM dept_ranked
        WHERE dept_position <= 3
        ORDER BY dept_id, dept_position;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Basic 10 of 10 — top 3 employees by department')
    return (_df,)


@app.cell
def _(con, show):
    # Intermediate 1 of 5 — top salary tiers by department
    # Natural-language question:
    # Which salary values are in the top 3 salary tiers within each department?
    #
    # Concept in simple English:
    # Use `DENSE_RANK()` when you want top salary levels, not just top rows. If many employees share a salary, they belong to the same salary tier.

    _SQL_QUERY = """
        WITH salary_tiers AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            degree,
            salary,
            DENSE_RANK() OVER ( PARTITION BY dept_id
        ORDER BY salary DESC ) AS dept_salary_tier
        FROM employees )
        SELECT *
        FROM salary_tiers
        WHERE dept_salary_tier <= 3
        ORDER BY dept_id, dept_salary_tier, salary DESC, emp_id;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Intermediate 1 of 5 — top salary tiers by department')
    return (_df,)


@app.cell
def _(con, show):
    # Intermediate 2 of 5 — rank departments by average salary
    # Natural-language question:
    # Which departments have the highest average salary?
    #
    # Concept in simple English:
    # Ranking does not have to be applied only to raw employee rows. We can first aggregate in a CTE, then rank the aggregated department rows.

    _SQL_QUERY = """
        WITH dept_summary AS (
        SELECT
            dept_id,
            COUNT(*) AS employees,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY dept_id ), ranked_departments AS (
        SELECT
            dept_id,
            employees,
            avg_salary,
            RANK() OVER (
        ORDER BY avg_salary DESC) AS avg_salary_rank
        FROM dept_summary )
        SELECT *
        FROM ranked_departments
        ORDER BY avg_salary_rank, dept_id;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Intermediate 2 of 5 — rank departments by average salary')
    return (_df,)


@app.cell
def _(con, show):
    # Intermediate 3 of 5 — best performer per department
    # Natural-language question:
    # Who has the highest performance score in each department?
    #
    # Concept in simple English:
    # When ties matter, `RANK()` is safer than `ROW_NUMBER()`. It returns all employees tied for first place.

    _SQL_QUERY = """
        WITH performance_ranked AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            performance,
            salary,
            RANK() OVER ( PARTITION BY dept_id
        ORDER BY performance DESC ) AS performance_rank
        FROM employees )
        SELECT *
        FROM performance_ranked
        WHERE performance_rank = 1
        ORDER BY dept_id, salary DESC, emp_id;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Intermediate 3 of 5 — best performer per department')
    return (_df,)


@app.cell
def _(con, show):
    # Intermediate 4 of 5 — newest hires by country
    # Natural-language question:
    # Who are the 5 most recently hired employees in each country?
    #
    # Concept in simple English:
    # Ranking can use dates. `ORDER BY hire_date DESC` means newest employees receive the smallest row numbers.

    _SQL_QUERY = """
        WITH country_hires AS (
        SELECT
            emp_id,
            emp_name,
            country,
            dept_id,
            hire_date,
            ROW_NUMBER() OVER ( PARTITION BY country
        ORDER BY hire_date DESC, emp_id ) AS newest_hire_position
        FROM employees )
        SELECT *
        FROM country_hires
        WHERE newest_hire_position <= 5
        ORDER BY country, newest_hire_position;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Intermediate 4 of 5 — newest hires by country')
    return (_df,)


@app.cell
def _(con, show):
    # Intermediate 5 of 5 — salary rank within degree
    # Natural-language question:
    # Within each degree, who are the 5 highest-paid employees?
    #
    # Concept in simple English:
    # This teaches a different partition. `PARTITION BY degree` answers: rank people only against others with the same degree.

    _SQL_QUERY = """
        WITH degree_ranked AS (
        SELECT
            emp_id,
            emp_name,
            degree,
            dept_id,
            country,
            salary,
            ROW_NUMBER() OVER ( PARTITION BY degree
        ORDER BY salary DESC, emp_id ) AS degree_salary_position
        FROM employees )
        SELECT *
        FROM degree_ranked
        WHERE degree_salary_position <= 5
        ORDER BY degree, degree_salary_position;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Intermediate 5 of 5 — salary rank within degree')
    return (df,)


@app.cell
def _(con, show):
    # Intermediate+ 1 of 5 — top employee per department and country
    # Natural-language question:
    # Who is the highest-paid employee for every department-country combination?
    #
    # Concept in simple English:
    # Ranking can partition by multiple columns. Here each group is a unique `(dept_id, country)` combination.

    _SQL_QUERY = """
        WITH dept_country_ranked AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            country,
            degree,
            salary,
            ROW_NUMBER() OVER ( PARTITION BY dept_id, country
        ORDER BY salary DESC, emp_id ) AS position_in_dept_country
        FROM employees )
        SELECT *
        FROM dept_country_ranked
        WHERE position_in_dept_country = 1
        ORDER BY dept_id, country;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Intermediate+ 1 of 5 — top employee per department and country')
    return (_df,)


@app.cell
def _(con, show):
    # Intermediate+ 2 of 5 — find second-highest salary tier by department
    # Natural-language question:
    # What is the second-highest salary tier in each department?
    #
    # Concept in simple English:
    # Use `DENSE_RANK()` when the business question asks for the second distinct salary level, not the second row.

    _SQL_QUERY = """
        WITH dept_salary_tiers AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            degree,
            salary,
            DENSE_RANK() OVER ( PARTITION BY dept_id
        ORDER BY salary DESC ) AS salary_tier
        FROM employees )
        SELECT *
        FROM dept_salary_tiers
        WHERE salary_tier = 2
        ORDER BY dept_id, salary DESC, emp_id;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Intermediate+ 2 of 5 — find second-highest salary tier by department')
    return (_df,)


@app.cell
def _(con, show):
    # Intermediate+ 3 of 5 — rank employees against department average
    # Natural-language question:
    # Who earns the most above their department average?
    #
    # Concept in simple English:
    # This combines aggregation and ranking. First compute department averages, join them back, then rank salary difference inside each department.

    _SQL_QUERY = """
        WITH dept_avg AS (
        SELECT
            dept_id,
            AVG(salary) AS avg_dept_salary
        FROM employees
        GROUP BY dept_id ), employee_gap AS (
        SELECT
            e.emp_id,
            e.emp_name,
            e.dept_id,
            e.degree,
            e.salary,
            ROUND(d.avg_dept_salary, 2) AS avg_dept_salary,
            ROUND(e.salary - d.avg_dept_salary, 2) AS salary_above_dept_avg
        FROM employees e
        JOIN dept_avg d ON e.dept_id = d.dept_id ), gap_ranked AS (
        SELECT
            *,
            ROW_NUMBER() OVER ( PARTITION BY dept_id
        ORDER BY salary_above_dept_avg DESC, emp_id ) AS gap_position
        FROM employee_gap )
        SELECT *
        FROM gap_ranked
        WHERE gap_position <= 3
        ORDER BY dept_id, gap_position;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Intermediate+ 3 of 5 — rank employees against department average')
    return (_df,)


@app.cell
def _(con, show):
    # Intermediate+ 4 of 5 — rank departments inside each country
    # Natural-language question:
    # For each country, which departments have the highest average salary?
    #
    # Concept in simple English:
    # This is ranking aggregated groups within another group. We summarize by country and department, then rank departments inside each country.

    _SQL_QUERY = """
        WITH country_dept_summary AS (
        SELECT
            country,
            dept_id,
            COUNT(*) AS employees,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY country, dept_id ), country_dept_ranked AS (
        SELECT
            country,
            dept_id,
            employees,
            avg_salary,
            DENSE_RANK() OVER ( PARTITION BY country
        ORDER BY avg_salary DESC ) AS dept_rank_in_country
        FROM country_dept_summary )
        SELECT *
        FROM country_dept_ranked
        WHERE dept_rank_in_country <= 3
        ORDER BY country, dept_rank_in_country, dept_id;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Intermediate+ 4 of 5 — rank departments inside each country')
    return (_df,)


@app.cell
def _(con, show):
    # Intermediate+ 5 of 5 — final mastery comparison
    # Natural-language question:
    # For each department, compare employee salary position, salary rank, and salary tier.
    #
    # Concept in simple English:
    # Final mastery cell: `ROW_NUMBER()` gives a unique position, `RANK()` preserves ties with gaps, and `DENSE_RANK()` preserves ties without gaps.

    _SQL_QUERY = """
        WITH final_ranked AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            degree,
            salary,
            ROW_NUMBER() OVER ( PARTITION BY dept_id
        ORDER BY salary DESC, emp_id ) AS unique_position, RANK() OVER ( PARTITION BY dept_id
        ORDER BY salary DESC ) AS rank_with_gaps, DENSE_RANK() OVER ( PARTITION BY dept_id
        ORDER BY salary DESC ) AS rank_without_gaps
        FROM employees )
        SELECT *
        FROM final_ranked
        WHERE unique_position <= 12
        ORDER BY dept_id, unique_position;
    """

    _df = con.execute(_SQL_QUERY).df()
    show(_df, caption='Intermediate+ 5 of 5 — final mastery comparison')
    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary: what students should remember

    - `ROW_NUMBER()` gives every row a unique position.
    - `RANK()` gives tied rows the same rank and leaves gaps.
    - `DENSE_RANK()` gives tied rows the same rank and does not leave gaps.
    - `PARTITION BY` restarts the ranking inside each group.
    - `ORDER BY` defines what “best,” “highest,” “newest,” or “first” means.
    - The most common pattern is: use `WITH` to rank first, then filter the rank in the final `SELECT`.
    """)
    return


if __name__ == "__main__":
    app.run()
