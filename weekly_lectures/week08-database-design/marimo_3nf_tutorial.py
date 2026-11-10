import marimo

__generated_by = "0.1.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import duckdb
    import pandas as pd
    return duckdb, mo, pd


@app.cell
def __(mo):
    mo.md(
        r"""
        # 🔗 Database Design & Third Normal Form (3NF) with DuckDB

        Welcome to the final interactive notebook on Database Normalization: **Third Normal Form (3NF)**!

        ---

        ### 🎯 Core Concepts Covered
        1. **Prerequisite for 3NF**: The table must already be in **2NF**.
        2. **Transitive Dependency**: What happens when a non-key column depends on *another non-key column* instead of the primary key directly.
        3. **Drawbacks of Transitive Dependencies**: Redundant data, update anomalies, and structural integrity risks.
        4. **Decomposition**: Splitting 2NF tables into 3NF tables using DuckDB SQL (`CREATE TABLE AS SELECT DISTINCT ...`).
        """
    )
    return


@app.cell
def __(duckdb):
    # Initialize an in-memory DuckDB database
    con = duckdb.connect(database=":memory:")

    # Create 2NF table with single-column Primary Key (employee_id)
    # This table satisfies 2NF (no partial key dependencies), but violates 3NF!
    # Transitive dependency: department_name and location depend on department_id, NOT directly on employee_id!
    con.execute("""
        CREATE TABLE employee_departments_2nf (
            employee_id INT PRIMARY KEY,
            employee_name VARCHAR,
            department_id INT,
            department_name VARCHAR,
            office_location VARCHAR
        );
    """)

    con.execute("""
        INSERT INTO employee_departments_2nf VALUES
            (1, 'Alice Smith', 10, 'Engineering', 'Building A'),
            (2, 'Bob Jones', 20, 'Marketing', 'Building B'),
            (3, 'Charlie Brown', 10, 'Engineering', 'Building A'),
            (4, 'Diana Prince', 30, 'Finance', 'Building C'),
            (5, 'Evan Wright', 20, 'Marketing', 'Building B');
    """)

    # Decomposed 3NF Tables
    con.execute("""
        CREATE TABLE departments_3nf AS 
        SELECT DISTINCT department_id, department_name, office_location 
        FROM employee_departments_2nf;
    """)

    con.execute("""
        CREATE TABLE employees_3nf AS 
        SELECT employee_id, employee_name, department_id 
        FROM employee_departments_2nf;
    """)
    return con,


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 🚨 The Problem: Table in 2NF, but Violating 3NF

        Look at the table below. The primary key is **`employee_id`**.

        ### What is a Transitive Dependency?
        * `employee_name` depends directly on `employee_id`.
        * `department_id` depends directly on `employee_id`.
        * **However**: `department_name` and `office_location` depend on **`department_id`**, which is a non-key column!
        * *Transitive Link*: `employee_id` ➔ `department_id` ➔ `department_name` / `office_location`.

        ### Why is this BAD?
        * **Redundancy**: Repeating `'Engineering'` and `'Building A'` for every employee in department 10.
        * **Update Anomaly**: If Marketing moves from `Building B` to `Building D`, you must update every employee row in that department.
        * **Insertion Anomaly**: You cannot create a new department unless an employee is assigned to it!
        """
    )
    return


@app.cell
def __(con, mo):
    df_2nf = con.execute("SELECT * FROM employee_departments_2nf").df()
    mo.md(f"### ❌ Table in 2NF (Violates 3NF due to Transitive Dependencies)
{mo.ui.table(df_2nf)}")
    return df_2nf,


@app.cell
def __(mo):
    mo.md(
        r"""
        ## ✅ The 3NF Fix: Removing Transitive Dependencies

        To achieve **3NF**, every non-key column must depend **only on the primary key, the whole primary key, and nothing but the primary key**.

        We remove the transitive dependency by decomposing into **2 separate tables**:
        1. **`Employees`**: Holds employee details and links to `department_id` (Foreign Key).
        2. **`Departments`**: Holds department details (`department_id` ➔ `department_name`, `office_location`).
        """
    )
    return


@app.cell
def __(con, mo):
    df_employees = con.execute("SELECT * FROM employees_3nf").df()
    df_departments = con.execute("SELECT * FROM departments_3nf").df()

    mo.md(
        f"""
        ### ✅ Decomposed 3NF Tables

        #### 1. Employees Table (`employee_id` is Primary Key)
        {mo.ui.table(df_employees)}

        #### 2. Departments Table (`department_id` is Primary Key)
        {mo.ui.table(df_departments)}
        """
    )
    return df_departments, df_employees


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 🛠️ DuckDB Magic: Rejoining 3NF Tables with `JOIN`

        By separating the data into 3NF, we maintain clean single-purpose tables without data duplication.
        When we need a full workforce report, we simply use an inner `JOIN` in DuckDB SQL:
        """
    )
    return


@app.cell
def __(con, mo):
    join_query = """
    SELECT 
        e.employee_id,
        e.employee_name,
        d.department_id,
        d.department_name,
        d.office_location
    FROM employees_3nf e
    JOIN departments_3nf d ON e.department_id = d.department_id;
    """

    reconstructed_df = con.execute(join_query).df()

    mo.md(
        f"""
        ### 🔄 Reconstructed View using SQL JOIN
        ```sql
        {join_query.strip()}
        ```
        {mo.ui.table(reconstructed_df)}
        """
    )
    return join_query, reconstructed_df


@app.cell
def __(mo):
    dept_selector = mo.ui.dropdown(
        options=['Engineering', 'Marketing', 'Finance'],
        value='Engineering',
        label='Select Department to Filter:'
    )
    dept_selector
    return dept_selector,


@app.cell
def __(con, mo, dept_selector):
    filtered_df = con.execute("""
        SELECT 
            e.employee_id,
            e.employee_name,
            d.department_name,
            d.office_location
        FROM employees_3nf e
        JOIN departments_3nf d ON e.department_id = d.department_id
        WHERE d.department_name = ?
    """, [dept_selector.value]).df()

    mo.md(
        f"""
        ### 🔍 Interactive Query on 3NF Schema
        Showing employees and location for **{dept_selector.value}**:

        {mo.ui.table(filtered_df)}
        """
    )
    return filtered_df,


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## 💡 Summary: Normalization Ladder (1NF ➔ 2NF ➔ 3NF)

        | Normal Form | Rule Summary | What it Eliminates |
        | :--- | :--- | :--- |
        | **1NF** | Atomic values, unique primary key | Multi-value cells & repeating columns |
        | **2NF** | In 1NF + Full functional dependency on composite key | Partial dependencies |
        | **3NF** | In 2NF + Non-key columns depend ONLY on primary key | Transitive dependencies |

        > 🧠 **Memorable Rule of Thumb**: *"Every non-key attribute must provide a fact about the key, the whole key, and nothing but the key."*
        """
    )
    return


if __name__ == "__main__":
    app.run()
