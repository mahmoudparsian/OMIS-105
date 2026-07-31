---
title: LIMIT vs RANK with Ties (Critical Concept)
author: OMIS 105 - Database Management Systems
marp: true
theme: default
paginate: true
class: lead
style: |
  section {
    justify-content: flex-start;
  }
---

# LIMIT vs RANK (Handling Ties)

---

# Scenario

After grouping by country:

| country | total_revenue |
|---------|---------------|
| USA     | 2800 |
| CANADA  | 2500 |
| ITALY   | 2500 |
| GERMANY | 2000 |

---

# Question

👉 “Show the top 2 countries by revenue”

---

# Using LIMIT 2

```sql
SELECT country, total_revenue
FROM revenue_table
ORDER BY total_revenue DESC
LIMIT 2;
```

---

# Possible Output (LIMIT)

| country | total_revenue |
|---------|---------------|
| USA     | 2800 |
| CANADA  | 2500 |

OR

| country | total_revenue |
|---------|---------------|
| USA     | 2800 |
| ITALY   | 2500 |

---

# ⚠️ Problem with LIMIT

- LIMIT returns ONLY 2 rows
- It does NOT understand ties
- It may exclude equally ranked rows

👉 Not deterministic for ties

---

# Using RANK()

```sql
SELECT
    country,
    total_revenue,
    RANK() OVER (ORDER BY total_revenue DESC) AS rnk
FROM revenue_table;
```

---

# RANK Output

| country | total_revenue | rnk |
|---------|---------------|-----|
| USA     | 2800 | 1 |
| CANADA  | 2500 | 2 |
| ITALY   | 2500 | 2 |
| GERMANY | 2000 | 4 |

---

# Now Filter Top 2 Ranks

```sql
WITH ranked AS (
    SELECT
        country,
        total_revenue,
        RANK() OVER (ORDER BY total_revenue DESC) AS rnk
    FROM revenue_table
)
SELECT *
FROM ranked
WHERE rnk <= 2;
```

---

# RANK Result

| country | total_revenue | rnk |
|---------|---------------|-----|
| USA     | 2800 | 1 |
| CANADA  | 2500 | 2 |
| ITALY   | 2500 | 2 |

---

# 🔥 Key Insight

## LIMIT 2 → returns 2 rows ONLY

## RANK <= 2 → returns ALL rows in top 2 ranks

👉 Includes ties

---

# Visual Comparison

| Method | Result |
|--------|--------|
| LIMIT 2 | 2 rows only |
| RANK <= 2 | 3 rows (includes ties) |

---

# Why This Matters

Business question:

> “Top 2 countries by revenue”

Interpretation:

- LIMIT → arbitrary cutoff ❌
- RANK → fair ranking ✅

---

# Real-World Example

If:
- 2 countries tie for second place

Should we:
- Drop one? ❌
- Include both? ✅

👉 RANK handles this correctly

---

# When to Use What

## Use LIMIT
- Quick preview
- Top N (no concern for ties)

## Use RANK
- Leaderboards
- Fair ranking
- Tie-aware analysis

---

# Final Mental Model

## LIMIT = cut rows

## RANK = respect ranking

## RANK handles ties correctly

---

# End
