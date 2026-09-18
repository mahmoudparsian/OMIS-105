"""
Shared sample dataset for the "Introduction to RDBMS with DuckDB" course.

This is a plain Python module (NOT a marimo notebook). The notebooks import
it so that every notebook works with the *exact same* small e-commerce
database, without re-typing the data-generation code twelve times.

Schema (5 tables):

    customers(customer_id PK, first_name, last_name, email, city, state, signup_date)
    employees(employee_id PK, first_name, last_name, title, manager_id FK -> employees.employee_id)
    products(product_id PK, product_name, category, unit_price, in_stock)
    orders(order_id PK, customer_id FK -> customers, employee_id FK -> employees,
           order_date, ship_city)
    order_items(order_id FK -> orders, product_id FK -> products, quantity,
                unit_price, PRIMARY KEY(order_id, product_id))

Everything is generated with a fixed random seed, so rebuilding the database
always produces identical data.

The persistent, on-disk `ecommerce_database.duckdb` file is a *build
artifact*: run `./create_database.sh` once (see that script, and notebook
03) to create it, then every notebook connects to it directly with the
plain DuckDB API:

    con = duckdb.connect("ecommerce_database.duckdb", read_only=True)

(08 and 10 open it without `read_only=True`, since they deliberately
`INSERT`/`UPDATE`/`DELETE`/run transactions as teaching demos — 10 cleans
up after itself so the shared file always ends up back in its original
state.) It is not checked into the repo, and this module has no wrapper
around that call on purpose — it's the same `duckdb.connect(...)` pattern
notebook 01 already taught, just pointed at a file instead of `:memory:`.
"""

from __future__ import annotations

import os
import random
from datetime import date, timedelta

import pandas as pd

SEED = 42

DB_FILENAME = "ecommerce_database.duckdb"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_FILENAME)


def customers_df() -> pd.DataFrame:
    rng = random.Random(SEED)
    first_names = [
        "Ava", "Liam", "Maya", "Noah", "Zoe", "Ethan", "Mia", "Lucas",
        "Ivy", "Owen", "Nora", "Leo", "Ruby", "Kai", "Elena", "Marcus",
        "Priya", "Diego", "Hana", "Omar", "Sofia", "Jamal", "Chloe", "Theo",
        "Amara", "Felix", "Layla", "Victor", "Nina", "Isaac",
    ]
    last_names = [
        "Garcia", "Smith", "Chen", "Patel", "Nguyen", "Johnson", "Kim",
        "Rossi", "Muller", "Silva", "Khan", "Brown", "Diaz", "Okafor",
        "Novak",
    ]
    cities_states = [
        ("San Jose", "CA"), ("Santa Clara", "CA"), ("Austin", "TX"),
        ("Seattle", "WA"), ("Denver", "CO"), ("Chicago", "IL"),
        ("Boston", "MA"), ("Miami", "FL"), ("Portland", "OR"),
        ("Atlanta", "GA"),
    ]

    rows = []
    start = date(2023, 1, 1)
    for i in range(1, 31):
        fn = rng.choice(first_names)
        ln = rng.choice(last_names)
        city, state = rng.choice(cities_states)
        signup = start + timedelta(days=rng.randint(0, 640))
        rows.append(
            {
                "customer_id": i,
                "first_name": fn,
                "last_name": ln,
                "email": f"{fn.lower()}.{ln.lower()}{i}@example.com",
                "city": city,
                "state": state,
                "signup_date": signup,
            }
        )
    return pd.DataFrame(rows)


def employees_df() -> pd.DataFrame:
    # A small reporting hierarchy: employee 1 (VP Sales) has no manager;
    # everyone else reports to someone with a smaller employee_id.
    # This is deliberately used later to teach self-joins.
    data = [
        (1, "Priya", "Anand", "VP of Sales", None),
        (2, "Marcus", "Lee", "Sales Manager", 1),
        (3, "Elena", "Kowalski", "Sales Manager", 1),
        (4, "Owen", "Baptiste", "Sales Rep", 2),
        (5, "Nora", "Alvarez", "Sales Rep", 2),
        (6, "Kai", "Yoshida", "Sales Rep", 3),
    ]
    return pd.DataFrame(
        data,
        columns=["employee_id", "first_name", "last_name", "title", "manager_id"],
    )


def products_df() -> pd.DataFrame:
    data = [
        (1, "Wireless Mouse", "Electronics", 24.99, True),
        (2, "Mechanical Keyboard", "Electronics", 89.99, True),
        (3, "USB-C Hub", "Electronics", 34.50, True),
        (4, "27in Monitor", "Electronics", 249.00, True),
        (5, "Laptop Stand", "Office", 39.95, True),
        (6, "Standing Desk", "Office", 399.00, False),
        (7, "Desk Lamp", "Office", 22.00, True),
        (8, "Notebook (3-pack)", "Stationery", 8.99, True),
        (9, "Gel Pens (12-pack)", "Stationery", 6.49, True),
        (10, "Whiteboard", "Office", 54.00, True),
        (11, "Webcam 1080p", "Electronics", 45.00, True),
        (12, "Noise-Cancelling Headphones", "Electronics", 179.00, True),
        (13, "Ergonomic Chair Cushion", "Office", 29.99, True),
        (14, "Sticky Notes (6-pack)", "Stationery", 4.25, True),
        (15, "Portable SSD 1TB", "Electronics", 109.00, True),
    ]
    return pd.DataFrame(
        data,
        columns=["product_id", "product_name", "category", "unit_price", "in_stock"],
    )


def orders_df(
    customers: pd.DataFrame | None = None,
    employees: pd.DataFrame | None = None,
) -> pd.DataFrame:
    customers = customers_df() if customers is None else customers
    employees = employees_df() if employees is None else employees

    rng = random.Random(SEED + 1)
    sales_reps = employees[employees["title"] == "Sales Rep"]["employee_id"].tolist()
    start = date(2023, 2, 1)

    rows = []
    for order_id in range(1, 81):
        cust = customers.sample(random_state=rng.randint(0, 10_000)).iloc[0]
        order_date = start + timedelta(days=rng.randint(0, 580))
        rows.append(
            {
                "order_id": order_id,
                "customer_id": int(cust["customer_id"]),
                "employee_id": rng.choice(sales_reps),
                "order_date": order_date,
                "ship_city": cust["city"],
            }
        )
    return pd.DataFrame(rows)


def order_items_df(
    orders: pd.DataFrame | None = None,
    products: pd.DataFrame | None = None,
) -> pd.DataFrame:
    orders = orders_df() if orders is None else orders
    products = products_df() if products is None else products

    rng = random.Random(SEED + 2)
    rows = []
    for order_id in orders["order_id"]:
        n_items = rng.randint(1, 4)
        chosen = products.sample(n=n_items, random_state=rng.randint(0, 10_000))
        for _, prod in chosen.iterrows():
            rows.append(
                {
                    "order_id": int(order_id),
                    "product_id": int(prod["product_id"]),
                    "quantity": rng.randint(1, 5),
                    "unit_price": float(prod["unit_price"]),
                }
            )
    df = pd.DataFrame(rows)
    # Guard against the rare case where sampling produced a duplicate
    # (order_id, product_id) pair, which would violate the composite
    # primary key we define on this table.
    df = df.drop_duplicates(subset=["order_id", "product_id"]).reset_index(drop=True)
    return df


DDL = """
CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    first_name    VARCHAR NOT NULL,
    last_name     VARCHAR NOT NULL,
    email         VARCHAR UNIQUE NOT NULL,
    city          VARCHAR,
    state         VARCHAR,
    signup_date   DATE NOT NULL
);

CREATE TABLE employees (
    employee_id   INTEGER PRIMARY KEY,
    first_name    VARCHAR NOT NULL,
    last_name     VARCHAR NOT NULL,
    title         VARCHAR NOT NULL,
    manager_id    INTEGER REFERENCES employees(employee_id)
);

CREATE TABLE products (
    product_id    INTEGER PRIMARY KEY,
    product_name  VARCHAR NOT NULL,
    category      VARCHAR NOT NULL,
    unit_price    DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
    in_stock      BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE orders (
    order_id      INTEGER PRIMARY KEY,
    customer_id   INTEGER NOT NULL REFERENCES customers(customer_id),
    employee_id   INTEGER NOT NULL REFERENCES employees(employee_id),
    order_date    DATE NOT NULL,
    ship_city     VARCHAR
);

CREATE TABLE order_items (
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    product_id    INTEGER NOT NULL REFERENCES products(product_id),
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
    PRIMARY KEY (order_id, product_id)
);
"""


def create_schema(con) -> None:
    """Create the five tables (with keys/constraints) on an open DuckDB connection."""
    con.execute(DDL)


def load_data(con) -> None:
    """Create the schema (if needed) and populate it with the generated sample data."""
    existing = con.execute(
        "SELECT count(*) FROM information_schema.tables WHERE table_name = 'customers'"
    ).fetchone()[0]
    if existing == 0:
        create_schema(con)

    customers = customers_df()
    employees = employees_df()
    products = products_df()
    orders = orders_df(customers, employees)
    order_items = order_items_df(orders, products)

    con.register("_customers_df", customers)
    con.register("_employees_df", employees)
    con.register("_products_df", products)
    con.register("_orders_df", orders)
    con.register("_order_items_df", order_items)

    con.execute("INSERT INTO customers SELECT * FROM _customers_df")
    # employees.manager_id is a *self-referencing* foreign key. A single
    # bulk INSERT ... SELECT checks all rows against the pre-statement
    # table state, so a manager row and the rows that reference it can't
    # be inserted together. Insert one row at a time instead, in
    # employee_id order, so each manager already exists before anyone
    # who reports to them is inserted.
    for row in employees.itertuples(index=False):
        manager_id = None if pd.isna(row.manager_id) else int(row.manager_id)
        con.execute(
            "INSERT INTO employees VALUES (?, ?, ?, ?, ?)",
            [row.employee_id, row.first_name, row.last_name, row.title, manager_id],
        )
    con.execute("INSERT INTO products SELECT * FROM _products_df")
    con.execute("INSERT INTO orders SELECT * FROM _orders_df")
    con.execute("INSERT INTO order_items SELECT * FROM _order_items_df")


def build_database(path: str = DB_PATH, overwrite: bool = True) -> None:
    """Build the persistent, on-disk course database at `path`.

    This is what `create_database.sh` calls. Notebooks should not call
    this directly — they connect to the already-built file with the
    plain DuckDB API instead: `duckdb.connect("ecommerce_database.duckdb", read_only=True)`.
    """
    if overwrite and os.path.exists(path):
        os.remove(path)

    import duckdb

    con = duckdb.connect(path)
    try:
        load_data(con)
    finally:
        con.close()
