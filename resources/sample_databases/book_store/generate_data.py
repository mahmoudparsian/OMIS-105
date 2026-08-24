import csv
import random
import copy
from datetime import date, timedelta

random.seed(42)

DATA_DIR = "/sessions/wonderful-blissful-gauss/mnt/duckdb_book_store/data"

# ── Read existing data ──────────────────────────────────────────────
def read_csv(path):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [r for r in reader]
    return header, rows

books_hdr, books_rows = read_csv(f"{DATA_DIR}/books.csv")
cust_hdr, cust_rows   = read_csv(f"{DATA_DIR}/customers.csv")
ord_hdr, ord_rows     = read_csv(f"{DATA_DIR}/orders.csv")

print(f"Original books: {len(books_rows)}, customers: {len(cust_rows)}, orders: {len(ord_rows)}")

# ── 1. Generate 7000 new orders ─────────────────────────────────────
# Year distribution: 2023→1000, 2024→2000, 2025→4000
year_alloc = [(2023, 1000), (2024, 2000), (2025, 4000)]

# Monthly weights: heavier Nov/Dec
month_weights = {
    1: 5, 2: 5, 3: 6, 4: 6, 5: 7, 6: 7,
    7: 8, 8: 7, 9: 7, 10: 8, 11: 16, 12: 18
}
months = list(month_weights.keys())
weights = list(month_weights.values())

# Customer purchasing power: power-law (some buy MUCH more)
customer_ids = list(range(1, 501))
# Create a power-law-ish distribution: 20 "whale" customers, 60 "heavy", rest normal
whales = random.sample(customer_ids, 20)    # buy ~10x more
heavy  = random.sample([c for c in customer_ids if c not in whales], 60)  # buy ~4x more
normal = [c for c in customer_ids if c not in whales and c not in heavy]

# Build weighted customer pool
customer_pool = []
for c in whales:
    customer_pool.extend([c] * 40)
for c in heavy:
    customer_pool.extend([c] * 12)
for c in normal:
    customer_pool.extend([c] * 2)

book_ids = list(range(1, 501))

# Build a price lookup for books
book_prices = {}
for r in books_rows:
    book_prices[int(r[0])] = float(r[5])

next_order_id = len(ord_rows) + 1
new_orders = []

for year, count in year_alloc:
    for _ in range(count):
        month = random.choices(months, weights=weights, k=1)[0]
        # Random day within that month
        start = date(year, month, 1)
        if month == 12:
            end = date(year, 12, 31)
        else:
            end = date(year, month + 1, 1) - timedelta(days=1)
        day = random.randint(start.day, end.day)
        order_date = date(year, month, day).isoformat()

        cid = random.choice(customer_pool)
        bid = random.choice(book_ids)
        qty = random.choices(range(1, 11), weights=[30, 25, 15, 10, 8, 5, 3, 2, 1, 1], k=1)[0]
        price = book_prices.get(bid, round(random.uniform(5, 50), 2))
        total = round(price * qty, 2)

        new_orders.append([
            str(next_order_id), str(cid), str(bid),
            order_date, str(qty), str(total)
        ])
        next_order_id += 1

ord_rows.extend(new_orders)
print(f"Orders after adding 7000: {len(ord_rows)}")

# ── 2. Add 25 duplicate rows to books ──────────────────────────────
dup_books = random.choices(books_rows, k=25)
books_rows.extend([copy.copy(r) for r in dup_books])
print(f"Books after adding 25 dupes: {len(books_rows)}")

# ── 3. Add 42 duplicate rows to customers ──────────────────────────
dup_custs = random.choices(cust_rows, k=42)
cust_rows.extend([copy.copy(r) for r in dup_custs])
print(f"Customers after adding 42 dupes: {len(cust_rows)}")

# ── 4. Add 100 duplicate rows to orders ─────────────────────────────
dup_orders = random.choices(ord_rows, k=100)
ord_rows.extend([copy.copy(r) for r in dup_orders])
print(f"Orders after adding 100 dupes: {len(ord_rows)}")

# ── Write back ──────────────────────────────────────────────────────
def write_csv(path, header, rows):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

write_csv(f"{DATA_DIR}/books.csv", books_hdr, books_rows)
write_csv(f"{DATA_DIR}/customers.csv", cust_hdr, cust_rows)
write_csv(f"{DATA_DIR}/orders.csv", ord_hdr, ord_rows)

print("\n✓ All CSV files updated successfully.")
print(f"  books.csv:     {len(books_rows)} rows (500 original + 25 duplicates)")
print(f"  customers.csv: {len(cust_rows)} rows (500 original + 42 duplicates)")
print(f"  orders.csv:    {len(ord_rows)} rows (500 original + 7000 new + 100 duplicates)")
