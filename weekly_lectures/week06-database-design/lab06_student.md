# Lab 6: Database Design & Normalization

## OMIS 105 — Database Management Systems
**Week 6 | Estimated time: 75–90 minutes**

---

## Setup

```python
import duckdb
con = duckdb.connect()
con.sql("CREATE TABLE orders_denorm AS SELECT * FROM read_csv_auto('orders_denormalized.csv')")
```

---

## Part 1: Functional Dependencies (15 points)

**Q1.** List all functional dependencies you can identify in the `orders_denormalized` table. Write a query to verify at least 3 of them.

**Q2.** What is the candidate key for `orders_denormalized`? Prove it with a query that checks uniqueness.

**Q3.** Classify each FD as "full," "partial," or "transitive" with respect to the candidate key.

---

## Part 2: Identifying Anomalies (10 points)

**Q4.** Write a query that demonstrates the **redundancy** problem — show how many times each customer's information is repeated.

**Q5.** Describe (in words) how each of the following anomalies would occur in this table: update anomaly, insertion anomaly, deletion anomaly. Give specific examples.

---

## Part 3: Normalization (25 points)

**Q6.** Decompose `orders_denormalized` into **2NF**. Write CREATE TABLE statements and INSERT...SELECT queries to populate each new table. Verify row counts.

**Q7.** Further decompose your 2NF tables into **3NF**. Show your CREATE TABLE statements.

**Q8.** Is your 3NF schema also in BCNF? Explain why or why not.

---

## Part 4: Design Challenge (15 points)

**Q9.** Given the following denormalized table for a library, normalize it to 3NF:

```
library_flat(
    loan_id, loan_date, return_date,
    member_id, member_name, member_email, member_phone,
    book_id, book_title, isbn, author_name, author_nationality,
    branch_id, branch_name, branch_city
)
```

List all FDs, then provide the 3NF decomposition (CREATE TABLE statements).

**Q10.** Draw an ER diagram for your normalized library schema.

---

## Part 5: Denormalization Discussion (10 points)

**Q11.** Create a VIEW that presents the denormalized data from your normalized ShopSmart tables. Show that it returns the same data as the original denormalized table.

**Q12.** Describe two real-world scenarios where denormalization would be appropriate. For each, explain what you would denormalize and the trade-offs involved.

---

## Submission

- Submit notebook with all queries, outputs, and written explanations
- **Total: 75 points**

