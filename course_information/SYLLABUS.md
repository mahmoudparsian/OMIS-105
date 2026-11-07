# OMIS 105 — Introduction to Database Management Systems

[← Course home](../README.md) · [Course information](README.md) · **Syllabus**

**Santa Clara University · Leavey School of Business · Department of Information Systems and Analytics**<br>
**Fall 2026 · 10 weeks, 20 sessions**

This syllabus collects, in one document, what the course repository
publishes in its separate pages. If this page and a linked page ever
disagree, the linked page in [`course_information/`](./) is the one that
applies, and the instructor will correct this page.

---

## 1. Course Information

| | |
|---|---|
| **Course** | OMIS 105 — Introduction to Database Management Systems |
| **Units** | *See the SCU course listing* <!-- TODO(syllabus): units --> |
| **Quarter** | Fall 2026 |
| **Format** | 10 weeks · 20 sessions (2 per week) · 100 minutes per session |
| **Meetings** | Tuesday and Thursday — section 1: 12:10–1:50 pm; section 2: 2:00–3:40 pm (Pacific Time) |
| **First / last class** | *See Camino* <!-- TODO(syllabus): first and last class dates --> |
| **Classroom** | *See Camino* <!-- TODO(syllabus): room --> |
| **Prerequisite** | [OMIS 30 — Introduction to Programming](https://www.scu.edu/business/isa/academics/courses/#collapseOMIS_30) |
| **Learning management system** | Camino (Canvas) — announcements, Discussions, exams |
| **Course materials** | Course repository: <https://github.com/mahmoudparsian/OMIS-105> — or one ZIP per week ([`DOWNLOADING_COURSE_FILES.md`](DOWNLOADING_COURSE_FILES.md)) |

### Instructor

| | |
|---|---|
| **Instructor** | [Dr. Mahmoud Parsian](https://www.scu.edu/business/isa/faculty/parsian/), Assistant Teaching Professor ([`INSTRUCTOR.md`](INSTRUCTOR.md)) |
| **Email** | [mparsian@scu.edu](mailto:mparsian@scu.edu) |
| **Office hours** | Mondays and Wednesdays, 4:15–5:00 pm Pacific Time |
| **Where** | In person at Lucas Hall, Room 316U, or on Zoom (link in [`QUESTIONS_and_OFFICE_HOURS.md`](QUESTIONS_and_OFFICE_HOURS.md)) |
| **First / last office hour** | Wednesday, September 23, 2026 / Wednesday, December 2, 2026 |

---

## 2. Course Description

> You will learn the fundamentals of modern relational data management.
> Topics include SQL, schema design, data modeling, querying data with SQL,
> database applications, and transactions. Through lectures, hands-on labs,
> and assignments, you will discover how real-world database systems work,
> the principles behind them, and how they shape the way organizations store,
> retrieve, and analyze information every day.

The course covers the core issues in databases and database management
systems (DBMS). Students acquire technical and managerial skills in
planning, analysis, design, implementation, and maintenance of databases,
with hands-on training in relational database design, normalization, SQL,
and database implementation. Use of a DBMS — **DuckDB** — is required; it
runs inside Python with no server to install.

**Audience:** undergraduate students in the
[Department of Information Systems and Analytics](https://www.scu.edu/business/isa/academics/courses/).
No prior experience with SQL or databases is needed.

---

## 3. Learning Outcomes

By the end of this course, students will be able to:

1. **Design** a normalized relational database from business requirements.
2. **Write** complex SQL queries to extract business insights.
3. **Rank** and compare rows with window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`).
4. **Manage** data integrity through transactions and constraints.
5. **Answer** multi-step business questions with joins and subqueries.
6. **Communicate** database designs using ER diagrams.

---

## 4. Course Schedule

Two sessions per week. Each session is a lecture and live demo, then an
in-class lab (posted after about 45 minutes of lecture).

| Week | Topic | Key SQL concepts |
|:---:|---|---|
| 1 | Database Foundations | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `LIKE`, `DISTINCT` |
| 2 | Relational Modeling | `GROUP BY`, `HAVING`, multi-table schemas |
| 3 | SQL Basics | `CASE`, string functions, `UPPER`, `YEAR`, computed columns |
| 4 | SQL Aggregation | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `INNER JOIN`, `LEFT JOIN` |
| 5 | SQL Joins | Multi-table `JOIN`, `LEFT JOIN`, `IS NULL`, `COALESCE` |
| 6 | Joins II | `INNER` / `LEFT` / `RIGHT JOIN` practice, finding what is missing, self-joins, 3+ tables |
| 7 | Subqueries | Scalar subqueries, `IN` / `NOT IN` (and the `NULL` trap), `EXISTS`, subqueries in `FROM`, correlated subqueries, CTEs |
| 8 | Database Design | Normalization (1NF, 2NF, 3NF), decomposition |
| 9 | Ranking Functions | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `PARTITION BY`, filtering a rank with a CTE |
| 10 | Transactions & ACID | `BEGIN`, `COMMIT`, `ROLLBACK`, `CHECK`, `NOT NULL` |
| Bonus | *Optional:* Project Integration · Review & Modern Data · Query Performance | See [`weekly_lectures/bonus/`](../weekly_lectures/bonus) |

| Exam | Date and time | Where |
|---|---|---|
| **Midterm Exam** | Thursday, October 22, 2026, in class | Your classroom |
| **Final Exam** — 12:10–1:50 pm section | Tuesday, December 8, 2026, 1:30–4:30 pm | 129 Vari Hall |
| **Final Exam** — 2:00–3:40 pm section | Thursday, December 10, 2026, 1:30–4:30 pm | 129 Vari Hall |

Source: [`ASSIGNMENTS_and_GRADING.md`](ASSIGNMENTS_and_GRADING.md) §2 and
[`FINAL_EXAM.md`](FINAL_EXAM.md); the university's
[Fall 2026 final exam schedule](https://www.scu.edu/media/offices/registrar/2026---2027-Final-Exam-Schedule-1.pdf).

The topic table is the course's authoritative list (repository
[`README.md`](../README.md) §18); the slide decks in
[`weekly_lectures/`](../weekly_lectures) and the
[10-week outline](../outline-10-weeks) follow a somewhat slower pacing, and
where they disagree, the table applies. Each week's lectures and review
notebooks are in [`weekly_lectures/`](../weekly_lectures) and
[`weekly_reviews/`](../weekly_reviews).

---

## 5. Required Materials

**No textbook is required.** All course materials — lectures, labs,
installation guides, reference documents — are in the course repository.
Optional reading: *DuckDB in Action*, in the [`books/`](../books) folder
([`REQUIRED_BOOK.md`](REQUIRED_BOOK.md)).

**A laptop at every session** (fully charged, with its charger): every
session includes an in-class lab. A dead battery, a forgotten charger, or
software installed incorrectly is not an excused reason to miss a lab
([`LAPTOP.md`](LAPTOP.md)).

**Software** — install before the first lab, following the step-by-step
guide for macOS or Windows in
[`software_installation/`](../software_installation/README.md):

| Tool | Used for |
|---|---|
| Python 3 | Runs the notebooks |
| DuckDB | The course's SQL database |
| Marimo | Reactive Python notebooks — every lab is a Marimo notebook |
| Pandas, Matplotlib | Query results as data frames, and charts |
| qStudio | Desktop SQL editor |
| [Respondus LockDown Browser](https://download.respondus.com/lockdown/download.php?ID=597745928) | **Midterm and Final Exam** — install it as soon as possible |

---

## 6. Assessment and Grading

| Component | Points |
|---|---:|
| 20 in-class labs — one per class session, 30 points each | 600 |
| Midterm Exam — in class, closed book, LockDown Browser | 200 |
| Final Exam — in class, closed book, LockDown Browser | 200 |
| **Total** | **1,000** |

### Labs

- One lab per class session (20 labs). Each lab is a Marimo notebook
  (`.py`) — open it in Marimo, complete the exercises, and run all cells.
- The lab is **started, completed, and submitted during the class session**
  in which it is assigned.
- **Lowest lab replaced:** the lowest lab score is replaced by the average
  of the other 19 lab scores, so labs still total 600 points.
- Clear SQL logic and problem-solving approach are graded more heavily than
  minor formatting or syntax issues.
- Each lab (with blanks) and its answers are posted in
  [`LABS/`](../LABS/README.md) after class.

### Exams

Both exams are **closed book, closed notes, closed software, and closed
Internet**, and are taken in the **Respondus LockDown Browser** — install it
as soon as possible. Dates: Section 4.

### Letter grades

Total points out of 1,000; fractional totals are rounded to the nearest
whole point first (939.5 → 940 → A; 939.4 → 939 → A−).

| Letter | Points | Letter | Points | Letter | Points |
|:---:|---|:---:|---|:---:|---|
| A | 940 – 1,000 | B− | 800 – 829 | D+ | 670 – 699 |
| A− | 900 – 939 | C+ | 770 – 799 | D | 630 – 669 |
| B+ | 870 – 899 | C | 730 – 769 | D− | 600 – 629 |
| B | 830 – 869 | C− | 700 – 729 | F | below 600 |

Full policy: [`ASSIGNMENTS_and_GRADING.md`](ASSIGNMENTS_and_GRADING.md).

---

## 7. Lab Submission

| Item | Rule |
|---|---|
| **When** | Before the end of the class session in which the lab is assigned |
| **File name** | `week##_lab_##_firstname_lastname.py`, all lower case — e.g. Jane Smith, Week 1: `week01_lab_01_jane_smith.py` (Tuesday) and `week01_lab_02_jane_smith.py` (Thursday) |
| **Late or incomplete** | May receive reduced credit unless otherwise approved by the instructor |

Full rules: [`LAB-IN-CLASS-POLICY.md`](LAB-IN-CLASS-POLICY.md).

---

## 8. Attendance

**Attendance is mandatory.** Each in-class lab must be completed and
submitted during the class session in which it is assigned. If you are
absent, you receive 0 on that lab (30 points); a missed lab cannot be made
up, because the lab environment and instructor support are only available
during class. The "lowest lab replaced" policy absorbs one missed lab.
Details: [`CLASS_ATTENDANCE.md`](CLASS_ATTENDANCE.md).

---

## 9. Accessibility and Accommodations

If you have a documented disability for which accommodations may be
required in this class, contact the **Office of Accessible Education
(OAE)** — <https://www.scu.edu/oae/> — as early as possible to arrange
accommodations, and share your accommodation letter with the instructor.

---

## 10. Academic Integrity and Conduct

- **Your own work (NO-COPY-PASTE).** You may use any appropriate resources
  to help you understand and complete your labs, but the work you submit
  must reflect your own understanding and effort. You may discuss concepts
  during class; copying another student's notebook or submitting duplicated
  work is not permitted.
- **SCU Academic Integrity:** <https://www.scu.edu/academic-integrity/> —
  the university's pledge, policy, and resources.
- **Classroom conduct:** respect, resourcefulness, honesty, and constructive
  feedback — see [`ACADEMIC_CONDUCT.md`](ACADEMIC_CONDUCT.md).
- **Discrimination, harassment, and sexual misconduct:** Santa Clara
  University does not tolerate them. Information, reporting options, and
  support: <https://www.scu.edu/title-ix/>.

---

## 11. Getting Help

| Need | Where |
|---|---|
| A question about course content | Ask in class, come to office hours, post on **Camino Discussions** (students, the TA, and the instructor respond), or [email the instructor](mailto:mparsian@scu.edu) |
| Installing the course software | [`software_installation/`](../software_installation/README.md) |
| LockDown Browser or other SCU technology | SCU Technology Help: (408) 554-5700, or a [Computing Support Request](https://help.scu.edu/TDClient/111/Portal/Home/) |

---

## 12. Course Documents

| Document | Contents |
|---|---|
| [`ASSIGNMENTS_and_GRADING.md`](ASSIGNMENTS_and_GRADING.md) | Grading, exam dates, course policies, letter grades |
| [`LAB-IN-CLASS-POLICY.md`](LAB-IN-CLASS-POLICY.md) | How the in-class labs work, and file naming |
| [`CLASS_ATTENDANCE.md`](CLASS_ATTENDANCE.md) | Attendance |
| [`FINAL_EXAM.md`](FINAL_EXAM.md) | Final Exam dates, times, and room |
| [`QUESTIONS_and_OFFICE_HOURS.md`](QUESTIONS_and_OFFICE_HOURS.md) | Office hours and how to ask questions |
| [`LAPTOP.md`](LAPTOP.md) | Laptop requirement |
| [`REQUIRED_BOOK.md`](REQUIRED_BOOK.md) | Course materials and the optional book |
| [`ACADEMIC_CONDUCT.md`](ACADEMIC_CONDUCT.md) | Classroom conduct |
| [`DOWNLOADING_COURSE_FILES.md`](DOWNLOADING_COURSE_FILES.md) | One ZIP per week (no git needed) |
| [`outline-10-weeks/`](../outline-10-weeks) | The 10-week course outline |

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
