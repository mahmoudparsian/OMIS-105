"""
build_db.py  ·  In-N-Out POS demo database builder
OMIS-105 Introduction to DBMS

Creates innout.duckdb from scratch:
  1. applies schema.sql
  2. loads the menu reference (lookup) tables
  3. generates realistic historical orders (1500 / 2000 / 2500 per store)

Run:  python build_db.py
"""

import os
import random
from datetime import datetime, timedelta

import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "innout.duckdb")
SCHEMA_PATH = os.path.join(HERE, "schema.sql")

# Per-store order volume (store_id -> number of historical orders).
# Different sizes make cross-store comparisons interesting on the dashboard.
STORE_ORDER_COUNTS = {1: 1500, 2: 2000, 3: 2500}
DAYS_OF_HISTORY = 365          # a full year, so monthly trends have ~12 buckets
TAX_RATE = 0.0925                       # Santa Clara County sales tax
RANDOM_SEED = 105                       # reproducible for class demos
random.seed(RANDOM_SEED)

# ----------------------------------------------------------------------
# Reference data  (the menu, straight from menu.md)
# ----------------------------------------------------------------------
STORES = [
    (1, "In-N-Out #214 – Santa Clara", "Santa Clara", "CA"),
    (2, "In-N-Out #088 – San Jose",    "San Jose",    "CA"),
    (3, "In-N-Out #301 – Mountain View","Mountain View","CA"),
]

CATEGORIES = [
    (1, "Burgers",   1),
    (2, "Sides",     2),
    (3, "Beverages", 3),
    (4, "Shakes",    4),
]

SIZES = [
    (1, "Regular", 0),
    (2, "Small",   1),
    (3, "Medium",  2),
    (4, "Large",   3),
    (5, "X-Large", 4),
]

# (item_id, category_id, name, description, is_secret_menu)
MENU_ITEMS = [
    (1, 1, "Double-Double", "Two patties, two cheese, lettuce, tomato, spread", False),
    (2, 1, "Cheeseburger",  "Single patty, one cheese, lettuce, tomato, spread", False),
    (3, 1, "Hamburger",     "Single patty, lettuce, tomato, spread", False),
    (4, 1, "Flying Dutchman","Two patties, two cheese, no bun (secret menu)", True),
    (5, 1, "Grilled Cheese","Melted cheese, lettuce, tomato, spread (secret menu)", True),
    (6, 2, "French Fries",  "Freshly made, 100% real potatoes", False),
    (7, 3, "Coca-Cola",     "Fountain drink", False),
    (8, 3, "Diet Coke",     "Fountain drink", False),
    (9, 3, "7Up",           "Fountain drink", False),
    (10, 3, "Root Beer",    "Fountain drink", False),
    (11, 3, "Dr Pepper",    "Fountain drink", False),
    (12, 3, "Minute Maid",  "Fountain drink", False),
    (13, 3, "Pink Lemonade","Fountain drink", False),
    (14, 3, "Iced Tea",     "Fountain drink", False),
    (15, 3, "Coffee",       "Hot coffee", False),
    (16, 3, "Milk",         "Carton of milk", False),
    (17, 4, "Chocolate Shake","Hand-spun shake", False),
    (18, 4, "Strawberry Shake","Hand-spun shake", False),
    (19, 4, "Vanilla Shake","Hand-spun shake", False),
]

FOUNTAIN_IDS = list(range(7, 15))       # items priced by size
FOUNTAIN_PRICES = {2: 2.40, 3: 2.55, 4: 2.75, 5: 2.95}  # size_id -> price

# (item_id, size_id, price)
ITEM_PRICES = [
    (1, 1, 6.50), (2, 1, 4.55), (3, 1, 4.00), (4, 1, 3.50), (5, 1, 3.00),
    (6, 1, 2.50),
    (15, 1, 1.65), (16, 1, 1.25),
    (17, 1, 3.25), (18, 1, 3.25), (19, 1, 3.25),
]
for fid in FOUNTAIN_IDS:
    for sid, price in FOUNTAIN_PRICES.items():
        ITEM_PRICES.append((fid, sid, price))

# (modifier_id, name, description, price_delta, applies_to)
MODIFIERS = [
    (1, "Animal Style",     "Mustard-fried, extra spread, pickles, grilled onions", 0.00, "any"),
    (2, "Protein Style",    "Bun replaced with lettuce wrap", 0.00, "burger"),
    (3, "Add Onion",        "Fresh or grilled onions", 0.00, "burger"),
    (4, "No Onion",         "Hold the onions", 0.00, "burger"),
    (5, "Extra Spread",     "More Thousand Island", 0.00, "burger"),
    (6, "Extra Patty",      "One more beef patty", 1.00, "burger"),
    (7, "Extra Cheese",     "One more slice of cheese", 0.30, "burger"),
    (8, "Chopped Chilies",  "Add chopped chilies", 0.00, "any"),
    (9, "Well-Done Fries",  "Extra crispy", 0.00, "fries"),
    (10,"Light Fries",      "Cooked lighter", 0.00, "fries"),
]

# (combo_id, name, burger_item_id, description, price)
COMBOS = [
    (1, "Combo #1 – Double-Double", 1, "Double-Double + Fries + Medium Drink", 9.99),
    (2, "Combo #2 – Cheeseburger",  2, "Cheeseburger + Fries + Medium Drink",  8.49),
    (3, "Combo #3 – Hamburger",     3, "Hamburger + Fries + Medium Drink",     7.99),
]

BURGER_IDS = [1, 2, 3, 4, 5]
ORDER_TYPES = (["Drive-Thru"] * 5 + ["Dine-In"] * 3 + ["Takeout"] * 2)
PAYMENTS = (["Card"] * 6 + ["Mobile"] * 2 + ["Cash"] * 2)

# Hour-of-day weights: lunch (11-13) and dinner (17-20) peaks
HOUR_WEIGHTS = {
    10: 2, 11: 6, 12: 10, 13: 8, 14: 4, 15: 3, 16: 4,
    17: 8, 18: 10, 19: 9, 20: 6, 21: 4, 22: 2,
}


def load_reference(con):
    con.executemany("INSERT INTO stores VALUES (?,?,?,?)", STORES)
    con.executemany("INSERT INTO menu_categories VALUES (?,?,?)", CATEGORIES)
    con.executemany("INSERT INTO sizes VALUES (?,?,?)", SIZES)
    con.executemany("INSERT INTO menu_items VALUES (?,?,?,?,?)", MENU_ITEMS)
    con.executemany("INSERT INTO item_prices VALUES (?,?,?)", ITEM_PRICES)
    con.executemany("INSERT INTO modifiers VALUES (?,?,?,?,?)", MODIFIERS)
    con.executemany("INSERT INTO combos VALUES (?,?,?,?,?)", COMBOS)


def price_of(item_id, size_id):
    for iid, sid, price in ITEM_PRICES:
        if iid == item_id and sid == size_id:
            return price
    raise KeyError((item_id, size_id))


def random_timestamp():
    day_offset = random.randint(0, DAYS_OF_HISTORY - 1)
    base = datetime.now().replace(microsecond=0) - timedelta(days=day_offset)
    hours = list(HOUR_WEIGHTS.keys())
    hour = random.choices(hours, weights=[HOUR_WEIGHTS[h] for h in hours])[0]
    return base.replace(hour=hour, minute=random.randint(0, 59),
                        second=random.randint(0, 59))


def build_line(item_id):
    """Return (item_id, combo_id, size_id, qty, unit_price, modifier_ids)."""
    # ~30% of burgers are ordered as a combo
    if item_id in (1, 2, 3) and random.random() < 0.30:
        combo_id = {1: 1, 2: 2, 3: 3}[item_id]
        unit = next(c[4] for c in COMBOS if c[0] == combo_id)
        return (None, combo_id, 1, 1, unit, [])

    if item_id in FOUNTAIN_IDS:
        size_id = random.choices([2, 3, 4, 5], weights=[2, 4, 3, 1])[0]
    else:
        size_id = 1
    unit = price_of(item_id, size_id)

    mods = []
    if item_id in BURGER_IDS and random.random() < 0.45:
        pool = [m[0] for m in MODIFIERS if m[4] in ("burger", "any")]
        mods = random.sample(pool, k=random.randint(1, 2))
    elif item_id == 6 and random.random() < 0.30:   # fries
        pool = [m[0] for m in MODIFIERS if m[4] in ("fries", "any")]
        mods = random.sample(pool, k=1)

    qty = random.choices([1, 2, 3], weights=[8, 2, 1])[0]
    return (item_id, None, size_id, qty, unit, mods)


def generate_orders(con):
    mod_delta = {m[0]: m[3] for m in MODIFIERS}
    # Popularity weights so the data has a believable "best sellers" shape
    item_pool = (
        [1] * 30 + [2] * 18 + [3] * 12 + [4] * 3 + [5] * 4 +    # burgers
        [6] * 28 +                                              # fries
        [7] * 10 + [8] * 7 + [9] * 4 + [10] * 4 + [11] * 6 +    # fountain
        [12] * 3 + [13] * 4 + [14] * 5 + [15] * 3 + [16] * 2 +
        [17] * 8 + [18] * 6 + [19] * 6                          # shakes
    )

    order_rows, item_rows, mod_rows = [], [], []
    seq_by_key = {}

    # Build a shuffled list of store_ids so each store gets its target volume
    # but orders are interleaved in time rather than grouped by store.
    store_sequence = []
    for sid, cnt in STORE_ORDER_COUNTS.items():
        store_sequence.extend([sid] * cnt)
    random.shuffle(store_sequence)

    for store_id in store_sequence:
        oid = con.execute("SELECT nextval('seq_order_id')").fetchone()[0]
        ts = random_timestamp()
        key = (store_id, ts.strftime("%Y%m%d"))
        seq_by_key[key] = seq_by_key.get(key, 0) + 1
        txn = f"INO-{store_id:02d}-{ts:%Y%m%d}-{seq_by_key[key]:05d}"

        n_lines = random.choices([1, 2, 3, 4], weights=[3, 5, 3, 1])[0]
        subtotal = 0.0
        for _ in range(n_lines):
            item_id = random.choice(item_pool)
            iid, cid, sid, qty, unit, mods = build_line(item_id)
            line_item_id = con.execute(
                "SELECT nextval('seq_order_item_id')").fetchone()[0]
            mods_total = sum(mod_delta[m] for m in mods)
            line_total = round((unit + mods_total) * qty, 2)
            subtotal += line_total
            item_rows.append((line_item_id, oid, iid, cid, sid, qty,
                              round(unit, 2), line_total))
            for m in mods:
                mod_rows.append((line_item_id, m, mod_delta[m]))

        subtotal = round(subtotal, 2)
        tax = round(subtotal * TAX_RATE, 2)
        total = round(subtotal + tax, 2)
        order_rows.append((oid, txn, store_id, ts,
                           random.choice(ORDER_TYPES), random.choice(PAYMENTS),
                           subtotal, TAX_RATE, tax, total))

    # Explicit column list: the orders table also has is_voided/voided_at,
    # which we intentionally omit here so they take their schema DEFAULTs
    # (FALSE / NULL). Naming columns keeps this INSERT working even as the
    # table grows more columns later.
    con.executemany(
        """INSERT INTO orders
             (order_id, transaction_id, store_id, order_ts, order_type,
              payment_method, subtotal, tax_rate, tax_amount, total)
           VALUES (?,?,?,?,?,?,?,?,?,?)""", order_rows)
    con.executemany(
        "INSERT INTO order_items VALUES (?,?,?,?,?,?,?,?)", item_rows)
    con.executemany(
        "INSERT INTO order_item_modifiers VALUES (?,?,?)", mod_rows)

    # Soft-delete a small, realistic fraction (~1.5%) of historical orders so
    # the "exclude voided" behavior is actually visible on the dashboard.
    # Voiding is an UPDATE (not a DELETE): the rows stay in the table, we just
    # flip the flag and stamp WHEN it happened (a few minutes after the sale).
    void_updates = [
        (row[3] + timedelta(minutes=random.randint(3, 90)), row[0])  # (ts, oid)
        for row in order_rows if random.random() < 0.015
    ]
    con.executemany(
        "UPDATE orders SET is_voided = TRUE, voided_at = ? WHERE order_id = ?",
        void_updates)

    return len(order_rows), len(item_rows), len(mod_rows), len(void_updates)


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = duckdb.connect(DB_PATH)
    with open(SCHEMA_PATH) as f:
        con.execute(f.read())
    load_reference(con)
    n_o, n_i, n_m, n_v = generate_orders(con)
    con.close()
    print(f"Built {DB_PATH}")
    print(f"  orders               : {n_o}  ({n_v} voided)")
    print(f"  order_items          : {n_i}")
    print(f"  order_item_modifiers : {n_m}")


if __name__ == "__main__":
    main()
