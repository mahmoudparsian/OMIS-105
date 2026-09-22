"""
Problem #1: 
     Write a DELETE query to remove duplicate emails 
     while keeping the OLDEST entry (smallest created_on) 
     for each email.

Approach (single set-based DELETE, no self-join / 
no row-by-row Python loop):
   Rank each email's rows with ROW_NUMBER() ordered 
   by created_on ascending (ties broken by user_id 
   for determinism), then delete every row whose rank
   is not 1. This is O(n log n) (one sort per email 
   partition) and lets DuckDB do the work in a single 
   query instead of iterating in Python.
"""

import duckdb

from db_setup import create_and_seed, print_table

DELETE_KEEP_OLDEST_SQL = """
DELETE FROM users
WHERE user_id NOT IN (
    SELECT user_id
    FROM (
        SELECT
            user_id,
            ROW_NUMBER() OVER (
                PARTITION BY email
                ORDER BY created_on ASC, user_id ASC
            ) AS rn
        FROM users
    ) ranked
    WHERE rn = 1
);
"""


def main() -> None:
    con = duckdb.connect("users.db")
    create_and_seed(con)  # fresh, known state each run

    print_table(con, "BEFORE (all rows)")
    before_count = con.execute("SELECT COUNT(*) FROM users;").fetchone()[0]

    con.execute(DELETE_KEEP_OLDEST_SQL)

    after_count = con.execute("SELECT COUNT(*) FROM users;").fetchone()[0]
    print(f"\nRows deleted: {before_count - after_count}")

    print_table(con, "AFTER (oldest row kept per email)")

    con.close()


if __name__ == "__main__":
    main()
