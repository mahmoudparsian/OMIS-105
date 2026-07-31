import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Superstore Sales Analysis with DuckDB

    This notebook performs all data exploration and analysis using **DuckDB** SQL.
    Plotting code is decoupled into `superstore_plots.py` and called inline after queries.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup
    """)
    return


@app.cell
def _():
    import duckdb
    import warnings
    warnings.filterwarnings('ignore')

    # Plotting functions live in a separate module
    import superstore_plots as plots

    # Create a persistent connection so all cells share the same context
    con = duckdb.connect()
    return con, plots


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load Data
    """)
    return


@app.cell
def _(con):
    con.execute("""
        CREATE OR REPLACE TABLE superstore AS
        SELECT *,
            "Order Date" AS order_dt,
            "Ship Date" AS ship_dt
        FROM read_csv_auto("./sample_superstore.csv", header=true, dateformat='%m/%d/%Y')
    """)

    con.execute("SELECT count(*) AS total_rows FROM superstore").df()
    return


@app.cell
def _(con):
    # Rename columns to snake_case
    con.execute("""
        ALTER TABLE superstore RENAME COLUMN "Row ID" TO row_id;
        ALTER TABLE superstore RENAME COLUMN "Order ID" TO order_id;
        ALTER TABLE superstore RENAME COLUMN "Order Date" TO order_date;
        ALTER TABLE superstore RENAME COLUMN "Ship Date" TO ship_date;
        ALTER TABLE superstore RENAME COLUMN "Ship Mode" TO ship_mode;
        ALTER TABLE superstore RENAME COLUMN "Customer ID" TO customer_id;
        ALTER TABLE superstore RENAME COLUMN "Customer Name" TO customer_name;
        ALTER TABLE superstore RENAME COLUMN "Country/Region" TO country_region;
        ALTER TABLE superstore RENAME COLUMN "State/Province" TO state_province;
        ALTER TABLE superstore RENAME COLUMN "Postal Code" TO postal_code;
        ALTER TABLE superstore RENAME COLUMN "Product ID" TO product_id;
        ALTER TABLE superstore RENAME COLUMN "Sub-Category" TO sub_category;
        ALTER TABLE superstore RENAME COLUMN "Product Name" TO product_name;
    """)

    # Lowercase the rest (already single-word but uppercase first letter)
    for col in ["Segment", "City", "Region", "Category", "Sales", "Quantity", "Discount", "Profit"]:
        con.execute(f'ALTER TABLE superstore RENAME COLUMN "{col}" TO {col.lower()}')

    con.execute("DESCRIBE superstore").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data Overview
    """)
    return


@app.cell
def _(con):
    # First 5 rows
    con.execute("SELECT * FROM superstore LIMIT 5").df()
    return


@app.cell
def _(con):
    # Column names and types
    con.execute("DESCRIBE superstore").df()
    return


@app.cell
def _(con):
    # Summary statistics
    con.execute("""
        SELECT
            count(*) AS n,
            round(avg(sales), 2) AS avg_sales,
            round(min(sales), 2) AS min_sales,
            round(max(sales), 2) AS max_sales,
            round(stddev(sales), 2) AS std_sales,
            round(avg(profit), 2) AS avg_profit,
            round(min(profit), 2) AS min_profit,
            round(max(profit), 2) AS max_profit,
            round(avg(quantity), 2) AS avg_qty,
            round(avg(discount), 3) AS avg_discount
        FROM superstore
    """).df()
    return


@app.cell
def _(con):
    # Null check
    con.execute("""
        SELECT
            count(*) - count(order_id) AS null_order_id,
            count(*) - count(sales) AS null_sales,
            count(*) - count(profit) AS null_profit,
            count(*) - count(customer_name) AS null_customer_name
        FROM superstore
    """).df()
    return


@app.cell
def _(con):
    # Duplicate check
    con.execute("""
        SELECT count(*) AS duplicate_rows
        FROM (
            SELECT row_id, count(*) AS cnt
            FROM superstore
            GROUP BY row_id
            HAVING cnt > 1
        )
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Category & Sub-Category Analysis
    """)
    return


@app.cell
def _(con):
    # 1. Category-wise total sales and profit
    df_category = con.execute("""
        SELECT category,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit,
               round(sum(profit)/sum(sales)*100, 2) AS profit_margin_pct
        FROM superstore
        GROUP BY category
        ORDER BY total_sales DESC
    """).df()
    df_category
    return (df_category,)


@app.cell
def _(df_category, plots):
    plots.plot_category_sales_profit(df_category)
    return


@app.cell
def _(con):
    # 2. Sub-category sales and profit
    df_subcat = con.execute("""
        SELECT sub_category,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit,
               count(*) AS order_count
        FROM superstore
        GROUP BY sub_category
        ORDER BY total_sales DESC
    """).df()
    df_subcat
    return (df_subcat,)


@app.cell
def _(df_subcat, plots):
    plots.plot_top_subcategories(df_subcat)
    return


@app.cell
def _(df_subcat, plots):
    plots.plot_loss_subcategories(df_subcat)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Regional Analysis
    """)
    return


@app.cell
def _(con):
    # 3. Region-wise sales and profit
    df_region = con.execute("""
        SELECT region,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit,
               count(DISTINCT customer_id) AS unique_customers,
               round(sum(profit)/sum(sales)*100, 2) AS margin_pct
        FROM superstore
        GROUP BY region
        ORDER BY total_sales DESC
    """).df()
    df_region
    return (df_region,)


@app.cell
def _(df_region, plots):
    plots.plot_region_sales_profit(df_region)
    return


@app.cell
def _(con):
    # 4. Top 10 cities by sales
    df_top_cities_sales = con.execute("""
        SELECT city, state_province,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit
        FROM superstore
        GROUP BY city, state_province
        ORDER BY total_sales DESC
        LIMIT 10
    """).df()
    df_top_cities_sales
    return (df_top_cities_sales,)


@app.cell
def _(df_top_cities_sales, plots):
    plots.plot_top_cities(df_top_cities_sales)
    return


@app.cell
def _(con):
    # 5. Top 10 cities by profit
    df_top_cities_profit = con.execute("""
        SELECT city, state_province,
               round(sum(profit), 2) AS total_profit,
               round(sum(sales), 2) AS total_sales
        FROM superstore
        GROUP BY city, state_province
        ORDER BY total_profit DESC
        LIMIT 10
    """).df()
    df_top_cities_profit
    return (df_top_cities_profit,)


@app.cell
def _(df_top_cities_profit, plots):
    plots.plot_top_cities_profit(df_top_cities_profit)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Segment & Shipping Analysis
    """)
    return


@app.cell
def _(con):
    # 6. Segment-wise sales and profit
    df_segment = con.execute("""
        SELECT segment,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit,
               count(*) AS order_count,
               round(avg(discount), 3) AS avg_discount
        FROM superstore
        GROUP BY segment
        ORDER BY total_sales DESC
    """).df()
    df_segment
    return (df_segment,)


@app.cell
def _(df_segment, plots):
    plots.plot_segment_sales_profit(df_segment)
    return


@app.cell
def _(con):
    # 7. Ship mode analysis
    df_shipmode = con.execute("""
        SELECT ship_mode,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit,
               count(*) AS order_count,
               round(avg(ship_dt - order_dt), 1) AS avg_ship_days
        FROM superstore
        GROUP BY ship_mode
        ORDER BY total_sales DESC
    """).df()
    df_shipmode
    return (df_shipmode,)


@app.cell
def _(df_shipmode, plots):
    plots.plot_shipmode_sales_profit(df_shipmode)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Time Series Analysis
    """)
    return


@app.cell
def _(con):
    # 8. Monthly sales trend
    df_monthly = con.execute("""
        SELECT strftime(order_dt, '%Y-%m') AS month,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit,
               count(*) AS order_count
        FROM superstore
        GROUP BY month
        ORDER BY month
    """).df()
    df_monthly.head(10)
    return (df_monthly,)


@app.cell
def _(df_monthly, plots):
    plots.plot_monthly_trend(df_monthly)
    return


@app.cell
def _(con):
    # 9. Yearly performance
    df_yearly = con.execute("""
        SELECT year(order_dt) AS order_year,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit,
               count(DISTINCT order_id) AS total_orders,
               count(DISTINCT customer_id) AS unique_customers
        FROM superstore
        GROUP BY order_year
        ORDER BY order_year
    """).df()
    df_yearly
    return (df_yearly,)


@app.cell
def _(df_yearly, plots):
    plots.plot_yearly_performance(df_yearly)
    return


@app.cell
def _(con):
    # 10. Quarter-over-quarter growth
    df_quarterly = con.execute("""
        WITH quarterly AS (
            SELECT year(order_dt) AS yr,
                   quarter(order_dt) AS qtr,
                   round(sum(sales), 2) AS total_sales
            FROM superstore
            GROUP BY yr, qtr
        )
        SELECT yr, qtr, total_sales,
               lag(total_sales) OVER (ORDER BY yr, qtr) AS prev_qtr_sales,
               round((total_sales - lag(total_sales) OVER (ORDER BY yr, qtr))
                     / lag(total_sales) OVER (ORDER BY yr, qtr) * 100, 2) AS growth_pct
        FROM quarterly
        ORDER BY yr, qtr
    """).df()
    df_quarterly
    return (df_quarterly,)


@app.cell
def _(df_quarterly, plots):
    plots.plot_quarterly_growth(df_quarterly)
    return


@app.cell
def _(con):
    # 11. Seasonality: total sales by calendar month
    df_season = con.execute("""
        SELECT month(order_dt) AS month_num,
               strftime(order_dt, '%B') AS month_name,
               round(sum(sales), 2) AS total_sales,
               round(avg(sales), 2) AS avg_sale_per_item,
               count(DISTINCT order_id) AS num_orders
        FROM superstore
        GROUP BY month_num, month_name
        ORDER BY month_num
    """).df()
    df_season
    return (df_season,)


@app.cell
def _(df_season, plots):
    plots.plot_seasonality(df_season)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Customer Analysis
    """)
    return


@app.cell
def _(con):
    # 12. Top 10 customers by sales
    con.execute("""
        SELECT customer_name, segment,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit,
               count(DISTINCT order_id) AS num_orders
        FROM superstore
        GROUP BY customer_name, segment
        ORDER BY total_sales DESC
        LIMIT 10
    """).df()
    return


@app.cell
def _(con):
    # 13. Top 10 customers by profit
    con.execute("""
        SELECT customer_name, segment,
               round(sum(profit), 2) AS total_profit,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit)/sum(sales)*100, 2) AS margin_pct
        FROM superstore
        GROUP BY customer_name, segment
        ORDER BY total_profit DESC
        LIMIT 10
    """).df()
    return


@app.cell
def _(con):
    # 14. Worst customers (most loss-generating)
    con.execute("""
        SELECT customer_name, segment, city,
               round(sum(profit), 2) AS total_profit,
               round(sum(sales), 2) AS total_sales,
               round(avg(discount), 3) AS avg_discount
        FROM superstore
        GROUP BY customer_name, segment, city
        ORDER BY total_profit ASC
        LIMIT 10
    """).df()
    return


@app.cell
def _(con):
    # 15. Repeat customers vs one-time buyers
    con.execute("""
        WITH customer_orders AS (
            SELECT customer_id, customer_name,
                   count(DISTINCT order_id) AS num_orders,
                   round(sum(sales), 2) AS total_sales,
                   round(sum(profit), 2) AS total_profit
            FROM superstore
            GROUP BY customer_id, customer_name
        )
        SELECT
            CASE WHEN num_orders = 1 THEN 'One-time' ELSE 'Repeat' END AS customer_type,
            count(*) AS num_customers,
            round(avg(total_sales), 2) AS avg_lifetime_sales,
            round(avg(total_profit), 2) AS avg_lifetime_profit,
            round(sum(total_sales), 2) AS group_total_sales
        FROM customer_orders
        GROUP BY customer_type
    """).df()
    return


@app.cell
def _(con):
    # 16. RFM-style segmentation
    con.execute("""
        WITH customer_rfm AS (
            SELECT customer_id, customer_name,
                   max(order_dt) AS last_order,
                   count(DISTINCT order_id) AS frequency,
                   round(sum(sales), 2) AS monetary
            FROM superstore
            GROUP BY customer_id, customer_name
        )
        SELECT
            CASE
                WHEN frequency >= 10 AND monetary >= 5000 THEN 'Champions'
                WHEN frequency >= 5 AND monetary >= 2000 THEN 'Loyal'
                WHEN frequency >= 3 THEN 'Regular'
                ELSE 'At Risk'
            END AS segment,
            count(*) AS num_customers,
            round(avg(monetary), 2) AS avg_revenue,
            round(avg(frequency), 1) AS avg_orders
        FROM customer_rfm
        GROUP BY segment
        ORDER BY avg_revenue DESC
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Discount Impact Analysis
    """)
    return


@app.cell
def _(con):
    # 17. Discount vs profitability by band
    con.execute("""
        SELECT
            CASE
                WHEN discount = 0 THEN 'No discount'
                WHEN discount <= 0.2 THEN '1-20%'
                WHEN discount <= 0.4 THEN '21-40%'
                ELSE '41%+'
            END AS discount_band,
            count(*) AS order_count,
            round(sum(sales), 2) AS total_sales,
            round(sum(profit), 2) AS total_profit,
            round(avg(profit), 2) AS avg_profit_per_item,
            round(sum(profit)/sum(sales)*100, 2) AS margin_pct
        FROM superstore
        GROUP BY discount_band
        ORDER BY discount_band
    """).df()
    return


@app.cell
def _(con):
    # 18. Discount level vs average profit (binned at 0.1 increments)
    df_disc_profit = con.execute("""
        SELECT round(discount, 1) AS discount_level,
               count(*) AS n,
               round(avg(profit), 2) AS avg_profit,
               round(avg(sales), 2) AS avg_sales
        FROM superstore
        GROUP BY discount_level
        ORDER BY discount_level
    """).df()
    df_disc_profit
    return (df_disc_profit,)


@app.cell
def _(df_disc_profit, plots):
    plots.plot_discount_vs_profit(df_disc_profit)
    return


@app.cell
def _(con):
    # 19. Discount impact by category
    con.execute("""
        SELECT category,
               round(avg(discount), 3) AS avg_discount,
               round(sum(CASE WHEN discount > 0 THEN profit ELSE 0 END), 2) AS discounted_profit,
               round(sum(CASE WHEN discount = 0 THEN profit ELSE 0 END), 2) AS full_price_profit
        FROM superstore
        GROUP BY category
        ORDER BY category
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Scatter & Correlation
    """)
    return


@app.cell
def _(con, plots):
    # 20. Quantity vs Sales scatter
    df_scatter = con.execute("""
        SELECT quantity, sales, profit, segment
        FROM superstore
    """).df()

    plots.plot_quantity_vs_sales(df_scatter)
    return (df_scatter,)


@app.cell
def _(df_scatter, plots):
    plots.plot_sales_vs_profit(df_scatter)
    return


@app.cell
def _(con, plots):
    # 21. Correlation heatmap
    df_corr = con.execute("""
        SELECT sales, quantity, discount, profit
        FROM superstore
    """).df()

    plots.plot_correlation_heatmap(df_corr)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Product Analysis
    """)
    return


@app.cell
def _(con):
    # 22. Top 10 products by sales
    con.execute("""
        SELECT product_name, category, sub_category,
               round(sum(sales), 2) AS total_sales,
               sum(quantity) AS total_qty
        FROM superstore
        GROUP BY product_name, category, sub_category
        ORDER BY total_sales DESC
        LIMIT 10
    """).df()
    return


@app.cell
def _(con):
    # 23. Top 10 products by quantity sold
    con.execute("""
        SELECT product_name, sub_category,
               sum(quantity) AS total_qty,
               count(DISTINCT order_id) AS num_orders,
               round(sum(sales), 2) AS total_sales
        FROM superstore
        GROUP BY product_name, sub_category
        ORDER BY total_qty DESC
        LIMIT 10
    """).df()
    return


@app.cell
def _(con):
    # 24. Products with highest loss
    con.execute("""
        SELECT product_name, category, sub_category,
               round(sum(profit), 2) AS total_profit,
               round(avg(discount), 3) AS avg_discount,
               sum(quantity) AS total_qty
        FROM superstore
        GROUP BY product_name, category, sub_category
        ORDER BY total_profit ASC
        LIMIT 10
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## State-Level Analysis
    """)
    return


@app.cell
def _(con):
    # 25. State-level profitability ranking
    df_states = con.execute("""
        SELECT state_province,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit,
               round(sum(profit)/sum(sales)*100, 2) AS margin_pct
        FROM superstore
        GROUP BY state_province
        ORDER BY total_profit DESC
    """).df()
    df_states.head(15)
    return (df_states,)


@app.cell
def _(df_states, plots):
    plots.plot_top_states_profit(df_states, n=15)
    return


@app.cell
def _(con):
    # 26. States with negative profit
    con.execute("""
        SELECT state_province, region,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit,
               round(avg(discount), 3) AS avg_discount
        FROM superstore
        GROUP BY state_province, region
        HAVING sum(profit) < 0
        ORDER BY total_profit ASC
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Advanced Queries
    """)
    return


@app.cell
def _(con):
    # 27. Average order value by segment and region
    con.execute("""
        SELECT segment, region,
               count(DISTINCT order_id) AS num_orders,
               round(sum(sales) / count(DISTINCT order_id), 2) AS avg_order_value
        FROM superstore
        GROUP BY segment, region
        ORDER BY avg_order_value DESC
    """).df()
    return


@app.cell
def _(con):
    # 28. Shipping delay analysis
    con.execute("""
        SELECT ship_mode,
               round(avg(ship_dt - order_dt), 1) AS avg_days_to_ship,
               round(avg(profit), 2) AS avg_profit,
               count(*) AS n
        FROM superstore
        GROUP BY ship_mode
        ORDER BY avg_days_to_ship
    """).df()
    return


@app.cell
def _(con):
    # 29. Month-over-month with running total
    con.execute("""
        WITH monthly AS (
            SELECT strftime(order_dt, '%Y-%m') AS month,
                   round(sum(sales), 2) AS monthly_sales
            FROM superstore
            GROUP BY month
        )
        SELECT month, monthly_sales,
               round(sum(monthly_sales) OVER (ORDER BY month), 2) AS cumulative_sales
        FROM monthly
        ORDER BY month
    """).df()
    return


@app.cell
def _(con):
    # 30. Day-of-week ordering patterns
    con.execute("""
        SELECT dayname(order_dt) AS day_of_week,
               dayofweek(order_dt) AS day_num,
               count(*) AS order_count,
               round(sum(sales), 2) AS total_sales,
               round(avg(sales), 2) AS avg_sale
        FROM superstore
        GROUP BY day_of_week, day_num
        ORDER BY day_num
    """).df()
    return


@app.cell
def _(con):
    # 31. Basket analysis - items per order by segment
    con.execute("""
        WITH order_sizes AS (
            SELECT order_id, segment,
                   count(*) AS items_in_order,
                   sum(sales) AS order_total
            FROM superstore
            GROUP BY order_id, segment
        )
        SELECT segment,
               round(avg(items_in_order), 2) AS avg_items_per_order,
               round(avg(order_total), 2) AS avg_order_total,
               max(items_in_order) AS max_basket_size
        FROM order_sizes
        GROUP BY segment
        ORDER BY avg_order_total DESC
    """).df()
    return


@app.cell
def _(con):
    # 32. Year-over-year growth by category
    con.execute("""
        WITH yearly_cat AS (
            SELECT year(order_dt) AS yr, category,
                   round(sum(sales), 2) AS sales
            FROM superstore
            GROUP BY yr, category
        )
        SELECT yr, category, sales,
               lag(sales) OVER (PARTITION BY category ORDER BY yr) AS prev_year,
               round((sales - lag(sales) OVER (PARTITION BY category ORDER BY yr))
                     / lag(sales) OVER (PARTITION BY category ORDER BY yr) * 100, 2) AS yoy_growth_pct
        FROM yearly_cat
        ORDER BY category, yr
    """).df()
    return


@app.cell
def _(con):
    # 33. Pareto: What % of products drive 80% of sales?
    con.execute("""
        WITH product_sales AS (
            SELECT product_name,
                   sum(sales) AS total_sales
            FROM superstore
            GROUP BY product_name
        ),
        ranked AS (
            SELECT *,
                   sum(total_sales) OVER (ORDER BY total_sales DESC) AS running_total,
                   sum(total_sales) OVER () AS grand_total,
                   row_number() OVER (ORDER BY total_sales DESC) AS rn,
                   count(*) OVER () AS total_products
            FROM product_sales
        )
        SELECT
            min(rn) FILTER (WHERE running_total >= grand_total * 0.8) AS products_for_80pct_sales,
            total_products AS total_products,
            round(min(rn) FILTER (WHERE running_total >= grand_total * 0.8) * 100.0 / total_products, 1) AS pct_of_products
        FROM ranked
        GROUP BY total_products
    """).df()
    return


@app.cell
def _(con):
    # 34. Country/Region breakdown
    con.execute("""
        SELECT country_region,
               count(*) AS order_lines,
               round(sum(sales), 2) AS total_sales,
               round(sum(profit), 2) AS total_profit,
               count(DISTINCT customer_id) AS unique_customers
        FROM superstore
        GROUP BY country_region
        ORDER BY total_sales DESC
    """).df()
    return


@app.cell
def _(con):
    con.close()
    print('Done.')
    return


if __name__ == "__main__":
    app.run()
