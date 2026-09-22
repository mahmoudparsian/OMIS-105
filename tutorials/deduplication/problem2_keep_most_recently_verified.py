"""
Problem #2: 
   Write a DELETE query to remove duplicate 
   emails while keeping the MOST RECENTLY VERIFIED 
   entry for each email.

Approach (single set-based DELETE):
Rank each email's rows so that:
  1. 'verified' rows sort ahead of 'not-verified' rows, and
  2. within that, the most recent created_on sorts first.
ROW_NUMBER() assigns rn = 1 to the row we want to keep for 
each email - the latest verified row if one exists, otherwise 
(no verified row at all) the latest row overall. Every other 
row for that email is deleted.
"""

import duckdb

from db_setup import create_and_seed, print_table

DELETE_KEEP_MOST_RECENTLY_VERIFIED_SQL = """
DELETE FROM users
WHERE user_id NOT IN (
    SELECT user_id
    FROM (
        SELECT
            user_id,
            ROW_NUMBER() OVER (
                PARTITION BY email
                ORDER BY (status = 'verified') DESC, created_on DESC, user_id ASC
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

    con.execute(DELETE_KEEP_MOST_RECENTLY_VERIFIED_SQL)

    after_count = con.execute("SELECT COUNT(*) FROM users;").fetchone()[0]
    print(f"\nRows deleted: {before_count - after_count}")

    print_table(con, "AFTER (most recently verified row kept per email)")

    con.close()


if __name__ == "__main__":
    main()
