# Deduplicating Rows in DuckDB Using `ROW_NUMBER()`

In DuckDB, the cleanest way to deduplicate rows using `ROW_NUMBER()` is with the **`QUALIFY` clause**, which filters window function results directly without requiring an extra CTE or subquery.

## 1. Create a Sample Table with Duplicate Rows

```sql
CREATE OR REPLACE TABLE user_events (
    event_id    INTEGER,
    user_id     INTEGER,
    event_type  VARCHAR,
    updated_at  TIMESTAMP
);

INSERT INTO user_events VALUES
    (101, 1, 'login',    '2026-11-17 09:00:00'),
    (101, 1, 'login',    '2026-11-17 09:00:05'), -- Duplicate event_id (newer timestamp)
    (102, 2, 'purchase', '2026-11-17 09:15:00'),
    (103, 1, 'logout',   '2026-11-17 09:30:00'),
    (103, 1, 'logout',   '2026-11-17 09:30:00'), -- Exact duplicate row
    (103, 1, 'logout',   '2026-11-17 09:31:10'); -- Duplicate event_id (newest timestamp)
```

## 2. Deduplicate Using `ROW_NUMBER()` + `QUALIFY` (Recommended in DuckDB)

Partition by the unique key (`event_id`) and order by `updated_at DESC` so the most recent record receives `rn = 1`:

```sql
SELECT *
FROM user_events
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY event_id
    ORDER BY updated_at DESC
) = 1
ORDER BY event_id;
```

**Output:**

| event_id | user_id | event_type | updated_at |
| :--- | :--- | :--- | :--- |
| 101 | 1 | login | 2026-11-17 09:00:05 |
| 102 | 2 | purchase | 2026-11-17 09:15:00 |
| 103 | 1 | logout | 2026-11-17 09:31:10 |

## 3. Standard ANSI SQL Equivalent (Using a CTE + `EXCLUDE`)

If you prefer a standard CTE instead of `QUALIFY`, DuckDB's `EXCLUDE` keyword drops the helper `rn` column cleanly:

```sql
WITH ranked_events AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY event_id
            ORDER BY updated_at DESC
        ) AS rn
    FROM user_events
)
SELECT * EXCLUDE (rn)
FROM ranked_events
WHERE rn = 1
ORDER BY event_id;
```

## How It Works

* **`PARTITION BY event_id`**: Groups identical keys into separate windows (`101`, `102`, `103`).
* **`ORDER BY updated_at DESC`**: Ranks the newest record first (`1`). Use `ASC` if you want to keep the earliest record instead.
* **`QUALIFY ... = 1`**: Filters out every row assigned `2`, `3`, etc., without adding a `rn` column to the output schema.