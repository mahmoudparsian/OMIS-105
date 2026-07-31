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


@app.cell
def _(con, mo):
    _df = con.execute("SELECT * FROM employees ORDER BY emp_id;").df()
    mo.ui.table(_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. `mo.ui.slider` — Filter by Minimum Salary

    **Business Question:** *"Show me employees who earn at least $X."*

    **SQL Concept:** `WHERE salary >= value`

    The slider below controls the minimum salary in the SQL query.
    Move it and watch the results update instantly!

    ---
    """)
    return


@app.cell
def _(mo):
    salary_slider = mo.ui.slider(
        start=55000,
        stop=115000,
        step=5000,
        value=70000,
        label="Minimum Salary ($)",
        show_value=True,
    )
    salary_slider
    return (salary_slider,)


@app.cell
def _(con, mo, salary_slider):
    _sql = f"""
    SELECT name, department, salary, age, city
    FROM   employees
    WHERE  salary >= {salary_slider.value}
    ORDER BY salary DESC;
    """

    _df = con.execute(_sql).df()

    mo.vstack([
        mo.md(f"""
**SQL Query:**
```sql
SELECT name, department, salary, age, city
FROM   employees
WHERE  salary >= {salary_slider.value}
ORDER BY salary DESC;
```
**Result:** {len(_df)} employee(s) earn **${salary_slider.value:,}** or more
        """),
        mo.ui.table(_df),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. `mo.ui.dropdown` — Filter by Department

    **Business Question:** *"Show me everyone in the ___ department."*

    **SQL Concept:** `WHERE department = 'value'`

    Pick a department from the dropdown and the query filters to that team.

    ---
    """)
    return


@app.cell
def _(mo):
    dept_dropdown = mo.ui.dropdown(
        options=["All Departments", "Engineering", "Finance", "Marketing", "Sales"],
        value="All Departments",
        label="Select Department",
    )
    dept_dropdown
    return (dept_dropdown,)


@app.cell
def _(con, dept_dropdown, mo):
    if dept_dropdown.value == "All Departments":
        _where = ""
        _filter_label = "All Departments"
    else:
        _where = f"WHERE department = '{dept_dropdown.value}'"
        _filter_label = dept_dropdown.value

    _sql = f"""
    SELECT name, department, salary, city
    FROM   employees
    {_where}
    ORDER BY name;
    """
    _df = con.execute(_sql).df()

    # Also compute department stats
    _stats_sql = f"""
    SELECT COUNT(*)        AS headcount,
           ROUND(AVG(salary)) AS avg_salary,
           MIN(salary)     AS min_salary,
           MAX(salary)     AS max_salary
    FROM   employees
    {_where};
    """
    _stats = con.execute(_stats_sql).df()

    mo.vstack([
        mo.md(f"""
**Showing:** {_filter_label} — **{len(_df)}** employee(s)

| Statistic | Value |
|-----------|-------|
| Headcount | {int(_stats['headcount'][0])} |
| Avg Salary | ${int(_stats['avg_salary'][0]):,} |
| Salary Range | ${int(_stats['min_salary'][0]):,} – ${int(_stats['max_salary'][0]):,} |
        """),
        mo.ui.table(_df),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. `mo.ui.text` — Search by Name

    **Business Question:** *"Find employees whose name contains ___."*

    **SQL Concept:** `WHERE name LIKE '%text%'`

    Type part of a name (try **Kim**, **ar**, or **Lo**) and the query
    searches for matches. This is how search boxes work in real apps!

    ---
    """)
    return


@app.cell
def _(mo):
    name_search = mo.ui.text(
        placeholder="Type a name to search...",
        label="Search Employee Name",
    )
    name_search
    return (name_search,)


@app.cell
def _(con, mo, name_search):
    _search = (name_search.value or "").strip()

    if _search:
        _sql = f"""
        SELECT name, department, salary, city
        FROM   employees
        WHERE  LOWER(name) LIKE LOWER('%{_search}%')
        ORDER BY name;
        """
        _df = con.execute(_sql).df()
        _header = mo.md(f"""
**Searching for:** `{_search}` — Found **{len(_df)}** match(es)

```sql
WHERE LOWER(name) LIKE LOWER('%{_search}%')
```
        """)
        _table = mo.ui.table(_df)
    else:
        _header = mo.md("*Type a name above to search. Try: `Kim`, `ar`, `Lo`*")
        _table = mo.md("")

    mo.vstack([_header, _table])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. `mo.ui.number` — Control LIMIT

    **Business Question:** *"Show me the top N highest-paid employees."*

    **SQL Concept:** `ORDER BY salary DESC LIMIT n`

    Enter a number to control how many rows the query returns.
    This is like asking "show me the top 3" or "top 10."

    ---
    """)
    return


@app.cell
def _(mo):
    limit_number = mo.ui.number(
        start=1,
        stop=15,
        value=5,
        label="How many top earners to show?",
    )
    limit_number
    return (limit_number,)


@app.cell
def _(con, limit_number, mo):
    _n = limit_number.value

    _sql = f"""
    SELECT name,
           department,
           salary,
           RANK() OVER (ORDER BY salary DESC) AS salary_rank
    FROM   employees
    ORDER BY salary DESC
    LIMIT  {_n};
    """

    _df = con.execute(_sql).df()

    mo.vstack([
        mo.md(f"""
**Top {_n} Highest-Paid Employees**

```sql
SELECT name, department, salary,
       RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM   employees
ORDER BY salary DESC
LIMIT  {_n};
```
        """),
        mo.ui.table(_df),
    ])
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
    ## 6. `mo.ui.switch` — Toggle a Filter On/Off

    **Business Question:** *"Show only employees in San Jose (yes/no)."*

    **SQL Concept:** Conditionally add or remove a `WHERE` clause

    A switch is a simple on/off toggle. Here it controls whether
    we filter the results to a single city.

    ---
    """)
    return


@app.cell
def _(mo):
    sj_switch = mo.ui.switch(
        value=False,
        label="Show only San Jose employees",
    )
    sj_switch
    return (sj_switch,)


@app.cell
def _(con, mo, sj_switch):
    if sj_switch.value:
        _where = "WHERE city = 'San Jose'"
        _label = "San Jose Only"
    else:
        _where = ""
        _label = "All Cities"

    _sql = f"""
    SELECT name, department, salary, city
    FROM   employees
    {_where}
    ORDER BY name;
    """

    _df = con.execute(_sql).df()

    mo.vstack([
        mo.md(f"**Filter:** {_label} — **{len(_df)}** employee(s)"),
        mo.ui.table(_df),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7. Combining Widgets — Build Your Own Query

    **Business Question:** *"Show me employees in ___ department
    who earn at least $___, sorted by ___."*

    **SQL Concept:** `WHERE ... AND ... ORDER BY ...`

    In real business applications, users combine multiple filters.
    Here you control **three parts** of the SQL query at once!

    ---
    """)
    return


@app.cell
def _(mo):
    combo_dept = mo.ui.dropdown(
        options=["All", "Engineering", "Finance", "Marketing", "Sales"],
        value="All",
        label="Department",
    )
    combo_salary = mo.ui.slider(
        start=50000,
        stop=115000,
        step=5000,
        value=60000,
        label="Minimum Salary ($)",
        show_value=True,
    )
    combo_sort = mo.ui.dropdown(
        options={
            "Name": "name",
            "Salary (High to Low)": "salary DESC",
            "Age": "age",
        },
        value="Salary (High to Low)",
        label="Sort By",
    )

    mo.hstack(
        [combo_dept, combo_salary, combo_sort],
        justify="start",
        gap=1,
    )
    return combo_dept, combo_salary, combo_sort


@app.cell
def _(combo_dept, combo_salary, combo_sort, con, mo):
    # Build WHERE clause from widget values
    _conditions = [f"salary >= {combo_salary.value}"]
    if combo_dept.value != "All":
        _conditions.append(f"department = '{combo_dept.value}'")

    _where = "WHERE " + " AND ".join(_conditions)
    _order = combo_sort.value

    _sql = f"""
    SELECT name, department, salary, age, city
    FROM   employees
    {_where}
    ORDER BY {_order};
    """

    _df = con.execute(_sql).df()

    mo.vstack([
        mo.md(f"""
**Your Custom Query:**
```sql
SELECT name, department, salary, age, city
FROM   employees
{_where}
ORDER BY {_order};
```
**Result:** {len(_df)} employee(s) matched
        """),
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
