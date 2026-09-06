A Streamlit + DuckDB app that teaches `INNER`, `LEFT`, `RIGHT`, and
`FULL OUTER` JOIN — with seed data deliberately chosen to make the
Cartesian-product behavior of a JOIN impossible to miss.

**Schema:** two tables, `employees` and `projects`, linked by `dept_id`.

| dept_id | employees (left) | projects (right) | INNER JOIN rows |
|---|---|---|---|
| 10 | Alice, Bob (2) | Alpha, Beta, Gamma (3) | **2 × 3 = 6** |
| 20 | Charlie (1) | Delta (1) | 1 |
| 30 | Diana (1) | — (0) | LEFT-only |
| 40 | — (0) | Epsilon (1) | RIGHT-only |

That one table covers every case: a Cartesian-product department, a
simple 1:1 match, an unmatched left row, and an unmatched right row.

**Tabs:**

1. **Manage Data** — add/remove employees and projects, reset to the seed data
2. **INNER JOIN**
3. **LEFT JOIN**
4. **RIGHT JOIN**
5. **FULL OUTER JOIN**
6. **SQL Explorer** — pre-loaded examples (CROSS JOIN, self-join, join multiplier), plus free-form queries

Every join tab shows the left and right tables side by side, the exact
SQL, and the result with unmatched (`NULL`) rows highlighted.

Run it with:

```bash
pip install -r requirements.txt
streamlit run app_joins.py
```
