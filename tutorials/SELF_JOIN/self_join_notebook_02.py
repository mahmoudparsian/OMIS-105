import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb

    # Two tiny tables, built in memory. Re-running is safe
    # because of CREATE OR REPLACE.
    con = duckdb.connect(database=":memory:")

    con.execute("""
        CREATE OR REPLACE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            name        VARCHAR,
            title       VARCHAR,
            department  VARCHAR,
            manager_id  INTEGER,
            salary      INTEGER,
            hire_date   DATE
        )
    """)
    con.execute("""
        INSERT INTO employees VALUES
            (1,  'Alice', 'CEO',                 'Leadership',  NULL, 180000, '2015-03-01'),
            (2,  'Bob',   'VP of Engineering',   'Engineering', 1,    140000, '2016-06-15'),
            (3,  'Carol', 'VP of Sales',         'Sales',       1,    135000, '2017-01-10'),
            (4,  'David', 'Engineering Manager', 'Engineering', 2,    115000, '2018-04-02'),
            (5,  'Eva',   'Senior Engineer',     'Engineering', 2,    145000, '2015-09-20'),
            (6,  'Frank', 'Sales Manager',       'Sales',       3,     95000, '2019-02-11'),
            (7,  'Grace', 'Account Executive',   'Sales',       3,     98000, '2016-11-05'),
            (8,  'Henry', 'Engineer',            'Engineering', 4,    105000, '2020-07-01'),
            (9,  'Ivy',   'Engineer',            'Engineering', 4,    118000, '2021-01-18'),
            (10, 'Jack',  'Sales Rep',           'Sales',       6,     72000, '2022-03-14'),
            (11, 'Kim',   'Sales Rep',           'Sales',       6,     76000, '2018-08-30'),
            (12, 'Leo',   'Intern',              'Engineering', 4,     45000, '2024-06-10')
    """)

    con.execute("""
        CREATE OR REPLACE TABLE daily_sales (
            sale_date DATE PRIMARY KEY,
            revenue   INTEGER
        )
    """)
    con.execute("""
        INSERT INTO daily_sales VALUES
            ('2026-10-05', 1200),
            ('2026-10-06', 1350),
            ('2026-10-07', 1100),
            ('2026-10-08', 1100),
            ('2026-10-09', 1600),
            ('2026-10-10', 2100),
            ('2026-10-11', 1900)
    """)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 🪞 Self Join — When a Table Joins Itself

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### The Story: Bronco Robotics 🤖

    **Bronco Robotics** is a small startup with 12 employees.
    All of them live in **one table**, `employees`.

    Each row has a `manager_id` column. It holds the
    `employee_id` of that person's manager. So the manager is
    **also a row in the same table**.

    The HR director asks:

    > **"Show me every employee next to the name of their manager."**

    The name of the manager is in the table — but in a
    **different row**. To put two rows of the same table side by
    side, we join the table **to itself**. This is a **self join**.

    ### The Big Idea in One Line

    > A self join is a normal join. The only trick: you use the
    > **same table twice**, with **two different aliases**
    > (nicknames), and each alias plays a **role**.

    There is no `SELF JOIN` keyword in SQL. You write
    `INNER JOIN` or `LEFT JOIN`, exactly as before.

    ### The Plan

    | Part | Queries | What happens |
    |------|---------|--------------|
    | 1. Meet the data | Q1–Q2 | Look at the table and its org chart. |
    | 2. One table, two roles | — | Why we need two aliases. |
    | 3. Your first self join | Q3 | Employee next to manager. |
    | 4. How the matching works | — | Trace one row, step by step. |
    | 5. Keep the boss | Q4–Q5 | `LEFT JOIN` and `COALESCE`. |
    | 6. Compare a row to its partner | Q6–Q7 | Paid more, or hired earlier, than the manager — colored on the org chart. |
    | 7. Pairs from one table | Q8–Q10 | Teammates, and the `<` trick. |
    | 8. Count the team | Q11–Q12 | Direct reports, the `COUNT(*)` trap, team payroll. |
    | 9. Two steps up | Q13 | Three copies of one table. |
    | 10. Not only org charts | Q14–Q15 | Compare today with yesterday. |
    | 11. Explore | — | Pick a manager, see the team. |
    | 12. Common mistakes | — | Real errors, and one silent bug. |
    | 13. Cheat sheet & practice | — | A template and 6 exercises with solutions. |

    The tables are tiny on purpose: you can check every answer by eye.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 1 — Meet the Data

    ### Q1. The `employees` table

    Look at the `manager_id` column. Bob's `manager_id` is `1`.
    Who has `employee_id = 1`? Alice. So **Alice is Bob's manager**.

    Alice is the CEO. She has no manager, so her `manager_id` is `NULL`.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT employee_id,
               name,
               title,
               department,
               manager_id,
               salary,
               hire_date
        FROM employees
        ORDER BY employee_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. The same data as an org chart

    The `manager_id` column describes a tree. Each arrow below goes
    from a manager to one direct report.

    **Fun fact:** this chart is drawn from the result of a self join —
    the query you will write in Q3.
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _nodes = con.execute("""
        SELECT employee_id, name, title
        FROM employees
        ORDER BY employee_id
    """).fetchall()
    _edges = con.execute("""
        SELECT m.employee_id, e.employee_id
        FROM employees AS e
        INNER JOIN employees AS m
            ON e.manager_id = m.employee_id
        ORDER BY m.employee_id, e.employee_id
    """).fetchall()

    _ids = {_name: _id for _id, _name, _title in _nodes}

    def org_chart(employees=(), managers=(), color="#FDE68A", border="#B45309"):
        # Fill each employee's box, outline each manager's box (dashed),
        # and thicken the arrow between each pair.
        employees, managers = list(employees), list(managers)
        _pairs = {(_ids[m], _ids[e]) for e, m in zip(employees, managers)}
        _lines = ["graph TD"]
        for _id, _name, _title in _nodes:
            _lines.append(f'    E{_id}["<b>{_name}</b><br/>{_title}<br/>id = {_id}"]')
        for _i, (_m, _e) in enumerate(_edges):
            _lines.append(f"    E{_m} --> E{_e}")
            if (_m, _e) in _pairs:
                _lines.append(f"    linkStyle {_i} stroke:{border},stroke-width:4px")
        _lines.append(f"    classDef emp fill:{color},stroke:{border},stroke-width:3px,color:#111")
        _lines.append(f"    classDef mgr fill:#FFFFFF,stroke:{border},stroke-width:3px,stroke-dasharray:6 4,color:#111")
        if employees:
            _lines.append("    class " + ",".join(f"E{_ids[e]}" for e in employees) + " emp")
        _boss_only = [m for m in dict.fromkeys(managers) if m not in employees]
        if _boss_only:
            _lines.append("    class " + ",".join(f"E{_ids[m]}" for m in _boss_only) + " mgr")
        return mo.mermaid("\n".join(_lines))

    org_chart()
    return (org_chart,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 2 — One Table, Two Roles

    In a normal join, you have two tables: `orders` and `customers`.
    In a self join, you have **one** table. So we **pretend** there
    are two copies of it, and give each copy an alias:

    | Alias | Role | Read it as |
    |-------|------|------------|
    | `e` | the **employee** | "the person we are talking about" |
    | `m` | the **manager** | "the person `e` reports to" |

    Both copies have the same 12 rows. The `ON` rule connects them:

    ```sql
    ON e.manager_id = m.employee_id
    ```

    Read it out loud: *"the employee's `manager_id` must equal the
    manager's `employee_id`."*

    ```
       e  (employee copy)                     m  (manager copy)
    ┌────┬───────┬────────────┐          ┌────┬───────┐
    │ id │ name  │ manager_id │          │ id │ name  │
    ├────┼───────┼────────────┤          ├────┼───────┤
    │  4 │ David │      2 ────┼────────▶ │  2 │ Bob   │
    │  8 │ Henry │      4 ────┼────────▶ │  4 │ David │
    │  1 │ Alice │   NULL     │   ✗      │    │       │
    └────┴───────┴────────────┘          └────┴───────┘
    ```

    **Without aliases, SQL cannot tell the two copies apart.**
    `employees.name` could mean either one. (You will see the real
    error in Part 12.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 3 — Your First Self Join

    ### Q3. Who manages each employee?

    `e` gives us the employee's name. `m` gives us the manager's name.

    **Predict first:** there are 12 employees. How many rows will
    `INNER JOIN` return?

    **Expected: 11 rows.** Alice is missing — her `manager_id` is
    `NULL`, and `NULL` never matches anything.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT e.name  AS employee,
               e.title AS employee_title,
               m.name  AS manager,
               m.title AS manager_title
        FROM employees AS e
        INNER JOIN employees AS m
            ON e.manager_id = m.employee_id
        ORDER BY e.employee_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 4 — How the Matching Works 🔍

    Pick an employee. Watch DuckDB take their `manager_id` from the
    `e` copy, then look for the row with that `employee_id` in the
    `m` copy.
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _names = [r[0] for r in con.execute(
        "SELECT name FROM employees ORDER BY employee_id"
    ).fetchall()]
    trace_picker = mo.ui.dropdown(
        options=_names, value="Henry", label="Employee (`e`):"
    )
    trace_picker
    return (trace_picker,)


@app.cell(hide_code=True)
def _(con, mo, trace_picker):
    _e = con.execute("""
        SELECT employee_id, name, title, manager_id
        FROM employees
        WHERE name = ?
    """, [trace_picker.value]).fetchdf()
    _m = con.execute("""
        SELECT m.employee_id, m.name, m.title
        FROM employees AS e
        INNER JOIN employees AS m
            ON e.manager_id = m.employee_id
        WHERE e.name = ?
    """, [trace_picker.value]).fetchdf()

    _mid = _e["manager_id"].iloc[0]
    if _m.empty:
        _step = mo.callout(mo.md(
            f"**Step 2:** `manager_id` is `NULL`. `NULL = anything` is never "
            f"true, so **no row matches**. With `INNER JOIN`, "
            f"{trace_picker.value} is **dropped** from the result. "
            f"(Part 5 shows how `LEFT JOIN` keeps this row.)"
        ), kind="warn")
    else:
        _step = mo.callout(mo.md(
            f"**Step 2:** look in `m` for `employee_id = {int(_mid)}` → "
            f"found **{_m['name'].iloc[0]}**. So {trace_picker.value}'s "
            f"manager is {_m['name'].iloc[0]}. ✅"
        ), kind="success")

    mo.vstack([
        mo.md(f"**Step 1:** the row for {trace_picker.value} in the `e` copy:"),
        mo.ui.table(_e, selection=None, pagination=False),
        _step,
        mo.ui.table(_m, selection=None, pagination=False) if not _m.empty else mo.md(""),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 5 — Keep the Boss

    ### Q4. `LEFT JOIN` keeps every employee

    `LEFT JOIN` keeps **every row of the left copy** (`e`), even
    when no manager matches. The `ON` rule does not change.

    **Expected: 12 rows.** Alice is back, with a `NULL` manager.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT e.name AS employee,
               m.name AS manager
        FROM employees AS e
        LEFT JOIN employees AS m
            ON e.manager_id = m.employee_id
        ORDER BY e.employee_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Replace `NULL` with a friendly label

    `COALESCE(a, b)` returns `a` if it is not `NULL`, otherwise `b`.
    A report for HR should say *"(reports to the board)"*, not `NULL`.

    **Expected: 12 rows,** no `NULL` anywhere.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT e.name AS employee,
               e.department,
               COALESCE(m.name, '(reports to the board)') AS manager
        FROM employees AS e
        LEFT JOIN employees AS m
            ON e.manager_id = m.employee_id
        ORDER BY e.employee_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 6 — Compare a Row to Its Partner

    After the join, each result row holds **two people**: `e` and `m`.
    Now you can compare their columns, just like any two columns.

    > `ON` decides **which rows belong together**.
    > `WHERE` decides **which of those pairs to keep**.

    ### Q6. Who earns more than their manager?

    **Expected: 2 rows.** Eva earns 145,000 (Bob: 140,000).
    Ivy earns 118,000 (David: 115,000).
    """)
    return


@app.cell
def _(con, mo):
    q6_df = mo.sql(
        f"""
        SELECT e.name   AS employee,
               e.salary AS employee_salary,
               m.name   AS manager,
               m.salary AS manager_salary,
               e.salary - m.salary AS difference
        FROM employees AS e
        INNER JOIN employees AS m
            ON e.manager_id = m.employee_id
        WHERE e.salary > m.salary
        ORDER BY difference DESC;
        """,
        engine=con
    )
    return (q6_df,)


@app.cell(hide_code=True)
def _(mo, org_chart, q6_df):
    mo.vstack([
        mo.md("""
    **Q6 on the org chart.** 🟨 A **yellow** box earns more than
    their manager. The **dashed** box is that manager, and the
    **thick arrow** is the self-join match between them.
    Both pairs happen in Engineering.
        """),
        org_chart(q6_df["employee"], q6_df["manager"],
                  color="#FDE68A", border="#B45309"),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. Who joined the company before their manager?

    Dates compare like numbers: an earlier date is "smaller".

    **Expected: 3 rows** — Eva, Grace, and Kim. Each one was hired
    before the person they report to today.
    """)
    return


@app.cell
def _(con, mo):
    q7_df = mo.sql(
        f"""
        SELECT e.name      AS employee,
               e.hire_date AS employee_hired,
               m.name      AS manager,
               m.hire_date AS manager_hired
        FROM employees AS e
        INNER JOIN employees AS m
            ON e.manager_id = m.employee_id
        WHERE e.hire_date < m.hire_date
        ORDER BY e.hire_date;
        """,
        engine=con
    )
    return (q7_df,)


@app.cell(hide_code=True)
def _(mo, org_chart, q7_df):
    mo.vstack([
        mo.md("""
    **Q7 on the org chart.** 🟦 A **blue** box joined the company
    before their manager. The **dashed** box is that manager.
    Notice Eva: she is blue here **and** yellow in Q6 — she earns
    more than Bob *and* was hired before him.
        """),
        org_chart(q7_df["employee"], q7_df["manager"],
                  color="#BFDBFE", border="#1D4ED8"),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 7 — Pairs From One Table

    A self join can also pair up **peers**: two people who share
    something, such as the same manager.

    Here both aliases play the **same role**, so we call them
    `a` and `b` (not `e` and `m`).

    ### Q8. Which teammates share a manager?

    ```sql
    ON a.manager_id = b.manager_id     -- same manager
    AND a.employee_id < b.employee_id  -- the "<" trick
    ```

    **Expected: 7 pairs.** Bob–Carol · David–Eva · Frank–Grace ·
    Henry–Ivy · Henry–Leo · Ivy–Leo · Jack–Kim.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT a.name       AS teammate_1,
               b.name       AS teammate_2,
               m.name       AS shared_manager
        FROM employees AS a
        INNER JOIN employees AS b
            ON a.manager_id = b.manager_id
           AND a.employee_id < b.employee_id
        INNER JOIN employees AS m
            ON a.manager_id = m.employee_id
        ORDER BY a.employee_id, b.employee_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Why the `<` trick? Count the pairs three ways

    | Extra condition | What goes wrong |
    |-----------------|-----------------|
    | *(none)* | Every person is paired **with themselves** (Henry–Henry). |
    | `a.employee_id <> b.employee_id` | No self-pairs, but every pair appears **twice** (Henry–Ivy **and** Ivy–Henry). |
    | `a.employee_id < b.employee_id` | Each pair appears **once**. ✅ |

    **Expected:** 25, then 14, then 7.
    (25 = 14 two-way pairs + 11 self-pairs. 14 ÷ 2 = 7.)
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT
            (SELECT COUNT(*)
             FROM employees AS a
             INNER JOIN employees AS b
                 ON a.manager_id = b.manager_id) AS no_extra_rule,
            (SELECT COUNT(*)
             FROM employees AS a
             INNER JOIN employees AS b
                 ON a.manager_id = b.manager_id
                AND a.employee_id <> b.employee_id) AS with_not_equal,
            (SELECT COUNT(*)
             FROM employees AS a
             INNER JOIN employees AS b
                 ON a.manager_id = b.manager_id
                AND a.employee_id < b.employee_id) AS with_less_than;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. Teammates who earn very different salaries

    Pairs plus a filter: find teammates (same manager) whose salaries
    differ by **more than 20,000**. `ABS()` makes the difference
    positive, whichever person earns more.

    **Expected: 3 pairs.** Ivy–Leo (73,000), Henry–Leo (60,000), and
    David–Eva (30,000).
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT a.name AS teammate_1,
               a.salary AS salary_1,
               b.name AS teammate_2,
               b.salary AS salary_2,
               ABS(a.salary - b.salary) AS gap
        FROM employees AS a
        INNER JOIN employees AS b
            ON a.manager_id = b.manager_id
           AND a.employee_id < b.employee_id
        WHERE ABS(a.salary - b.salary) > 20000
        ORDER BY gap DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 8 — Count the Team

    ### Q11. How many direct reports does each person have?

    Now `m` goes on the **left**: we start from every person and look
    for their reports (`e`). `LEFT JOIN` keeps people with no reports.

    Two counts, side by side:

    * `COUNT(e.employee_id)` counts only **real** matches. ✅
    * `COUNT(*)` counts **rows** — and an unmatched person still has
      one row (full of `NULL`s), so it says **1**. ❌

    **Expected: 12 rows.** David has 3; Alice, Bob, Carol, and Frank
    have 2; everyone else has 0. Look at the `wrong_count` column:
    Eva shows 1, but nobody reports to her.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT m.name AS person,
               m.title,
               COUNT(e.employee_id) AS direct_reports,
               COUNT(*)             AS wrong_count,
               STRING_AGG(e.name, ', ' ORDER BY e.name) AS who
        FROM employees AS m
        LEFT JOIN employees AS e
            ON e.manager_id = m.employee_id
        GROUP BY m.employee_id, m.name, m.title
        ORDER BY direct_reports DESC, m.employee_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q12. Which teams cost more than 200,000?

    Use `INNER JOIN` this time (only people **with** reports).
    `GROUP BY` the manager, then `HAVING` keeps only the teams whose
    total salary is over 200,000.

    **Expected: 3 rows** — Alice (275,000), David (268,000), and
    Bob (260,000). Carol's and Frank's teams cost less.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT m.name             AS manager,
               COUNT(*)           AS team_size,
               SUM(e.salary)      AS team_payroll,
               ROUND(AVG(e.salary)) AS avg_salary
        FROM employees AS m
        INNER JOIN employees AS e
            ON e.manager_id = m.employee_id
        GROUP BY m.employee_id, m.name
        HAVING SUM(e.salary) > 200000
        ORDER BY team_payroll DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 9 — Two Steps Up the Ladder 🪜

    ### Q13. Who is each employee's manager's manager?

    You can use the same table **three times**. Each copy gets its
    own alias and its own role:

    | Alias | Role |
    |-------|------|
    | `e` | the employee |
    | `m` | their manager |
    | `g` | their manager's manager (the "grand-manager") |

    Each `JOIN` climbs **one step** up the org chart.

    **Expected: 9 rows.** Alice, Bob, and Carol are missing: they do
    not have two levels of managers above them.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT e.name AS employee,
               m.name AS manager,
               g.name AS grand_manager
        FROM employees AS e
        INNER JOIN employees AS m
            ON e.manager_id = m.employee_id
        INNER JOIN employees AS g
            ON m.manager_id = g.employee_id
        ORDER BY g.employee_id, m.employee_id, e.employee_id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 10 — Not Only Org Charts 📈

    A self join works for **any** table where one row should be
    compared with another row. A classic business case: compare
    **today** with **yesterday**.

    Meet `daily_sales` — one row per day for one week.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT sale_date,
               DAYNAME(sale_date) AS day,
               revenue
        FROM daily_sales
        ORDER BY sale_date;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q14. Day-over-day change

    Two aliases, two roles: `t` is **today**, `y` is **yesterday**.
    The `ON` rule says "yesterday is the day before today":

    ```sql
    ON t.sale_date = y.sale_date + 1
    ```

    In DuckDB, `date + 1` means "the next day".

    **Expected: 7 rows.** Monday has no yesterday in the table, so
    `LEFT JOIN` shows `NULL`. The biggest jump is **+500** (twice).
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT t.sale_date,
               DAYNAME(t.sale_date)   AS day,
               t.revenue              AS today,
               y.revenue              AS yesterday,
               t.revenue - y.revenue  AS change
        FROM daily_sales AS t
        LEFT JOIN daily_sales AS y
            ON t.sale_date = y.sale_date + 1
        ORDER BY t.sale_date;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q15. Which days were better than the day before?

    Same join, plus a `WHERE` filter. `INNER JOIN` is fine here,
    because Monday cannot be "better than yesterday" anyway.

    **Expected: 3 rows** — Tuesday, Friday, and Saturday.
    (Thursday tied Wednesday, so it does not count.)

    💡 In Week 9 you will meet `LAG()`, a window function that does
    this same job in a different way. The self join is the classic,
    works-everywhere version.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT t.sale_date,
               DAYNAME(t.sale_date)  AS day,
               y.revenue             AS yesterday,
               t.revenue             AS today,
               t.revenue - y.revenue AS increase
        FROM daily_sales AS t
        INNER JOIN daily_sales AS y
            ON t.sale_date = y.sale_date + 1
        WHERE t.revenue > y.revenue
        ORDER BY t.sale_date;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 11 — Explore: Pick a Manager 🎛️

    Choose a manager. The query below re-runs by itself and shows
    their team. This is the same self join as Q3 — only the
    `WHERE` filter changes.
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _managers = [r[0] for r in con.execute("""
        SELECT DISTINCT m.name, m.employee_id
        FROM employees AS e
        INNER JOIN employees AS m
            ON e.manager_id = m.employee_id
        ORDER BY m.employee_id
    """).fetchall()]
    team_picker = mo.ui.dropdown(
        options=_managers, value="David", label="Manager (`m`):"
    )
    team_picker
    return (team_picker,)


@app.cell
def _(con, mo, team_picker):
    _df = mo.sql(
        f"""
        SELECT m.name  AS manager,
               e.name  AS team_member,
               e.title,
               e.salary
        FROM employees AS e
        INNER JOIN employees AS m
            ON e.manager_id = m.employee_id
        WHERE m.name = '{team_picker.value}'
        ORDER BY e.salary DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Part 12 — Common Mistakes ⚠️

    The first two mistakes stop with an error. The cell below runs
    them for real, so you see DuckDB's exact message.
    """)
    return


@app.cell(hide_code=True)
def _(con, mo):
    _mistakes = [
        (
            "Mistake 1 — No aliases at all",
            """SELECT name
    FROM employees
    INNER JOIN employees
        ON manager_id = employee_id;""",
            "Both copies are called `employees`, so DuckDB cannot tell "
            "which `manager_id` you mean. **Fix:** give each copy its "
            "own alias — `employees AS e` and `employees AS m`.",
        ),
        (
            "Mistake 2 — Aliases, but no prefix on the column",
            """SELECT name
    FROM employees AS e
    INNER JOIN employees AS m
        ON e.manager_id = m.employee_id;""",
            "**Every** column exists in both copies. A bare `name` is "
            "always ambiguous in a self join. **Fix:** write `e.name` "
            "or `m.name` — always prefix every column.",
        ),
    ]

    _blocks = []
    for _title, _sql, _fix in _mistakes:
        try:
            con.execute(_sql)
            _err = "(no error?)"
        except Exception as _e:
            _err = str(_e)
        _blocks.append(mo.md(
            f"### {_title}\n\n"
            f"```sql\n{_sql}\n```\n\n"
            f"**DuckDB says:**\n\n```\n{_err}\n```\n\n"
            f"{_fix}"
        ))
    mo.vstack(_blocks)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Mistake 3 — The `ON` rule backwards (a silent bug 🐛)

    This one is **dangerous**: there is no error. The query runs and
    returns 11 rows. But the roles are swapped, so the labels lie.

    ```sql
    ON e.employee_id = m.manager_id   -- backwards!
    ```

    Look at the first row: it says Alice's "manager" is Carol.
    In fact, Carol reports to Alice.

    **Fix:** say the rule out loud — *"the **employee's**
    `manager_id` equals the **manager's** `employee_id`"* — so the
    `manager_id` column always sits next to the employee alias:
    `e.manager_id = m.employee_id`.
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT e.name AS employee,
               m.name AS manager_WRONG
        FROM employees AS e
        INNER JOIN employees AS m
            ON e.employee_id = m.manager_id
        ORDER BY e.employee_id, m.employee_id DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Mistake 4 — Forgetting the `<` rule in pairs

    You saw it in Q9: without `a.employee_id < b.employee_id` you get
    self-pairs and double-counted pairs. A report that says "14
    teammate pairs" when the truth is 7 is a **silent** error, too.

    ---
    # Part 13 — Cheat Sheet 📋

    ```sql
    -- Pattern 1: row → its parent (employee → manager)
    SELECT e.name AS employee, m.name AS manager
    FROM employees AS e
    LEFT JOIN employees AS m              -- LEFT keeps the top boss
        ON e.manager_id = m.employee_id;

    -- Pattern 2: pairs of peers (each pair once)
    SELECT a.name, b.name
    FROM employees AS a
    INNER JOIN employees AS b
        ON a.manager_id = b.manager_id    -- what they share
       AND a.employee_id < b.employee_id; -- no self-pairs, no duplicates

    -- Pattern 3: row → the row before it (today vs. yesterday)
    SELECT t.sale_date, t.revenue - y.revenue AS change
    FROM daily_sales AS t
    LEFT JOIN daily_sales AS y
        ON t.sale_date = y.sale_date + 1;
    ```

    | Remember | Why |
    |----------|-----|
    | One table, **two aliases** | Each alias is a copy with a **role**. |
    | Name aliases after roles | `e`/`m`, `t`/`y` — the query reads like English. |
    | **Prefix every column** | Every column exists in both copies. |
    | Say the `ON` rule out loud | It catches the "backwards" bug. |
    | `INNER` drops rows with no partner | Alice (no manager), Monday (no yesterday). |
    | `LEFT` keeps them, with `NULL` | Use `COALESCE` for a friendly label. |
    | Pairs need `<` | `=` alone → self-pairs; `<>` → duplicates. |
    | Count with `COUNT(alias.key)` | `COUNT(*)` counts an unmatched row as 1. |
    | One more step = one more copy | Grand-manager needs three aliases. |

    ---
    # Try It Yourself ✍️

    Write each query in a new cell, then open the solution to check.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Exercise 1 — List each employee with their manager's department.": mo.md("""
    ```sql
    SELECT e.name AS employee,
           e.department,
           m.name AS manager,
           m.department AS manager_department
    FROM employees AS e
    INNER JOIN employees AS m
        ON e.manager_id = m.employee_id;
    ```
    11 rows. Bob and Carol are the only ones whose manager (Alice)
    works in a different department.
        """),
        "Exercise 2 — Who works in a different department than their manager?": mo.md("""
    ```sql
    SELECT e.name, e.department, m.department AS manager_department
    FROM employees AS e
    INNER JOIN employees AS m
        ON e.manager_id = m.employee_id
    WHERE e.department <> m.department;
    ```
    2 rows: Bob (Engineering) and Carol (Sales). Their manager, Alice,
    is in Leadership.
        """),
        "Exercise 3 — Who has no direct reports? (Hint: LEFT JOIN + IS NULL)": mo.md("""
    ```sql
    SELECT m.name
    FROM employees AS m
    LEFT JOIN employees AS e
        ON e.manager_id = m.employee_id
    WHERE e.employee_id IS NULL
    ORDER BY m.employee_id;
    ```
    7 rows: Eva, Grace, Henry, Ivy, Jack, Kim, Leo.
        """),
        "Exercise 4 — Pair up every two employees in the same department.": mo.md("""
    ```sql
    SELECT a.name, b.name, a.department
    FROM employees AS a
    INNER JOIN employees AS b
        ON a.department = b.department
       AND a.employee_id < b.employee_id
    ORDER BY a.employee_id, b.employee_id;
    ```
    25 pairs: 15 in Engineering (6 people) and 10 in Sales (5 people).
    Alice is alone in Leadership, so she has no pair.
        """),
        "Exercise 5 — Who earns more than their grand-manager?": mo.md("""
    ```sql
    SELECT e.name, e.salary, g.name AS grand_manager, g.salary AS gm_salary
    FROM employees AS e
    INNER JOIN employees AS m
        ON e.manager_id = m.employee_id
    INNER JOIN employees AS g
        ON m.manager_id = g.employee_id
    WHERE e.salary > g.salary;
    ```
    0 rows! Eva (145,000) earns more than Bob, but her grand-manager
    is Alice (180,000). A query that returns nothing can still be a
    correct answer.
        """),
        "Exercise 6 — Which days fell below the day before?": mo.md("""
    ```sql
    SELECT t.sale_date, y.revenue AS yesterday, t.revenue AS today
    FROM daily_sales AS t
    INNER JOIN daily_sales AS y
        ON t.sale_date = y.sale_date + 1
    WHERE t.revenue < y.revenue;
    ```
    2 rows: Wednesday 2026-10-07 (1,350 → 1,100) and Sunday 2026-10-11
    (2,100 → 1,900).
        """),
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ### Key Takeaway

    > A self join is just a join where **both sides are the same
    > table**. Give each side an alias that names its **role**, write
    > the `ON` rule that connects the roles, and everything you know
    > about `INNER JOIN`, `LEFT JOIN`, `WHERE`, and `GROUP BY` works
    > exactly as before.

    **Further reading:**
    [DuckDB joins](https://duckdb.org/docs/lts/sql/query_syntax/from) ·
    [Marimo SQL cells](https://docs.marimo.io/guides/working_with_data/sql/)

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
