"""
app_level3.py — University Bookstore · Level 3: Analytics & Power
OMIS-105: Introduction to DBMS · Santa Clara University

Concepts covered:
    Window functions (ROW_NUMBER, RANK, SUM OVER, AVG OVER PARTITION BY),
    subqueries (scalar and correlated), INSERT, CREATE / DROP INDEX,
    query timing and performance

Run:
    pip install streamlit duckdb pandas
    streamlit run app_level3.py
"""

import os
import time
import duckdb
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Config ────────────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "bookstore.duckdb")

st.set_page_config(
    page_title="Bookstore · Level 3",
    page_icon="🚀",
    layout="wide",
)

# ── DB helpers ────────────────────────────────────────────────────────────────
# Level 3 opens in write mode (needed for INSERT and CREATE INDEX).
# A new connection is created per write operation to avoid stale state;
# reads use a cached connection for speed.

@st.cache_resource
def get_conn():
    """Cached read/write connection — used for SELECT queries."""
    return duckdb.connect(DB_PATH)

def run(sql: str) -> pd.DataFrame:
    return get_conn().execute(sql).df()

def run_write(sql: str):
    """Execute a write statement and clear the read cache so results refresh."""
    con = duckdb.connect(DB_PATH)
    con.execute(sql)
    con.close()
    get_conn.clear()          # invalidate cache so next read sees new data

def next_id(table: str, pk_col: str) -> int:
    return int(run(f"SELECT COALESCE(MAX({pk_col}),0)+1 FROM {table}").iloc[0, 0])

# ── Sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.title("📚 University Bookstore")
st.sidebar.caption("OMIS-105 · Level 3: Analytics & Power")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📈 Analytics Dashboard", "➕ Add Records", "⚡ Index Lab"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
**Level 3 Concepts**
- `ROW_NUMBER()` — unique rank per row
- `RANK()` — rank with ties
- `SUM() OVER` — running total
- `AVG() OVER PARTITION BY` — group avg alongside each row
- Subqueries — queries inside queries
- `INSERT INTO` — add new data
- `CREATE INDEX` — speed up lookups
"""
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 · ANALYTICS DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────

if page == "📈 Analytics Dashboard":
    st.title("📈 Analytics Dashboard")
    st.markdown(
        "Window functions and subqueries let you ask questions that are impossible "
        "with simple GROUP BY — comparing each row to a group average, computing "
        "running totals, and ranking within partitions."
    )

    analysis = st.selectbox(
        "Choose an analysis",
        [
            "1 · Running total of revenue by date",
            "2 · Rank students by total spend",
            "3 · Rank books by purchases within category",
            "4 · Each student vs their major's average spend",
            "5 · Students who spent above the overall average (subquery)",
            "6 · Books priced above their category average (subquery)",
        ],
    )

    st.markdown("---")

    # ── Analysis 1: Running total ─────────────────────────────────────────────
    if analysis.startswith("1"):
        st.subheader("📅 Running Total of Revenue by Date")

        sql = """\
SELECT purchase_date,
       ROUND(SUM(total_amount), 2)           AS daily_revenue,
       ROUND(SUM(SUM(total_amount))
             OVER (ORDER BY purchase_date), 2) AS running_total
FROM   purchases
GROUP  BY purchase_date
ORDER  BY purchase_date;"""

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"{len(df)} distinct purchase dates · "
                       f"final total ${df['running_total'].iloc[-1]:,.2f}")
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                """
**How it works:**

`SUM(total_amount)` inside `GROUP BY` computes the **daily** total.

`SUM(...) OVER (ORDER BY purchase_date)` is a **window function** — it looks
at all rows in the result, ordered by date, and keeps a cumulative sum.

The `OVER` clause is the key: it tells SQL *"apply this aggregate across a
sliding window of rows"*, not just within the current group.
                """
            )

        # Chart — bars for daily revenue, line for running total
        fig, ax1 = plt.subplots(figsize=(12, 4))
        fig.patch.set_facecolor("#0e1117")
        ax1.set_facecolor("#0e1117")
        dates = pd.to_datetime(df["purchase_date"])
        ax1.bar(dates, df["daily_revenue"], color="#6366f1", alpha=0.7,
                width=1.5, label="Daily Revenue")
        ax1.set_ylabel("Daily Revenue ($)", color="#6366f1")
        ax1.tick_params(axis="y", colors="#6366f1")
        ax1.tick_params(axis="x", colors="#aaa", rotation=45)
        ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax2 = ax1.twinx()
        ax2.plot(dates, df["running_total"], color="#10b981", linewidth=2.5,
                 marker="o", markersize=3, label="Running Total")
        ax2.set_ylabel("Running Total ($)", color="#10b981")
        ax2.tick_params(axis="y", colors="#10b981")
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        for spine in ax1.spines.values(): spine.set_edgecolor("#333")
        for spine in ax2.spines.values(): spine.set_edgecolor("#333")
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, facecolor="#1e1e2e",
                   labelcolor="white", loc="upper left", fontsize=9)
        ax1.set_title("Daily Revenue (bars) vs Cumulative Revenue (line)",
                      color="white", fontsize=11, pad=10)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ── Analysis 2: Rank students by spend ───────────────────────────────────
    elif analysis.startswith("2"):
        st.subheader("🏆 Rank Students by Total Spend")

        rank_fn = st.radio(
            "Ranking function",
            ["ROW_NUMBER", "RANK", "DENSE_RANK"],
            horizontal=True,
        )

        sql = f"""\
SELECT {rank_fn}() OVER (ORDER BY total_spent DESC) AS rank,
       name, major,
       ROUND(total_spent, 2) AS total_spent
FROM (
    SELECT s.name, s.major,
           SUM(p.total_amount) AS total_spent
    FROM   purchases p
    JOIN   students s ON p.student_id = s.student_id
    GROUP  BY s.name, s.major
) ranked
ORDER BY rank;"""

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql)
            st.dataframe(df, use_container_width=True, hide_index=True)
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                f"""
**`{rank_fn}()` explained:**

- **`ROW_NUMBER`** — always gives each row a unique number (1, 2, 3 …),
  even if two students spent the same amount.
- **`RANK`** — gives tied rows the same number, then skips ahead
  (1, 2, 2, 4 …).
- **`DENSE_RANK`** — gives tied rows the same number, no gaps
  (1, 2, 2, 3 …).

Try switching between them — the dataset may not have ties,
but the difference becomes critical in larger datasets.
                """
            )

        # Chart — horizontal bar chart ranked by spend, colored by major
        major_colors = {
            "Computer Science":      "#6366f1",
            "Electrical Engineering":"#10b981",
            "Business Analytics":    "#f59e0b",
            "English Literature":    "#ec4899",
            "Mechanical Engineering":"#3b82f6",
        }
        df_sorted = df.sort_values("total_spent", ascending=True)
        colors = [major_colors.get(m, "#94a3b8") for m in df_sorted["major"]]
        fig, ax = plt.subplots(figsize=(10, max(4, len(df_sorted) * 0.45)))
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")
        bars = ax.barh(df_sorted["name"], df_sorted["total_spent"],
                       color=colors, edgecolor="none")
        for bar, val in zip(bars, df_sorted["total_spent"]):
            ax.text(bar.get_width() + 8, bar.get_y() + bar.get_height() / 2,
                    f"${val:,.0f}", va="center", color="white", fontsize=8.5)
        ax.set_xlabel("Total Spend ($)", color="#aaa")
        ax.tick_params(colors="#aaa")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        for spine in ax.spines.values(): spine.set_edgecolor("#333")
        # Legend for majors
        seen = {}
        for m, c in zip(df_sorted["major"], colors):
            seen[m] = c
        handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in seen.values()]
        ax.legend(handles, list(seen.keys()), facecolor="#1e1e2e",
                  labelcolor="white", fontsize=8, loc="lower right")
        ax.set_title(f"Students Ranked by Total Spend  ({rank_fn})",
                     color="white", fontsize=11, pad=10)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ── Analysis 3: Books ranked within category ──────────────────────────────
    elif analysis.startswith("3"):
        st.subheader("📚 Books Ranked by Purchases Within Category")

        sql = """\
SELECT b.category,
       b.title,
       COUNT(*)                                           AS times_purchased,
       RANK() OVER (
           PARTITION BY b.category
           ORDER BY COUNT(*) DESC
       )                                                  AS rank_in_category
FROM   purchases p
JOIN   books b ON p.book_id = b.book_id
GROUP  BY b.category, b.title
ORDER  BY b.category, rank_in_category;"""

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql)
            st.dataframe(df, use_container_width=True, hide_index=True)
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                """
**Key clause:** `PARTITION BY b.category`

`PARTITION BY` splits the window into groups — here, one group per category.
The `RANK()` counter **restarts at 1** for each category.

Without `PARTITION BY`, all books would be ranked together globally.
With it, you get the #1 book *within each category* — much more useful.

This pattern (ranking within a group) is one of the most common uses
of window functions in real-world analytics.
                """
            )

        # Chart — horizontal bars faceted by category
        cat_palette = {"Textbook": "#6366f1", "Reference": "#10b981", "Novel": "#f59e0b"}
        categories = df["category"].unique()
        fig, axes = plt.subplots(1, len(categories),
                                  figsize=(14, max(3, df["rank_in_category"].max() * 0.5)),
                                  sharey=False)
        fig.patch.set_facecolor("#0e1117")
        if len(categories) == 1:
            axes = [axes]
        for ax, cat in zip(axes, sorted(categories)):
            ax.set_facecolor("#0e1117")
            sub = df[df["category"] == cat].sort_values("rank_in_category")
            color = cat_palette.get(cat, "#94a3b8")
            # Shorten long titles
            labels = [t[:28] + "…" if len(t) > 28 else t for t in sub["title"]]
            bars = ax.barh(labels[::-1], sub["times_purchased"].values[::-1],
                           color=color, alpha=0.85, edgecolor="none")
            for bar, val in zip(bars, sub["times_purchased"].values[::-1]):
                ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                        str(int(val)), va="center", color="white", fontsize=8)
            ax.set_title(cat, color=color, fontsize=10, fontweight="bold", pad=8)
            ax.tick_params(colors="#aaa", labelsize=8)
            ax.set_xlabel("Times Purchased", color="#aaa", fontsize=8)
            for spine in ax.spines.values(): spine.set_edgecolor("#333")
            ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        fig.suptitle("Purchase Count Ranked Within Each Category  (RANK + PARTITION BY)",
                     color="white", fontsize=11, y=1.02)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ── Analysis 4: Student vs major average ─────────────────────────────────
    elif analysis.startswith("4"):
        st.subheader("🎓 Each Student vs Their Major's Average Spend")

        sql = """\
SELECT s.name,
       s.major,
       ROUND(SUM(p.total_amount), 2)                   AS student_total,
       ROUND(AVG(SUM(p.total_amount))
             OVER (PARTITION BY s.major), 2)            AS major_avg,
       ROUND(SUM(p.total_amount)
             - AVG(SUM(p.total_amount))
               OVER (PARTITION BY s.major), 2)          AS vs_major_avg
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.name, s.major
ORDER  BY s.major, student_total DESC;"""

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql)
            # Colour vs_major_avg column
            def color_diff(val):
                color = "color: #10b981" if val > 0 else ("color: #ef4444" if val < 0 else "")
                return color
            styled = df.style.applymap(color_diff, subset=["vs_major_avg"])
            st.dataframe(styled, use_container_width=True, hide_index=True)
            st.caption("Green = spent above major average · Red = below major average")
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                """
**`AVG(...) OVER (PARTITION BY major)`**

This computes the average spend for all students in the same major —
and places that value *alongside* each individual student's row.

Without a window function, you'd need a self-join or subquery to
achieve this. The result lets you compare each row to its group
in a single pass.

`vs_major_avg` = student's total minus their major's average.
Positive means they spent more than their peers; negative means less.
                """
            )

        # Chart — bars per student, colored above/below, avg line per major group
        fig, ax = plt.subplots(figsize=(12, 4))
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")
        x = range(len(df))
        bar_colors = ["#10b981" if v >= 0 else "#ef4444" for v in df["vs_major_avg"]]
        ax.bar(x, df["student_total"], color=bar_colors, alpha=0.85, edgecolor="none",
               label="Student Total")
        # Draw major-average line segments
        major_groups = df.groupby("major", sort=False)
        for major, grp in major_groups:
            idxs = grp.index.tolist()
            positions = [list(df.index).index(i) for i in idxs]
            avg_val = grp["major_avg"].iloc[0]
            ax.hlines(avg_val, min(positions) - 0.4, max(positions) + 0.4,
                      colors="#f59e0b", linewidth=2, linestyles="--")
            ax.text(max(positions) + 0.5, avg_val, f"avg\n${avg_val:,.0f}",
                    color="#f59e0b", fontsize=7.5, va="center")
        ax.set_xticks(list(x))
        ax.set_xticklabels(
            [f"{n.split()[0]}\n({m[:4]}…)" if len(m) > 7 else f"{n.split()[0]}\n({m})"
             for n, m in zip(df["name"], df["major"])],
            fontsize=8, color="#aaa"
        )
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax.tick_params(axis="y", colors="#aaa")
        for spine in ax.spines.values(): spine.set_edgecolor("#333")
        from matplotlib.lines import Line2D
        legend_els = [
            plt.Rectangle((0,0),1,1, color="#10b981", alpha=0.85, label="Above major avg"),
            plt.Rectangle((0,0),1,1, color="#ef4444", alpha=0.85, label="Below major avg"),
            Line2D([0],[0], color="#f59e0b", linewidth=2, linestyle="--", label="Major average"),
        ]
        ax.legend(handles=legend_els, facecolor="#1e1e2e", labelcolor="white",
                  fontsize=8, loc="upper right")
        ax.set_title("Student Spend vs Major Average  (AVG OVER PARTITION BY major)",
                     color="white", fontsize=11, pad=10)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ── Analysis 5: Subquery — above average spenders ────────────────────────
    elif analysis.startswith("5"):
        st.subheader("💡 Students Who Spent Above the Overall Average (Subquery)")

        sql = """\
SELECT s.name, s.major,
       ROUND(SUM(p.total_amount), 2) AS total_spent
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.name, s.major
HAVING SUM(p.total_amount) > (
    SELECT AVG(student_total)
    FROM (
        SELECT SUM(total_amount) AS student_total
        FROM   purchases
        GROUP  BY student_id
    )
)
ORDER  BY total_spent DESC;"""

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql)
            avg_val = run("""
                SELECT ROUND(AVG(student_total),2) AS avg
                FROM (SELECT SUM(total_amount) AS student_total
                      FROM purchases GROUP BY student_id)
            """).iloc[0]["avg"]
            st.info(f"Overall average spend per student: **${avg_val:,.2f}**")
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"{len(df)} students spent above the ${avg_val:,.2f} average.")
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                """
**What is a subquery?**

A subquery is a `SELECT` statement nested inside another query.
Here, the inner query computes the average spend per student.
The outer `HAVING` clause compares each student's total to that average.

The inner query runs *first* and returns a single number (a **scalar subquery**).
The outer query uses that number as if it were a literal value.

You could not write `HAVING SUM(...) > AVG(SUM(...))` directly —
the scalar subquery is the clean, readable way to express this.
                """
            )

        # Chart — all students shown, above-avg highlighted, avg reference line
        all_students = run("""
            SELECT s.name, ROUND(SUM(p.total_amount),2) AS total_spent
            FROM purchases p JOIN students s ON p.student_id = s.student_id
            GROUP BY s.name ORDER BY total_spent DESC
        """)
        fig, ax = plt.subplots(figsize=(11, 4))
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")
        colors = ["#6366f1" if v > avg_val else "#334155" for v in all_students["total_spent"]]
        ax.bar(all_students["name"], all_students["total_spent"],
               color=colors, edgecolor="none")
        ax.axhline(avg_val, color="#f59e0b", linewidth=2, linestyle="--",
                   label=f"Overall avg  ${avg_val:,.2f}")
        ax.set_xticklabels(all_students["name"], rotation=30, ha="right",
                           fontsize=9, color="#aaa")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax.tick_params(axis="y", colors="#aaa")
        for spine in ax.spines.values(): spine.set_edgecolor("#333")
        from matplotlib.patches import Patch
        legend_els = [
            Patch(color="#6366f1", label="Above average"),
            Patch(color="#334155", label="Below average"),
            plt.Line2D([0],[0], color="#f59e0b", linewidth=2,
                       linestyle="--", label=f"Average ${avg_val:,.2f}"),
        ]
        ax.legend(handles=legend_els, facecolor="#1e1e2e", labelcolor="white",
                  fontsize=8, loc="upper right")
        ax.set_title("All Students by Total Spend — Above-Average Highlighted  (Scalar Subquery)",
                     color="white", fontsize=11, pad=10)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ── Analysis 6: Subquery — books above category average ──────────────────
    elif analysis.startswith("6"):
        st.subheader("📖 Books Priced Above Their Category Average (Correlated Subquery)")

        sql = """\
SELECT b.title, b.category, b.price,
       ROUND((SELECT AVG(price)
              FROM   books b2
              WHERE  b2.category = b.category), 2) AS category_avg,
       ROUND(b.price
             - (SELECT AVG(price)
                FROM   books b2
                WHERE  b2.category = b.category), 2) AS above_avg_by
FROM   books b
WHERE  b.price > (
    SELECT AVG(price)
    FROM   books b2
    WHERE  b2.category = b.category
)
ORDER  BY b.category, b.price DESC;"""

        col1, col2 = st.columns([3, 2])
        with col1:
            df = run(sql)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"{len(df)} books cost more than their category average.")
        with col2:
            st.code(sql, language="sql")
            st.markdown(
                """
**Correlated subquery:**

The inner `SELECT AVG(price) ... WHERE b2.category = b.category`
references `b.category` from the *outer* query. This means it runs
once *per row* of the outer query — it is **correlated**.

Each book is compared to the average price of its own category,
not the average of all books. Without correlation, a cheap novel
could be falsely flagged as expensive just because textbooks
pull the overall average up.

Correlated subqueries are powerful but can be slow on large tables —
which is exactly why indexes and query optimisers exist.
                """
            )

        # Chart — all books as dots by category, avg line per category, above-avg filled
        all_books = run("""
            SELECT b.title, b.category, b.price,
                   ROUND(AVG(b2.price),2) AS cat_avg
            FROM books b
            JOIN books b2 ON b.category = b2.category
            GROUP BY b.title, b.category, b.price
            ORDER BY b.category, b.price DESC
        """)
        cat_palette = {"Textbook": "#6366f1", "Reference": "#10b981", "Novel": "#f59e0b"}
        categories = sorted(all_books["category"].unique())
        fig, axes = plt.subplots(1, len(categories), figsize=(14, 5), sharey=False)
        fig.patch.set_facecolor("#0e1117")
        if len(categories) == 1:
            axes = [axes]
        for ax, cat in zip(axes, categories):
            ax.set_facecolor("#0e1117")
            sub = all_books[all_books["category"] == cat].sort_values("price", ascending=False)
            cat_avg = sub["cat_avg"].iloc[0]
            color = cat_palette.get(cat, "#94a3b8")
            short = [t[:22]+"…" if len(t)>22 else t for t in sub["title"]]
            ypos = range(len(sub))
            # All books as dots
            ax.scatter(sub["price"], list(ypos), color=color, s=80, zorder=3)
            # Horizontal bars from 0 to price
            for i, (p, above) in enumerate(zip(sub["price"], sub["price"] > cat_avg)):
                ax.barh(i, p, color=color, alpha=0.55 if above else 0.2,
                        edgecolor="none", height=0.6)
            # Category average line
            ax.axvline(cat_avg, color="#f59e0b", linewidth=1.8, linestyle="--",
                       label=f"Avg ${cat_avg:,.0f}")
            ax.set_yticks(list(ypos))
            ax.set_yticklabels(short, fontsize=7.5, color="#aaa")
            ax.tick_params(axis="x", colors="#aaa", labelsize=8)
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
            for spine in ax.spines.values(): spine.set_edgecolor("#333")
            ax.set_title(cat, color=color, fontsize=10, fontweight="bold", pad=8)
            ax.legend(facecolor="#1e1e2e", labelcolor="white", fontsize=8)
        fig.suptitle("Book Prices vs Category Average  (Correlated Subquery) — Bright = Above Average",
                     color="white", fontsize=11, y=1.02)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 · ADD RECORDS
# ─────────────────────────────────────────────────────────────────────────────

elif page == "➕ Add Records":
    st.title("➕ Add Records")
    st.markdown(
        "Level 3 is the first app that can **write** to the database. "
        "Use the forms below to INSERT new students and purchases. "
        "The generated SQL is shown before each write."
    )

    tab1, tab2 = st.tabs(["🎓 Add a Student", "🛒 Add a Purchase"])

    # ── Tab 1: Add student ────────────────────────────────────────────────────
    with tab1:
        st.subheader("Insert a New Student")

        col1, col2 = st.columns(2)
        with col1:
            new_name  = st.text_input("Full name", placeholder="e.g. Sofia Reyes")
            new_email = st.text_input("SCU email", placeholder="e.g. sreyes@scu.edu")
            new_major = st.selectbox(
                "Major",
                ["Computer Science", "Electrical Engineering",
                 "Business Analytics", "English Literature",
                 "Mechanical Engineering", "Other"],
            )
        with col2:
            new_year = st.selectbox("Year", [1, 2, 3, 4],
                                    format_func=lambda x: {1:"Freshman",2:"Sophomore",
                                                            3:"Junior",4:"Senior"}[x])
            new_gpa  = st.slider("GPA", 0.0, 4.0, 3.5, 0.01)

        new_id = next_id("students", "student_id")
        insert_sql = (
            f"INSERT INTO students\n"
            f"    (student_id, name, email, major, year, gpa)\n"
            f"VALUES\n"
            f"    ({new_id}, '{new_name}', '{new_email}',\n"
            f"     '{new_major}', {new_year}, {new_gpa});"
        )

        st.markdown("**Generated SQL:**")
        st.code(insert_sql, language="sql")

        if st.button("▶ Run INSERT — Add Student", type="primary"):
            if not new_name.strip():
                st.error("Please enter a name.")
            elif not new_email.strip():
                st.error("Please enter an email.")
            elif "@" not in new_email:
                st.error("Email must contain @.")
            else:
                try:
                    run_write(insert_sql.rstrip(";"))
                    st.success(f"✓ Student **{new_name}** added with student_id = {new_id}.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Insert failed: {e}")

        st.markdown("---")
        st.subheader("Current Students Table")
        st.dataframe(run("SELECT * FROM students ORDER BY student_id"),
                     use_container_width=True, hide_index=True)

    # ── Tab 2: Add purchase ───────────────────────────────────────────────────
    with tab2:
        st.subheader("Insert a New Purchase")

        students_df = run("SELECT student_id, name FROM students ORDER BY name")
        books_df    = run("SELECT book_id, title, price FROM books ORDER BY title")
        courses_df  = run("SELECT course_id, course_name FROM courses ORDER BY course_name")

        col1, col2 = st.columns(2)
        with col1:
            student_opts = {row["name"]: row["student_id"]
                            for _, row in students_df.iterrows()}
            sel_student  = st.selectbox("Student", list(student_opts.keys()))
            sel_student_id = student_opts[sel_student]

            book_opts   = {row["title"]: (row["book_id"], row["price"])
                           for _, row in books_df.iterrows()}
            sel_book    = st.selectbox("Book", list(book_opts.keys()))
            sel_book_id, book_price = book_opts[sel_book]

        with col2:
            course_opts = {"(none — personal purchase)": None}
            course_opts.update({row["course_name"]: row["course_id"]
                                 for _, row in courses_df.iterrows()})
            sel_course    = st.selectbox("Course (optional)", list(course_opts.keys()))
            sel_course_id = course_opts[sel_course]

            import datetime
            purch_date = st.date_input("Purchase date", value=datetime.date.today())
            quantity   = st.number_input("Quantity", min_value=1, max_value=10, value=1)

        total_amount = round(book_price * quantity, 2)
        st.info(
            f"**Total amount:** {quantity} × ${book_price:.2f} = **${total_amount:.2f}**  "
            f"_(price locked at today's catalog value)_"
        )

        new_pid = next_id("purchases", "purchase_id")
        course_sql_val = "NULL" if sel_course_id is None else str(sel_course_id)

        insert_sql_p = (
            f"INSERT INTO purchases\n"
            f"    (purchase_id, student_id, book_id, course_id,\n"
            f"     purchase_date, quantity, total_amount)\n"
            f"VALUES\n"
            f"    ({new_pid}, {sel_student_id}, {sel_book_id}, {course_sql_val},\n"
            f"     '{purch_date}', {quantity}, {total_amount});"
        )

        st.markdown("**Generated SQL:**")
        st.code(insert_sql_p, language="sql")

        if st.button("▶ Run INSERT — Add Purchase", type="primary"):
            try:
                run_write(insert_sql_p.rstrip(";"))
                st.success(
                    f"✓ Purchase #{new_pid} added: **{sel_student}** bought "
                    f"*{sel_book}* for ${total_amount:.2f}."
                )
                st.balloons()
            except Exception as e:
                st.error(f"Insert failed: {e}")

        st.markdown("---")
        st.subheader("Recent Purchases")
        st.dataframe(
            run("""
                SELECT p.purchase_id, s.name AS student, b.title AS book,
                       p.purchase_date, p.quantity, p.total_amount
                FROM   purchases p
                JOIN   students s ON p.student_id = s.student_id
                JOIN   books    b ON p.book_id    = b.book_id
                ORDER  BY p.purchase_id DESC
                LIMIT  15
            """),
            use_container_width=True, hide_index=True,
        )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 · INDEX LAB
# ─────────────────────────────────────────────────────────────────────────────

elif page == "⚡ Index Lab":
    st.title("⚡ Index Lab")
    st.markdown(
        "An index lets the database find rows without scanning the entire table. "
        "This page lets you create and drop indexes, then time the same query "
        "with and without them."
    )

    # ── Index status ──────────────────────────────────────────────────────────
    def index_exists(name: str) -> bool:
        result = run(f"""
            SELECT COUNT(*) AS n FROM duckdb_indexes()
            WHERE index_name = '{name}'
        """)
        return int(result.iloc[0]["n"]) > 0

    INDEXES = {
        "idx_purchases_student": ("purchases", "student_id"),
        "idx_purchases_book":    ("purchases", "book_id"),
        "idx_purchases_date":    ("purchases", "purchase_date"),
    }

    st.subheader("📋 Index Status")
    idx_col1, idx_col2, idx_col3 = st.columns(3)
    for col, (idx_name, (tbl, col_name)) in zip(
        [idx_col1, idx_col2, idx_col3], INDEXES.items()
    ):
        exists = index_exists(idx_name)
        col.metric(
            label=f"`{tbl}({col_name})`",
            value="✅ EXISTS" if exists else "❌ MISSING",
        )
        if exists:
            if col.button(f"DROP {idx_name}", key=f"drop_{idx_name}"):
                run_write(f"DROP INDEX IF EXISTS {idx_name}")
                st.rerun()
        else:
            if col.button(f"CREATE {idx_name}", key=f"create_{idx_name}"):
                run_write(
                    f"CREATE INDEX {idx_name} ON {tbl}({col_name})"
                )
                st.rerun()

    st.markdown("---")

    # ── Query timing ──────────────────────────────────────────────────────────
    st.subheader("⏱️ Query Timing — Before vs After Index")

    TIMED_QUERIES = {
        "Find all purchases by a student  (uses student_id)": {
            "sql": "SELECT * FROM purchases WHERE student_id = 1",
            "index": "idx_purchases_student",
            "col":   "student_id",
            "table": "purchases",
        },
        "Find all purchases of a book  (uses book_id)": {
            "sql": "SELECT * FROM purchases WHERE book_id = 1",
            "index": "idx_purchases_book",
            "col":   "book_id",
            "table": "purchases",
        },
        "Find purchases in a date range  (uses purchase_date)": {
            "sql": "SELECT * FROM purchases WHERE purchase_date BETWEEN '2025-09-01' AND '2025-12-31'",
            "index": "idx_purchases_date",
            "col":   "purchase_date",
            "table": "purchases",
        },
    }

    chosen = st.selectbox("Choose a query to time", list(TIMED_QUERIES.keys()))
    q = TIMED_QUERIES[chosen]
    runs = st.slider("Number of repetitions (more = more stable measurement)",
                     50, 1000, 300, 50)

    st.code(q["sql"], language="sql")

    def time_query(sql: str, n: int) -> float:
        con = duckdb.connect(DB_PATH)
        start = time.perf_counter()
        for _ in range(n):
            con.execute(sql).fetchall()
        elapsed = time.perf_counter() - start
        con.close()
        return (elapsed / n) * 1_000  # ms per call

    if st.button("▶ Run Timing Comparison", type="primary"):
        idx_name = q["index"]
        exists_before = index_exists(idx_name)

        # Ensure no index for the "without" measurement
        if exists_before:
            run_write(f"DROP INDEX IF EXISTS {idx_name}")

        with st.spinner("Timing without index …"):
            t_without = time_query(q["sql"], runs)

        # Create index for the "with" measurement
        run_write(f"CREATE INDEX {idx_name} ON {q['table']}({q['col']})")

        with st.spinner("Timing with index …"):
            t_with = time_query(q["sql"], runs)

        # Restore original state
        if not exists_before:
            run_write(f"DROP INDEX IF EXISTS {idx_name}")

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Without index", f"{t_without:.4f} ms / query")
        c2.metric("With index",    f"{t_with:.4f} ms / query",
                  delta=f"{t_with - t_without:.4f} ms",
                  delta_color="inverse")
        speedup = t_without / t_with if t_with > 0 else 1.0
        c3.metric("Speedup", f"{speedup:.1f}×")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Without index — SQL executed:**")
            st.code(q["sql"], language="sql")
            st.markdown(
                "The database performs a **full table scan** — it reads every row "
                "in `purchases` and checks the condition one by one. "
                f"On {runs} repetitions this is measurably slower."
            )
        with col2:
            st.markdown("**With index — what changed under the hood:**")
            st.code(
                f"-- Index created before the test:\n"
                f"CREATE INDEX {idx_name}\n"
                f"ON {q['table']}({q['col']});\n\n"
                f"-- Same query — faster execution:\n"
                f"{q['sql']};",
                language="sql",
            )
            st.markdown(
                "The database uses the index as a sorted lookup structure — "
                "it jumps directly to the matching rows without scanning the whole table. "
                "The query is identical; only the *execution plan* changes."
            )

        if speedup < 1.2:
            st.info(
                "💡 The speedup is modest here because the table only has ~60 rows. "
                "On a table with millions of rows, the same index can make a query "
                "thousands of times faster — the difference grows with table size."
            )

    st.markdown("---")

    # ── EXPLAIN output ────────────────────────────────────────────────────────
    st.subheader("🔬 Query Execution Plan (EXPLAIN)")
    st.markdown(
        "DuckDB can show you *how* it plans to run a query before executing it. "
        "This is called the **execution plan** or **query plan**."
    )

    chosen_q = TIMED_QUERIES[chosen]["sql"]
    col_ex1, col_ex2 = st.columns(2)

    for col, idx_present, label in [
        (col_ex1, False, "Without index"),
        (col_ex2, True,  "With index"),
    ]:
        idx_name = TIMED_QUERIES[chosen]["index"]
        tbl      = TIMED_QUERIES[chosen]["table"]
        idx_col  = TIMED_QUERIES[chosen]["col"]
        with col:
            st.markdown(f"**{label}**")
            try:
                # Ensure correct index state for each plan
                con = duckdb.connect(DB_PATH)
                if idx_present:
                    con.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {tbl}({idx_col})")
                else:
                    con.execute(f"DROP INDEX IF EXISTS {idx_name}")
                plan_df = con.execute(f"EXPLAIN {chosen_q}").df()
                con.close()
                get_conn.clear()

                if not plan_df.empty:
                    # DuckDB returns columns: explain_key, explain_value
                    plan_text = "\n\n".join(
                        f"── {row['explain_key']} ──\n{row['explain_value']}"
                        for _, row in plan_df.iterrows()
                        if str(row.get("explain_value", "")).strip()
                    )
                    st.code(plan_text if plan_text else plan_df.to_string(index=False),
                            language="text")
                else:
                    st.info("No plan returned.")
            except Exception as e:
                st.warning(f"EXPLAIN error: {e}")

    st.caption(
        "Look for **SEQ_SCAN** (full table scan — no index) vs **INDEX_SCAN** "
        "(direct lookup via index). The query is identical; only the plan changes."
    )

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption("OMIS-105 · Santa Clara University · Leavey School of Business · Level 3 of 3")
