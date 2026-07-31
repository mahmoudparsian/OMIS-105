# Lab 8: Transactions & ACID

## OMIS 105 — Database Management Systems
**Week 8 | Estimated time: 75–90 minutes**

---

## Setup

```python
import duckdb
con = duckdb.connect()
for t, f in [('categories','categories.csv'),('products','products.csv'),
             ('customers','customers.csv'),('orders','orders.csv'),
             ('order_items','order_items.csv'),('shipping','shipping.csv')]:
    con.sql(f"CREATE TABLE {t} AS SELECT * FROM read_csv_auto('{f}')")

# Create a bank_accounts table for exercises
con.sql("""
    CREATE TABLE bank_accounts (
        account_id INTEGER PRIMARY KEY,
        owner_name VARCHAR NOT NULL,
        balance DECIMAL(10,2) CHECK (balance >= 0)
    )
""")
con.execute("INSERT INTO bank_accounts VALUES (1,'Alice',1000.00)")
con.execute("INSERT INTO bank_accounts VALUES (2,'Bob',500.00)")
con.execute("INSERT INTO bank_accounts VALUES (3,'Carol',750.00)")
```

---

## Part 1: ACID Concepts (15 points)

**Q1.** In your own words, explain each ACID property (2–3 sentences each). Give a ShopSmart example for each.

**Q2.** For each scenario, identify which ACID property is most at risk and explain why:

a) Two customers simultaneously buy the last item in stock.
b) The server crashes while processing a multi-item order — 2 of 3 items were inserted.
c) A price update sets price to -$5.
d) After a successful checkout, the order disappears from the database.

---

## Part 2: Basic Transactions (15 points)

**Q3.** Write a transaction that transfers $200 from Alice (account 1) to Bob (account 2). Verify the balances before and after.

```sql
-- Your transaction here
```

**Q4.** Write a transaction that attempts to transfer $1500 from Carol to Alice. What happens when the CHECK constraint is violated? Show the balances after the attempt.

```sql
-- Your transaction here
```

**Q5.** Using a SAVEPOINT, write a transaction that:
1. Adds a new account for "Dave" with $300
2. Creates a savepoint
3. Adds a new account for "Eve" with $400
4. Rolls back to the savepoint (undoing Eve)
5. Commits (keeping Dave)

Verify that Dave exists but Eve does not.

```sql
-- Your transaction here
```

---

## Part 3: Transaction Patterns (20 points)

**Q6.** Write a Python function `transfer(con, from_id, to_id, amount)` that:
- Begins a transaction
- Checks that the sender has sufficient balance
- Performs the transfer
- Commits on success, rolls back on failure
- Returns True/False

Test it with: (a) a valid transfer, (b) insufficient funds, (c) non-existent account.

```python
# Your function here
```

**Q7.** Write a Python function `place_order(con, customer_id, items)` where `items` is a list of `(product_id, quantity)` tuples. The function should:
- Begin a transaction
- Create a new order record
- For each item: check stock, insert order_item, decrement stock
- If any item fails, roll back the entire order
- Update the order total on success
- Commit

Test with a valid order and an order with an out-of-stock item.

```python
# Your function here
```

---

## Part 4: Concurrency Analysis (10 points)

**Q8.** Consider this scenario with two transactions running concurrently:

```
T1: BEGIN; SELECT balance FROM accounts WHERE id=1; -- reads $1000
T2: BEGIN; SELECT balance FROM accounts WHERE id=1; -- reads $1000
T1: UPDATE accounts SET balance=1000-200=800 WHERE id=1; COMMIT;
T2: UPDATE accounts SET balance=1000-300=700 WHERE id=1; COMMIT;
```

a) What is the final balance? What should it be?
b) Which concurrency problem is this?
c) How would you fix this? Show the corrected SQL.

**Q9.** For each isolation level (READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE), describe a ShopSmart scenario where that level would be appropriate or inappropriate.

---

## Part 5: Real-World Design (15 points)

**Q10.** Design a complete transaction for a "product return" workflow at ShopSmart. The transaction should:
- Update the order status to 'returned'
- Restore the product stock
- Create a refund record (design the refund table yourself)
- Handle errors gracefully

Write both the CREATE TABLE for the refund table and the Python function for the transaction.

```python
# Your design + code here
```

---

## Submission

- Submit notebook with all code, queries, outputs, and written explanations
- **Total: 75 points**

