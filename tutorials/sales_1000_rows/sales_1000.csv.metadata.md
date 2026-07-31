# Flagship Dataset: Retail Sales (1000 Rows)

## Overview
This dataset simulates a messy real-world retail (e-commerce) dataset.

It is intentionally designed for teaching:
- SQL querying
- Data cleaning
- Aggregation
- JOINs
- Normalization

---

## Table: sales_raw

| Column | Description |
|--------|------------|
| order_id | Transaction ID (NOT unique) |
| order_date | Date in inconsistent formats |
| customer_name | Customer name (inconsistent / missing) |
| product | Product name |
| category | Product category |
| price | Price (may include `$` or be numeric) |
| quantity | Quantity (numeric or text like 'two') |
| discount | Discount percentage (string, may be empty) |
| country | Country (inconsistent casing) |
| status | Order status (shipped, pending, delivered) |

---

## Data Issues (Intentional)

This dataset includes realistic problems:

- Duplicate order_ids
- Missing customer names
- Inconsistent date formats
- Mixed data types (strings vs numbers)
- Inconsistent country casing
- Optional / missing discount values

---

## Usage by Week

- Week 1–2: Explore data
- Week 3: SELECT, WHERE
- Week 4: GROUP BY
- Week 5: Normalize + JOIN
- Week 6: Design improvements
- Week 7–8: Performance & transactions
- Week 9: Project extension

---

## Learning Goal

Students learn that:
> Real data is messy — and databases help organize it.

