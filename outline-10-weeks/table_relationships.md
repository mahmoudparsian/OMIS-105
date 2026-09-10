# Table Relationships

This document explains the three primary types of relationships between
tables in a relational database, with DuckDB SQL examples for each:

- **1-1 (One-to-One)**
- **1-M (One-to-Many)**
- **M-M (Many-to-Many)**

Every example was run against DuckDB 1.5.5 to confirm it works as written.

## Table of Contents

- [Overview](#overview)
- [1. One-to-One (1-1) Relationship](#1-one-to-one-1-1-relationship)
  - [1.1 Schema and Sample Data](#11-schema-and-sample-data)
  - [1.2 Querying a One-to-One Relationship](#12-querying-a-one-to-one-relationship)
  - [1.3 Aggregation in a One-to-One Relationship](#13-aggregation-in-a-one-to-one-relationship)
- [2. One-to-Many (1-M) Relationship](#2-one-to-many-1-m-relationship)
  - [2.1 Schema and Sample Data](#21-schema-and-sample-data)
  - [2.2 Querying a One-to-Many Relationship](#22-querying-a-one-to-many-relationship)
  - [2.3 Aggregation in a One-to-Many Relationship](#23-aggregation-in-a-one-to-many-relationship)
- [3. Many-to-Many (M-M) Relationship](#3-many-to-many-m-m-relationship)
  - [3.1 Schema and Sample Data](#31-schema-and-sample-data)
  - [3.2 Querying a Many-to-Many Relationship](#32-querying-a-many-to-many-relationship)
  - [3.3 Aggregation in a Many-to-Many Relationship](#33-aggregation-in-a-many-to-many-relationship)
- [Summary Comparison](#summary-comparison)

## Overview

The table below is a quick preview; each relationship is explained in
full, with schema, sample data, and queries, in its own section.

| Relationship | Junction table needed? | Real-world example |
|---|---|---|
| 1-1 | No | A `User` has exactly one `User Profile` |
| 1-M | No | A `Customer` places many `Orders` |
| M-M | Yes | A `Student` enrolls in many `Courses`, and a `Course` has many `Students` |

---

## 1. One-to-One (1-1) Relationship

In a One-to-One relationship, a record in Table A can align with only one
record in Table B, and vice versa. This is often used to split a large
table for performance or security reasons (e.g., isolating sensitive data).

Real-world Example: A User has exactly one User Profile.

### 1.1 Schema and Sample Data

* Table Definitions

```sql
-- Create the parent table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR NOT NULL,
    email VARCHAR NOT NULL
);
```

```sql
-- Create the child table with a
-- UNIQUE foreign key constraint
CREATE TABLE user_profiles (
    profile_id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(user_id),
    biography TEXT,
    birth_date DATE
);
```

* Table Populations

```sql
-- Insert sample data
INSERT INTO users VALUES
    (1, 'alice_dev', 'alice@example.com'),
    (2, 'jane_700', 'jane@yahoo.com');

INSERT INTO user_profiles VALUES
    (101, 1, 'Software Engineer from NY', '1992-05-12'),
    (102, 2, 'AI Expert', '2000-04-17');
```

### 1.2 Querying a One-to-One Relationship

To get a complete view of a user alongside their
profile, we use an INNER JOIN. Since it's a 1-1
relationship, this will return exactly one row
per user who has a profile.

```sql
SELECT 
    u.user_id,
    u.username,
    u.email,
    p.biography,
    p.birth_date
FROM users u
INNER JOIN user_profiles p ON u.user_id = p.user_id;
```

### 1.3 Aggregation in a One-to-One Relationship

While 1-1 relationships rarely require standard math
aggregation (like sums), a common practice is calculating
values derived from dates. Here, we calculate each user's
current age based on their profile data using a LEFT JOIN
to ensure we still see users who haven't filled out a profile.

```sql
SELECT 
    u.username,
    p.birth_date,
    -- Extract whole years from the interval AGE() returns
    DATE_PART('year', AGE(CURRENT_DATE, p.birth_date)) AS current_age
FROM users u
LEFT JOIN user_profiles p ON u.user_id = p.user_id;
```

> **Note:** `AGE()` returns an `INTERVAL`, not a struct, so DuckDB
> cannot resolve a `.years` field access on it. `DATE_PART('year', ...)`
> (or the equivalent `EXTRACT(YEAR FROM ...)`) is the correct way to
> pull the year component out of that interval.

---

## 2. One-to-Many (1-M) Relationship

In a One-to-Many (1-M) relationship, a record in
Table A can be associated with multiple records
in Table B, but a record in Table B belongs to
only one record in Table A.

Real-world Example: A Customer can place many Orders,
but each specific order belongs to only one customer.

### 2.1 Schema and Sample Data

* Table Definitions

```sql
-- Create the parent table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR NOT NULL
);

-- Create the child table (many side)
-- referencing the parent
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2)
);
```

* Table Populations

```sql
-- Insert sample data
INSERT INTO customers VALUES (1, 'Bob Smith');

INSERT INTO orders VALUES (5001, 1, '2026-09-01', 45.99);
INSERT INTO orders VALUES (5002, 1, '2026-09-08', 120.00);
```

### 2.2 Querying a One-to-Many Relationship

To see a list of customers and the details of every
order they have placed, we join the customers table
to the orders table. If you want to include customers
who haven't placed any orders yet, you can swap
INNER JOIN for a LEFT JOIN.

```sql
SELECT 
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.order_date,
    o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_name, o.order_date;
```

### 2.3 Aggregation in a One-to-Many Relationship

This query calculates business metrics per customer.
It uses a LEFT JOIN so customers with zero orders are
still listed with 0 values, rather than being excluded
from the results.

```sql
SELECT 
    c.customer_name,
    COUNT(o.order_id) AS total_orders_placed,
    COALESCE(SUM(o.total_amount), 0.00) AS lifetime_spend
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY lifetime_spend DESC;
```

---

## 3. Many-to-Many (M-M) Relationship

In a Many-to-Many relationship, multiple records
in Table A can relate to multiple records in
Table B. Relational databases handle this by
introducing a **third table**, known as a
**junction table (or bridge table)**, which
breaks the relationship down into two separate
One-to-Many relationships.

Real-world Example: A Student can enroll in many
Courses, and a Course can have many Students.

### 3.1 Schema and Sample Data

* Table Definitions

```sql
-- Create the first base table
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    student_name VARCHAR NOT NULL
);

-- Create the second base table
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_title VARCHAR NOT NULL
);

-- Create the junction table linking both together
CREATE TABLE student_courses (
    student_id INTEGER REFERENCES students(student_id),
    course_id INTEGER REFERENCES courses(course_id),
    enrollment_date DATE DEFAULT CURRENT_DATE,
    -- Composite primary key prevents duplicates
    PRIMARY KEY (student_id, course_id) 
);
```

* Table Populations

```sql
-- Insert sample data
INSERT INTO students VALUES (1, 'Charlie'), (2, 'Dana');
INSERT INTO courses VALUES (101, 'Intro to SQL'), (102, 'Data Analytics');

-- Enrollments (Charlie takes both, Dana takes Intro to SQL)
INSERT INTO student_courses (student_id, course_id) VALUES (1, 101);
INSERT INTO student_courses (student_id, course_id) VALUES (1, 102);
INSERT INTO student_courses (student_id, course_id) VALUES (2, 101);
```

### 3.2 Querying a Many-to-Many Relationship

To resolve a many-to-many relationship, you must
join through the junction table (`student_courses`).
This requires two consecutive joins: first from the
students table to the junction table, and then from
the junction table to the courses table.

```sql
SELECT 
    s.student_name,
    c.course_title,
    sc.enrollment_date
FROM students s
INNER JOIN student_courses sc ON s.student_id = sc.student_id
INNER JOIN courses c          ON sc.course_id = c.course_id
ORDER BY s.student_name, c.course_title;
```

### 3.3 Aggregation in a Many-to-Many Relationship

To aggregate across a many-to-many relationship,
you group by the primary entity and run calculations
across the junction table. This query counts how many
classes each student is taking and lists them as a
comma-separated text string.

```sql
SELECT 
    s.student_name,
    COUNT(sc.course_id) AS courses_enrolled,
    -- Merges all course titles for the
    -- student into a single readable list
    STRING_AGG(c.course_title, ', ') AS course_list
FROM students s
LEFT JOIN student_courses sc ON s.student_id = sc.student_id
LEFT JOIN courses c          ON sc.course_id = c.course_id
GROUP BY s.student_id, s.student_name;
```

---

## Summary Comparison

| Relationship | Junction table? | Example | Typical join |
|---|---|---|---|
| **1-1** | No — a `UNIQUE` foreign key on the child table enforces it | User ↔ User Profile | `INNER`/`LEFT JOIN` on the shared key |
| **1-M** | No — a plain foreign key on the "many" side | Customer → Orders | `JOIN` parent to child on the foreign key |
| **M-M** | Yes — a junction table with a composite primary key | Students ↔ Courses | `JOIN` through the junction table twice |

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
