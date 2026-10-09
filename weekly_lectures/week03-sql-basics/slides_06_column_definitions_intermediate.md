# DuckDB Column Definitions & Constraints Guide

This tutorial explores the rich set of column 
definitions, constraints, default values, and 
complex data types supported by **DuckDB**. 

To demonstrate these features, we will build a 
realistic **E-Commerce & Logistics Engine** schema 
spanning customer management, product catalogs,
inventory tracking, order processing, and spatial 
delivery tracking.

---

## 1. Schema Overview & Features Covered

Our schema includes the following column definition features in DuckDB:

| Category | Features / Constraints Demonstrated |
| :--- | :--- |
| **Identifiers & Keys** | `PRIMARY KEY`, Compound Primary Key, `FOREIGN KEY`, `UUID` default generation |
| **Nullability & Uniqueness**| `NOT NULL`, `UNIQUE`, Compound `UNIQUE` constraint |
| **Check Constraints** | Range checks (`CHECK (unit_price > 0)`), String pattern matching (`LIKE`), List length validation |
| **Defaults & Sequences** | `DEFAULT`, auto-increment with `SEQUENCE` + `nextval()`, `CURRENT_TIMESTAMP` |
| **Complex & Nested Types** | `STRUCT`, `LIST`, `MAP`, `ENUM` |
| **Specialized Types** | `DECIMAL`, `TIMESTAMP WITH TIME ZONE`, `GEOMETRY` (Spatial extension) |

> **Auto-increment reminder:** DuckDB has no
> `AUTOINCREMENT` keyword. An auto-increment column
> is built from a `SEQUENCE` plus
> `DEFAULT nextval('seq_name')` (see `slides_09`).

---

## 2. Table Definitions (DDL)

```sql
-- Enable the Spatial extension for the GEOMETRY type
-- (INSTALL downloads it once; needs an internet connection)
INSTALL spatial;
LOAD spatial;

-- 1. Custom Types (ENUMs)
CREATE TYPE order_status 
AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');

CREATE TYPE payment_method 
AS ENUM ('credit_card', 'paypal', 'crypto', 'bank_transfer');

-- 2. Customers Table
-- Demonstrates: UUID generation, Check constraints 
-- (email pattern), Default timestamps
CREATE TABLE customers (
    customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE CHECK (email LIKE '%@%.%'),
    loyalty_tier VARCHAR(20) DEFAULT 'Bronze' CHECK (loyalty_tier IN ('Bronze', 'Silver', 'Gold', 'Platinum')),
    metadata MAP(VARCHAR, VARCHAR), -- Key-value pairs for flexible user preferences
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Warehouses Table
-- Demonstrates: auto-increment primary key (SEQUENCE),
-- GEOMETRY data type, STRUCT for addresses
CREATE SEQUENCE warehouse_id_seq START 1;

CREATE TABLE warehouses (
    warehouse_id INTEGER PRIMARY KEY DEFAULT nextval('warehouse_id_seq'),
    warehouse_code VARCHAR(10) NOT NULL UNIQUE,
    location_name VARCHAR(100) NOT NULL,
    address STRUCT(
        street VARCHAR(100),
        city VARCHAR(50),
        postal_code VARCHAR(20),
        country VARCHAR(50)
    ) NOT NULL,
    geo_location GEOMETRY, -- Point location (longitude, latitude)
    is_active BOOLEAN DEFAULT TRUE
);

-- 4. Products Table
-- Demonstrates: auto-increment primary key (SEQUENCE),
-- positive-value and cross-column CHECK constraints,
-- LIST type, STRUCT for dimensions
CREATE SEQUENCE product_id_seq START 1;

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY DEFAULT nextval('product_id_seq'),
    sku VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    description TEXT,  -- TEXT is another name for VARCHAR
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0.00),
    cost_price DECIMAL(10, 2) NOT NULL CHECK (cost_price >= 0.00 AND cost_price <= unit_price),
    tags VARCHAR[] CHECK (len(tags) > 0), -- ARRAY/LIST of tags with non-empty check
    dimensions STRUCT(length_cm DOUBLE, width_cm DOUBLE, height_cm DOUBLE),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Inventory Table
-- Demonstrates: Compound Primary Key, Foreign Keys, non-negative quantity CHECK constraint
CREATE TABLE warehouse_inventory (
    warehouse_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity_on_hand INTEGER NOT NULL DEFAULT 0 CHECK (quantity_on_hand >= 0),
    reorder_threshold INTEGER DEFAULT 10 CHECK (reorder_threshold >= 0),
    last_restocked_at TIMESTAMP,
    -- Compound Primary Key
    PRIMARY KEY (warehouse_id, product_id),
    -- Foreign Keys
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 6. Orders Table
-- Demonstrates: ENUM types, Foreign key to UUID, CHECK on total price
CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(customer_id),
    status order_status DEFAULT 'pending',
    payment_type payment_method NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL CHECK (total_amount >= 0.00),
    shipping_address STRUCT(street VARCHAR, city VARCHAR, zip VARCHAR, country VARCHAR),
    order_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Order Items Table
-- Demonstrates: auto-increment BIGINT key, Foreign Keys,
-- Compound UNIQUE constraint, BETWEEN check
CREATE SEQUENCE item_id_seq START 1;

CREATE TABLE order_items (
    item_id BIGINT PRIMARY KEY DEFAULT nextval('item_id_seq'),
    order_id UUID NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0.00),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    discount_rate DECIMAL(3, 2) DEFAULT 0.00 CHECK (discount_rate BETWEEN 0.00 AND 1.00),
    -- Compound UNIQUE: a product appears at most once per order
    UNIQUE (order_id, product_id)
);
```

---

## 2.1 Notes on This Schema

* **`VARCHAR(n)` length is not enforced.** DuckDB
  accepts `VARCHAR(50)`, but it stores any length of
  text. The `(50)` is documentation only. Use
  `CHECK (length(col) <= 50)` if you need a real limit.

* **No `ON DELETE CASCADE`.** DuckDB foreign keys
  do not support `CASCADE`, `SET NULL`, or
  `SET DEFAULT`. You get this error:
  `FOREIGN KEY constraints cannot use CASCADE, SET NULL or SET DEFAULT`.
  To delete a parent row, delete its child rows first.

* **Two kinds of generated IDs.** `customers` and
  `orders` use a random `UUID` from `gen_random_uuid()`.
  `warehouses`, `products`, and `order_items` use an
  auto-increment number from a `SEQUENCE`.

* **Create parents before children.** A table must
  exist before another table can reference it.

---

## 3. Inserting Sample Data

Here we insert sample data that satisfies
all check constraints, foreign keys, and
structural definitions.

We give the `UUID` values by hand so the rows can
point to each other. We do **not** give
`warehouse_id` or `product_id`: the sequences number
them 1, 2, ... The inventory rows below rely on
those numbers.

```sql
-- Insert Customers
INSERT INTO customers (customer_id, first_name, last_name, email, loyalty_tier, metadata) 
VALUES 
(
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 
    'Alice', 
    'Smith', 
    'alice@example.com', 
    'Gold', 
    MAP {'theme': 'dark', 'notifications': 'email'}
),
(
    'b1fefc99-9c0b-4ef8-bb6d-6bb9bd380a22', 
    'Bob', 
    'Jones', 
    'bob.jones@service.org', 
    'Bronze', 
    MAP {'theme': 'light'}
);

-- Insert Warehouses
INSERT INTO warehouses (warehouse_code, location_name, address, geo_location)
VALUES 
(
    'WH-US-EAST', 
    'New Jersey Logistics Hub', 
    {'street': '100 Logistics Way', 'city': 'Newark', 'postal_code': '07102', 'country': 'USA'},
    ST_Point(-74.1724, 40.7357)
),
(
    'WH-US-WEST', 
    'California Distribution Center', 
    {'street': '500 Commerce Blvd', 'city': 'Ontario', 'postal_code': '91764', 'country': 'USA'},
    ST_Point(-117.5931, 34.0633)
);

-- Insert Products
INSERT INTO products (sku, name, description, unit_price, cost_price, tags, dimensions)
VALUES 
(
    'PROD-AUDIO-001', 
    'Noise Cancelling Headphones', 
    'Wireless over-ear headphones with active noise cancellation.', 
    299.99, 
    120.00, 
    ['electronics', 'audio', 'wireless'], 
    {'length_cm': 20.0, 'width_cm': 18.0, 'height_cm': 8.0}
),
(
    'PROD-DESK-002', 
    'Ergonomic Mechanical Keyboard', 
    'Split mechanical keyboard with tactile switches.', 
    149.50, 
    65.00, 
    ['electronics', 'office', 'ergonomic'], 
    {'length_cm': 35.0, 'width_cm': 15.0, 'height_cm': 4.0}
);

-- Insert Inventory
INSERT INTO warehouse_inventory (warehouse_id, product_id, quantity_on_hand, reorder_threshold)
VALUES 
(1, 1, 150, 20),
(1, 2, 80, 15),
(2, 1, 200, 25);

-- Insert Orders
INSERT INTO orders (order_id, customer_id, status, payment_type, total_amount, shipping_address)
VALUES 
(
    'c2fffd99-9c0b-4ef8-bb6d-6bb9bd380a33', 
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 
    'shipped', 
    'credit_card', 
    449.49, 
    {'street': '742 Evergreen Terrace', 'city': 'Springfield', 'zip': '97477', 'country': 'USA'}
);

-- Insert Order Items
INSERT INTO order_items (order_id, product_id, unit_price, quantity, discount_rate)
VALUES 
('c2fffd99-9c0b-4ef8-bb6d-6bb9bd380a33', 1, 299.99, 1, 0.00),
('c2fffd99-9c0b-4ef8-bb6d-6bb9bd380a33', 2, 149.50, 1, 0.00);
```

---

## 4. Sample Rows & Query Results

### `customers` Table

```sql
SELECT customer_id, first_name, email, loyalty_tier, metadata FROM customers;
```

| customer_id | first_name | email | loyalty_tier | metadata |
| :--- | :--- | :--- | :--- | :--- |
| `a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11` | Alice | `alice@example.com` | Gold | `{'theme': 'dark', 'notifications': 'email'}` |
| `b1fefc99-9c0b-4ef8-bb6d-6bb9bd380a22` | Bob | `bob.jones@service.org` | Bronze | `{'theme': 'light'}` |

---

### `products` Table (Complex STRUCTs & ARRAYs)

```sql
SELECT product_id, sku, name, unit_price, tags, dimensions FROM products;
```

| product_id | sku | name | unit_price | tags | dimensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `1` | `PROD-AUDIO-001` | Noise Cancelling Headphones | `299.99` | `['electronics', 'audio', 'wireless']` | `{'length_cm': 20.0, 'width_cm': 18.0, 'height_cm': 8.0}` |
| `2` | `PROD-DESK-002` | Ergonomic Mechanical Keyboard | `149.50` | `['electronics', 'office', 'ergonomic']` | `{'length_cm': 35.0, 'width_cm': 15.0, 'height_cm': 4.0}` |

---

### `warehouse_inventory` Table (Compound PK)

```sql
SELECT * FROM warehouse_inventory;
```

| warehouse_id | product_id | quantity_on_hand | reorder_threshold | last_restocked_at |
| :--- | :--- | :--- | :--- | :--- |
| `1` | `1` | `150` | `20` | *NULL* |
| `1` | `2` | `80` | `15` | *NULL* |
| `2` | `1` | `200` | `25` | *NULL* |

---

## 5. Constraint Violations & Edge Cases in DuckDB

To understand how DuckDB enforces these definitions, here are examples of statements that will trigger constraint violations:

### Violation 1: Cross-Column Check (`CHECK (cost_price <= unit_price)`)
```sql
-- FAILS: Cost price (350.00) is greater than unit price (299.99)
INSERT INTO products (sku, name, unit_price, cost_price, tags)
VALUES ('PROD-FAIL-1', 'Invalid Product', 299.99, 350.00, ['electronics']);

-- Constraint Error: CHECK constraint failed on table products with expression
-- CHECK(((cost_price >= 0.00) AND (cost_price <= unit_price)))
```

### Violation 2: Pattern Check (`CHECK (email LIKE '%@%.%')`)
```sql
-- FAILS: Invalid email format (no '@')
INSERT INTO customers (first_name, last_name, email) 
VALUES ('John', 'Doe', 'invalid_email_at_domain.com');

-- Constraint Error: CHECK constraint failed on table customers with expression
-- CHECK((email ~~ '%@%.%'))
-- (~~ is DuckDB's internal name for LIKE)
```

### Violation 3: Foreign Key Constraint (`REFERENCES products(product_id)`)
```sql
-- FAILS: Referenced product_id 9999 does not exist
INSERT INTO warehouse_inventory (warehouse_id, product_id, quantity_on_hand)
VALUES (1, 9999, 50);

-- Constraint Error: Violates foreign key constraint because key
-- "product_id: 9999" does not exist in the referenced table
```

### Violation 4: Compound UNIQUE (`UNIQUE (order_id, product_id)`)
```sql
-- FAILS: product 1 is already in this order
INSERT INTO order_items (order_id, product_id, unit_price, quantity)
VALUES ('c2fffd99-9c0b-4ef8-bb6d-6bb9bd380a33', 1, 299.99, 2);

-- Constraint Error: Duplicate key "order_id: c2fffd99-9c0b-4ef8-bb6d-6bb9bd380a33,
-- product_id: 1" violates unique constraint.
```

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
