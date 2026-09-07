# OMIS 105 — Week 8 Review Notes: Transactions, ACID & Constraints

**Course:** OMIS 105 — Introduction to Database Management Systems
**Instructor:** Dr. Mahmoud Parsian (mparsian@scu.edu)
**Quarter:** Fall 2026
**Tech Stack:** Python · DuckDB · Marimo

These notes accompany `week08_review_notebook.py`. Open the notebook
and teach from it; use these notes for timing, discussion prompts, and the
homework assignment.

---

## Dataset: CloudMetrics SaaS

The same SaaS company as Week 7. The notebook loads the four core tables,
then builds three more inside the transaction exercises:

| Table | Rows | Purpose |
|-------|------|---------|
| `plans` | 3 | Subscription tiers |
| `customers` | 10 | Companies subscribed to CloudMetrics |
| `payments` | 25 | Monthly payment records |
| `support_tickets` | 15 | Support requests by priority and category |
| `accounts` | 10 | Account balances — the subject of every transfer exercise |
| `safe_accounts` | 1 | A constrained table used to demonstrate `CHECK` / `NOT NULL` |
| `audit_log` | 4 | Who changed what, when |

**Why this dataset?** Money moving between accounts is the clearest case
for transactions. Students immediately understand why a half-finished
transfer is unacceptable.

---

## Session 1 — Transactions & ACID

### Learning Objectives

Students will be able to:

- Explain what a transaction is and why it matters
- Use `BEGIN`, `COMMIT`, and `ROLLBACK`
- Walk through a transfer scenario step by step
- Define the four ACID properties
- Explain why atomicity prevents partial updates

### Key Concepts

**Transaction:** A group of SQL statements that must either ALL
succeed or ALL fail. No partial results.

**ACID:**
- **Atomicity** — All or nothing. If one step fails, everything
  rolls back.
- **Consistency** — The database moves from one valid state to
  another. Constraints are never violated.
- **Isolation** — Concurrent transactions don't interfere with
  each other.
- **Durability** — Once committed, the data survives crashes.

**The bank transfer analogy:** Moving `$100` from Account A to
Account B requires two UPDATEs. If the first succeeds but the
second fails, `$100` disappears. Transactions prevent this.

### Teaching Flow (2 hours)

1. **Motivating scenario** (15 min): "You're transferring `$500`
   between two customer accounts. The power goes out after the
   debit but before the credit. What happens to the $500?"

2. **BEGIN / COMMIT** (20 min): Walk through a successful
   transfer. Show the account balances before, during, and after.

3. **ROLLBACK** (20 min): Simulate a failed transfer. Show that
   ROLLBACK undoes everything — balances return to original state.

4. **Multi-step scenario** (20 min): Transfer → accidental
   double-debit → ROLLBACK → retry correctly → COMMIT.

5. **ACID properties** (20 min): Go through each property with
   concrete examples from the exercises. Ask students to identify
   which property each scenario demonstrates.

6. **Practice** (25 min): Students write their own transfer
   scenarios with BEGIN/COMMIT and BEGIN/ROLLBACK.

### Discussion Questions

- What real-world systems need transactions? (Banking, airline
  bookings, inventory, e-commerce checkout)
- What would happen if databases didn't have atomicity?
- Can you think of a case where you'd WANT a partial update?

---

## Session 2 — Constraints & Data Integrity

### Learning Objectives

Students will be able to:

- Create tables with `CHECK` constraints
- Use `NOT NULL` to enforce required fields
- Handle `PRIMARY KEY` violation errors
- Write audit log entries for transaction tracking
- Simulate constraint violations and explain the error

### Key Concepts

**Constraints enforce business rules in the database itself.**
Instead of hoping the application checks for valid data,
the database rejects bad data automatically.

- `CHECK (balance >= 0)` — No negative balances
- `NOT NULL` — Field must have a value
- `PRIMARY KEY` — Unique identifier, no duplicates
- `FOREIGN KEY` — Must reference an existing row

**Audit logging:** Recording who did what and when. Critical
for financial systems, healthcare, compliance.

### Teaching Flow (2 hours)

1. **CHECK constraints** (20 min): Create a table with
   `CHECK (balance >= 0)`. Try to INSERT a negative balance.
   Show the error. Try an UPDATE that would go negative. Show
   the error.

2. **NOT NULL** (15 min): Create a table where customer_name
   is NOT NULL. Try to INSERT without a name. Show the error.

3. **PRIMARY KEY violations** (15 min): Try to INSERT a
   duplicate payment_id. Show the error. Explain why duplicates
   are dangerous.

4. **Audit logging** (25 min): Create an audit_log table.
   After each successful transaction, INSERT a record with
   timestamp, action type, and amounts.

5. **Putting it all together** (20 min): Full transfer workflow:
   BEGIN → check balance → debit → credit → log → COMMIT.
   If balance insufficient → ROLLBACK → log failed attempt.

6. **Practice** (25 min): Students build a constrained table
   and write transactions that test each constraint.

### Discussion Questions

- Should business rules live in the database or the application?
- What's the cost of NOT having constraints?
- Why do banks keep audit logs forever?

---

## Homework / Review Exercises

1. Write a transaction that processes a refund: debit the company
   account, credit the customer account, log the refund in the
   audit table.

2. Create a table with appropriate constraints for an
   e-commerce order (order_id PK, quantity > 0, total NOT NULL,
   customer_id FK). Test each constraint with invalid data.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
