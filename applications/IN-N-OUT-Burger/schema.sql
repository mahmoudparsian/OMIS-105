-- =====================================================================
-- In-N-Out POS  ·  Fully Normalized Schema  ·  DuckDB
-- OMIS-105 Introduction to DBMS  ·  Santa Clara University
-- ---------------------------------------------------------------------
-- Reference (lookup) tables describe the menu.
-- Transaction tables (orders / order_items / order_item_modifiers)
-- record what customers actually bought.
--
-- Relationships (parent -> child):
--   menu_categories 1--* menu_items
--   sizes           1--* item_prices
--   menu_items      1--* item_prices
--   menu_items      1--* combos        (the combo's headline burger)
--   stores          1--* orders
--   orders          1--* order_items
--   menu_items      1--* order_items   (an item line)
--   combos          1--* order_items   (a combo line)
--   sizes           1--* order_items
--   order_items     1--* order_item_modifiers
--   modifiers       1--* order_item_modifiers
-- =====================================================================

-- Sequences give us clean, auto-incrementing surrogate primary keys.
CREATE SEQUENCE IF NOT EXISTS seq_order_id      START 1;
CREATE SEQUENCE IF NOT EXISTS seq_order_item_id START 1;

-- ---------------------------------------------------------------------
-- 1. STORES  (which restaurant rang up the order)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stores (
    store_id    INTEGER      PRIMARY KEY,
    store_name  VARCHAR      NOT NULL,
    city        VARCHAR      NOT NULL,
    state       VARCHAR      NOT NULL
);

-- ---------------------------------------------------------------------
-- 2. MENU_CATEGORIES  (Burgers, Sides, Beverages, Shakes)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS menu_categories (
    category_id   INTEGER   PRIMARY KEY,
    category_name VARCHAR   NOT NULL UNIQUE,
    sort_order    INTEGER   NOT NULL
);

-- ---------------------------------------------------------------------
-- 3. SIZES  (Regular for most items; small..X-large for fountain drinks)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sizes (
    size_id    INTEGER   PRIMARY KEY,
    size_name  VARCHAR   NOT NULL UNIQUE,
    sort_order INTEGER   NOT NULL
);

-- ---------------------------------------------------------------------
-- 4. MENU_ITEMS  (every individually sellable thing)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS menu_items (
    item_id        INTEGER   PRIMARY KEY,
    category_id    INTEGER   NOT NULL REFERENCES menu_categories(category_id),
    item_name      VARCHAR   NOT NULL,
    description    VARCHAR,
    is_secret_menu BOOLEAN   NOT NULL DEFAULT FALSE
);

-- ---------------------------------------------------------------------
-- 5. ITEM_PRICES  (an item's price AT a given size)
--    Composite PK (item_id, size_id): the classic many-to-many bridge.
--    Burgers/shakes/etc. have one row at the 'Regular' size;
--    fountain drinks have four rows (small/medium/large/X-large).
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS item_prices (
    item_id  INTEGER   NOT NULL REFERENCES menu_items(item_id),
    size_id  INTEGER   NOT NULL REFERENCES sizes(size_id),
    price    DECIMAL(6,2) NOT NULL,
    PRIMARY KEY (item_id, size_id)
);

-- ---------------------------------------------------------------------
-- 6. MODIFIERS  (the "Not So Secret" customizations & extras)
--    price_delta is added to the line; many are free (0.00).
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS modifiers (
    modifier_id   INTEGER   PRIMARY KEY,
    modifier_name VARCHAR   NOT NULL UNIQUE,
    description   VARCHAR,
    price_delta   DECIMAL(6,2) NOT NULL DEFAULT 0.00,
    applies_to    VARCHAR   NOT NULL          -- 'burger', 'fries', or 'any'
);

-- ---------------------------------------------------------------------
-- 7. COMBOS  (#1/#2/#3 = burger + fries + medium drink at a set price)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS combos (
    combo_id        INTEGER   PRIMARY KEY,
    combo_name      VARCHAR   NOT NULL,
    burger_item_id  INTEGER   NOT NULL REFERENCES menu_items(item_id),
    description     VARCHAR,
    price           DECIMAL(6,2) NOT NULL
);

-- ---------------------------------------------------------------------
-- 8. ORDERS  (one row per transaction / receipt)
--    transaction_id is the human-readable business key the cashier sees;
--    order_id is the surrogate primary key used by foreign keys.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
    order_id       INTEGER      PRIMARY KEY,
    transaction_id VARCHAR      NOT NULL UNIQUE,
    store_id       INTEGER      NOT NULL REFERENCES stores(store_id),
    order_ts       TIMESTAMP    NOT NULL,
    order_type     VARCHAR      NOT NULL,      -- 'Dine-In','Drive-Thru','Takeout'
    payment_method VARCHAR      NOT NULL,      -- 'Card','Cash','Mobile'
    subtotal       DECIMAL(8,2) NOT NULL,
    tax_rate       DECIMAL(5,4) NOT NULL,
    tax_amount     DECIMAL(8,2) NOT NULL,
    total          DECIMAL(8,2) NOT NULL
);

-- ---------------------------------------------------------------------
-- 9. ORDER_ITEMS  (line items on a receipt)
--    Each line is EITHER a single item OR a combo (CHECK enforces it).
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER   PRIMARY KEY,
    order_id      INTEGER   NOT NULL REFERENCES orders(order_id),
    item_id       INTEGER   REFERENCES menu_items(item_id),
    combo_id      INTEGER   REFERENCES combos(combo_id),
    size_id       INTEGER   NOT NULL REFERENCES sizes(size_id),
    quantity      INTEGER   NOT NULL DEFAULT 1,
    unit_price    DECIMAL(8,2) NOT NULL,       -- base price before modifiers
    line_total    DECIMAL(8,2) NOT NULL,       -- (unit_price + modifiers) * qty
    CHECK (item_id IS NOT NULL OR combo_id IS NOT NULL)
);

-- ---------------------------------------------------------------------
-- 10. ORDER_ITEM_MODIFIERS  (bridge: which mods are on which line)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_item_modifiers (
    order_item_id INTEGER   NOT NULL REFERENCES order_items(order_item_id),
    modifier_id   INTEGER   NOT NULL REFERENCES modifiers(modifier_id),
    price_delta   DECIMAL(6,2) NOT NULL,
    PRIMARY KEY (order_item_id, modifier_id)
);
