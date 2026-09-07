A Streamlit + DuckDB app that teaches `ROW_NUMBER`, `RANK`, and `DENSE_RANK` —
and how ties make them behave differently.

**Schema:** one table, `player_scores` (player, country, score), loaded from
`players.csv`.

**Tabs:**

1. **View Data** — the full table, plus a tie summary
2. **ROW_NUMBER** — unique sequential number, no gaps, no ties
3. **RANK** — ties share a rank, then a gap appears
4. **DENSE_RANK** — ties share a rank, no gap
5. **Compare All Three** — side-by-side in one query
6. **PARTITION BY** — ranking within groups (e.g., per country)
7. **SQL Explorer** — free-form practice

Run it with:

```bash
pip install streamlit duckdb pandas
streamlit run app_ranking.py
```
