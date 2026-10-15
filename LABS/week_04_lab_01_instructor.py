import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Week 04: SQL Aggregation
    ## Lab 01 — Aggregate Functions · Instructor

    Work with a **Sales** database. Master `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, and `HAVING`. Run the setup cells first, then each question. Answers are filled in.

    See `week_04_lab_01_instructor_design_notes.md` in this folder for the reasoning
    behind Q8 (explain), Q11 (debug), and Q12 (bonus).
    """)
    return

@app.cell
def _():
    import marimo as mo

    return (mo,)

@app.cell
def _(mo):
    regions = mo.sql(
        f"""
        CREATE OR REPLACE TABLE regions AS
        SELECT * FROM (
            VALUES
            (1,'North East','USA'),(2,'South','USA'),(3,'Midwest','USA'),
            (4,'West','USA'),(5,'Europe','EU')
        ) AS t(region_id, region_name, country);
        """
    )
    return

@app.cell
def _(mo):
    salespeople = mo.sql(
        f"""
        CREATE OR REPLACE TABLE salespeople AS
        SELECT * FROM (
            VALUES
            (1,'Alice',   1,'2020-01-15',65000),
            (2,'Bob',     2,'2019-06-01',60000),
            (3,'Carol',   3,'2021-03-20',62000),
            (4,'David',   4,'2018-11-10',70000),
            (5,'Eva',     5,'2022-02-28',75000),
            (6,'Frank',   1,'2020-09-15',64000),
            (7,'Grace',   2,'2021-07-01',61000),
            (8,'Henry',   3,'2017-04-12',68000),
            (9,'Iris',    4,'2023-01-05',66000),
            (10,'Jack',   5,'2019-08-20',72000)
        ) AS t(sp_id, name, region_id, hire_date, base_salary);
        """
    )
    return

@app.cell
def _(mo):
    sales = mo.sql(
        f"""
        CREATE OR REPLACE TABLE sales AS
        SELECT * FROM (
            VALUES
            (1, 1,'Widget A',  5000,  '2024-01-10','Q1'),
            (2, 1,'Widget B',  3200,  '2024-02-15','Q1'),
            (3, 2,'Gadget X',  7800,  '2024-01-20','Q1'),
            (4, 2,'Widget A',  4100,  '2024-03-05','Q1'),
            (5, 3,'Gadget Y',  6500,  '2024-04-10','Q2'),
            (6, 3,'Widget B',  2900,  '2024-05-20','Q2'),
            (7, 4,'Premium Z', 12000, '2024-04-15','Q2'),
            (8, 4,'Widget A',  8200,  '2024-06-01','Q2'),
            (9, 5,'Premium Z', 15000, '2024-07-10','Q3'),
            (10,5,'Gadget X',  9300,  '2024-08-05','Q3'),
            (11,6,'Widget B',  3700,  '2024-07-20','Q3'),
            (12,6,'Widget A',  4400,  '2024-09-10','Q3'),
            (13,7,'Gadget Y',  5600,  '2024-10-05','Q4'),
            (14,7,'Premium Z', 11000, '2024-11-15','Q4'),
            (15,8,'Widget A',  6300,  '2024-10-20','Q4'),
            (16,8,'Gadget X',  8900,  '2024-12-01','Q4'),
            (17,9,'Widget B',  3100,  '2024-11-10','Q4'),
            (18,9,'Premium Z', 14000, '2024-12-20','Q4'),
            (19,10,'Gadget Y', 7200,  '2024-11-25','Q4'),
            (20,10,'Widget A', 5500,  '2024-12-30','Q4')
        ) AS t(sale_id, sp_id, product, amount, sale_date, quarter);
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q1. Count the total number of sales records.
    """)
    return

@app.cell
def _(mo, sales):
    q1 = mo.sql(
        f"""
        SELECT COUNT(*) AS total_sales
        FROM sales;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q2. Find the total (`SUM`) of all sale amounts.
    """)
    return

@app.cell
def _(mo, sales):
    q2 = mo.sql(
        f"""
        SELECT SUM(amount) AS total_revenue
        FROM sales;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q3. Calculate the average sale amount.
    """)
    return

@app.cell
def _(mo, sales):
    q3 = mo.sql(
        f"""
        SELECT ROUND(AVG(amount), 2) AS avg_sale
        FROM sales;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q4. Find the minimum and maximum sale amounts.
    """)
    return

@app.cell
def _(mo, sales):
    q4 = mo.sql(
        f"""
        SELECT MIN(amount) AS min_sale, MAX(amount) AS max_sale
        FROM sales;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q5. Count sales per salesperson (`sp_id`).
    """)
    return

@app.cell
def _(mo, sales):
    q5 = mo.sql(
        f"""
        SELECT sp_id, COUNT(*) AS num_sales
        FROM sales
        GROUP BY sp_id
        ORDER BY num_sales DESC;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q6. Calculate total revenue per quarter.
    """)
    return

@app.cell
def _(mo, sales):
    q6 = mo.sql(
        f"""
        SELECT quarter, SUM(amount) AS total
        FROM sales
        GROUP BY quarter
        ORDER BY quarter;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q7. Find the average base salary of salespeople.
    """)
    return

@app.cell
def _(mo, salespeople):
    q7 = mo.sql(
        f"""
        SELECT ROUND(AVG(base_salary), 2) AS avg_salary
        FROM salespeople;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q8. Count how many salespeople are in each region.

    ✍️ **Explain it (sample answer):** "No — this only groups the rows
    that already exist in `salespeople`. A region with zero salespeople
    has no rows to group, so it simply wouldn't appear at all — not even
    with a `0`. To see 'empty' regions, you'd need to start from the
    `regions` table and LEFT JOIN to `salespeople`, keeping every region
    even when nothing matches." (This is exactly what next class covers.)
    """)
    return

@app.cell
def _(mo, salespeople):
    q8 = mo.sql(
        f"""
        -- grouping salespeople alone can never reveal a region with 0 --
        -- there'd be no row to group in the first place
        SELECT region_id, COUNT(*) AS num_people
        FROM salespeople
        GROUP BY region_id;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q9. Find the total revenue per product.
    """)
    return

@app.cell
def _(mo, sales):
    q9 = mo.sql(
        f"""
        SELECT product, SUM(amount) AS total
        FROM sales
        GROUP BY product
        ORDER BY total DESC;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q10. Find the maximum single sale amount per quarter.
    """)
    return

@app.cell
def _(mo, sales):
    q10 = mo.sql(
        f"""
        SELECT quarter, MAX(amount) AS max_sale
        FROM sales
        GROUP BY quarter
        ORDER BY quarter;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Q11. 🐞 Debug it

    Broken (silently wrong) query:

    ```sql
    SELECT COUNT(product) AS num_products FROM sales;
    ```

    **The bug:** `COUNT(product)` counts every **row** that has a
    non-empty `product` value — all 20 of them — not how many *different*
    products there are. It's not asking the question the classmate
    thinks it's asking.

    **The fix:** `COUNT(DISTINCT product)`.

    **Talking point for class:** `COUNT(column)` vs `COUNT(DISTINCT
    column)` is one of the most common real-world analytics mistakes —
    "how many customers ordered" vs "how many orders" is the exact same
    trap, and it silently inflates a number with no error at all.
    """)
    return

@app.cell
def _(mo, sales):
    q11 = mo.sql(
        f"""
        -- COUNT(product) = 20 (every row); we want distinct products = 5
        SELECT COUNT(DISTINCT product) AS num_products
        FROM sales;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🌟 Q12. Bonus (optional)

    Total revenue per product, Q4 sales only, highest first.

    Expected: Premium Z (25,000), Gadget Y (12,800), Widget A (11,800),
    Gadget X (8,900), Widget B (3,100).
    """)
    return

@app.cell
def _(mo, sales):
    q12 = mo.sql(
        f"""
        SELECT product, SUM(amount) AS total
        FROM sales
        WHERE quarter = 'Q4'
        GROUP BY product
        ORDER BY total DESC;
        """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## ✅ Exit Ticket — before you submit

    (Instructor copy — read a few out loud, anonymously, next class.
    Q8's answer is a deliberate setup for next session's LEFT JOIN lab —
    worth calling back to explicitly when you introduce LEFT JOIN.)
    """)
    return

@app.cell
def _():
    exit_ticket = """
    1. One thing that clicked for you today:


    2. One thing about SQL that is still fuzzy or confusing:


    """
    return (exit_ticket,)

if __name__ == "__main__":
    app.run()
