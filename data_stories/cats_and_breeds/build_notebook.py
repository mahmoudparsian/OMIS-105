import json

def make_cell(cell_type, source, metadata=None):
    cell = {
        "cell_type": cell_type,
        "metadata": metadata or {},
        "source": source if isinstance(source, list) else [source]
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell

cells = []

# ═══════════════════════════════════════════════════════════════════
# Title and Introduction
# ═══════════════════════════════════════════════════════════════════
cells.append(make_cell("markdown", [
    "# 🐱 Cats, Breeds & Tricks — Data Story with DuckDB\n",
    "\n",
    "**Course:** OMIS 105 — Data Analytics with SQL  \n",
    "**Topic:** Exploring a Cat Show database using DuckDB, CTEs, Window Functions, and Visualizations  \n",
    "\n",
    "---\n",
    "\n",
    "## Database Schema\n",
    "\n",
    "| Table | Description |\n",
    "|-------|-------------|\n",
    "| `breeds` | Cat breed names and descriptions (15 breeds) |\n",
    "| `cats` | Individual cats with attributes: name, DOB, color, country, gender, breed, price (80 cats) |\n",
    "| `tricks` | Available tricks a cat can learn (15 tricks) |\n",
    "| `cat_tricks` | Many-to-many relationship: which cat knows which trick |\n",
    "\n",
    "### Relationships\n",
    "```\n",
    "breeds (1) ──── (M) cats (1) ──── (M) cat_tricks (M) ──── (1) tricks\n",
    "```"
]))

# ═══════════════════════════════════════════════════════════════════
# Setup Cell
# ═══════════════════════════════════════════════════════════════════
cells.append(make_cell("markdown", [
    "## Setup: Import Libraries and Load Data\n",
    "\n",
    "We load our CSV files into DuckDB tables. All display and plotting functions\n",
    "are defined in external modules (`display_utils.py` and `plot_utils.py`)\n",
    "to keep this notebook clean and focused on SQL."
]))

cells.append(make_cell("code", [
    "import duckdb\n",
    "import pandas as pd\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "# Import our utility modules (external to keep notebook clean)\n",
    "from display_utils import run_query, show_table, run_and_show\n",
    "from plot_utils import (plot_bar, plot_horizontal_bar, plot_pie,\n",
    "                         plot_line, plot_scatter, plot_grouped_bar,\n",
    "                         plot_histogram, plot_stacked_bar)\n",
    "\n",
    "# Create an in-memory DuckDB connection\n",
    "con = duckdb.connect(database=':memory:')\n",
    "\n",
    "print('Libraries loaded successfully!')"
]))

# ═══════════════════════════════════════════════════════════════════
# Create Tables from CSV
# ═══════════════════════════════════════════════════════════════════
cells.append(make_cell("markdown", [
    "## Create DuckDB Tables from CSV Files\n",
    "\n",
    "DuckDB can read CSV files directly into tables using `CREATE TABLE ... AS SELECT * FROM read_csv_auto(...)`."
]))

cells.append(make_cell("code", [
    "# ── Create tables by reading CSV files ──\n",
    "\n",
    "con.execute(\"\"\"\n",
    "    CREATE TABLE breeds AS\n",
    "    SELECT * FROM read_csv_auto('data/breeds.csv');\n",
    "\"\"\")\n",
    "\n",
    "con.execute(\"\"\"\n",
    "    CREATE TABLE tricks AS\n",
    "    SELECT * FROM read_csv_auto('data/tricks.csv');\n",
    "\"\"\")\n",
    "\n",
    "con.execute(\"\"\"\n",
    "    CREATE TABLE cats AS\n",
    "    SELECT * FROM read_csv_auto('data/cats.csv');\n",
    "\"\"\")\n",
    "\n",
    "con.execute(\"\"\"\n",
    "    CREATE TABLE cat_tricks AS\n",
    "    SELECT * FROM read_csv_auto('data/cat_tricks.csv');\n",
    "\"\"\")\n",
    "\n",
    "print('All 4 tables created successfully from CSV files!')\n",
    "print()\n",
    "\n",
    "# Quick row counts\n",
    "for table in ['breeds', 'tricks', 'cats', 'cat_tricks']:\n",
    "    count = con.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]\n",
    "    print(f'  {table:12s} → {count:>4d} rows')"
]))

# ═══════════════════════════════════════════════════════════════════
# SECTION 1: Basic Queries
# ═══════════════════════════════════════════════════════════════════
cells.append(make_cell("markdown", [
    "---\n",
    "## Section 1: Basic SELECT Queries"
]))

# Q1
cells.append(make_cell("markdown", [
    "### Q1: List All Breeds\n",
    "Retrieve all breed names and their descriptions."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT breed, description\n",
    "FROM   breeds\n",
    "ORDER BY breed;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='All Cat Breeds')"
]))

# Q2
cells.append(make_cell("markdown", [
    "### Q2: List All Available Tricks\n",
    "Show every trick a cat can learn."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT trick_id, trick\n",
    "FROM   tricks\n",
    "ORDER BY trick_id;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='All Tricks')"
]))

# Q3
cells.append(make_cell("markdown", [
    "### Q3: Cats from the USA\n",
    "Filter cats whose country is USA."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT name, color, gender, breed, price\n",
    "FROM   cats\n",
    "WHERE  country = 'USA'\n",
    "ORDER BY name;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Cats from the USA')"
]))

# Q4
cells.append(make_cell("markdown", [
    "### Q4: Count of Cats by Country\n",
    "How many cats are registered in each country?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT   country,\n",
    "         COUNT(*) AS num_cats\n",
    "FROM     cats\n",
    "GROUP BY country\n",
    "ORDER BY num_cats DESC;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Cats per Country')\n",
    "plot_bar(df, 'country', 'num_cats',\n",
    "         title='Number of Cats by Country',\n",
    "         xlabel='Country', ylabel='Count')"
]))

# Q5
cells.append(make_cell("markdown", [
    "### Q5: Distinct Coat Colors\n",
    "What are all the different coat colors in our data?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT   color,\n",
    "         COUNT(*) AS num_cats\n",
    "FROM     cats\n",
    "GROUP BY color\n",
    "ORDER BY num_cats DESC;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Cats by Color')\n",
    "plot_pie(df, 'color', 'num_cats',\n",
    "         title='Distribution of Coat Colors')"
]))

# Q6
cells.append(make_cell("markdown", [
    "### Q6: Top 10 Most Expensive Cats\n",
    "Which cats command the highest prices?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT name, breed, country, price\n",
    "FROM   cats\n",
    "ORDER BY price DESC\n",
    "LIMIT 10;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Top 10 Most Expensive Cats')\n",
    "plot_horizontal_bar(df, 'name', 'price',\n",
    "                    title='Top 10 Most Expensive Cats',\n",
    "                    xlabel='Price ($)')"
]))

# Q7
cells.append(make_cell("markdown", [
    "### Q7: Average Price by Breed\n",
    "Which breeds are the most valuable on average?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT   breed,\n",
    "         ROUND(AVG(price), 0) AS avg_price,\n",
    "         COUNT(*)             AS num_cats\n",
    "FROM     cats\n",
    "GROUP BY breed\n",
    "ORDER BY avg_price DESC;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Average Price by Breed')\n",
    "plot_bar(df, 'breed', 'avg_price',\n",
    "         title='Average Cat Price by Breed',\n",
    "         xlabel='Breed', ylabel='Avg Price ($)')"
]))

# Q8
cells.append(make_cell("markdown", [
    "### Q8: Price Distribution\n",
    "How are cat prices distributed?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT price FROM cats ORDER BY price;\n",
    "\"\"\"\n",
    "\n",
    "df = run_query(con, sql)\n",
    "plot_histogram(df, 'price',\n",
    "              title='Distribution of Cat Prices',\n",
    "              xlabel='Price ($)', bins=12)"
]))

# ═══════════════════════════════════════════════════════════════════
# SECTION 2: Joins
# ═══════════════════════════════════════════════════════════════════
cells.append(make_cell("markdown", [
    "---\n",
    "## Section 2: JOIN Queries"
]))

# Q9
cells.append(make_cell("markdown", [
    "### Q9: Cats with Their Breed Descriptions (INNER JOIN)\n",
    "Join cats with breeds to see each cat's breed description."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT c.name,\n",
    "       c.breed,\n",
    "       b.description,\n",
    "       c.price\n",
    "FROM   cats   c\n",
    "JOIN   breeds b ON c.breed = b.breed\n",
    "ORDER BY c.name\n",
    "LIMIT 15;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Cats with Breed Descriptions (first 15)')"
]))

# Q10
cells.append(make_cell("markdown", [
    "### Q10: Cats and Their Tricks (Multi-Table JOIN)\n",
    "Join through the junction table to see which cat knows which trick."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT c.name    AS cat_name,\n",
    "       c.breed,\n",
    "       t.trick\n",
    "FROM   cats       c\n",
    "JOIN   cat_tricks ct ON c.cat_id  = ct.cat_id\n",
    "JOIN   tricks     t  ON ct.trick_id = t.trick_id\n",
    "ORDER BY c.name, t.trick\n",
    "LIMIT 20;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Cats and Their Tricks (first 20 rows)')"
]))

# Q11
cells.append(make_cell("markdown", [
    "### Q11: Number of Tricks Per Cat\n",
    "How many tricks does each cat know? (GROUP BY with JOIN)"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT   c.name,\n",
    "         c.breed,\n",
    "         COUNT(ct.trick_id) AS num_tricks\n",
    "FROM     cats       c\n",
    "JOIN     cat_tricks ct ON c.cat_id = ct.cat_id\n",
    "GROUP BY c.name, c.breed\n",
    "ORDER BY num_tricks DESC\n",
    "LIMIT 15;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Top 15 Cats by Trick Count')\n",
    "plot_horizontal_bar(df, 'name', 'num_tricks',\n",
    "                    title='Top 15 Cats by Number of Tricks',\n",
    "                    xlabel='Number of Tricks')"
]))

# Q12
cells.append(make_cell("markdown", [
    "### Q12: Most Popular Tricks\n",
    "Which tricks are learned by the most cats?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT   t.trick,\n",
    "         COUNT(ct.cat_id) AS num_cats\n",
    "FROM     tricks     t\n",
    "JOIN     cat_tricks ct ON t.trick_id = ct.trick_id\n",
    "GROUP BY t.trick\n",
    "ORDER BY num_cats DESC;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Trick Popularity')\n",
    "plot_bar(df, 'trick', 'num_cats',\n",
    "         title='Trick Popularity (Number of Cats That Know Each Trick)',\n",
    "         xlabel='Trick', ylabel='Number of Cats')"
]))

# Q13
cells.append(make_cell("markdown", [
    "### Q13: Cats with No Tricks (LEFT JOIN)\n",
    "Which cats haven't learned any tricks?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT c.name, c.breed, c.country\n",
    "FROM   cats       c\n",
    "LEFT JOIN cat_tricks ct ON c.cat_id = ct.cat_id\n",
    "WHERE  ct.trick_id IS NULL\n",
    "ORDER BY c.name;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Cats with No Tricks')"
]))

# Q14
cells.append(make_cell("markdown", [
    "### Q14: Trick Count by Breed\n",
    "Which breeds are the most trainable overall?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT   c.breed,\n",
    "         COUNT(ct.trick_id) AS total_tricks,\n",
    "         COUNT(DISTINCT c.cat_id) AS num_cats,\n",
    "         ROUND(COUNT(ct.trick_id) * 1.0 / COUNT(DISTINCT c.cat_id), 1)\n",
    "             AS avg_tricks_per_cat\n",
    "FROM     cats       c\n",
    "JOIN     cat_tricks ct ON c.cat_id = ct.cat_id\n",
    "GROUP BY c.breed\n",
    "ORDER BY avg_tricks_per_cat DESC;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Trainability by Breed')\n",
    "plot_bar(df, 'breed', 'avg_tricks_per_cat',\n",
    "         title='Average Tricks Per Cat by Breed',\n",
    "         xlabel='Breed', ylabel='Avg Tricks/Cat')"
]))

# ═══════════════════════════════════════════════════════════════════
# SECTION 3: CTEs
# ═══════════════════════════════════════════════════════════════════
cells.append(make_cell("markdown", [
    "---\n",
    "## Section 3: Common Table Expressions (CTEs)\n",
    "\n",
    "CTEs use `WITH ... AS (...)` to create temporary named result sets that make\n",
    "complex queries easier to read and maintain."
]))

# Q15
cells.append(make_cell("markdown", [
    "### Q15: Most Expensive Cat Per Breed (CTE)\n",
    "Find the single most expensive cat within each breed."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH max_prices AS (\n",
    "    SELECT breed,\n",
    "           MAX(price) AS max_price\n",
    "    FROM   cats\n",
    "    GROUP BY breed\n",
    ")\n",
    "SELECT c.name,\n",
    "       c.breed,\n",
    "       c.price\n",
    "FROM   cats c\n",
    "JOIN   max_prices mp\n",
    "       ON c.breed = mp.breed\n",
    "      AND c.price = mp.max_price\n",
    "ORDER BY c.price DESC;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Most Expensive Cat Per Breed')\n",
    "plot_bar(df, 'breed', 'price',\n",
    "         title='Most Expensive Cat in Each Breed',\n",
    "         xlabel='Breed', ylabel='Price ($)')"
]))

# Q16
cells.append(make_cell("markdown", [
    "### Q16: Cats Priced Above Their Breed Average (CTE)\n",
    "Find cats that are more expensive than the average for their breed."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH breed_avg AS (\n",
    "    SELECT breed,\n",
    "           AVG(price) AS avg_price\n",
    "    FROM   cats\n",
    "    GROUP BY breed\n",
    ")\n",
    "SELECT c.name,\n",
    "       c.breed,\n",
    "       c.price,\n",
    "       ROUND(ba.avg_price, 0) AS breed_avg_price\n",
    "FROM   cats c\n",
    "JOIN   breed_avg ba ON c.breed = ba.breed\n",
    "WHERE  c.price > ba.avg_price\n",
    "ORDER BY c.breed, c.price DESC;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Cats Priced Above Their Breed Average')"
]))

# Q17
cells.append(make_cell("markdown", [
    "### Q17: Cats with 5 or More Tricks (CTE)\n",
    "Find the most talented cats (those who know at least 5 tricks)."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH trick_counts AS (\n",
    "    SELECT cat_id,\n",
    "           COUNT(*) AS num_tricks\n",
    "    FROM   cat_tricks\n",
    "    GROUP BY cat_id\n",
    ")\n",
    "SELECT c.name,\n",
    "       c.breed,\n",
    "       tc.num_tricks\n",
    "FROM   cats c\n",
    "JOIN   trick_counts tc ON c.cat_id = tc.cat_id\n",
    "WHERE  tc.num_tricks >= 5\n",
    "ORDER BY tc.num_tricks DESC;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Cats with 5+ Tricks')\n",
    "plot_horizontal_bar(df, 'name', 'num_tricks',\n",
    "                    title='Talented Cats (5+ Tricks)',\n",
    "                    xlabel='Number of Tricks')"
]))

# Q18
cells.append(make_cell("markdown", [
    "### Q18: Youngest Cat Per Breed (CTE)\n",
    "Find the youngest (most recently born) cat in each breed."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH youngest AS (\n",
    "    SELECT breed,\n",
    "           MAX(date_of_birth) AS latest_dob\n",
    "    FROM   cats\n",
    "    GROUP BY breed\n",
    ")\n",
    "SELECT c.name,\n",
    "       c.breed,\n",
    "       c.date_of_birth,\n",
    "       c.price\n",
    "FROM   cats c\n",
    "JOIN   youngest y\n",
    "       ON c.breed = y.breed\n",
    "      AND c.date_of_birth = y.latest_dob\n",
    "ORDER BY c.date_of_birth DESC;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Youngest Cat Per Breed')"
]))

# Q19
cells.append(make_cell("markdown", [
    "### Q19: Most Popular Trick Per Country (CTE)\n",
    "Which trick is most commonly learned in each country?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH trick_by_country AS (\n",
    "    SELECT c.country,\n",
    "           t.trick,\n",
    "           COUNT(*) AS cnt\n",
    "    FROM   cats       c\n",
    "    JOIN   cat_tricks ct ON c.cat_id    = ct.cat_id\n",
    "    JOIN   tricks     t  ON ct.trick_id = t.trick_id\n",
    "    GROUP BY c.country, t.trick\n",
    "),\n",
    "ranked AS (\n",
    "    SELECT *,\n",
    "           ROW_NUMBER() OVER (\n",
    "               PARTITION BY country\n",
    "               ORDER BY cnt DESC\n",
    "           ) AS rn\n",
    "    FROM trick_by_country\n",
    ")\n",
    "SELECT country, trick, cnt AS times_learned\n",
    "FROM   ranked\n",
    "WHERE  rn = 1\n",
    "ORDER BY country;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Most Popular Trick Per Country')"
]))

# ═══════════════════════════════════════════════════════════════════
# SECTION 4: Window / Ranking Functions
# ═══════════════════════════════════════════════════════════════════
cells.append(make_cell("markdown", [
    "---\n",
    "## Section 4: Window & Ranking Functions\n",
    "\n",
    "Window functions perform calculations across rows related to the current row\n",
    "without collapsing them (unlike GROUP BY). Key functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE()`."
]))

# Q20
cells.append(make_cell("markdown", [
    "### Q20: Rank Cats by Price Within Each Breed\n",
    "Assign a rank to each cat within its breed based on price (most expensive = rank 1)."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT name,\n",
    "       breed,\n",
    "       price,\n",
    "       RANK() OVER (\n",
    "           PARTITION BY breed\n",
    "           ORDER BY price DESC\n",
    "       ) AS price_rank\n",
    "FROM   cats\n",
    "ORDER BY breed, price_rank\n",
    "LIMIT 30;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Price Rankings Within Each Breed (Top 30 Rows)')"
]))

# Q21
cells.append(make_cell("markdown", [
    "### Q21: Top 3 Most Expensive Cats Overall (ROW_NUMBER)\n",
    "Use ROW_NUMBER to get exactly the top 3."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH ranked AS (\n",
    "    SELECT name,\n",
    "           breed,\n",
    "           country,\n",
    "           price,\n",
    "           ROW_NUMBER() OVER (ORDER BY price DESC) AS rn\n",
    "    FROM cats\n",
    ")\n",
    "SELECT name, breed, country, price, rn AS rank\n",
    "FROM   ranked\n",
    "WHERE  rn <= 3;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Top 3 Most Expensive Cats')"
]))

# Q22
cells.append(make_cell("markdown", [
    "### Q22: Cheapest Cat Per Breed (RANK)\n",
    "Find the least expensive cat in each breed."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH cheapest AS (\n",
    "    SELECT name,\n",
    "           breed,\n",
    "           price,\n",
    "           RANK() OVER (\n",
    "               PARTITION BY breed\n",
    "               ORDER BY price ASC\n",
    "           ) AS rnk\n",
    "    FROM cats\n",
    ")\n",
    "SELECT name, breed, price\n",
    "FROM   cheapest\n",
    "WHERE  rnk = 1\n",
    "ORDER BY price;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Cheapest Cat Per Breed')\n",
    "plot_bar(df, 'breed', 'price',\n",
    "         title='Cheapest Cat Price by Breed',\n",
    "         xlabel='Breed', ylabel='Price ($)')"
]))

# Q23
cells.append(make_cell("markdown", [
    "### Q23: Two Youngest Cats Per Breed (ROW_NUMBER)\n",
    "Find the 2 most recently born cats in each breed."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH ranked AS (\n",
    "    SELECT name,\n",
    "           breed,\n",
    "           date_of_birth,\n",
    "           ROW_NUMBER() OVER (\n",
    "               PARTITION BY breed\n",
    "               ORDER BY date_of_birth DESC\n",
    "           ) AS rn\n",
    "    FROM cats\n",
    ")\n",
    "SELECT name, breed, date_of_birth\n",
    "FROM   ranked\n",
    "WHERE  rn <= 2\n",
    "ORDER BY breed, rn;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Two Youngest Cats Per Breed')"
]))

# Q24
cells.append(make_cell("markdown", [
    "### Q24: Rank Breeds by Average Price (RANK)\n",
    "Rank breeds from most to least expensive (by average)."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH breed_price AS (\n",
    "    SELECT breed,\n",
    "           ROUND(AVG(price), 0) AS avg_price\n",
    "    FROM   cats\n",
    "    GROUP BY breed\n",
    ")\n",
    "SELECT breed,\n",
    "       avg_price,\n",
    "       RANK() OVER (ORDER BY avg_price DESC) AS rank\n",
    "FROM   breed_price\n",
    "ORDER BY rank;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Breeds Ranked by Average Price')\n",
    "plot_horizontal_bar(df, 'breed', 'avg_price',\n",
    "                    title='Breeds Ranked by Average Price',\n",
    "                    xlabel='Average Price ($)')"
]))

# Q25
cells.append(make_cell("markdown", [
    "### Q25: Cat with Maximum Tricks (RANK + CTE)\n",
    "Who are the trickiest cats?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH trick_counts AS (\n",
    "    SELECT c.cat_id,\n",
    "           c.name,\n",
    "           c.breed,\n",
    "           COUNT(ct.trick_id) AS num_tricks\n",
    "    FROM   cats       c\n",
    "    JOIN   cat_tricks ct ON c.cat_id = ct.cat_id\n",
    "    GROUP BY c.cat_id, c.name, c.breed\n",
    "),\n",
    "ranked AS (\n",
    "    SELECT *,\n",
    "           RANK() OVER (ORDER BY num_tricks DESC) AS rnk\n",
    "    FROM trick_counts\n",
    ")\n",
    "SELECT name, breed, num_tricks, rnk AS rank\n",
    "FROM   ranked\n",
    "WHERE  rnk <= 5;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Top 5 Cats by Number of Tricks')"
]))

# Q26
cells.append(make_cell("markdown", [
    "### Q26: Most Expensive Male and Female Per Breed\n",
    "Use PARTITION BY breed, gender to find the top cat of each gender in each breed."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH ranked AS (\n",
    "    SELECT name,\n",
    "           breed,\n",
    "           gender,\n",
    "           price,\n",
    "           ROW_NUMBER() OVER (\n",
    "               PARTITION BY breed, gender\n",
    "               ORDER BY price DESC\n",
    "           ) AS rn\n",
    "    FROM cats\n",
    ")\n",
    "SELECT name, breed, gender, price\n",
    "FROM   ranked\n",
    "WHERE  rn = 1\n",
    "ORDER BY breed, gender;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Most Expensive Cat per Breed & Gender')\n",
    "plot_grouped_bar(df, 'breed', 'gender', 'price',\n",
    "                 title='Most Expensive Cat per Breed by Gender',\n",
    "                 xlabel='Breed', ylabel='Price ($)')"
]))

# ═══════════════════════════════════════════════════════════════════
# SECTION 5: Advanced Analytics
# ═══════════════════════════════════════════════════════════════════
cells.append(make_cell("markdown", [
    "---\n",
    "## Section 5: Advanced Analytics & Insights"
]))

# Q27
cells.append(make_cell("markdown", [
    "### Q27: Gender Distribution by Breed\n",
    "Compare male vs female counts across breeds."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT   breed,\n",
    "         gender,\n",
    "         COUNT(*) AS cnt\n",
    "FROM     cats\n",
    "GROUP BY breed, gender\n",
    "ORDER BY breed, gender;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Gender Distribution by Breed')\n",
    "plot_grouped_bar(df, 'breed', 'gender', 'cnt',\n",
    "                 title='Gender Distribution Across Breeds',\n",
    "                 xlabel='Breed', ylabel='Count')"
]))

# Q28
cells.append(make_cell("markdown", [
    "### Q28: Price vs Number of Tricks (Scatter)\n",
    "Is there a relationship between a cat's price and how many tricks it knows?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT c.name,\n",
    "       c.price,\n",
    "       COUNT(ct.trick_id) AS num_tricks\n",
    "FROM   cats       c\n",
    "JOIN   cat_tricks ct ON c.cat_id = ct.cat_id\n",
    "GROUP BY c.cat_id, c.name, c.price\n",
    "ORDER BY c.price DESC;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Price vs Tricks', max_rows=15)\n",
    "plot_scatter(df, 'num_tricks', 'price',\n",
    "             title='Cat Price vs Number of Tricks Known',\n",
    "             xlabel='Number of Tricks', ylabel='Price ($)')"
]))

# Q29
cells.append(make_cell("markdown", [
    "### Q29: Cats Born Per Year (Trend)\n",
    "How has our cat population grown over time?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT   EXTRACT(YEAR FROM date_of_birth) AS birth_year,\n",
    "         COUNT(*) AS num_cats\n",
    "FROM     cats\n",
    "GROUP BY birth_year\n",
    "ORDER BY birth_year;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Cats Born Per Year')\n",
    "plot_line(df, 'birth_year', 'num_cats',\n",
    "          title='Number of Cats Born Per Year',\n",
    "          xlabel='Year', ylabel='Count')"
]))

# Q30
cells.append(make_cell("markdown", [
    "### Q30: Price Quartiles Using NTILE\n",
    "Divide all cats into 4 price quartiles."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT name,\n",
    "       breed,\n",
    "       price,\n",
    "       NTILE(4) OVER (ORDER BY price) AS price_quartile\n",
    "FROM   cats\n",
    "ORDER BY price_quartile, price DESC\n",
    "LIMIT 20;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Cats with Price Quartiles (sample)')"
]))

# Q31
cells.append(make_cell("markdown", [
    "### Q31: Running Total of Cat Prices by Birth Date\n",
    "Cumulative price using a window function."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT name,\n",
    "       date_of_birth,\n",
    "       price,\n",
    "       SUM(price) OVER (\n",
    "           ORDER BY date_of_birth\n",
    "           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n",
    "       ) AS running_total\n",
    "FROM   cats\n",
    "ORDER BY date_of_birth\n",
    "LIMIT 20;\n",
    "\"\"\"\n",
    "\n",
    "run_and_show(con, sql, title='Running Total of Prices (first 20)')"
]))

# Q32
cells.append(make_cell("markdown", [
    "### Q32: Average Price Per Country (with Comparison to Overall)\n",
    "Compare each country's average price to the global average."
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH country_avg AS (\n",
    "    SELECT country,\n",
    "           ROUND(AVG(price), 0) AS country_avg_price\n",
    "    FROM   cats\n",
    "    GROUP BY country\n",
    "),\n",
    "overall AS (\n",
    "    SELECT ROUND(AVG(price), 0) AS overall_avg\n",
    "    FROM cats\n",
    ")\n",
    "SELECT ca.country,\n",
    "       ca.country_avg_price,\n",
    "       o.overall_avg,\n",
    "       ca.country_avg_price - o.overall_avg AS diff_from_overall\n",
    "FROM   country_avg ca\n",
    "CROSS JOIN overall o\n",
    "ORDER BY diff_from_overall DESC;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Country Avg vs Overall Avg Price')\n",
    "plot_bar(df, 'country', 'diff_from_overall',\n",
    "         title='Country Avg Price vs Overall Average (Difference)',\n",
    "         xlabel='Country', ylabel='Difference ($)')"
]))

# Q33
cells.append(make_cell("markdown", [
    "### Q33: Breed Diversity by Country\n",
    "How many distinct breeds are represented in each country?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "SELECT   country,\n",
    "         COUNT(DISTINCT breed) AS num_breeds\n",
    "FROM     cats\n",
    "GROUP BY country\n",
    "ORDER BY num_breeds DESC;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Breed Diversity by Country')\n",
    "plot_bar(df, 'country', 'num_breeds',\n",
    "         title='Number of Distinct Breeds Per Country',\n",
    "         xlabel='Country', ylabel='Number of Breeds')"
]))

# Q34
cells.append(make_cell("markdown", [
    "### Q34: Percentage of Cats Knowing Each Trick\n",
    "What fraction of all cats know each trick?"
]))
cells.append(make_cell("code", [
    "sql = \"\"\"\n",
    "WITH total_cats AS (\n",
    "    SELECT COUNT(DISTINCT cat_id) AS total\n",
    "    FROM   cat_tricks\n",
    ")\n",
    "SELECT t.trick,\n",
    "       COUNT(ct.cat_id) AS cats_know_it,\n",
    "       ROUND(COUNT(ct.cat_id) * 100.0 / tc.total, 1)\n",
    "           AS pct_of_cats\n",
    "FROM   tricks t\n",
    "JOIN   cat_tricks ct ON t.trick_id = ct.trick_id\n",
    "CROSS JOIN total_cats tc\n",
    "GROUP BY t.trick, tc.total\n",
    "ORDER BY pct_of_cats DESC;\n",
    "\"\"\"\n",
    "\n",
    "df = run_and_show(con, sql, title='Trick Penetration Rate')\n",
    "plot_horizontal_bar(df, 'trick', 'pct_of_cats',\n",
    "                    title='Percentage of Cats That Know Each Trick',\n",
    "                    xlabel='% of Cats')"
]))

# Closing
cells.append(make_cell("markdown", [
    "---\n",
    "## Summary\n",
    "\n",
    "In this notebook we explored:\n",
    "\n",
    "1. **Basic SELECT** — filtering, sorting, aggregation\n",
    "2. **JOINs** — INNER, LEFT, multi-table joins through junction tables\n",
    "3. **CTEs** — `WITH ... AS` for readable, reusable subqueries\n",
    "4. **Window Functions** — `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE()`, running totals\n",
    "5. **Advanced Analytics** — cross-comparisons, trend analysis, scatter correlations\n",
    "\n",
    "All queries run on **DuckDB** (fast, in-process, SQL-native analytics engine).\n",
    "\n",
    "---\n",
    "*End of notebook*"
]))

# ═══════════════════════════════════════════════════════════════════
# Assemble Notebook
# ═══════════════════════════════════════════════════════════════════
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "cells": cells
}

with open('/sessions/serene-festive-mccarthy/mnt/cats_and_breeds/cats_and_breeds_duckdb.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print("Notebook created successfully!")
print(f"Total cells: {len(cells)}")
