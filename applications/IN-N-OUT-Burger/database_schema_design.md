# In-N-Out POS — Database Schema Design

**Course:** OMIS-105 Introduction to DBMS · Santa Clara University
**Engine:** DuckDB (a single-file analytical SQL database)
**Design goal:** a fully **normalized** relational model that is realistic
enough to feel like a real point-of-sale system, yet small enough to read in
one sitting. The same tables serve two very different jobs — recording live
transactions (the register) and answering analytical questions (the
dashboard).

---

## 1. The big picture

The schema has ten tables that fall into two groups.

**Reference (lookup) tables** describe the menu. They change rarely and are
written mostly by `build_db.py` (and by the "Add a store" form). They answer
the question *"what can be sold, and for how much?"*

- `stores`
- `menu_categories`
- `sizes`
- `menu_items`
- `item_prices`
- `modifiers`
- `combos`

**Transaction tables** record what customers actually bought. They grow every
time the register places an order. They answer the question *"what was sold,
when, where, and how was it customized?"*

- `orders`
- `order_items`
- `order_item_modifiers`

A useful way to read the model: the reference tables are the *nouns* of the
business, and the transaction tables are the *events* that connect those nouns
together at a moment in time.

---

## 2. Relationship map

```
menu_categories ──1:M──┐
                       ▼
sizes ──1:M──► item_prices ◄──M:1── menu_items ──1:M──► combos
                                          │   ▲              │
                                          │   └──────────────┘ (combo's headline burger)
                                          │
stores ──1:M──► orders ──1:M──► order_items ──1:M──► order_item_modifiers
                                   ▲   ▲   ▲                  ▲
                                   │   │   │                  │
                          menu_items  combos  sizes        modifiers
                          (an item line) (a combo line) (M:1)  (M:1)
```

Read the arrows as **"one parent has many children."** For example, one
`orders` row has many `order_items`; one `menu_items` row can appear on many
`order_items`.

The two **many-to-many** relationships in the business are resolved with
**bridge (junction) tables**, which is the heart of relational design:

- *Items priced at multiple sizes* → resolved by `item_prices`
  (one row per item-and-size combination).
- *Order lines carrying multiple customizations* → resolved by
  `order_item_modifiers` (one row per line-and-modifier combination).

---

## 3. Keys, in plain language

- A **primary key (PK)** uniquely identifies a row. Most tables use a
  **surrogate key** — a meaningless integer like `order_id` — because it never
  changes and is easy for foreign keys to point at.
- A **foreign key (FK)** is a column that holds the primary key of another
  table, creating the link between them. The database refuses to insert an
  `order_items` row whose `order_id` doesn't exist in `orders`; this is
  **referential integrity**.
- A **business (natural) key** is a value that means something to humans.
  `orders.transaction_id` (e.g. `INO-01-20260618-00042`) is the receipt number
  a cashier reads aloud. We keep it *alongside* the surrogate `order_id` rather
  than using it as the PK, so the human-facing identifier and the internal
  plumbing are decoupled. This surrogate-vs-business-key contrast is one of the
  main teaching points of the schema.

---

## 4. Table-by-table reference

### 4.1 `stores`
Which restaurant rang up an order.

| Column | Type | Notes |
|---|---|---|
| `store_id` | INTEGER | **PK** (surrogate) |
| `store_name` | VARCHAR | e.g. "In-N-Out #214 – Santa Clara" |
| `city` | VARCHAR | |
| `state` | VARCHAR | |

Parent of `orders`. New stores are added at runtime via the Stores page
(`store_id = max(store_id) + 1`).

---

### 4.2 `menu_categories`
The top-level menu groupings: Burgers, Sides, Beverages, Shakes.

| Column | Type | Notes |
|---|---|---|
| `category_id` | INTEGER | **PK** |
| `category_name` | VARCHAR | `UNIQUE` |
| `sort_order` | INTEGER | controls display order |

Parent of `menu_items`.

---

### 4.3 `sizes`
The sizes a sellable item can come in.

| Column | Type | Notes |
|---|---|---|
| `size_id` | INTEGER | **PK** |
| `size_name` | VARCHAR | `UNIQUE` — Regular, Small, Medium, Large, X-Large |
| `sort_order` | INTEGER | |

`Regular` is the single size used by burgers, fries, shakes, coffee and milk.
Fountain drinks use the four graduated sizes. Modeling *every* item as
having a size (even if it's just "Regular") keeps `order_items` uniform — every
line references exactly one `size_id`.

---

### 4.4 `menu_items`
Every individually sellable thing, including the secret-menu burgers.

| Column | Type | Notes |
|---|---|---|
| `item_id` | INTEGER | **PK** |
| `category_id` | INTEGER | **FK** → `menu_categories` |
| `item_name` | VARCHAR | |
| `description` | VARCHAR | shown on the POS cards |
| `is_secret_menu` | BOOLEAN | flags Flying Dutchman, Grilled Cheese |

Note what is **not** a `menu_items` row: "Animal Style Fries" is not stored as
a separate product. It is `French Fries` (an item) **plus** the `Animal Style`
modifier. That keeps the menu small and avoids duplicating every fries variant
— another normalization payoff.

---

### 4.5 `item_prices`  *(bridge table)*
The price of a given item **at a given size**.

| Column | Type | Notes |
|---|---|---|
| `item_id` | INTEGER | **PK part 1**, **FK** → `menu_items` |
| `size_id` | INTEGER | **PK part 2**, **FK** → `sizes` |
| `price` | DECIMAL(6,2) | |

The **composite primary key** `(item_id, size_id)` is the classic many-to-many
resolution: a burger has one row (at Regular), a fountain drink has four rows
(Small/Medium/Large/X-Large). Price lives here — *not* on `menu_items` —
because the same product legitimately has different prices at different sizes.

---

### 4.6 `modifiers`
The "Not So Secret Menu" customizations and paid extras.

| Column | Type | Notes |
|---|---|---|
| `modifier_id` | INTEGER | **PK** |
| `modifier_name` | VARCHAR | `UNIQUE` |
| `description` | VARCHAR | |
| `price_delta` | DECIMAL(6,2) | added to the line; many are 0.00 |
| `applies_to` | VARCHAR | `'burger'`, `'fries'`, or `'any'` |

Examples: Animal Style ($0.00), Protein Style ($0.00), Extra Patty (+$1.00),
Extra Cheese (+$0.30). `applies_to` lets the app show only the relevant
customizations for a given item.

---

### 4.7 `combos`
The #1/#2/#3 meals: a headline burger + fries + a medium drink at a set price.

| Column | Type | Notes |
|---|---|---|
| `combo_id` | INTEGER | **PK** |
| `combo_name` | VARCHAR | |
| `burger_item_id` | INTEGER | **FK** → `menu_items` |
| `description` | VARCHAR | |
| `price` | DECIMAL(6,2) | bundled price |

A combo references its headline burger by FK, so the relationship between a
meal and its star item is explicit and queryable.

---

### 4.8 `orders`
One row per transaction / receipt.

| Column | Type | Notes |
|---|---|---|
| `order_id` | INTEGER | **PK** (surrogate) |
| `transaction_id` | VARCHAR | `UNIQUE` business key (receipt number) |
| `store_id` | INTEGER | **FK** → `stores` |
| `order_ts` | TIMESTAMP | when the order was placed |
| `order_type` | VARCHAR | Dine-In / Drive-Thru / Takeout |
| `payment_method` | VARCHAR | Card / Cash / Mobile |
| `subtotal` | DECIMAL(8,2) | sum of line totals |
| `tax_rate` | DECIMAL(5,4) | stored so historical orders stay correct |
| `tax_amount` | DECIMAL(8,2) | |
| `total` | DECIMAL(8,2) | `subtotal + tax_amount` |

Storing `tax_rate` on each order (rather than relying on a global constant) is
a small but realistic touch: if the tax rate changes next year, old receipts
still reflect the rate that actually applied.

---

### 4.9 `order_items`
The line items on a receipt.

| Column | Type | Notes |
|---|---|---|
| `order_item_id` | INTEGER | **PK** (surrogate) |
| `order_id` | INTEGER | **FK** → `orders` |
| `item_id` | INTEGER | **FK** → `menu_items` (nullable) |
| `combo_id` | INTEGER | **FK** → `combos` (nullable) |
| `size_id` | INTEGER | **FK** → `sizes` |
| `quantity` | INTEGER | |
| `unit_price` | DECIMAL(8,2) | base price *before* modifiers |
| `line_total` | DECIMAL(8,2) | `(unit_price + Σ modifier deltas) × quantity` |

A line is **either** a single item **or** a combo, enforced by a table-level
constraint:

```sql
CHECK (item_id IS NOT NULL OR combo_id IS NOT NULL)
```

This is a deliberate teaching nuance. Because combo lines carry `combo_id` and
no `item_id`, an analytics query that joins `order_items → menu_items` silently
excludes combos. The dashboard's "Revenue by category" chart flags this on
purpose — a great prompt for discussing the trade-offs of how you model a
"bundle."

`unit_price` and `line_total` are **stored** (denormalized) rather than
recomputed from the price tables on every read. In a transactional system this
is correct: the receipt must capture the price *as it was at the moment of
sale*, even if menu prices change later.

---

### 4.10 `order_item_modifiers`  *(bridge table)*
Which customizations were applied to which line.

| Column | Type | Notes |
|---|---|---|
| `order_item_id` | INTEGER | **PK part 1**, **FK** → `order_items` |
| `modifier_id` | INTEGER | **PK part 2**, **FK** → `modifiers` |
| `price_delta` | DECIMAL(6,2) | the delta at the time of sale |

The **composite PK** `(order_item_id, modifier_id)` resolves the many-to-many
between lines and modifiers, and prevents the same modifier being attached
twice to the same line.

---

## 5. How a single order touches the schema

When a cashier taps **Place order**, the app writes to three tables inside one
database transaction (all-or-nothing):

1. One row into `orders` (gets an `order_id` from a sequence and a generated
   `transaction_id`).
2. One row into `order_items` for each line on the ticket.
3. Zero or more rows into `order_item_modifiers` for each customization.

If any insert failed, the whole thing is rolled back — so you never end up with
an order that has no line items, or line items that point at a missing order.
This is **atomicity**, the "A" in ACID.

---

## 6. Identity generation

DuckDB **sequences** supply gap-free surrogate keys:

```sql
CREATE SEQUENCE seq_order_id      START 1;
CREATE SEQUENCE seq_order_item_id START 1;
-- usage:
INSERT INTO orders (order_id, ...) VALUES (nextval('seq_order_id'), ...);
```

The business key is generated in application code in the form
`INO-<store>-<YYYYMMDD>-<daily sequence>`, e.g. `INO-02-20260618-00031`.

---

## 7. Normalization summary (why it's in 3NF)

- **1NF** — every column holds a single atomic value; there are no repeating
  groups. (Customizations are rows in a bridge table, not a comma-separated
  list in a column.)
- **2NF** — every non-key column depends on the *whole* key. In `item_prices`,
  `price` depends on both `item_id` *and* `size_id`, not just one of them.
- **3NF** — non-key columns don't depend on other non-key columns. A burger's
  name lives only in `menu_items`; its price lives only in `item_prices`;
  nothing is duplicated, so there's no way for two copies to disagree.

The one intentional exception is the **stored** `unit_price` / `line_total` /
`tax_amount` on the transaction tables. That is a normal and correct choice for
a point-of-sale system: a receipt is a historical record and must not change
when the menu does.

---

## 8. Try these queries

```sql
-- Best-selling items (join across the M:1 item link)
SELECT m.item_name, sum(oi.quantity) AS sold
FROM order_items oi JOIN menu_items m ON m.item_id = oi.item_id
GROUP BY m.item_name ORDER BY sold DESC;

-- Orders per store (LEFT JOIN keeps brand-new, empty stores visible)
SELECT s.store_name, count(o.order_id) AS orders
FROM stores s LEFT JOIN orders o ON o.store_id = s.store_id
GROUP BY s.store_name ORDER BY orders DESC;

-- Most popular customizations (walk the bridge table)
SELECT md.modifier_name, count(*) AS times_added
FROM order_item_modifiers oim
JOIN modifiers md ON md.modifier_id = oim.modifier_id
GROUP BY md.modifier_name ORDER BY times_added DESC;

-- Combo vs. à-la-carte revenue (the CHECK constraint made this clean)
SELECT CASE WHEN combo_id IS NOT NULL THEN 'Combo' ELSE 'A la carte' END AS kind,
       round(sum(line_total), 2) AS revenue
FROM order_items GROUP BY kind;
```
