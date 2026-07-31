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
    # 🏆 Ranking Functions in SQL — A Complete Tutorial
    ### Using DuckDB + Python in Jupyter

    ---

    **What you'll learn in 20 cells:**
    - `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()` — how they work and where they differ
    - `WITH` clauses (CTEs) to write clean, readable SQL
    - Real-world patterns: leaderboards, top-N per group, salary tiers, composite scoring

    **Dataset:** 1,000 employees · salary · department · country · degree · performance · hire_date

    > 🟢 **Cells 2–10** — Basics (SQL foundations, no ranking yet)
    > 🟡 **Cells 11–15** — Intermediate (ranking functions introduced)
    > 🔴 **Cells 16–20** — Intermediate+ (ranking + CTEs for real analytics)
    """)
    return


@app.cell
def _(df):
    # ─── Cell 1 · Setup & show() helper ────────────────────────────────────────
    # !pip install duckdb   # uncomment if needed

    import duckdb
    import pandas as pd
    from IPython.display import display, HTML

    # ── show() ─────────────────────────────────────────────────────────────────
    # All SQL results render through show(): dark navy headers, alternating rows,
    # hover highlight, row-count footer.  Rendering code lives here once.
    # ───────────────────────────────────────────────────────────────────────────
    CSS = ".sqlt{font-family:'Segoe UI',Helvetica,sans-serif;margin:10px 0 20px}.sqlt .tbl-title{font-size:.80em;font-weight:700;letter-spacing:.08em;color:#8ab4f8;text-transform:uppercase;margin-bottom:6px}.sqlt table{border-collapse:collapse;width:100%;box-shadow:0 2px 14px rgba(0,0,0,.40);border-radius:8px;overflow:hidden}.sqlt th{background:#0d1b40;color:#e8f0fe;padding:9px 14px;text-align:left;font-size:.77em;letter-spacing:.06em;text-transform:uppercase;border-bottom:2px solid #1a3a8f}.sqlt td{padding:7px 14px;font-size:.85em;color:#d2d8e8;border-bottom:1px solid #1e2d55}.sqlt tr.even td{background:#101c3d}.sqlt tr.odd td{background:#0c1530}.sqlt tr:hover td{background:#1a3a6b;color:#fff;transition:.15s}.sqlt .footer{font-size:.74em;color:#8ab4f8;margin-top:5px;text-align:right}"

    def show(df, title=""):
        n    = len(df)
        cols = df.columns.tolist()
        header = "".join(f"<th>{c}</th>" for c in cols)
        rows_html = ""
        for idx, (_, row) in enumerate(df.iterrows()):
            cls = "even" if idx % 2 == 0 else "odd"
            tds = "".join(f"<td>{v}</td>" for v in row)
            rows_html += f'<tr class="{cls}">{tds}</tr>'
        title_block = f"<div class='tbl-title'>{title}</div>" if title else ""
        html = (
            f"<style>{CSS}</style>"
            f"<div class='sqlt'>{title_block}"
            f"<table><thead><tr>{header}</tr></thead>"
            f"<tbody>{rows_html}</tbody></table>"
            f"<div class='footer'>{n:,} row{'s' if n != 1 else ''} returned</div>"
            f"</div>"
        )
        display(HTML(html))

    print("✅  DuckDB ready. show() helper loaded.")

    return (duckdb, show)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🟢 Part 1 — Basics (Cells 2–10)
    ### Cell 2 · Load the Dataset

    We load `employees.csv` into an **in-memory DuckDB table** using SQL.
    DuckDB's `read_csv_auto` infers types automatically — no pandas needed.

    | Column | Description |
    |---|---|
    | `emp_id` | 1 – 1000 |
    | `emp_name` | Full name |
    | `dept_id` | SALES · BUSINESS · AI · MARKETING · SOFTWARE · HARDWARE |
    | `country` | USA · CANADA · GERMANY · CHINA · INDIA |
    | `salary` | Integer 80,000 – 280,000 |
    | `degree` | BA · BS · MS · MSIS · PHD |
    | `performance` | 1–10 yearly score |
    | `hire_date` | Spans 3 years |
    """)
    return


@app.cell
def _(duckdb, show):
    # ─── Cell 2 · Load the Dataset ─────────────────────────────────────────────
    con = duckdb.connect()   # fresh in-memory DuckDB

    con.execute("""
        CREATE TABLE employees AS
        SELECT *
        FROM read_csv_auto('employees.csv');
    """)

    _df = con.execute("""
        SELECT COUNT(*) AS total_employees
        FROM employees;
    """).df()
    show(_df, "Row Count")

    return (con, _df)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 3 · Schema & Sample Rows

    Before writing complex queries, always understand your data.
    `DESCRIBE` shows column names and types; `LIMIT` gives a quick preview.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 3 · Schema & Sample ───────────────────────────────────────────────
    df_schema = con.execute("""
        DESCRIBE employees;
    """).df()
    show(df_schema[['column_name','column_type']], "Table Schema")

    df_sample = con.execute("""
        SELECT
            emp_id,
            emp_name,
            dept_id,
            country,
            gender,
            salary,
            degree,
            performance,
            hire_date
        FROM employees
        LIMIT 8;
    """).df()
    show(df_sample, "First 8 Rows")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 4 · Department Distribution

    `GROUP BY` + `ORDER BY` for a quick headcount summary.
    This confirms the dataset matches our target distribution.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 4 · Department Distribution ──────────────────────────────────────
    _df = con.execute("""
        SELECT
            dept_id AS Department,
            COUNT(*) AS Headcount,
            ROUND(COUNT(*) * 100.0 / 1000, 1) AS Pct
        FROM employees
        GROUP BY dept_id
        ORDER BY Headcount DESC;
    """).df()
    show(_df, "Employees per Department")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 5 · Salary by Degree

    **Key insight:** PHD holders earn the most — by design.
    `AVG`, `MIN`, `MAX` reveal the salary spread per education level.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 5 · Salary Statistics by Degree ───────────────────────────────────
    _df = con.execute("""
        SELECT
            degree AS Degree,
            COUNT(*) AS COUNT,
            '$' || FORMAT('{:,}', CAST(AVG(salary) AS INT)) AS Avg_Salary,
            '$' || FORMAT('{:,}', MIN(salary)) AS Min_Salary,
            '$' || FORMAT('{:,}', MAX(salary)) AS Max_Salary
        FROM employees
        GROUP BY degree
        ORDER BY AVG(salary) DESC;
    """).df()
    show(_df, "Salary by Degree — PHD earns the most")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 6 · Country & Gender Breakdown

    DuckDB's `FILTER` clause enables conditional aggregation inline — no `CASE WHEN` needed.

    ```sql
    COUNT(*) FILTER (gender = 'MALE')   -- counts only males
    ```
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 6 · Country x Gender ──────────────────────────────────────────────
    _df = con.execute("""
        SELECT
            country AS Country,
            COUNT(*) AS Total,
            COUNT(*) FILTER (gender = 'MALE') AS Male,
            COUNT(*) FILTER (gender = 'FEMALE') AS Female,
            CAST(ROUND(AVG(salary)) AS INT) AS Avg_Salary
        FROM employees
        GROUP BY country
        ORDER BY Total DESC;
    """).df()
    show(_df, "Employees by Country & Gender")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 7 · Top 10 Highest-Paid (The Simple Way)

    `ORDER BY salary DESC LIMIT 10` gives a global top 10 easily.

    > ⚠️ **Limitation:** This can't give you the **top 3 per department**.
    > That's exactly what ranking functions solve — coming soon!
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 7 · Top 10 Highest-Paid ───────────────────────────────────────────
    _df = con.execute("""
        SELECT
            emp_id,
            emp_name,
            dept_id,
            country,
            degree,
            '$' || FORMAT('{:,}', salary) AS Salary,
            performance
        FROM employees
        ORDER BY salary DESC
        LIMIT 10;
    """).df()
    show(_df, "Top 10 Highest-Paid Employees")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 8 · Performance by Department

    Which teams score highest? Using `FILTER` to count high (≥ 8) and low (≤ 3) performers.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 8 · Performance by Department ─────────────────────────────────────
    _df = con.execute("""
        SELECT
            dept_id AS Department,
            COUNT(*) AS Headcount,
            ROUND(AVG(performance), 2) AS Avg_Performance,
            COUNT(*) FILTER (performance >= 8) AS High_Performers,
            COUNT(*) FILTER (performance <= 3) AS Low_Performers
        FROM employees
        GROUP BY dept_id
        ORDER BY Avg_Performance DESC;
    """).df()
    show(_df, "Performance by Department")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 9 · Subquery Warm-Up — Above-Average Earners

    Our first **subquery**: employees who earn more than the company average.
    The inner query computes the average; the outer query filters on it.

    ```sql
    WHERE salary > (SELECT AVG(salary) FROM employees)
                     └── returns a single number
    ```

    This works, but the inner query is buried and can't be reused. Next cell: the cleaner `WITH` version.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 9 · Above-Average Earners (inline subquery style) ─────────────────
    avg_df = con.execute(
        """
            SELECT CAST(ROUND(AVG(salary)) AS INT) AS Company_Avg
            FROM employees;
        """
    ).df()
    show(avg_df, "Company Average Salary")

    _df = con.execute("""
        SELECT
            emp_name,
            dept_id,
            degree,
            '$' || FORMAT('{:,}', salary) AS Salary
        FROM employees
        WHERE salary > (
        SELECT AVG(salary)
        FROM employees)
        ORDER BY salary DESC
        LIMIT 15;
    """).df()
    show(_df, "Above-Average Earners — top 15 shown")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 10 · Introducing `WITH` — Common Table Expressions

    The **`WITH` clause** (CTE = Common Table Expression) lets you:
    - Give a subquery a **name** so SQL reads like plain English
    - **Reuse** that result multiple times without repeating it
    - **Chain** multiple named steps (pipeline style)

    ```sql
    WITH my_cte AS (
        SELECT ...    -- subquery here
    )
    SELECT * FROM my_cte WHERE ...
    ```

    > 💡 Think of a CTE as a temporary named view — exists only for this query.
    > **From here on, every subquery uses `WITH`.**
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 10 · Same Query — Rewritten with WITH ─────────────────────────────
    _df = con.execute("""
        WITH company_avg AS (
        SELECT AVG(salary) AS avg_sal
        FROM employees )
        SELECT
            e.emp_name,
            e.dept_id,
            e.degree,
            '$' || FORMAT('{:,}', e.salary) AS Salary,
            '$' || FORMAT('{:,}', CAST(c.avg_sal AS INT)) AS Company_Avg
        FROM employees AS e
        CROSS
        JOIN company_avg AS c
        WHERE e.salary > c.avg_sal
        ORDER BY e.salary DESC
        LIMIT 15;
    """).df()
    show(_df, """
        WITH version — Above-Average Earners (named, readable, reusable);
    """)

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ---
    ## 🟡 Part 2 — Intermediate: Ranking Functions (Cells 11–15)

    ### 🎯 The Core Idea

    You want to **rank employees by salary within each department**.
    `ORDER BY` sorts rows but doesn't assign a rank *number* to each one.

    | Function | Behavior | Values 300, 300, 250 |
    |---|---|---|
    | `ROW_NUMBER()` | Always unique | 1, 2, 3 |
    | `RANK()` | Ties share rank; next rank **skips** | 1, 1, 3 |
    | `DENSE_RANK()` | Ties share rank; next rank **doesn't skip** | 1, 1, 2 |

    ### 🔧 The Syntax Template

    ```sql
    FUNCTION() OVER ( PARTITION BY group_col  ORDER BY sort_col DESC )
      ↑ fn          ↑ keyword  ↑ reset per group        ↑ who is rank 1?
    ```

    - **`OVER()`** — marks this as a *window* function (operates across rows)
    - **`PARTITION BY`** — resets the rank counter per group
    - **`ORDER BY`** inside `OVER()` — determines ranking order
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 11 · `ROW_NUMBER()` — Always Unique, Never Ties

    `ROW_NUMBER()` counts rows in sorted order: 1, 2, 3 …
    Even if two employees earn the **exact same salary**, they get **different numbers**.

    > 🎽 Like jersey numbers — every player gets a unique one, no matter how equal.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 11 · ROW_NUMBER() ─────────────────────────────────────────────────
    _df = con.execute("""
        WITH ranked AS (
        SELECT
            emp_name,
            dept_id,
            salary,
            ROW_NUMBER() OVER ( PARTITION BY dept_id /* restart at 1 per department */
        ORDER BY salary DESC /* highest salary = rank 1 */ ) AS row_num
        FROM employees )
        SELECT *
        FROM ranked
        WHERE dept_id IN ('AI', 'SALES')
        ORDER BY dept_id, row_num
        LIMIT 20;
    """).df()
    show(_df, "ROW_NUMBER() — Rank within AI & SALES by Salary")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 12 · `RANK()` — Ties Share a Rank, Next Rank Skips

    When two employees earn the same salary, both get rank 1.
    The **next employee skips to rank 3** — the gap shows how many tied.

    > 🏆 Olympic podium: two Gold medalists → next athlete gets Bronze (rank 3).
    > There is no Silver. The skip reveals the size of the tie.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 12 · RANK() ───────────────────────────────────────────────────────
    _df = con.execute("""
        WITH dept_ranked AS (
        SELECT
            emp_name,
            dept_id,
            salary,
            RANK() OVER ( PARTITION BY dept_id
        ORDER BY salary DESC ) AS rnk
        FROM employees
        WHERE dept_id = 'BUSINESS' )
        SELECT *
        FROM dept_ranked
        ORDER BY rnk
        LIMIT 20;
    """).df()
    show(_df, "RANK() within BUSINESS — notice rank jumps after ties")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 13 · `DENSE_RANK()` — Ties Share a Rank, No Gaps

    `DENSE_RANK()` is like `RANK()` but **never skips a number**.
    Two employees at the same salary both get rank 1; the next one gets rank **2** (not 3).

    > 📚 Class-standing style: two students score 98 → both are #1.
    > The next student is #2 — not #3. No rank is skipped.

    Use `DENSE_RANK` when you want clean tier numbers (Tier 1, Tier 2…).
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 13 · DENSE_RANK() ─────────────────────────────────────────────────
    _df = con.execute("""
        WITH comparison AS (
        SELECT
            emp_name,
            dept_id,
            salary,
            RANK() OVER (PARTITION BY dept_id
        ORDER BY salary DESC) AS rnk, DENSE_RANK() OVER (PARTITION BY dept_id
        ORDER BY salary DESC) AS dense_rnk, ROW_NUMBER() OVER (PARTITION BY dept_id
        ORDER BY salary DESC) AS row_num
        FROM employees
        WHERE dept_id = 'MARKETING' )
        SELECT *
        FROM comparison
        ORDER BY rnk
        LIMIT 20;
    """).df()
    show(_df, "MARKETING — All 3 functions side-by-side. Spot the differences!")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 14 · The Definitive Side-by-Side Comparison

    All three on the same data makes the difference crystal clear:

    ```
    Salary:       300   300   250   250   200
    ROW_NUMBER:     1     2     3     4     5   always unique
    RANK:           1     1     3     3     5   ties same, then jumps
    DENSE_RANK:     1     1     2     2     3   ties same, no jump
    ```

    Where `RANK ≠ DENSE_RANK` is exactly where ties exist.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 14 · Side-by-Side Global Salary Ranking ───────────────────────────
    _df = con.execute("""
        WITH all_ranked AS (
        SELECT
            emp_name,
            dept_id,
            salary,
            ROW_NUMBER() OVER (
        ORDER BY salary DESC) AS ROW_NUMBER, RANK() OVER (
        ORDER BY salary DESC) AS RANK, DENSE_RANK() OVER (
        ORDER BY salary DESC) AS DENSE_RANK
        FROM employees )
        SELECT *
        FROM all_ranked
        WHERE RANK <= 30
        ORDER BY salary DESC
        LIMIT 25;
    """).df()
    show(_df, "Global Salary — ROW_NUMBER vs RANK vs DENSE_RANK (top 30 by rank)")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 15 · Top-N Per Group — The Most Common Ranking Pattern

    **Problem:** Top 3 earners in each department.
    `ORDER BY + LIMIT` only gives a *global* top 3.

    **The classic pattern** (appears in virtually every SQL interview):
    1. `ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)` in a CTE
    2. Filter `WHERE salary_rank <= 3` in the outer query

    > 🧠 `WHERE` cannot reference window functions directly — you **must** wrap
    > the window function in a CTE (or subquery) first.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 15 · Top 3 Earners per Department ─────────────────────────────────
    _df = con.execute("""
        WITH dept_ranked AS (
        SELECT
            emp_name,
            dept_id,
            salary,
            degree,
            ROW_NUMBER() OVER ( PARTITION BY dept_id
        ORDER BY salary DESC ) AS salary_rank
        FROM employees )
        SELECT
            dept_id AS Department,
            salary_rank AS RANK,
            emp_name AS Employee,
            degree AS Degree,
            '$' || FORMAT('{:,}', salary) AS Salary
        FROM dept_ranked
        WHERE salary_rank <= 3
        ORDER BY dept_id, salary_rank;
    """).df()
    show(_df, "Top 3 Earners per Department — classic ROW_NUMBER() + CTE pattern")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ---
    ## 🔴 Part 3 — Intermediate+: Advanced Ranking Patterns (Cells 16–20)

    Now we combine **ranking functions + chained CTEs** for real analytics.
    These mirror production queries written by data analysts every day.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cell 16 · Salary Tiers with `DENSE_RANK`

    Instead of ranking individuals, rank **salary bands** for clean tier numbers.
    We round salaries to the nearest $20k so same-step employees share a tier.

    `DENSE_RANK` is perfect here — Tier 1, Tier 2, Tier 3 … no gaps, no skips.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 16 · Salary Tiers ──────────────────────────────────────────────────
    _df = con.execute("""
        WITH salary_bands AS (
        SELECT
            salary,
            (salary // 20000) * 20000 AS band_floor,
            DENSE_RANK() OVER (
        ORDER BY (salary // 20000)) AS tier
        FROM employees )
        SELECT
            tier AS Tier,
            '$' || FORMAT('{:,}', CAST(band_floor AS INT)) AS Band_Start,
            '$' || FORMAT('{:,}', CAST(band_floor+19999 AS INT)) AS Band_End,
            COUNT(*) AS Employees,
            ROUND(COUNT(*) * 100.0 / 1000, 1) AS Pct
        FROM salary_bands
        GROUP BY tier, band_floor
        ORDER BY tier;
    """).df()
    show(_df, "Salary Tier Distribution — DENSE_RANK on salary bands")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 17 · Dual-Dimension Ranking — Salary AND Performance

    Apply two independent `RANK()` calls on the same rows inside one CTE.
    Then filter for employees who rank **top 5 in both metrics** — well-paid *and* high-performing.
    These are the "golden employees."
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 17 · Dual-Dimension Ranking ───────────────────────────────────────
    _df = con.execute("""
        WITH dual_ranked AS (
        SELECT
            emp_name,
            dept_id,
            country,
            salary,
            performance,
            degree,
            RANK() OVER (PARTITION BY dept_id
        ORDER BY salary DESC) AS sal_rank, RANK() OVER (PARTITION BY dept_id
        ORDER BY performance DESC) AS perf_rank
        FROM employees )
        SELECT
            emp_name AS Employee,
            dept_id AS Dept,
            country AS Country,
            degree AS Degree,
            '$' || FORMAT('{:,}', salary) AS Salary,
            performance AS Perf,
            sal_rank AS Salary_Rank,
            perf_rank AS Perf_Rank
        FROM dual_ranked
        WHERE sal_rank <= 5
        AND perf_rank <= 5
        ORDER BY dept_id, sal_rank;
    """).df()
    show(_df, "Golden Employees — Top 5 in Both Salary AND Performance per Dept")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 18 · Running Totals — Cumulative Salary Share

    `SUM() OVER (ORDER BY ...)` is a **window aggregate** — a running total.
    Combined with ranking it answers: what share of total salary goes to the top earners?

    ```sql
    SUM(salary) OVER (
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )
    ```
    `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` = sum from first row to this row.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 18 · Cumulative Salary Share ──────────────────────────────────────
    _df = con.execute("""
        WITH global_ranked AS (
        SELECT
            emp_name,
            dept_id,
            salary,
            ROW_NUMBER() OVER (
        ORDER BY salary DESC) AS rn, SUM(salary) OVER () AS total_sal, SUM(salary) OVER (
        ORDER BY salary DESC ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW ) AS cumulative_sal
        FROM employees )
        SELECT
            rn AS Overall_Rank,
            emp_name AS Employee,
            dept_id AS Dept,
            '$' || FORMAT('{:,}', salary) AS Salary,
            '$' || FORMAT('{:,}', CAST(cumulative_sal AS INT)) AS Cumulative_Sal,
            ROUND(cumulative_sal * 100.0 / total_sal, 2) AS Cumul_Pct
        FROM global_ranked
        WHERE rn <= 20
        ORDER BY rn;
    """).df()
    show(_df, "Top 20 Earners — Cumulative Share of Total Salary Budget")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 19 · Chained CTEs — A 4-Step Analytics Pipeline

    Multiple `WITH` blocks can **chain** — each CTE references the previous one.
    SQL equivalent of a named data pipeline.

    **Problem:** For each country, find the highest-paying department,
    then identify the top earner in that dept-country combo.

    **4 CTE steps:**
    1. `dept_country_avg` — average salary per (country, dept) pair
    2. `dept_ranked` — rank depts within each country
    3. `top_dept` — keep only the #1 dept per country
    4. `top_earner` — find the highest earner in each winning combo
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 19 · Chained CTEs — 4-Step Pipeline ───────────────────────────────
    _df = con.execute("""
        WITH dept_country_avg AS (
        SELECT
            country,
            dept_id,
            ROUND(AVG(salary)) AS avg_sal,
            COUNT(*) AS headcount
        FROM employees
        GROUP BY country, dept_id ), dept_ranked AS (
        SELECT
            country,
            dept_id,
            avg_sal,
            RANK() OVER (PARTITION BY country
        ORDER BY avg_sal DESC) AS dept_rank
        FROM dept_country_avg ), top_dept AS (
        SELECT
            country,
            dept_id,
            avg_sal
        FROM dept_ranked
        WHERE dept_rank = 1 ), top_earner AS (
        SELECT
            emp_name,
            dept_id,
            country,
            salary,
            degree,
            ROW_NUMBER() OVER ( PARTITION BY dept_id, country
        ORDER BY salary DESC ) AS rn
        FROM employees )
        SELECT
            t.country AS Country,
            t.dept_id AS Top_Dept,
            '$' || FORMAT('{:,}', CAST(t.avg_sal AS INT)) AS Dept_Avg_Salary,
            e.emp_name AS Top_Earner,
            '$' || FORMAT('{:,}', e.salary) AS Top_Earner_Salary,
            e.degree AS Degree
        FROM top_dept t
        JOIN top_earner e ON e.dept_id=t.dept_id
        AND e.country=t.country
        AND e.rn=1
        ORDER BY t.country;
    """).df()
    show(_df, "Per Country: Highest-Paying Dept and Its Top Earner")

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Cell 20 · Grand Finale — The Composite Employee Leaderboard

    Combining everything: `PERCENT_RANK`, `DENSE_RANK`, chained CTEs, weighted scoring.

    **Composite score formula:**
    - Salary rank (40%) — `PERCENT_RANK()` by salary within dept
    - Performance rank (40%) — `PERCENT_RANK()` by performance within dept
    - Tenure (20%) — `PERCENT_RANK()` by days employed within dept

    `PERCENT_RANK()` returns 0.0 (top) to 1.0 (bottom).
    We invert it (`1 - pct`) so higher score = better employee.
    """)
    return


@app.cell
def _(con, show):
    # ─── Cell 20 · Grand Finale — Composite Leaderboard ─────────────────────────
    _df = con.execute("""
        WITH base AS (
        SELECT
            emp_id,
            emp_name,
            dept_id,
            country,
            degree,
            salary,
            performance,
            DATE_DIFF('day', hire_date::DATE, CURRENT_DATE) AS tenure_days
        FROM employees ), ranked AS (
        SELECT
            *,
            PERCENT_RANK() OVER (PARTITION BY dept_id
        ORDER BY salary DESC) AS sal_pct, PERCENT_RANK() OVER (PARTITION BY dept_id
        ORDER BY performance DESC) AS perf_pct, PERCENT_RANK() OVER (PARTITION BY dept_id
        ORDER BY tenure_days DESC) AS ten_pct
        FROM base ), scored AS (
        SELECT
            *,
            ROUND((0.4*(1.0-sal_pct) + 0.4*(1.0-perf_pct) + 0.2*(1.0-ten_pct))*100, 1) AS composite_score
        FROM ranked ), leaderboard AS (
        SELECT
            *,
            DENSE_RANK() OVER (
        ORDER BY composite_score DESC) AS overall_rank
        FROM scored )
        SELECT
            overall_rank AS "#",
            emp_name AS Employee,
            dept_id AS Dept,
            country AS Country,
            degree AS Degree,
            '$' || FORMAT('{:,}', salary) AS Salary,
            performance AS Perf,
            tenure_days AS Tenure_Days,
            composite_score AS Score
        FROM leaderboard
        ORDER BY overall_rank
        LIMIT 25;
    """).df()
    show(_df, "Company Leaderboard — Top 25 (40% Salary + 40% Performance + 20% Tenure)")

    print()
    print("=" * 60)
    print("  Tutorial Complete!")
    print("  You now know: ROW_NUMBER · RANK · DENSE_RANK · PERCENT_RANK")
    print("""
        WITH (CTEs) · Chained CTEs · Running Totals · Composite Scoring;
    """)
    print("  Next: NTILE · LAG · LEAD · FIRST_VALUE · LAST_VALUE")
    print("=" * 60)

    return (_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📚 Summary — Ranking Functions Cheat Sheet

    | Concept | Key Rule | Best Used For |
    |---|---|---|
    | `ROW_NUMBER()` | 1,2,3,4 — no ties ever | Pagination, deduplication, pick exactly 1 row |
    | `RANK()` | Ties share rank; next rank skips | Competitions, Olympic-style leaderboards |
    | `DENSE_RANK()` | Ties share rank; no gaps | Salary tiers, grade levels, compact rankings |
    | `PERCENT_RANK()` | 0.0 to 1.0 relative position | Percentile comparisons, composite scoring |
    | `PARTITION BY` | Resets rank per group | Any 'rank within group' scenario |
    | `WITH` CTE | Named, reusable subquery | Any query needing named intermediate results |
    | Chained CTEs | CTE2 references CTE1 | Multi-step analytics pipelines |

    ### 🚀 What to Explore Next
    - **`NTILE(n)`** — divide rows into n equal buckets (quartiles, deciles)
    - **`LAG(col, n)`** / **`LEAD(col, n)`** — look n rows backward / forward
    - **`FIRST_VALUE()`** / **`LAST_VALUE()`** — boundary values of a window
    - **`ROWS BETWEEN`** — custom sliding window frames
    - **`QUALIFY`** — DuckDB/Snowflake shortcut: filter on window functions directly (no CTE needed!)
    """)
    return


if __name__ == "__main__":
    app.run()
