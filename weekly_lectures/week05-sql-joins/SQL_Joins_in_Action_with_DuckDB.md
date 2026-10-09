# SQL Joins in Action with DuckDB

A **join** combines rows from two tables into one result.
It pairs rows that "belong together" — usually rows that
share the same **key** (for example, the same `customer_id`).

DuckDB supports all the standard SQL join types out of the
box. Under the hood, it uses a fast *hash join* engine, so
joins stay quick even on large tables.

This document has three parts:

1. **The five join types** — a quick reference with symbols.
2. **Intuition and mathematics** — what each join means.
3. **Joins in action** — real DuckDB queries and their output.

---

## Quick Reference

Each join type has a standard symbol from *relational
algebra* (the mathematics behind databases). You will see
these symbols in textbooks and on diagrams.

| Join Type | Symbol | Example | What it keeps | SQL syntax |
| :-------- | :----: | :-----: | :------------ | :--------- |
| **Inner Join** | ⋈ | `A ⋈ B` | Only rows whose key matches in **both** tables | `FROM A JOIN B ON A.key = B.key` |
| **Left Outer Join** | ⟕ | `A ⟕ B` | **All** rows of `A`, plus matches from `B` (`NULL` if none) | `FROM A LEFT JOIN B ON A.key = B.key` |
| **Right Outer Join** | ⟖ | `A ⟖ B` | **All** rows of `B`, plus matches from `A` (`NULL` if none) | `FROM A RIGHT JOIN B ON A.key = B.key` |
| **Full Outer Join** | ⟗ | `A ⟗ B` | **All** rows of **both** tables (`NULL` where no match) | `FROM A FULL JOIN B ON A.key = B.key` |
| **Cross Join** | × | `A × B` | **Every** row of `A` paired with **every** row of `B` | `FROM A CROSS JOIN B` |

**How to read the symbols.** The small "wing" on the
outer-join symbols points to the side that is **kept in
full**:

* ⟕ — wing on the **left** → keep all of the left table (`A`).
* ⟖ — wing on the **right** → keep all of the right table (`B`).
* ⟗ — wings on **both** sides → keep all of both tables.
* ⋈ — no wings → keep only the matches.

> **Note:** `JOIN` and `INNER JOIN` mean the same thing.
> `LEFT JOIN` = `LEFT OUTER JOIN`, `RIGHT JOIN` =
> `RIGHT OUTER JOIN`, and `FULL JOIN` = `FULL OUTER JOIN`.
> The word `OUTER` is optional.

---

# Part 1 — Intuition and Mathematics

Imagine you have two tables, **A** and **B**:

* **Table A** has columns `(key, value1)`
* **Table B** has columns `(key, value2)`

In mathematics, a table (also called a **relation**) is a
set of rows. Each row is a **tuple** — an ordered list of
values:

$$A = \{(k, v_1) \mid k \in K_A,\ v_1 \in V_1\}$$

$$B = \{(k, v_2) \mid k \in K_B,\ v_2 \in V_2\}$$

Sometimes a `key` exists in one table but not in the other.
To fill the empty spots in the result, SQL uses a special
marker called **`NULL`**. `NULL` means "missing" or
"unknown" — it is **not** zero and **not** an empty string.

---

## 1. Inner Join — `A ⋈ B`

### Simple Explanation

An **Inner Join** keeps only the rows where the `key`
matches in **both** Table **A** and Table **B**. If a key
is in **A** but not in **B** (or the other way around),
that row is dropped.

Think of it as the **overlap** of the two tables.

### Mathematical Definition

$$A ⋈ B = \{ (k, v_1, v_2) \mid (k, v_1) \in A \ \text{ and } \ (k, v_2) \in B \}$$

An equivalent view: start from the Cross Join (every
possible pair), then keep only the pairs whose keys are
equal:

$$A ⋈ B = \{ (k_1, v_1, v_2) \mid (k_1, v_1, k_2, v_2) \in A \times B \ \text{ and } \ k_1 = k_2 \}$$

This is a useful way to think: **an inner join is a cross
join followed by a filter.**

---

## 2. Left Outer Join — `A ⟕ B`

### Simple Explanation

A **Left Join** keeps **all** rows from Table **A** (the
left table).

* If a key from **A** matches a key in **B**, the matching
  $v_2$ value is attached.
* If a key from **A** has **no** match in **B**, the row is
  still kept, but $v_2$ is filled with `NULL`.

No row of **A** is ever lost.

### Mathematical Definition

The Left Join is the Inner Join **plus** the unmatched rows
of **A**, padded with `NULL`:

$$A ⟕ B = (A ⋈ B) \ \cup \ \{ (k, v_1, \text{NULL}) \mid (k, v_1) \in A \ \text{ and } \ \nexists\, v_2 : (k, v_2) \in B \}$$

---

## 3. Right Outer Join — `A ⟖ B`

### Simple Explanation

A **Right Join** is the mirror image of a Left Join. It
keeps **all** rows from Table **B** (the right table).

* If a key from **B** matches a key in **A**, the matching
  $v_1$ value is attached.
* If a key from **B** has **no** match in **A**, the row is
  still kept, but $v_1$ is filled with `NULL`.

### Mathematical Definition

The Right Join is the Inner Join **plus** the unmatched rows
of **B**, padded with `NULL`:

$$A ⟖ B = (A ⋈ B) \ \cup \ \{ (k, \text{NULL}, v_2) \mid (k, v_2) \in B \ \text{ and } \ \nexists\, v_1 : (k, v_1) \in A \}$$

> **Tip:** `A ⟖ B` gives the same rows as `B ⟕ A` (only the
> column order differs). Many people use only `LEFT JOIN`
> and simply swap the table order when they need a right
> join.

---

## 4. Full Outer Join — `A ⟗ B`

### Simple Explanation

A **Full Join** keeps **everything**:

* all matching rows,
* all unmatched rows from **A** (with `NULL` for $v_2$), and
* all unmatched rows from **B** (with `NULL` for $v_1$).

### Mathematical Definition

The Full Join is the union of the Left Join and the Right
Join:

$$A ⟗ B = (A ⟕ B) \ \cup \ (A ⟖ B)$$

Written out in full, it has three pieces:

$$
\begin{aligned}
A ⟗ B = \ & \{ (k, v_1, v_2) \mid (k, v_1) \in A \ \text{ and } \ (k, v_2) \in B \} && \text{(matches)} \\
\cup \ & \{ (k, v_1, \text{NULL}) \mid (k, v_1) \in A \ \text{ and } \ \nexists\, v_2 : (k, v_2) \in B \} && \text{(only in A)} \\
\cup \ & \{ (k, \text{NULL}, v_2) \mid (k, v_2) \in B \ \text{ and } \ \nexists\, v_1 : (k, v_1) \in A \} && \text{(only in B)}
\end{aligned}
$$

> **Note:** In set mathematics, `∪` removes duplicates, so
> the matched rows (which appear in both `A ⟕ B` and
> `A ⟖ B`) are counted only **once**. That is exactly what
> SQL's `FULL JOIN` does.

---

## 5. Cross Join — `A × B`

### Simple Explanation

A **Cross Join** pairs **every** row of Table **A** with
**every** row of Table **B**. Keys are ignored completely.
It is also called the **Cartesian product**.

If **A** has 3 rows and **B** has 4 rows, the result has
`3 × 4 = 12` rows.

> **Warning:** Cross joins grow fast. Two tables with
> 10,000 rows each produce **100,000,000** rows. Use them
> on purpose, never by accident.

### Mathematical Definition

$$A \times B = \{ (k_1, v_1, k_2, v_2) \mid (k_1, v_1) \in A \ \text{ and } \ (k_2, v_2) \in B \}$$

---

## How Many Rows Will I Get?

You can **predict** the size of a join before you run it.
For each key $k$, let $|A_k|$ be the number of rows in
**A** with that key, and $|B_k|$ the number in **B**.

| Join | Number of result rows |
| :--- | :-------------------- |
| `A ⋈ B` | $\sum_k \lvert A_k \rvert \cdot \lvert B_k \rvert$ — each match multiplies |
| `A ⟕ B` | $\lvert A ⋈ B \rvert$ + (rows of A with no match) |
| `A ⟖ B` | $\lvert A ⋈ B \rvert$ + (rows of B with no match) |
| `A ⟗ B` | $\lvert A ⋈ B \rvert$ + (unmatched in A) + (unmatched in B) |
| `A × B` | $\lvert A \rvert \cdot \lvert B \rvert$ |

**Key idea:** when a key appears **more than once** in both
tables, the rows **multiply**. Two rows with `key = 1` in
**A** and two rows with `key = 1` in **B** give
`2 × 2 = 4` result rows. This surprises many beginners —
we will see it in the examples below.

---

## Summary Matrix

| Join Type | Symbol | Matched rows? | Unmatched left (`A`)? | Unmatched right (`B`)? |
| :-------- | :----: | :-----------: | :-------------------: | :--------------------: |
| **Inner Join** | ⋈ | Yes | No | No |
| **Left Outer Join** | ⟕ | Yes | Yes (with `NULL`) | No |
| **Right Outer Join** | ⟖ | Yes | No | Yes (with `NULL`) |
| **Full Outer Join** | ⟗ | Yes | Yes (with `NULL`) | Yes (with `NULL`) |
| **Cross Join** | × | All pairs (`N × M`) | N/A | N/A |

---

# Part 2 — Joins in Action with DuckDB

All the examples below were run in the DuckDB command-line
shell. You can copy each query and run it yourself.

## Step 1 — Create the Two Tables

```sql
% duckdb
DuckDB v1.5.5 (Variegata)
Enter ".help" for usage hints.

duckdb ▸ CREATE TABLE A (
           key   INT,
           value VARCHAR
         );

duckdb ▸ INSERT INTO A
         VALUES
           (1, 'a1'),
           (1, 'a2'),
           (2, 'b1'),
           (2, 'b2'),
           (2, 'b3'),
           (3, 'c1'),
           (4, 'd1');

duckdb ▸ CREATE TABLE B (
           key   INT,
           value VARCHAR
         );

duckdb ▸ INSERT INTO B
         VALUES
           (1, 'p1'),
           (1, 'p2'),
           (2, 't1'),
           (2, 't2'),
           (5, 'x1'),
           (6, 'y1');
```

## Step 2 — Look at the Data

```sql
duckdb ▸ SELECT * FROM A;
┌───────┬─────────┐
│  key  │  value  │
│ int32 │ varchar │
├───────┼─────────┤
│     1 │ a1      │
│     1 │ a2      │
│     2 │ b1      │
│     2 │ b2      │
│     2 │ b3      │
│     3 │ c1      │
│     4 │ d1      │
└───────┴─────────┘

duckdb ▸ SELECT * FROM B;
┌───────┬─────────┐
│  key  │  value  │
│ int32 │ varchar │
├───────┼─────────┤
│     1 │ p1      │
│     1 │ p2      │
│     2 │ t1      │
│     2 │ t2      │
│     5 │ x1      │
│     6 │ y1      │
└───────┴─────────┘
```

Before joining, notice how the keys line up:

| key | rows in A | rows in B | Status |
| :-: | :-------: | :-------: | :----- |
| 1 | 2 (`a1`, `a2`) | 2 (`p1`, `p2`) | match → `2 × 2 = 4` rows |
| 2 | 3 (`b1`, `b2`, `b3`) | 2 (`t1`, `t2`) | match → `3 × 2 = 6` rows |
| 3 | 1 (`c1`) | 0 | only in **A** |
| 4 | 1 (`d1`) | 0 | only in **A** |
| 5 | 0 | 1 (`x1`) | only in **B** |
| 6 | 0 | 1 (`y1`) | only in **B** |

Using the row-count rules from Part 1, we can **predict**
every result:

| Join | Prediction | Rows |
| :--- | :--------- | :--: |
| `A ⋈ B` | `4 + 6` | **10** |
| `A ⟕ B` | `10 + 2` (keys 3, 4) | **12** |
| `A ⟖ B` | `10 + 2` (keys 5, 6) | **12** |
| `A ⟗ B` | `10 + 2 + 2` | **14** |
| `A × B` | `7 × 6` | **42** |

Now let's check each prediction in DuckDB.

> **Why the long `ORDER BY`?** SQL does not promise any row
> order unless you ask for one. Sorting by key **and** by
> value makes the output the same every time you run it.

---

## Inner Join — `A ⋈ B` (10 rows)

Only keys 1 and 2 appear in both tables, so only they
survive. Keys 3, 4, 5, and 6 are dropped.

```sql
duckdb ▸ SELECT A.key   AS A_key,
                B.key   AS B_key,
                A.value AS A_value,
                B.value AS B_value
         FROM A
         INNER JOIN B ON A.key = B.key
         ORDER BY A_key, A_value, B_value;
┌───────┬───────┬─────────┬─────────┐
│ A_key │ B_key │ A_value │ B_value │
│ int32 │ int32 │ varchar │ varchar │
├───────┼───────┼─────────┼─────────┤
│     1 │     1 │ a1      │ p1      │
│     1 │     1 │ a1      │ p2      │
│     1 │     1 │ a2      │ p1      │
│     1 │     1 │ a2      │ p2      │
│     2 │     2 │ b1      │ t1      │
│     2 │     2 │ b1      │ t2      │
│     2 │     2 │ b2      │ t1      │
│     2 │     2 │ b2      │ t2      │
│     2 │     2 │ b3      │ t1      │
│     2 │     2 │ b3      │ t2      │
└───────┴───────┴─────────┴─────────┘
  10 rows                 4 columns
```

Look at key 1: each of `a1`, `a2` is paired with each of
`p1`, `p2` — that is the `2 × 2 = 4` multiplication.

---

## Left Outer Join — `A ⟕ B` (12 rows)

Every row of **A** is kept. Keys 3 and 4 have no partner in
**B**, so their **B** columns are `NULL`.

```sql
duckdb ▸ SELECT A.key   AS A_key,
                B.key   AS B_key,
                A.value AS A_value,
                B.value AS B_value
         FROM A
         LEFT JOIN B ON A.key = B.key
         ORDER BY A_key, A_value, B_value;
┌───────┬───────┬─────────┬─────────┐
│ A_key │ B_key │ A_value │ B_value │
│ int32 │ int32 │ varchar │ varchar │
├───────┼───────┼─────────┼─────────┤
│     1 │     1 │ a1      │ p1      │
│     1 │     1 │ a1      │ p2      │
│     1 │     1 │ a2      │ p1      │
│     1 │     1 │ a2      │ p2      │
│     2 │     2 │ b1      │ t1      │
│     2 │     2 │ b1      │ t2      │
│     2 │     2 │ b2      │ t1      │
│     2 │     2 │ b2      │ t2      │
│     2 │     2 │ b3      │ t1      │
│     2 │     2 │ b3      │ t2      │
│     3 │  NULL │ c1      │ NULL    │  ◀── only in A
│     4 │  NULL │ d1      │ NULL    │  ◀── only in A
└───────┴───────┴─────────┴─────────┘
  12 rows                 4 columns
```

---

## Right Outer Join — `A ⟖ B` (12 rows)

Every row of **B** is kept. Keys 5 and 6 have no partner in
**A**, so their **A** columns are `NULL`. Here we sort by
`B_key`, because `A_key` is `NULL` for the unmatched rows.

```sql
duckdb ▸ SELECT A.key   AS A_key,
                B.key   AS B_key,
                A.value AS A_value,
                B.value AS B_value
         FROM A
         RIGHT JOIN B ON A.key = B.key
         ORDER BY B_key, A_value, B_value;
┌───────┬───────┬─────────┬─────────┐
│ A_key │ B_key │ A_value │ B_value │
│ int32 │ int32 │ varchar │ varchar │
├───────┼───────┼─────────┼─────────┤
│     1 │     1 │ a1      │ p1      │
│     1 │     1 │ a1      │ p2      │
│     1 │     1 │ a2      │ p1      │
│     1 │     1 │ a2      │ p2      │
│     2 │     2 │ b1      │ t1      │
│     2 │     2 │ b1      │ t2      │
│     2 │     2 │ b2      │ t1      │
│     2 │     2 │ b2      │ t2      │
│     2 │     2 │ b3      │ t1      │
│     2 │     2 │ b3      │ t2      │
│  NULL │     5 │ NULL    │ x1      │  ◀── only in B
│  NULL │     6 │ NULL    │ y1      │  ◀── only in B
└───────┴───────┴─────────┴─────────┘
  12 rows                 4 columns
```

---

## Full Outer Join — `A ⟗ B` (14 rows)

Everything is kept: the 10 matches, the 2 rows only in
**A**, and the 2 rows only in **B**.

`COALESCE(A.key, B.key)` returns the first value that is
**not** `NULL`. We use it to sort every row by its "real"
key, no matter which side it came from.

```sql
duckdb ▸ SELECT A.key   AS A_key,
                B.key   AS B_key,
                A.value AS A_value,
                B.value AS B_value
         FROM A
         FULL JOIN B ON A.key = B.key
         ORDER BY COALESCE(A.key, B.key), A_value, B_value;
┌───────┬───────┬─────────┬─────────┐
│ A_key │ B_key │ A_value │ B_value │
│ int32 │ int32 │ varchar │ varchar │
├───────┼───────┼─────────┼─────────┤
│     1 │     1 │ a1      │ p1      │
│     1 │     1 │ a1      │ p2      │
│     1 │     1 │ a2      │ p1      │
│     1 │     1 │ a2      │ p2      │
│     2 │     2 │ b1      │ t1      │
│     2 │     2 │ b1      │ t2      │
│     2 │     2 │ b2      │ t1      │
│     2 │     2 │ b2      │ t2      │
│     2 │     2 │ b3      │ t1      │
│     2 │     2 │ b3      │ t2      │
│     3 │  NULL │ c1      │ NULL    │  ◀── only in A
│     4 │  NULL │ d1      │ NULL    │  ◀── only in A
│  NULL │     5 │ NULL    │ x1      │  ◀── only in B
│  NULL │     6 │ NULL    │ y1      │  ◀── only in B
└───────┴───────┴─────────┴─────────┘
  14 rows                 4 columns
```

---

## Cross Join — `A × B` (42 rows)

There is **no** `ON` clause. Every one of the 7 rows in
**A** is paired with every one of the 6 rows in **B**:
`7 × 6 = 42` rows. Notice that most pairs have **different**
keys — the cross join does not care about keys at all.

```sql
duckdb ▸ SELECT A.key   AS A_key,
                B.key   AS B_key,
                A.value AS A_value,
                B.value AS B_value
         FROM A
         CROSS JOIN B
         ORDER BY A_value, B_value;
┌───────┬───────┬─────────┬─────────┐
│ A_key │ B_key │ A_value │ B_value │
│ int32 │ int32 │ varchar │ varchar │
├───────┼───────┼─────────┼─────────┤
│     1 │     1 │ a1      │ p1      │
│     1 │     1 │ a1      │ p2      │
│     1 │     2 │ a1      │ t1      │
│     1 │     2 │ a1      │ t2      │
│     1 │     5 │ a1      │ x1      │
│     1 │     6 │ a1      │ y1      │
│     1 │     1 │ a2      │ p1      │
│     1 │     1 │ a2      │ p2      │
│     1 │     2 │ a2      │ t1      │
│     1 │     2 │ a2      │ t2      │
│     1 │     5 │ a2      │ x1      │
│     1 │     6 │ a2      │ y1      │
│     2 │     1 │ b1      │ p1      │
│     2 │     1 │ b1      │ p2      │
│     2 │     2 │ b1      │ t1      │
│     2 │     2 │ b1      │ t2      │
│     2 │     5 │ b1      │ x1      │
│     2 │     6 │ b1      │ y1      │
│     2 │     1 │ b2      │ p1      │
│     2 │     1 │ b2      │ p2      │
│     2 │     2 │ b2      │ t1      │
│     2 │     2 │ b2      │ t2      │
│     2 │     5 │ b2      │ x1      │
│     2 │     6 │ b2      │ y1      │
│     2 │     1 │ b3      │ p1      │
│     2 │     1 │ b3      │ p2      │
│     2 │     2 │ b3      │ t1      │
│     2 │     2 │ b3      │ t2      │
│     2 │     5 │ b3      │ x1      │
│     2 │     6 │ b3      │ y1      │
│     3 │     1 │ c1      │ p1      │
│     3 │     1 │ c1      │ p2      │
│     3 │     2 │ c1      │ t1      │
│     3 │     2 │ c1      │ t2      │
│     3 │     5 │ c1      │ x1      │
│     3 │     6 │ c1      │ y1      │
│     4 │     1 │ d1      │ p1      │
│     4 │     1 │ d1      │ p2      │
│     4 │     2 │ d1      │ t1      │
│     4 │     2 │ d1      │ t2      │
│     4 │     5 │ d1      │ x1      │
│     4 │     6 │ d1      │ y1      │
└───────┴───────┴─────────┴─────────┘
  42 rows                 4 columns
```

> **Connection to the math:** if you add
> `WHERE A.key = B.key` to this cross join, you get exactly
> the 10 rows of the inner join. That is the formula
> $A ⋈ B = \sigma_{k_1 = k_2}(A \times B)$ in action
> ($\sigma$ means "filter" in relational algebra).

---

# Part 3 — Practical Patterns

## Finding Unmatched Rows: `LEFT JOIN` + `IS NULL`

A very common business question is: *"Which rows have
**no** partner?"* For example: customers who never placed
an order, or products that never sold.

The trick: do a `LEFT JOIN`, then keep only the rows where
the right side is `NULL`.

```sql
duckdb ▸ SELECT A.key, A.value
         FROM A
         LEFT JOIN B ON A.key = B.key
         WHERE B.key IS NULL
         ORDER BY A.key;
┌───────┬─────────┐
│  key  │  value  │
│ int32 │ varchar │
├───────┼─────────┤
│     3 │ c1      │
│     4 │ d1      │
└───────┴─────────┘
```

These are exactly the rows of **A** that `A ⟕ B` padded
with `NULL`. (In relational algebra this is called an
**anti-join**.)

> **Important:** always write `IS NULL`, never `= NULL`.
> `B.key = NULL` is never true, so it returns no rows.

## Cleaning Up `NULL`s: `COALESCE`

`NULL` values can confuse readers of a report. `COALESCE`
replaces them with something friendlier. Here we use a
`FULL JOIN` to list **all** unmatched rows from both sides:

```sql
duckdb ▸ SELECT COALESCE(A.key, B.key)     AS key,
                COALESCE(A.value, '(none)') AS A_value,
                COALESCE(B.value, '(none)') AS B_value
         FROM A
         FULL JOIN B ON A.key = B.key
         WHERE A.key IS NULL OR B.key IS NULL
         ORDER BY key;
┌───────┬─────────┬─────────┐
│  key  │ A_value │ B_value │
│ int32 │ varchar │ varchar │
├───────┼─────────┼─────────┤
│     3 │ c1      │ (none)  │
│     4 │ d1      │ (none)  │
│     5 │ (none)  │ x1      │
│     6 │ (none)  │ y1      │
└───────┴─────────┴─────────┘
```

---

## Key Takeaways

* **⋈ Inner Join** keeps only matches — the overlap.
* **⟕ Left Join** keeps all of the left table; **⟖ Right
  Join** keeps all of the right table.
* **⟗ Full Join** keeps everything from both tables.
* **× Cross Join** pairs every row with every row — no
  `ON` clause, and the result can be huge.
* Missing partners show up as **`NULL`**. Use `IS NULL` to
  find them and `COALESCE` to replace them.
* **Duplicate keys multiply rows.** Always predict your row
  count, then check it.
* Add a full `ORDER BY` when you need the same output order
  every time.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
