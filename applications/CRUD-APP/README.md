Two Streamlit + DuckDB apps that teach CRUD (Create, Read, Update,
Delete) operations against a single `customers` table.

**Schema:** `customers` (customer_id, customer_name, gender, country,
customer_email, date_created) — customer_id and date_created are set
automatically by the app.

| App | Adds | Tabs |
|---|---|---|
| [`app_v1_basic.py`](app_v1_basic.py) | The basics | Create, View, Search (by email), Delete |
| [`app_v2_with_update.py`](app_v2_with_update.py) | Update, plus a SQL cheat sheet | Create, View, Search, **Update**, Delete, **SQL Explorer** |

Start with `app_v1_basic.py` to see Create/Read/Delete in isolation,
then move to `app_v2_with_update.py` once Update is introduced.

Run with:

```bash
pip install -r requirements.txt
streamlit run app_v1_basic.py
# or
streamlit run app_v2_with_update.py
```
