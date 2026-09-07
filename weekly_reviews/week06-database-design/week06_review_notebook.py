import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from pathlib import Path

    import duckdb

    DATA_DIR = Path(__file__).parent / "data"
    con = duckdb.connect(database=":memory:")
    return DATA_DIR, con


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # OMIS 105 — Week 6 Review: Database Design, Constraints & Views

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    Week 2 normalized a table by intuition. This week formalizes it — 1NF,
    2NF, 3NF — then protects the design with constraints and simplifies it
    with views.

    ### What This Notebook Covers

    | Topic | SQL You Will Use |
    |-------|-----------------|
    | Formal normalization | Functional dependencies, 1NF, 2NF, 3NF |
    | Protect the data | `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK` |
    | Simplify access | `CREATE VIEW` |
    | Change data safely | `UPDATE`, `DELETE`, the SELECT-then-DELETE pattern |

    ### How to Use

    Run the cells from top to bottom. Every database cell takes `con`, the
    DuckDB connection created in the setup cell. Read the markdown between
    queries — it explains the *why*, not just the *how*.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Setup — Build the Company Database

    `company_data.csv` lives in this folder's `data/` directory. We load it into a
    staging table, then split it into `departments`, `employees`, `projects`, and
    `assignments`.

    The data has deliberate imperfections: some employees have a `NULL` department,
    one department has no employees, and `manager_id` points back into the same
    table. Those are the cases that make JOINs interesting.
    """)
    return


@app.cell
def _(DATA_DIR, con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE raw_data AS
            SELECT * FROM read_csv_auto('{DATA_DIR}/company_data.csv')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT 'company_data.csv loaded!' AS status,
               COUNT(*) AS total_rows
        FROM raw_data
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE departments (
            dept_id       INTEGER PRIMARY KEY,
            dept_name     VARCHAR NOT NULL,
            dept_location VARCHAR NOT NULL,
            budget        DECIMAL(12,2) NOT NULL
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO departments VALUES
            (10, 'Engineering',  'San Jose',      2000000),
            (20, 'Marketing',    'San Francisco', 1200000),
            (30, 'Sales',        'Santa Clara',   1500000),
            (40, 'Finance',      'Palo Alto',     1000000),
            (50, 'HR',           'San Jose',       800000),
            (60, 'Legal',        'San Francisco',  600000)
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- departments: 6 rows (note: Legal has NO employees)
        SELECT * FROM departments ORDER BY dept_id
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE employees (
            emp_id     INTEGER PRIMARY KEY,
            emp_name   VARCHAR NOT NULL,
            gender     VARCHAR NOT NULL,
            dept_id    INTEGER,
            salary     DECIMAL(10,2) NOT NULL,
            hire_date  DATE NOT NULL,
            manager_id INTEGER
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO employees
        SELECT emp_id, emp_name, gender, dept_id, salary, hire_date, manager_id
        FROM   raw_data
        ORDER BY emp_id
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- employees: 30 rows (3 have NULL dept_id — unassigned)
        SELECT * FROM employees ORDER BY emp_id LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE projects (
            project_id   INTEGER PRIMARY KEY,
            project_name VARCHAR NOT NULL,
            budget       DECIMAL(12,2) NOT NULL,
            status       VARCHAR NOT NULL,
            start_date   DATE NOT NULL
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO projects VALUES
            (101, 'Cloud Migration',   500000, 'Active',    '2024-01-15'),
            (102, 'Mobile App v2',     300000, 'Active',    '2024-03-01'),
            (103, 'Data Warehouse',    450000, 'Active',    '2024-06-10'),
            (104, 'Brand Refresh',     200000, 'Completed', '2023-09-01'),
            (105, 'CRM Upgrade',       350000, 'Active',    '2024-04-20'),
            (106, 'Security Audit',    150000, 'Completed', '2023-11-15'),
            (107, 'AI Chatbot',        400000, 'Planning',  '2025-01-01'),
            (108, 'Office Relocation', 250000, 'Planning',  '2025-03-01')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- projects: 8 rows
        SELECT * FROM projects ORDER BY project_id
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE assignments (
            assignment_id INTEGER PRIMARY KEY,
            emp_id        INTEGER,
            project_id    INTEGER,
            role          VARCHAR NOT NULL,
            hours_per_week INTEGER NOT NULL
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO assignments VALUES
            (1,  1,  101, 'Lead',       20),
            (2,  2,  101, 'Developer',  30),
            (3,  3,  102, 'Lead',       25),
            (4,  4,  101, 'Developer',  35),
            (5,  5,  102, 'Developer',  30),
            (6,  6,  103, 'Developer',  40),
            (7,  7,  104, 'Lead',       15),
            (8,  8,  105, 'Analyst',    20),
            (9,  9,  104, 'Analyst',    25),
            (10, 10, 105, 'Analyst',    30),
            (11, 12, 105, 'Lead',       20),
            (12, 13, 105, 'Sales Rep',  25),
            (13, 14, 106, 'Auditor',    35),
            (14, 18, 106, 'Lead',       15),
            (15, 19, 103, 'Analyst',    20),
            (16, 20, 103, 'Analyst',    25),
            (17, 29, 101, 'Developer',  30),
            (18, 29, 102, 'Developer',  15),
            (19, 1,  107, 'Lead',       10),
            (20, 3,  107, 'Developer',  15),
            (21, 18, 103, 'Analyst',    10),
            (22, 7,  108, 'Lead',       10),
            (23, 23, 108, 'Coordinator',20),
            (24, 12, 106, 'Auditor',    10),
            (25, 30, 104, 'Analyst',    20)
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- assignments: 25 rows
        SELECT * FROM assignments ORDER BY assignment_id LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        DROP TABLE IF EXISTS raw_data
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6.1 — Normalization: The Formal Rules

    In Week 2, we split a flat CSV into multiple tables to remove redundancy.
    That was **normalization by intuition**. Now we formalize it.

    ### Functional Dependencies

    A **functional dependency** means one column uniquely determines another:

    ```
    emp_id → emp_name        (knowing emp_id gives you exactly one emp_name)
    dept_id → dept_name      (knowing dept_id gives you exactly one dept_name)
    (emp_id, project_id) → hours_per_week   (the pair determines the hours)
    ```

    This is the foundation of normalization.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### First Normal Form (1NF)

    **Rule:** Every cell holds a single atomic value. No lists, no arrays, no repeating groups.

    Here's a table that **violates 1NF**:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- BAD: skills column holds multiple values in one cell
        CREATE OR REPLACE TABLE bad_1nf (
            emp_id   INTEGER,
            emp_name VARCHAR,
            skills   VARCHAR
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO bad_1nf VALUES
            (1, 'Alice', 'Python, SQL, Java'),
            (2, 'Bob',   'SQL, Excel'),
            (3, 'Carol', 'Python, R, SQL, Tableau')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM bad_1nf
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Problem:** You can't easily query "find everyone who knows SQL" because
    skills are buried inside a comma-separated string.

    **Fix:** One row per skill (or better: a separate skills table with a bridge).
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- GOOD: 1NF — one skill per row
        CREATE OR REPLACE TABLE good_1nf (
            emp_id   INTEGER,
            emp_name VARCHAR,
            skill    VARCHAR
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO good_1nf VALUES
            (1, 'Alice', 'Python'), (1, 'Alice', 'SQL'), (1, 'Alice', 'Java'),
            (2, 'Bob',   'SQL'),    (2, 'Bob',   'Excel'),
            (3, 'Carol', 'Python'), (3, 'Carol', 'R'),
            (3, 'Carol', 'SQL'),    (3, 'Carol', 'Tableau')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM good_1nf ORDER BY emp_id, skill
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Now we CAN query: "Who knows SQL?"
        SELECT DISTINCT emp_name
        FROM   good_1nf
        WHERE  skill = 'SQL'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Second Normal Form (2NF)

    **Rule:** 1NF + every non-key column depends on the **entire** primary key
    (not just part of it).

    Only matters when the primary key has **multiple columns**.

    Here's a table that **violates 2NF**:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- BAD: product_name depends only on product_id, not on (order_id, product_id)
        CREATE OR REPLACE TABLE bad_2nf (
            order_id      INTEGER,
            product_id    INTEGER,
            quantity      INTEGER,
            product_name  VARCHAR,
            product_price DECIMAL(10,2),
            PRIMARY KEY (order_id, product_id)
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO bad_2nf VALUES
            (1, 100, 2, 'Laptop', 999.99),
            (1, 200, 1, 'Mouse',   29.99),
            (2, 100, 1, 'Laptop', 999.99),
            (3, 200, 3, 'Mouse',   29.99)
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM bad_2nf
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Problem:** `product_name` and `product_price` depend only on `product_id`,
    not on the full key `(order_id, product_id)`. That's a **partial dependency**.
    Result: "Laptop" and 999.99 are stored 2 times.

    **Fix:** Move product info to its own table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **GOOD: 2NF — separate tables**

    Products (stored ONCE):
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE products_2nf (
            product_id    INTEGER PRIMARY KEY,
            product_name  VARCHAR,
            product_price DECIMAL(10,2)
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO products_2nf VALUES
            (100, 'Laptop', 999.99),
            (200, 'Mouse', 29.99)
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM products_2nf
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Orders (IDs only, no redundancy):
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE orders_2nf (
            order_id   INTEGER,
            product_id INTEGER,
            quantity   INTEGER,
            PRIMARY KEY (order_id, product_id)
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO orders_2nf VALUES
            (1, 100, 2), (1, 200, 1), (2, 100, 1), (3, 200, 3)
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM orders_2nf
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Third Normal Form (3NF)

    **Rule:** 2NF + no non-key column depends on another non-key column
    (no **transitive dependencies**).

    Here's a table that **violates 3NF**:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- BAD: dept_name depends on dept_id, not directly on emp_id
        CREATE OR REPLACE TABLE bad_3nf (
            emp_id    INTEGER PRIMARY KEY,
            emp_name  VARCHAR,
            dept_id   INTEGER,
            dept_name VARCHAR,
            dept_loc  VARCHAR
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        INSERT INTO bad_3nf VALUES
            (1, 'Alice', 10, 'Engineering', 'San Jose'),
            (2, 'Bob',   10, 'Engineering', 'San Jose'),
            (3, 'Carol', 20, 'Marketing',   'San Francisco'),
            (4, 'David', 20, 'Marketing',   'San Francisco')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM bad_3nf
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Problem:** `dept_name` and `dept_loc` depend on `dept_id`, not on `emp_id`.
    That's a **transitive dependency**: `emp_id → dept_id → dept_name`.
    Result: "Engineering, San Jose" stored twice.

    **Fix:** This is exactly what our `employees` + `departments` tables already do!
    The `employees` table stores only `dept_id`, and the department details live in `departments`.

    ### Normalization Summary

    | Normal Form | Rule | Fixes |
    |-------------|------|-------|
    | **1NF** | Atomic values, no lists | Split multi-value cells into rows |
    | **2NF** | No partial dependencies | Move columns that depend on part of the key |
    | **3NF** | No transitive dependencies | Move columns that depend on non-key columns |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6.2 — Constraints: The Database Enforces Your Rules

    Constraints prevent bad data from entering the database.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Demo table with ALL constraint types
        CREATE OR REPLACE TABLE employees_strict (
            emp_id   INTEGER PRIMARY KEY,
            emp_name VARCHAR NOT NULL,
            email    VARCHAR UNIQUE,
            dept_id  INTEGER REFERENCES departments(dept_id),
            salary   DECIMAL(10,2) CHECK (salary > 0),
            status   VARCHAR DEFAULT 'Active'
        )
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Good insert — all constraints satisfied
        INSERT INTO employees_strict (emp_id, emp_name, email, dept_id, salary)
        VALUES (1, 'Test User', 'test@company.com', 10, 100000)
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Notice: status is 'Active' even though we didn't provide it — that's the DEFAULT
        SELECT * FROM employees_strict
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's see what happens when we **violate** each constraint:
    """)
    return


@app.cell
def _(con):
    # Violate NOT NULL — the database rejects the insert
    try:
        con.execute(
            f"""
            INSERT INTO employees_strict (emp_id, email) VALUES (2, 'x@y.com')
            """
        )
    except Exception as e:
        print(f"NOT NULL violation: {e}")
    return


@app.cell
def _(con):
    # Violate UNIQUE — duplicate email rejected
    try:
        con.execute(
            f"""
            INSERT INTO employees_strict (emp_id, emp_name, email, salary)
            VALUES (3, 'Another', 'test@company.com', 90000)
            """
        )
    except Exception as e:
        print(f"UNIQUE violation: {e}")
    return


@app.cell
def _(con):
    # Violate CHECK — negative salary rejected
    try:
        con.execute(
            f"""
            INSERT INTO employees_strict (emp_id, emp_name, email, salary)
            VALUES (4, 'Negative', 'neg@co.com', -5000)
            """
        )
    except Exception as e:
        print(f"CHECK violation: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The database itself rejects bad data. You don't need application code to validate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6.3 — Views: A Saved Query That Acts Like a Table

    A view is a **virtual table** — it stores a query, not data.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE VIEW dept_summary AS
        SELECT d.dept_name,
               COUNT(e.emp_id)         AS headcount,
               ROUND(AVG(e.salary), 0) AS avg_salary,
               MIN(e.salary)           AS min_salary,
               MAX(e.salary)           AS max_salary
        FROM   departments d
        LEFT JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Use it like a regular table
        SELECT * FROM dept_summary ORDER BY avg_salary DESC
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- A view that hides salary info (for non-HR users)
        CREATE OR REPLACE VIEW employee_directory AS
        SELECT e.emp_name,
               e.gender,
               d.dept_name,
               e.hire_date
        FROM   employees e
        LEFT JOIN departments d ON e.dept_id = d.dept_id
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM employee_directory ORDER BY emp_name LIMIT 10
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Why Views?

    | Use Case | Example |
    |----------|---------|
    | **Simplification** | Complex JOIN hidden behind a simple view name |
    | **Security** | Hide salary column from non-HR users |
    | **Reusability** | Define once, query many times |
    | **Consistency** | Everyone uses the same definition |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6.4 — UPDATE and DELETE: Modifying Data

    Until now, we've only queried data. Now we change it.

    **Golden rule:** Always test your WHERE clause with SELECT first,
    then change SELECT to UPDATE or DELETE.

    ### UPDATE
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **BEFORE** — current Engineering salaries:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name, salary
        FROM   employees
        WHERE  dept_id = 10
        ORDER BY emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Give Engineering a **10% raise**:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        UPDATE employees
        SET    salary = ROUND(salary * 1.10, 2)
        WHERE  dept_id = 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **AFTER** — Engineering salaries (10% raise applied):
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name, salary
        FROM   employees
        WHERE  dept_id = 10
        ORDER BY emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### UPDATE with CASE — conditional updates
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- Tiered raises: 8% under 100K, 5% under 130K, 3% above
        UPDATE employees
        SET salary = ROUND(
            CASE
                WHEN salary < 100000  THEN salary * 1.08
                WHEN salary < 130000  THEN salary * 1.05
                ELSE salary * 1.03
            END, 2)
        WHERE dept_id = 30
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **AFTER** — Sales team salaries (tiered raises applied):
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name, salary
        FROM   employees
        WHERE  dept_id = 30
        ORDER BY salary DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### DELETE

    > **WARNING:** `DELETE` without `WHERE` deletes EVERY row in the table!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Step 1:** SELECT first to verify which rows will be affected:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        -- These rows will be deleted
        SELECT emp_name, salary, hire_date
        FROM   employees
        WHERE  emp_name = 'Ben'
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Step 2:** Now delete (same WHERE clause):
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        DELETE FROM employees
        WHERE  emp_name = 'Ben'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Remaining unassigned employees after deletion:
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT emp_name, salary
        FROM   employees
        WHERE  dept_id IS NULL
        ORDER BY emp_name
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Best Practice: The SELECT-then-DELETE Pattern

    ```sql
    -- Step 1: VERIFY (run this first)
    SELECT * FROM employees WHERE <your_condition>

    -- Step 2: DELETE (only after Step 1 looks correct)
    DELETE FROM employees WHERE <your_condition>
    ```

    Same pattern works for UPDATE. This prevents accidental mass changes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Week 6 Summary

    | Concept | What It Solves |
    |---------|---------------|
    | 1NF | One value per cell — no comma-separated lists |
    | 2NF | No partial dependency on part of a composite key |
    | 3NF | No column depending on another non-key column |
    | `NOT NULL` / `UNIQUE` / `CHECK` | The database rejects bad data itself |
    | `CREATE VIEW` | Save a query and reuse it like a table |
    | `UPDATE` / `DELETE` | Change data — always `SELECT` first to check the `WHERE` |

    ### Looking Ahead

    Weeks 7–10 move to a SaaS analytics dataset and shift from *writing* queries
    to making them fast, safe, and production-ready.
    """)
    return


if __name__ == "__main__":
    app.run()
