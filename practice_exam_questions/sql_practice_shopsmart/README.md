# SQL Practice 02: ShopSmart Database (DuckDB)

100 practice queries with answers for **Weeks 6-10**, on the multi-table
ShopSmart e-commerce database used in the Week 6-10 labs.
Every query and result was validated with DuckDB v1.5.5.

| File | Coverage |
|------|----------|
|[`sql_practice_level_1.md`](./sql_practice_level_1.md)| Weeks 6-8: 50 queries — JOIN warm-up, keys & constraints, normalization, query plans & indexes, transactions & ACID |
|[`sql_practice_level_2.md`](./sql_practice_level_2.md)| Weeks 9-10: 50 queries — views, multi-table business reports, sub-queries & set operations, window functions, final-review analytics |
|[`create_shopsmart_db.sql`](./create_shopsmart_db.sql)| Builds the database: schema with PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, and NOT NULL constraints, then loads the CSV files |
|[`data/`](./data)| The 10 CSV files (9 ShopSmart tables + `orders_denormalized.csv` for normalization practice) |

For Weeks 1-5, see [`../sql_practice_insurance/`](../sql_practice_insurance).


## 1. Build the Database

From this folder:

```bash
duckdb shopsmart.duckdb < create_shopsmart_db.sql
```

The script prints the row count of every table:

```
┌─────────────────────┬──────────┐
│     table_name      │ num_rows │
│       varchar       │  int64   │
├─────────────────────┼──────────┤
│ categories          │        8 │
│ customers           │       40 │
│ suppliers           │       10 │
│ products            │       64 │
│ orders              │      200 │
│ order_items         │      607 │
│ product_suppliers   │       90 │
│ reviews             │      150 │
│ shipping            │      141 │
│ orders_denormalized │      100 │
└─────────────────────┴──────────┘
```

Then open the database and start practicing:

```bash
duckdb shopsmart.duckdb
```

Re-running `create_shopsmart_db.sql` rebuilds everything from the CSV
files, so you can always reset the database after practicing.


## 2. Tables and Relationships

```
categories 1──M products M──M suppliers        (through product_suppliers)
customers  1──M orders   1──M order_items M──1 products
customers  1──M reviews  M──1 products
orders     1──1 shipping                        (an order has at most one shipment)
```

| Table | Columns |
|-------|---------|
| `categories` | `category_id` (PK), `category_name`, `description` |
| `customers` | `customer_id` (PK), `first_name`, `last_name`, `email` (UNIQUE), `city`, `state`, `join_date` |
| `suppliers` | `supplier_id` (PK), `supplier_name`, `email`, `city`, `state`, `partner_since` |
| `products` | `product_id` (PK), `product_name`, `category_id` (FK), `price`, `stock_quantity` |
| `orders` | `order_id` (PK), `customer_id` (FK), `order_date`, `status` (processing / shipped / completed / cancelled), `total_amount` |
| `order_items` | `item_id` (PK), `order_id` (FK), `product_id` (FK), `quantity`, `unit_price` |
| `product_suppliers` | `product_id` + `supplier_id` (composite PK, both FKs), `cost_price` |
| `reviews` | `review_id` (PK), `product_id` (FK), `customer_id` (FK), `rating` (1-5), `review_text`, `review_date` |
| `shipping` | `shipping_id` (PK), `order_id` (FK, UNIQUE), `carrier`, `ship_date`, `delivery_date` (NULL = in transit), `shipping_cost` |
| `orders_denormalized` | one row per order line, repeating order, customer, and product data — no keys on purpose |


## 3. Things to Know About the Data

* Orders run from 2024-01-01 to 2025-02-04.
* `orders.total_amount` does **not** equal the sum of the order's
  `quantity * unit_price` (Level 2, Q43). The practice files define
  **revenue** as the sum of line items for orders that are not cancelled.
* `processing` and `cancelled` orders have no shipping record; `shipped`
  orders have a ship date but no delivery date yet.


## 4. DuckDB Notes for Weeks 7-8

* With tables this small, `EXPLAIN` shows sequential scans even when an
  index exists — DuckDB uses an index only when it pays off.
* Inside `BEGIN TRANSACTION`, a failed statement aborts the transaction:
  later statements are refused, and `COMMIT` saves nothing.
* DuckDB does **not** support `SAVEPOINT`.
* DuckDB cannot `UPDATE` a `UNIQUE` or key column of a row that other
  tables reference through a foreign key (for example,
  `customers.email` of a customer who has orders).
