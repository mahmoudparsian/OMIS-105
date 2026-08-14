# 🏬 Superstore Sales

**OMIS-105 · Week 4 — SQL Aggregation**

**The aggregation workhorse of this folder — 74 `GROUP BY` clauses across eleven
analysis sections.** A retail order dataset with enough dimensions (category, region,
segment, ship mode, state, time) that almost any grouping question has a real answer.

If you assign one Week 4 story, make it this one.

---

## Run it

```bash
marimo edit superstore-sales-1-marimo.py    # ← use this one
```

| File | Role |
|---|---|
| `superstore-sales-1-marimo.py` | **The notebook to use** |
| `superstore-sales-2-marimo.py` | Same analysis, different formatting — see below |
| `superstore_plots.py` | All chart functions, kept out of the notebook |
| `sample_superstore.csv` | **10,194 orders** |

> ⚠️ **The two notebooks are duplicates.** Same sections, same queries, same
> conclusions — they differ only in code formatting. Use
> `superstore-sales-1-marimo.py`: it sets `sql_output="pandas"`, which is what the
> plotting functions expect. Assign one, not both.

---

## The data

One row per order line, with 21 columns spanning several natural groupings:

| Dimension | Columns |
|---|---|
| **Time** | Order Date, Ship Date |
| **Geography** | Country/Region, City, State/Province, Postal Code, Region |
| **Customer** | Customer ID, Customer Name, Segment |
| **Product** | Product ID, Category, Sub-Category, Product Name |
| **Logistics** | Ship Mode |
| **Measures** | Sales, Quantity, Discount, **Profit** |

---

## What it covers

| § | Section | Grouped by |
|---|---|---|
| 1 | Data overview | — |
| 2 | Category & sub-category analysis | Product hierarchy |
| 3 | Regional analysis | Region |
| 4 | Segment & shipping analysis | Customer segment, ship mode |
| 5 | Time series analysis | Order date |
| 6 | Customer analysis | Customer |
| 7 | **Discount impact analysis** | Discount band |
| 8 | Scatter & correlation | — |
| 9 | Product analysis | Product |
| 10 | State-level analysis | State |
| 11 | Advanced queries | mixed |

---

## The finding worth building a lesson around

**Sales and profit are different measures, and grouping reveals it.** Some
sub-categories sell heavily and lose money — because the discounts required to move
them exceed the margin.

```sql
SELECT "Sub-Category",
       SUM(Sales)  AS sales,
       SUM(Profit) AS profit
FROM superstore
GROUP BY "Sub-Category"
ORDER BY profit ASC;          -- the losers come first
```

A student who has only ever grouped by one measure will assume the best-selling
category is the best category. This dataset proves otherwise in one query, and §7
(discount impact) explains why.

That is a genuinely valuable business-analytics lesson, not just a SQL one.

---

## A note on scope

The profile of this notebook shows **22 window functions and 14 CTEs**, mostly in the
later sections. Those techniques are not taught in the 10-week core (see the outline's
optional Advanced SQL appendix).

Sections 1–7 are solid Week 4 material. Treat 8–11 as demonstration, or as reading for
students who want more — but not as assessed work unless you have taught the
techniques first.

---

## Teaching notes

- **Column names contain spaces and slashes** (`"Sub-Category"`, `"Country/Region"`),
  so they must be double-quoted in SQL. Annoying, realistic, and worth ten seconds of
  explanation before students hit the error themselves.
- Start with §2 and ask for the *most profitable* category before anyone runs
  anything. Then run it. The gap between intuition and result is the hook.
- Pairs naturally with `video_game_sales/` — both are sales data, both reward
  grouping, and the regional split in one mirrors the category split in the other.
