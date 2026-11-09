# Design Notes — Week 07, Lab 2

## Q11 is a silent bug — read before class

```sql
WHERE price > (SELECT AVG(price) FROM products p2
               WHERE p2.category = category)
```

The bare `category` binds to the **nearest** table, `p2`, so the
condition is always true and the subquery returns the overall average
(325.88). No error; 2 rows instead of 3 (the Blender is missing).
Verified in DuckDB 1.5.5. Lesson: in a correlated subquery, write the
alias on both sides.

## Q8 shows both versions

The instructor copy has two cells: the JOIN version (6 rows — Alice and
David once per Electronics order) and the `IN` version (4 rows).

## Q6 was changed during writing

The first draft ("orders above the customer's own average quantity")
returned exactly the same 6 orders as Lab 1's Q2. Replaced with
"each customer's first order" (`MIN`), which gives a different set.

## The four moves

| Move | Where |
|---|---|
| Predict | Q1 (6 of 8 products were ordered) |
| Explain it | Q7 (why the subquery must be correlated) |
| Debug it | Q11 (silent correlation bug) |
| Bonus | Q12 (`EXISTS AND NOT EXISTS`; without `EXISTS`, George and Hana sneak in) |

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
