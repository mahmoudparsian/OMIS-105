# Week 9 Quiz — Ranking Functions

Questions 2–13 and 15 use the Week 9 lecture data: 12 `sales_reps` on 3 teams
(Session 1) and the café chain's `items`, `orders`, and `shops` (Session 2).
Ties: Ava and Fay (95), Ben and Chloe (88, both in East), Gus and Hal (60).

---

**1.** What can a window function do that `GROUP BY` cannot?

- a) Add up numbers
- b) Rank rows while **keeping every row** in the result ✅
- c) Sort the result
- d) Join two tables

**2.** Ava and Fay both have sales of 95, after three reps with higher
sales. What does `RANK() OVER (ORDER BY sales DESC)` give them?

- a) 4 and 5
- b) 4 and 4 ✅
- c) 3 and 3
- d) 1 and 1

**3.** In the same ranking, Ben (88) comes right after Ava and Fay. What is
Ben's `RANK()`?

- a) 5
- b) 6 ✅
- c) 4
- d) 7

**4.** With `DENSE_RANK()` instead, what is Ben's rank?

- a) 5 ✅
- b) 6
- c) 4
- d) 7

**5.** Which statement about `ROW_NUMBER()` is true?

- a) Tied rows get the same number
- b) Tied rows get different numbers, and without a tie-breaker the order
  between them can change from run to run ✅
- c) It skips numbers after a tie
- d) It only works with `PARTITION BY`

**6.** Why write `ROW_NUMBER() OVER (ORDER BY sales DESC, rep_name)`
instead of just `ORDER BY sales DESC`?

- a) `rep_name` makes the query faster
- b) `rep_name` breaks ties, so the numbering is the same every time ✅
- c) It sorts the final result by name
- d) `ROW_NUMBER` needs two columns

**7.** What does `PARTITION BY team` do inside `OVER (...)`?

- a) It removes duplicate teams
- b) It restarts the numbering or ranking at 1 for each team ✅
- c) It groups the rows into one row per team, like `GROUP BY`
- d) It sorts the teams by name

**8.** A query asks for "the top rep in each team" with
`ROW_NUMBER() OVER (ORDER BY sales DESC, rep_name) = 1` — but **without**
`PARTITION BY`. How many rows does it return?

- a) 3 — one per team
- b) 12
- c) 1 ✅
- d) 0

**9.** `SELECT ..., ROW_NUMBER() OVER (...) AS rn FROM sales_reps WHERE rn = 1`
fails with *"WHERE clause cannot contain window functions!"* Why?

- a) `rn` is a reserved word
- b) `WHERE` is applied before window functions are computed, so `rn` does
  not exist yet ✅
- c) `ROW_NUMBER` needs `GROUP BY`
- d) Window functions cannot be given a name with `AS`

**10.** What is the correct way to keep only the top 2 reps per team?

- a) Add `LIMIT 2` to the query
- b) Compute the ranking in a subquery or CTE, then filter `rn <= 2`
  outside it ✅
- c) Put `rn <= 2` inside the `OVER (...)`
- d) Use `HAVING rn <= 2`

**11.** "Top 2 per team" with `RANK()` returns **7** rows, not 6. Why?

- a) `RANK` always returns one extra row
- b) In East, Ben and Chloe tie at 88 and both get rank 2 ✅
- c) One team has 7 reps
- d) `RANK` ignores `PARTITION BY`

**12.** The café's prices from the top are 6.00, 6.00, 5.50, 5.50, 4.50, …
Which function, filtered to `= 2`, finds the items with the
**second-highest price**?

- a) `ROW_NUMBER()`
- b) `RANK()`
- c) `DENSE_RANK()` ✅
- d) Any of the three

**13.** With the same prices, what does `RANK() ... = 2` return?

- a) The two 5.50 items
- b) One of the 6.00 items
- c) No rows — the two 6.00 items share rank 1, so the next rank is 3 ✅
- d) An error

**14.** Which question is answered best with `ROW_NUMBER()`?

- a) "Which products have the 3rd-highest price?"
- b) "Show each customer's **first** order" ✅
- c) "Which stores are in the top 3, including ties?"
- d) "How many price levels are there?"

**15.** Gus and Hal (60) have the lowest sales of all 12 reps. Over **all**
reps (no `PARTITION BY`), what are their `RANK()` and `DENSE_RANK()`?

- a) 11 and 9 ✅
- b) 11 and 11
- c) 12 and 9
- d) 9 and 11

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
