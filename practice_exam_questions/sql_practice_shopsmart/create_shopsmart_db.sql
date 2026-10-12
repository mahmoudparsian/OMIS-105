-- ============================================================
-- ShopSmart database for SQL Practice 02 (Weeks 6-10)
--
-- Build it from this folder with:
--     duckdb shopsmart.duckdb < create_shopsmart_db.sql
--
-- Re-running this script rebuilds every table from the CSV
-- files in data/, so it also resets the database after practice.
-- ============================================================

-- Drop children before parents (foreign keys)
DROP VIEW  IF EXISTS order_summary;
DROP VIEW  IF EXISTS product_catalog;
DROP TABLE IF EXISTS shipping;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS product_suppliers;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS orders_denormalized;

-- ---------- parent tables ----------

CREATE TABLE categories (
    category_id   INTEGER PRIMARY KEY,
    category_name VARCHAR NOT NULL UNIQUE,
    description   VARCHAR
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name  VARCHAR NOT NULL,
    last_name   VARCHAR NOT NULL,
    email       VARCHAR NOT NULL UNIQUE,
    city        VARCHAR,
    state       VARCHAR,
    join_date   DATE
);

CREATE TABLE suppliers (
    supplier_id   INTEGER PRIMARY KEY,
    supplier_name VARCHAR NOT NULL,
    email         VARCHAR,
    city          VARCHAR,
    state         VARCHAR,
    partner_since DATE
);

-- ---------- child tables ----------

CREATE TABLE products (
    product_id     INTEGER PRIMARY KEY,
    product_name   VARCHAR NOT NULL,
    category_id    INTEGER NOT NULL REFERENCES categories(category_id),
    price          DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0)
);

CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date   DATE NOT NULL,
    status       VARCHAR NOT NULL
                 CHECK (status IN ('processing', 'shipped', 'completed', 'cancelled')),
    total_amount DECIMAL(10,2)
);

CREATE TABLE order_items (
    item_id    INTEGER PRIMARY KEY,
    order_id   INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0)
);

-- junction table for the many-to-many products <-> suppliers relationship
CREATE TABLE product_suppliers (
    product_id  INTEGER REFERENCES products(product_id),
    supplier_id INTEGER REFERENCES suppliers(supplier_id),
    cost_price  DECIMAL(10,2),
    PRIMARY KEY (product_id, supplier_id)
);

CREATE TABLE reviews (
    review_id   INTEGER PRIMARY KEY,
    product_id  INTEGER NOT NULL REFERENCES products(product_id),
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text VARCHAR,
    review_date DATE
);

-- one shipment per order (1-1 with orders)
CREATE TABLE shipping (
    shipping_id   INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL UNIQUE REFERENCES orders(order_id),
    carrier       VARCHAR,
    ship_date     DATE,
    delivery_date DATE,            -- NULL = still in transit
    shipping_cost DECIMAL(10,2),
    CHECK (delivery_date >= ship_date)
);

-- the "before normalization" table used in Week 6 (no keys on purpose)
CREATE TABLE orders_denormalized (
    order_id       INTEGER,
    order_date     DATE,
    status         VARCHAR,
    customer_id    INTEGER,
    customer_name  VARCHAR,
    customer_email VARCHAR,
    customer_city  VARCHAR,
    product_id     INTEGER,
    product_name   VARCHAR,
    category_name  VARCHAR,
    unit_price     DECIMAL(10,2),
    quantity       INTEGER,
    line_price     DECIMAL(10,2)
);

-- ---------- load the data (parents first) ----------

COPY categories          FROM 'data/categories.csv'          (HEADER true);
COPY customers           FROM 'data/customers.csv'           (HEADER true);
COPY suppliers           FROM 'data/suppliers.csv'           (HEADER true);
COPY products            FROM 'data/products.csv'            (HEADER true);
COPY orders              FROM 'data/orders.csv'              (HEADER true);
COPY order_items         FROM 'data/order_items.csv'         (HEADER true);
COPY product_suppliers   FROM 'data/product_suppliers.csv'   (HEADER true);
COPY reviews             FROM 'data/reviews.csv'             (HEADER true);
COPY shipping            FROM 'data/shipping.csv'            (HEADER true);
COPY orders_denormalized FROM 'data/orders_denormalized.csv' (HEADER true);

-- ---------- verify ----------

SELECT 'categories' AS table_name, COUNT(*) AS num_rows FROM categories
UNION ALL SELECT 'customers',           COUNT(*) FROM customers
UNION ALL SELECT 'suppliers',           COUNT(*) FROM suppliers
UNION ALL SELECT 'products',            COUNT(*) FROM products
UNION ALL SELECT 'orders',              COUNT(*) FROM orders
UNION ALL SELECT 'order_items',         COUNT(*) FROM order_items
UNION ALL SELECT 'product_suppliers',   COUNT(*) FROM product_suppliers
UNION ALL SELECT 'reviews',             COUNT(*) FROM reviews
UNION ALL SELECT 'shipping',            COUNT(*) FROM shipping
UNION ALL SELECT 'orders_denormalized', COUNT(*) FROM orders_denormalized;
