# Capstone Project Specification

## OMIS 105 — Database Management Systems
**Week 9 | Due: Week 10 (presentation)**

---

## Overview

Design, implement, and present a **complete relational database system** for a real-world domain of your choosing. This project integrates all concepts from Weeks 1–8.

---

## Deliverables

| # | Deliverable | Weight | Format |
|---|-------------|--------|--------|
| 1 | ER Diagram | 15% | Image or ASCII in notebook |
| 2 | Normalized Schema (CREATE TABLE) | 15% | SQL in notebook |
| 3 | Sample Data | 10% | CSV files or INSERT statements |
| 4 | 10 SQL Queries | 25% | SQL in notebook with output |
| 5 | Transaction Demo | 10% | Python function in notebook |
| 6 | Views (2+) and Indexes (3+) | 10% | SQL in notebook |
| 7 | Presentation | 15% | 5–8 minutes, live demo |

---

## Requirements

### Database Design
- Minimum **5 tables**
- At least one **1:M** relationship
- At least one **M:M** relationship (with junction table)
- Schema must be in **3NF** (document your normalization check)
- Use appropriate **constraints**: PK, FK, NOT NULL, CHECK, UNIQUE, DEFAULT

### Sample Data
- At least **20 rows** per main entity table
- Data must be **meaningful and realistic** (not "test1", "test2")
- Include variety: different statuses, date ranges, edge cases

### SQL Queries (10 total)
Your queries must demonstrate the following skills:

| Category | Minimum Count |
|----------|--------------|
| Basic SELECT with WHERE, ORDER BY | 2 |
| JOINs (INNER, LEFT, multi-table) | 3 |
| GROUP BY with HAVING or CASE | 2 |
| Window functions or CTEs | 2 |
| Transaction (Python function) | 1 |

Each query must include:
- A comment explaining its **business purpose**
- The **SQL code**
- The **output**

### Views and Indexes
- At least **2 views** with justification
- At least **3 indexes** with justification (explain which queries they help)

### Transaction
- Must be a **multi-step** operation (3+ SQL statements)
- Must include **error handling** (try/except with ROLLBACK)
- Must demonstrate both **success** and **failure** cases

---

## Suggested Domains

| Domain | Key Entities |
|--------|-------------|
| Restaurant Management | Menus, Items, Orders, Tables, Staff, Reservations |
| Fitness Gym | Members, Classes, Trainers, Rooms, Bookings, Payments |
| Music Streaming | Artists, Albums, Songs, Users, Playlists, Listening History |
| Hospital/Clinic | Patients, Doctors, Appointments, Prescriptions, Departments |
| Library System | Books, Authors, Members, Loans, Fines, Branches |
| Airline Booking | Flights, Passengers, Bookings, Aircraft, Airports, Crew |
| Hotel Management | Rooms, Guests, Reservations, Services, Invoices |
| Online Learning | Courses, Students, Instructors, Enrollments, Assignments, Grades |

You may also propose your own domain — clear it with the instructor first.

---

## Presentation Guide (5–8 minutes)

1. **Introduction** (1 min): What is your domain? What problem does your database solve?
2. **ER Diagram** (1 min): Walk through your entities and relationships
3. **Schema Highlights** (1 min): Key tables, interesting constraints
4. **Live Demo** (3–4 min): Run 3–4 of your best queries in Jupyter
5. **Transaction Demo** (1 min): Show success and failure cases
6. **Reflection** (30 sec): What did you learn? What would you do differently?

---

## Grading Rubric

| Criterion | Excellent (A: 90–100%) | Good (B: 80–89%) | Adequate (C: 70–79%) | Needs Work (<70%) |
|-----------|----------------------|------------------|---------------------|-------------------|
| **Design** | 5+ tables, proper keys, FK, 3NF verified, M:M present | 5 tables, minor normalization issues | <5 tables or not normalized | Major design flaws |
| **Data** | 20+ rows, realistic, varied, edge cases | 20 rows, mostly realistic | <20 rows or unrealistic data | Minimal or missing data |
| **Queries** | 10 diverse, complex, well-documented | 10 queries, some basic | <10 or mostly simple | Few or non-functional |
| **Transaction** | Multi-step, error handling, both cases shown | Basic transaction works | Only COMMIT, no error handling | No transaction |
| **Views/Indexes** | Justified, useful, demonstrate understanding | Present but minimal justification | Only 1 of each | Missing |
| **Presentation** | Clear, organized, live demo, within time | Adequate, mostly clear | Disorganized or over time | Confusing or missing |

---

## Submission

- Upload your **Jupyter notebook** (.ipynb) with all code and outputs
- Include any **CSV data files**
- Include your **ER diagram** (image or in notebook)
- Be prepared to **present live** in Week 10

---

## Template

Use the provided `week09_project_template.ipynb` as your starting point.

**Good luck and have fun!**

