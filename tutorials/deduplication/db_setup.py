"""
Creates the `users` table in a DuckDB database 
and populates it with the sample data from the 
problem statement (MySQL / Spark SQL syntax 
translated to DuckDB).

Run directly to build a standalone users.db file 
(Step 1 of the assignment):

    python3 db_setup.py
"""

import duckdb

DB_FILE = "users.db"

CREATE_TABLE_SQL = """
CREATE TABLE users (
    user_id    INTEGER PRIMARY KEY,
    email      VARCHAR(100),
    status     VARCHAR(50),
    created_on TIMESTAMP
);
"""

INSERT_SQL = """
INSERT INTO users (user_id, email, status, created_on) VALUES
(1,  'john@yahoo.com',   'not-verified', '2026-01-01 02:00:00'),
(2,  'john@yahoo.com',   'verified',     '2026-01-02 03:00:00'),
(3,  'john@yahoo.com',   'verified',     '2026-01-02 04:00:00'),
(4,  'john@yahoo.com',   'not-verified', '2026-01-02 05:00:00'),
(5,  'rakesh@yahoo.com', 'not-verified', '2026-01-01 02:00:00'),
(6,  'rakesh@yahoo.com', 'verified',     '2026-01-01 03:00:00'),
(7,  'rakesh@yahoo.com', 'verified',     '2026-01-01 04:00:00'),
(8,  'rakesh@yahoo.com', 'not-verified', '2026-01-01 07:00:00'),
(9,  'rakesh@yahoo.com', 'not-verified', '2026-01-02 08:00:00'),
(10, 'steve@gmail.com',  'not-verified', '2026-01-01 01:00:00');
"""


def create_and_seed(con: duckdb.DuckDBPyConnection) -> None:
    """(Re)create the users table and load the sample rows."""
    con.execute("DROP TABLE IF EXISTS users;")
    con.execute(CREATE_TABLE_SQL)
    con.execute(INSERT_SQL)


def print_table(con: duckdb.DuckDBPyConnection, title: str) -> None:
    """Print the current contents of `users` as a labeled table."""
    df = con.execute("SELECT * FROM users ORDER BY email, created_on;").df()
    print(f"\n{title}")
    print("-" * len(title))
    print(df.to_string(index=False))


def main() -> None:
    con = duckdb.connect(DB_FILE)
    create_and_seed(con)
    print(f"Created and seeded 'users' table in {DB_FILE}")
    print(con.execute("SELECT * FROM users ORDER BY email, created_on;").df())
    con.close()


if __name__ == "__main__":
    main()
