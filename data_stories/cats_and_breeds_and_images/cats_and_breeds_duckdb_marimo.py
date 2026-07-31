import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🐱 Cats, Breeds & Tricks — Data Story with DuckDB + Images

    **Course:** OMIS 105 — Data Analytics with SQL
    **Topic:** Exploring a Cat Show database using DuckDB, CTEs, Window Functions, Visualizations, and Cat Avatars

    ---

    ## Database Schema

    | Table | Description |
    |-------|-------------|
    | `breeds` | Cat breed names and descriptions (15 breeds) |
    | `cats` | Individual cats with name, DOB, color, country, gender, breed, price, **image_url** (80 cats) |
    | `tricks` | Available tricks a cat can learn (15 tricks) |
    | `cat_tricks` | Many-to-many: which cat knows which trick |

    ### Relationships
    ```
    breeds (1) ──── (M) cats (1) ──── (M) cat_tricks (M) ──── (1) tricks
    ```

    ### What's New: Image Column
    Each cat has a unique avatar image generated via [RoboHash](https://robohash.org) (set=4, kitten avatars).
    The `image_url` column stores the URL, enabling visual gallery displays directly in the notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup: Import Libraries and Load Data

    All display and plotting functions are in external modules to keep this notebook clean:
    - `display_utils.py` — styled tables, image galleries, tables with thumbnails
    - `plot_utils.py` — bar, pie, scatter, line, histogram, grouped/stacked bar charts
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import warnings
    warnings.filterwarnings('ignore')

    # Import our utility modules (external to keep notebook clean)
    from display_utils import (run_query, show_table, run_and_show,
                                show_gallery, show_table_with_images)
    from plot_utils import (plot_bar, plot_horizontal_bar, plot_pie,
                             plot_line, plot_scatter, plot_grouped_bar,
                             plot_histogram, plot_stacked_bar)

    # Create an in-memory DuckDB connection
    con = duckdb.connect(database=':memory:')

    print('Libraries loaded successfully!')
    return (
        con,
        plot_bar,
        plot_grouped_bar,
        plot_histogram,
        plot_horizontal_bar,
        plot_line,
        plot_pie,
        plot_scatter,
        run_and_show,
        run_query,
        show_gallery,
        show_table_with_images,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create DuckDB Tables from CSV Files

    DuckDB reads CSV files directly into tables with automatic type detection.
    """)
    return


@app.cell
def _(con):
    # ── Create tables by reading CSV files ──

    con.execute("""
        CREATE TABLE breeds AS
        SELECT *
        FROM read_csv_auto('data/breeds.csv');
    """)

    con.execute("""
        CREATE TABLE tricks AS
        SELECT *
        FROM read_csv_auto('data/tricks.csv');
    """)

    con.execute("""
        CREATE TABLE cats AS
        SELECT *
        FROM read_csv_auto('data/cats.csv');
    """)

    con.execute("""
        CREATE TABLE cat_tricks AS
        SELECT *
        FROM read_csv_auto('data/cat_tricks.csv');
    """)

    print('All 4 tables created successfully!')
    print()
    for table in ['breeds', 'tricks', 'cats', 'cat_tricks']:
        count = con.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        print(f'  {table:12s} --> {count:>4d} rows')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Section 1: Meet the Cats! (Image Gallery)

    Let's see our cats with their unique avatar images. Each cat has a distinct
    avatar generated from their name — no two cats look alike!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q1: Full Cat Gallery
    Display all 80 cats in a visual card grid with their avatar, breed, and price.
    """)
    return


@app.cell
def _(con, run_query, show_gallery):
    _sql = """
    SELECT name, breed, price, country, image_url
    FROM   cats
    ORDER BY name;
    """

    _df = run_query(con, _sql)
    show_gallery(_df, name_col='name', image_col='image_url',
                 detail_cols=['breed', 'price', 'country'],
                 title='Meet All 80 Cats!', columns=5, img_size=100)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q2: Top 10 Most Expensive Cats (with Avatars)
    Show the priciest cats with their images in a table.
    """)
    return


@app.cell
def _(con, run_query, show_table_with_images):
    _sql = """
    SELECT image_url, name, breed, country, price
    FROM   cats
    ORDER BY price DESC
    LIMIT 10;
    """

    _df = run_query(con, _sql)
    show_table_with_images(_df, image_col='image_url',
                           title='Top 10 Most Expensive Cats')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q3: Cat Gallery Filtered by Breed
    Display only Bengal cats with their avatars.
    """)
    return


@app.cell
def _(con, run_query, show_gallery):
    _sql = """
    SELECT name, breed, color, price, image_url
    FROM   cats
    WHERE  breed = 'Bengal'
    ORDER BY price DESC;
    """

    _df = run_query(con, _sql)
    show_gallery(_df, name_col='name', image_col='image_url',
                 detail_cols=['color', 'price'],
                 title='Bengal Cats Gallery', columns=4, img_size=110)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Section 2: Basic SELECT Queries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q4: List All Breeds
    Retrieve all breed names and descriptions.
    """)
    return


@app.cell
def _(con, run_and_show):
    _sql = """
    SELECT breed, description
    FROM   breeds
    ORDER BY breed;
    """

    run_and_show(con, _sql, title='All Cat Breeds')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q5: Count of Cats by Country
    How many cats are registered in each country?
    """)
    return


@app.cell
def _(con, plot_bar, run_and_show):
    _sql = """
        SELECT
            country,
            COUNT(*) AS num_cats
        FROM cats
        GROUP BY country
        ORDER BY num_cats DESC;
    """

    _df = run_and_show(con, _sql, title='Cats per Country')
    plot_bar(_df, 'country', 'num_cats',
             title='Number of Cats by Country',
             xlabel='Country', ylabel='Count')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q6: Coat Color Distribution
    What are all the different coat colors?
    """)
    return


@app.cell
def _(con, plot_pie, run_and_show):
    _sql = """
        SELECT
            color,
            COUNT(*) AS num_cats
        FROM cats
        GROUP BY color
        ORDER BY num_cats DESC;
    """

    _df = run_and_show(con, _sql, title='Cats by Color')
    plot_pie(_df, 'color', 'num_cats',
             title='Distribution of Coat Colors')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q7: Average Price by Breed
    Which breeds are the most valuable on average?
    """)
    return


@app.cell
def _(con, plot_bar, run_and_show):
    _sql = """
        SELECT
            breed,
            ROUND(AVG(price), 0) AS avg_price,
            COUNT(*) AS num_cats
        FROM cats
        GROUP BY breed
        ORDER BY avg_price DESC;
    """

    _df = run_and_show(con, _sql, title='Average Price by Breed')
    plot_bar(_df, 'breed', 'avg_price',
             title='Average Cat Price by Breed',
             xlabel='Breed', ylabel='Avg Price ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q8: Price Distribution (Histogram)
    How are cat prices distributed across our dataset?
    """)
    return


@app.cell
def _(con, plot_histogram, run_query):
    _sql = """
        SELECT price
        FROM cats
        ORDER BY price;
    """

    _df = run_query(con, _sql)
    plot_histogram(_df, 'price',
                  title='Distribution of Cat Prices',
                  xlabel='Price ($)', bins=12)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q9: Cats from Germany (with Images)
    Show German cats with their avatars.
    """)
    return


@app.cell
def _(con, run_query, show_table_with_images):
    _sql = """
    SELECT image_url, name, breed, color, price
    FROM   cats
    WHERE  country = 'GERMANY'
    ORDER BY price DESC;
    """

    _df = run_query(con, _sql)
    show_table_with_images(_df, image_col='image_url',
                           title='German Cats (sorted by price)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Section 3: JOIN Queries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q10: Cats with Breed Descriptions (INNER JOIN)
    Join cats with breeds to see each cat's breed description.
    """)
    return


@app.cell
def _(con, run_query, show_table_with_images):
    _sql = """
    SELECT c.image_url,
           c.name,
           c.breed,
           b.description,
           c.price
    FROM   cats   c
    JOIN   breeds b ON c.breed = b.breed
    ORDER BY c.price DESC
    LIMIT 12;
    """

    _df = run_query(con, _sql)
    show_table_with_images(_df, image_col='image_url',
                           title='Top 12 Cats with Breed Info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q11: Number of Tricks Per Cat
    How many tricks does each cat know?
    """)
    return


@app.cell
def _(con, plot_horizontal_bar, run_and_show):
    _sql = """
        SELECT
            c.name,
            c.breed,
            COUNT(ct.trick_id) AS num_tricks
        FROM cats c
        JOIN cat_tricks ct ON c.cat_id = ct.cat_id
        GROUP BY c.name, c.breed
        ORDER BY num_tricks DESC
        LIMIT 15;
    """

    _df = run_and_show(con, _sql, title='Top 15 Cats by Trick Count')
    plot_horizontal_bar(_df, 'name', 'num_tricks',
                        title='Top 15 Cats by Number of Tricks',
                        xlabel='Number of Tricks')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q12: Most Popular Tricks
    Which tricks are learned by the most cats?
    """)
    return


@app.cell
def _(con, plot_bar, run_and_show):
    _sql = """
        SELECT
            t.trick,
            COUNT(ct.cat_id) AS num_cats
        FROM tricks t
        JOIN cat_tricks ct ON t.trick_id = ct.trick_id
        GROUP BY t.trick
        ORDER BY num_cats DESC;
    """

    _df = run_and_show(con, _sql, title='Trick Popularity')
    plot_bar(_df, 'trick', 'num_cats',
             title='Trick Popularity (Cats That Know Each Trick)',
             xlabel='Trick', ylabel='Number of Cats')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q13: Cats with No Tricks (LEFT JOIN + Images)
    Which cats haven't learned any tricks yet?
    """)
    return


@app.cell
def _(con, run_query, show_table_with_images):
    _sql = """
    SELECT c.image_url, c.name, c.breed, c.country, c.price
    FROM   cats       c
    LEFT JOIN cat_tricks ct ON c.cat_id = ct.cat_id
    WHERE  ct.trick_id IS NULL
    ORDER BY c.name;
    """

    _df = run_query(con, _sql)
    show_table_with_images(_df, image_col='image_url',
                           title='Cats with No Tricks (need training!)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q14: Trainability by Breed
    Average number of tricks per cat, grouped by breed.
    """)
    return


@app.cell
def _(con, plot_bar, run_and_show):
    _sql = """
        SELECT
            c.breed,
            COUNT(ct.trick_id) AS total_tricks,
            COUNT(DISTINCT c.cat_id) AS num_cats,
            ROUND(COUNT(ct.trick_id) * 1.0 / COUNT(DISTINCT c.cat_id), 1) AS avg_tricks_per_cat
        FROM cats c
        JOIN cat_tricks ct ON c.cat_id = ct.cat_id
        GROUP BY c.breed
        ORDER BY avg_tricks_per_cat DESC;
    """

    _df = run_and_show(con, _sql, title='Trainability by Breed')
    plot_bar(_df, 'breed', 'avg_tricks_per_cat',
             title='Average Tricks Per Cat by Breed',
             xlabel='Breed', ylabel='Avg Tricks/Cat')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Section 4: Common Table Expressions (CTEs)

    CTEs use `WITH ... AS (...)` to create temporary named result sets,
    making complex queries easier to read and maintain.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q15: Most Expensive Cat Per Breed (CTE + Images)
    Find the single most expensive cat in each breed — shown with avatars.
    """)
    return


@app.cell
def _(con, plot_bar, run_query, show_table_with_images):
    _sql = """
        WITH max_prices AS (
        SELECT
            breed,
            MAX(price) AS max_price
        FROM cats
        GROUP BY breed )
        SELECT
            c.image_url,
            c.name,
            c.breed,
            c.price
        FROM cats c
        JOIN max_prices mp ON c.breed = mp.breed
        AND c.price = mp.max_price
        ORDER BY c.price DESC;
    """

    _df = run_query(con, _sql)
    show_table_with_images(_df, image_col='image_url',
                           title='Most Expensive Cat Per Breed')

    # Also plot
    plot_bar(_df, 'breed', 'price',
             title='Highest Price Cat in Each Breed',
             xlabel='Breed', ylabel='Price ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q16: Cats Priced Above Their Breed Average (CTE)
    Find cats more expensive than the average for their breed.
    """)
    return


@app.cell
def _(con, run_and_show):
    _sql = """
        WITH breed_avg AS (
        SELECT
            breed,
            AVG(price) AS avg_price
        FROM cats
        GROUP BY breed )
        SELECT
            c.name,
            c.breed,
            c.price,
            ROUND(ba.avg_price, 0) AS breed_avg_price
        FROM cats c
        JOIN breed_avg ba ON c.breed = ba.breed
        WHERE c.price > ba.avg_price
        ORDER BY c.breed, c.price DESC;
    """

    run_and_show(con, _sql, title='Cats Priced Above Their Breed Average')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q17: Cats with 5+ Tricks (CTE + Gallery)
    The most talented cats shown as a visual gallery.
    """)
    return


@app.cell
def _(con, plot_horizontal_bar, run_query, show_gallery):
    _sql = """
        WITH trick_counts AS (
        SELECT
            cat_id,
            COUNT(*) AS num_tricks
        FROM cat_tricks
        GROUP BY cat_id )
        SELECT
            c.name,
            c.breed,
            tc.num_tricks,
            c.image_url
        FROM cats c
        JOIN trick_counts tc ON c.cat_id = tc.cat_id
        WHERE tc.num_tricks >= 5
        ORDER BY tc.num_tricks DESC;
    """

    _df = run_query(con, _sql)
    show_gallery(_df, name_col='name', image_col='image_url',
                 detail_cols=['breed', 'num_tricks'],
                 title='Talented Cats (5+ Tricks)', columns=5, img_size=100)

    # Also as a bar chart
    plot_horizontal_bar(_df, 'name', 'num_tricks',
                        title='Cats with 5+ Tricks',
                        xlabel='Number of Tricks')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q18: Most Popular Trick Per Country (CTE + Window)
    Which trick is most commonly learned in each country?
    """)
    return


@app.cell
def _(con, run_and_show):
    _sql = """
        WITH trick_by_country AS (
        SELECT
            c.country,
            t.trick,
            COUNT(*) AS cnt
        FROM cats c
        JOIN cat_tricks ct ON c.cat_id = ct.cat_id
        JOIN tricks t ON ct.trick_id = t.trick_id
        GROUP BY c.country, t.trick ), ranked AS (
        SELECT
            *,
            ROW_NUMBER() OVER ( PARTITION BY country
        ORDER BY cnt DESC ) AS rn
        FROM trick_by_country )
        SELECT
            country,
            trick,
            cnt AS times_learned
        FROM ranked
        WHERE rn = 1
        ORDER BY country;
    """

    run_and_show(con, _sql, title='Most Popular Trick Per Country')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q19: Youngest Cat Per Breed (CTE)
    Find the youngest (most recently born) cat in each breed.
    """)
    return


@app.cell
def _(con, run_query, show_table_with_images):
    _sql = """
        WITH youngest AS (
        SELECT
            breed,
            MAX(date_of_birth) AS latest_dob
        FROM cats
        GROUP BY breed )
        SELECT
            c.image_url,
            c.name,
            c.breed,
            c.date_of_birth,
            c.price
        FROM cats c
        JOIN youngest y ON c.breed = y.breed
        AND c.date_of_birth = y.latest_dob
        ORDER BY c.date_of_birth DESC;
    """

    _df = run_query(con, _sql)
    show_table_with_images(_df, image_col='image_url',
                           title='Youngest Cat Per Breed')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Section 5: Window & Ranking Functions

    Window functions compute across rows without collapsing them.
    Key functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE()`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q20: Rank Cats by Price Within Each Breed
    Assign a price rank within each breed (most expensive = rank 1).
    """)
    return


@app.cell
def _(con, run_and_show):
    _sql = """
        SELECT
            name,
            breed,
            price,
            RANK() OVER ( PARTITION BY breed
        ORDER BY price DESC ) AS price_rank
        FROM cats
        ORDER BY breed, price_rank
        LIMIT 30;
    """

    run_and_show(con, _sql, title='Price Rankings Within Each Breed (first 30)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q21: Top 3 Most Expensive Cats (ROW_NUMBER)
    Use ROW_NUMBER to get exactly the top 3 — with images.
    """)
    return


@app.cell
def _(con, run_query, show_table_with_images):
    _sql = """
        WITH ranked AS (
        SELECT
            name,
            breed,
            country,
            price,
            image_url,
            ROW_NUMBER() OVER (
        ORDER BY price DESC) AS rn
        FROM cats )
        SELECT
            image_url,
            name,
            breed,
            country,
            price,
            rn AS RANK
        FROM ranked
        WHERE rn <= 3;
    """

    _df = run_query(con, _sql)
    show_table_with_images(_df, image_col='image_url',
                           title='Top 3 Most Expensive Cats')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q22: Cheapest Cat Per Breed (RANK)
    Find the least expensive cat in each breed.
    """)
    return


@app.cell
def _(con, plot_bar, run_and_show):
    _sql = """
        WITH cheapest AS (
        SELECT
            name,
            breed,
            price,
            RANK() OVER ( PARTITION BY breed
        ORDER BY price ASC ) AS rnk
        FROM cats )
        SELECT
            name,
            breed,
            price
        FROM cheapest
        WHERE rnk = 1
        ORDER BY price;
    """

    _df = run_and_show(con, _sql, title='Cheapest Cat Per Breed')
    plot_bar(_df, 'breed', 'price',
             title='Cheapest Cat Price by Breed',
             xlabel='Breed', ylabel='Price ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q23: Rank Breeds by Average Price
    Rank breeds from most to least expensive.
    """)
    return


@app.cell
def _(con, plot_horizontal_bar, run_and_show):
    _sql = """
        WITH breed_price AS (
        SELECT
            breed,
            ROUND(AVG(price), 0) AS avg_price
        FROM cats
        GROUP BY breed )
        SELECT
            breed,
            avg_price,
            RANK() OVER (
        ORDER BY avg_price DESC) AS RANK
        FROM breed_price
        ORDER BY RANK;
    """

    _df = run_and_show(con, _sql, title='Breeds Ranked by Average Price')
    plot_horizontal_bar(_df, 'breed', 'avg_price',
                        title='Breeds Ranked by Average Price',
                        xlabel='Average Price ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q24: Top Tricksters by Rank (RANK + CTE)
    Who are the trickiest cats? Show top 5 with images.
    """)
    return


@app.cell
def _(con, run_query, show_table_with_images):
    _sql = """
        WITH trick_counts AS (
        SELECT
            c.cat_id,
            c.name,
            c.breed,
            c.image_url,
            COUNT(ct.trick_id) AS num_tricks
        FROM cats c
        JOIN cat_tricks ct ON c.cat_id = ct.cat_id
        GROUP BY c.cat_id, c.name, c.breed, c.image_url ), ranked AS (
        SELECT
            *,
            RANK() OVER (
        ORDER BY num_tricks DESC) AS rnk
        FROM trick_counts )
        SELECT
            image_url,
            name,
            breed,
            num_tricks,
            rnk AS RANK
        FROM ranked
        WHERE rnk <= 5;
    """

    _df = run_query(con, _sql)
    show_table_with_images(_df, image_col='image_url',
                           title='Top 5 Trickiest Cats')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q25: Most Expensive Male & Female Per Breed
    PARTITION BY breed, gender to find the top cat of each gender.
    """)
    return


@app.cell
def _(con, plot_grouped_bar, run_and_show):
    _sql = """
        WITH ranked AS (
        SELECT
            name,
            breed,
            gender,
            price,
            ROW_NUMBER() OVER ( PARTITION BY breed, gender
        ORDER BY price DESC ) AS rn
        FROM cats )
        SELECT
            name,
            breed,
            gender,
            price
        FROM ranked
        WHERE rn = 1
        ORDER BY breed, gender;
    """

    _df = run_and_show(con, _sql, title='Most Expensive Cat per Breed & Gender')
    plot_grouped_bar(_df, 'breed', 'gender', 'price',
                     title='Most Expensive Cat per Breed by Gender',
                     xlabel='Breed', ylabel='Price ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q26: Price Quartiles Using NTILE
    Divide all cats into 4 price quartiles.
    """)
    return


@app.cell
def _(con, run_and_show):
    _sql = """
        SELECT
            name,
            breed,
            price,
            NTILE(4) OVER (
        ORDER BY price) AS price_quartile
        FROM cats
        ORDER BY price_quartile, price DESC
        LIMIT 20;
    """

    run_and_show(con, _sql, title='Price Quartiles (sample of 20)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Section 6: Advanced Analytics & Insights
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q27: Gender Distribution by Breed
    Compare male vs female counts across breeds.
    """)
    return


@app.cell
def _(con, plot_grouped_bar, run_and_show):
    _sql = """
        SELECT
            breed,
            gender,
            COUNT(*) AS cnt
        FROM cats
        GROUP BY breed, gender
        ORDER BY breed, gender;
    """

    _df = run_and_show(con, _sql, title='Gender Distribution by Breed')
    plot_grouped_bar(_df, 'breed', 'gender', 'cnt',
                     title='Gender Distribution Across Breeds',
                     xlabel='Breed', ylabel='Count')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q28: Price vs Number of Tricks (Scatter)
    Is there a relationship between a cat's price and trick count?
    """)
    return


@app.cell
def _(con, plot_scatter, run_and_show):
    _sql = """
        SELECT
            c.name,
            c.price,
            COUNT(ct.trick_id) AS num_tricks
        FROM cats c
        JOIN cat_tricks ct ON c.cat_id = ct.cat_id
        GROUP BY c.cat_id, c.name, c.price
        ORDER BY c.price DESC;
    """

    _df = run_and_show(con, _sql, title='Price vs Tricks', max_rows=15)
    plot_scatter(_df, 'num_tricks', 'price',
                 title='Cat Price vs Number of Tricks Known',
                 xlabel='Number of Tricks', ylabel='Price ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q29: Cats Born Per Year (Trend Line)
    How has cat registration grown over time?
    """)
    return


@app.cell
def _(con, plot_line, run_and_show):
    _sql = """
        SELECT EXTRACT(YEAR
        FROM date_of_birth) AS birth_year, COUNT(*) AS num_cats
        FROM cats
        GROUP BY birth_year
        ORDER BY birth_year;
    """

    _df = run_and_show(con, _sql, title='Cats Born Per Year')
    plot_line(_df, 'birth_year', 'num_cats',
              title='Number of Cats Born Per Year',
              xlabel='Year', ylabel='Count')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q30: Running Total of Prices by Birth Date
    Cumulative price sum as a window function.
    """)
    return


@app.cell
def _(con, run_and_show):
    _sql = """
        SELECT
            name,
            date_of_birth,
            price,
            SUM(price) OVER (
        ORDER BY date_of_birth ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW ) AS running_total
        FROM cats
        ORDER BY date_of_birth
        LIMIT 20;
    """

    run_and_show(con, _sql, title='Running Total of Prices (first 20)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q31: Country Average vs Overall Average
    Compare each country's average price to the global average.
    """)
    return


@app.cell
def _(con, plot_bar, run_and_show):
    _sql = """
        WITH country_avg AS (
        SELECT
            country,
            ROUND(AVG(price), 0) AS country_avg_price
        FROM cats
        GROUP BY country ), overall AS (
        SELECT ROUND(AVG(price), 0) AS overall_avg
        FROM cats )
        SELECT
            ca.country,
            ca.country_avg_price,
            o.overall_avg,
            ca.country_avg_price - o.overall_avg AS diff_from_overall
        FROM country_avg ca
        CROSS
        JOIN overall o
        ORDER BY diff_from_overall DESC;
    """

    _df = run_and_show(con, _sql, title='Country Avg vs Overall Avg')
    plot_bar(_df, 'country', 'diff_from_overall',
             title='Country Avg Price vs Overall Average (Difference)',
             xlabel='Country', ylabel='Difference ($)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q32: Percentage of Cats Knowing Each Trick
    What fraction of all cats know each trick?
    """)
    return


@app.cell
def _(con, plot_horizontal_bar, run_and_show):
    _sql = """
        WITH total_cats AS (
        SELECT COUNT(DISTINCT cat_id) AS total
        FROM cat_tricks )
        SELECT
            t.trick,
            COUNT(ct.cat_id) AS cats_know_it,
            ROUND(COUNT(ct.cat_id) * 100.0 / tc.total, 1) AS pct_of_cats
        FROM tricks t
        JOIN cat_tricks ct ON t.trick_id = ct.trick_id
        CROSS
        JOIN total_cats tc
        GROUP BY t.trick, tc.total
        ORDER BY pct_of_cats DESC;
    """

    _df = run_and_show(con, _sql, title='Trick Penetration Rate')
    plot_horizontal_bar(_df, 'trick', 'pct_of_cats',
                        title='Percentage of Cats That Know Each Trick',
                        xlabel='% of Cats')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q33: Breed Diversity by Country
    How many distinct breeds are in each country?
    """)
    return


@app.cell
def _(con, plot_bar, run_and_show):
    _sql = """
        SELECT
            country,
            COUNT(DISTINCT breed) AS num_breeds
        FROM cats
        GROUP BY country
        ORDER BY num_breeds DESC;
    """

    _df = run_and_show(con, _sql, title='Breed Diversity by Country')
    plot_bar(_df, 'country', 'num_breeds',
             title='Number of Distinct Breeds Per Country',
             xlabel='Country', ylabel='Number of Breeds')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q34: Cat Profile Cards — The Premium Collection
    Display the top 8 most expensive cats as profile cards with full details.
    """)
    return


@app.cell
def _(con, run_query, show_gallery):
    _sql = """
        WITH trick_counts AS (
        SELECT
            cat_id,
            COUNT(*) AS num_tricks
        FROM cat_tricks
        GROUP BY cat_id )
        SELECT
            c.name,
            c.breed,
            c.country,
            c.color,
            c.price,
            COALESCE(tc.num_tricks, 0) AS num_tricks,
            c.image_url
        FROM cats c
        LEFT
        JOIN trick_counts tc ON c.cat_id = tc.cat_id
        ORDER BY c.price DESC
        LIMIT 8;
    """

    _df = run_query(con, _sql)
    show_gallery(_df, name_col='name', image_col='image_url',
                 detail_cols=['breed', 'country', 'color', 'price', 'num_tricks'],
                 title='Premium Cat Collection (Top 8 by Price)',
                 columns=4, img_size=130)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    In this notebook we explored:

    1. **Image Galleries** — rendering cat avatars in card grids and inline table thumbnails
    2. **Basic SELECT** — filtering, sorting, aggregation with bar/pie/histogram charts
    3. **JOINs** — INNER, LEFT, multi-table joins through junction tables
    4. **CTEs** — `WITH ... AS` for readable, reusable subqueries
    5. **Window Functions** — `ROW_NUMBER()`, `RANK()`, `NTILE()`, running totals
    6. **Advanced Analytics** — cross-comparisons, trends, scatter correlations

    All queries run on **DuckDB** with cat avatars from **RoboHash** (set=4).

    ---
    *End of notebook*
    """)
    return


if __name__ == "__main__":
    app.run()
