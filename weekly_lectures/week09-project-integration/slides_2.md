---
marp: true
theme: default
paginate: true
header: "OMIS 105 – Database Management Systems"
footer: "Week 9: Capstone Project"
---

# OMIS 105: Database Management Systems
## Week 9 — Capstone Project
### Design, Build, and Present a Complete Database

---

# This Week's Goals

1. Understand the capstone project requirements
2. Review the full database development lifecycle
3. Work through a project methodology
4. Design and implement your own database system
5. Prepare a presentation of your work

---

# The Capstone Project

**Design and implement a complete database system** for a real-world scenario of your choosing.

This project integrates everything from Weeks 1–8:
- Relational design & ER diagrams
- Normalization (3NF/BCNF)
- SQL (DDL + DML + complex queries)
- Performance considerations
- Transaction safety

---

# Session 1: Project Requirements & Methodology

---

# Project Deliverables

| Deliverable | Weight |
|------------|--------|
| ER Diagram | 15% |
| Normalized Schema (DDL) | 15% |
| Sample Data (CSV or INSERT) | 10% |
| SQL Queries (10 meaningful queries) | 25% |
| Transaction Demo | 10% |
| Views and Indexes | 10% |
| Presentation / Write-up | 15% |

---

# Project Timeline

| Session | Activity |
|---------|----------|
| Session 1 (Today) | Topic selection, requirements, ER design |
| Session 2 (Today) | Schema creation, data loading, queries |
| Week 10 Session 1 | Presentations (Group A) |
| Week 10 Session 2 | Presentations (Group B) |

---

# Choosing a Domain

Pick something you find interesting! Examples:

| Domain | Entities |
|--------|----------|
| Restaurant | Menus, Orders, Tables, Staff, Reservations |
| Fitness Gym | Members, Classes, Trainers, Equipment, Bookings |
| Music Streaming | Artists, Albums, Songs, Users, Playlists |
| Hospital | Patients, Doctors, Appointments, Prescriptions |
| University | Students, Courses, Professors, Enrollments |
| Library | Books, Authors, Members, Loans, Fines |
| Airline | Flights, Passengers, Bookings, Aircraft, Crew |
| Social Media | Users, Posts, Comments, Likes, Followers |

---

# Domain Requirements

Your database must include:
- **Minimum 5 tables** (more is fine)
- At least one **1:M** relationship
- At least one **M:M** relationship (with junction table)
- At least **20 rows** of sample data per main table
- **Meaningful data** (not random gibberish)

---

# Step 1: Requirements Analysis

Before designing, answer these questions:

1. **What is the purpose** of this database?
2. **Who are the users?** What will they do?
3. **What data** do we need to store?
4. **What questions** should the database answer?
5. **What business rules** must be enforced?

---

# Example: Fitness Gym

1. **Purpose**: Manage members, classes, and bookings
2. **Users**: Front desk staff, trainers, managers
3. **Data**: Members, trainers, classes, rooms, bookings, payments
4. **Questions**: Who is booked for yoga tomorrow? How much revenue this month?
5. **Rules**: Max class capacity, one trainer per class, members must be active

---

# Step 2: Conceptual Design (ER Diagram)

For each entity, identify:
- **Attributes** (columns)
- **Primary key**
- **Relationships** to other entities
- **Cardinality** (1:1, 1:M, M:M)

Draw the ER diagram using Crow's Foot notation.

---

# ER Diagram Checklist

- [ ] All entities identified and named
- [ ] Primary keys marked for each entity
- [ ] All attributes listed
- [ ] Relationships drawn with cardinality
- [ ] M:M relationships have junction tables
- [ ] No redundant relationships
- [ ] Diagram is readable and organized

---

# Step 3: Logical Design (Schema)

Convert your ER diagram into CREATE TABLE statements:

```sql
CREATE TABLE members (
    member_id    INTEGER PRIMARY KEY,
    first_name   VARCHAR NOT NULL,
    last_name    VARCHAR NOT NULL,
    email        VARCHAR UNIQUE NOT NULL,
    phone        VARCHAR,
    join_date    DATE DEFAULT CURRENT_DATE,
    status       VARCHAR CHECK (status IN ('active','inactive','suspended'))
);
```

---

# Schema Checklist

- [ ] Every table has a PRIMARY KEY
- [ ] Foreign keys reference valid tables
- [ ] NOT NULL on required fields
- [ ] CHECK constraints for business rules
- [ ] UNIQUE constraints where appropriate
- [ ] DEFAULT values where sensible
- [ ] Data types are appropriate

---

# Step 4: Normalization Check

Verify your schema is in **3NF**:

1. **1NF**: All atomic values? No repeating groups?
2. **2NF**: No partial dependencies? (Check composite keys)
3. **3NF**: No transitive dependencies?

Document any intentional denormalization and justify it.

---

# Step 5: Sample Data

Create realistic data for each table:
- Minimum **20 rows** for main entity tables
- Enough junction table data to demonstrate M:M
- **Meaningful** values (real-sounding names, valid dates, etc.)
- Include edge cases (zero values, NULLs where allowed)

```sql
INSERT INTO members VALUES
(1, 'Alice', 'Johnson', 'alice@email.com', '555-0101', '2023-06-15', 'active'),
(2, 'Bob', 'Smith', 'bob@email.com', '555-0102', '2023-08-20', 'active'),
...
```

---

# Session 2: Implementation

---

# Step 6: SQL Queries (10 Required)

Your queries should demonstrate mastery:

| Category | Count | Examples |
|----------|-------|---------|
| Basic SELECT with filtering | 2 | WHERE, ORDER BY, LIMIT |
| JOINs (multi-table) | 3 | INNER, LEFT, 3+ table joins |
| Aggregation (GROUP BY) | 2 | With HAVING, CASE |
| Advanced (Window/CTE) | 2 | Window functions, CTEs |
| Transaction | 1 | Multi-step with error handling |

---

# Query Examples: Fitness Gym

```sql
-- Q1: Active members who joined this year
SELECT first_name, last_name, join_date
FROM members
WHERE status = 'active'
  AND EXTRACT(YEAR FROM join_date) = 2024
ORDER BY join_date;

-- Q2: Revenue by class type this month
WITH class_revenue AS (
    SELECT ct.type_name,
           SUM(p.amount) AS revenue
    FROM bookings b
    JOIN classes c ON b.class_id = c.class_id
    JOIN class_types ct ON c.type_id = ct.type_id
    JOIN payments p ON b.booking_id = p.booking_id
    WHERE EXTRACT(MONTH FROM p.payment_date) = EXTRACT(MONTH FROM CURRENT_DATE)
    GROUP BY ct.type_name
)
SELECT type_name, revenue,
       ROUND(revenue / SUM(revenue) OVER () * 100, 1) AS pct
FROM class_revenue
ORDER BY revenue DESC;
```

---

# Step 7: Views

Create at least **2 views**:

```sql
-- View 1: Member dashboard
CREATE VIEW member_dashboard AS
SELECT m.first_name || ' ' || m.last_name AS name,
       m.status,
       COUNT(b.booking_id) AS total_bookings,
       MAX(c.class_date) AS last_class
FROM members m
LEFT JOIN bookings b ON m.member_id = b.member_id
LEFT JOIN classes c ON b.class_id = c.class_id
GROUP BY m.member_id, m.first_name, m.last_name, m.status;

-- View 2: Class utilization
CREATE VIEW class_utilization AS ...
```

---

# Step 8: Indexes

Create at least **3 indexes** with justification:

```sql
-- Index on frequently filtered column
CREATE INDEX idx_members_status ON members(status);
-- Justification: Front desk frequently filters by active/inactive

-- Composite index for date-range queries
CREATE INDEX idx_classes_date ON classes(class_date, type_id);
-- Justification: Schedule lookups filter by date and type

-- Index for JOIN performance
CREATE INDEX idx_bookings_member ON bookings(member_id);
-- Justification: Member history queries join on this column
```

---

# Step 9: Transaction Demo

Demonstrate a meaningful transaction:

```python
def book_class(con, member_id, class_id):
    try:
        con.execute("BEGIN")
        # Check member is active
        # Check class has capacity
        # Create booking
        # Create payment
        # Update class enrollment count
        con.execute("COMMIT")
    except Exception as e:
        con.execute("ROLLBACK")
        print(f"Booking failed: {e}")
```

---

# Step 10: Presentation

**5–8 minute presentation** covering:

1. **Domain** — what problem are you solving?
2. **ER Diagram** — show your design
3. **Schema** — highlight key tables and constraints
4. **Demo** — run 3–4 of your best queries live
5. **Transaction** — demonstrate your transaction
6. **Lessons learned** — what was challenging?

---

# Presentation Tips

- Start with the **business problem**, not technical details
- Show the ER diagram **early** to give context
- **Run queries live** in a Jupyter notebook
- Explain **why** you made design choices
- Keep it within **8 minutes** — practice timing!

---

# Grading Criteria

| Criterion | Excellent (A) | Good (B) | Needs Work (C) |
|-----------|--------------|----------|----------------|
| Design | 5+ tables, proper keys, 3NF | 5 tables, minor issues | <5 tables or not normalized |
| SQL | 10 diverse, complex queries | 10 queries, some basic | <10 or mostly simple |
| Transaction | Multi-step with error handling | Basic BEGIN/COMMIT | No transaction |
| Presentation | Clear, well-organized, live demo | Adequate | Confusing or incomplete |

---

# Common Mistakes to Avoid

1. **Too few tables** — aim for 5–8 entities
2. **No junction table** — every project needs at least one M:M
3. **Unrealistic data** — "test1", "test2" is not meaningful data
4. **All simple queries** — show JOINs, CTEs, window functions
5. **No error handling** — transactions should handle failures
6. **No indexes** — show you considered performance
7. **Over-scoping** — better to do 5 tables well than 15 badly

---

# Getting Help

- Office hours: [your schedule]
- Use the ShopSmart project as a **reference** for structure
- Start with the ER diagram — everything flows from good design
- Don't wait until the last minute!

---

# Suggested Approach: Today's Sessions

**Session 1** (2 hours):
- Choose domain (15 min)
- Requirements analysis (15 min)
- ER diagram (45 min)
- CREATE TABLE statements (45 min)

**Session 2** (2 hours):
- Load sample data (30 min)
- Write 10 queries (60 min)
- Create views, indexes, transaction (30 min)

---

# Summary

- The capstone integrates **everything** from Weeks 1–8
- Choose a domain you care about
- Follow the design methodology step by step
- Demonstrate a variety of SQL skills
- Include transactions with error handling
- Present your work clearly and concisely

---

# Project Due

**Presentations in Week 10**

Good luck, and have fun with your projects!

---

# Questions?

Thank you!

