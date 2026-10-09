import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import duckdb

    con = duckdb.connect(database=":memory:")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 9 — Capstone Project: A Worked Example

    This notebook shows a **finished** small project (a library database),
    one section for each deliverable in `lab09_student.md`.
    Run it to see what each section should look like.

    **Your starting template is `lab09_student_marimo.py`.** Use this notebook
    only as a model. Your project must be your own original design —
    not this library example, and not a copy of ShopSmart.
    (This example also has fewer than 20 rows per table, to keep it short;
    your project needs at least 20.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Requirements

    Answer each question in one or two sentences.

    1. **Purpose:** What is this database for?
       _Example: Track the books a small library owns and who borrows them._
    2. **Users:** Who will use it, and what will they do?
       _Example: Librarians record loans and returns; managers run reports._
    3. **Data:** What do we need to store?
       _Example: Authors, books, members, and loans._
    4. **Questions:** What should the database answer?
       _Example: Which books are overdue? Who are the most active members?_
    5. **Business rules:** What rules must always hold?
       _Example: A loan's due date is after its loan date; a member's email is unique._
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: ER Diagram (15%)

    Draw your diagram with a tool (e.g., draw.io) and insert the image here:
    `mo.image("er_diagram.png")` — or describe it in text like the example below.

    ```
    authors ──(1:M)──▶ book_authors ◀──(M:1)── books      (M:M via book_authors)
    members ──(1:M)──▶ loans ◀──(M:1)── books
    ```

    - **Entities:** authors, books, members, loans
    - **Junction table:** book_authors (a book can have many authors,
      and an author can write many books)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Normalized Schema — CREATE TABLE (15%)

    - Every table has a `PRIMARY KEY`
    - Use `FOREIGN KEY` (`REFERENCES`), `NOT NULL`, `CHECK`, `UNIQUE`, and `DEFAULT` where they fit
    - Create **parent** tables before **child** tables

    The `DROP TABLE` lines (children first) let you re-run this cell safely.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        -- Drop child tables first, then parents (so the cell can be re-run)
        DROP TABLE IF EXISTS loans;
        DROP TABLE IF EXISTS book_authors;
        DROP TABLE IF EXISTS books;
        DROP TABLE IF EXISTS authors;
        DROP TABLE IF EXISTS members;

        CREATE TABLE authors (
            author_id   INTEGER PRIMARY KEY,
            full_name   VARCHAR NOT NULL,
            country     VARCHAR
        );

        CREATE TABLE books (
            book_id     INTEGER PRIMARY KEY,
            title       VARCHAR NOT NULL,
            genre       VARCHAR NOT NULL,
            year        INTEGER CHECK (year BETWEEN 1450 AND 2100),
            copies      INTEGER NOT NULL DEFAULT 1 CHECK (copies >= 0)
        );

        CREATE TABLE book_authors (           -- junction table (M:M)
            book_id     INTEGER NOT NULL REFERENCES books(book_id),
            author_id   INTEGER NOT NULL REFERENCES authors(author_id),
            PRIMARY KEY (book_id, author_id)
        );

        CREATE TABLE members (
            member_id   INTEGER PRIMARY KEY,
            full_name   VARCHAR NOT NULL,
            email       VARCHAR NOT NULL UNIQUE,
            join_date   DATE NOT NULL DEFAULT CURRENT_DATE,
            status      VARCHAR NOT NULL DEFAULT 'active'
                        CHECK (status IN ('active', 'suspended'))
        );

        CREATE TABLE loans (
            loan_id     INTEGER PRIMARY KEY,
            book_id     INTEGER NOT NULL REFERENCES books(book_id),
            member_id   INTEGER NOT NULL REFERENCES members(member_id),
            loan_date   DATE NOT NULL,
            due_date    DATE NOT NULL,
            return_date DATE,                 -- NULL = not returned yet
            CHECK (due_date > loan_date)
        );
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Normalization Check

    For each table, explain in one line why it is in **3NF**.

    - **1NF:** Every column holds one value. _Example: authors are in their own
      table, not a comma-separated list inside `books`._
    - **2NF:** No column depends on only part of a composite key.
      _Example: `book_authors` has only its two key columns._
    - **3NF:** No column depends on another non-key column.
      _Example: the author's country is stored in `authors`, not in `books`._

    If you denormalized anything on purpose, say what and why.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5: Sample Data (10%)

    - At least **20 rows** in each main table (the example has fewer, to keep it short)
    - Realistic values — not "test1", "test2"
    - Include edge cases: a member with no loans, a book not returned yet (`NULL`)

    To load a CSV file instead, insert into the table you created, so the
    constraints are checked:
    `INSERT INTO members SELECT * FROM read_csv('data/members.csv');`
    """)
    return


@app.cell
def _(con):
    con.execute("""
        INSERT INTO authors VALUES
            (1, 'Toni Morrison',    'USA'),
            (2, 'Gabriel García Márquez', 'Colombia'),
            (3, 'Chinua Achebe',    'Nigeria'),
            (4, 'Terry Pratchett',  'UK'),
            (5, 'Neil Gaiman',      'UK');

        INSERT INTO books VALUES
            (1, 'Beloved',                     'Fiction', 1987, 3),
            (2, 'One Hundred Years of Solitude','Fiction', 1967, 2),
            (3, 'Things Fall Apart',           'Fiction', 1958, 2),
            (4, 'Good Omens',                  'Fantasy', 1990, 4),
            (5, 'Song of Solomon',             'Fiction', 1977, 1);

        INSERT INTO book_authors VALUES
            (1, 1), (2, 2), (3, 3), (4, 4), (4, 5), (5, 1);

        INSERT INTO members VALUES
            (1, 'Maria Lopez', 'maria@email.com', DATE '2025-01-10', 'active'),
            (2, 'Kenji Sato',  'kenji@email.com', DATE '2025-03-22', 'active'),
            (3, 'Amina Bello', 'amina@email.com', DATE '2025-06-05', 'active'),
            (4, 'David Chen',  'david@email.com', DATE '2025-09-14', 'suspended');

        INSERT INTO loans VALUES
            (1, 1, 1, DATE '2026-09-01', DATE '2026-09-15', DATE '2026-09-12'),
            (2, 4, 1, DATE '2026-09-20', DATE '2026-10-04', NULL),
            (3, 2, 2, DATE '2026-09-25', DATE '2026-10-09', NULL),
            (4, 4, 2, DATE '2026-08-01', DATE '2026-08-15', DATE '2026-08-20'),
            (5, 3, 4, DATE '2026-07-10', DATE '2026-07-24', DATE '2026-07-23');
    """)
    return


@app.cell
def _(con):
    con.execute("""
        -- Row counts: check that every table has data
        SELECT 'authors' AS table_name, COUNT(*) AS row_count FROM authors
        UNION ALL SELECT 'books',        COUNT(*) FROM books
        UNION ALL SELECT 'book_authors', COUNT(*) FROM book_authors
        UNION ALL SELECT 'members',      COUNT(*) FROM members
        UNION ALL SELECT 'loans',        COUNT(*) FROM loans;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6: Ten SQL Queries (25%)

    | Category | How many |
    |----------|----------|
    | Basic SELECT (WHERE, ORDER BY) | 2 — Q1, Q2 |
    | JOINs (INNER, LEFT, 3+ tables) | 3 — Q3, Q4, Q5 |
    | GROUP BY with HAVING or CASE | 2 — Q6, Q7 |
    | Window functions or CTEs | 2 — Q8, Q9 |
    | Transaction (Python) | 1 — Q10, in Step 9 |

    Each query needs a `-- Business purpose:` comment. Running the cell shows the output.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        -- Q1 (Basic SELECT)
        -- Business purpose: list fiction books, newest first
        SELECT title, year
        FROM books
        WHERE genre = 'Fiction'
        ORDER BY year DESC;
    """).fetchdf()
    return


@app.cell
def _(con):
    con.execute("""
        -- Q2 (Basic SELECT)
        -- Business purpose: books with only one copy (candidates to buy more)
        SELECT title, copies
        FROM books
        WHERE copies = 1
        ORDER BY title;
    """).fetchdf()
    return


@app.cell
def _(con):
    con.execute("""
        -- Q3 (INNER JOIN, 3 tables)
        -- Business purpose: each book with its author(s)
        SELECT b.title, a.full_name AS author
        FROM books b
        JOIN book_authors ba ON b.book_id = ba.book_id
        JOIN authors a       ON ba.author_id = a.author_id
        ORDER BY b.title, author;
    """).fetchdf()
    return


@app.cell
def _(con):
    con.execute("""
        -- Q4 (LEFT JOIN + IS NULL)
        -- Business purpose: members who have never borrowed a book
        SELECT m.full_name
        FROM members m
        LEFT JOIN loans l ON m.member_id = l.member_id
        WHERE l.loan_id IS NULL;
    """).fetchdf()
    return


@app.cell
def _(con):
    con.execute("""
        -- Q5 (JOIN, 3 tables)
        -- Business purpose: books that are overdue today (due, but not returned)
        SELECT m.full_name, b.title, l.due_date
        FROM loans l
        JOIN members m ON l.member_id = m.member_id
        JOIN books b   ON l.book_id = b.book_id
        WHERE l.return_date IS NULL
          AND l.due_date < CURRENT_DATE
        ORDER BY l.due_date;
    """).fetchdf()
    return


@app.cell
def _(con):
    con.execute("""
        -- Q6 (GROUP BY + HAVING)
        -- Business purpose: books borrowed more than once
        SELECT b.title, COUNT(*) AS times_borrowed
        FROM loans l
        JOIN books b ON l.book_id = b.book_id
        GROUP BY b.book_id, b.title
        HAVING COUNT(*) > 1;
    """).fetchdf()
    return


@app.cell
def _(con):
    con.execute("""
        -- Q7 (GROUP BY + CASE)
        -- Business purpose: count loans returned on time, late, or still out
        SELECT CASE
                   WHEN return_date IS NULL      THEN 'still out'
                   WHEN return_date <= due_date  THEN 'on time'
                   ELSE 'late'
               END AS loan_status,
               COUNT(*) AS loans
        FROM loans
        GROUP BY loan_status
        ORDER BY loans DESC;
    """).fetchdf()
    return


@app.cell
def _(con):
    con.execute("""
        -- Q8 (CTE)
        -- Business purpose: members with more loans than the average member
        WITH member_loans AS (
            SELECT m.member_id, m.full_name, COUNT(l.loan_id) AS loans
            FROM members m
            LEFT JOIN loans l ON m.member_id = l.member_id
            GROUP BY m.member_id, m.full_name
        )
        SELECT full_name, loans
        FROM member_loans
        WHERE loans > (SELECT AVG(loans) FROM member_loans)
        ORDER BY loans DESC;
    """).fetchdf()
    return


@app.cell
def _(con):
    con.execute("""
        -- Q9 (Window function)
        -- Business purpose: number each member's loans in date order
        SELECT m.full_name, b.title, l.loan_date,
               ROW_NUMBER() OVER (PARTITION BY l.member_id
                                  ORDER BY l.loan_date) AS loan_number
        FROM loans l
        JOIN members m ON l.member_id = m.member_id
        JOIN books b   ON l.book_id = b.book_id
        ORDER BY m.full_name, loan_number;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 7: Views (2+) — part of 10%

    For each view, write one line: **who** uses it and **why**.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        -- View 1: Member activity (used by librarians at the front desk)
        CREATE OR REPLACE VIEW member_activity AS
        SELECT m.member_id, m.full_name, m.status,
               COUNT(l.loan_id) AS total_loans,
               COUNT(l.loan_id) - COUNT(l.return_date) AS books_out
        FROM members m
        LEFT JOIN loans l ON m.member_id = l.member_id
        GROUP BY m.member_id, m.full_name, m.status;

        -- View 2: Book availability (used by members searching the catalog)
        CREATE OR REPLACE VIEW book_availability AS
        SELECT b.book_id, b.title, b.copies,
               b.copies - COUNT(l.loan_id) AS available
        FROM books b
        LEFT JOIN loans l ON b.book_id = l.book_id AND l.return_date IS NULL
        GROUP BY b.book_id, b.title, b.copies;
    """)
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM book_availability ORDER BY title;").fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 8: Indexes (3+) — part of 10%

    For each index, say **which query it helps** (Week 7):
    - Good: columns used to look up **a few rows** (one member, one book)
    - Not useful: columns with few different values (like `status`)
    - `PRIMARY KEY` and `UNIQUE` columns already have an index
    """)
    return


@app.cell
def _(con):
    con.execute("""
        -- Helps: "show the loans of one member" (Q9, member_activity)
        CREATE INDEX IF NOT EXISTS idx_loans_member ON loans(member_id);

        -- Helps: "who has this book?" lookups for one book
        CREATE INDEX IF NOT EXISTS idx_loans_book ON loans(book_id);

        -- Helps: "find a book by its title" at the front desk
        CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
    """)
    con.execute(
        "SELECT index_name, table_name, sql FROM duckdb_indexes();"
    ).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 9: Transaction Demo — Q10 (10%)

    Requirements:
    - A **multi-step** operation (3+ SQL statements)
    - **Error handling:** `try` / `except` with `ROLLBACK`
    - Show **both** a success case and a failure case

    Example: lend a book. Check that the member is active, check that a copy is
    available (using the `book_availability` view), then record the loan —
    all or nothing. `copies` is the number the library owns, so it does not
    change; availability is always computed from the open loans.
    """)
    return


@app.cell
def _(con):
    def lend_book(con, loan_id, book_id, member_id):
        """Lend a book: 3 SQL statements that succeed or fail together."""
        try:
            con.execute("BEGIN")
            _status = con.execute(
                "SELECT status FROM members WHERE member_id = ?", [member_id]
            ).fetchone()
            if _status is None or _status[0] != "active":
                raise ValueError("member is not active")
            _available = con.execute(
                "SELECT available FROM book_availability WHERE book_id = ?",
                [book_id],
            ).fetchone()
            if _available is None or _available[0] < 1:
                raise ValueError("no copies available")
            con.execute(
                "INSERT INTO loans VALUES (?, ?, ?, CURRENT_DATE, CURRENT_DATE + 14, NULL)",
                [loan_id, book_id, member_id],
            )
            con.execute("COMMIT")
            return f"Loan {loan_id}: success"
        except Exception as e:
            con.execute("ROLLBACK")
            return f"Loan {loan_id}: rolled back ({e})"

    return (lend_book,)


@app.cell
def _(con, lend_book, mo):
    _results = [
        lend_book(con, 6, 3, 3),   # success: Amina is active, a copy is available
        lend_book(con, 7, 1, 4),   # failure: David is suspended
        lend_book(con, 8, 5, 3),   # success: takes the last copy of Song of Solomon
        lend_book(con, 9, 5, 2),   # failure: no copies left
    ]
    mo.md("\n".join(f"- {r}" for r in _results))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 10: Reflection

    Answer in a few sentences (you will also say this in your presentation):

    1. What was the hardest part of your design?
    2. Which query gives the most useful business insight, and why?
    3. What would you add or change with more time?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
