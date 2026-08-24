#!/usr/bin/env python3
"""
build_bookstore_db.py
=====================
Reads CSV files from a data directory, loads them into a DuckDB database
called bookstore.duckdb, deduplicates all tables, and prints a summary.

Usage:
    python build_bookstore_db.py <data_directory>

Example:
    python build_bookstore_db.py data/
"""

import sys
import os
import duckdb


def main():
    if len(sys.argv) < 2:
        print("Usage: python build_bookstore_db.py <data_directory>")
        sys.exit(1)

    data_dir = sys.argv[1]
    if not os.path.isdir(data_dir):
        print(f"Error: '{data_dir}' is not a valid directory.")
        sys.exit(1)

    db_path = os.path.join(os.path.dirname(os.path.abspath(data_dir)), "bookstore.duckdb")

    # Remove existing database so we start fresh
    if os.path.exists(db_path):
        os.remove(db_path)

    con = duckdb.connect(db_path)

    # ── Table definitions ────────────────────────────────────────────
    tables = {
        "books": {
            "file": os.path.join(data_dir, "books.csv"),
            "ddl": """
                CREATE TABLE books (
                    book_id        INTEGER,
                    title          VARCHAR,
                    author         VARCHAR,
                    genre          VARCHAR,
                    published_year INTEGER,
                    price          DOUBLE,
                    stock          INTEGER
                )
            """,
        },
        "customers": {
            "file": os.path.join(data_dir, "customers.csv"),
            "ddl": """
                CREATE TABLE customers (
                    customer_id INTEGER,
                    name        VARCHAR,
                    email       VARCHAR,
                    phone       VARCHAR,
                    city        VARCHAR,
                    country     VARCHAR
                )
            """,
        },
        "orders": {
            "file": os.path.join(data_dir, "orders.csv"),
            "ddl": """
                CREATE TABLE orders (
                    order_id     INTEGER,
                    customer_id  INTEGER,
                    book_id      INTEGER,
                    order_date   DATE,
                    quantity     INTEGER,
                    total_amount DOUBLE
                )
            """,
        },
    }

    print("=" * 60)
    print("  Building bookstore.duckdb")
    print("=" * 60)

    for name, spec in tables.items():
        csv_path = spec["file"]
        if not os.path.exists(csv_path):
            print(f"  WARNING: {csv_path} not found, skipping {name}.")
            continue

        # Create table
        con.execute(spec["ddl"])

        # Load CSV into table (with duplicates)
        con.execute(f"""
            INSERT INTO {name}
            SELECT * FROM read_csv_auto('{csv_path}', header=true)
        """)
        raw_count = con.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]

        # Deduplicate: keep one copy of each distinct row
        con.execute(f"""
            CREATE OR REPLACE TABLE {name} AS
            SELECT DISTINCT * FROM {name}
        """)
        dedup_count = con.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        removed = raw_count - dedup_count

        print(f"\n  Table: {name}")
        print(f"    Rows loaded from CSV : {raw_count:>7,}")
        print(f"    Duplicates removed   : {removed:>7,}")
        print(f"    Final row count      : {dedup_count:>7,}")

    # ── Summary ──────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  Final Database Summary")
    print("=" * 60)
    for name in tables:
        count = con.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        print(f"    {name:<12s} : {count:>7,} records")
    print("=" * 60)
    print(f"\n  Database saved to: {db_path}")

    con.close()


if __name__ == "__main__":
    main()
