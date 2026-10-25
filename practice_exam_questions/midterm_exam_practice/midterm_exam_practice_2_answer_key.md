# OMIS 105 — Midterm Exam Practice Version 2 Answer Key (Material Covered So Far)

Instructor-only. Pair with `midterm_exam_practice_2.md`.

All query results below were verified by running them in DuckDB against the 10-row sample data.

---

## Part 1 — Multiple Choice (30 pts, 2 pts each)

| # | Answer | Topic | Why |
|---|--------|-------|-----|
| 1 | B | Week 1 — file system vs DBMS | A DBMS enforces a schema (types, constraints) and controls concurrent access; spreadsheets do neither. It does not auto-correct spelling (C) and is the opposite of "no structure" (D). |
| 2 | C | Week 1 — metadata | Column definitions, types, and constraints describe the data; A, B, D are data values stored in rows. |
| 3 | B | Week 1 — data types | `DECIMAL(8,2)` stores exact dollars and cents; `INTEGER` would lose the `.50` in `24.50`. |
| 4 | D | Week 1 — constraints | `'refunded'` violates `CHECK (status IN ('placed','delivered','cancelled'))`. `tip`, `cuisine`, and `city` have no `NOT NULL`, so A–C are accepted. |
| 5 | B | Week 3 — primary keys | A PK must be unique and non-NULL for every row, forever. Names, restaurants, and dates repeat in the real world even if they look unique in a small sample. |
| 6 | C | Week 3 — PK enforcement | Duplicate key `order_id: 3` violates the PK; the `INSERT` fails and the table is unchanged (no replace, no auto-renumber). |
| 7 | C | Week 3 — UPDATE without WHERE | Without `WHERE`, `UPDATE` changes every row, and it runs with no error. Same bug as the Week 3 lab "Debug it" question. |
| 8 | B | Week 3 — DELETE vs DROP | `DELETE ... WHERE` removes matching rows only. `DROP TABLE` removes the whole table, `DELETE` with no `WHERE` empties it, and D just changes values. |
| 9 | C | Week 1 — BETWEEN | `BETWEEN` is **inclusive**: 24.50, 28.00, **22.00**, **31.25** → 4 rows. Answer A (2) is what students get if they treat it as exclusive. |
| 10 | B | Week 3 — NULL & COUNT | `COUNT(*)` counts rows (10); `COUNT(tip)` counts non-NULL values (6). Orders 2, 4, 6, 10 have NULL tips. |
| 11 | B | Week 3 — three-valued logic | For a NULL tip, both `tip > 3` and `tip <= 3` are UNKNOWN, so those 4 rows are filtered out → 6 rows. Answer C (5) is `tip > 3` alone. |
| 12 | B | Week 1 — ORDER BY / LIMIT | A gives the 3 smallest; C has `LIMIT` before `ORDER BY` (syntax error); D puts an aggregate in `WHERE` (error). Result: orders 9, 3, 5. |
| 13 | B | Week 2 — WHERE + GROUP BY + HAVING | `WHERE` keeps 7 delivered rows → Taco Loco 1, Pho King 2, Pizza Roma 3, Curry House 1; `HAVING >= 2` keeps Pho King and Pizza Roma. C ignores `HAVING`; D ignores `WHERE`. |
| 14 | B | Week 2 — GROUP BY rule | `restaurant` is neither in `GROUP BY` nor inside an aggregate. DuckDB: *Binder Error: column "restaurant" must appear in the GROUP BY clause or must be part of an aggregate function.* |
| 15 | B | Week 2 — execution order | FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. This is why `WHERE` can't use aggregates or `SELECT` aliases, but `ORDER BY` can use aliases. |

---

## Part 2 — Written Questions (70 pts)

### S1 (10 pts): Primary key
**Expected points:**
- A primary key is a column (or set of columns) that **uniquely identifies each row** of a table.
- Rule 1: **unique**. No two rows may share the same PK value.
- Rule 2: **not NULL**. Every row must have a PK value.
- `customer_name` is a poor PK because (any one of these is enough): two different customers can share a name; the same customer can place **many** orders, so their name would repeat; names can change or be misspelled. Looking unique in 10 sample rows doesn't guarantee uniqueness as the table grows.
- Grading: 3 pts definition, 2 pts each rule (4 total), 3 pts for a correct reason that `customer_name` fails. Full credit for the reason requires saying that sample uniqueness isn't enough.

### S2 (10 pts): NULL
**Expected points:**
- `NULL` means **missing / unknown**: no tip has been recorded. It is not `0` and not an empty string.
- (a) Any comparison with `NULL` using `=` (or `<>`, `>`, …) evaluates to **UNKNOWN**, not TRUE, so `WHERE` filters the row out. Correct form: `WHERE tip IS NULL` (or `IS NOT NULL`).
- (b) `COUNT(*)` counts **rows** → 10. `COUNT(tip)` counts **non-NULL values** in `tip` → 6, because orders 2, 4, 6, 10 have NULL tips. Aggregate functions on a column ignore NULLs.
- Grading: 2 pts meaning of NULL, 4 pts (a) (2 why, 2 `IS NULL`), 4 pts (b) (must give 10 vs 6 with the reason).

### I1 (15 pts)
```sql
SELECT customer_name, restaurant, order_total
FROM orders
WHERE status = 'delivered'
  AND city IN ('San Jose', 'Santa Clara')
  AND order_total >= 25
ORDER BY order_total DESC;
```
**Result (4 rows):**

| customer_name | restaurant  | order_total |
|---------------|-------------|------------:|
| Ian           | Pizza Roma  | 55.00 |
| Cara          | Pizza Roma  | 42.00 |
| Eli           | Pizza Roma  | 36.50 |
| Hana          | Curry House | 31.25 |

**Grading:** 3 pts `status = 'delivered'`, 4 pts correct city filter, 2 pts `>= 25` (not `> 25`), 2 pts `ORDER BY order_total DESC`, 2 pts correct columns, 2 pts correct row count (4).
- Accept `(city = 'San Jose' OR city = 'Santa Clara')` **with parentheses**.
- **Common mistake (deduct 4 pts):** `OR` without parentheses, e.g. `WHERE status = 'delivered' AND city = 'San Jose' OR city = 'Santa Clara' AND order_total >= 25`. Because `AND` binds tighter than `OR`, this returns 5 rows: it wrongly includes Ana (San Jose, $24.50).

### I2 (15 pts)
```sql
-- (a) Create
INSERT INTO orders
VALUES (11, 'Kim', 'Sunnyvale', 'Pizza Roma', 'Italian', 47.00, NULL, '2026-09-06', 'placed');

-- (b) Update: two columns, one statement, filtered by PK
UPDATE orders
SET status = 'delivered',
    tip    = 5.00
WHERE order_id = 6;

-- (c) Delete
DELETE FROM orders
WHERE status = 'cancelled';
```
**(d)** 10 rows (10 + 1 inserted − 1 deleted [order 4]). `'placed'` rows: **2** (orders 10 and 11; order 6 is now delivered).

**Grading:** 4 pts (a): correct values in column order, `NULL` (not `0` or `'NULL'`) for tip. 5 pts (b): both columns in one `SET` separated by a comma, and `WHERE order_id = 6`. **Deduct all 5 if there is no `WHERE`.** 3 pts (c): `DELETE FROM ... WHERE`. 3 pts (d): 1.5 per count.
- Accept an explicit column list in the `INSERT`.

### A1 (10 pts)
```sql
SELECT cuisine,
       COUNT(*)         AS num_orders,
       SUM(order_total) AS total_revenue,
       AVG(order_total) AS avg_order
FROM orders
WHERE status = 'delivered'
GROUP BY cuisine
HAVING COUNT(*) >= 2
ORDER BY total_revenue DESC;
```
**Result:**

| cuisine    | num_orders | total_revenue | avg_order |
|------------|-----------:|--------------:|----------:|
| Italian    | 3 | 133.50 | 44.50 |
| Vietnamese | 2 | 40.00  | 20.00 |

(Mexican has 1 delivered order and Indian has 1, so both are removed by `HAVING`.)

**Grading:** 2 pts `WHERE status = 'delivered'` (row filter, before grouping), 2 pts `GROUP BY cuisine`, 2 pts `HAVING COUNT(*) >= 2` (group filter), 1 pt correct aggregates + aliases, 1 pt `ORDER BY total_revenue DESC`, 2 pts correct result table.
- Putting the status filter in `HAVING` or the count filter in `WHERE` loses the 2 pts for that clause. This question tests the WHERE vs. HAVING distinction.
- Accept `ROUND(AVG(order_total), 2)`.

### A2 (10 pts)
**(a) Two mistakes:**
1. `WHERE AVG(tip) > 4`: aggregate functions can't be used in `WHERE`, because `WHERE` runs **before** `GROUP BY` and no groups exist yet. Group-level conditions go in `HAVING`.
2. `restaurant` is in `SELECT` but not in `GROUP BY` and not aggregated. Each city group contains several restaurants, so the database can't pick a single value.

**(b) Corrected query:**
```sql
SELECT city, AVG(tip) AS avg_tip
FROM orders
GROUP BY city
HAVING AVG(tip) > 4
ORDER BY avg_tip DESC;
```

**(c) Result:**

| city        | avg_tip |
|-------------|--------:|
| San Jose    | 6.00 |
| Santa Clara | 4.75 |

Work: San Jose tips 4, 6, 8 (one NULL) → 18 / 3 = 6.00. Santa Clara: 5, 4.50 (one NULL) → 9.50 / 2 = 4.75. Sunnyvale: 3 only (two NULLs) → 3.00, which is filtered out.

**(d)** **Santa Clara** drops out. With NULLs treated as $0, its average becomes 9.50 / 3 ≈ **3.17**, which is not above 4. (San Jose becomes 18 / 4 = 4.50, still above 4. Sunnyvale becomes 1.00.) The point: `AVG()` divides by the count of **non-NULL** values, so how NULLs are treated changes the result.

**Grading:** (a) 3 pts (1.5 per mistake, with reason). (b) 3 pts: `HAVING` instead of `WHERE`, and `restaurant` removed (adding `restaurant` to `GROUP BY` is also acceptable if the student says it changes the question). (c) 2 pts. (d) 2 pts: names Santa Clara with the 3.17 reasoning.

---

## Suggested Grading Summary Table

| Section | Points |
|---------|--------|
| Part 1: Multiple Choice (15 × 2 pts) | 30 |
| S1 | 10 |
| S2 | 10 |
| I1 | 15 |
| I2 | 15 |
| A1 | 10 |
| A2 | 10 |
| **Total** | **100** |

---

## Instructor Note: Scope

This version covers only what has been taught in class so far (Weeks 1–3: SELECT basics, GROUP BY/HAVING, primary keys, CRUD, NULL). It has **no** JOIN, window-function, CTE, or set-operation questions, unlike `midterm_exam_practice.md` and versions 1–3, which cover Weeks 1–5. Pair it with one of those once Weeks 4–5 are taught.
