"""
generate_db_records.py
======================
Writes db_records.sql (the INSERT statements for db_schema.sql):
500 students, 50 courses, 8,000 grades.

The data is random but repeatable: the seed is fixed, so every run
writes exactly the same file. Change the seed or the settings below
to get different data, then rebuild the database:

    python3 generate_db_records.py
    ./create_duckdb_database.sh

Built-in gaps (used by the LEFT/RIGHT JOIN queries in notebook.py):
  - 5 students never take a course   (NO_COURSES)
  - 3 courses are never taken        (NEVER_TAKEN)
"""
import random
from pathlib import Path

OUT_FILE = Path(__file__).resolve().parent / "db_records.sql"

HEADER = """-- ============================================================
-- db_records.sql -- Sample data for db_schema.sql
--
-- Tables:   
--         students:   500  rows
--         courses      50  rows
--         grades    8,000  rows 
--
--         5 students have never taken any courses
--         3 of the courses have never appeared in the grades table
--
-- Database: DuckDB
--
-- ============================================================
"""

random.seed(105)

COURSES = {
    "BUSINESS": ("BUS", [
        "Principles of Management", "Business Communication", "Marketing Fundamentals",
        "Organizational Behavior", "Operations Management", "Business Law",
        "Strategic Management", "Global Business Strategy", "Negotiation and Leadership",
        "Entrepreneurship and Innovation"]),
    "ENGINEERING": ("ENGR", [
        "Engineering Graphics", "Statics", "Circuits I", "Thermodynamics",
        "Materials Science", "Fluid Mechanics", "Control Systems",
        "Advanced Signal Processing", "Finite Element Analysis", "Robotics"]),
    "MATH": ("MATH", [
        "Calculus I", "Calculus II", "Linear Algebra", "Probability",
        "Discrete Mathematics", "Differential Equations", "Real Analysis",
        "Numerical Methods", "Stochastic Processes", "Optimization Theory"]),
    "COMPUTER-SCIENCE": ("CSCI", [
        "Introduction to Programming", "Data Structures", "Database Systems",
        "Computer Networks", "Operating Systems", "Web Development",
        "Algorithms", "Machine Learning", "Distributed Systems", "Cloud Computing"]),
    "FINANCE": ("FIN", [
        "Financial Accounting", "Corporate Finance", "Investments",
        "Money and Banking", "Personal Finance", "International Finance",
        "Financial Modeling", "Derivatives and Risk", "Portfolio Management",
        "Fintech and Digital Payments"]),
}

# 6 undergraduate (101..106) + 4 graduate (201..204) per department
courses = []          # (course_id, name, level, credits, dept)
for dept, (prefix, names) in COURSES.items():
    for i, name in enumerate(names):
        if i < 6:
            cid, level, credits = f"{prefix}{101 + i}", "undergraduate", random.choice([3, 4, 4, 5])
        else:
            cid, level, credits = f"{prefix}{201 + i - 6}", "graduate", random.choice([2, 3, 3, 4])
        courses.append((cid, name, level, credits, dept))

NEVER_TAKEN = {"ENGR204", "MATH204", "FIN204"}

NAMES = {
    "USA": (["James", "Michael", "David", "Ryan", "Tyler", "Ethan", "Noah", "Logan"],
            ["Emily", "Sarah", "Jessica", "Ashley", "Olivia", "Madison", "Hannah", "Grace"],
            ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson",
             "Anderson", "Taylor", "Moore", "Clark"]),
    "CANADA": (["Liam", "Lucas", "Owen", "Nathan"], ["Chloe", "Emma", "Ava", "Zoe"],
               ["Tremblay", "Gagnon", "Roy", "Campbell", "MacDonald", "Martin"]),
    "CHINA": (["Wei", "Jun", "Hao", "Lei", "Ming", "Jian", "Tao", "Yang"],
              ["Mei", "Li", "Xin", "Ying", "Lan", "Hui", "Fang", "Jing"],
              ["Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou"]),
    "INDIA": (["Arjun", "Rahul", "Vikram", "Rohan", "Aditya", "Karan", "Sanjay", "Amit"],
              ["Priya", "Ananya", "Divya", "Kavya", "Neha", "Pooja", "Shreya", "Meera"],
              ["Sharma", "Patel", "Singh", "Kumar", "Gupta", "Reddy", "Iyer", "Nair", "Rao", "Mehta"]),
    "GERMANY": (["Lukas", "Felix", "Jonas", "Max"], ["Lena", "Anna", "Hannah", "Laura"],
                ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Becker"]),
    "MEXICO": (["Diego", "Carlos", "Luis", "Mateo"], ["Sofia", "Valeria", "Camila", "Lucia"],
               ["Hernandez", "Garcia", "Martinez", "Lopez", "Gonzalez", "Ramirez"]),
    "ITALY": (["Marco", "Luca", "Matteo", "Giovanni"], ["Giulia", "Chiara", "Francesca", "Sara"],
              ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano"]),
}
COUNTRY_W = {"USA": 34, "CHINA": 23, "INDIA": 23, "CANADA": 6, "MEXICO": 6, "GERMANY": 5, "ITALY": 3}
MAJOR_W = {"BUSINESS": 26, "COMPUTER-SCIENCE": 26, "FINANCE": 18, "ENGINEERING": 16, "MATH": 14}

students = []   # (id, first, last, major, gender, country)
for sid in range(1, 501):
    country = random.choices(list(COUNTRY_W), list(COUNTRY_W.values()))[0]
    major = random.choices(list(MAJOR_W), list(MAJOR_W.values()))[0]
    gender = random.choices(["MALE", "FEMALE", "NA"], [48, 48, 4])[0]
    male, female, last = NAMES[country]
    pool = male if gender == "MALE" else female if gender == "FEMALE" else male + female
    students.append((sid, random.choice(pool), random.choice(last), major, gender, country))

NO_COURSES = {37, 142, 256, 391, 478}
# give the 5 "no courses" students distinct, easy-to-spot names
FIXED = {142: ("Priya", "Sharma", "FEMALE", "INDIA"), 256: ("Lukas", "Weber", "MALE", "GERMANY"),
         391: ("Emily", "Clark", "FEMALE", "USA"), 478: ("Carlos", "Lopez", "MALE", "MEXICO")}
students = [(s[0], *FIXED[s[0]][:2], s[3], *FIXED[s[0]][2:]) if s[0] in FIXED else s
            for s in students]

# ---- grades: 8,000 rows over 495 students and 47 courses -----------------
active = [s for s in students if s[0] not in NO_COURSES]
offered = [c for c in courses if c[0] not in NEVER_TAKEN]
TOTAL = 8000

loads = [random.randint(8, 24) for _ in active]
while sum(loads) != TOTAL:          # nudge to exactly 8,000
    i = random.randrange(len(loads))
    if sum(loads) > TOTAL and loads[i] > 6:
        loads[i] -= 1
    elif sum(loads) < TOTAL and loads[i] < 28:
        loads[i] += 1

# graduate courses are a little harder; some courses are known as tough
TOUGH = {"MATH105", "ENGR104", "FIN203", "MATH203"}
EASY = {"BUS102", "FIN105", "CSCI106", "BUS105"}

def draw_grade(cid, level):
    w = [30, 36, 21, 8, 5]
    if level == "graduate":
        w = [36, 38, 17, 6, 3]
    if cid in TOUGH:
        w = [15, 28, 30, 15, 12]
    if cid in EASY:
        w = [50, 32, 12, 4, 2]
    return random.choices("ABCDF", w)[0]

rows = []
for s, k in zip(active, loads):
    sid, major = s[0], s[3]
    weights = [6 if c[4] == major else 1 for c in offered]
    chosen = set()
    while len(chosen) < k:
        chosen.add(random.choices(range(len(offered)), weights)[0])
    start = random.randint(2021, 2024)
    for idx in chosen:
        cid, _, level, _, _ = offered[idx]
        lo = start + (1 if level == "graduate" else 0)
        year = min(2025, random.randint(lo, min(2025, lo + 2)))
        rows.append((sid, cid, year, draw_grade(cid, level)))

# make sure every offered course appears at least once
taken = {r[1] for r in rows}
assert taken == {c[0] for c in offered}, set(c[0] for c in offered) - taken
rows.sort(key=lambda r: (r[2], r[0], r[1]))
assert len(rows) == TOTAL

def q(s):
    return "'" + s.replace("'", "''") + "'"

out = [HEADER]
out.append("\n-- ------------------------------------------------------------\n-- courses: 50 rows (10 per department; 6 undergraduate + 4 graduate)\n-- Never taken: " + ", ".join(sorted(NEVER_TAKEN)) + "\n-- ------------------------------------------------------------\n")
out.append("INSERT INTO courses (course_id, course_name, course_level, num_of_credits) VALUES\n")
out.append(",\n".join(f"   ({q(c[0])}, {q(c[1])}, {q(c[2])}, {c[3]})" for c in courses) + ";\n")

out.append("\n-- ------------------------------------------------------------\n-- students: 500 rows\n-- No courses taken: student_id " + ", ".join(map(str, sorted(NO_COURSES))) + "\n-- ------------------------------------------------------------\n")
out.append("INSERT INTO students (student_id, first_name, last_name, major, gender, country) VALUES\n")
out.append(",\n".join(f"   ({s[0]}, {q(s[1])}, {q(s[2])}, {q(s[3])}, {q(s[4])}, {q(s[5])})" for s in students) + ";\n")

out.append("\n-- ------------------------------------------------------------\n-- grades: 8,000 rows (years 2021-2025)\n-- ------------------------------------------------------------\n")
CHUNK = 1000
for i in range(0, TOTAL, CHUNK):
    out.append("INSERT INTO grades (grade_id, student_id, course_id, year, grade) VALUES\n")
    out.append(",\n".join(f"   ({i + j + 1}, {r[0]}, {q(r[1])}, {r[2]}, {q(r[3])})"
                          for j, r in enumerate(rows[i:i + CHUNK])) + ";\n\n")

OUT_FILE.write_text("".join(out).rstrip() + "\n", encoding="utf-8")
print(f"Wrote {OUT_FILE} ({len(students)} students, {len(courses)} courses, {len(rows):,} grades)")
