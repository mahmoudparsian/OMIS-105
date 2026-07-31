# Lab 8: Transactions & ACID — INSTRUCTOR SOLUTIONS

## OMIS 105 — Database Management Systems
**Week 8 | Answer Key**

---

## Part 1: ACID Concepts (15 points)

**Q1.** (8 pts, 2 each)
- **Atomicity**: All operations in a transaction succeed or none do. Example: When placing a ShopSmart order, the order row, order_items, and stock update all happen together — if stock update fails, the order row is also removed.
- **Consistency**: The database always moves from one valid state to another. Example: A CHECK constraint ensures product prices can never be negative; any transaction violating this is rejected.
- **Isolation**: Concurrent transactions don't interfere with each other. Example: Two customers buying the last item — only one should succeed; the other should see updated stock.
- **Durability**: Once committed, data survives crashes. Example: After a customer completes checkout and sees confirmation, their order persists even if the server crashes.

**Q2.** (7 pts)
a) **Isolation** — without proper isolation, both might read stock=1 and both succeed.
b) **Atomicity** — partial insert violates all-or-nothing.
c) **Consistency** — violates CHECK constraint.
d) **Durability** — committed data should survive any failure.

---

## Part 2: Basic Transactions (15 points)

**Q3.** (5 pts)
```python
con.sql("SELECT * FROM bank_accounts").show()  # Before

con.execute("BEGIN")
con.execute("UPDATE bank_accounts SET balance = balance - 200 WHERE account_id = 1")
con.execute("UPDATE bank_accounts SET balance = balance + 200 WHERE account_id = 2")
con.execute("COMMIT")

con.sql("SELECT * FROM bank_accounts").show()  # After
# Alice: 800, Bob: 700
```

**Q4.** (5 pts)
```python
try:
    con.execute("BEGIN")
    con.execute("UPDATE bank_accounts SET balance = balance - 1500 WHERE account_id = 3")
    con.execute("UPDATE bank_accounts SET balance = balance + 1500 WHERE account_id = 1")
    con.execute("COMMIT")
except Exception as e:
    con.execute("ROLLBACK")
    print(f"Rolled back: {e}")

con.sql("SELECT * FROM bank_accounts").show()
# Carol still has 750 — CHECK constraint prevented the overdraw
```

**Q5.** (5 pts)
```python
con.execute("BEGIN")
con.execute("INSERT INTO bank_accounts VALUES (4, 'Dave', 300.00)")
con.execute("SAVEPOINT after_dave")
con.execute("INSERT INTO bank_accounts VALUES (5, 'Eve', 400.00)")
con.execute("ROLLBACK TO SAVEPOINT after_dave")
con.execute("COMMIT")

con.sql("SELECT * FROM bank_accounts WHERE account_id IN (4, 5)").show()
# Dave exists (300), Eve does not
```

---

## Part 3: Transaction Patterns (20 points)

**Q6.** (10 pts)
```python
def transfer(con, from_id, to_id, amount):
    try:
        con.execute("BEGIN")
        bal = con.sql(f"SELECT balance FROM bank_accounts WHERE account_id={from_id}").fetchone()
        if bal is None:
            raise Exception(f"Account {from_id} not found")
        if bal[0] < amount:
            raise Exception(f"Insufficient funds: ${bal[0]} < ${amount}")
        
        dest = con.sql(f"SELECT account_id FROM bank_accounts WHERE account_id={to_id}").fetchone()
        if dest is None:
            raise Exception(f"Account {to_id} not found")
        
        con.execute(f"UPDATE bank_accounts SET balance = balance - {amount} WHERE account_id = {from_id}")
        con.execute(f"UPDATE bank_accounts SET balance = balance + {amount} WHERE account_id = {to_id}")
        con.execute("COMMIT")
        print(f"Transferred ${amount} from {from_id} to {to_id}")
        return True
    except Exception as e:
        con.execute("ROLLBACK")
        print(f"Transfer failed: {e}")
        return False

# Tests
transfer(con, 1, 2, 100)        # Valid
transfer(con, 3, 1, 10000)      # Insufficient funds
transfer(con, 1, 99, 50)        # Non-existent account
```

**Q7.** (10 pts)
```python
def place_order(con, customer_id, items):
    try:
        con.execute("BEGIN")
        oid = con.sql("SELECT COALESCE(MAX(order_id),0)+1 FROM orders").fetchone()[0]
        con.execute(f"INSERT INTO orders VALUES ({oid},{customer_id},CURRENT_DATE,'processing',0)")
        
        total = 0
        iid = con.sql("SELECT COALESCE(MAX(item_id),0) FROM order_items").fetchone()[0]
        
        for product_id, qty in items:
            iid += 1
            row = con.sql(f"SELECT price, stock_quantity FROM products WHERE product_id={product_id}").fetchone()
            if row is None:
                raise Exception(f"Product {product_id} not found")
            price, stock = row
            if stock < qty:
                raise Exception(f"Product {product_id}: need {qty}, have {stock}")
            
            line = round(price * qty, 2)
            total += line
            con.execute(f"INSERT INTO order_items VALUES ({iid},{oid},{product_id},{qty},{price})")
            con.execute(f"UPDATE products SET stock_quantity=stock_quantity-{qty} WHERE product_id={product_id}")
        
        con.execute(f"UPDATE orders SET total_amount={round(total,2)} WHERE order_id={oid}")
        con.execute("COMMIT")
        print(f"Order {oid}: {len(items)} items, ${total:.2f}")
        return oid
    except Exception as e:
        con.execute("ROLLBACK")
        print(f"Order failed: {e}")
        return None

place_order(con, 1, [(1,1),(5,2)])          # Valid
place_order(con, 2, [(1,1),(999,1)])         # Product 999 missing
```

---

## Part 4: Concurrency Analysis (10 points)

**Q8.** (5 pts)
a) Final balance = $700. Should be $500 ($1000 - $200 - $300).
b) **Lost Update** — T2's update overwrites T1's committed change.
c) Fix: use atomic updates:
```sql
T1: UPDATE accounts SET balance = balance - 200 WHERE id = 1;
T2: UPDATE accounts SET balance = balance - 300 WHERE id = 1;
```
Or use SERIALIZABLE isolation level.

**Q9.** (5 pts)
- **READ UNCOMMITTED**: Acceptable for rough analytics dashboards that tolerate stale data. Not appropriate for inventory checks.
- **READ COMMITTED**: Good default for most ShopSmart operations (product browsing, order history). Not ideal for inventory reservation during checkout.
- **REPEATABLE READ**: Good for generating reports that span multiple queries. Over-kill for simple lookups.
- **SERIALIZABLE**: Necessary for buying the last item in stock, financial transactions. Too slow for product search pages.

---

## Part 5: Real-World Design (15 points)

**Q10.** (15 pts)
```python
# Refund table
con.sql("""
    CREATE TABLE IF NOT EXISTS refunds (
        refund_id INTEGER PRIMARY KEY,
        order_id INTEGER REFERENCES orders(order_id),
        refund_date DATE NOT NULL,
        refund_amount DECIMAL(10,2) CHECK (refund_amount > 0),
        reason VARCHAR
    )
""")

def process_return(con, order_id, reason="Customer return"):
    try:
        con.execute("BEGIN")
        
        # 1. Verify order exists and is 'completed'
        order = con.sql(f"""
            SELECT status, total_amount FROM orders WHERE order_id = {order_id}
        """).fetchone()
        if order is None:
            raise Exception(f"Order {order_id} not found")
        if order[0] != 'completed':
            raise Exception(f"Order {order_id} status is '{order[0]}', not 'completed'")
        
        # 2. Update order status
        con.execute(f"UPDATE orders SET status = 'cancelled' WHERE order_id = {order_id}")
        
        # 3. Restore stock for each item
        items = con.sql(f"""
            SELECT product_id, quantity FROM order_items WHERE order_id = {order_id}
        """).fetchall()
        for pid, qty in items:
            con.execute(f"UPDATE products SET stock_quantity = stock_quantity + {qty} WHERE product_id = {pid}")
        
        # 4. Create refund record
        rid = con.sql("SELECT COALESCE(MAX(refund_id),0)+1 FROM refunds").fetchone()[0]
        con.execute(f"""
            INSERT INTO refunds VALUES ({rid}, {order_id}, CURRENT_DATE, {order[1]}, '{reason}')
        """)
        
        con.execute("COMMIT")
        print(f"Return processed: Order {order_id}, refund ${order[1]:.2f}")
        return True
    except Exception as e:
        con.execute("ROLLBACK")
        print(f"Return failed: {e}")
        return False
```

**Grading**: 5 pts for refund table design, 5 pts for correct transaction logic, 3 pts for error handling, 2 pts for stock restoration.

---

## Grading Rubric

| Part | Points |
|------|--------|
| Part 1: ACID Concepts | 15 |
| Part 2: Basic Transactions | 15 |
| Part 3: Transaction Patterns | 20 |
| Part 4: Concurrency Analysis | 10 |
| Part 5: Real-World Design | 15 |
| **Total** | **75** |

