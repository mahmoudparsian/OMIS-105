import marimo

__generated_with = "0.23.10"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Interactive SQL Explorer
    # Marimo UI Widgets + DuckDB
    ---

    * **Course:** OMIS 105 — Database Management
    * **Environment:** DuckDB (in-memory) + Marimo UI Widgets

    ---

    ### What You Will Learn

    This notebook shows how **Marimo's interactive widgets**
    can drive SQL queries in real time. Move a slider, pick
    from a dropdown, or type in a search box — the query
    results update instantly.

    | Widget | What It Does | SQL Concept |
    |--------|-------------|-------------|
    | `mo.ui.slider` | Pick a number on a range | `WHERE col >= value` |
    | `mo.ui.dropdown` | Choose from a list | `WHERE col = value` |
    | `mo.ui.text` | Type free-form text | `WHERE col LIKE '%text%'` |
    | `mo.ui.number` | Enter an exact number | `LIMIT n` |
    | `mo.ui.radio` | Pick one option | `ORDER BY col` |
    | `mo.ui.switch` | Toggle on/off | Include/exclude a filter |

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Setup — Create Our Company Database
    ---
    """)
    return


@app.cell
def _():
    import duckdb

    # Create a DuckDB in-memory connection
    con = duckdb.connect()

    # Create and populate the employees table in one step
    # (15 employees across 4 departments)
    con.execute("""
    CREATE TABLE employees (
        emp_id      INT PRIMARY KEY,
        name        VARCHAR(50) NOT NULL,
        department  VARCHAR(30),
        salary      INT,
        age         INT,
        city        VARCHAR(30)
    );

    INSERT INTO employees VALUES
        (1,  'Alice Chen',      'Marketing',    72000, 28, 'San Jose'),
        (2,  'Bob Kumar',       'Engineering',  95000, 34, 'San Francisco'),
        (3,  'Carol Davis',     'Marketing',    68000, 26, 'San Jose'),
        (4,  'David Park',      'Engineering', 105000, 31, 'Oakland'),
        (5,  'Emma Wilson',     'Sales',        61000, 24, 'San Jose'),
        (6,  'Frank Lopez',     'Sales',        58000, 29, 'San Francisco'),
        (7,  'Grace Kim',       'Engineering', 112000, 37, 'Oakland'),
        (8,  'Henry Zhang',     'Finance',      82000, 32, 'San Jose'),
        (9,  'Ivy Patel',       'Marketing',    75000, 30, 'San Francisco'),
        (10, 'Jack Brown',      'Sales',        64000, 27, 'Oakland'),
        (11, 'Karen Lee',       'Finance',      88000, 35, 'San Jose'),
        (12, 'Leo Martinez',    'Engineering',  98000, 29, 'San Francisco'),
        (13, 'Mia Thompson',    'Finance',      79000, 33, 'Oakland'),
        (14, 'Noah Garcia',     'Sales',        67000, 25, 'San Jose'),
        (15, 'Olivia White',    'Marketing',    71000, 31, 'San Francisco');
    """)

    print("DuckDB version:", duckdb.__version__)
    print("Company database created: 15 employees, 4 departments")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Our Dataset: 15 Employees

    Here is the complete `employees` table. The interactive widgets below
    will let you filter, sort, and explore this data using SQL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. `mo.ui.radio` — Choose Sort Column

    **Business Question:** *"Sort employees by ___."*

    **SQL Concept:** `ORDER BY column_name`

    Radio buttons let you pick exactly one option — perfect for
    choosing which column to sort by.

    ---
    """)
    return


@app.cell
def _(mo):
    sort_radio = mo.ui.radio(
        options={
            "Name": "name",
            "Salary": "salary",
            "Age": "age",
            "Department": "department",
        },
        value="Salary",
        label="Sort employees by:",
    )

    sort_radio
    return (sort_radio,)


@app.cell
def _(con, mo, sort_radio):
    _col = sort_radio.value

    _sql = f"""
    SELECT name, department, salary, age, city
    FROM   employees
    ORDER BY {_col} ASC;
    """

    _df = con.execute(_sql).df()

    mo.vstack([
        mo.md(f"**Sorted by:** `{_col}` (ascending)"),
        mo.ui.table(_df),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary — Marimo UI Widgets for SQL

    | Widget | Code | Best For |
    |--------|------|----------|
    | **Slider** | `mo.ui.slider(start=0, stop=100)` | Numeric ranges (salary, age, quantity) |
    | **Dropdown** | `mo.ui.dropdown(options=[...])` | Pick from a list (departments, cities) |
    | **Text** | `mo.ui.text(placeholder="...")` | Free-form search (names, descriptions) |
    | **Number** | `mo.ui.number(start=1, stop=50)` | Exact numeric input (LIMIT, thresholds) |
    | **Radio** | `mo.ui.radio(options=[...])` | Pick one from a few options (sort column) |
    | **Switch** | `mo.ui.switch(value=False)` | Toggle a filter on/off |

    ### Key Takeaway

    Marimo widgets are **reactive** — when you change any widget,
    every cell that uses that widget automatically re-runs.
    This is exactly how dashboards and business intelligence tools work!

    ---

    ### What is Next?

    In class, you will combine these widgets with the SQL you learned in
    previous notebooks: JOINs, GROUP BY, HAVING, and more.

    ---
    *Notebook by Professor M. Parsian — Santa Clara University*
    """)
    return


@app.cell
def _():
    print("Interactive SQL Explorer — complete!")
    return


if __name__ == "__main__":
    app.run()
