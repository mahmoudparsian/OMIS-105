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
    # Relational Database Table Relationships: A Hands-On Tutorial

    **Tools:** Python, DuckDB, Jupyter Notebook  
    **Author:** Tutorial for SCU Database Course  
    **Date:** May 2026

    ---

    ## Overview

    Relational database table relationships define how data in one table links to another.  
    They use **foreign keys** to maintain **referential integrity** — ensuring that references between tables are always valid.

    The three fundamental relationship types are:

    | Relationship | Notation | Example |
    |:-------------|:---------|:--------|
    | One-to-One   | 1:1      | Person ↔ Passport |
    | One-to-Many  | 1:N      | Department → Employees |
    | Many-to-Many | N:M      | Students ↔ Courses |

    In this notebook we will:
    1. Create simple tables in **DuckDB** (an in-process analytical database)
    2. Insert sample data
    3. Run queries that demonstrate each relationship
    4. Visualize each relationship with diagrams
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    First, install DuckDB if you haven't already:
    ```bash
    pip install duckdb
    ```
    """)
    return


@app.cell
def _():
    import duckdb

    # Create an in-memory DuckDB database
    con = duckdb.connect(database=':memory:')

    # Helper function to display query results as a formatted table
    def run(sql, title=None):
        """Execute SQL and display results."""
        if title:
            print(f"\n{'='*60}")
            print(f"  {title}")
            print(f"{'='*60}")
        result = con.execute(sql)
        try:
            df = result.fetchdf()
            if not df.empty:
                print(df.to_string(index=False))
            else:
                print("(no rows returned)")
            return df
        except:
            print("(statement executed successfully)")
            return None

    print(f"DuckDB version: {duckdb.__version__}")
    print("In-memory database created successfully.")
    return (con, run)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # 1. One-to-One (1:1) Relationship

    ## Concept

    In a **One-to-One** relationship, each row in Table A is linked to **at most one** row in Table B, and vice versa.

    **Key characteristics:**
    - The foreign key column has a `UNIQUE` constraint
    - Each record in one table corresponds to exactly one record in the other
    - Often used to split a table for security, performance, or organizational reasons

    **Real-world examples:**
    - Person ↔ Passport (each person has at most one passport)
    - User ↔ UserProfile (separating login credentials from profile details)
    - Employee ↔ ParkingSpot (one reserved spot per employee)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1:1 Relationship Diagram

    ```
      ┌──────────────────┐         ┌──────────────────────────┐
      │     persons       │         │       passports           │
      ├──────────────────┤         ├──────────────────────────┤
      │ PK  person_id    │───1:1──▶│ PK  passport_id          │
      │     name         │         │ FK  person_id  (UNIQUE)  │
      │     birth_date   │         │     passport_number      │
      │                  │         │     issue_date           │
      │                  │         │     expiry_date          │
      └──────────────────┘         └──────────────────────────┘

      PK = Primary Key
      FK = Foreign Key (with UNIQUE constraint → enforces 1:1)
    ```

    The `UNIQUE` constraint on `person_id` in the `passports` table is what **enforces** the 1:1 relationship. Without it, one person could have many passports (making it 1:N).
    """)
    return


@app.cell
def _(con):
    # ============================================================
    # 1:1 RELATIONSHIP — Person ↔ Passport
    # ============================================================

    # Create the parent table: persons
    con.execute("""
        CREATE TABLE persons (
            person_id  INTEGER PRIMARY KEY,
            name       VARCHAR NOT NULL,
            birth_date DATE NOT NULL
        );
    """)

    # Create the child table: passports
    # Note: person_id is UNIQUE — this enforces the 1:1 relationship
    con.execute("""
        CREATE TABLE passports (
            passport_id     INTEGER PRIMARY KEY,
            person_id       INTEGER NOT NULL UNIQUE,
            passport_number VARCHAR NOT NULL UNIQUE,
            issue_date      DATE NOT NULL,
            expiry_date     DATE NOT NULL,
            FOREIGN         KEY (person_id) REFERENCES persons(person_id)
        );
    """)

    print("Tables 'persons' and 'passports' created.")
    print("The UNIQUE constraint on passports.person_id enforces the 1:1 relationship.")
    return


@app.cell
def _(con, run):
    # Insert sample data into persons
    con.execute("""
        INSERT INTO persons (person_id, name, birth_date)
        VALUES
            (1, 'Alice Johnson', '1990-03-15'),
            (2, 'Bob Smith', '1985-07-22'),
            (3, 'Carol Williams', '1992-11-08'),
            (4, 'David Brown', '1988-01-30');
    """)

    # Insert sample data into passports
    # Note: David (person_id=4) does NOT have a passport
    con.execute("""
        INSERT INTO passports (passport_id, person_id, passport_number, issue_date, expiry_date)
        VALUES
            (101, 1, 'US-1234567', '2020-01-10', '2030-01-10'),
            (102, 2, 'US-2345678', '2019-06-15', '2029-06-15'),
            (103, 3, 'US-3456789', '2021-09-20', '2031-09-20');
    """)

    run("""
        SELECT *
        FROM persons;
    """, "All Persons")
    run("""
        SELECT *
        FROM passports;
    """, "All Passports")
    return


@app.cell
def _(run):
    # QUERY 1: JOIN persons with their passports
    # Uses INNER JOIN — only persons WITH a passport appear
    run("""
        SELECT
            p.person_id,
            p.name,
            pp.passport_number,
            pp.expiry_date
        FROM persons p
        INNER
        JOIN passports pp ON p.person_id = pp.person_id
        ORDER BY p.person_id;
    """, "INNER JOIN: Persons with Passports")
    return


@app.cell
def _(run):
    # QUERY 2: LEFT JOIN — shows ALL persons, even those without a passport
    # David appears with NULLs for passport fields
    run("""
        SELECT
            p.person_id,
            p.name,
            pp.passport_number,
            pp.expiry_date
        FROM persons p
        LEFT
        JOIN passports pp ON p.person_id = pp.person_id
        ORDER BY p.person_id;
    """, "LEFT JOIN: All Persons (with or without Passport)")
    return


@app.cell
def _(con):
    # PROOF OF 1:1 CONSTRAINT
    # Attempting to insert a second passport for Alice (person_id=1)
    # This SHOULD fail because of the UNIQUE constraint on person_id

    try:
        con.execute("""
            INSERT INTO passports (passport_id, person_id, passport_number, issue_date, expiry_date)
            VALUES (104, 1, 'US-9999999', '2025-01-01', '2035-01-01');
        """)
        print("ERROR: Insert succeeded — 1:1 constraint not enforced!")
    except Exception as e:
        print("SUCCESS: The 1:1 constraint prevented a duplicate!")
        print(f"Error message: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Key Takeaway — One-to-One

    The **1:1 relationship** is enforced by placing a `UNIQUE` constraint on the foreign key column.  
    This guarantees that no two rows in the child table can reference the same parent row.

    | Without UNIQUE | With UNIQUE |
    |:---------------|:------------|
    | Person → many passports (1:N) | Person → at most one passport (1:1) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # 2. One-to-Many (1:N) Relationship

    ## Concept

    In a **One-to-Many** relationship, a single row in Table A can be linked to **multiple** rows in Table B, but each row in Table B links to **at most one** row in Table A.

    **This is the most common relationship type in relational databases.**

    **Key characteristics:**
    - The foreign key is on the "many" side (the child table)
    - The foreign key column does **NOT** have a UNIQUE constraint
    - Multiple child rows can reference the same parent row

    **Real-world examples:**
    - Department → Employees (one department has many employees)
    - Customer → Orders (one customer places many orders)
    - Author → Books (one author writes many books)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1:N Relationship Diagram

    ```
      ┌──────────────────┐         ┌──────────────────────────┐
      │   departments     │         │       employees           │
      ├──────────────────┤         ├──────────────────────────┤
      │ PK  dept_id      │──┐      │ PK  emp_id               │
      │     dept_name    │  │      │ FK  dept_id  (NOT UNIQUE)│
      │     location     │  │1:N   │     emp_name             │
      │                  │  ├─────▶│     salary               │
      │                  │  │      │     hire_date            │
      │                  │  │      │                          │
      └──────────────────┘  │      └──────────────────────────┘
                            │
             One dept ──────┘────── has Many employees

      PK = Primary Key
      FK = Foreign Key (NO unique constraint → allows 1:N)
    ```

    Notice that `dept_id` in `employees` is a foreign key **without** a UNIQUE constraint. This allows multiple employees to belong to the same department.
    """)
    return


@app.cell
def _(con):
    # ============================================================
    # 1:N RELATIONSHIP — Department → Employees
    # ============================================================

    # Create the parent table (the "one" side): departments
    con.execute("""
        CREATE TABLE departments (
            dept_id   INTEGER PRIMARY KEY,
            dept_name VARCHAR NOT NULL,
            location  VARCHAR NOT NULL
        );
    """)

    # Create the child table (the "many" side): employees
    # Note: dept_id is NOT UNIQUE — multiple employees can share the same dept_id
    con.execute("""
        CREATE TABLE employees (
            emp_id    INTEGER PRIMARY KEY,
            dept_id   INTEGER NOT NULL,
            emp_name  VARCHAR NOT NULL,
            salary    DECIMAL(10, 2) NOT NULL,
            hire_date DATE NOT NULL,
            FOREIGN   KEY (dept_id) REFERENCES departments(dept_id)
        );
    """)

    print("Tables 'departments' and 'employees' created.")
    print("No UNIQUE constraint on employees.dept_id → allows 1:N.")
    return


@app.cell
def _(con, run):
    # Insert departments
    con.execute("""
        INSERT INTO departments (dept_id, dept_name, location)
        VALUES
            (10, 'Engineering', 'Building A'),
            (20, 'Marketing', 'Building B'),
            (30, 'Sales', 'Building C');
    """)

    # Insert employees — notice multiple employees per department
    con.execute("""
        INSERT INTO employees (emp_id, dept_id, emp_name, salary, hire_date)
        VALUES
            (1001, 10, 'Eve Adams', 95000.00, '2020-03-01'),
            (1002, 10, 'Frank Miller', 88000.00, '2021-06-15'),
            (1003, 10, 'Grace Lee', 102000.00, '2019-01-20'),
            (1004, 20, 'Hank Wilson', 78000.00, '2022-02-10'),
            (1005, 20, 'Ivy Chen', 82000.00, '2021-11-05'),
            (1006, 30, 'Jack Taylor', 91000.00, '2020-07-30');
    """)

    run("""
        SELECT *
        FROM departments;
    """, "All Departments")
    run("""
        SELECT *
        FROM employees;
    """, "All Employees")
    return


@app.cell
def _(run):
    # QUERY 1: JOIN — show each employee with their department name
    run("""
        SELECT
            e.emp_id,
            e.emp_name,
            d.dept_name,
            d.location,
            e.salary
        FROM employees e
        INNER
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY d.dept_name, e.emp_name;
    """, "Employees with their Departments")
    return


@app.cell
def _(run):
    # QUERY 2: COUNT employees per department (aggregation on the 1:N relationship)
    run("""
        SELECT
            d.dept_name,
            COUNT(e.emp_id) AS num_employees,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary
        FROM departments d
        LEFT
        JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
        ORDER BY num_employees DESC;
    """, "Department Summary (Aggregation over 1:N)")
    return


@app.cell
def _(run):
    # PROOF: Multiple employees CAN reference the same department
    # This is the fundamental difference from 1:1
    run("""
        SELECT
            dept_id,
            COUNT(*) AS employee_count
        FROM employees
        GROUP BY dept_id
        HAVING COUNT(*) > 1
        ORDER BY dept_id;
    """, "Departments with Multiple Employees (proves 1:N)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Key Takeaway — One-to-Many

    | Feature | 1:1 (Person↔Passport) | 1:N (Dept→Employees) |
    |:--------|:---------------------|:---------------------|
    | FK has UNIQUE? | Yes | **No** |
    | Multiple children per parent? | No | **Yes** |
    | Most common? | Rare | **Very common** |

    The **absence** of a `UNIQUE` constraint on the foreign key is what allows the one-to-many relationship.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # 3. Many-to-Many (N:M) Relationship

    ## Concept

    In a **Many-to-Many** relationship, each row in Table A can be linked to **multiple** rows in Table B, **and** each row in Table B can be linked to **multiple** rows in Table A.

    **Key characteristics:**
    - Cannot be represented with a single foreign key
    - Requires a **junction table** (also called a bridge, link, or associative table)
    - The junction table contains two foreign keys — one to each of the related tables
    - The junction table may also carry additional attributes about the relationship itself

    **Real-world examples:**
    - Students ↔ Courses (a student enrolls in many courses; a course has many students)
    - Authors ↔ Books (an author can write many books; a book can have many authors)
    - Actors ↔ Movies (an actor appears in many movies; a movie has many actors)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### N:M Relationship Diagram

    ```
      ┌──────────────────┐       ┌─────────────────────────┐       ┌──────────────────┐
      │    students       │       │     enrollments          │       │     courses       │
      ├──────────────────┤       │    (junction table)      │       ├──────────────────┤
      │ PK  student_id   │──┐    ├─────────────────────────┤    ┌──│ PK  course_id    │
      │     student_name │  │    │ PK  enrollment_id       │    │  │     course_name  │
      │     major        │  │1:N │ FK  student_id ─────────│────┘  │     credits      │
      │                  │  └───▶│ FK  course_id  ─────────│───┘   │                  │
      │                  │       │     grade      (extra!) │  N:1  │                  │
      │                  │       │     semester   (extra!) │       │                  │
      └──────────────────┘       └─────────────────────────┘       └──────────────────┘

      The N:M relationship is decomposed into two 1:N relationships
      via the junction table 'enrollments'.

      students  ──1:N──▶  enrollments  ◀──N:1──  courses
    ```

    **Important insight:** An N:M relationship is always **decomposed into two 1:N relationships** through a junction table. The junction table sits in the middle and holds foreign keys to both sides.
    """)
    return


@app.cell
def _(con):
    # ============================================================
    # N:M RELATIONSHIP — Students ↔ Courses
    # ============================================================

    # Table A: students
    con.execute("""
        CREATE TABLE students (
            student_id   INTEGER PRIMARY KEY,
            student_name VARCHAR NOT NULL,
            major        VARCHAR NOT NULL
        );
    """)

    # Table B: courses
    con.execute("""
        CREATE TABLE courses (
            course_id   INTEGER PRIMARY KEY,
            course_name VARCHAR NOT NULL,
            credits     INTEGER NOT NULL
        );
    """)

    # Junction table: enrollments
    # This table "connects" students and courses
    # It also stores relationship-specific data: grade and semester
    con.execute("""
        CREATE TABLE enrollments (
            enrollment_id INTEGER PRIMARY KEY,
            student_id    INTEGER NOT NULL,
            course_id     INTEGER NOT NULL,
            grade         VARCHAR,
            semester      VARCHAR NOT NULL,
            FOREIGN       KEY (student_id) REFERENCES students(student_id),
            FOREIGN       KEY (course_id) REFERENCES courses(course_id),
            UNIQUE        (student_id, course_id, semester) /* prevent duplicate enrollments */
        );
    """)

    print("Tables 'students', 'courses', and 'enrollments' (junction) created.")
    print("The junction table decomposes the N:M into two 1:N relationships.")
    return


@app.cell
def _(con, run):
    # Insert students
    con.execute("""
        INSERT INTO students (student_id, student_name, major)
        VALUES
            (1, 'Maria Garcia', 'Computer Science'),
            (2, 'James Wilson', 'Mathematics'),
            (3, 'Sarah Kim', 'Computer Science'),
            (4, 'Robert Johnson', 'Physics');
    """)

    # Insert courses
    con.execute("""
        INSERT INTO courses (course_id, course_name, credits)
        VALUES
            (201, 'Database Systems', 4),
            (202, 'Linear Algebra', 3),
            (203, 'Machine Learning', 4),
            (204, 'Data Structures', 4);
    """)

    # Insert enrollments (the N:M connections)
    # Each student takes multiple courses; each course has multiple students
    con.execute("""
        INSERT INTO enrollments (enrollment_id, student_id, course_id, grade, semester)
        VALUES
            (1, 1, 201, 'A', 'Fall 2025'),
            (2, 1, 203, 'A-', 'Fall 2025'),
            (3, 1, 204, 'B+', 'Fall 2025'),
            (4, 2, 201, 'B', 'Fall 2025'),
            (5, 2, 202, 'A', 'Fall 2025'),
            (6, 3, 201, 'A', 'Fall 2025'),
            (7, 3, 203, 'B+', 'Fall 2025'),
            (8, 4, 202, 'A-', 'Fall 2025'),
            (9, 4, 203, 'B', 'Fall 2025'),
            (10, 4, 204, 'A', 'Fall 2025');
    """)

    run("""
        SELECT *
        FROM students;
    """, "All Students")
    run("""
        SELECT *
        FROM courses;
    """, "All Courses")
    run("""
        SELECT *
        FROM enrollments;
    """, "All Enrollments (Junction Table)")
    return


@app.cell
def _(run):
    # QUERY 1: Show each student with all their courses
    run("""
        SELECT
            s.student_name,
            c.course_name,
            e.grade,
            c.credits
        FROM students s
        INNER
        JOIN enrollments e ON s.student_id = e.student_id
        INNER
        JOIN courses c ON e.course_id = c.course_id
        ORDER BY s.student_name, c.course_name;
    """, "Students and Their Courses (N:M via Junction Table)")
    return


@app.cell
def _(run):
    # QUERY 2: Show each course with all enrolled students
    # (Same data, viewed from the other direction)
    run("""
        SELECT
            c.course_name,
            c.credits,
            s.student_name,
            e.grade
        FROM courses c
        INNER
        JOIN enrollments e ON c.course_id = e.course_id
        INNER
        JOIN students s ON e.student_id = s.student_id
        ORDER BY c.course_name, s.student_name;
    """, "Courses and Their Students (reverse direction of N:M)")
    return


@app.cell
def _(run):
    # QUERY 3: Count of courses per student AND count of students per course
    # This proves the "many" on both sides

    run("""
        SELECT
            s.student_name,
            COUNT(e.course_id) AS courses_enrolled
        FROM students s
        LEFT
        JOIN enrollments e ON s.student_id = e.student_id
        GROUP BY s.student_name
        ORDER BY courses_enrolled DESC;
    """, "Courses per Student (proves MANY on student side)")

    run("""
        SELECT
            c.course_name,
            COUNT(e.student_id) AS students_enrolled
        FROM courses c
        LEFT
        JOIN enrollments e ON c.course_id = e.course_id
        GROUP BY c.course_name
        ORDER BY students_enrolled DESC;
    """, "Students per Course (proves MANY on course side)")
    return


@app.cell
def _(run):
    # QUERY 4: GPA calculation using the junction table
    # The junction table's 'grade' attribute enables this

    run("""
        WITH grade_points AS (
        SELECT
            s.student_name,
            c.course_name,
            c.credits,
            e.grade,
            CASE e.grade WHEN 'A' THEN 4.0 WHEN 'A-' THEN 3.7 WHEN 'B+' THEN 3.3 WHEN 'B' THEN 3.0 WHEN 'B-' THEN 2.7 WHEN 'C+' THEN 2.3 WHEN 'C' THEN 2.0 ELSE 0.0 END AS gpa_points
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id )
        SELECT
            student_name,
            ROUND(SUM(gpa_points * credits) / SUM(credits), 2) AS weighted_gpa,
            SUM(credits) AS total_credits
        FROM grade_points
        GROUP BY student_name
        ORDER BY weighted_gpa DESC;
    """, "Weighted GPA per Student (computed via junction table)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Key Takeaway — Many-to-Many

    An N:M relationship **cannot** be represented with a single foreign key. It requires a **junction table** that:

    1. Contains foreign keys to **both** related tables
    2. Decomposes the N:M into **two 1:N relationships**
    3. Can carry **additional attributes** about the relationship itself (e.g., grade, semester)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # 4. Visual Summary of All Three Relationships
    """)
    return


@app.cell
def _():
    from IPython.display import SVG, display, HTML

    # ============================================================
    # SVG Diagram: One-to-One (1:1)
    # ============================================================
    svg_one_to_one = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 220" width="700" height="220">
      <defs>
        <marker id="arrow1" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
          <polygon points="0 0, 10 3.5, 0 7" fill="#2563eb"/>
        </marker>
      </defs>
      
      <!-- Title -->
      <text x="350" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#1e293b">One-to-One (1:1) Relationship</text>
      
      <!-- Persons table -->
      <rect x="40" y="50" width="220" height="140" rx="8" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <rect x="40" y="50" width="220" height="35" rx="8" fill="#2563eb"/>
      <rect x="40" y="77" width="220" height="8" fill="#2563eb"/>
      <text x="150" y="74" text-anchor="middle" font-size="14" font-weight="bold" fill="white">persons</text>
      <text x="60" y="110" font-size="13" fill="#1e293b" font-family="monospace">PK  person_id</text>
      <text x="60" y="130" font-size="13" fill="#1e293b" font-family="monospace">    name</text>
      <text x="60" y="150" font-size="13" fill="#1e293b" font-family="monospace">    birth_date</text>
      
      <!-- Passports table -->
      <rect x="440" y="50" width="220" height="140" rx="8" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <rect x="440" y="50" width="220" height="35" rx="8" fill="#2563eb"/>
      <rect x="440" y="77" width="220" height="8" fill="#2563eb"/>
      <text x="550" y="74" text-anchor="middle" font-size="14" font-weight="bold" fill="white">passports</text>
      <text x="460" y="110" font-size="13" fill="#1e293b" font-family="monospace">PK  passport_id</text>
      <text x="460" y="130" font-size="13" fill="#1e293b" font-family="monospace">FK  person_id (UQ)</text>
      <text x="460" y="150" font-size="13" fill="#1e293b" font-family="monospace">    passport_number</text>
      <text x="460" y="170" font-size="13" fill="#1e293b" font-family="monospace">    expiry_date</text>
      
      <!-- Arrow -->
      <line x1="260" y1="120" x2="430" y2="120" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrow1)"/>
      <text x="345" y="112" text-anchor="middle" font-size="15" font-weight="bold" fill="#2563eb">1 : 1</text>
      
      <!-- Cardinality labels -->
      <text x="268" y="138" font-size="12" fill="#64748b">one</text>
      <text x="410" y="138" font-size="12" fill="#64748b">one</text>
      
      <!-- Note -->
      <text x="350" y="210" text-anchor="middle" font-size="12" fill="#64748b" font-style="italic">UNIQUE constraint on FK enforces the 1:1 rule</text>
    </svg>
    """

    display(SVG(svg_one_to_one))
    print()
    return (SVG, display)


@app.cell
def _(SVG, display):
    # ============================================================
    # SVG Diagram: One-to-Many (1:N)
    # ============================================================
    svg_one_to_many = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 220" width="700" height="220">
      <defs>
        <marker id="arrow2" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
          <polygon points="0 0, 10 3.5, 0 7" fill="#059669"/>
        </marker>
      </defs>
      
      <!-- Title -->
      <text x="350" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#1e293b">One-to-Many (1:N) Relationship</text>
      
      <!-- Departments table -->
      <rect x="40" y="50" width="220" height="140" rx="8" fill="#d1fae5" stroke="#059669" stroke-width="2"/>
      <rect x="40" y="50" width="220" height="35" rx="8" fill="#059669"/>
      <rect x="40" y="77" width="220" height="8" fill="#059669"/>
      <text x="150" y="74" text-anchor="middle" font-size="14" font-weight="bold" fill="white">departments</text>
      <text x="60" y="110" font-size="13" fill="#1e293b" font-family="monospace">PK  dept_id</text>
      <text x="60" y="130" font-size="13" fill="#1e293b" font-family="monospace">    dept_name</text>
      <text x="60" y="150" font-size="13" fill="#1e293b" font-family="monospace">    location</text>
      
      <!-- Employees table -->
      <rect x="440" y="50" width="220" height="140" rx="8" fill="#d1fae5" stroke="#059669" stroke-width="2"/>
      <rect x="440" y="50" width="220" height="35" rx="8" fill="#059669"/>
      <rect x="440" y="77" width="220" height="8" fill="#059669"/>
      <text x="550" y="74" text-anchor="middle" font-size="14" font-weight="bold" fill="white">employees</text>
      <text x="460" y="110" font-size="13" fill="#1e293b" font-family="monospace">PK  emp_id</text>
      <text x="460" y="130" font-size="13" fill="#1e293b" font-family="monospace">FK  dept_id</text>
      <text x="460" y="150" font-size="13" fill="#1e293b" font-family="monospace">    emp_name</text>
      <text x="460" y="170" font-size="13" fill="#1e293b" font-family="monospace">    salary</text>
      
      <!-- Arrow with fork (crow's foot) -->
      <line x1="260" y1="120" x2="420" y2="120" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow2)"/>
      <!-- Crow's foot lines -->
      <line x1="425" y1="110" x2="440" y2="120" stroke="#059669" stroke-width="2"/>
      <line x1="425" y1="130" x2="440" y2="120" stroke="#059669" stroke-width="2"/>
      <text x="345" y="112" text-anchor="middle" font-size="15" font-weight="bold" fill="#059669">1 : N</text>
      
      <!-- Cardinality labels -->
      <text x="268" y="138" font-size="12" fill="#64748b">one</text>
      <text x="410" y="138" font-size="12" fill="#64748b">many</text>
      
      <!-- Note -->
      <text x="350" y="210" text-anchor="middle" font-size="12" fill="#64748b" font-style="italic">No UNIQUE on FK — multiple employees can share one department</text>
    </svg>
    """

    display(SVG(svg_one_to_many))
    print()
    return


@app.cell
def _(SVG, display):
    # ============================================================
    # SVG Diagram: Many-to-Many (N:M)
    # ============================================================
    svg_many_to_many = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 250" width="800" height="250">
      <defs>
        <marker id="arrow3L" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
          <polygon points="0 0, 10 3.5, 0 7" fill="#9333ea"/>
        </marker>
        <marker id="arrow3R" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
          <polygon points="10 0, 0 3.5, 10 7" fill="#9333ea"/>
        </marker>
      </defs>
      
      <!-- Title -->
      <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#1e293b">Many-to-Many (N:M) Relationship</text>
      
      <!-- Students table -->
      <rect x="20" y="55" width="200" height="130" rx="8" fill="#f3e8ff" stroke="#9333ea" stroke-width="2"/>
      <rect x="20" y="55" width="200" height="35" rx="8" fill="#9333ea"/>
      <rect x="20" y="82" width="200" height="8" fill="#9333ea"/>
      <text x="120" y="79" text-anchor="middle" font-size="14" font-weight="bold" fill="white">students</text>
      <text x="40" y="115" font-size="13" fill="#1e293b" font-family="monospace">PK  student_id</text>
      <text x="40" y="135" font-size="13" fill="#1e293b" font-family="monospace">    student_name</text>
      <text x="40" y="155" font-size="13" fill="#1e293b" font-family="monospace">    major</text>
      
      <!-- Enrollments (junction) table -->
      <rect x="280" y="55" width="240" height="150" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
      <rect x="280" y="55" width="240" height="35" rx="8" fill="#d97706"/>
      <rect x="280" y="82" width="240" height="8" fill="#d97706"/>
      <text x="400" y="79" text-anchor="middle" font-size="14" font-weight="bold" fill="white">enrollments (junction)</text>
      <text x="300" y="115" font-size="13" fill="#1e293b" font-family="monospace">PK  enrollment_id</text>
      <text x="300" y="135" font-size="13" fill="#1e293b" font-family="monospace">FK  student_id</text>
      <text x="300" y="155" font-size="13" fill="#1e293b" font-family="monospace">FK  course_id</text>
      <text x="300" y="175" font-size="13" fill="#92400e" font-family="monospace">    grade, semester</text>
      
      <!-- Courses table -->
      <rect x="580" y="55" width="200" height="130" rx="8" fill="#f3e8ff" stroke="#9333ea" stroke-width="2"/>
      <rect x="580" y="55" width="200" height="35" rx="8" fill="#9333ea"/>
      <rect x="580" y="82" width="200" height="8" fill="#9333ea"/>
      <text x="680" y="79" text-anchor="middle" font-size="14" font-weight="bold" fill="white">courses</text>
      <text x="600" y="115" font-size="13" fill="#1e293b" font-family="monospace">PK  course_id</text>
      <text x="600" y="135" font-size="13" fill="#1e293b" font-family="monospace">    course_name</text>
      <text x="600" y="155" font-size="13" fill="#1e293b" font-family="monospace">    credits</text>
      
      <!-- Arrows -->
      <line x1="220" y1="120" x2="270" y2="120" stroke="#9333ea" stroke-width="2.5" marker-end="url(#arrow3L)"/>
      <line x1="580" y1="120" x2="530" y2="120" stroke="#9333ea" stroke-width="2.5" marker-end="url(#arrow3R)"/>
      
      <!-- Labels -->
      <text x="245" y="112" text-anchor="middle" font-size="13" font-weight="bold" fill="#9333ea">1:N</text>
      <text x="555" y="112" text-anchor="middle" font-size="13" font-weight="bold" fill="#9333ea">N:1</text>
      
      <!-- Bottom note -->
      <text x="400" y="230" text-anchor="middle" font-size="12" fill="#64748b" font-style="italic">Junction table decomposes N:M into two 1:N relationships</text>
      <text x="400" y="246" text-anchor="middle" font-size="12" fill="#64748b" font-style="italic">and can carry extra attributes (grade, semester)</text>
    </svg>
    """

    display(SVG(svg_many_to_many))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # 5. Side-by-Side Comparison

    | Feature | 1:1 | 1:N | N:M |
    |:--------|:----|:----|:----|
    | **Example** | Person ↔ Passport | Dept → Employees | Students ↔ Courses |
    | **FK location** | Child table | Child ("many" side) | Junction table |
    | **UNIQUE on FK?** | Yes | No | No (but composite unique often used) |
    | **Junction table needed?** | No | No | **Yes** |
    | **Extra attributes?** | N/A | N/A | Yes (on junction table) |
    | **How many tables?** | 2 | 2 | 3 (two entity + one junction) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # 6. Bonus: Querying Across All Relationships

    Let's run a few more queries to solidify understanding.
    """)
    return


@app.cell
def _(run):
    # BONUS QUERY 1: Find persons who do NOT have a passport (1:1)
    run("""
        SELECT
            p.person_id,
            p.name
        FROM persons p
        WHERE p.person_id NOT IN (
        SELECT person_id
        FROM passports );
    """, "Persons WITHOUT a Passport (anti-join on 1:1)")
    return


@app.cell
def _(run):
    # BONUS QUERY 2: Find the department with the highest average salary (1:N)
    run("""
        SELECT
            d.dept_name,
            ROUND(AVG(e.salary), 2) AS avg_salary
        FROM departments d
        JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
        ORDER BY avg_salary DESC
        LIMIT 1;
    """, "Department with Highest Average Salary (1:N)")
    return


@app.cell
def _(run):
    # BONUS QUERY 3: Find students taking the same courses (N:M self-comparison)
    run("""
        SELECT DISTINCT
            s1.student_name AS student_1,
            s2.student_name AS student_2,
            c.course_name AS shared_course
        FROM enrollments e1
        JOIN enrollments e2 ON e1.course_id = e2.course_id
        AND e1.student_id < e2.student_id
        JOIN students s1 ON e1.student_id = s1.student_id
        JOIN students s2 ON e2.student_id = s2.student_id
        JOIN courses c ON e1.course_id = c.course_id
        ORDER BY shared_course, student_1;
    """, "Student Pairs Sharing a Course (N:M self-join)")
    return


@app.cell
def _(run):
    # BONUS QUERY 4: Comprehensive schema inspection
    # DuckDB's information_schema shows all tables, columns, and constraints

    run("""
        SELECT
            table_name,
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'main'
        ORDER BY table_name, ordinal_position;
    """, "Full Schema: All Tables and Columns")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # 7. Summary

    ## What We Covered

    1. **One-to-One (1:1):** Each person has at most one passport. Enforced by a `UNIQUE` constraint on the foreign key.

    2. **One-to-Many (1:N):** One department has many employees. The foreign key on the "many" side has no `UNIQUE` constraint.

    3. **Many-to-Many (N:M):** Students enroll in many courses, and courses have many students. Implemented via a **junction table** (`enrollments`) that decomposes N:M into two 1:N relationships.

    ## Key Design Principles

    - **Foreign keys** maintain referential integrity — they ensure that every reference points to a valid row.
    - The **UNIQUE constraint** on a foreign key is the difference between 1:1 and 1:N.
    - **Junction tables** are required for N:M and can carry additional relationship attributes.
    - Always think about the relationship from **both directions** when designing your schema.

    ## Further Reading

    - [DuckDB Documentation](https://duckdb.org/docs/)
    - Database normalization (1NF, 2NF, 3NF)
    - Entity-Relationship (ER) diagrams and modeling
    """)
    return


@app.cell
def _(con):
    # Clean up: close the connection
    con.close()
    print("Database connection closed. Tutorial complete!")
    return


if __name__ == "__main__":
    app.run()
