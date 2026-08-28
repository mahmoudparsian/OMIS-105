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

    **Focus:** `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` and `WITH`-based subqueries.

    This notebook is designed for students who have never used ranking functions before. We start with plain grouping and sorting, then introduce ranking step by step. Every SQL example uses `WITH` when a subquery is needed.

    Dataset: 1,000 employees with exact department and country distributions. PhD salaries range from **$200,000 to $280,000**, so ranking examples have realistic spread and ties.
    """)
    return


@app.cell
def _():
    # Cell 1 — Setup: import DuckDB, helpers, and connect
    import duckdb
    import pandas as pd

    from helpers.rendering import show
    from helpers.plots import (
        plot_salary_by_degree,
        plot_top_departments,
        plot_rank_curve,
        plot_top_n_per_dept,
    )

    con = duckdb.connect(database=":memory:")
    return (con, plot_rank_curve, plot_salary_by_degree, plot_top_n_per_dept, show)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 2 — Load the CSV into DuckDB

    **Concept:** In analytics, we usually start from a table. Here the source is a CSV file, and DuckDB can read it directly.

    **Natural language query:** Create an `employees` table from the CSV file.
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        CREATE
        OR REPLACE TABLE employees AS
        SELECT *
        FROM read_csv_auto('data/employees_1000.csv');
    """
    con.execute(_sql)

    show(con.execute("""
        SELECT *
        FROM employees
        LIMIT 10;
    """).df(), "First 10 employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 3 — Basic inspection

    **Concept:** Before ranking, always understand the table shape and columns.

    **Natural language query:** How many rows are in the table, and what are the first few values?
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH table_summary AS (
        SELECT COUNT(*) AS total_employees
        FROM employees )
        SELECT *
        FROM table_summary;
    """

    show(con.execute(_sql).df(), "Table size")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 4 — Validate department distribution

    **Concept:** `GROUP BY` creates groups. This helps us verify that our teaching dataset matches the required department sizes.

    **Natural language query:** How many employees are in each department?
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH dept_counts AS (
        SELECT
            dept_id,
            COUNT(*) AS employee_count
        FROM employees
        GROUP BY dept_id )
        SELECT *
        FROM dept_counts
        ORDER BY employee_count DESC;
    """

    show(con.execute(_sql).df(), "Employees by department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 5 — Validate country distribution

    **Concept:** Grouping is also useful for quality checks. We verify that country counts match the specification.

    **Natural language query:** How many employees are in each country?
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH country_counts AS (
        SELECT
            country,
            COUNT(*) AS employee_count
        FROM employees
        GROUP BY country )
        SELECT *
        FROM country_counts
        ORDER BY employee_count DESC;
    """

    show(con.execute(_sql).df(), "Employees by country")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 6 — Validate salary ranges by degree

    **Concept:** Ranking examples work best when data has realistic variation. PhD salaries should be high, but not all identical.

    **Natural language query:** What is the minimum, maximum, and average salary by degree?
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH degree_salary_stats AS (
        SELECT
            degree,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            ROUND(AVG(salary), 0) AS avg_salary,
            COUNT(*) AS employees
        FROM employees
        GROUP BY degree )
        SELECT *
        FROM degree_salary_stats
        ORDER BY avg_salary DESC;
    """

    show(con.execute(_sql).df(), "Salary range by degree")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 7 — Plotting intuition: average salary by degree

    **Concept:** A plot helps students see why PhD employees often appear near the top of rankings.

    The plotting code is hidden in an external helper file: `helpers/plots.py`.
    """)
    return


@app.cell
def _(con, plot_salary_by_degree):
    plot_salary_by_degree(con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 8 — Sorting before ranking

    **Concept:** Ranking functions depend on an `ORDER BY`. Before using a ranking function, first understand the ordering.

    **Natural language query:** Who are the 10 highest-paid employees?
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH ordered_employees AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            country,
            degree,
            salary
        FROM employees )
        SELECT *
        FROM ordered_employees
        ORDER BY salary DESC, emp_id
        LIMIT 10;
    """

    show(con.execute(_sql).df(), "Top 10 employees by salary before ranking")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 9 — First ranking function: ROW_NUMBER()

    **Concept:** `ROW_NUMBER()` gives every row a unique number. Even if two employees have the same salary, their row numbers are different.

    **Natural language query:** Assign a unique salary position to each employee from highest salary to lowest salary.
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH ranked_employees AS (
        SELECT
            emp_id,
            emp_name,
            degree,
            salary,
            ROW_NUMBER() OVER (
        ORDER BY salary DESC, emp_id) AS row_number_salary
        FROM employees )
        SELECT *
        FROM ranked_employees
        ORDER BY row_number_salary
        LIMIT 15;
    """

    show(con.execute(_sql).df(), "ROW_NUMBER over salary")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 10 — RANK(): ranking with gaps

    **Concept:** `RANK()` gives the same rank to tied values. But after a tie, it leaves a gap.

    Example: if two employees tie for rank 1, the next rank is 3, not 2.

    **Natural language query:** Rank employees by salary and allow ties.
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH ranked_employees AS (
        SELECT
            emp_id,
            emp_name,
            degree,
            salary,
            RANK() OVER (
        ORDER BY salary DESC) AS salary_rank
        FROM employees )
        SELECT *
        FROM ranked_employees
        ORDER BY salary_rank, emp_id
        LIMIT 20;
    """

    show(con.execute(_sql).df(), "RANK over salary")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 11 — DENSE_RANK(): ranking without gaps

    **Concept:** `DENSE_RANK()` also gives the same rank to tied values. But it does not leave gaps.

    Example: if two employees tie for rank 1, the next rank is 2.

    **Natural language query:** Rank employees by salary using dense ranking.
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH ranked_employees AS (
        SELECT
            emp_id,
            emp_name,
            degree,
            salary,
            DENSE_RANK() OVER (
        ORDER BY salary DESC) AS dense_salary_rank
        FROM employees )
        SELECT *
        FROM ranked_employees
        ORDER BY dense_salary_rank, emp_id
        LIMIT 20;
    """

    show(con.execute(_sql).df(), "DENSE_RANK over salary")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 12 — Side-by-side comparison

    **Concept:** This is the most important comparison in the tutorial.

    - `ROW_NUMBER()` always creates unique positions.
    - `RANK()` handles ties but may create gaps.
    - `DENSE_RANK()` handles ties and does not create gaps.

    **Natural language query:** Show all three ranking functions side by side.
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH ranking_comparison AS (
        SELECT
            emp_id,
            emp_name,
            degree,
            salary,
            ROW_NUMBER() OVER (
        ORDER BY salary DESC, emp_id) AS row_number_value, RANK() OVER (
        ORDER BY salary DESC) AS rank_value, DENSE_RANK() OVER (
        ORDER BY salary DESC) AS dense_rank_value
        FROM employees )
        SELECT *
        FROM ranking_comparison
        ORDER BY salary DESC, emp_id
        LIMIT 30;
    """

    show(con.execute(_sql).df(), "ROW_NUMBER vs RANK vs DENSE_RANK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 13 — Ranking inside each department with PARTITION BY

    **Concept:** `PARTITION BY` restarts the ranking inside each group. This is extremely useful for business questions like “top employees per department.”

    **Natural language query:** Rank employees by salary within each department.
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH dept_ranked AS (
        SELECT
            dept_id,
            emp_id,
            emp_name,
            degree,
            salary,
            ROW_NUMBER() OVER ( PARTITION BY dept_id
        ORDER BY salary DESC, emp_id ) AS dept_salary_position
        FROM employees )
        SELECT *
        FROM dept_ranked
        WHERE dept_salary_position <= 5
        ORDER BY dept_id, dept_salary_position;
    """

    show(con.execute(_sql).df(), "Top 5 salary positions inside each department", max_rows=40)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 14 — Top-N per department using WITH

    **Concept:** A ranking function is often placed inside a `WITH` query, then filtered outside.

    Why? Because SQL usually does not allow filtering directly on a window-function alias in the same SELECT level.

    **Natural language query:** Find the top 3 highest-paid employees in each department.
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH dept_ranked AS (
        SELECT
            dept_id,
            emp_id,
            emp_name,
            country,
            degree,
            salary,
            ROW_NUMBER() OVER ( PARTITION BY dept_id
        ORDER BY salary DESC, emp_id ) AS rn
        FROM employees )
        SELECT *
        FROM dept_ranked
        WHERE rn <= 3
        ORDER BY dept_id, rn;
    """

    show(con.execute(_sql).df(), "Top 3 employees per department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 15 — Top-N per country using WITH

    **Concept:** The same pattern works for any grouping column. Here, ranking restarts inside each country.

    **Natural language query:** Find the top 5 highest-paid employees in each country.
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH country_ranked AS (
        SELECT
            country,
            emp_id,
            emp_name,
            dept_id,
            degree,
            salary,
            ROW_NUMBER() OVER ( PARTITION BY country
        ORDER BY salary DESC, emp_id ) AS rn
        FROM employees )
        SELECT *
        FROM country_ranked
        WHERE rn <= 5
        ORDER BY country, rn;
    """

    show(con.execute(_sql).df(), "Top 5 employees per country", max_rows=35)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 16 — Plotting intuition: top salaries per department

    **Concept:** Top-N ranking is easier to understand when students can see the top positions visually.

    The plotting code is hidden in `helpers/plots.py`.
    """)
    return


@app.cell
def _(con, plot_top_n_per_dept):
    plot_top_n_per_dept(con, n=3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 17 — Intermediate+: find tied salaries

    **Concept:** Ties are where `RANK()` and `DENSE_RANK()` become important. If no ties exist, all three ranking functions look very similar.

    **Natural language query:** Which salary values occur most often?
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH salary_frequency AS (
        SELECT
            salary,
            COUNT(*) AS employees_with_same_salary
        FROM employees
        GROUP BY salary ), ranked_salary_frequency AS (
        SELECT
            salary,
            employees_with_same_salary,
            RANK() OVER (
        ORDER BY employees_with_same_salary DESC, salary DESC) AS frequency_rank
        FROM salary_frequency )
        SELECT *
        FROM ranked_salary_frequency
        WHERE frequency_rank <= 10
        ORDER BY frequency_rank, salary DESC;
    """

    show(con.execute(_sql).df(), "Most common salary values")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 18 — Intermediate+: top salary tiers using DENSE_RANK()

    **Concept:** `DENSE_RANK()` is excellent when you want the top distinct values, not just the top rows.

    **Natural language query:** Show all employees who are in the top 5 distinct salary levels.
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH salary_tiers AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            country,
            degree,
            salary,
            DENSE_RANK() OVER (
        ORDER BY salary DESC) AS salary_tier
        FROM employees )
        SELECT *
        FROM salary_tiers
        WHERE salary_tier <= 5
        ORDER BY salary_tier, emp_id;
    """

    show(con.execute(_sql).df(), "Employees in the top 5 distinct salary tiers", max_rows=50)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 19 — Intermediate+: best performer among high earners per department

    **Concept:** We can rank by multiple columns. This is common in business rules.

    Here we rank employees inside each department by:

    1. performance descending
    2. salary descending
    3. hire date ascending

    **Natural language query:** Who is the best overall employee candidate in each department based on performance, salary, and seniority?
    """)
    return


@app.cell
def _(con, show):
    _sql = """
        WITH department_candidates AS (
        SELECT
            dept_id,
            emp_id,
            emp_name,
            degree,
            salary,
            performance,
            hire_date,
            ROW_NUMBER() OVER ( PARTITION BY dept_id
        ORDER BY performance DESC, salary DESC, hire_date ASC, emp_id ) AS candidate_rank
        FROM employees )
        SELECT *
        FROM department_candidates
        WHERE candidate_rank <= 3
        ORDER BY dept_id, candidate_rank;
    """

    show(con.execute(_sql).df(), "Top 3 candidate employees per department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 20 — Intermediate+: compare employee salary to department average, then rank the gap

    **Concept:** Ranking functions become more powerful when combined with analytical calculations.

    First, we calculate department average salary. Then we calculate how far each employee is above that average. Finally, we rank those gaps.

    **Natural language query:** Which employees are most above their own department average salary?
    """)
    return


@app.cell
def _(con, plot_rank_curve, show):
    _sql = """
        WITH dept_avg AS (
        SELECT
            dept_id,
            ROUND(AVG(salary), 0) AS dept_avg_salary
        FROM employees
        GROUP BY dept_id ), employee_gap AS (
        SELECT
            e.dept_id,
            e.emp_id,
            e.emp_name,
            e.degree,
            e.salary,
            d.dept_avg_salary,
            e.salary - d.dept_avg_salary AS salary_above_dept_avg
        FROM employees e
        JOIN dept_avg d ON e.dept_id = d.dept_id ), ranked_gap AS (
        SELECT
            *,
            RANK() OVER (
        ORDER BY salary_above_dept_avg DESC) AS gap_rank
        FROM employee_gap )
        SELECT *
        FROM ranked_gap
        WHERE gap_rank <= 20
        ORDER BY gap_rank, emp_id;
    """

    show(con.execute(_sql).df(), "Employees most above department average salary")

    plot_rank_curve(con)
    return


if __name__ == "__main__":
    app.run()
