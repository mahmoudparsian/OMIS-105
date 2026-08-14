# 🛒 FreshCart — Grocery Analytics

**OMIS-105 · Week 6 — Database Design** *(→ also Week 9, project integration)*

An omnichannel grocer's analytics database, built from a written business
requirement. **The most complete end-to-end story in this folder**: a stated business
need, a schema designed to serve it, and 74 queries answering it.

---

## Run it

```bash
marimo edit freshcart_duckdb_notebook_marimo.py
```

| File | Role |
|---|---|
| `freshcart_duckdb_notebook_marimo.py` | The notebook |
| `freshcart_helpers.py` | Display and chart helpers |
| `freshcart_data_story_package.md` | **The business story, schema and query set — read first** |

The data is **generated inside the notebook**, so there are no CSVs to manage and the
notebook is self-contained.

---

## The business story

> FreshCart is a mid-sized omnichannel grocer operating in the USA, Canada, India and
> Germany. Customers shop both online and in-store, mixing weekly staples with impulse
> items. Leadership wants to know which products drive repeat purchases, how
> seasonality changes basket composition, and which customer segments respond best to
> promotions.

The KPIs are named up front: revenue, average order value, units per order, and
customer lifetime value.

**Everything in the schema exists to serve one of those.** That is what makes this a
design story rather than a query story.

---

## The schema

Three tables — `customers`, `products`, `orders` — with `orders` as the fact table
carrying the product, quantity, price *at time of purchase*, and channel.

Two design decisions are worth discussing:

**1 · Price is stored on the order, not just on the product.**

- Prices change over time.
- If you only kept `products.price`, last year's revenue would be recalculated at
  **today's** prices every time you ran the report.
- Storing the price paid **freezes history** — the order remembers what the customer
  actually paid.
- This is one of the most commonly missed points in schema design, and here it is
  explicit.

**2 · Each order is a single line item.**

- The package says so on purpose: *"to keep the model compact"*.
- **What it buys:** a much simpler schema.
- **What it costs:** "how many items were in that basket?" becomes harder to answer.
- The document even names the way out — multi-line orders, inventory, promotions.

Being able to point at a **documented, deliberate** simplification is worth more than
a perfect schema with no rationale.

---

## Scope

The notebook contains **43 joins, 42 `GROUP BY`s, 18 CTEs and 18 window functions** —
by far the densest in this folder.

- The joins and `GROUP BY`s are fine from Week 5 onward.
- The **CTEs and window functions go beyond the 10-week core** (see the outline's
  optional Advanced SQL appendix).

| Use it for | In week |
|---|---|
| Reading the requirement and critiquing the schema | **6** |
| An end-to-end worked example | **9** |
| Query practice | only after the techniques are taught |

---

## Teaching notes

- **Hand out the business story with the schema removed** and ask students to design
  the tables. Then compare with what is there. The price-on-order decision is the one
  almost nobody gets, and that makes it memorable.
- The package includes a MySQL schema; the notebook runs DuckDB. Comparing them is a
  short, concrete look at dialect differences.
- Pairs with `emps_depts_projects/` (TechNova), which uses the same
  business-story-first structure at smaller scale.
