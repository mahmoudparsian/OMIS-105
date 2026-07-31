# Longest-Serving President by Political Party

## What does this query do?

This query finds **the president who served the longest term for each political party**.

For example:

| Party | President | Days in Office |
|---------|---------|---------|
| Democratic | Franklin D. Roosevelt | 4,422 |
| Republican | Dwight D. Eisenhower | 2,922 |
| ... | ... | ... |

---

## SQL Query

```sql
WITH terms AS (
    SELECT p.sequence,
           p.first_name || ' ' || p.last_name AS president,
           pt.party_name,
           (p.term_end - p.term_start) AS days_in_office
    FROM presidents p
    JOIN parties pt ON p.party_id = pt.party_id
),
ranked AS (
    SELECT *,
           RANK() OVER (
               PARTITION BY party_name
               ORDER BY days_in_office DESC
           ) AS rnk
    FROM terms
)
SELECT party_name, president, days_in_office
FROM ranked
WHERE rnk = 1
ORDER BY days_in_office DESC;
```

---

## Step 1: Build the `terms` Table

```sql
WITH terms AS (
    SELECT p.sequence,
           p.first_name || ' ' || p.last_name AS president,
           pt.party_name,
           (p.term_end - p.term_start) AS days_in_office
    FROM presidents p
    JOIN parties pt ON p.party_id = pt.party_id
)
```

### What happens here?

We join the `presidents` table with the `parties` table and calculate how many days each president served.

### Example

#### presidents

| first_name | last_name | party_id | term_start | term_end |
|------------|------------|-----------|------------|----------|
| George | Washington | 1 | 1789-04-30 | 1797-03-04 |
| Franklin | Roosevelt | 2 | 1933-03-04 | 1945-04-12 |

#### parties

| party_id | party_name |
|-----------|-------------|
| 1 | Independent |
| 2 | Democratic |

Result of `terms`:

| president | party_name | days_in_office |
|------------|------------|---------------|
| George Washington | Independent | 2865 |
| Franklin Roosevelt | Democratic | 4422 |

---

## Step 2: Rank Presidents Within Each Party

```sql
ranked AS (
    SELECT *,
           RANK() OVER (
               PARTITION BY party_name
               ORDER BY days_in_office DESC
           ) AS rnk
    FROM terms
)
```

### What is happening?

The `RANK()` window function ranks presidents **within each political party**.

```sql
PARTITION BY party_name
```

means:

> Start a separate ranking for each party.

```sql
ORDER BY days_in_office DESC
```

means:

> The president with the most days in office receives rank 1.

### Example

Suppose the Democratic Party has:

| president | days_in_office |
|------------|---------------|
| Franklin Roosevelt | 4422 |
| Harry Truman | 2814 |
| Jimmy Carter | 1461 |

After applying `RANK()`:

| president | days_in_office | rnk |
|------------|---------------|-----|
| Franklin Roosevelt | 4422 | 1 |
| Harry Truman | 2814 | 2 |
| Jimmy Carter | 1461 | 3 |

A separate ranking starts for each party.

---

## Step 3: Keep Only the Winners

```sql
SELECT party_name, president, days_in_office
FROM ranked
WHERE rnk = 1
```

This means:

> Keep only the presidents ranked #1 in their party.

In other words:

> Keep the longest-serving president from each political party.

---

## Step 4: Sort the Final Result

```sql
ORDER BY days_in_office DESC
```

This displays the party winners from longest service to shortest service.

---

## Visual Summary

```text
presidents
     +
parties
     |
     v
+------------------+
| terms            |
| president        |
| party_name       |
| days_in_office   |
+------------------+
     |
     v
RANK() OVER (
  PARTITION BY party
  ORDER BY days DESC
)
     |
     v
+------------------+
| ranked           |
| president        |
| party_name       |
| days_in_office   |
| rnk              |
+------------------+
     |
     v
WHERE rnk = 1
     |
     v
Longest-serving president
for each political party
```

---

## Key Concepts Learned

1. **CTE (`WITH`)** creates temporary result sets.
2. **JOIN** combines data from multiple tables.
3. **Window Functions** perform calculations across related rows.
4. **RANK()** assigns rankings within groups.
5. **PARTITION BY** creates independent ranking groups.
6. **ORDER BY** inside a window function determines the ranking order.
7. **WHERE rnk = 1** selects the top-ranked row(s) from each group.

---

## Plain-English Description

> For each political party, find the president who served the greatest number of days in office, and display those presidents from longest service to shortest service.
