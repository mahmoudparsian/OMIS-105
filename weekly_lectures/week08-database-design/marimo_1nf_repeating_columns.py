import marimo

__generated_with = "0.24.2"
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
        # 📞 Database Design & 1NF: Solving Repeating Groups

        Welcome to Part 2 of First Normal Form (1NF)! 

        In this interactive notebook, we examine another common violation of **1NF**: **Repeating Groups / Repeating Columns** (e.g., `phone_number_1`, `phone_number_2`, `phone_number_3`).

        ---

        ### 🎯 Core Concepts Covered
        1. **What are Repeating Groups?** Why creating numbered columns for multiple values breaks 1NF.
        2. **Drawbacks of Repeating Columns**:
           - Rigid schema (what if a customer has 4 phone numbers?).
           - Inefficient storage and NULL values.
           - Complicated queries and indexing.
        3. **DuckDB SQL Normalization**: Using `UNPIVOT` to transform repeating columns into a clean 1NF table.
        """
    )
    return


@app.cell
def __(duckdb):
    # Initialize an in-memory DuckDB database
    con = duckdb.connect(database=":memory:")

    # Create unnormalized table with repeating columns (violates 1NF)
    con.execute("""
        CREATE TABLE customer_contacts_non_1nf (
            customer_id INT,
            customer_name VARCHAR,
            phone_number_1 VARCHAR,
            phone_number_2 VARCHAR,
            phone_number_3 VARCHAR
        );
    """)

    con.execute("""
        INSERT INTO customer_contacts_non_1nf VALUES
            (201, 'Alice Smith', '555-0101', '555-0102', NULL),
            (202, 'Bob Jones', '555-0201', NULL, NULL),
            (203, 'Charlie Brown', '555-0301', '555-0302', '555-0303');
    """)

    # Create normalized table (1NF Compliant)
    con.execute("""
        CREATE TABLE customer_contacts_1nf (
            customer_id INT,
            phone_type VARCHAR,
            phone_number VARCHAR,
            PRIMARY KEY (customer_id, phone_number)
        );
    """)

    con.execute("""
        INSERT INTO customer_contacts_1nf VALUES
            (201, 'primary', '555-0101'),
            (201, 'secondary', '555-0102'),
            (202, 'primary', '555-0201'),
            (203, 'primary', '555-0301'),
            (203, 'secondary', '555-0302'),
            (203, 'work', '555-0303');
    """)
    return con,


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 🚨 The Anti-Pattern: Repeating Columns (`phone_number_1`, `2`, `3`)

        Look at the table structure below. To allow multiple phone numbers per customer, columns were created for each additional number.

        ### Why is this BAD design?
        * **Inflexible Schema**: If a customer has a 4th phone number, you have to alter the table structure (`ALTER TABLE ADD COLUMN phone_number_4`).
        * **Wasted Space (NULLs)**: Customers with only 1 phone number leave multiple columns filled with `NULL` values.
        * **Difficult Searches**: Finding who owns phone number `'555-0302'` requires checking every single column:
          ```sql
          WHERE phone_number_1 = '555-0302' OR phone_number_2 = '555-0302' OR phone_number_3 = '555-0302'
          ```
        """
    )
    return


@app.cell
def __(con, mo):
    df_non_1nf = con.execute("SELECT * FROM customer_contacts_non_1nf").df()
    mo.md(f"### ❌ Table Before 1NF (Repeating Columns Anti-Pattern)\n{mo.ui.table(df_non_1nf)}")
    return df_non_1nf,


@app.cell
def __(mo):
    mo.md(
        r"""
        ## ✅ The 1NF Fix: Row-Based Design

        To bring this table into **First Normal Form (1NF)**:
        1. Eliminate repeating attributes across columns.
        2. Move repeating data into new **rows**.
        3. Option to include a descriptor column (e.g., `phone_type` like 'primary', 'secondary', 'work').

        Now, a customer can have 0, 1, or 100 phone numbers without changing the database schema!
        """
    )
    return


@app.cell
def __(con, mo):
    df_1nf = con.execute("SELECT * FROM customer_contacts_1nf").df()
    mo.md(f"### ✅ Table in 1NF (Normalized)\n{mo.ui.table(df_1nf)}")
    return df_1nf,


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 🛠️ DuckDB Magic: Unpivoting Repeating Columns to 1NF

        In DuckDB SQL, you can automatically convert wide repeating columns into a tall 1NF table using the `UNPIVOT` clause!
        """
    )
    return


@app.cell
def __(con, mo):
    unpivot_query = """
    UNPIVOT customer_contacts_non_1nf
    ON phone_number_1, phone_number_2, phone_number_3
    INTO
        NAME phone_slot
        VALUE phone_number;
    """

    unpivoted_df = con.execute(unpivot_query).df()

    mo.md(
        f"""
        ### 🔄 Live SQL Transformation Result (`UNPIVOT`)
        ```sql
        {unpivot_query.strip()}
        ```
        {mo.ui.table(unpivoted_df)}
        """
    )
    return unpivot_query, unpivoted_df


@app.cell
def __(mo):
    search_input = mo.ui.text(
        value='555-0302',
        label='Search Phone Number:'
    )
    search_input
    return search_input,


@app.cell
def __(con, mo, search_input):
    filtered_df = con.execute(
        "SELECT * FROM customer_contacts_1nf WHERE phone_number = ?",
        [search_input.value]
    ).df()

    mo.md(
        f"""
        ### 🔍 Simplified Single-Column Searching in 1NF
        In 1NF, searching for a phone number requires checking only **one column** instead of three:

        ```sql
        SELECT * FROM customer_contacts_1nf WHERE phone_number = '{search_input.value}';
        ```
        {mo.ui.table(filtered_df)}
        """
    )
    return filtered_df,


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## 💡 Summary: Repeating Columns vs 1NF

        | Aspect | Repeating Columns (Non-1NF) | Normalized Rows (1NF) |
        | :--- | :--- | :--- |
        | **Structure** | `phone_1`, `phone_2`, `phone_3` | `phone_number` |
        | **Flexibility** | Fixed limit (max 3 numbers) | Unlimited numbers per entity |
        | **Storage** | Sparse with lots of `NULL`s | Compact, only stores existing values |
        | **Queries** | `WHERE col1 = x OR col2 = x OR col3 = x` | `WHERE phone_number = x` |
        """
    )
    return


if __name__ == "__main__":
    app.run()
