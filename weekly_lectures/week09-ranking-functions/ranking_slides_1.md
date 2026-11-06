---
title: OMIS 105 - Week 9 (Ranking Functions — ROW_NUMBER and RANK)
author: Dr. Mahmoud Parsian
marp: true
theme: default
paginate: true
class: lead
style: |
  section {
    justify-content: flex-start;
  }
  table {
    font-size: 0.7em;
  }

---

# OMIS 105: Week 9
## Ranking Functions — Session 1 <br> `ROW_NUMBER` and `RANK`

---

# Agenda

- Why `GROUP BY` cannot rank rows
- Our data: 12 sales reps on 3 teams
- `ROW_NUMBER()` — number the rows 1, 2, 3, …
- `RANK()` — what happens with **ties**
- `PARTITION BY` — restart the numbering for each group
- **Top N per group** — filter the ranking in a subquery
- ⚠️ Why `WHERE` cannot see a ranking column
- Hands-on: Lab 1

---

# What You Already Know

- `GROUP BY` + `MAX` gives **one row per group** (Week 4)
- Subqueries in `FROM` (Week 7)

```sql
SELECT team, MAX(sales) AS top_sales
FROM sales_reps
GROUP BY team
ORDER BY team;
```

| team | top_sales |
|---|---:|
| Central | 105 |
| East | 95 |
| West | 120 |

👉 But **who** is the top rep? And who is **2nd**? `GROUP BY` folds the
rows away — we lose the names.

---

# Our Data: `sales_reps` (12 rows)

| rep_id | rep_name | team | sales |
|---:|---|---|---:|
| 1 | Ava | East | 95 |
| 2 | Ben | East | 88 |
| 3 | Chloe | East | 88 |
| 4 | Dan | East | 70 |
| 5 | Eli | West | 120 |
| 6 | Fay | West | 95 |
| 7 | Gus | West | 60 |
| 8 | Hal | West | 60 |
| 9 | Ivy | Central | 105 |
| 10 | Jon | Central | 99 |
| 11 | Kim | Central | 80 |
| 12 | Leo | Central | 75 |

`sales` is in thousands of dollars. Watch the **ties**: Ava and Fay (95),
Ben and Chloe (88), Gus and Hal (60).

---

# `ROW_NUMBER()` — Number the Rows

```sql
SELECT rep_name, team, sales,
       ROW_NUMBER() OVER (ORDER BY sales DESC, rep_name) AS rn
FROM sales_reps
ORDER BY rn
LIMIT 8;
```

| rep_name | team | sales | rn |
|---|---|---:|---:|
| Eli | West | 120 | 1 |
| Ivy | Central | 105 | 2 |
| Jon | Central | 99 | 3 |
| Ava | East | 95 | 4 |
| Fay | West | 95 | 5 |
| Ben | East | 88 | 6 |
| Chloe | East | 88 | 7 |
| Kim | Central | 80 | 8 |

---

# How to Read a Window Function

```sql
ROW_NUMBER() OVER (ORDER BY sales DESC, rep_name)
```

- `ROW_NUMBER()` — the function: give each row the next number
- `OVER (...)` — the **window**: which rows, in what order
- `ORDER BY sales DESC` — highest sales gets number 1
- `, rep_name` — the **tie-breaker**

👉 Every row **stays** in the result — nothing is grouped away.

---

# ⚠️ `ROW_NUMBER` and Ties

Ava and Fay both have 95. `ROW_NUMBER` must still give them **different**
numbers (4 and 5).

- **Without** a tie-breaker, SQL may give 4 to either one — and the
  answer can change from run to run
- **With** `ORDER BY sales DESC, rep_name`, Ava (A) is always 4

👉 **Rule:** with `ROW_NUMBER`, always add a tie-breaker column.

---

# `RANK()` — Ties Share a Rank

```sql
SELECT rep_name, team, sales,
       RANK() OVER (ORDER BY sales DESC) AS rnk
FROM sales_reps
ORDER BY rnk, rep_name
LIMIT 8;
```

| rep_name | team | sales | rnk |
|---|---|---:|---:|
| Eli | West | 120 | 1 |
| Ivy | Central | 105 | 2 |
| Jon | Central | 99 | 3 |
| Ava | East | 95 | 4 |
| Fay | West | 95 | 4 |
| Ben | East | 88 | 6 |
| Chloe | East | 88 | 6 |
| Kim | Central | 80 | 8 |

---

# `RANK()` Leaves a Gap

- Ava and Fay tie → **both** get rank **4**
- The next rep, Ben, gets rank **6** — rank 5 is **skipped**
- Like a race: two runners tie for 4th, so nobody finishes 5th

👉 `RANK` needs no tie-breaker: tied rows **should** get the same rank.

---

# Side by Side

```sql
SELECT rep_name, sales,
       ROW_NUMBER() OVER (ORDER BY sales DESC, rep_name) AS rn,
       RANK()       OVER (ORDER BY sales DESC)           AS rnk
FROM sales_reps
ORDER BY rn
LIMIT 8;
```

| rep_name | sales | rn | rnk |
|---|---:|---:|---:|
| Eli | 120 | 1 | 1 |
| Ivy | 105 | 2 | 2 |
| Jon | 99 | 3 | 3 |
| Ava | 95 | 4 | 4 |
| Fay | 95 | 5 | 4 |
| Ben | 88 | 6 | 6 |
| Chloe | 88 | 7 | 6 |
| Kim | 80 | 8 | 8 |

---

# `PARTITION BY` — Restart for Each Group

```sql
SELECT team, rep_name, sales,
       ROW_NUMBER() OVER (PARTITION BY team
                          ORDER BY sales DESC, rep_name) AS rn
FROM sales_reps
ORDER BY team, rn;
```

---

# `PARTITION BY` — Result

| team | rep_name | sales | rn |
|---|---|---:|---:|
| Central | Ivy | 105 | 1 |
| Central | Jon | 99 | 2 |
| Central | Kim | 80 | 3 |
| Central | Leo | 75 | 4 |
| East | Ava | 95 | 1 |
| East | Ben | 88 | 2 |
| East | Chloe | 88 | 3 |
| East | Dan | 70 | 4 |
| West | Eli | 120 | 1 |
| West | Fay | 95 | 2 |
| West | Gus | 60 | 3 |
| West | Hal | 60 | 4 |

👉 The numbering **restarts at 1** for every team.

---

# ⚠️ You Cannot Filter `rn` in `WHERE`

We want only the top rep, so we try:

```sql
SELECT rep_name, sales,
       ROW_NUMBER() OVER (ORDER BY sales DESC, rep_name) AS rn
FROM sales_reps
WHERE rn = 1;
```

```
Binder Error: WHERE clause cannot contain window functions!
```

👉 `WHERE` runs **before** the window function, so `rn` does not exist yet.

---

# ✅ Fix: Rank in a Subquery, Filter Outside

```sql
SELECT team, rep_name, sales
FROM (
    SELECT team, rep_name, sales,
           ROW_NUMBER() OVER (PARTITION BY team
                              ORDER BY sales DESC, rep_name) AS rn
    FROM sales_reps
) AS ranked
WHERE rn = 1
ORDER BY team;
```

| team | rep_name | sales |
|---|---|---:|
| Central | Ivy | 105 |
| East | Ava | 95 |
| West | Eli | 120 |

---

# Top 2 per Team with `ROW_NUMBER`

```sql
SELECT team, rep_name, sales, rn
FROM (
    SELECT team, rep_name, sales,
           ROW_NUMBER() OVER (PARTITION BY team
                              ORDER BY sales DESC, rep_name) AS rn
    FROM sales_reps
) AS ranked
WHERE rn <= 2
ORDER BY team, rn;
```

---

# Top 2 per Team — Result

| team | rep_name | sales | rn |
|---|---|---:|---:|
| Central | Ivy | 105 | 1 |
| Central | Jon | 99 | 2 |
| East | Ava | 95 | 1 |
| East | Ben | 88 | 2 |
| West | Eli | 120 | 1 |
| West | Fay | 95 | 2 |

👉 Exactly **2 rows per team** — but East has a tie at 88
(Ben and Chloe). Chloe is left out only because of the tie-breaker.

---

# Top 2 per Team with `RANK`

```sql
SELECT team, rep_name, sales, rnk
FROM (
    SELECT team, rep_name, sales,
           RANK() OVER (PARTITION BY team ORDER BY sales DESC) AS rnk
    FROM sales_reps
) AS ranked
WHERE rnk <= 2
ORDER BY team, rnk, rep_name;
```

---

# Top 2 per Team with `RANK` — Result

| team | rep_name | sales | rnk |
|---|---|---:|---:|
| Central | Ivy | 105 | 1 |
| Central | Jon | 99 | 2 |
| East | Ava | 95 | 1 |
| East | Ben | 88 | 2 |
| East | Chloe | 88 | 2 |
| West | Eli | 120 | 1 |
| West | Fay | 95 | 2 |

👉 **7 rows**: East returns Ava, Ben **and** Chloe — tied rows are kept.

---

# `ROW_NUMBER` or `RANK`?

| The question says… | Use |
|---|---|
| "exactly N rows per group" (a fixed list) | `ROW_NUMBER` + a tie-breaker |
| "the top N, and **include ties**" (fair to everyone) | `RANK` |
| "number the rows" (pagination, first/last event) | `ROW_NUMBER` |

---

# ⚠️ Common Mistake: Forgetting `PARTITION BY`

"The top rep **in each team**", without `PARTITION BY`:

```sql
SELECT team, rep_name, sales
FROM (
    SELECT team, rep_name, sales,
           ROW_NUMBER() OVER (ORDER BY sales DESC, rep_name) AS rn
    FROM sales_reps
) AS ranked
WHERE rn = 1;
```

| team | rep_name | sales |
|---|---|---:|
| West | Eli | 120 |

👉 Only **1 row** — the numbering ran over all 12 reps, not per team.

---

# Summary

| Pattern | SQL |
|---|---|
| number the rows | `ROW_NUMBER() OVER (ORDER BY col DESC, tie_breaker)` |
| rank with ties | `RANK() OVER (ORDER BY col DESC)` |
| per group | `... OVER (PARTITION BY group_col ORDER BY ...)` |
| top N per group | rank in a subquery, then `WHERE rn <= N` outside |

Demo notebook: `ranking_demo_1.py`

---

# Next Session

- `DENSE_RANK()` — ranks with **no gaps**
- All three functions side by side
- Ranking `GROUP BY` results (with a CTE)
- "Second-highest" questions

---

# Questions?

Thank you!

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
