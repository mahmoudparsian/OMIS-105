"""
Streamlit + DuckDB — RANK, DENSE_RANK & ROW_NUMBER Explorer
=============================================================
One table: player_scores (player, country, score), loaded from players.csv.

Designed to teach the three SQL ranking/window functions and how
they behave differently when there are TIES in the data.

Tabs:
  1. View Data              — the full table + tie summary
  2. ROW_NUMBER             — unique sequential number, no gaps, no ties
  3. RANK                   — ties get the same rank, then GAPS
  4. DENSE_RANK             — ties get the same rank, NO gaps
  5. Compare All Three      — side-by-side in one query
  6. PARTITION BY            — ranking within groups
  7. SQL Explorer            — free-form practice

Usage:
    pip install streamlit duckdb pandas
    streamlit run app_ranking.py
"""

import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

DB_FILE = "ranking_demo.duckdb"
CSV_FILE = Path(__file__).parent / "players.csv"


def get_connection() -> duckdb.DuckDBPyConnection:
    if "db_conn" not in st.session_state:
        conn = duckdb.connect(DB_FILE)
        _init_table(conn)
        st.session_state.db_conn = conn
    return st.session_state.db_conn


def _init_table(conn: duckdb.DuckDBPyConnection):
    """Create and load player_scores from CSV."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS player_scores (
            player   VARCHAR NOT NULL,
            country  VARCHAR NOT NULL,
            score    INTEGER NOT NULL
        )
    """)
    if conn.execute("SELECT COUNT(*) FROM player_scores").fetchone()[0] == 0:
        if not CSV_FILE.exists():
            st.error(
                f"Data file not found: **{CSV_FILE.name}**\n\n"
                f"Place `players.csv` in the same folder as this script:\n"
                f"`{CSV_FILE.parent}`"
            )
            st.stop()
        conn.execute(f"""
            INSERT INTO player_scores
            SELECT * FROM read_csv_auto('{CSV_FILE}', header = true)
        """)


def reset_table():
    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS player_scores")
    _init_table(conn)


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def run_query(sql: str) -> pd.DataFrame:
    conn = get_connection()
    return conn.execute(sql).fetchdf()


def run_query_safe(sql: str):
    try:
        conn = get_connection()
        result = conn.execute(sql)
        try:
            cols = [d[0] for d in result.description]
            rows = result.fetchall()
            return pd.DataFrame(rows, columns=cols), None
        except Exception:
            return None, None
    except Exception as e:
        return None, str(e)


def get_all_scores() -> pd.DataFrame:
    return run_query("SELECT * FROM player_scores ORDER BY score DESC, player, country")


# ---------------------------------------------------------------------------
# Streamlit App
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Ranking Functions Explorer", page_icon="🏆", layout="wide")

st.title("🏆 RANK, DENSE_RANK & ROW_NUMBER Explorer")
st.caption(
    "Powered by **Streamlit** and **DuckDB** — "
    "See exactly how the three ranking functions differ when there are ties"
)

# Sidebar
with st.sidebar:
    st.header("Schema")
    st.code(
        "player_scores (\n"
        "  player   VARCHAR,\n"
        "  country  VARCHAR,\n"
        "  score    INTEGER\n"
        ")",
        language="sql",
    )
    st.divider()

    row_count = get_connection().execute("SELECT COUNT(*) FROM player_scores").fetchone()[0]
    st.metric("Total Records", row_count)
    st.divider()

    st.subheader("Key Differences")
    st.markdown(
        "| Function | Ties? | Gaps? |\n"
        "|----------|-------|-------|\n"
        "| ROW_NUMBER | No ties | No gaps |\n"
        "| RANK | Same rank for ties | Gaps after ties |\n"
        "| DENSE_RANK | Same rank for ties | No gaps |\n"
    )
    st.divider()

    st.subheader("Quick Example")
    st.markdown(
        "Scores: **95, 95, 88**\n\n"
        "| ROW_NUMBER | RANK | DENSE_RANK |\n"
        "|------------|------|------------|\n"
        "| 1 | 1 | 1 |\n"
        "| 2 | 1 | 1 |\n"
        "| 3 | **3** | **2** |\n"
    )
    st.divider()

    if st.button("Reset Table from CSV", type="secondary"):
        reset_table()
        st.success("Table reloaded from players.csv!")
        st.rerun()

    st.divider()
    st.caption(f"Data source: `{CSV_FILE.name}`")
    st.caption(f"DuckDB file: `{DB_FILE}`")


# Tabs
tab_data, tab_rownum, tab_rank, tab_dense, tab_compare, tab_top2, tab_partition, tab_sql = st.tabs([
    "📋 View Data",
    "1️⃣ ROW_NUMBER",
    "🏅 RANK",
    "🎖️ DENSE_RANK",
    "⚖️ Compare All Three",
    "🥇 Top-2 Per Group",
    "📊 PARTITION BY",
    "🧪 SQL Explorer",
])


# ---- TAB: View Data ----------------------------------------------------------
with tab_data:
    st.subheader("The player_scores Table")
    st.code("SELECT * FROM player_scores ORDER BY score DESC, player, country;", language="sql")

    df_all = get_all_scores()
    st.dataframe(df_all, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_all)} record(s)")

    st.divider()

    st.markdown("##### Data Summary")
    sum1, sum2, sum3 = st.columns(3)
    with sum1:
        st.markdown("**Players**")
        st.dataframe(
            run_query("SELECT player, COUNT(*) AS games FROM player_scores GROUP BY player ORDER BY player"),
            use_container_width=True, hide_index=True,
        )
    with sum2:
        st.markdown("**Countries**")
        st.dataframe(
            run_query("SELECT country, COUNT(*) AS games FROM player_scores GROUP BY country ORDER BY country"),
            use_container_width=True, hide_index=True,
        )
    with sum3:
        st.markdown("**Score Frequencies (ties!)**")
        st.dataframe(
            run_query("""
                SELECT score, COUNT(*) AS frequency
                FROM player_scores
                GROUP BY score
                ORDER BY score DESC
            """),
            use_container_width=True, hide_index=True,
        )

    st.info(
        "Notice that several scores appear multiple times (e.g., 95 and 88). "
        "These **ties** are what make RANK, DENSE_RANK, and ROW_NUMBER behave differently."
    )


# ---- TAB: ROW_NUMBER ---------------------------------------------------------
with tab_rownum:
    st.subheader("ROW_NUMBER()")
    st.markdown(
        "Assigns a **unique sequential integer** to each row. "
        "**No ties, no gaps.** If two rows have the same score, "
        "they still get different numbers (the order among ties is arbitrary)."
    )

    sql_rownum = """
SELECT
    ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num,
    player,
    country,
    score
FROM player_scores
ORDER BY row_num;"""

    st.markdown("##### Raw Table (sorted by score DESC)")
    st.dataframe(get_all_scores(), use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("##### ROW_NUMBER Result")
    st.code(sql_rownum.strip(), language="sql")
    df_rn = run_query(sql_rownum)
    st.dataframe(df_rn, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_rn)} row(s)")

    st.info(
        "**Notice:** Even though multiple rows have score = 95, each gets a *different* "
        "row_num (1, 2, 3, ...). ROW_NUMBER never produces duplicates."
    )


# ---- TAB: RANK ---------------------------------------------------------------
with tab_rank:
    st.subheader("RANK()")
    st.markdown(
        "Assigns the same rank to tied rows, then **skips numbers** (creates gaps). "
        "If two rows tie at rank 1, the next row gets rank **3** (not 2)."
    )

    sql_rank = """
SELECT
    RANK() OVER (ORDER BY score DESC) AS rank,
    player,
    country,
    score
FROM player_scores
ORDER BY rank, player;"""

    st.markdown("##### Raw Table (sorted by score DESC)")
    st.dataframe(get_all_scores(), use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("##### RANK Result")
    st.code(sql_rank.strip(), language="sql")
    df_rank = run_query(sql_rank)
    st.dataframe(df_rank, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_rank)} row(s)")

    # Highlight the gaps
    rank_values = sorted(df_rank["rank"].unique())
    gaps = [rank_values[i] for i in range(1, len(rank_values))
            if rank_values[i] != rank_values[i-1] + 1]
    if gaps:
        st.warning(
            f"**Gaps detected!** The rank sequence skips to: {', '.join(str(g) for g in gaps)}. "
            "This happens because RANK leaves gaps after tied rows."
        )


# ---- TAB: DENSE_RANK ---------------------------------------------------------
with tab_dense:
    st.subheader("DENSE_RANK()")
    st.markdown(
        "Assigns the same rank to tied rows, but **no gaps**. "
        "If two rows tie at rank 1, the next distinct score gets rank **2**."
    )

    sql_dense = """
SELECT
    DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank,
    player,
    country,
    score
FROM player_scores
ORDER BY dense_rank, player;"""

    st.markdown("##### Raw Table (sorted by score DESC)")
    st.dataframe(get_all_scores(), use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("##### DENSE_RANK Result")
    st.code(sql_dense.strip(), language="sql")
    df_dense = run_query(sql_dense)
    st.dataframe(df_dense, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_dense)} row(s)")

    dense_values = sorted(df_dense["dense_rank"].unique())
    expected = list(range(1, len(dense_values) + 1))
    if dense_values == expected:
        st.success(
            f"**No gaps!** Dense ranks go from 1 to {dense_values[-1]} with no skips. "
            "That's the key difference from RANK."
        )


# ---- TAB: Compare All Three --------------------------------------------------
with tab_compare:
    st.subheader("Compare: ROW_NUMBER vs RANK vs DENSE_RANK")
    st.markdown(
        "All three functions applied to the **same data** in a single query. "
        "Look at where the values diverge — that's where ties exist."
    )

    sql_compare = """
SELECT
    ROW_NUMBER()  OVER (ORDER BY score DESC) AS row_number,
    RANK()        OVER (ORDER BY score DESC) AS rank,
    DENSE_RANK()  OVER (ORDER BY score DESC) AS dense_rank,
    player,
    country,
    score
FROM player_scores
ORDER BY row_number;"""

    st.markdown("##### Raw Table")
    st.dataframe(get_all_scores(), use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("##### All Three Rankings Side by Side")
    st.code(sql_compare.strip(), language="sql")
    df_cmp = run_query(sql_compare)

    # Add a column that flags where the three functions diverge
    df_cmp["tie?"] = df_cmp.apply(
        lambda r: "← TIE"
        if not (r["row_number"] == r["rank"] == r["dense_rank"])
        else "",
        axis=1,
    )

    st.dataframe(df_cmp, use_container_width=True, hide_index=True)
    tie_count = (df_cmp["tie?"] != "").sum()
    st.caption(
        f"{len(df_cmp)} row(s) — "
        f"**{tie_count}** rows marked **← TIE** where the three functions give different values"
    )

    st.divider()

    st.markdown("##### Summary: How They Differ")
    diff_data = {
        "Function": ["ROW_NUMBER()", "RANK()", "DENSE_RANK()"],
        "Ties get same number?": ["No — always unique", "Yes", "Yes"],
        "Gaps after ties?": ["N/A (no ties)", "Yes — skips ranks", "No — consecutive"],
        "Max value": [
            "Always = row count",
            "Always = row count",
            "= number of distinct scores",
        ],
        "Use when": [
            "You need a unique row ID",
            "You want competition-style ranking (1st, 1st, 3rd)",
            "You want dense numbering (1st, 1st, 2nd)",
        ],
    }
    st.dataframe(pd.DataFrame(diff_data), use_container_width=True, hide_index=True)


# ---- TAB: Top-2 Per Group ----------------------------------------------------
with tab_top2:
    st.subheader("Top-2 Scores Per Player & Per Country")
    st.markdown(
        "A very common real-world pattern: *find the top N rows within each group*. "
        "This uses a **ranking window function inside a subquery**, "
        "then filters in the outer query."
    )

    # --- Top 2 per player ---
    st.markdown("##### Top-2 Scores Per Player")

    sql_top2_player = """
SELECT *
FROM (
    SELECT
        player,
        country,
        score,
        ROW_NUMBER()  OVER (PARTITION BY player ORDER BY score DESC) AS row_num,
        RANK()        OVER (PARTITION BY player ORDER BY score DESC) AS rank,
        DENSE_RANK()  OVER (PARTITION BY player ORDER BY score DESC) AS dense_rank
    FROM player_scores
) ranked
WHERE dense_rank <= 2
ORDER BY player, dense_rank, country;"""

    st.markdown("**Raw Table**")
    st.dataframe(get_all_scores(), use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("**Step 1 — Rank all rows within each player (inner subquery)**")
    sql_inner_player = """
SELECT
    player,
    country,
    score,
    ROW_NUMBER()  OVER (PARTITION BY player ORDER BY score DESC) AS row_num,
    RANK()        OVER (PARTITION BY player ORDER BY score DESC) AS rank,
    DENSE_RANK()  OVER (PARTITION BY player ORDER BY score DESC) AS dense_rank
FROM player_scores
ORDER BY player, dense_rank, country;"""
    st.code(sql_inner_player.strip(), language="sql")
    df_inner_player = run_query(sql_inner_player)
    st.dataframe(df_inner_player, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_inner_player)} row(s) — all rows with rankings per player")

    st.markdown("**Step 2 — Filter: keep only DENSE_RANK <= 2**")
    st.code(sql_top2_player.strip(), language="sql")
    df_top2_player = run_query(sql_top2_player)
    st.dataframe(df_top2_player, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_top2_player)} row(s) kept")

    st.info(
        "**Why DENSE_RANK?** If a player has two scores tied at #1, "
        "DENSE_RANK gives both rank 1, and the next score gets rank 2 — "
        "so `WHERE dense_rank <= 2` captures the top 2 *distinct* score levels. "
        "Using RANK might miss the second-best score if there are many ties at #1. "
        "Using ROW_NUMBER would always return exactly 2 rows but might arbitrarily "
        "exclude a tied score."
    )

    st.divider()

    # --- Top 2 per country ---
    st.markdown("##### Top-2 Scores Per Country")

    sql_top2_country = """
SELECT *
FROM (
    SELECT
        country,
        player,
        score,
        ROW_NUMBER()  OVER (PARTITION BY country ORDER BY score DESC) AS row_num,
        RANK()        OVER (PARTITION BY country ORDER BY score DESC) AS rank,
        DENSE_RANK()  OVER (PARTITION BY country ORDER BY score DESC) AS dense_rank
    FROM player_scores
) ranked
WHERE dense_rank <= 2
ORDER BY country, dense_rank, player;"""

    st.markdown("**Step 1 — Rank all rows within each country (inner subquery)**")
    sql_inner_country = """
SELECT
    country,
    player,
    score,
    ROW_NUMBER()  OVER (PARTITION BY country ORDER BY score DESC) AS row_num,
    RANK()        OVER (PARTITION BY country ORDER BY score DESC) AS rank,
    DENSE_RANK()  OVER (PARTITION BY country ORDER BY score DESC) AS dense_rank
FROM player_scores
ORDER BY country, dense_rank, player;"""
    st.code(sql_inner_country.strip(), language="sql")
    df_inner_country = run_query(sql_inner_country)
    st.dataframe(df_inner_country, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_inner_country)} row(s) — all rows with rankings per country")

    st.markdown("**Step 2 — Filter: keep only DENSE_RANK <= 2**")
    st.code(sql_top2_country.strip(), language="sql")
    df_top2_country = run_query(sql_top2_country)
    st.dataframe(df_top2_country, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_top2_country)} row(s) kept")

    st.info(
        "Notice that some countries return more than 2 rows — that's because "
        "multiple players share the same top scores, and DENSE_RANK keeps all ties. "
        "Compare the `row_num`, `rank`, and `dense_rank` columns to see the differences."
    )


# ---- TAB: PARTITION BY -------------------------------------------------------
with tab_partition:
    st.subheader("PARTITION BY — Ranking Within Groups")
    st.markdown(
        "Without PARTITION BY, ranking is over the **entire table**. "
        "With PARTITION BY, ranking **restarts for each group**."
    )

    part_col = st.selectbox(
        "PARTITION BY column",
        ["player", "country"],
        key="part_col",
    )

    func_choice = st.selectbox(
        "Ranking function",
        ["ROW_NUMBER()", "RANK()", "DENSE_RANK()"],
        key="part_func",
    )

    sql_partition = f"""
SELECT
    {part_col},
    player || ' — ' || country AS detail,
    score,
    {func_choice} OVER (
        PARTITION BY {part_col}
        ORDER BY score DESC
    ) AS ranking
FROM player_scores
ORDER BY {part_col}, ranking;"""

    st.markdown("##### Raw Table")
    st.dataframe(get_all_scores(), use_container_width=True, hide_index=True)

    st.divider()

    st.markdown(f"##### {func_choice} Partitioned by `{part_col}`")
    st.code(sql_partition.strip(), language="sql")
    df_part = run_query(sql_partition)
    st.dataframe(df_part, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_part)} row(s)")

    # Show how many partitions and their sizes
    st.divider()
    st.markdown("##### Partition Sizes")

    sql_part_sizes = f"""
SELECT
    {part_col},
    COUNT(*) AS rows_in_partition,
    MIN(score) AS min_score,
    MAX(score) AS max_score,
    STRING_AGG(
        player || ' (' || score || ')',
        ', '
        ORDER BY score DESC
    ) AS members
FROM player_scores
GROUP BY {part_col}
ORDER BY {part_col};"""

    st.code(sql_part_sizes.strip(), language="sql")
    st.dataframe(run_query(sql_part_sizes), use_container_width=True, hide_index=True)

    st.info(
        f"The ranking **restarts at 1** for each `{part_col}`. "
        "Compare with the non-partitioned version in the other tabs "
        "where ranking goes across all rows."
    )

    # Bonus: practical example
    with st.expander("Practical Use: Top N per Group"):
        n_val = st.number_input("Show top N per group", min_value=1, max_value=5, value=2, key="topn")

        sql_topn = f"""
-- Get the top {n_val} score(s) per {part_col}
SELECT *
FROM (
    SELECT
        {part_col},
        player,
        country,
        score,
        DENSE_RANK() OVER (
            PARTITION BY {part_col}
            ORDER BY score DESC
        ) AS dr
    FROM player_scores
) ranked
WHERE dr <= {n_val}
ORDER BY {part_col}, dr;"""

        st.code(sql_topn.strip(), language="sql")
        st.dataframe(run_query(sql_topn), use_container_width=True, hide_index=True)
        st.caption(
            f"This is a common pattern: use a window function in a subquery, "
            f"then filter in the outer query. Here we keep only rows with DENSE_RANK <= {n_val}."
        )


# ---- TAB: SQL Explorer -------------------------------------------------------
with tab_sql:
    st.subheader("SQL Explorer")
    st.info("Write any SQL against the **player_scores** table.")

    examples = {
        "(custom)": "",
        "All three rankings": (
            "SELECT\n"
            "    ROW_NUMBER()  OVER (ORDER BY score DESC) AS row_number,\n"
            "    RANK()        OVER (ORDER BY score DESC) AS rank,\n"
            "    DENSE_RANK()  OVER (ORDER BY score DESC) AS dense_rank,\n"
            "    player, country, score\n"
            "FROM player_scores\n"
            "ORDER BY row_number;"
        ),
        "Rank per player": (
            "SELECT\n"
            "    player,\n"
            "    country,\n"
            "    score,\n"
            "    RANK() OVER (PARTITION BY player ORDER BY score DESC) AS rank_within_player\n"
            "FROM player_scores\n"
            "ORDER BY player, rank_within_player;"
        ),
        "Rank per country": (
            "SELECT\n"
            "    country,\n"
            "    player,\n"
            "    score,\n"
            "    DENSE_RANK() OVER (PARTITION BY country ORDER BY score DESC) AS country_rank\n"
            "FROM player_scores\n"
            "ORDER BY country, country_rank;"
        ),
        "Top 1 per country": (
            "SELECT * FROM (\n"
            "    SELECT\n"
            "        country,\n"
            "        player,\n"
            "        score,\n"
            "        ROW_NUMBER() OVER (PARTITION BY country ORDER BY score DESC) AS rn\n"
            "    FROM player_scores\n"
            ") sub\n"
            "WHERE rn = 1\n"
            "ORDER BY country;"
        ),
        "Running total per player": (
            "SELECT\n"
            "    player,\n"
            "    country,\n"
            "    score,\n"
            "    SUM(score) OVER (\n"
            "        PARTITION BY player\n"
            "        ORDER BY score DESC\n"
            "        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
            "    ) AS running_total\n"
            "FROM player_scores\n"
            "ORDER BY player, score DESC;"
        ),
        "Percentile rank": (
            "SELECT\n"
            "    player,\n"
            "    country,\n"
            "    score,\n"
            "    ROUND(\n"
            "        PERCENT_RANK() OVER (ORDER BY score DESC) * 100, 1\n"
            "    ) AS percentile\n"
            "FROM player_scores\n"
            "ORDER BY score DESC;"
        ),
        "Score vs group average": (
            "SELECT\n"
            "    player,\n"
            "    country,\n"
            "    score,\n"
            "    ROUND(AVG(score) OVER (PARTITION BY player), 1) AS player_avg,\n"
            "    score - ROUND(AVG(score) OVER (PARTITION BY player), 1) AS diff_from_avg\n"
            "FROM player_scores\n"
            "ORDER BY player, score DESC;"
        ),
        "LAG / LEAD (prev & next score)": (
            "SELECT\n"
            "    player,\n"
            "    country,\n"
            "    score,\n"
            "    LAG(score)  OVER (ORDER BY score DESC) AS prev_score,\n"
            "    LEAD(score) OVER (ORDER BY score DESC) AS next_score\n"
            "FROM player_scores\n"
            "ORDER BY score DESC;"
        ),
        "Describe table": "DESCRIBE player_scores;",
    }

    chosen = st.selectbox("Quick examples", examples.keys(), key="sql_ex")
    default_sql = examples[chosen]

    sql_input = st.text_area(
        "Enter your SQL",
        value=default_sql,
        height=200,
        placeholder="SELECT *, RANK() OVER (ORDER BY score DESC) FROM player_scores;",
        key="sql_input",
    )

    if st.button("Run Query", type="primary", key="run_sql"):
        if not sql_input.strip():
            st.error("Please enter a SQL statement.")
        else:
            statements = [
                s.strip() for s in sql_input.strip().split(";")
                if s.strip() and not s.strip().startswith("--")
            ]
            for i, stmt in enumerate(statements):
                if len(statements) > 1:
                    st.markdown(f"**Statement {i+1}:**")
                    st.code(stmt + ";", language="sql")
                df, err = run_query_safe(stmt)
                if err:
                    st.error(f"SQL Error: {err}")
                elif df is not None:
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.caption(f"Returned {len(df)} row(s)")
                else:
                    st.success("Statement executed successfully.")


# Footer
st.divider()
st.caption(
    "Built with [Streamlit](https://streamlit.io) • "
    "Data stored in [DuckDB](https://duckdb.org) • "
    "Designed for introductory DBMS courses"
)
