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
    # 🦆 Mastering SQL Sub-Queries with `WITH` (CTEs)
    ### A Beginner-Friendly Tutorial using DuckDB

    ---

    ## 🎯 What You'll Learn

    | Lesson | Concept |
    |--------|------------------------------------------|
    | 1 | Why sub-queries exist & what a CTE is |
    | 2 | Basic `WITH` syntax |
    | 3 | Filtering with a CTE |
    | 4 | Aggregating inside a CTE |
    | 5 | Chaining multiple CTEs |
    | 6 | Joining a CTE back to the base table |
    | 7 | Nesting logic step-by-step |
    | 8 | Ranking with `RANK()` & `DENSE_RANK()` |

    ---

    > **CTE** stands for **Common Table Expression**.  
    > Think of it as giving a *nickname* to a temporary result set so you can reference it cleanly later in the same query.

    ```sql
    WITH my_temp_table AS (
        SELECT ...   -- your sub-query lives here
    )
    SELECT * FROM my_temp_table;   -- then you use it here
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 1 — Setup: Install DuckDB & Rendering Helper

    We install **DuckDB** (an in-process SQL engine — no server needed!) and define a small helper function `show()` that renders query results as a beautiful HTML table.  

    > **Run this cell first.** The `show()` helper is used in every subsequent cell.
    """)
    return


@app.cell
def _():
    # ── Install & import ──────────────────────────────────────────────────────────

    import duckdb
    from IPython.display import display, HTML

    # ── Connect (in-memory database) ─────────────────────────────────────────────
    con = duckdb.connect()

    # ── Rendering helper (kept here, reused everywhere) ──────────────────────────
    def show(sql, title=None):
        """Execute SQL and render results as a styled HTML table."""
        df = con.execute(sql).df()

        # ── Build header ──
        header_cells = "".join(f"<th>{c}</th>" for c in df.columns)
        header = f"<thead><tr>{header_cells}</tr></thead>"

        # ── Build rows ──
        rows = ""
        for i, row in df.iterrows():
            cls = "even" if i % 2 == 0 else "odd"
            cells = "".join(f"<td>{v}</td>" for v in row)
            rows += f"<tr class='{cls}'>{cells}</tr>"
        body = f"<tbody>{rows}</tbody>"

        # ── Caption ──
        caption = f"<caption>{title}</caption>" if title else ""
        row_count = f"<p class='meta'>{len(df)} row(s) returned</p>"

        html = f"""
        <style>
          .dq-wrap  {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 18px 0; }}
          .dq-wrap caption {{
            caption-side: top;
            font-size: 1.05em;
            font-weight: 700;
            color: #1a1a2e;
            text-align: left;
            padding: 6px 0 8px 2px;
            letter-spacing: .3px;
          }}
          .dq-wrap table {{
            border-collapse: collapse;
            width: 100%;
            box-shadow: 0 2px 8px rgba(0,0,0,.12);
            border-radius: 8px;
            overflow: hidden;
            font-size: .92em;
          }}
          .dq-wrap th {{
            background: #1a1a2e;
            color: #e2e8f0;
            padding: 10px 14px;
            text-align: left;
            font-weight: 600;
            letter-spacing: .4px;
            text-transform: uppercase;
            font-size: .82em;
          }}
          .dq-wrap td {{ padding: 9px 14px; color: #2d3748; }}
          .dq-wrap tr.even td {{ background: #f7f9fc; }}
          .dq-wrap tr.odd  td {{ background: #ffffff; }}
          .dq-wrap tr:hover td {{ background: #ebf4ff; transition: background .15s; }}
          .dq-wrap .meta  {{ font-size:.78em; color:#718096; margin:4px 2px 0; }}
        </style>
        <div class='dq-wrap'>
          <table>{caption}{header}{body}</table>
          {row_count}
        </div>"""
        display(HTML(html))

    print("✅ DuckDB", duckdb.__version__, "ready. show() helper loaded.")
    return (con, show)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 2 — Create the Dataset: `employees` (20 rows)

    We'll work with a single table throughout the entire tutorial.

    | Column | Description |
    |---|---|
    | `emp_id` | Unique employee ID |
    | `name` | Employee name |
    | `department` | Department they belong to |
    | `job_title` | Their role |
    | `salary` | Annual salary (USD) |
    | `years_exp` | Years of experience |
    | `hire_year` | Year they were hired |
    | `rating` | Annual performance rating (1–5) |
    """)
    return


@app.cell
def _(con, show):
    con.execute("""
        CREATE
        OR REPLACE TABLE employees AS
        SELECT *
        FROM (
        VALUES
            (1, 'Alice Chen', 'Engineering', 'Senior Engineer', 120000, 8, 2016, 5),
            (2, 'Bob Martinez', 'Engineering', 'Junior Engineer', 72000, 2, 2022, 3),
            (3, 'Clara Osei', 'Engineering', 'Lead Engineer', 145000, 12, 2012, 5),
            (4, 'David Kim', 'Engineering', 'Junior Engineer', 68000, 1, 2023, 4),
            (5, 'Eva Rossi', 'Marketing', 'Marketing Manager', 105000, 7, 2017, 4),
            (6, 'Felix Nguyen', 'Marketing', 'Analyst', 62000, 3, 2021, 3),
            (7, 'Grace Patel', 'Marketing', 'Analyst', 65000, 4, 2020, 4),
            (8, 'Hiro Tanaka', 'Marketing', 'Director', 135000, 11, 2013, 5),
            (9, 'Isla Scott', 'HR', 'HR Manager', 90000, 6, 2018, 4),
            (10, 'James Okafor', 'HR', 'Recruiter', 58000, 2, 2022, 3),
            (11, 'Karen Li', 'HR', 'Recruiter', 60000, 3, 2021, 5),
            (12, 'Leo Diaz', 'Finance', 'CFO', 200000, 15, 2009, 5),
            (13, 'Mia Brown', 'Finance', 'Accountant', 78000, 4, 2020, 3),
            (14, 'Nate Wilson', 'Finance', 'Accountant', 80000, 5, 2019, 4),
            (15, 'Olivia Turner', 'Finance', 'Financial Analyst', 92000, 6, 2018, 4),
            (16, 'Paul Adams', 'Engineering', 'Staff Engineer', 160000, 14, 2010, 5),
            (17, 'Quinn Bell', 'Engineering', 'Engineer', 95000, 5, 2019, 3),
            (18, 'Rachel Green', 'Sales', 'Sales Rep', 70000, 3, 2021, 4),
            (19, 'Sam Hughes', 'Sales', 'Sales Manager', 110000, 9, 2015, 5),
            (20, 'Tina Ford', 'Sales', 'Sales Rep', 67000, 2, 2022, 2) ) t(emp_id,
            name,
            department,
            job_title,
            salary,
            years_exp,
            hire_year,
            rating);
    """)

    show("""
        SELECT *
        FROM employees;
    """, title="📋 Full employees table (20 rows)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 3 — Lesson 1: Why Do We Need `WITH`?

    ### The Problem 🤔

    Imagine you want to find employees who earn **more than the company average salary**.  
    Without CTEs, you'd need a messy nested query:

    ```sql
    -- ❌ Hard to read — sub-query buried inside
    SELECT name, salary
    FROM employees
    WHERE salary > (SELECT AVG(salary) FROM employees);
    ```

    With `WITH`, we **name** that inner calculation and make the query self-documenting:

    ```sql
    -- ✅ Clean & readable
    WITH avg_salary AS (
        SELECT AVG(salary) AS avg_sal FROM employees
    )
    SELECT name, salary
    FROM employees, avg_salary
    WHERE salary > avg_sal;
    ```

    Both do the **same thing** — but the second version reads like English. 👇
    """)
    return


@app.cell
def _(show):
    show("""
        WITH avg_salary AS (
        SELECT ROUND(AVG(salary), 2) AS avg_sal
        FROM employees )
        SELECT
            e.name,
            e.department,
            e.salary,
            a.avg_sal AS company_avg,
            e.salary - a.avg_sal AS diff_from_avg
        FROM employees e, avg_salary a
        WHERE e.salary > a.avg_sal
        ORDER BY e.salary DESC;
    """,
    title="Lesson 1 — Employees earning above company average")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 4 — Lesson 2: Basic `WITH` Syntax — Filtering

    **Goal:** Find all employees hired before 2020 who also have a rating ≥ 4.

    We first build a CTE of *veteran employees* (hired before 2020), then filter for high performers.

    ```
    Step 1 ─► CTE  →  veteran_employees  (hired before 2020)
    Step 2 ─► main query filters CTE  → rating >= 4
    ```
    """)
    return


@app.cell
def _(show):
    show("""
        WITH veteran_employees AS ( /* Step 1: isolate employees hired before 2020 */
        SELECT
            emp_id,
            name,
            department,
            hire_year,
            salary,
            rating
        FROM employees
        WHERE hire_year < 2020 ) /* Step 2: from that subset, keep only top performers */
        SELECT
            name,
            department,
            hire_year,
            salary,
            rating
        FROM veteran_employees
        WHERE rating >= 4
        ORDER BY hire_year ASC;
    """,
    title="Lesson 2 — Veteran employees (pre-2020) with rating ≥ 4")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 5 — Lesson 3: Aggregating Inside a CTE

    **Goal:** Show each department's headcount, total payroll, and average salary.

    We push the `GROUP BY` logic inside the CTE. The outer query then just selects from it — clean and reusable.

    ```
    CTE  →  dept_stats  (GROUP BY department)
    Main →  SELECT * FROM dept_stats ORDER BY avg_salary DESC
    ```
    """)
    return


@app.cell
def _(show):
    show("""
        WITH dept_stats AS (
        SELECT
            department,
            COUNT(*) AS headcount,
            SUM(salary) AS total_payroll,
            ROUND(AVG(salary), 0) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY department )
        SELECT
            department,
            headcount,
            '$' || total_payroll AS total_payroll,
            '$' || avg_salary AS avg_salary,
            '$' || min_salary AS min_salary,
            '$' || max_salary AS max_salary
        FROM dept_stats
        ORDER BY avg_salary DESC;
    """,
    title="Lesson 3 — Department-level payroll summary")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 6 — Lesson 4: Chaining Two CTEs

    **Goal:** Find departments whose *average salary* is above the *overall company average*.

    This requires **two** CTEs, one after another, separated by a comma:

    ```sql
    WITH
      cte_one AS ( ... ),       -- first CTE
      cte_two AS ( ... )        -- second CTE (can reference cte_one!)
    SELECT ... FROM cte_two;
    ```

    ```
    CTE 1  →  dept_avg      (avg salary per department)
    CTE 2  →  company_avg   (single overall average)
    Main   →  JOIN both, keep departments above the bar
    ```
    """)
    return


@app.cell
def _(show):
    show("""
        WITH dept_avg AS ( /* CTE 1: average salary per department */
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_dept_salary
        FROM employees
        GROUP BY department ), company_avg AS ( /* CTE 2: single overall average (references base table, not CTE 1) */
        SELECT ROUND(AVG(salary), 0) AS avg_company_salary
        FROM employees ) /* Main query: use both CTEs together */
        SELECT
            d.department,
            d.avg_dept_salary,
            c.avg_company_salary,
            d.avg_dept_salary - c.avg_company_salary AS premium
        FROM dept_avg d
        CROSS
        JOIN company_avg c
        WHERE d.avg_dept_salary > c.avg_company_salary
        ORDER BY premium DESC;
    """,
    title="Lesson 4 — Departments above the company-wide salary average")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 7 — Lesson 5: Joining a CTE back to the Base Table

    **Goal:** For every employee, show their salary **and** their department's average — side by side.

    This is one of the most practical CTE patterns: compute a summary in a CTE, then **JOIN it** back to the detail rows.

    ```
    CTE  →  dept_avg   (avg per department)
    Main →  JOIN employees ON department  → show both individual + dept average
    ```
    """)
    return


@app.cell
def _(show):
    show("""
        WITH dept_avg AS (
        SELECT
            department,
            ROUND(AVG(salary), 0) AS avg_dept_salary
        FROM employees
        GROUP BY department )
        SELECT
            e.name,
            e.department,
            e.salary AS individual_salary,
            d.avg_dept_salary,
            e.salary - d.avg_dept_salary AS vs_dept_avg,
            CASE WHEN e.salary > d.avg_dept_salary THEN '▲ Above' WHEN e.salary < d.avg_dept_salary THEN '▼ Below' ELSE '= Equal' END AS position
        FROM employees e
        JOIN dept_avg d ON e.department = d.department
        ORDER BY e.department, e.salary DESC;
    """,
    title="Lesson 5 — Every employee vs. their department average")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 8 — Lesson 6: Building Logic Step-by-Step (3 CTEs)

    **Goal:** Find the **top earner in each department**, then show only those top earners who also have a rating of 5.

    We solve it in three clear steps:

    ```
    CTE 1  →  dept_max_salary   (MAX salary per department)
    CTE 2  →  top_earners       (join back employees to get who owns that salary)
    CTE 3  →  elite             (filter top_earners where rating = 5)
    Main   →  SELECT from elite
    ```

    > 💡 **Key insight:** each CTE can reference *any* previously defined CTE — you're building a query pipeline!
    """)
    return


@app.cell
def _(show):
    show("""
        WITH dept_max_salary AS ( /* CTE 1: highest salary in each department */
        SELECT
            department,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY department ), top_earners AS ( /* CTE 2: match employees to their dept's max salary */
        SELECT
            e.name,
            e.department,
            e.salary,
            e.rating,
            e.job_title
        FROM employees e
        JOIN dept_max_salary m ON e.department = m.department
        AND e.salary = m.max_salary ), elite AS ( /* CTE 3: among top earners, keep only perfect raters */
        SELECT *
        FROM top_earners
        WHERE rating = 5 )
        SELECT
            name,
            department,
            job_title,
            salary,
            rating,
            '🏆 Top earner + perfect rating' AS badge
        FROM elite
        ORDER BY salary DESC;
    """,
    title="Lesson 6 — Top earner per department who also has a perfect rating")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 9 — Lesson 7: Practical CTE — Salary Bands

    **Goal:** Classify every employee into a salary band, then count how many fall into each band.

    ```
    CTE 1  →  banded   (assign each employee a band with CASE)
    Main   →  GROUP BY band, count and sum
    ```

    This pattern — *derive a column in a CTE, then aggregate by it* — is extremely common in real analytics work.
    """)
    return


@app.cell
def _(show):
    show("""
        WITH banded AS (
        SELECT
            name,
            department,
            salary,
            CASE WHEN salary < 70000 THEN '💛 Entry  (<$70k)' WHEN salary >= 70000
        AND salary < 100000 THEN '🟠 Mid    ($70k-$100k)' WHEN salary >= 100000
        AND salary < 140000 THEN '🔵 Senior ($100k-$140k)' ELSE '🟣 Executive ($140k+)' END AS salary_band
        FROM employees )
        SELECT
            salary_band,
            COUNT(*) AS employee_count,
            MIN(salary) AS band_min,
            MAX(salary) AS band_max,
            ROUND(AVG(salary),0) AS band_avg
        FROM banded
        GROUP BY salary_band
        ORDER BY band_min;
    """,
    title="Lesson 7 — Employee count per salary band")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 10 — Lesson 8: Intro to Window / Ranking Functions with `WITH`

    Now we step it up! **Ranking functions** let you rank rows *within groups* without collapsing them (unlike `GROUP BY`).

    | Function | Behaviour when tied |
    |---|---|
    | `ROW_NUMBER()` | Always unique — ties broken arbitrarily |
    | `RANK()` | Ties share a rank; next rank **skips** (1,1,3) |
    | `DENSE_RANK()` | Ties share a rank; next rank **does not skip** (1,1,2) |

    **Goal:** Rank every employee by salary *within their department*.

    ```
    CTE  →  ranked   (add RANK() and DENSE_RANK() columns)
    Main →  SELECT everything from ranked
    ```
    """)
    return


@app.cell
def _(show):
    show("""
        WITH ranked AS (
        SELECT
            name,
            department,
            job_title,
            salary,
            ROW_NUMBER() OVER (PARTITION BY department
        ORDER BY salary DESC) AS row_num, RANK() OVER (PARTITION BY department
        ORDER BY salary DESC) AS RANK, DENSE_RANK() OVER (PARTITION BY department
        ORDER BY salary DESC) AS DENSE_RANK
        FROM employees )
        SELECT *
        FROM ranked
        ORDER BY department, RANK;
    """,
    title="Lesson 8 — Salary rank within each department (ROW_NUMBER vs RANK vs DENSE_RANK)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 11 — Lesson 9: Filter by Rank — `#1 in Department`

    **The golden pattern:** compute ranks inside a CTE, then filter `WHERE rank = 1` in the outer query.

    > ⚠️ You **cannot** write `WHERE RANK() = 1` directly in a single query — window functions aren't allowed in `WHERE`. A CTE elegantly solves this!

    **Goal:** Show the **#1 highest-paid employee in each department**.
    """)
    return


@app.cell
def _(show):
    show("""
        WITH dept_ranked AS (
        SELECT
            name,
            department,
            job_title,
            salary,
            years_exp,
            rating,
            DENSE_RANK() OVER (PARTITION BY department
        ORDER BY salary DESC) AS sal_rank
        FROM employees )
        SELECT
            department,
            name,
            job_title,
            salary,
            years_exp,
            rating,
            '🥇 #1' AS dept_rank
        FROM dept_ranked
        WHERE sal_rank = 1
        ORDER BY salary DESC;
    """,
    title="Lesson 9 — The highest-paid employee in each department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 12 — 🏁 Grand Finale: Everything Together

    Let's combine **all concepts** in one elegant query:

    1. Compute company-wide average salary  
    2. Classify employees into salary bands  
    3. Rank by salary within department  
    4. Show only top-2 per department who earn above the company average

    ```
    CTE 1  →  company_avg   (overall average)
    CTE 2  →  enriched      (band + above/below avg flag)
    CTE 3  →  ranked        (DENSE_RANK by salary per dept)
    Main   →  top-2 per dept, above company avg, ordered nicely
    ```
    """)
    return


@app.cell
def _(show):
    show("""
        WITH company_avg AS ( /* Step 1: overall company average */
        SELECT ROUND(AVG(salary), 0) AS avg_sal
        FROM employees ), enriched AS ( /* Step 2: attach avg, add band & flag */
        SELECT
            e.emp_id,
            e.name,
            e.department,
            e.job_title,
            e.salary,
            e.rating,
            c.avg_sal,
            CASE WHEN e.salary < 70000 THEN '💛 Entry' WHEN e.salary < 100000 THEN '🟠 Mid' WHEN e.salary < 140000 THEN '🔵 Senior' ELSE '🟣 Executive' END AS band,
            CASE WHEN e.salary > c.avg_sal THEN '✅ Yes' ELSE '❌ No' END AS above_company_avg
        FROM employees e
        CROSS
        JOIN company_avg c ), ranked AS ( /* Step 3: rank within department by salary */
        SELECT
            *,
            DENSE_RANK() OVER (PARTITION BY department
        ORDER BY salary DESC) AS dept_rank
        FROM enriched ) /* Final: top-2 per department, only those above company avg */
        SELECT
            dept_rank AS "🏅 Rank",
            department,
            name,
            job_title,
            salary,
            band,
            rating,
            above_company_avg
        FROM ranked
        WHERE dept_rank <= 2
        AND above_company_avg = '✅ Yes'
        ORDER BY department, dept_rank;
    """,
    title="🏁 Grand Finale — Top-2 earners per dept who are above the company average")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 🎓 Summary — What You Learned

    | Cell | Pattern | Key Idea |
    |------|---------|----------|
    | 3 | Basic `WITH` | Name a sub-query to reuse it cleanly |
    | 4 | Filter in CTE | Pre-filter rows before the main query |
    | 5 | Aggregate in CTE | Push `GROUP BY` into the CTE |
    | 6 | Two CTEs | Chain CTEs with a comma |
    | 7 | JOIN CTE to base | Attach summary stats to detail rows |
    | 8 | Three CTEs | Build multi-step analytics pipelines |
    | 9 | Derive + aggregate | Create columns in CTE, group by them |
    | 10 | `RANK()` / `DENSE_RANK()` | Rank rows within partitions |
    | 11 | Filter on rank | `WHERE rank = 1` requires a CTE |
    | 12 | Everything together | Compose all patterns into one query |

    ---

    > **Next steps:** Explore recursive CTEs (`WITH RECURSIVE`) for hierarchical data, or try `NTILE()`, `PERCENT_RANK()`, and `LAG()` / `LEAD()` window functions!
    """)
    return


if __name__ == "__main__":
    app.run()
