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
    # Week 2: Relational Thinking — Demo Notebook
    ## OMIS 105: Database Management Systems

    In this notebook we will:
    1. Load multiple related tables
    2. Explore primary and foreign keys
    3. Verify referential integrity
    4. Preview multi-table queries
    5. Understand table relationships
    """)
    return


@app.cell
def _():
    import duckdb
    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE categories AS
            SELECT * FROM read_csv_auto('./data/categories.csv')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE products AS
            SELECT * FROM read_csv_auto('./data/products.csv')
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        f"""
        CREATE OR REPLACE TABLE customers AS
            SELECT * FROM read_csv_auto('./data/customers.csv')
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tables Loaded
    Let's inspect each table.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM categories
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM products
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT * FROM customers
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Understanding Primary Keys
    A primary key uniquely identifies each row. Let's verify uniqueness.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT customer_id, COUNT(*) AS cnt
                FROM customers
                GROUP BY customer_id
                HAVING COUNT(*) > 1
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT product_id, COUNT(*) AS cnt
                FROM products
                GROUP BY product_id
                HAVING COUNT(*) > 1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Candidate Keys
    An email could also serve as a PK — let's check if it's unique.
    """)
    return


@app.cell
def _(con):
    # Check if email is unique across customers
    con.execute(
        f"""
        SELECT email, COUNT(*) AS cnt
        FROM customers
        GROUP BY email
        HAVING COUNT(*) > 1
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Foreign Keys — Linking Tables
    `products.category_id` references `categories.category_id`.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT p.product_id, p.product_name, p.category_id,
                       c.category_name
                FROM products p, categories c
                WHERE p.category_id = c.category_id
                LIMIT 10
        """
    ).fetchdf()
    return


@app.cell
def _(con):
    # Check: Are there any products with invalid category_id?
    con.execute(
        f"""
        SELECT p.product_id, p.product_name, p.category_id
        FROM products p
        WHERE p.category_id NOT IN (SELECT category_id FROM categories)
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Exploring Relationships

    ### One-to-Many: Categories → Products
    One category has many products.
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.category_name, COUNT(*) AS product_count
                FROM categories c, products p
                WHERE c.category_id = p.category_id
                GROUP BY c.category_name
                ORDER BY product_count DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Identifying the "One" side and "Many" side

    - **Categories** is the "one" side (each category appears once)
    - **Products** is the "many" side (many products per category)
    - The FK (`category_id`) lives in the "many" side table
    """)
    return


@app.cell
def _(con):
    con.execute(
        f"""
        SELECT c.category_name, p.product_name, p.price
                FROM categories c, products p
                WHERE c.category_id = p.category_id
                  AND c.category_name = 'Electronics'
                ORDER BY p.price DESC
        """
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Schema Design with CREATE OR REPLACE TABLE
    Let's create tables with proper constraints.
    """)
    return


@app.cell
def _(duckdb):
    # Create a properly constrained schema
    con2 = duckdb.connect()

    con2.sql("""
        CREATE OR REPLACE TABLE categories (
            category_id   INTEGER PRIMARY KEY,
            category_name VARCHAR NOT NULL UNIQUE,
            description   VARCHAR
        )
    """)

    con2.sql("""
        CREATE OR REPLACE TABLE products (
            product_id     INTEGER PRIMARY KEY,
            product_name   VARCHAR NOT NULL,
            category_id    INTEGER REFERENCES categories(category_id),
            price          DECIMAL(10,2) CHECK (price > 0),
            stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0)
        )
    """)

    con2.sql("DESCRIBE categories").show()
    con2.sql("DESCRIBE products").show()
    print("Schema created with constraints!")
    return (con2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Testing Constraints
    """)
    return


@app.cell
def _(con2):
    # Insert valid data
    con2.sql("INSERT INTO categories VALUES (1, 'Electronics', 'Gadgets and devices')")
    con2.sql("INSERT INTO products VALUES (1, 'Laptop', 1, 999.99, 10)")
    print("Valid inserts succeeded!")

    # Try inserting a product with negative price
    try:
        con2.sql("INSERT INTO products VALUES (2, 'Bad Product', 1, -5.00, 10)")
        print("Inserted (unexpected!)")
    except Exception as e:
        print(f"Constraint violation (expected): {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Many-to-Many Relationships
    Products ↔ Suppliers requires a junction table.
    """)
    return


@app.cell
def _(duckdb):
    # Create a Many-to-Many example
    con3 = duckdb.connect()

    con3.sql("CREATE OR REPLACE TABLE suppliers (supplier_id INTEGER PRIMARY KEY, supplier_name VARCHAR)")
    con3.sql("CREATE OR REPLACE TABLE products_m2m (product_id INTEGER PRIMARY KEY, product_name VARCHAR)")
    con3.sql("""
        CREATE OR REPLACE TABLE product_suppliers (
            product_id  INTEGER REFERENCES products_m2m(product_id),
            supplier_id INTEGER REFERENCES suppliers(supplier_id),
            cost_price  DECIMAL(10,2),
            PRIMARY KEY (product_id, supplier_id)
        )
    """)

    # Insert sample data
    con3.sql("INSERT INTO suppliers VALUES (1,'TechWorld'), (2,'GlobalTech')")
    con3.sql("INSERT INTO products_m2m VALUES (1,'Laptop'), (2,'Phone')")
    con3.sql("INSERT INTO product_suppliers VALUES (1,1,500), (1,2,520), (2,1,300)")

    # Query the M:M relationship
    con3.sql("""
        SELECT p.product_name, s.supplier_name, ps.cost_price
        FROM products_m2m p, product_suppliers ps, suppliers s
        WHERE p.product_id = ps.product_id
          AND ps.supplier_id = s.supplier_id
        ORDER BY p.product_name, ps.cost_price
    """).show()
    print("Laptop has 2 suppliers, Phone has 1 supplier")
    return (con3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Design Exercise: Thinking Relationally

    Let's design tables for a new feature: customer reviews.
    """)
    return


@app.cell
def _():
    # What does a review need?
    # - Which product is being reviewed (FK to products)
    # - Which customer wrote it (FK to customers)
    # - Rating (1-5)
    # - Text of the review
    # - Date

    # This is a junction-like table (links customers and products)
    # but with extra attributes

    print("Reviews table design:")
    print("  review_id   INTEGER PRIMARY KEY")
    print("  product_id  INTEGER FK -> products")
    print("  customer_id INTEGER FK -> customers")
    print("  rating      INTEGER CHECK (1-5)")
    print("  review_text VARCHAR")
    print("  review_date DATE")
    print()
    print("Relationship: customers --(1:M)--> reviews <--(M:1)-- products")
    print("Effectively a M:M between customers and products, with attributes")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    Key concepts covered:
    - **Primary Key**: Uniquely identifies each row (e.g., `customer_id`)
    - **Foreign Key**: References another table's PK (e.g., `orders.customer_id`)
    - **Candidate Key**: Could serve as PK (e.g., `email`)
    - **Composite Key**: PK made of multiple columns (e.g., `(order_id, product_id)`)
    - **1:M relationship**: One category → many products (most common)
    - **M:M relationship**: Products ↔ Suppliers (needs junction table)
    - **Referential integrity**: FKs ensure valid references

    **Next week**: SQL JOINs — the proper way to combine tables!
    """)
    return


if __name__ == "__main__":
    app.run()
