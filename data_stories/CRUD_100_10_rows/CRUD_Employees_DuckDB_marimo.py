import marimo

__generated_with = "0.23.9"
app = marimo.App(
    width="medium",
    app_title="CRUD with DuckDB",
    sql_output="pandas",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🦆 CRUD Operations with DuckDB — Employee Data

    > **Course:** OMIS 105 · Data Stories  **Topic:** Create · Read · Update · Delete

    **DuckDB** is a fast, in-process SQL engine — it runs inside this notebook, no server needed.

    ## CRUD at a glance

    | Letter | Operation | SQL | What it does |
    |--------|-----------|-----|--------------|
    | **C** | Create | `INSERT INTO` | adds new rows |
    | **R** | Read   | `SELECT`      | retrieves rows |
    | **U** | Update | `UPDATE … SET`| changes rows |
    | **D** | Delete | `DELETE FROM` | removes rows |

    ---

    ### 📌 How this notebook works (please read)

    marimo is **reactive** — it does not run top-to-bottom like Jupyter. To make a
    *sequential* CRUD story behave correctly, this notebook follows two rules:

    1. **Read queries** (`SELECT`) are ordinary **pure-SQL cells** — they always show
       live results.
    2. **Write operations** (`INSERT` / `UPDATE` / `DELETE`) are **button-gated**: the
       SQL is shown, and it runs *only when you click its ▶ button*. This makes the
       order intentional and prevents marimo from re-applying a change on its own.

    > **Tip:** *Run All* (or restart) resets everything to the original **10 rows** —
    > nothing is mutated until you click a button. Use the **🔄 Restore** buttons to
    > reset at any time.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import duckdb
    import pandas as pd

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker

    return duckdb, mo, mticker, plt


@app.cell
def _(duckdb, mo):
    import pathlib

    try:
        _base = mo.notebook_dir()
    except Exception:
        _base = None
    if _base is None:
        _base = pathlib.Path(".").resolve()
    CSV_PATH = str(_base / "data" / "employees.csv")

    con = duckdb.connect()  # fresh in-memory database every run

    _CREATE = """
        CREATE OR REPLACE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR,
            department VARCHAR,
            salary     INTEGER,
            gender     VARCHAR
        )
    """

    def reseed(connection):
        """(Re)build `employees` with the canonical 10 rows from the CSV."""
        connection.execute(_CREATE)
        connection.execute(
            f"INSERT INTO employees SELECT * FROM read_csv_auto('{CSV_PATH}')"
        )

    # employees = mutable playground;  employees_backup = never modified
    reseed(con)
    con.execute(
        f"CREATE OR REPLACE TABLE employees_backup AS "
        f"SELECT * FROM read_csv_auto('{CSV_PATH}')"
    )
    return con, reseed


@app.cell
def _(mticker, plt):
    PALETTE = {
        "SALES": "#4C72B0", "BUSINESS": "#55A868", "AI": "#C44E52",
        "MALE": "#4878CF", "FEMALE": "#E58606", "default": "#8172B2",
    }
    BARS = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#E58606",
            "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]

    def _money(v, _=None):
        return f"${v:,.0f}"

    def fig_vbar(df, x, y, title, ylabel="", color_col=None, money=False):
        fig, ax = plt.subplots(figsize=(8, 4.2), dpi=120)
        colors = ([PALETTE.get(v, PALETTE["default"]) for v in df[color_col]]
                  if color_col else BARS[:len(df)])
        bars = ax.bar(df[x].astype(str), df[y], color=colors, edgecolor="white")
        ax.bar_label(bars, fmt=(_money if money else "{:,.0f}".format),
                     padding=3, fontsize=10, color="#2c3e50")
        ax.set_title(title, fontsize=13, fontweight="bold", color="#2c3e50", pad=10)
        ax.set_ylabel(ylabel, fontsize=10)
        if money:
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(_money))
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        fig.tight_layout()
        return fig

    def fig_hbar(df, x, y, title, xlabel="", color_col=None):
        fig, ax = plt.subplots(figsize=(8, 4.6), dpi=120)
        colors = ([PALETTE.get(v, PALETTE["default"]) for v in df[color_col]]
                  if color_col else BARS[:len(df)])
        bars = ax.barh(df[y].astype(str), df[x], color=colors, edgecolor="white")
        ax.bar_label(bars, fmt=_money, padding=4, fontsize=9, color="#2c3e50")
        ax.set_title(title, fontsize=13, fontweight="bold", color="#2c3e50", pad=10)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.invert_yaxis()
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(_money))
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="x", linestyle="--", alpha=0.4)
        fig.tight_layout()
        return fig

    def fig_pie(df, label, value, title):
        colors = [PALETTE.get(v, BARS[i % len(BARS)])
                  for i, v in enumerate(df[label])]
        fig, ax = plt.subplots(figsize=(6, 6), dpi=120)
        _, _, auto = ax.pie(df[value], labels=df[label].astype(str),
                            autopct="%1.1f%%", startangle=90, colors=colors,
                            pctdistance=0.78,
                            wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2))
        for t in auto:
            t.set_color("white"); t.set_fontweight("bold")
        ax.set_title(title, fontsize=13, fontweight="bold", color="#2c3e50", pad=12)
        fig.tight_layout()
        return fig

    def fig_range(df, dept, lo, hi, title):
        import numpy as np
        x = np.arange(len(df)); w = 0.35
        fig, ax = plt.subplots(figsize=(9, 5), dpi=120)
        b1 = ax.bar(x - w/2, df[lo], w, label="Min salary", color="#4C72B0", edgecolor="white")
        b2 = ax.bar(x + w/2, df[hi], w, label="Max salary", color="#C44E52", edgecolor="white")
        ax.bar_label(b1, fmt=_money, padding=3, fontsize=9)
        ax.bar_label(b2, fmt=_money, padding=3, fontsize=9)
        ax.set_xticks(x); ax.set_xticklabels(df[dept].astype(str))
        ax.set_title(title, fontsize=13, fontweight="bold", color="#2c3e50", pad=10)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_money))
        ax.legend(fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        fig.tight_layout()
        return fig

    return fig_hbar, fig_pie, fig_range, fig_vbar


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🗂️ The starting table

    `employees` is seeded with 10 rows from `data/employees.csv`. A second table,
    `employees_backup`, holds the same rows and is **never modified** (we use it in
    the INSERT … SELECT example). Below: the column definitions, then the data.
    """)
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        DESCRIBE employees;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM employees
        ORDER BY emp_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ C — CREATE (`INSERT`)

    `INSERT` adds new rows. Each step shows the SQL and a ▶ button — click it to run
    the statement against the live table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    sql_c1 = r'''INSERT INTO employees (emp_id, emp_name, department, salary, gender)
    VALUES (920, 'Carlos', 'AI', 210000, 'MALE');'''
    btn_c1 = mo.ui.run_button(label="▶ Run C1")
    mo.vstack([
        mo.md(r'''### C-1 · Insert a single new employee

    Adds one new row with `INSERT INTO … VALUES`.

    ```sql
    ''' + sql_c1 + r'''
    ```'''),
        btn_c1,
    ])
    return btn_c1, sql_c1


@app.cell(hide_code=True)
def _(btn_c1, con, mo, sql_c1):
    if btn_c1.value:
        try:
            con.execute(sql_c1)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    sql_c2 = r'''INSERT INTO employees (emp_id, emp_name, department, salary, gender)
    VALUES
    (930, 'Diana', 'BUSINESS', 155000, 'FEMALE'),
    (940, 'Ethan', 'AI', 195000, 'MALE');'''
    btn_c2 = mo.ui.run_button(label="▶ Run C2")
    mo.vstack([
        mo.md(r'''### C-2 · Insert several rows in one statement

    One `INSERT` can add many rows — separate the value tuples with commas.

    ```sql
    ''' + sql_c2 + r'''
    ```'''),
        btn_c2,
    ])
    return btn_c2, sql_c2


@app.cell(hide_code=True)
def _(btn_c2, con, mo, sql_c2):
    if btn_c2.value:
        try:
            con.execute(sql_c2)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    sql_c3 = r'''INSERT INTO employees
    SELECT 950          AS emp_id,
       'Fiona'      AS emp_name,
       department,
       salary + 5000 AS salary,
       'FEMALE'     AS gender
    FROM employees_backup
    WHERE emp_id = 700;'''
    btn_c3 = mo.ui.run_button(label="▶ Run C3")
    mo.vstack([
        mo.md(r'''### C-3 · `INSERT … SELECT` — derive a row from the backup

    Instead of literal values, insert rows *computed by a query*. Here a new hire is based on employee 700 in the untouched `employees_backup`.

    ```sql
    ''' + sql_c3 + r'''
    ```'''),
        btn_c3,
    ])
    return btn_c3, sql_c3


@app.cell(hide_code=True)
def _(btn_c3, con, mo, sql_c3):
    if btn_c3.value:
        try:
            con.execute(sql_c3)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    sql_c4 = r'''INSERT INTO employees (emp_id, emp_name, department, salary, gender)
    VALUES (960, 'George', 'SALES', NULL, 'MALE');'''
    btn_c4 = mo.ui.run_button(label="▶ Run C4")
    mo.vstack([
        mo.md(r'''### C-4 · Insert with `NULL` (unknown value)

    `NULL` means *unknown / not yet recorded* — here a salary that hasn't been set.

    ```sql
    ''' + sql_c4 + r'''
    ```'''),
        btn_c4,
    ])
    return btn_c4, sql_c4


@app.cell(hide_code=True)
def _(btn_c4, con, mo, sql_c4):
    if btn_c4.value:
        try:
            con.execute(sql_c4)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    btn_restore_c = mo.ui.run_button(label="🔄 Restore original 10 rows")
    mo.vstack([
        mo.md(r'''Done experimenting with INSERT? Reset before the next section.'''),
        btn_restore_c,
    ])
    return (btn_restore_c,)


@app.cell(hide_code=True)
def _(btn_restore_c, con, mo, reseed):
    if btn_restore_c.value:
        reseed(con)
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"Current `employees` table  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 📖 R — READ (`SELECT`)

    `SELECT` retrieves rows and never changes data, so these are ordinary
    **pure-SQL cells** — they show live results immediately.

    ```sql
    SELECT columns FROM table WHERE condition ORDER BY column LIMIT n;
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-1 · All columns, all rows
    """)
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- All columns and all rows
        SELECT *
        FROM employees
        ORDER BY emp_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-2 · Specific columns
    """)
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- Pick specific columns, sort by salary
        SELECT emp_id, emp_name, salary
        FROM employees
        ORDER BY salary DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-3 · Filter rows with `WHERE`
    """)
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM employees
        WHERE department = 'SALES'
        ORDER BY emp_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### R-4 · Top-3 highest paid (`ORDER BY` + `LIMIT`)
    """)
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        SELECT emp_id, emp_name, department, salary
        FROM employees
        ORDER BY salary DESC
        LIMIT 3;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📚 10 basic `SELECT` queries
    A quick tour of `WHERE`, `ORDER BY`, `LIMIT`, `BETWEEN`, `IN`, and `LIKE`.
    """)
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- Q1 · All female employees
        SELECT * FROM employees
        WHERE gender = 'FEMALE'
        ORDER BY emp_id;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- Q2 · Salary above $150,000
        SELECT emp_name, department, salary FROM employees
        WHERE salary > 150000
        ORDER BY salary DESC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- Q3 · AI department, highest paid first
        SELECT * FROM employees
        WHERE department = 'AI'
        ORDER BY salary DESC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- Q4 · Everyone, alphabetical by name
        SELECT emp_id, emp_name, department FROM employees
        ORDER BY emp_name ASC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- Q5 · Bottom-3 earners
        SELECT emp_id, emp_name, salary FROM employees
        ORDER BY salary ASC
        LIMIT 3;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- Q6 · BUSINESS women
        SELECT * FROM employees
        WHERE department = 'BUSINESS' AND gender = 'FEMALE'
        ORDER BY salary DESC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- Q7 · Salary BETWEEN 140k and 170k
        SELECT emp_name, department, salary FROM employees
        WHERE salary BETWEEN 140000 AND 170000
        ORDER BY salary;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- Q8 · SALES or AI (IN operator)
        SELECT * FROM employees
        WHERE department IN ('SALES', 'AI')
        ORDER BY department, salary DESC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- Q9 · emp_id > 500, first 4 rows
        SELECT * FROM employees
        WHERE emp_id > 500
        ORDER BY emp_id
        LIMIT 4;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- Q10 · Names starting with a vowel (LIKE)
        SELECT emp_id, emp_name, department FROM employees
        WHERE emp_name LIKE 'A%' OR emp_name LIKE 'E%'
           OR emp_name LIKE 'I%' OR emp_name LIKE 'O%'
           OR emp_name LIKE 'U%'
        ORDER BY emp_name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📊 10 `GROUP BY` queries
    `GROUP BY` collapses rows that share a value and pairs with aggregates —
    `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. `HAVING` filters *after* aggregation.
    """)
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- G1 · Headcount per department
        SELECT department, COUNT(*) AS num_employees
        FROM employees GROUP BY department
        ORDER BY num_employees DESC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- G2 · Average salary per department
        SELECT department, ROUND(AVG(salary), 0) AS avg_salary
        FROM employees GROUP BY department
        ORDER BY avg_salary DESC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- G3 · Min and max salary per department
        SELECT department, MIN(salary) AS min_salary, MAX(salary) AS max_salary
        FROM employees GROUP BY department
        ORDER BY department;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- G4 · Headcount by gender
        SELECT gender, COUNT(*) AS num_employees
        FROM employees GROUP BY gender
        ORDER BY num_employees DESC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- G5 · Total payroll per department
        SELECT department, SUM(salary) AS total_payroll
        FROM employees GROUP BY department
        ORDER BY total_payroll DESC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- G6 · HAVING — departments with more than 2 people
        SELECT department, COUNT(*) AS num_employees
        FROM employees GROUP BY department
        HAVING COUNT(*) > 2
        ORDER BY num_employees DESC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- G7 · HAVING — average salary above 160k
        SELECT department, ROUND(AVG(salary), 0) AS avg_salary
        FROM employees GROUP BY department
        HAVING AVG(salary) > 160000
        ORDER BY avg_salary DESC;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- G8 · Gender count per department
        SELECT department, gender, COUNT(*) AS num_employees
        FROM employees GROUP BY department, gender
        ORDER BY department, gender;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- G9 · Department with the largest payroll
        SELECT department, SUM(salary) AS total_payroll
        FROM employees GROUP BY department
        ORDER BY total_payroll DESC
        LIMIT 1;
        """,
        engine=con
    )
    return


@app.cell
def _(con, employees, mo):
    _df = mo.sql(
        f"""
        -- G10 · Overall salary statistics
        SELECT COUNT(*) AS total_employees, MIN(salary) AS min_salary,
               MAX(salary) AS max_salary, ROUND(AVG(salary), 0) AS avg_salary,
               SUM(salary) AS total_payroll
        FROM employees;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✏️ U — UPDATE (`UPDATE … SET`)

    `UPDATE` changes existing rows.

    ```sql
    UPDATE table SET column = value WHERE condition;
    ```
    > ⚠️ Without a `WHERE`, every row is changed. Each step is button-gated below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    sql_u1 = r'''UPDATE employees
    SET    gender = 'FEMALE'
    WHERE  emp_id = 400;'''
    btn_u1 = mo.ui.run_button(label="▶ Run U1")
    mo.vstack([
        mo.md(r'''### U-1 · Fix a typo — Susan's gender `FMALE` → `FEMALE`

    Susan (emp_id 400) was seeded with a typo. A precise `WHERE` fixes exactly one row.

    ```sql
    ''' + sql_u1 + r'''
    ```'''),
        btn_u1,
    ])
    return btn_u1, sql_u1


@app.cell(hide_code=True)
def _(btn_u1, con, mo, sql_u1):
    if btn_u1.value:
        try:
            con.execute(sql_u1)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    sql_u2 = r'''UPDATE employees
    SET    salary = ROUND(salary * 1.10, 0)
    WHERE  department = 'SALES';'''
    btn_u2 = mo.ui.run_button(label="▶ Run U2")
    mo.vstack([
        mo.md(r'''### U-2 · Give every SALES employee a 10% raise

    A broad `WHERE` updates many rows at once; the new value is computed from the old.

    ```sql
    ''' + sql_u2 + r'''
    ```'''),
        btn_u2,
    ])
    return btn_u2, sql_u2


@app.cell(hide_code=True)
def _(btn_u2, con, mo, sql_u2):
    if btn_u2.value:
        try:
            con.execute(sql_u2)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    sql_u3 = r'''UPDATE employees
    SET    department = 'BUSINESS'
    WHERE  emp_id = 700;'''
    btn_u3 = mo.ui.run_button(label="▶ Run U3")
    mo.vstack([
        mo.md(r'''### U-3 · Transfer Dara from AI to BUSINESS

    Updating a text column — reassigning a department for emp_id 700.

    ```sql
    ''' + sql_u3 + r'''
    ```'''),
        btn_u3,
    ])
    return btn_u3, sql_u3


@app.cell(hide_code=True)
def _(btn_u3, con, mo, sql_u3):
    if btn_u3.value:
        try:
            con.execute(sql_u3)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    sql_u4 = r'''UPDATE employees
    SET    salary = 180000
    WHERE  salary > 180000;'''
    btn_u4 = mo.ui.run_button(label="▶ Run U4")
    mo.vstack([
        mo.md(r'''### U-4 · Cap salaries above $180,000

    A comparison in `WHERE` limits the update to rows over a threshold.

    ```sql
    ''' + sql_u4 + r'''
    ```'''),
        btn_u4,
    ])
    return btn_u4, sql_u4


@app.cell(hide_code=True)
def _(btn_u4, con, mo, sql_u4):
    if btn_u4.value:
        try:
            con.execute(sql_u4)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    btn_restore_u = mo.ui.run_button(label="🔄 Restore original 10 rows")
    mo.vstack([
        mo.md(r'''Reset to the original 10 rows before the DELETE section.'''),
        btn_restore_u,
    ])
    return (btn_restore_u,)


@app.cell(hide_code=True)
def _(btn_restore_u, con, mo, reseed):
    if btn_restore_u.value:
        reseed(con)
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"Current `employees` table  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 🗑️ D — DELETE (`DELETE FROM`)

    `DELETE` removes rows.

    ```sql
    DELETE FROM table WHERE condition;
    ```
    > ⚠️ `DELETE FROM employees;` with no `WHERE` empties the whole table (step D-4).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    sql_d1 = r'''DELETE FROM employees
    WHERE emp_id = 100;'''
    btn_d1 = mo.ui.run_button(label="▶ Run D1")
    mo.vstack([
        mo.md(r'''### D-1 · Delete a single employee by ID

    A precise `WHERE` removes exactly one row (emp_id 100, Alex).

    ```sql
    ''' + sql_d1 + r'''
    ```'''),
        btn_d1,
    ])
    return btn_d1, sql_d1


@app.cell(hide_code=True)
def _(btn_d1, con, mo, sql_d1):
    if btn_d1.value:
        try:
            con.execute(sql_d1)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    sql_d2 = r'''DELETE FROM employees
    WHERE department = 'AI';'''
    btn_d2 = mo.ui.run_button(label="▶ Run D2")
    mo.vstack([
        mo.md(r'''### D-2 · Delete every employee in a department

    A broader `WHERE` removes a whole group.

    ```sql
    ''' + sql_d2 + r'''
    ```'''),
        btn_d2,
    ])
    return btn_d2, sql_d2


@app.cell(hide_code=True)
def _(btn_d2, con, mo, sql_d2):
    if btn_d2.value:
        try:
            con.execute(sql_d2)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    sql_d3 = r'''DELETE FROM employees
    WHERE salary < 150000;'''
    btn_d3 = mo.ui.run_button(label="▶ Run D3")
    mo.vstack([
        mo.md(r'''### D-3 · Delete rows matching a numeric condition

    Remove everyone earning below a threshold.

    ```sql
    ''' + sql_d3 + r'''
    ```'''),
        btn_d3,
    ])
    return btn_d3, sql_d3


@app.cell(hide_code=True)
def _(btn_d3, con, mo, sql_d3):
    if btn_d3.value:
        try:
            con.execute(sql_d3)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    sql_d4 = r'''DELETE FROM employees;'''
    btn_d4 = mo.ui.run_button(label="▶ Run D4")
    mo.vstack([
        mo.md(r'''### D-4 · Delete ALL rows (no `WHERE` — careful!)

    Leaving off `WHERE` empties the entire table. This is *why* `WHERE` matters.

    ```sql
    ''' + sql_d4 + r'''
    ```'''),
        btn_d4,
    ])
    return btn_d4, sql_d4


@app.cell(hide_code=True)
def _(btn_d4, con, mo, sql_d4):
    if btn_d4.value:
        try:
            con.execute(sql_d4)
            _msg = "✅ Statement executed — the `employees` table is now:"
        except Exception as _e:
            _msg = f"⚠️ DuckDB error (re-click *Restore* to reset): {_e}"
    else:
        _msg = "Table *before* running — click ▶ above to execute the statement:"
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"**{_msg}**  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    btn_restore_d = mo.ui.run_button(label="🔄 Restore original 10 rows")
    mo.vstack([
        mo.md(r'''**Restore the full dataset** so the analytics below reflect all 10 employees.'''),
        btn_restore_d,
    ])
    return (btn_restore_d,)


@app.cell(hide_code=True)
def _(btn_restore_d, con, mo, reseed):
    if btn_restore_d.value:
        reseed(con)
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id").df()
    mo.vstack([
        mo.md(f"Current `employees` table  ·  {len(_df)} row(s)"),
        mo.ui.table(_df, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 📊 Analytics & visualisations

    These run on the current `employees` table — click **🔄 Restore** above (or
    *Run All*) first so they reflect the full 10-row dataset.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 1 · Gender distribution
    """)
    return


@app.cell(hide_code=True)
def _(con, fig_pie):
    _df = con.execute("""
        SELECT gender, COUNT(*) AS num_employees
        FROM employees GROUP BY gender ORDER BY num_employees DESC
    """).df()
    fig_pie(_df, label="gender", value="num_employees",
            title="Gender distribution — all employees")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 2 · Headcount per department
    """)
    return


@app.cell(hide_code=True)
def _(con, fig_vbar):
    _df = con.execute("""
        SELECT department, COUNT(*) AS num_employees
        FROM employees GROUP BY department ORDER BY num_employees DESC
    """).df()
    fig_vbar(_df, x="department", y="num_employees",
             title="Headcount by department", ylabel="Employees",
             color_col="department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 3 · All salaries ranked
    """)
    return


@app.cell(hide_code=True)
def _(con, fig_hbar):
    _df = con.execute("""
        SELECT emp_name, department, salary
        FROM employees ORDER BY salary DESC
    """).df()
    fig_hbar(_df, x="salary", y="emp_name",
             title="Individual salaries (highest → lowest)",
             xlabel="Annual salary (USD)", color_col="department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 4 · Salary range per department
    """)
    return


@app.cell(hide_code=True)
def _(con, fig_range):
    _df = con.execute("""
        SELECT department, MIN(salary) AS min_salary, MAX(salary) AS max_salary
        FROM employees GROUP BY department ORDER BY department
    """).df()
    fig_range(_df, dept="department", lo="min_salary", hi="max_salary",
              title="Salary range (min vs max) per department")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot 5 · Average salary per department
    """)
    return


@app.cell(hide_code=True)
def _(con, fig_vbar):
    _df = con.execute("""
        SELECT department, ROUND(AVG(salary), 0) AS avg_salary
        FROM employees GROUP BY department ORDER BY avg_salary DESC
    """).df()
    fig_vbar(_df, x="department", y="avg_salary",
             title="Average salary by department", ylabel="Avg salary (USD)",
             color_col="department", money=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ✅ Summary

    | Operation | Statement | Examples covered |
    |-----------|-----------|------------------|
    | **Create** | `INSERT INTO` | single row · multi-row · `INSERT … SELECT` · `NULL` |
    | **Read**   | `SELECT` | all/specific columns · `WHERE` · `ORDER BY` · `LIMIT` · `GROUP BY` · `HAVING` |
    | **Update** | `UPDATE … SET` | fix a typo · bulk raise · transfer dept · salary cap |
    | **Delete** | `DELETE FROM` | by id · by group · by condition · full wipe |

    **Why the writes are button-gated:** marimo is reactive, so a hidden mutation on
    a shared table could be re-applied whenever a cell re-runs. Gating each write
    behind a ▶ button makes the order explicit and the notebook reproducible — *Run
    All* always starts from the same 10 rows.
    """)
    return


if __name__ == "__main__":
    app.run()
