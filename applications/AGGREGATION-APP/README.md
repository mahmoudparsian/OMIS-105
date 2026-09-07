Two Streamlit + DuckDB apps that teach SQL's aggregate functions and
`GROUP BY` — every tab pairs the aggregate with `STRING_AGG`/`LIST` so
students can see exactly which rows were collapsed into each group.

| App | Schema | Focus |
|---|---|---|
| [`app_aggregation_single.py`](app_aggregation_single.py) | one table, `employees` (from `employees.csv`) | Aggregating a single table |
| [`app_aggregation_3_tables.py`](app_aggregation_3_tables.py) | three tables — `customers`, `products`, `orders` | Aggregating across a join |

**Tabs (both apps):**

1. **View Data** — the raw table(s)
2. **COUNT** — `COUNT(*)` vs `COUNT(DISTINCT ...)`
3. **SUM / AVG**
4. **MIN / MAX**
5. **STRING_AGG / LIST** — see the actual rows behind each aggregate
6. **HAVING** — filtering on an aggregated value
7. **Multi-Column GROUP BY** *(single-table app only)*
8. **SQL Explorer** — free-form practice

Run either app with:

```bash
pip install streamlit duckdb pandas
streamlit run app_aggregation_single.py
# or
streamlit run app_aggregation_3_tables.py
```
