#!/usr/bin/env python3
"""
Python + DuckDB Integration Demo (IN-MEMORY)
==============================================
Course : OMIS 105 — Database Management Systems
Author : Dr. Mahmoud Parsian
Topic  : Python-DuckDB CRUD with an IN-MEMORY database

This program demonstrates:
  1. Creating an in-memory DuckDB database (no file on disk)
  2. Creating a sales table
  3. Inserting records one-by-one (4 records)
  4. Inserting records in bulk (4 records)
  5. Updating columns (2 updates with before/after)
  6. Deleting records (2 deletes with before/after)

Every operation shows BEFORE and AFTER snapshots.

Key difference from the persistent version:
  - duckdb.connect(database=':memory:')  ← IN-MEMORY (this script)
  - duckdb.connect(database='file.duckdb') ← PERSISTENT (other script)

  The in-memory database lives ONLY while the script is running.
  Once the script ends, all data is gone. No file is created.

Usage:
    python python_duckdb_crud_in_memory.py
"""

import duckdb

# ════════════════════════════════════════════════════════════════
#  Helper functions for clean output
# ════════════════════════════════════════════════════════════════

def banner(title: str) -> None:
    """Print a section banner."""
    width = 62
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)

def show(con: duckdb.DuckDBPyConnection, title: str) -> None:
    """Run SELECT * and display as a formatted table."""
    df = con.execute("SELECT * FROM sales ORDER BY sale_id").fetchdf()
    print(f"\n  [{title}]  ({len(df)} rows)")
    if df.empty:
        print("  (no rows)")
    else:
        print(df.to_string(index=False))
    print()

def show_sql(sql: str) -> None:
    """Pretty-print the SQL being executed."""
    lines = sql.strip().split("\n")
    print("  SQL:")
    for line in lines:
        print(f"    {line.strip()}")

# ════════════════════════════════════════════════════════════════
#  MAIN PROGRAM
# ════════════════════════════════════════════════════════════════

def main():
    # ── In-memory database ────────────────────────────────────
    # ':memory:' means no file is created on disk.
    # The database exists ONLY while this script is running.
    con = duckdb.connect(database=':memory:')
    print("Connected to IN-MEMORY DuckDB database")
    print("(No file on disk — data lives only during this run)")

    # ══════════════════════════════════════════════════════════
    # STEP 1: CREATE TABLE
    # ══════════════════════════════════════════════════════════
    banner("STEP 1: CREATE TABLE sales")

    sql = """
    CREATE TABLE sales (
        sale_id    INTEGER PRIMARY KEY,
        customer   VARCHAR NOT NULL,
        product    VARCHAR NOT NULL,
        price      DECIMAL(10, 2) NOT NULL,
        sale_date  DATE NOT NULL
    )
    """
    show_sql(sql)
    con.execute("""
        CREATE TABLE sales (
            sale_id    INTEGER PRIMARY KEY,
            customer   VARCHAR NOT NULL,
            product    VARCHAR NOT NULL,
            price      DECIMAL(10, 2) NOT NULL,
            sale_date  DATE NOT NULL
        )
    """)
    print("\n  Table 'sales' created successfully (in memory).")
    show(con, "Table after creation (empty)")

    # ══════════════════════════════════════════════════════════
    # STEP 2: INSERT records ONE-BY-ONE (4 records)
    # ══════════════════════════════════════════════════════════
    banner("STEP 2: INSERT 4 records ONE-BY-ONE")

    one_by_one = [
        (1, 'Alice',  'Laptop',     999.99, '2025-01-15'),
        (2, 'Bob',    'Mouse',       29.99, '2025-01-16'),
        (3, 'Carol',  'Keyboard',    79.99, '2025-02-01'),
        (4, 'David',  'Monitor',    349.99, '2025-02-10'),
    ]

    for record in one_by_one:
        sql_text = (
            f"INSERT INTO sales VALUES "
            f"({record[0]}, '{record[1]}', '{record[2]}', "
            f"{record[3]}, '{record[4]}')"
        )
        show_sql(sql_text)
        con.execute(
            "INSERT INTO sales VALUES (?, ?, ?, ?, ?)",
            record
        )
        print(f"    -> Inserted: sale_id={record[0]}, "
              f"customer='{record[1]}', product='{record[2]}'")

    show(con, "AFTER inserting 4 records one-by-one")

    # ══════════════════════════════════════════════════════════
    # STEP 3: INSERT records IN BULK (4 records)
    # ══════════════════════════════════════════════════════════
    banner("STEP 3: INSERT 4 records IN BULK")

    show(con, "BEFORE bulk insert")

    bulk_records = [
        (5, 'Eva',    'Headphones',  149.99, '2025-03-05'),
        (6, 'Frank',  'Webcam',       89.99, '2025-03-12'),
        (7, 'Grace',  'USB Hub',      39.99, '2025-04-01'),
        (8, 'Henry',  'SSD Drive',   119.99, '2025-04-15'),
    ]

    sql_bulk = """
    INSERT INTO sales VALUES
        (5, 'Eva',   'Headphones', 149.99, '2025-03-05'),
        (6, 'Frank', 'Webcam',      89.99, '2025-03-12'),
        (7, 'Grace', 'USB Hub',     39.99, '2025-04-01'),
        (8, 'Henry', 'SSD Drive',  119.99, '2025-04-15')
    """
    show_sql(sql_bulk)

    con.executemany(
        "INSERT INTO sales VALUES (?, ?, ?, ?, ?)",
        bulk_records
    )
    print("    -> 4 records inserted in bulk via executemany()")

    show(con, "AFTER bulk insert (8 records total)")

    # ══════════════════════════════════════════════════════════
    # STEP 4: UPDATE — change the price of sale_id=2
    # ══════════════════════════════════════════════════════════
    banner("STEP 4: UPDATE price of sale_id=2 (Bob's Mouse)")

    show(con, "BEFORE update")

    sql_update1 = """
    UPDATE sales
    SET    price = 24.99
    WHERE  sale_id = 2
    """
    show_sql(sql_update1)
    con.execute("""
        UPDATE sales
        SET    price = 24.99
        WHERE  sale_id = 2
    """)
    print("    -> Bob's Mouse price changed: $29.99 -> $24.99")

    show(con, "AFTER update (sale_id=2 price changed)")

    # ══════════════════════════════════════════════════════════
    # STEP 5: UPDATE — change the product of sale_id=7
    # ══════════════════════════════════════════════════════════
    banner("STEP 5: UPDATE product of sale_id=7 (Grace)")

    show(con, "BEFORE update")

    sql_update2 = """
    UPDATE sales
    SET    product = 'Docking Station'
    WHERE  sale_id = 7
    """
    show_sql(sql_update2)
    con.execute("""
        UPDATE sales
        SET    product = 'Docking Station'
        WHERE  sale_id = 7
    """)
    print("    -> Grace's product changed: 'USB Hub' -> 'Docking Station'")

    show(con, "AFTER update (sale_id=7 product changed)")

    # ══════════════════════════════════════════════════════════
    # STEP 6: DELETE — remove sale_id=4
    # ══════════════════════════════════════════════════════════
    banner("STEP 6: DELETE sale_id=4 (David's Monitor)")

    show(con, "BEFORE delete")

    sql_delete1 = """
    DELETE FROM sales
    WHERE  sale_id = 4
    """
    show_sql(sql_delete1)
    con.execute("""
        DELETE FROM sales
        WHERE  sale_id = 4
    """)
    print("    -> sale_id=4 (David, Monitor) deleted")

    show(con, "AFTER delete (sale_id=4 removed, 7 rows remain)")

    # ══════════════════════════════════════════════════════════
    # STEP 7: DELETE — remove sale_id=6
    # ══════════════════════════════════════════════════════════
    banner("STEP 7: DELETE sale_id=6 (Frank's Webcam)")

    show(con, "BEFORE delete")

    sql_delete2 = """
    DELETE FROM sales
    WHERE  sale_id = 6
    """
    show_sql(sql_delete2)
    con.execute("""
        DELETE FROM sales
        WHERE  sale_id = 6
    """)
    print("    -> sale_id=6 (Frank, Webcam) deleted")

    show(con, "AFTER delete (sale_id=6 removed, 6 rows remain)")

    # ══════════════════════════════════════════════════════════
    # FINAL STATE
    # ══════════════════════════════════════════════════════════
    banner("FINAL STATE OF THE sales TABLE")
    show(con, "Final sales table")

    print("  This is an IN-MEMORY database — no file on disk.")
    print("  When this script ends, all data is gone.")
    print()
    print("  To make data persistent instead, change the connection to:")
    print("    con = duckdb.connect(database='sales_demo.duckdb')")
    print()

    # ── Close connection ─────────────────────────────────────
    con.close()
    print("  Connection closed. In-memory database released. Done!")
    print()


if __name__ == "__main__":
    main()
