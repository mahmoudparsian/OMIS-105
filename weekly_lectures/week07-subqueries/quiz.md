# Week 7 Quiz — Subqueries

All questions use the Week 7 store data: 8 `customers`, 8 `products`,
14 `orders`. Order 12 is a guest order with `customer_id = NULL`.

---

**1.** What is a subquery?

- a) A query that runs only on small tables
- b) A `SELECT` written inside parentheses, inside another SQL statement ✅
- c) Another name for a JOIN
- d) A query saved in a file

**2.** Why does `WHERE price > AVG(price)` fail?

- a) `AVG` only works on whole numbers
- b) `WHERE` checks one row at a time, but `AVG` needs all rows ✅
- c) You must write `AVERAGE`, not `AVG`
- d) It does not fail

**3.** In `WHERE price > (SELECT AVG(price) FROM products)`, which part
runs **first**?

- a) The outer query
- b) The subquery in parentheses ✅
- c) Both at the same time
- d) Whichever is shorter

**4.** A **scalar** subquery returns:

- a) Exactly one row and one column ✅
- b) One column with many rows
- c) A whole table
- d) Nothing

**5.** The subquery `SELECT price FROM products WHERE category =
'Furniture'` returns 3 rows. Which works?

- a) `WHERE price = (SELECT price ...)`
- b) `WHERE price IN (SELECT price ...)` ✅
- c) `WHERE price > (SELECT price ...)`
- d) None of them

**6.** The list `SELECT customer_id FROM orders` contains `1, 2, 3, 4, 5,
6, NULL`. How many rows does `WHERE customer_id NOT IN (that list)`
return from `customers`?

- a) 2 (George and Hana)
- b) 0 ✅ — one `NULL` in a `NOT IN` list makes every test unknown
- c) 6
- d) 8

**7.** Which is always safe for "customers who **never** ordered", even
with the `NULL`?

- a) `NOT IN (SELECT customer_id FROM orders)`
- b) `NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)` ✅
- c) `IN (SELECT customer_id FROM orders)`
- d) `<> (SELECT customer_id FROM orders)`

**8.** A subquery in `FROM` must have:

- a) An `ORDER BY`
- b) A name (alias), like `AS t` ✅
- c) A `GROUP BY`
- d) Exactly one row

**9.** A **correlated** subquery:

- a) Runs only once
- b) Uses a column from the outer query, so it runs once per outer row ✅
- c) Can only be used with `IN`
- d) Cannot use `AVG`

**10.** `WITH customer_totals AS (...) SELECT ... FROM customer_totals`
is called a:

- a) View
- b) Derived table
- c) CTE (Common Table Expression) ✅
- d) Self-join

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
