Option 1 (Aggregation): also enable GROUP_CONCAT and other similar functions so students can see what is agrregated per key in Group BY.

Here's what's in the app — the core idea is that **every aggregation tab shows STRING_AGG or LIST alongside the aggregate function** so students can see exactly what's being collapsed:

**Schema:** 6 customers, 8 products (across Electronics, Furniture, Stationery), and 17 orders — enough data to make grouping interesting without being overwhelming.

**Tabs:**

1. **View Data** — All three raw tables plus a joined "detail view" that flattens orders + customers + products into one table with `line_total`. This is the reference students check against.

2. **COUNT** — Pick a GROUP BY column from a dropdown. The result shows `COUNT(*)`, `COUNT(DISTINCT ...)`, and `STRING_AGG` of what's being counted. Raw rows on the left, aggregated on the right.

3. **SUM / AVG** — Same side-by-side layout. The `line_details` column shows each product with its quantity and dollar amount (e.g., `Laptop (qty 1 = $999.99), Mouse (qty 2 = $59.98)`) so students can manually add them up and verify the SUM.

4. **MIN / MAX** — Shows `LIST(price ORDER BY price)` alongside MIN and MAX so students see the sorted list and can confirm the endpoints.

5. **STRING_AGG / LIST** — The star tab. Compares `STRING_AGG` vs `LIST`, with and without `DISTINCT`, and includes a reference table comparing function names across DuckDB, MySQL (`GROUP_CONCAT`), and PostgreSQL (`ARRAY_AGG`).

6. **HAVING** — Students pick an aggregate function, operator, and threshold value. Shows ALL groups on the left vs filtered groups on the right, plus a WHERE vs HAVING comparison table.

7. **SQL Explorer** — Pre-loaded examples include revenue by customer, monthly summary, cross-tab (customer × category spending with CASE WHEN), and products never ordered.

Run it with: `streamlit run app_aggregation.py`
