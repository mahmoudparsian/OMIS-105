"""
seed.py — University Bookstore Database Seeder
OMIS-105: Introduction to DBMS · Santa Clara University

Creates bookstore.duckdb with 5 tables and a curated dataset that tells
a consistent story:
  - CS & Engineering students buy the most books
  - Fall 2025 outsells Spring 2026
  - Required books outsell optional ones ~3:1
  - Seniors and juniors spend more per transaction than freshmen

Run:
    pip install duckdb
    python seed.py

Re-running drops and recreates all tables cleanly.
"""

import duckdb
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bookstore.duckdb")

# ── DDL ──────────────────────────────────────────────────────────────────────

DDL = """
DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS course_books;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS courses;

CREATE TABLE students (
    student_id   INTEGER        PRIMARY KEY,
    name         VARCHAR(100)   NOT NULL,
    email        VARCHAR(150)   UNIQUE NOT NULL,
    major        VARCHAR(80)    NOT NULL,
    year         INTEGER        NOT NULL CHECK (year BETWEEN 1 AND 4),
    gpa          DECIMAL(3,2)   CHECK (gpa BETWEEN 0.0 AND 4.0)
);

CREATE TABLE courses (
    course_id    INTEGER        PRIMARY KEY,
    course_name  VARCHAR(150)   NOT NULL,
    department   VARCHAR(80)    NOT NULL,
    credits      INTEGER        NOT NULL CHECK (credits BETWEEN 1 AND 6),
    semester     VARCHAR(20)    NOT NULL,
    instructor   VARCHAR(100)
);

CREATE TABLE books (
    book_id      INTEGER        PRIMARY KEY,
    title        VARCHAR(200)   NOT NULL,
    author       VARCHAR(150)   NOT NULL,
    isbn         VARCHAR(20)    UNIQUE NOT NULL,
    price        DECIMAL(6,2)   NOT NULL CHECK (price >= 0),
    category     VARCHAR(50)    NOT NULL,
    publisher    VARCHAR(100)
);

CREATE TABLE course_books (
    course_id    INTEGER        NOT NULL REFERENCES courses(course_id),
    book_id      INTEGER        NOT NULL REFERENCES books(book_id),
    required     BOOLEAN        NOT NULL DEFAULT TRUE,
    edition      VARCHAR(20),
    PRIMARY KEY (course_id, book_id)
);

CREATE TABLE purchases (
    purchase_id    INTEGER        PRIMARY KEY,
    student_id     INTEGER        NOT NULL REFERENCES students(student_id),
    book_id        INTEGER        NOT NULL REFERENCES books(book_id),
    course_id      INTEGER        REFERENCES courses(course_id),
    purchase_date  DATE           NOT NULL,
    quantity       INTEGER        NOT NULL DEFAULT 1 CHECK (quantity > 0),
    total_amount   DECIMAL(8,2)   NOT NULL CHECK (total_amount >= 0)
);
"""

# ── Seed Data ─────────────────────────────────────────────────────────────────

STUDENTS = [
    # (student_id, name, email, major, year, gpa)
    (1,  "Alice Chen",       "achen@scu.edu",    "Computer Science",      3, 3.82),
    (2,  "Brian Nguyen",     "bnguyen@scu.edu",  "Computer Science",      2, 3.45),
    (3,  "Carla Rivera",     "crivera@scu.edu",  "Electrical Engineering",4, 3.91),
    (4,  "David Park",       "dpark@scu.edu",    "Business Analytics",    2, 3.20),
    (5,  "Emma Torres",      "etorres@scu.edu",  "Computer Science",      1, 3.67),
    (6,  "Frank Zhao",       "fzhao@scu.edu",    "Mechanical Engineering",3, 3.55),
    (7,  "Grace Kim",        "gkim@scu.edu",     "Business Analytics",    4, 3.78),
    (8,  "Henry Okafor",     "hokafor@scu.edu",  "English Literature",    2, 3.30),
    (9,  "Isabella Martins", "imartins@scu.edu", "Computer Science",      4, 3.95),
    (10, "James Liu",        "jliu@scu.edu",     "Electrical Engineering",1, 3.10),
    # ── Students who have registered but never purchased a book ──
    (11, "Maria Santos",    "msantos@scu.edu",  "Computer Science",      1, 3.88),
    (12, "Kevin Osei",      "kosei@scu.edu",    "Business Analytics",    3, 3.42),
    (13, "Priya Nair",      "pnair@scu.edu",    "Electrical Engineering",2, 3.65),
]

COURSES = [
    # (course_id, course_name, department, credits, semester, instructor)
    (1,  "Introduction to Databases",     "Computer Science",      4, "Fall 2025",   "Dr. Parsian"),
    (2,  "Data Structures & Algorithms",  "Computer Science",      4, "Fall 2025",   "Dr. Lee"),
    (3,  "Circuit Analysis",              "Electrical Engineering",3, "Fall 2025",   "Dr. Nguyen"),
    (4,  "Business Statistics",           "Business Analytics",    3, "Fall 2025",   "Prof. Tanaka"),
    (5,  "Technical Writing",             "English Literature",    3, "Fall 2025",   "Prof. Walsh"),
    (6,  "Machine Learning Fundamentals", "Computer Science",      4, "Spring 2026", "Dr. Parsian"),
    (7,  "Digital Signal Processing",     "Electrical Engineering",3, "Spring 2026", "Dr. Nguyen"),
    (8,  "Marketing Analytics",           "Business Analytics",    3, "Spring 2026", "Prof. Tanaka"),
]

BOOKS = [
    # (book_id, title, author, isbn, price, category, publisher)
    (1,  "Database System Concepts",            "Silberschatz et al.",  "978-0078022159", 189.99, "Textbook",  "McGraw-Hill"),
    (2,  "Learning SQL",                        "Alan Beaulieu",        "978-0596520830",  49.99, "Reference", "O'Reilly"),
    (3,  "Introduction to Algorithms",          "Cormen et al.",        "978-0262046305", 114.95, "Textbook",  "MIT Press"),
    (4,  "Clean Code",                          "Robert Martin",        "978-0132350884",  44.99, "Reference", "Prentice Hall"),
    (5,  "Electric Circuits",                   "Nilsson & Riedel",     "978-0134746968", 224.99, "Textbook",  "Pearson"),
    (6,  "Fundamentals of Electric Circuits",   "Alexander & Sadiku",   "978-0078028229", 199.99, "Textbook",  "McGraw-Hill"),
    (7,  "Statistics for Business",             "Groebner et al.",      "978-0134496498", 179.99, "Textbook",  "Pearson"),
    (8,  "Naked Statistics",                    "Charles Wheelan",      "978-0393347777",  17.99, "Novel",     "Norton"),
    (9,  "The Elements of Style",               "Strunk & White",       "978-0205309023",  9.99,  "Reference", "Longman"),
    (10, "Technical Communication",             "Markel & Selber",      "978-1319058616", 139.99, "Textbook",  "Bedford"),
    (11, "Hands-On Machine Learning",           "Aurélien Géron",       "978-1492032649",  79.99, "Textbook",  "O'Reilly"),
    (12, "Deep Learning",                       "Goodfellow et al.",    "978-0262035613",  89.99, "Textbook",  "MIT Press"),
    (13, "Pattern Recognition & ML",            "Christopher Bishop",   "978-0387310732",  74.99, "Reference", "Springer"),
    (14, "Digital Signal Processing",           "Proakis & Manolakis",  "978-0131873742", 214.99, "Textbook",  "Pearson"),
    (15, "Signal Processing First",             "McClellan et al.",     "978-0130909992", 169.99, "Textbook",  "Pearson"),
    (16, "Marketing Analytics",                 "Wayne Winston",        "978-1119268529",  89.99, "Textbook",  "Wiley"),
    (17, "Data-Driven Marketing",               "Mark Jeffery",         "978-0470504543",  34.99, "Reference", "Wiley"),
    (18, "Invisible Man",                       "Ralph Ellison",        "978-0679732761",  16.99, "Novel",     "Vintage"),
    (19, "SQL Pocket Guide",                    "Alice Zheng",          "978-1492090397",  24.99, "Reference", "O'Reilly"),
    (20, "The Pragmatic Programmer",            "Hunt & Thomas",        "978-0135957059",  49.99, "Reference", "Addison-Wesley"),
    # ── Books in catalog that have never been purchased ──
    (21, "Artificial Intelligence: A Modern Approach", "Russell & Norvig",    "978-0136042594", 189.99, "Textbook",  "Pearson"),
    (22, "The Art of War",                             "Sun Tzu",             "978-1590302255",  12.99, "Novel",     "Shambhala"),
    (23, "Python for Data Analysis",                   "Wes McKinney",        "978-1491957660",  59.99, "Reference", "O'Reilly"),
    (24, "Operating System Concepts",                  "Silberschatz et al.", "978-1119800361", 199.99, "Textbook",  "Wiley"),
]

COURSE_BOOKS = [
    # (course_id, book_id, required, edition)
    (1, 1,  True,  "7th"),   # Intro DB → Database System Concepts (required)
    (1, 2,  False, "3rd"),   # Intro DB → Learning SQL (optional)
    (1, 19, False, "5th"),   # Intro DB → SQL Pocket Guide (optional)
    (2, 3,  True,  "4th"),   # DSA → Introduction to Algorithms (required)
    (2, 4,  False, "1st"),   # DSA → Clean Code (optional)
    (2, 20, False, "2nd"),   # DSA → Pragmatic Programmer (optional)
    (3, 5,  True,  "10th"),  # Circuits → Electric Circuits (required)
    (3, 6,  False, "7th"),   # Circuits → Fundamentals of Electric Circuits (optional)
    (4, 7,  True,  "9th"),   # Biz Stats → Statistics for Business (required)
    (4, 8,  False, "1st"),   # Biz Stats → Naked Statistics (optional)
    (5, 10, True,  "11th"),  # Tech Writing → Technical Communication (required)
    (5, 9,  True,  "50th"),  # Tech Writing → Elements of Style (required)
    (5, 18, False, "1st"),   # Tech Writing → Invisible Man (optional)
    (6, 11, True,  "3rd"),   # ML → Hands-On ML (required)
    (6, 12, False, "1st"),   # ML → Deep Learning (optional)
    (6, 13, False, "1st"),   # ML → Pattern Recognition (optional)
    (7, 14, True,  "4th"),   # DSP → Digital Signal Processing (required)
    (7, 15, False, "1st"),   # DSP → Signal Processing First (optional)
    (8, 16, True,  "1st"),   # Mktg Analytics → Marketing Analytics (required)
    (8, 17, False, "1st"),   # Mktg Analytics → Data-Driven Marketing (optional)
]

PURCHASES = [
    # (purchase_id, student_id, book_id, course_id, purchase_date, quantity, total_amount)
    # ── Fall 2025 purchases ──────────────────────────────────────────────────
    # Alice (CS junior) — takes Intro DB and DSA
    (1,  1, 1,  1, "2025-08-28", 1, 189.99),   # DB textbook
    (2,  1, 2,  1, "2025-08-28", 1,  49.99),   # Learning SQL
    (3,  1, 3,  2, "2025-08-29", 1, 114.95),   # Algorithms
    (4,  1, 4,  2, "2025-09-05", 1,  44.99),   # Clean Code

    # Brian (CS sophomore) — takes Intro DB
    (5,  2, 1,  1, "2025-08-30", 1, 189.99),   # DB textbook
    (6,  2, 19, 1, "2025-09-02", 1,  24.99),   # SQL Pocket Guide

    # Carla (EE senior) — takes Circuit Analysis
    (7,  3, 5,  3, "2025-08-27", 1, 224.99),   # Electric Circuits
    (8,  3, 6,  3, "2025-09-01", 1, 199.99),   # Fundamentals (optional but buys it)

    # David (BA sophomore) — takes Business Stats
    (9,  4, 7,  4, "2025-08-29", 1, 179.99),   # Stats for Business
    (10, 4, 8,  4, "2025-09-10", 1,  17.99),   # Naked Statistics

    # Emma (CS freshman) — takes Intro DB
    (11, 5, 1,  1, "2025-09-01", 1, 189.99),   # DB textbook
    (12, 5, 2,  1, "2025-09-03", 1,  49.99),   # Learning SQL

    # Frank (ME junior) — takes Circuit Analysis
    (13, 6, 5,  3, "2025-08-28", 1, 224.99),   # Electric Circuits

    # Grace (BA senior) — takes Business Stats
    (14, 7, 7,  4, "2025-08-27", 1, 179.99),   # Stats for Business
    (15, 7, 8,  4, "2025-09-08", 1,  17.99),   # Naked Statistics

    # Henry (English sophomore) — takes Technical Writing
    (16, 8, 10, 5, "2025-08-30", 1, 139.99),   # Technical Communication
    (17, 8, 9,  5, "2025-09-01", 1,   9.99),   # Elements of Style

    # Isabella (CS senior) — takes Intro DB and DSA
    (18, 9, 1,  1, "2025-08-26", 1, 189.99),   # DB textbook
    (19, 9, 2,  1, "2025-08-26", 1,  49.99),   # Learning SQL
    (20, 9, 3,  2, "2025-08-27", 1, 114.95),   # Algorithms
    (21, 9, 20, 2, "2025-09-04", 1,  49.99),   # Pragmatic Programmer

    # James (EE freshman) — takes Circuit Analysis
    (22, 10, 5, 3, "2025-09-02", 1, 224.99),   # Electric Circuits

    # Mid-semester purchases (Oct–Nov)
    (23, 1, 20, 2, "2025-10-15", 1,  49.99),   # Alice buys Pragmatic Programmer
    (24, 2, 4,  2, "2025-10-20", 1,  44.99),   # Brian buys Clean Code (for DSA)
    (25, 9, 19, 1, "2025-11-01", 1,  24.99),   # Isabella buys SQL Pocket Guide
    (26, 5, 19, 1, "2025-11-05", 1,  24.99),   # Emma buys SQL Pocket Guide
    (27, 3, 9,  5, "2025-10-18", 1,   9.99),   # Carla buys Elements of Style (no course)
    (28, 7, 17, None,"2025-11-12",1,  34.99),  # Grace buys Data-Driven Marketing (interest)
    (29, 4, 20, None,"2025-10-30",1,  49.99),  # David buys Pragmatic Programmer (interest)

    # ── Spring 2026 purchases ────────────────────────────────────────────────
    # Alice (CS junior) — takes Machine Learning
    (30, 1, 11, 6, "2026-01-15", 1,  79.99),   # Hands-On ML
    (31, 1, 12, 6, "2026-01-16", 1,  89.99),   # Deep Learning

    # Brian (CS sophomore) — takes Machine Learning
    (32, 2, 11, 6, "2026-01-17", 1,  79.99),   # Hands-On ML
    (33, 2, 13, 6, "2026-01-20", 1,  74.99),   # Pattern Recognition

    # Carla (EE senior) — takes DSP
    (34, 3, 14, 7, "2026-01-14", 1, 214.99),   # DSP textbook
    (35, 3, 15, 7, "2026-01-15", 1, 169.99),   # Signal Processing First

    # David (BA sophomore) — takes Marketing Analytics
    (36, 4, 16, 8, "2026-01-16", 1,  89.99),   # Marketing Analytics
    (37, 4, 17, 8, "2026-01-18", 1,  34.99),   # Data-Driven Marketing

    # Emma (CS freshman) — takes Machine Learning
    (38, 5, 11, 6, "2026-01-18", 1,  79.99),   # Hands-On ML

    # Frank (ME junior) — takes DSP
    (39, 6, 14, 7, "2026-01-15", 1, 214.99),   # DSP textbook

    # Grace (BA senior) — takes Marketing Analytics
    (40, 7, 16, 8, "2026-01-14", 1,  89.99),   # Marketing Analytics
    (41, 7, 17, 8, "2026-01-17", 1,  34.99),   # Data-Driven Marketing

    # Henry (English sophomore) — general interest reads
    (42, 8, 18, 5, "2026-01-20", 1,  16.99),   # Invisible Man

    # Isabella (CS senior) — takes Machine Learning
    (43, 9, 11, 6, "2026-01-13", 1,  79.99),   # Hands-On ML
    (44, 9, 12, 6, "2026-01-13", 1,  89.99),   # Deep Learning
    (45, 9, 13, 6, "2026-01-14", 1,  74.99),   # Pattern Recognition

    # James (EE freshman) — takes DSP
    (46, 10, 14, 7, "2026-01-16", 1, 214.99),  # DSP textbook

    # Mid-semester Spring purchases
    (47, 1, 13, 6,  "2026-02-10", 1,  74.99),  # Alice adds Pattern Recognition
    (48, 5, 12, 6,  "2026-02-15", 1,  89.99),  # Emma adds Deep Learning
    (49, 6, 15, 7,  "2026-02-08", 1, 169.99),  # Frank adds Signal Processing First
    (50, 10,15, 7,  "2026-02-12", 1, 169.99),  # James adds Signal Processing First
    (51, 4, 8,  None,"2026-03-01", 1,  17.99), # David re-buys Naked Statistics (gift)
    (52, 7, 20, None,"2026-02-20", 1,  49.99), # Grace buys Pragmatic Programmer
    (53, 9, 20, None,"2026-03-05", 1,  49.99), # Isabella buys Pragmatic Programmer
    (54, 2, 11, 6,  "2026-03-10", 2,  79.99),  # Brian buys 2 copies (one for friend)
    (55, 3, 9,  None,"2026-02-14", 1,   9.99), # Carla buys Elements of Style
    (56, 8, 9,  5,  "2026-01-22", 1,   9.99),  # Henry buys another copy (lost)
    (57, 1, 19, None,"2026-04-01", 1,  24.99), # Alice buys SQL Pocket Guide again
    (58, 5, 4,  None,"2026-03-20", 1,  44.99), # Emma buys Clean Code
    (59, 9, 4,  None,"2026-04-10", 1,  44.99), # Isabella buys Clean Code
    (60, 10, 6, 3,  "2026-04-15", 1, 199.99),  # James buys Fundamentals of Circuits
]


# ── Load ──────────────────────────────────────────────────────────────────────

def seed():
    con = duckdb.connect(DB_PATH)

    print(f"Creating database at: {DB_PATH}")
    for stmt in DDL.strip().split(";"):
        stmt = stmt.strip()
        if stmt:
            con.execute(stmt)

    print("Inserting students   ...", end=" ")
    con.executemany(
        "INSERT INTO students VALUES (?,?,?,?,?,?)", STUDENTS)
    print(f"{len(STUDENTS)} rows")

    print("Inserting courses    ...", end=" ")
    con.executemany(
        "INSERT INTO courses VALUES (?,?,?,?,?,?)", COURSES)
    print(f"{len(COURSES)} rows")

    print("Inserting books      ...", end=" ")
    con.executemany(
        "INSERT INTO books VALUES (?,?,?,?,?,?,?)", BOOKS)
    print(f"{len(BOOKS)} rows")

    print("Inserting course_books...", end=" ")
    con.executemany(
        "INSERT INTO course_books VALUES (?,?,?,?)", COURSE_BOOKS)
    print(f"{len(COURSE_BOOKS)} rows")

    print("Inserting purchases  ...", end=" ")
    con.executemany(
        "INSERT INTO purchases VALUES (?,?,?,?,?,?,?)", PURCHASES)
    print(f"{len(PURCHASES)} rows")

    # ── Verification ──
    print("\n── Row counts ──────────────────────────────")
    for table in ["students", "courses", "books", "course_books", "purchases"]:
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:<15} {n:>4} rows")

    print("\n── Story checks ────────────────────────────")
    dept_rev = con.execute("""
        SELECT c.department, ROUND(SUM(p.total_amount),2) AS revenue
        FROM purchases p
        JOIN courses c ON p.course_id = c.course_id
        WHERE p.course_id IS NOT NULL
        GROUP BY c.department
        ORDER BY revenue DESC
    """).fetchall()
    print("  Revenue by department:")
    for row in dept_rev:
        print(f"    {row[0]:<30} ${row[1]:>8,.2f}")

    sem_rev = con.execute("""
        SELECT c.semester, ROUND(SUM(p.total_amount),2) AS revenue
        FROM purchases p
        JOIN courses c ON p.course_id = c.course_id
        WHERE p.course_id IS NOT NULL
        GROUP BY c.semester
        ORDER BY revenue DESC
    """).fetchall()
    print("  Revenue by semester:")
    for row in sem_rev:
        print(f"    {row[0]:<15} ${row[1]:>8,.2f}")

    req_ratio = con.execute("""
        SELECT cb.required,
               COUNT(*) AS num_purchases,
               ROUND(SUM(p.total_amount),2) AS revenue
        FROM purchases p
        JOIN course_books cb
          ON p.book_id = cb.book_id AND p.course_id = cb.course_id
        GROUP BY cb.required
    """).fetchall()
    print("  Required vs optional purchases:")
    for row in req_ratio:
        label = "Required" if row[0] else "Optional"
        print(f"    {label:<10} {row[1]:>3} purchases  ${row[2]:>8,.2f}")

    con.close()
    print(f"\n✓ bookstore.duckdb is ready.\n")


if __name__ == "__main__":
    seed()
