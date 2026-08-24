import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from world_plots import plot_bar, plot_grouped_bar, plot_pie, plot_scatter

    return plot_bar, plot_grouped_bar, plot_pie, plot_scatter


@app.cell
def _():
    import duckdb

    # This notebook queries the pre-built world.duckdb file.
    # It ships ready-to-use in this folder — no build step required.
    con = duckdb.connect("world.duckdb", read_only=True)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — The World Database

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### The Story Behind This Database

    In the early 2000s, MySQL AB needed one sample database that could
    teach every SQL idea at once — and they picked the most universal
    subject there is: **the entire planet**. The result, nicknamed
    simply *"world,"* has been used to teach SQL to millions of students
    for over 20 years. This notebook uses that same dataset, ported to
    **DuckDB**, so we can query it with nothing more than Python — no
    server, no setup, just data.

    ### What's Inside

    | Table | Rows | What it holds |
    |-------|------|----------------|
    | `country` | 239 | Every country: population, GNP, life expectancy, government form |
    | `city` | 4,079 | Every city with 1 population figure, linked to its country |
    | `countrylanguage` | 984 | Which languages are spoken where, and whether they're official |

    Together, these 3 tables describe **6+ billion people**, spread
    across **7 continents**, speaking **457 distinct languages** —
    and every one of those numbers is something *you* will compute
    yourself in the queries below.

    ### 20 Practice Queries

    | Level | Count | Focus |
    |-------|-------|-------|
    | Basic | 5 | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT` |
    | Intermediate | 10 | `JOIN`, `GROUP BY`, `HAVING`, subqueries, aggregation |
    | Advanced | 5 | Window functions, CTEs, correlation, multi-metric summaries |

    Plotting is handled by the decoupled `world_plots.py` module, shared
    with the equivalent Jupyter notebook (`world_queries.ipynb`) — same
    charts, same colors, either tool.

    ### How to Use

    Run each cell in order. Read the markdown — it explains the *why*
    behind every query. In Marimo, SQL cells run directly against
    DuckDB — no Python wrappers needed!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Setup — Confirm the Database Loaded
    """)
    return


@app.cell
def _(city, con, country, countrylanguage, mo):
    _df = mo.sql(
        f"""
        SELECT 'country'          AS table_name, COUNT(*) AS row_count FROM country
        UNION ALL SELECT 'city',            COUNT(*) FROM city
        UNION ALL SELECT 'countrylanguage', COUNT(*) FROM countrylanguage;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # BASIC QUERIES (1–5)

    Fundamentals: `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## B1 — List All Distinct Continents

    **What are we doing?**
    Retrieve the unique continents stored in the `country` table to
    understand the geographic coverage of the dataset.
    """)
    return


@app.cell
def _(con, country, mo):
    _df = mo.sql(
        f"""
        SELECT DISTINCT continent
        FROM   country
        ORDER  BY continent;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## B2 — Top 10 Most Populated Countries

    **What are we doing?**
    Find the 10 countries with the largest populations, ordered
    descending.
    """)
    return


@app.cell
def _(con, country, mo):
    df_top10_pop = mo.sql(
        f"""
        SELECT   name,
                 continent,
                 population
        FROM     country
        WHERE    population > 0
        ORDER BY population DESC
        LIMIT    10;
        """,
        engine=con
    )
    return (df_top10_pop,)


@app.cell
def _(df_top10_pop, plot_bar):
    plot_bar(df_top10_pop, x='Name', y='Population',
             title='Top 10 Most Populated Countries',
             xlabel='Country', ylabel='Population',
             fmt_y_millions=True, rotate_labels=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## B3 — Count the Number of Cities per Country (Top 15)

    **What are we doing?**
    Count how many cities each country has in the database and show
    the top 15.
    """)
    return


@app.cell
def _(city, con, country, mo):
    df_city_counts = mo.sql(
        f"""
        SELECT   co.name       AS country,
                 COUNT(ci.id)  AS city_count
        FROM     city ci
        JOIN     country co ON ci.countrycode = co.code
        GROUP BY co.name
        ORDER BY city_count DESC
        LIMIT    15;
        """,
        engine=con
    )
    return (df_city_counts,)


@app.cell
def _(df_city_counts, plot_bar):
    plot_bar(df_city_counts, x='country', y='city_count',
             title='Top 15 Countries by Number of Cities',
             xlabel='Country', ylabel='Number of Cities',
             color='#55A868', rotate_labels=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## B4 — Countries with Life Expectancy Above 78

    **What are we doing?**
    Filter countries whose life expectancy exceeds 78 years, sorted by
    life expectancy descending.
    """)
    return


@app.cell
def _(con, country, mo):
    df_life_exp_high = mo.sql(
        f"""
        SELECT   name,
                 continent,
                 lifeexpectancy
        FROM     country
        WHERE    lifeexpectancy > 78
        ORDER BY lifeexpectancy DESC;
        """,
        engine=con
    )
    return (df_life_exp_high,)


@app.cell
def _(df_life_exp_high, plot_bar):
    plot_bar(df_life_exp_high, x='Name', y='LifeExpectancy',
             title='Countries with Life Expectancy > 78',
             xlabel='Country', ylabel='Life Expectancy (years)',
             horizontal=True, figsize=(10, 8), color='#8172B2')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## B5 — Find the Most Populated City in the World

    **What are we doing?**
    Identify the single most populated city along with its country.
    """)
    return


@app.cell
def _(city, con, country, mo):
    _df = mo.sql(
        f"""
        SELECT   ci.name       AS city,
                 co.name       AS country,
                 ci.district,
                 ci.population
        FROM     city ci
        JOIN     country co ON ci.countrycode = co.code
        ORDER BY ci.population DESC
        LIMIT    1;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # INTERMEDIATE QUERIES (6–15)

    JOINs, `GROUP BY`, subqueries, aggregation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I1 — Top 10 Countries with Their Capital Cities

    **What are we doing?**
    Join `country` to `city` via the `capital` foreign key to show
    each country's capital and both populations.
    """)
    return


@app.cell
def _(city, con, country, mo):
    df_capitals = mo.sql(
        f"""
        SELECT   co.name              AS country,
                 ci.name              AS capital_city,
                 co.population        AS country_pop,
                 ci.population        AS capital_pop
        FROM     country co
        JOIN     city ci ON co.capital = ci.id
        WHERE    co.population > 0
        ORDER BY co.population DESC
        LIMIT    10;
        """,
        engine=con
    )
    return (df_capitals,)


@app.cell
def _(df_capitals, plot_grouped_bar):
    plot_grouped_bar(df_capitals, category='country',
                     values=['country_pop', 'capital_pop'],
                     labels=['Country Population', 'Capital Population'],
                     title='Top 10 Countries: Country vs Capital Population',
                     figsize=(12, 6))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I2 — Average Life Expectancy by Continent

    **What are we doing?**
    Compute the mean life expectancy for each continent, excluding
    NULLs.
    """)
    return


@app.cell
def _(con, country, mo):
    df_avg_life = mo.sql(
        f"""
        SELECT   continent,
                 ROUND(AVG(lifeexpectancy), 1) AS avg_life_exp,
                 COUNT(*)                      AS num_countries
        FROM     country
        WHERE    lifeexpectancy IS NOT NULL
        GROUP BY continent
        ORDER BY avg_life_exp DESC;
        """,
        engine=con
    )
    return (df_avg_life,)


@app.cell
def _(df_avg_life, plot_bar):
    plot_bar(df_avg_life, x='Continent', y='avg_life_exp',
             title='Average Life Expectancy by Continent',
             xlabel='Continent', ylabel='Avg Life Expectancy (years)',
             color='#C44E52', rotate_labels=30)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I3 — GNP per Capita: Top 15 Countries

    **What are we doing?**
    Calculate GNP per capita (GNP / population) and rank the richest
    countries.
    """)
    return


@app.cell
def _(con, country, mo):
    df_gnp_capita = mo.sql(
        f"""
        SELECT   name,
                 continent,
                 gnp,
                 population,
                 ROUND(gnp * 1000000.0 / population, 2) AS gnp_per_capita
        FROM     country
        WHERE    population > 0
          AND    gnp > 0
        ORDER BY gnp_per_capita DESC
        LIMIT    15;
        """,
        engine=con
    )
    return (df_gnp_capita,)


@app.cell
def _(df_gnp_capita, plot_bar):
    plot_bar(df_gnp_capita, x='Name', y='gnp_per_capita',
             title='Top 15 Countries by GNP per Capita',
             xlabel='Country', ylabel='GNP per Capita ($)',
             horizontal=True, figsize=(10, 7), color='#E5AE38')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I4 — Languages Spoken in 10+ Countries

    **What are we doing?**
    Find languages that appear in 10 or more countries in the
    `countrylanguage` table.
    """)
    return


@app.cell
def _(con, countrylanguage, mo):
    df_lang_10plus = mo.sql(
        f"""
        SELECT   language,
                 COUNT(DISTINCT countrycode) AS num_countries
        FROM     countrylanguage
        GROUP BY language
        HAVING   COUNT(DISTINCT countrycode) >= 10
        ORDER BY num_countries DESC;
        """,
        engine=con
    )
    return (df_lang_10plus,)


@app.cell
def _(df_lang_10plus, plot_bar):
    plot_bar(df_lang_10plus, x='Language', y='num_countries',
             title='Languages Spoken in 10+ Countries',
             xlabel='Language', ylabel='Number of Countries',
             color='#64B5CD', rotate_labels=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I5 — Population Distribution by Continent

    **What are we doing?**
    Aggregate total population per continent and show as a pie chart.
    """)
    return


@app.cell
def _(con, country, mo):
    df_pop_continent = mo.sql(
        f"""
        SELECT   continent,
                 SUM(population) AS total_pop
        FROM     country
        GROUP BY continent
        ORDER BY total_pop DESC;
        """,
        engine=con
    )
    return (df_pop_continent,)


@app.cell
def _(df_pop_continent, plot_pie):
    plot_pie(df_pop_continent, labels_col='Continent', values_col='total_pop',
             title='World Population Distribution by Continent')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I6 — Population Density: Top 20 Countries

    **What are we doing?**
    Compute population density (people per km²) and rank the most
    densely populated countries.
    """)
    return


@app.cell
def _(con, country, mo):
    df_density = mo.sql(
        f"""
        SELECT   name,
                 continent,
                 population,
                 surfacearea,
                 ROUND(population / surfacearea, 1) AS density
        FROM     country
        WHERE    surfacearea > 0
          AND    population  > 0
        ORDER BY density DESC
        LIMIT    20;
        """,
        engine=con
    )
    return (df_density,)


@app.cell
def _(df_density, plot_bar):
    plot_bar(df_density, x='Name', y='density',
             title='Top 20 Countries by Population Density',
             xlabel='Country', ylabel='People / km²',
             horizontal=True, figsize=(10, 8), color='#6D904F')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I7 — Dependent Territories (No Independence Year)

    **What are we doing?**
    List territories that have no independence year (i.e. they are
    still dependencies or overseas territories).
    """)
    return


@app.cell
def _(con, country, mo):
    _df = mo.sql(
        f"""
        SELECT   name,
                 continent,
                 region,
                 governmentform,
                 population
        FROM     country
        WHERE    indepyear IS NULL
        ORDER BY population DESC;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I8 — Number of Official Languages per Country (Top 10)

    **What are we doing?**
    Count official languages per country and show which countries have
    the most.
    """)
    return


@app.cell
def _(con, country, countrylanguage, mo):
    df_official_langs = mo.sql(
        f"""
        SELECT   co.name                             AS country,
                 COUNT(cl.language)                   AS official_lang_count,
                 STRING_AGG(cl.language, ', '
                            ORDER BY cl.percentage DESC) AS languages
        FROM     countrylanguage cl
        JOIN     country co ON cl.countrycode = co.code
        WHERE    cl.isofficial = true
        GROUP BY co.name
        ORDER BY official_lang_count DESC
        LIMIT    10;
        """,
        engine=con
    )
    return (df_official_langs,)


@app.cell
def _(df_official_langs, plot_bar):
    plot_bar(df_official_langs, x='country', y='official_lang_count',
             title='Top 10 Countries by Number of Official Languages',
             xlabel='Country', ylabel='Official Languages',
             color='#D65F5F', rotate_labels=45)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I9 — Largest City in Each Continent

    **What are we doing?**
    Use a subquery to find the single most populated city on every
    continent.
    """)
    return


@app.cell
def _(city, con, country, mo):
    df_largest_city_continent = mo.sql(
        f"""
        SELECT   co.continent,
                 ci.name        AS city,
                 co.name        AS country,
                 ci.population
        FROM     city ci
        JOIN     country co ON ci.countrycode = co.code
        WHERE    ci.population = (
                     SELECT MAX(ci2.population)
                     FROM   city ci2
                     JOIN   country co2 ON ci2.countrycode = co2.code
                     WHERE  co2.continent = co.continent
                 )
        ORDER BY ci.population DESC;
        """,
        engine=con
    )
    return (df_largest_city_continent,)


@app.cell
def _(df_largest_city_continent, plot_bar):
    plot_bar(df_largest_city_continent, x='city', y='Population',
             title='Largest City on Each Continent',
             xlabel='City', ylabel='Population',
             fmt_y_millions=True, rotate_labels=30)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I10 — GNP Growth: Countries Where GNP Increased

    **What are we doing?**
    Compare current GNP vs. old GNP (`gnpold`) and find countries with
    the largest absolute growth.
    """)
    return


@app.cell
def _(con, country, mo):
    df_gnp_growth = mo.sql(
        f"""
        SELECT   name,
                 continent,
                 gnp,
                 gnpold,
                 ROUND(gnp - gnpold, 2)                       AS gnp_growth,
                 ROUND((gnp - gnpold) / gnpold * 100, 1)      AS growth_pct
        FROM     country
        WHERE    gnp IS NOT NULL
          AND    gnpold IS NOT NULL
          AND    gnpold > 0
        ORDER BY gnp_growth DESC
        LIMIT    15;
        """,
        engine=con
    )
    return (df_gnp_growth,)


@app.cell
def _(df_gnp_growth, plot_bar):
    plot_bar(df_gnp_growth, x='Name', y='gnp_growth',
             title='Top 15 Countries by GNP Growth (Absolute)',
             xlabel='Country', ylabel='GNP Growth (millions $)',
             horizontal=True, figsize=(10, 7), color='#55A868')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # ADVANCED QUERIES (16–20)

    Window functions, CTEs, correlation, multi-metric summaries.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A1 — Rank Countries Within Each Continent by Population (Window Function)

    **What are we doing?**
    Use `RANK() OVER (PARTITION BY continent)` to rank each country
    within its continent by population, then show the top 3 per
    continent.
    """)
    return


@app.cell
def _(con, country, mo):
    df_ranked = mo.sql(
        f"""
        WITH ranked AS (
            SELECT  name,
                    continent,
                    population,
                    RANK() OVER (
                        PARTITION BY continent
                        ORDER BY     population DESC
                    ) AS pop_rank
            FROM    country
            WHERE   population > 0
        )
        SELECT  continent,
                name,
                population,
                pop_rank
        FROM    ranked
        WHERE   pop_rank <= 3
        ORDER BY continent, pop_rank;
        """,
        engine=con
    )
    return (df_ranked,)


@app.cell
def _(df_ranked, mo):
    # Pivot for a grouped view: 1 row per continent, 1 column per rank
    _pivot = df_ranked.pivot_table(index='Continent', columns='pop_rank',
                                    values='Name', aggfunc='first')
    _pivot.columns = [f'Rank {int(c)}' for c in _pivot.columns]
    mo.plain(_pivot)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A2 — Countries Where Capital Is NOT the Most Populated City

    **What are we doing?**
    Use a CTE to find each country's largest city, then compare it
    with the capital. Show cases where they differ.
    """)
    return


@app.cell
def _(city, con, country, mo):
    df_capital_vs_biggest = mo.sql(
        f"""
        WITH biggest_city AS (
            SELECT   countrycode,
                     name       AS biggest_city_name,
                     population AS biggest_city_pop
            FROM     city
            WHERE    (countrycode, population) IN (
                         SELECT   countrycode, MAX(population)
                         FROM     city
                         GROUP BY countrycode
                     )
        )
        SELECT   co.name           AS country,
                 cap.name          AS capital,
                 cap.population    AS capital_pop,
                 bc.biggest_city_name,
                 bc.biggest_city_pop
        FROM     country co
        JOIN     city cap            ON co.capital = cap.id
        JOIN     biggest_city bc     ON co.code    = bc.countrycode
        WHERE    cap.name != bc.biggest_city_name
        ORDER BY bc.biggest_city_pop DESC
        LIMIT    15;
        """,
        engine=con
    )
    return (df_capital_vs_biggest,)


@app.cell
def _(df_capital_vs_biggest, plot_grouped_bar):
    plot_grouped_bar(df_capital_vs_biggest, category='country',
                     values=['capital_pop', 'biggest_city_pop'],
                     labels=['Capital Population', 'Biggest City Population'],
                     title='Capital vs Biggest City (Where They Differ)',
                     figsize=(14, 6))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A3 — Language Diversity Index per Country

    **What are we doing?**
    Compute a *Herfindahl-style* language diversity index:
    `1 - SUM(percentage² / 10000)`. A score near 1 means highly
    diverse; near 0 means one dominant language.
    """)
    return


@app.cell
def _(con, country, countrylanguage, mo):
    df_diversity = mo.sql(
        f"""
        WITH diversity AS (
            SELECT   cl.countrycode,
                     co.name,
                     co.continent,
                     COUNT(cl.language)                                   AS num_languages,
                     ROUND(1.0 - SUM(cl.percentage * cl.percentage) / 10000, 4)
                                                                          AS diversity_index
            FROM     countrylanguage cl
            JOIN     country co ON cl.countrycode = co.code
            GROUP BY cl.countrycode, co.name, co.continent
        )
        SELECT   name,
                 continent,
                 num_languages,
                 diversity_index
        FROM     diversity
        ORDER BY diversity_index DESC
        LIMIT    20;
        """,
        engine=con
    )
    return (df_diversity,)


@app.cell
def _(df_diversity, plot_bar):
    plot_bar(df_diversity, x='Name', y='diversity_index',
             title='Top 20 Countries by Language Diversity Index',
             xlabel='Country', ylabel='Diversity Index (0–1)',
             horizontal=True, figsize=(10, 8), color='#8172B2')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A4 — GNP per Capita vs Life Expectancy (Scatter with Continent Hue)

    **What are we doing?**
    Explore the relationship between wealth (GNP per capita) and
    health (life expectancy) across all countries, colored by
    continent.
    """)
    return


@app.cell
def _(con, country, mo):
    df_scatter = mo.sql(
        f"""
        SELECT   name,
                 continent,
                 lifeexpectancy,
                 population,
                 gnp,
                 ROUND(gnp * 1000000.0 / population, 2) AS gnp_per_capita
        FROM     country
        WHERE    population > 0
          AND    gnp > 0
          AND    lifeexpectancy IS NOT NULL;
        """,
        engine=con
    )
    return (df_scatter,)


@app.cell
def _(df_scatter, plot_scatter):
    plot_scatter(df_scatter, x='gnp_per_capita', y='LifeExpectancy',
                 hue='Continent',
                 title='GNP per Capita vs Life Expectancy',
                 xlabel='GNP per Capita ($)',
                 ylabel='Life Expectancy (years)',
                 annotate_col='name', annotate_top_n=5,
                 figsize=(12, 7))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A5 — Continent-Level Summary with Multiple Aggregations & Percentiles

    **What are we doing?**
    Build a comprehensive continent dashboard using multiple aggregate
    functions, including median population and the 90th-percentile
    GNP — all in a single query with window functions.
    """)
    return


@app.cell
def _(con, country, mo):
    df_continent_summary = mo.sql(
        f"""
        SELECT   continent,
                 COUNT(*)                                          AS num_countries,
                 SUM(population)                                   AS total_pop,
                 ROUND(AVG(population), 0)                         AS avg_pop,
                 MEDIAN(population)                                AS median_pop,
                 ROUND(SUM(CAST(gnp AS DOUBLE)), 0)                AS total_gnp,
                 ROUND(AVG(lifeexpectancy), 1)                     AS avg_life_exp,
                 ROUND(MIN(lifeexpectancy), 1)                     AS min_life_exp,
                 ROUND(MAX(lifeexpectancy), 1)                     AS max_life_exp,
                 ROUND(PERCENTILE_CONT(0.9)
                       WITHIN GROUP (ORDER BY CAST(gnp AS DOUBLE)), 0)
                                                                   AS p90_gnp
        FROM     country
        WHERE    population > 0
        GROUP BY continent
        ORDER BY total_pop DESC;
        """,
        engine=con
    )
    return (df_continent_summary,)


@app.cell
def _(df_continent_summary):
    # Life expectancy range (min-max) per continent, with the average marked
    import matplotlib.pyplot as plt

    _life_df = df_continent_summary[['Continent', 'min_life_exp', 'max_life_exp', 'avg_life_exp']].copy()
    _fig, _ax = plt.subplots(figsize=(10, 5))
    _ax.barh(_life_df['Continent'], _life_df['max_life_exp'] - _life_df['min_life_exp'],
             left=_life_df['min_life_exp'], color='#CCB974', alpha=0.7, label='Range')
    _ax.scatter(_life_df['avg_life_exp'], _life_df['Continent'],
                color='#C44E52', s=80, zorder=5, label='Average')
    _ax.set_xlabel('Life Expectancy (years)')
    _ax.set_title('Life Expectancy Range & Average by Continent', fontweight='bold', pad=12)
    _ax.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Summary

    In this notebook we practiced:

    - **Basic:** `SELECT`, `DISTINCT`, `WHERE`, `ORDER BY`, `LIMIT`
    - **Intermediate:** `JOIN`, `GROUP BY`, `HAVING`, subqueries,
      `STRING_AGG`, correlated subqueries
    - **Advanced:** CTEs (`WITH`), `RANK() OVER (PARTITION BY ...)`,
      `MEDIAN`, `PERCENTILE_CONT`, tuple-subquery joins

    Same 3 tables, same 20 questions, same charts as
    `world_queries.ipynb` — just written the Marimo way: reactive SQL
    cells instead of a `run()` helper function.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
