# DuckDB Column Definitions & Constraints Guide

This tutorial explores the rich set of column definitions, constraints, default values, and complex data types supported by **DuckDB**. 

To demonstrate these features, we will build a realistic **E-Commerce & Logistics Engine** schema spanning customer management, product catalogs, inventory tracking, order processing, and spatial delivery tracking.

---

## 1. Schema Overview & Features Covered

Our schema includes the following column definition features in DuckDB:

| Category | Features / Constraints Demonstrated |
| :--- | :--- |
| **Identifiers & Keys** | `PRIMARY KEY`, Compound Primary Keys, `FOREIGN KEY` (Single & Multi-column), `UUID` default generation |
| **Nullability & Uniqueness**| `NOT NULL`, `UNIQUE`, Compound `UNIQUE` constraints |
| **Check Constraints** | Range checks (`CHECK (price > 0)`), String pattern matching (`LIKE`), Array length validation |
| **Defaults & Sequences** | `DEFAULT`, `AUTOINCREMENT` / `SEQUENCE`, `CURRENT_TIMESTAMP` |
| **Complex & Nested Types** | `STRUCT`, `LIST`, `MAP`, `ENUM` |
| **Specialized Types** | `DECIMAL`, `TIMESTAMP WITH TIME ZONE`, `GEOMETRY` (Spatial extension) |

---

## 2. Table Definitions (DDL)

```sql
-- Enable Spatial extension for geometry types 
-- (optional but realistic)
INSTALL spatial;
LOAD spatial;

-- 1. Custom Custom Types (ENUMs)
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
-- Demonstrates: AUTOINCREMENT primary key, GEOMETRY data type, STRUCT for addresses
CREATE TABLE warehouses (
    warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
-- Demonstrates: Positive value CHECK constraints, LIST types, STRUCT dimensions
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
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
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
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
-- Demonstrates: Foreign keys, Multi-column validation, CHECK constraints
CREATE TABLE order_items (
    item_id BIGINT PRIMARY KEY AUTOINCREMENT,
    order_id UUID NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0.00),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    discount_rate DECIMAL(3, 2) DEFAULT 0.00 CHECK (discount_rate BETWEEN 0.00 AND 1.00)
);
```

---

## 3. Inserting Sample Data

Here we insert sample data that satisfies all check constraints, foreign keys, and structural definitions.

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

### Violation 1: Check Constraint (`CHECK (cost_price <= unit_price)`)
```sql
-- FAILS: Cost price (350.00) is greater than unit price (299.99)
INSERT INTO products (sku, name, unit_price, cost_price, tags)
VALUES ('PROD-FAIL-1', 'Invalid Product', 299.99, 350.00, ['electronics']);

-- Error: Constraint Error: CHECK constraint failed: (cost_price <= unit_price)
```

### Violation 2: Regex / String Check Constraint (`CHECK (email LIKE '%@%.%')`)
```sql
-- FAILS: Invalid email format
INSERT INTO customers (first_name, last_name, email) 
VALUES ('John', 'Doe', 'invalid_email_at_domain.com');

-- Error: Constraint Error: CHECK constraint failed: (email LIKE '%@%.%')
```

### Violation 3: Foreign Key Constraint (`REFERENCES products(product_id)`)
```sql
-- FAILS: Referenced product_id 9999 does not exist
INSERT INTO warehouse_inventory (warehouse_id, product_id, quantity_on_hand)
VALUES (1, 9999, 50);

-- Error: Constraint Error: Violates foreign key constraint
```