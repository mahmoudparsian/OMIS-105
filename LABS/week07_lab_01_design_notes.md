# Design Notes — Week 07, Lab 1

## Rule: no hand-typed numbers

Q2 could be "solved" with `WHERE quantity > 1.64`. The student
header says that gets no credit — the whole point is the subquery.

## The NULL in the data is deliberate

Order 12 is a guest order (`customer_id` is `NULL`). It makes Q9's
first attempt (`NOT IN` without `IS NOT NULL`) return **0 rows** —
the most important trap of the week. Q8 uses `NOT IN` on
`orders.product_id`, which has no `NULL`, so it is safe; the
contrast between Q8 and Q9 is intended.

## The four moves

| Move | Where | Why |
|---|---|---|
| Predict | Q1 | "1 row, 1 column" is what makes a subquery *scalar* |
| Explain it | Q9 | Why `NOT IN` + `NULL` = 0 rows |
| Debug it | Q11 | `=` with a 3-row subquery. DuckDB 1.5.5 raises a clear error (older versions silently picked a random row) |
| Bonus | Q12 | A subquery inside a subquery: second-highest price |

All results checked against DuckDB 1.5.5.

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
