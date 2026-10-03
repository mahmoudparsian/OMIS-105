# Users / Roles / Cities — Join Operations

Practice queries for the `users`, `roles`, and `cities` database in
this folder. They start simple (one table) and build up to
`LEFT JOIN`, `FULL OUTER JOIN`, and "find what is missing" queries.

**How to run them:**

- **DuckDB CLI:** run `./create_duckdb.sh`, then
  `duckdb users_roles_cities.duckdb` and paste a query.
- **Marimo / Python:** load `01_schema.sql` and `02_records.sql` into
  a connection (see the first cells of `notebook.py`), then
  `con.execute("...").fetchdf()`.

Every query below was run against the data in `02_records.sql`.
"Rows" tells you how many rows you should get back.

---

## The Data in One Picture

```
roles (id, role, description)     cities (id, city, population)
       ▲                                  ▲
       │ role_id (may be NULL)            │ city_id (may be NULL)
       └──────────────── users ───────────┘
                  (id, name, role_id, city_id)
```

| Table | Rows | Columns | Values |
|-------|-----:|---------|--------|
| `roles`  | 7  | `id`, `role`, `description` | 1 admin, 2 user, 3 superuser, 4 tester, 5 QA, 6 developer, 7 analyst |
| `cities` | 8  | `id`, `city`, `population` | 1 New York, 2 Philadelphia, 3 San Francisco, 4 Sunnyvale, 5 Cupertino, 6 Detroit, 7 San Jose, 8 Santa Clara |
| `users`  | 36 | `id`, `name`, `role_id`, `city_id` | every name is unique |

`population` is the 2020 U.S. Census count. When you join `users`
to `roles` or `cities`, you can bring `description` and `population`
along — any column of the joined table can go in `SELECT`.

**The gaps (on purpose):**

| Gap | Who |
|-----|-----|
| Roles no user has | `tester`, `QA` |
| Cities no user lives in | `Cupertino`, `Detroit` |
| Users with no role (`role_id IS NULL`) | Diego, Hana, Victor, Zoe, Tom |
| Users with no city (`city_id IS NULL`) | Grace, Ravi, Zoe, Tom |
| Users with no role **and** no city | Zoe, Tom |

Keep these in mind — they are why `INNER JOIN` and `LEFT JOIN` give
different answers in this database.

---

## 1. Basic Queries (no joins)

### B1 — All users, sorted by name

```sql
SELECT id, name, role_id, city_id
FROM   users
ORDER BY name;
```

Rows: 36. Empty cells are `NULL`.

### B2 — Users whose name starts with "J"

```sql
SELECT id, name
FROM   users
WHERE  name LIKE 'J%'
ORDER BY name;
```

Rows: 6 (Jack, James, Jane, Jo, John, Julia).

### B3 — Users who are admins (role 1) and live in San Francisco (city 3)

```sql
SELECT id, name
FROM   users
WHERE  role_id = 1
  AND  city_id = 3
ORDER BY id;
```

Rows: 4 (John, Coco, Rafa, Stan).

### B4 — Users in New York, Philadelphia, or Sunnyvale

```sql
SELECT id, name, city_id
FROM   users
WHERE  city_id IN (1, 2, 4)
ORDER BY city_id, name;
```

Rows: 13.

### B5 — The 5 users with the highest ids

```sql
SELECT id, name
FROM   users
ORDER BY id DESC
LIMIT 5;
```

Rows: 5 (Tom, Zoe, Ravi, Grace, Victor).

---

## 2. Aggregation (no joins)

### A1 — Total users, and how many have a role / a city

```sql
SELECT COUNT(*)       AS total_users,
       COUNT(role_id) AS users_with_role,
       COUNT(city_id) AS users_with_city
FROM   users;
```

Result: 36, 31, 32. `COUNT(column)` skips `NULL`s; `COUNT(*)` does not.

### A2 — Number of users per role_id

```sql
SELECT role_id,
       COUNT(*) AS num_users
FROM   users
GROUP BY role_id
ORDER BY role_id;
```

Rows: 6. `NULL` is its own group (5 users). Role ids 4 and 5 do not
appear at all — you need a join to see them (see J-section).

### A3 — Number of users per city_id, busiest first

```sql
SELECT city_id,
       COUNT(*) AS num_users
FROM   users
GROUP BY city_id
ORDER BY num_users DESC, city_id;
```

Rows: 7. City 3 (San Francisco) has the most users: 10.

### A4 — city_ids with more than 4 users

```sql
SELECT city_id,
       COUNT(*) AS num_users
FROM   users
GROUP BY city_id
HAVING COUNT(*) > 4
ORDER BY num_users DESC;
```

Rows: 4 (city 3: 10; cities 1, 2, and 7: 5 each).
`HAVING` filters **groups**; `WHERE` filters **rows**.

### A5 — How many distinct roles and cities are actually used?

```sql
SELECT COUNT(DISTINCT role_id) AS roles_used,
       COUNT(DISTINCT city_id) AS cities_used
FROM   users;
```

Result: 5 roles used (of 7), 6 cities used (of 8).
`COUNT(DISTINCT ...)` also ignores `NULL`.

---

## 3. Basic Joins

### J1 — Each user with their role name and description (INNER JOIN)

```sql
SELECT u.id, u.name, r.role, r.description
FROM   users u
JOIN   roles r ON u.role_id = r.id
ORDER BY u.id;
```

Rows: 31 — the 5 users with no role are dropped. `r.description`
comes from the `roles` table: one join, and every column of `roles`
is available.

### J2 — Each user with their city name and population (INNER JOIN)

```sql
SELECT u.id, u.name, c.city, c.population
FROM   users u
JOIN   cities c ON u.city_id = c.id
ORDER BY u.id;
```

Rows: 32 — the 4 users with no city are dropped.

### J3 — All developers, with their city id

```sql
SELECT u.name, u.city_id
FROM   users u
JOIN   roles r ON u.role_id = r.id
WHERE  r.role = 'developer'
ORDER BY u.name;
```

Rows: 6. Filtering by the role **name** instead of a magic number
like `6` is the whole point of the join.

### J4 — Users who live in a big city (population over 1 million)

```sql
SELECT u.name, c.city, c.population
FROM   users u
JOIN   cities c ON u.city_id = c.id
WHERE  c.population > 1000000
ORDER BY c.population DESC, u.name;
```

Rows: 15 (New York: 5, Philadelphia: 5, San Jose: 5). You can
filter on **any** column of the joined table, not just the key.

### J5 — Each user with role AND city (three-table INNER JOIN)

```sql
SELECT u.id, u.name,
       r.role, r.description,
       c.city, c.population
FROM   users u
JOIN   roles  r ON u.role_id = r.id
JOIN   cities c ON u.city_id = c.id
ORDER BY u.id;
```

Rows: 29 — only users who have **both** a role and a city.

---

## 4. Intermediate Joins (1) — LEFT JOIN, COALESCE, GROUP BY

### I1-1 — Every user with their role, keeping users with no role

```sql
SELECT u.id, u.name, r.role, r.description
FROM   users u
LEFT JOIN roles r ON u.role_id = r.id
ORDER BY u.id;
```

Rows: 36. Compare with J1 (31 rows). `LEFT JOIN` keeps every row
from the **left** table (`users`), and fills `NULL` where there is
no match — in **every** `roles` column (`role` and `description`).

### I1-2 — Every user with role and city, with friendly labels

```sql
SELECT u.id,
       u.name,
       COALESCE(r.role, '(none)')        AS role,
       COALESCE(r.description, '(none)') AS description,
       COALESCE(c.city, '(none)')        AS city,
       COALESCE(c.population, 0)         AS population
FROM   users u
LEFT JOIN roles  r ON u.role_id = r.id
LEFT JOIN cities c ON u.city_id = c.id
ORDER BY u.id;
```

Rows: 36. `COALESCE(a, b)` returns `a`, or `b` if `a` is `NULL`.
The fallback must match the column's type: text for `role`, a
number for `population`.

### I1-3 — Users per role, including roles with zero users

```sql
SELECT r.role,
       COUNT(u.id) AS num_users
FROM   roles r
LEFT JOIN users u ON u.role_id = r.id
GROUP BY r.role
ORDER BY num_users DESC, r.role;
```

Rows: 7. `tester` and `QA` show 0. Use `COUNT(u.id)`, **not**
`COUNT(*)` — `COUNT(*)` would count the empty match as 1.

### I1-4 — Users per city, including cities with zero users

```sql
SELECT c.city,
       c.population,
       COUNT(u.id) AS num_users
FROM   cities c
LEFT JOIN users u ON u.city_id = c.id
GROUP BY c.city, c.population
ORDER BY num_users DESC, c.city;
```

Rows: 8. `Cupertino` and `Detroit` show 0. `c.population` must be
in `GROUP BY` too: every `SELECT` column that is not inside an
aggregate like `COUNT()` has to be grouped.

### I1-5 — Users per city, with users who have no city in their own group

```sql
SELECT COALESCE(c.city, '(no city)') AS city,
       COUNT(*)                      AS num_users
FROM   users u
LEFT JOIN cities c ON u.city_id = c.id
GROUP BY COALESCE(c.city, '(no city)')
ORDER BY num_users DESC, city;
```

Rows: 7. Starting `FROM users` counts every user exactly once
(total = 36), but empty cities do not appear. Compare with I1-4:
**which table you start from decides which rows survive.**

---

## 5. Intermediate Joins (2) — RIGHT, FULL OUTER, CROSS, self-join, HAVING

### I2-1 — RIGHT JOIN: every role, with its users

```sql
SELECT r.role, u.name
FROM   users u
RIGHT JOIN roles r ON u.role_id = r.id
ORDER BY r.role, u.name;
```

Rows: 33 (31 matches + `tester` and `QA` with a `NULL` name).
`users RIGHT JOIN roles` gives the same rows as
`roles LEFT JOIN users`. Most people write the `LEFT JOIN` form.

### I2-2 — FULL OUTER JOIN: users and cities, unmatched on both sides

```sql
SELECT u.name, c.city, c.population
FROM   users u
FULL OUTER JOIN cities c ON u.city_id = c.id
WHERE  u.id IS NULL OR c.id IS NULL
ORDER BY c.city, u.name;
```

Rows: 6. `FULL OUTER JOIN` keeps unmatched rows from **both**
tables. The `WHERE` keeps only the leftovers: 2 empty cities
(Cupertino, Detroit) and 4 users with no city.

### I2-3 — Self-join: pairs of users who live in the same city

```sql
SELECT c.city,
       a.name AS user_1,
       b.name AS user_2
FROM   users a
JOIN   users b  ON a.city_id = b.city_id
               AND a.id < b.id
JOIN   cities c ON a.city_id = c.id
WHERE  c.city = 'Santa Clara'
ORDER BY user_1, user_2;
```

Rows: 6 (4 people in Santa Clara → 6 pairs). We join `users` to
**itself** with two aliases. `a.id < b.id` stops a person pairing
with themselves and stops each pair appearing twice.

### I2-4 — CROSS JOIN: role + city combinations nobody fills

```sql
SELECT r.role, c.city
FROM   roles r
CROSS JOIN cities c
LEFT JOIN users u ON u.role_id = r.id
                 AND u.city_id = c.id
WHERE  u.id IS NULL
  AND  r.role = 'admin'
ORDER BY c.city;
```

Rows: 4 (Cupertino, Detroit, San Jose, Santa Clara).
`CROSS JOIN` builds every possible pair (7 × 8 = 56). The
`LEFT JOIN ... IS NULL` then keeps the pairs no user matches.
Remove the `r.role = 'admin'` line to see all 38 empty combinations.

### I2-5 — JOIN + GROUP BY + HAVING: roles found in 3 or more cities

```sql
SELECT r.role,
       COUNT(DISTINCT u.city_id) AS num_cities,
       COUNT(*)                  AS num_users
FROM   users u
JOIN   roles r ON u.role_id = r.id
WHERE  u.city_id IS NOT NULL
GROUP BY r.role
HAVING COUNT(DISTINCT u.city_id) >= 3
ORDER BY num_cities DESC, r.role;
```

Rows: 5 (admin, analyst, user: 4 cities each;
developer, superuser: 3 each).

---

## 6. Cities Not Assigned to Any User

Expected answer for every query below:

| id | city | population |
|---:|------|-----------:|
| 5 | Cupertino | 60381 |
| 6 | Detroit | 639111 |

### 6a — LEFT JOIN + IS NULL (the standard way)

```sql
SELECT c.id, c.city, c.population
FROM   cities c
LEFT JOIN users u ON u.city_id = c.id
WHERE  u.id IS NULL
ORDER BY c.id;
```

### 6b — NOT EXISTS

```sql
SELECT c.id, c.city, c.population
FROM   cities c
WHERE  NOT EXISTS (
           SELECT 1
           FROM   users u
           WHERE  u.city_id = c.id
       )
ORDER BY c.id;
```

### 6c — NOT IN (watch out for NULL!)

```sql
SELECT c.id, c.city, c.population
FROM   cities c
WHERE  c.id NOT IN (
           SELECT city_id
           FROM   users
           WHERE  city_id IS NOT NULL
       )
ORDER BY c.id;
```

> **Trap:** remove the line `WHERE city_id IS NOT NULL` and you get
> **0 rows**. The list now contains `NULL`, and `x NOT IN (..., NULL)`
> is never true. `LEFT JOIN` and `NOT EXISTS` do not have this
> problem.

### 6d — EXCEPT (set difference)

```sql
SELECT id, city, population FROM cities
EXCEPT
SELECT c.id, c.city, c.population
FROM   cities c
JOIN   users  u ON u.city_id = c.id
ORDER BY id;
```

"All cities" minus "cities that have a user". Both `SELECT`s must
list the same columns, in the same order.

---

## 7. Roles Not Assigned to Any User

Expected answer for every query below:

| id | role | description |
|---:|------|-------------|
| 4 | tester | Tests new features before release |
| 5 | QA | Checks quality and reports defects |

### 7a — LEFT JOIN + IS NULL

```sql
SELECT r.id, r.role, r.description
FROM   roles r
LEFT JOIN users u ON u.role_id = r.id
WHERE  u.id IS NULL
ORDER BY r.id;
```

### 7b — NOT EXISTS

```sql
SELECT r.id, r.role, r.description
FROM   roles r
WHERE  NOT EXISTS (
           SELECT 1
           FROM   users u
           WHERE  u.role_id = r.id
       )
ORDER BY r.id;
```

### 7c — NOT IN (with the NULL filter)

```sql
SELECT r.id, r.role, r.description
FROM   roles r
WHERE  r.id NOT IN (
           SELECT role_id
           FROM   users
           WHERE  role_id IS NOT NULL
       )
ORDER BY r.id;
```

Same trap as 6c: without the `IS NOT NULL` filter, 0 rows.

### 7d — Role counts, then keep the zeros

```sql
SELECT r.id, r.role, r.description, COUNT(u.id) AS num_users
FROM   roles r
LEFT JOIN users u ON u.role_id = r.id
GROUP BY r.id, r.role, r.description
HAVING COUNT(u.id) = 0
ORDER BY r.id;
```

---

## 8. Users With No Role

Expected answer:

| id | name | city | population |
|---:|------|------|-----------:|
| 30 | Diego | San Francisco | 873965 |
| 31 | Hana | San Jose | 1013240 |
| 32 | Victor | New York | 8804190 |
| 35 | Zoe | (none) | NULL |
| 36 | Tom | (none) | NULL |

### 8a — Simple filter (no join needed)

```sql
SELECT id, name
FROM   users
WHERE  role_id IS NULL
ORDER BY id;
```

Remember: `role_id = NULL` returns nothing. Always use `IS NULL`.

### 8b — LEFT JOIN + IS NULL, showing the city too

```sql
SELECT u.id,
       u.name,
       COALESCE(c.city, '(none)') AS city,
       c.population
FROM   users u
LEFT JOIN roles  r ON u.role_id = r.id
LEFT JOIN cities c ON u.city_id = c.id
WHERE  r.id IS NULL
ORDER BY u.id;
```

The `LEFT JOIN` form also catches a `role_id` that points to a role
that doesn't exist. Here the `FOREIGN KEY` prevents that, but many
real databases have no such constraint.

---

## 9. Users With No City

Expected answer:

| id | name | role | description |
|---:|------|------|-------------|
| 33 | Grace | user | Uses everyday features of the tool |
| 34 | Ravi | developer | Builds and maintains the software |
| 35 | Zoe | (none) | (none) |
| 36 | Tom | (none) | (none) |

### 9a — Simple filter

```sql
SELECT id, name
FROM   users
WHERE  city_id IS NULL
ORDER BY id;
```

### 9b — LEFT JOIN + IS NULL, showing the role too

```sql
SELECT u.id,
       u.name,
       COALESCE(r.role, '(none)')        AS role,
       COALESCE(r.description, '(none)') AS description
FROM   users u
LEFT JOIN cities c ON u.city_id = c.id
LEFT JOIN roles  r ON u.role_id = r.id
WHERE  c.id IS NULL
ORDER BY u.id;
```

---

## 10. Users With No Role AND No City

Expected answer:

| id | name |
|---:|------|
| 35 | Zoe |
| 36 | Tom |

### 10a — Simple filter

```sql
SELECT id, name
FROM   users
WHERE  role_id IS NULL
  AND  city_id IS NULL
ORDER BY id;
```

### 10b — LEFT JOIN to both tables

```sql
SELECT u.id, u.name
FROM   users u
LEFT JOIN roles  r ON u.role_id = r.id
LEFT JOIN cities c ON u.city_id = c.id
WHERE  r.id IS NULL
  AND  c.id IS NULL
ORDER BY u.id;
```

### 10c — Bonus: label every user with what is missing

```sql
SELECT u.id,
       u.name,
       CASE
           WHEN r.id IS NULL AND c.id IS NULL THEN 'no role, no city'
           WHEN r.id IS NULL                  THEN 'no role'
           WHEN c.id IS NULL                  THEN 'no city'
           ELSE                                    'complete'
       END AS status
FROM   users u
LEFT JOIN roles  r ON u.role_id = r.id
LEFT JOIN cities c ON u.city_id = c.id
ORDER BY status, u.id;
```

Rows: 36 — 29 complete, 3 no role only, 2 no city only, 2 neither.

> **AND vs. OR:** `AND` (10a/10b) finds users missing **both**
> (2 rows). Change it to `OR` and you find users missing **either**
> (7 rows: 5 + 4 − 2, because Zoe and Tom are in both lists).

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
