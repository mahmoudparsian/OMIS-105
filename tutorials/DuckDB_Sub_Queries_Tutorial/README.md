# Jupyter/Notebook/DuckDB.

Create a Jupyter/Notebook/DuckDB (12 cells) 
to teach the fundamental concepts of sub-queries 
with using the "WITH" only. 

Render output of sql queries in a very nice high 
quality rendered tables (keep the rendering code outside)

for this create a 20 rows table (your choice) 

this is for students who have not used sub-queries at all. 

May be you can use ranking functions at the very end 
of this tutorial


built the notebook: Here's your 12-cell tutorial notebook! 

Here's what's inside:

**The Dataset** — A 20-row `employees` table with 
name, department, job title, salary, years of experience, 
hire year, and performance rating across 5 departments 
(Engineering, Marketing, HR, Finance, Sales).

**The 12 Cells:**

| # | Cell | What It Teaches |
|---|------|-----------------|
| 1 | Setup | Installs DuckDB; defines the `show()` rendering helper (kept separate, reused everywhere) |
| 2 | Dataset | Creates the 20-row `employees` table |
| 3 | Lesson 1 | *Why* `WITH` exists — readable vs. nested queries |
| 4 | Lesson 2 | Basic syntax: filter rows inside a CTE |
| 5 | Lesson 3 | Aggregate (`GROUP BY`) inside a CTE |
| 6 | Lesson 4 | Chain **two** CTEs with a comma |
| 7 | Lesson 5 | JOIN a CTE back to the base table |
| 8 | Lesson 6 | Three-CTE pipeline — step-by-step logic |
| 9 | Lesson 7 | Derive a column in CTE, then aggregate by it (salary bands) |
| 10 | Lesson 8 | `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` — compared side by side |
| 11 | Lesson 9 | The golden pattern: filter by rank using a CTE (impossible directly in `WHERE`) |
| 12 | Grand Finale | All concepts combined in one elegant 3-CTE query |

All SQL output renders via the styled `show()` helper — 
dark navy headers, alternating rows, hover highlights, 
and row counts.

