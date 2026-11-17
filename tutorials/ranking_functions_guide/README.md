# Ranking Functions Guide (DuckDB)

Eight short reading guides on SQL **ranking functions**: `ROW_NUMBER()`,
`RANK()`, `DENSE_RANK()`, and `PERCENT_RANK()`. Every example runs in
**DuckDB 2.0**, and every result table is real DuckDB output.

Best fit: **Week 9 — Ranking Functions**.

## Reading order

| # | File | What you learn |
|---|------|----------------|
| 1 | [`1.ranking_functions_tutorial.md`](1.ranking_functions_tutorial.md) | The three ranking functions side by side, with and without `PARTITION BY` |
| 2 | [`2.grouping_aggregation_ranking.md`](2.grouping_aggregation_ranking.md) | `GROUP BY` + aggregates first, then rank the groups; two-level grouping with CTEs |
| 3 | [`3.RANK_function.md`](3.RANK_function.md) | `RANK()` in depth: top/bottom performer per year, `QUALIFY`, top-3 per year with a join |
| 4 | [`4.Ranking_Functions_in_DuckDB.md`](4.Ranking_Functions_in_DuckDB.md) | `DENSE_RANK()`, `PERCENT_RANK()`, `ROW_NUMBER()`; a leaderboard with country and global ranks |
| 5 | [`5.Ranking_Functions_Examples.md`](5.Ranking_Functions_Examples.md) | Six analytics (OLAP) queries on a star schema: `RANK`, `DENSE_RANK`, `ROW_NUMBER`, `QUALIFY`, `LAG` |
| 6 | [`6.Ranking_Functions_with_Examples.md`](6.Ranking_Functions_with_Examples.md) | Many examples on one `ExamResult` table, ending with all four functions in one query |
| 7 | [`7.ranking_functions_by_cat_tricks.md`](7.ranking_functions_by_cat_tricks.md) | A small lab: 3 queries each for `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` |
| 8 | [`8.row_number_tutorial.md`](8.row_number_tutorial.md) | `ROW_NUMBER()` for top-N, latest record, pagination, and removing duplicates |

## How to try the examples

Open DuckDB (the CLI, qStudio, or a Marimo notebook) and run the
`CREATE OR REPLACE TABLE` and `INSERT` blocks of a guide first, then
its queries, in order. Each guide is self-contained.

## Two habits these guides use everywhere

* **End with `ORDER BY`.** The `ORDER BY` inside `OVER (...)` decides
  the ranks. It does **not** sort the output. Without a final
  `ORDER BY`, DuckDB may return the rows in any order.
* **Add a tie-breaker to `ROW_NUMBER()`.** When two rows tie, which one
  gets the smaller number is up to the database, unless you add another
  column, e.g. `ROW_NUMBER() OVER (ORDER BY score DESC, student_id)`.

## See also

* [`../ranking_functions_notebooks/`](../ranking_functions_notebooks/): Marimo notebooks on the same functions
* [`../LIMIT_vs_RANK/`](../LIMIT_vs_RANK/): why `LIMIT` can't answer top-N questions when there are ties
* [`../deduplication/`](../deduplication/): deleting duplicate rows with `ROW_NUMBER()`

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
