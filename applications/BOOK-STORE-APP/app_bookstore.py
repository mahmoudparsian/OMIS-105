"""
app_bookstore.py — SCU Bookstore Intelligence Platform
OMIS-105 · Santa Clara University · Leavey School of Business

A real-world bookstore management & analytics application powered by
DuckDB + Streamlit. Read-write: managers can record new purchases and
register new students. Every insight is one SQL query away.

Run:
    pip install streamlit duckdb pandas matplotlib
    streamlit run app_bookstore.py

Reset data anytime:
    python seed.py
"""

import os
import datetime
import duckdb
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# ── Paths & colours ────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "bookstore.duckdb")

BG    = "#0e1117"
CARD  = "#1e1e2e"
GRID  = "#2d2d3d"
TEXT  = "#f1f5f9"
MUTED = "#94a3b8"
C1    = "#6366f1"   # indigo  – CS / primary
C2    = "#10b981"   # emerald – EE / positive
C3    = "#f59e0b"   # amber   – BA / warning
C4    = "#ef4444"   # red     – alert / danger
C5    = "#3b82f6"   # blue    – ME
C6    = "#ec4899"   # pink    – English Lit

MAJOR_PAL = {
    "Computer Science":       C1,
    "Electrical Engineering": C2,
    "Business Analytics":     C3,
    "English Literature":     C6,
    "Mechanical Engineering": C5,
}
CAT_PAL = {"Textbook": C1, "Reference": C2, "Novel": C3}

# ── Page config ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SCU Bookstore Intelligence",
    page_icon="📚",
    layout="wide",
)

# ── Custom CSS for a polished look ─────────────────────────────────────────────

st.markdown("""
<style>
/* metric card value */
[data-testid="stMetricValue"] { font-size: 2rem !important; }
/* alert / info boxes */
.alert-red   { background:#2d0f0f; border-left:4px solid #ef4444;
               padding:12px 16px; border-radius:6px; margin:6px 0; }
.alert-amber { background:#2d1f0a; border-left:4px solid #f59e0b;
               padding:12px 16px; border-radius:6px; margin:6px 0; }
.alert-green { background:#0a2d1e; border-left:4px solid #10b981;
               padding:12px 16px; border-radius:6px; margin:6px 0; }
.insight     { background:#1a1a2e; border-left:4px solid #6366f1;
               padding:10px 14px; border-radius:6px; margin:4px 0;
               font-size:0.92rem; color:#cbd5e1; }
</style>
""", unsafe_allow_html=True)

# ── DB helpers ─────────────────────────────────────────────────────────────────

@st.cache_resource
def get_conn():
    return duckdb.connect(DB_PATH)

def run(sql: str) -> pd.DataFrame:
    return get_conn().execute(sql).df()

def run_write(sql: str):
    con = duckdb.connect(DB_PATH)
    con.execute(sql)
    con.close()
    get_conn.clear()

def next_id(table: str, pk: str) -> int:
    return int(run(f"SELECT COALESCE(MAX({pk}),0)+1 AS n FROM {table}").iloc[0]["n"])

# ── Chart factory ──────────────────────────────────────────────────────────────

def fig(w=12, h=4, ncols=1):
    f, axes = plt.subplots(1, ncols, figsize=(w, h))
    f.patch.set_facecolor(BG)
    axs = [axes] if ncols == 1 else list(axes)
    for ax in axs:
        ax.set_facecolor(CARD)
        for sp in ax.spines.values():
            sp.set_edgecolor(GRID)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.grid(axis="y", color=GRID, lw=0.5, alpha=0.6, zorder=0)
    return (f, axs[0]) if ncols == 1 else (f, axs)

def bar_labels(ax, bars, fmt="${:,.0f}", color=TEXT, fs=8):
    for b in bars:
        v = b.get_width() if hasattr(b, "get_width") and b.get_height() == 0 else b.get_height()
        # detect horizontal vs vertical
        if b.get_width() > b.get_height() * 10:
            ax.text(b.get_width() + 1, b.get_y() + b.get_height() / 2,
                    fmt.format(b.get_width()), va="center", color=color, fontsize=fs)
        else:
            ax.text(b.get_x() + b.get_width() / 2, v + 0.5,
                    fmt.format(v), ha="center", color=color, fontsize=fs)

def sql_box(sql: str, label: str = "View SQL behind this insight"):
    with st.expander(f"🔍 {label}"):
        st.code(sql.strip(), language="sql")

def insight(text: str):
    st.markdown(f'<div class="insight">💡 {text}</div>', unsafe_allow_html=True)

def alert_red(text: str):
    st.markdown(f'<div class="alert-red">🚨 {text}</div>', unsafe_allow_html=True)

def alert_amber(text: str):
    st.markdown(f'<div class="alert-amber">⚠️ {text}</div>', unsafe_allow_html=True)

def alert_green(text: str):
    st.markdown(f'<div class="alert-green">✅ {text}</div>', unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Santa_Clara_University_seal.svg/200px-Santa_Clara_University_seal.svg.png", width=72)
    st.markdown("## 📚 SCU Bookstore")
    st.caption("Intelligence Platform")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠  Executive Dashboard",
         "👥  Student Intelligence",
         "📖  Catalog & Inventory",
         "💰  Revenue Analytics",
         "✏️  Manager Actions",
         "🔬  SQL Playground"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    total_rev = run("SELECT ROUND(SUM(total_amount),2) AS t FROM purchases").iloc[0]["t"]
    n_students = run("SELECT COUNT(*) AS n FROM students").iloc[0]["n"]
    n_books    = run("SELECT COUNT(*) AS n FROM books").iloc[0]["n"]
    n_purch    = run("SELECT COUNT(*) AS n FROM purchases").iloc[0]["n"]
    st.metric("Total Revenue",  f"${total_rev:,.2f}")
    st.metric("Students",       f"{int(n_students)}")
    st.metric("Books in Catalog",f"{int(n_books)}")
    st.metric("Purchases",      f"{int(n_purch)}")
    st.markdown("---")
    st.caption(f"Database: `bookstore.duckdb`  \nRefreshed: {datetime.datetime.now().strftime('%H:%M:%S')}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 · EXECUTIVE DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

if page.startswith("🏠"):
    st.title("🏠 Executive Dashboard")
    st.caption("Real-time overview of bookstore operations — powered entirely by DuckDB SQL.")

    # ── KPIs ──────────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5, k6 = st.columns(6)

    active_buyers = int(run("SELECT COUNT(DISTINCT student_id) AS n FROM purchases").iloc[0]["n"])
    never_bought  = int(n_students) - active_buyers

    books_sold = int(run("""
        SELECT COUNT(DISTINCT book_id) AS n FROM purchases
    """).iloc[0]["n"])
    dead_stock = int(n_books) - books_sold

    avg_order = run("SELECT ROUND(AVG(total_amount),2) AS a FROM purchases").iloc[0]["a"]
    top_dept  = run("""
        SELECT c.department
        FROM purchases p JOIN courses c ON p.course_id = c.course_id
        GROUP BY c.department ORDER BY SUM(p.total_amount) DESC LIMIT 1
    """).iloc[0]["department"]

    k1.metric("💰 Total Revenue",    f"${total_rev:,.2f}")
    k2.metric("👥 Active Buyers",    f"{active_buyers} / {int(n_students)}",
              delta=f"{never_bought} never purchased", delta_color="inverse")
    k3.metric("📚 Books Sold",       f"{books_sold} / {int(n_books)}",
              delta=f"{dead_stock} never sold", delta_color="inverse")
    k4.metric("🛒 Total Purchases",  f"{int(n_purch)}")
    k5.metric("🧾 Avg Order Value",  f"${avg_order:,.2f}")
    k6.metric("🏆 Top Department",   top_dept)

    st.markdown("---")

    # ── Business Alerts ───────────────────────────────────────────────────────
    st.subheader("🚨 Business Alerts")
    col_a, col_b = st.columns(2)

    never_bought_df = run("""
        SELECT s.name, s.major, s.year,
               CASE s.year WHEN 1 THEN 'Freshman' WHEN 2 THEN 'Sophomore'
                           WHEN 3 THEN 'Junior'   ELSE 'Senior' END AS year_label,
               s.gpa
        FROM   students s
        LEFT   JOIN purchases p ON s.student_id = p.student_id
        WHERE  p.purchase_id IS NULL
        ORDER  BY s.name
    """)
    SQL_NEVER_BOUGHT = """
SELECT s.name, s.major, s.year, s.gpa
FROM   students s
LEFT   JOIN purchases p ON s.student_id = p.student_id
WHERE  p.purchase_id IS NULL   -- anti-join: no matching purchase
ORDER  BY s.name;"""

    dead_stock_df = run("""
        SELECT b.title, b.category, b.price, b.author
        FROM   books b
        LEFT   JOIN purchases p ON b.book_id = p.book_id
        WHERE  p.purchase_id IS NULL
        ORDER  BY b.category, b.price DESC
    """)
    SQL_DEAD_STOCK = """
SELECT b.title, b.category, b.price
FROM   books b
LEFT   JOIN purchases p ON b.book_id = p.book_id
WHERE  p.purchase_id IS NULL   -- anti-join: never purchased
ORDER  BY b.category, b.price DESC;"""

    with col_a:
        alert_red(f"<strong>{len(never_bought_df)} registered students have never made a purchase.</strong><br>"
                  f"These accounts are inactive — consider a targeted promotion or follow-up.")
        st.dataframe(never_bought_df[["name","major","year_label","gpa"]].rename(
            columns={"year_label":"Year"}), use_container_width=True, hide_index=True)
        sql_box(SQL_NEVER_BOUGHT, "LEFT JOIN anti-join: finding inactive students")

    with col_b:
        potential = dead_stock_df["price"].sum()
        alert_amber(f"<strong>{len(dead_stock_df)} books in the catalog have never been sold.</strong><br>"
                    f"Combined catalog value: ${potential:,.2f} in unrealised revenue.")
        st.dataframe(dead_stock_df[["title","category","price","author"]],
                     use_container_width=True, hide_index=True)
        sql_box(SQL_DEAD_STOCK, "LEFT JOIN anti-join: finding dead-stock books")

    st.markdown("---")

    # ── Monthly Revenue + Dept Revenue ────────────────────────────────────────
    st.subheader("📈 Revenue at a Glance")
    col1, col2 = st.columns([3, 2])

    monthly = run("""
        SELECT strftime(purchase_date,'%Y-%m') AS month,
               ROUND(SUM(total_amount),2)      AS revenue,
               COUNT(*)                         AS purchases
        FROM   purchases
        GROUP  BY month ORDER BY month
    """)
    SQL_MONTHLY = """
SELECT strftime(purchase_date,'%Y-%m') AS month,
       ROUND(SUM(total_amount),2)      AS revenue,
       COUNT(*)                        AS purchases
FROM   purchases
GROUP  BY month ORDER BY month;"""

    with col1:
        f1, ax1 = fig(9, 4)
        colors = [C2 if m.startswith("2026") else C1 for m in monthly["month"]]
        bars = ax1.bar(monthly["month"], monthly["revenue"], color=colors, edgecolor="none", zorder=3)
        ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax1.set_xticklabels(monthly["month"], rotation=35, ha="right", color=MUTED, fontsize=8)
        ax1.tick_params(axis="y", colors=MUTED)
        ax1.set_title("Monthly Revenue", color=TEXT, fontsize=11, pad=10)
        legend_els = [Patch(color=C1, label="Fall 2025"), Patch(color=C2, label="Spring 2026")]
        ax1.legend(handles=legend_els, facecolor=CARD, labelcolor=TEXT, fontsize=8)
        plt.tight_layout()
        st.pyplot(f1); plt.close(f1)
        sql_box(SQL_MONTHLY)

    dept_rev = run("""
        SELECT c.department                      AS dept,
               ROUND(SUM(p.total_amount),2)      AS revenue,
               COUNT(DISTINCT p.student_id)       AS students
        FROM   purchases p
        JOIN   courses c ON p.course_id = c.course_id
        GROUP  BY c.department
        ORDER  BY revenue DESC
    """)
    SQL_DEPT = """
SELECT c.department, ROUND(SUM(p.total_amount),2) AS revenue,
       COUNT(DISTINCT p.student_id) AS students
FROM   purchases p
JOIN   courses c ON p.course_id = c.course_id
GROUP  BY c.department ORDER BY revenue DESC;"""

    with col2:
        f2, ax2 = fig(6, 4)
        dept_colors = [MAJOR_PAL.get(d, MUTED) for d in dept_rev["dept"]]
        short_dept = [d.replace(" Engineering", " Eng.").replace(" Analytics", " Anal.") for d in dept_rev["dept"]]
        hbars = ax2.barh(short_dept[::-1], dept_rev["revenue"].values[::-1],
                         color=dept_colors[::-1], edgecolor="none", zorder=3)
        ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        for b in hbars:
            ax2.text(b.get_width() + 20, b.get_y() + b.get_height()/2,
                     f"${b.get_width():,.0f}", va="center", color=TEXT, fontsize=8)
        ax2.tick_params(colors=MUTED)
        ax2.grid(axis="x", color=GRID, lw=0.5, alpha=0.6)
        ax2.grid(axis="y", visible=False)
        ax2.set_title("Revenue by Department", color=TEXT, fontsize=11, pad=10)
        plt.tight_layout()
        st.pyplot(f2); plt.close(f2)
        sql_box(SQL_DEPT)

    st.markdown("---")

    # ── Smart Insights ────────────────────────────────────────────────────────
    st.subheader("💡 Smart Insights")

    top_student = run("""
        SELECT s.name, ROUND(SUM(p.total_amount),2) AS spent
        FROM purchases p JOIN students s ON p.student_id = s.student_id
        GROUP BY s.name ORDER BY spent DESC LIMIT 1
    """)
    avg_student_spend = run("""
        SELECT ROUND(AVG(t),2) AS a FROM (
            SELECT SUM(total_amount) AS t FROM purchases GROUP BY student_id)
    """).iloc[0]["a"]
    top_name  = top_student.iloc[0]["name"]
    top_spent = top_student.iloc[0]["spent"]
    multiplier = round(top_spent / avg_student_spend, 1)

    req_vs_opt = run("""
        SELECT CASE WHEN cb.required THEN 'Required' ELSE 'Optional' END AS book_type,
               ROUND(SUM(p.total_amount),2) AS revenue
        FROM   purchases p
        JOIN   course_books cb ON p.book_id=cb.book_id AND p.course_id=cb.course_id
        GROUP  BY cb.required
    """)
    req_rev = req_vs_opt[req_vs_opt["book_type"]=="Required"]["revenue"].values[0]
    opt_rev = req_vs_opt[req_vs_opt["book_type"]=="Optional"]["revenue"].values[0]

    fall_rev   = monthly[monthly["month"].str.startswith("2025")]["revenue"].sum()
    spring_rev = monthly[monthly["month"].str.startswith("2026")]["revenue"].sum()
    fall_pct   = round(fall_rev / (fall_rev + spring_rev) * 100)

    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        insight(f"<strong>{top_name}</strong> is your top customer — ${top_spent:,.2f} spent, "
                f"<strong>{multiplier}×</strong> the average buyer.")
    with ic2:
        insight(f"Required books generate <strong>${req_rev:,.2f}</strong> vs ${opt_rev:,.2f} for optional — "
                f"textbook pricing drives revenue.")
    with ic3:
        insight(f"Fall semester accounts for <strong>{fall_pct}%</strong> of annual revenue "
                f"(${fall_rev:,.2f} vs ${spring_rev:,.2f}). Rush season is real.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 · STUDENT INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════

elif page.startswith("👥"):
    st.title("👥 Student Intelligence")
    st.caption("Who's buying, who's spending the most — and who isn't buying at all.")

    # ── Leaderboard ───────────────────────────────────────────────────────────
    st.subheader("🏆 Customer Spending Leaderboard")

    leaderboard = run("""
        SELECT ROW_NUMBER() OVER (ORDER BY SUM(p.total_amount) DESC) AS rank,
               s.name, s.major,
               CASE s.year WHEN 1 THEN 'Freshman' WHEN 2 THEN 'Sophomore'
                           WHEN 3 THEN 'Junior'   ELSE 'Senior' END AS year,
               COUNT(*)                        AS purchases,
               ROUND(SUM(p.total_amount),2)    AS total_spent,
               ROUND(AVG(p.total_amount),2)    AS avg_per_order
        FROM   purchases p
        JOIN   students s ON p.student_id = s.student_id
        GROUP  BY s.name, s.major, s.year
        ORDER  BY total_spent DESC
    """)
    SQL_LEADERBOARD = """
SELECT ROW_NUMBER() OVER (ORDER BY SUM(p.total_amount) DESC) AS rank,
       s.name, s.major,
       COUNT(*)                     AS purchases,
       ROUND(SUM(p.total_amount),2) AS total_spent,
       ROUND(AVG(p.total_amount),2) AS avg_per_order
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.name, s.major, s.year
ORDER  BY total_spent DESC;"""

    col1, col2 = st.columns([2, 3])
    with col1:
        st.dataframe(leaderboard, use_container_width=True, hide_index=True)
        sql_box(SQL_LEADERBOARD)

    with col2:
        f3, ax3 = fig(8, 5)
        lb = leaderboard.sort_values("total_spent")
        colors = [MAJOR_PAL.get(m, MUTED) for m in lb["major"]]
        hb = ax3.barh(lb["name"], lb["total_spent"], color=colors, edgecolor="none", zorder=3)
        for b in hb:
            ax3.text(b.get_width() + 5, b.get_y() + b.get_height()/2,
                     f"${b.get_width():,.0f}", va="center", color=TEXT, fontsize=8.5)
        ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax3.tick_params(colors=MUTED)
        ax3.grid(axis="x", color=GRID, lw=0.5, alpha=0.6)
        ax3.grid(axis="y", visible=False)
        seen = {}
        for m, c in zip(lb["major"], colors):
            seen[m] = c
        ax3.legend([Patch(color=c) for c in seen.values()], list(seen.keys()),
                   facecolor=CARD, labelcolor=TEXT, fontsize=8, loc="lower right")
        ax3.set_title("Total Spend per Student  (window: ROW_NUMBER + SUM)",
                      color=TEXT, fontsize=10, pad=10)
        plt.tight_layout()
        st.pyplot(f3); plt.close(f3)

    st.markdown("---")

    # ── Never-purchased alert ─────────────────────────────────────────────────
    st.subheader("🚨 Inactive Accounts — Never Purchased")
    alert_red("The following students have registered accounts but have <strong>zero purchases</strong>. "
              "This is detected with a single LEFT JOIN anti-join — something impossible to do efficiently in a spreadsheet.")

    inactive = run("""
        SELECT s.student_id, s.name, s.email, s.major,
               CASE s.year WHEN 1 THEN 'Freshman' WHEN 2 THEN 'Sophomore'
                           WHEN 3 THEN 'Junior'   ELSE 'Senior' END AS year,
               s.gpa
        FROM   students s
        LEFT   JOIN purchases p ON s.student_id = p.student_id
        WHERE  p.purchase_id IS NULL
        ORDER  BY s.name
    """)
    SQL_INACTIVE = """
-- Classic LEFT JOIN anti-join pattern
-- "Give me everything from the left table that has NO match on the right"
SELECT s.student_id, s.name, s.email, s.major, s.year, s.gpa
FROM   students s
LEFT   JOIN purchases p ON s.student_id = p.student_id
WHERE  p.purchase_id IS NULL   -- ← the anti-join condition
ORDER  BY s.name;"""

    st.dataframe(inactive, use_container_width=True, hide_index=True)
    sql_box(SQL_INACTIVE, "The LEFT JOIN anti-join — one of the most powerful SQL patterns")

    st.markdown("---")

    # ── By major & by year ────────────────────────────────────────────────────
    st.subheader("📊 Spending Patterns")
    col3, col4 = st.columns(2)

    by_major = run("""
        SELECT s.major,
               COUNT(DISTINCT p.student_id)       AS active_students,
               ROUND(SUM(p.total_amount),2)       AS total_revenue,
               ROUND(AVG(p.total_amount),2)       AS avg_per_purchase,
               ROUND(SUM(p.total_amount)
                     / COUNT(DISTINCT p.student_id),2) AS revenue_per_student
        FROM   purchases p
        JOIN   students s ON p.student_id = s.student_id
        GROUP  BY s.major
        ORDER  BY total_revenue DESC
    """)
    SQL_MAJOR = """
SELECT s.major,
       COUNT(DISTINCT p.student_id)            AS active_students,
       ROUND(SUM(p.total_amount),2)            AS total_revenue,
       ROUND(SUM(p.total_amount)
             / COUNT(DISTINCT p.student_id),2) AS revenue_per_student
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.major ORDER BY total_revenue DESC;"""

    with col3:
        f4, ax4 = fig(6, 4)
        maj_cols = [MAJOR_PAL.get(m, MUTED) for m in by_major["major"]]
        short = [m.replace(" Engineering","").replace(" Analytics","").replace(" Literature","") for m in by_major["major"]]
        ax4.bar(short, by_major["total_revenue"], color=maj_cols, edgecolor="none", zorder=3)
        ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax4.tick_params(axis="x", colors=MUTED, rotation=15)
        ax4.tick_params(axis="y", colors=MUTED)
        ax4.set_title("Total Revenue by Major", color=TEXT, fontsize=11, pad=10)
        plt.tight_layout()
        st.pyplot(f4); plt.close(f4)
        st.dataframe(by_major, use_container_width=True, hide_index=True)
        sql_box(SQL_MAJOR)

    by_year = run("""
        SELECT CASE s.year WHEN 1 THEN '1 · Freshman' WHEN 2 THEN '2 · Sophomore'
                           WHEN 3 THEN '3 · Junior'   ELSE '4 · Senior' END AS yr,
               COUNT(*)                        AS purchases,
               ROUND(SUM(p.total_amount),2)    AS total_spent,
               ROUND(AVG(p.total_amount),2)    AS avg_per_order
        FROM   purchases p
        JOIN   students s ON p.student_id = s.student_id
        GROUP  BY s.year, yr
        ORDER  BY s.year
    """)
    SQL_YEAR = """
SELECT s.year,
       COUNT(*)                     AS purchases,
       ROUND(SUM(p.total_amount),2) AS total_spent,
       ROUND(AVG(p.total_amount),2) AS avg_per_order
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.year ORDER BY s.year;"""

    with col4:
        f5, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(6, 4))
        f5.patch.set_facecolor(BG)
        for ax in (ax5a, ax5b):
            ax.set_facecolor(CARD)
            for sp in ax.spines.values(): sp.set_edgecolor(GRID)
            ax.tick_params(colors=MUTED, labelsize=8)
            ax.grid(axis="y", color=GRID, lw=0.5, alpha=0.6)
        yr_colors = [C5, C1, C3, C2]
        ax5a.bar(by_year["yr"], by_year["total_spent"],
                 color=yr_colors[:len(by_year)], edgecolor="none", zorder=3)
        ax5a.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax5a.set_xticklabels(by_year["yr"], rotation=30, ha="right", fontsize=7)
        ax5a.set_title("Total Spend", color=TEXT, fontsize=9, pad=6)
        ax5b.bar(by_year["yr"], by_year["avg_per_order"],
                 color=yr_colors[:len(by_year)], edgecolor="none", zorder=3)
        ax5b.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax5b.set_xticklabels(by_year["yr"], rotation=30, ha="right", fontsize=7)
        ax5b.set_title("Avg per Order", color=TEXT, fontsize=9, pad=6)
        f5.suptitle("Spending by Academic Year", color=TEXT, fontsize=10)
        plt.tight_layout()
        st.pyplot(f5); plt.close(f5)
        st.dataframe(by_year, use_container_width=True, hide_index=True)
        sql_box(SQL_YEAR)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 · CATALOG & INVENTORY
# ══════════════════════════════════════════════════════════════════════════════

elif page.startswith("📖"):
    st.title("📖 Catalog & Inventory")
    st.caption("Every book — what's selling, what's sitting, and what each title has earned.")

    # ── Full catalog with stats ───────────────────────────────────────────────
    st.subheader("📋 Full Catalog Performance")

    catalog = run("""
        SELECT b.title, b.author, b.category, b.price,
               COALESCE(COUNT(p.purchase_id),0)    AS times_purchased,
               COALESCE(ROUND(SUM(p.total_amount),2),0) AS total_revenue,
               CASE WHEN COUNT(p.purchase_id) = 0
                    THEN '🔴 Never Sold'
                    ELSE '🟢 Active' END            AS status
        FROM   books b
        LEFT   JOIN purchases p ON b.book_id = p.book_id
        GROUP  BY b.book_id, b.title, b.author, b.category, b.price
        ORDER  BY total_revenue DESC
    """)
    SQL_CATALOG = """
SELECT b.title, b.author, b.category, b.price,
       COALESCE(COUNT(p.purchase_id), 0)         AS times_purchased,
       COALESCE(ROUND(SUM(p.total_amount), 2), 0) AS total_revenue,
       CASE WHEN COUNT(p.purchase_id) = 0
            THEN 'Never Sold' ELSE 'Active' END   AS status
FROM   books b
LEFT   JOIN purchases p ON b.book_id = p.book_id
GROUP  BY b.book_id, b.title, b.author, b.category, b.price
ORDER  BY total_revenue DESC;"""

    st.dataframe(catalog, use_container_width=True, hide_index=True,
                 column_config={
                     "price":         st.column_config.NumberColumn("Price",          format="$%.2f"),
                     "total_revenue": st.column_config.NumberColumn("Total Revenue",  format="$%.2f"),
                     "times_purchased": st.column_config.NumberColumn("Times Sold"),
                 })
    sql_box(SQL_CATALOG, "LEFT JOIN to compute purchase stats for every book including unsold ones")

    st.markdown("---")

    # ── Dead stock alert ──────────────────────────────────────────────────────
    st.subheader("🚨 Dead Stock — Books Never Sold")
    dead = catalog[catalog["times_purchased"] == 0]
    potential = dead["price"].sum()
    alert_amber(f"<strong>{len(dead)} books have zero sales.</strong> "
                f"Combined list price: <strong>${potential:,.2f}</strong>. "
                f"Consider promotions, course adoption, or price adjustments.")
    st.dataframe(dead[["title","author","category","price","status"]],
                 use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Charts ────────────────────────────────────────────────────────────────
    st.subheader("📊 Catalog Analytics")
    col1, col2 = st.columns(2)

    with col1:
        # Top 10 by revenue
        top10 = catalog[catalog["total_revenue"] > 0].head(10).sort_values("total_revenue")
        f6, ax6 = fig(7, 5)
        bar_colors = [CAT_PAL.get(c, MUTED) for c in top10["category"]]
        hb = ax6.barh(
            [t[:30]+"…" if len(t)>30 else t for t in top10["title"]],
            top10["total_revenue"], color=bar_colors, edgecolor="none", zorder=3
        )
        for b in hb:
            ax6.text(b.get_width()+5, b.get_y()+b.get_height()/2,
                     f"${b.get_width():,.0f}", va="center", color=TEXT, fontsize=7.5)
        ax6.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax6.tick_params(colors=MUTED)
        ax6.grid(axis="x", color=GRID, lw=0.5, alpha=0.6)
        ax6.grid(axis="y", visible=False)
        legend_els = [Patch(color=c, label=cat) for cat, c in CAT_PAL.items()]
        ax6.legend(handles=legend_els, facecolor=CARD, labelcolor=TEXT, fontsize=8)
        ax6.set_title("Top 10 Books by Revenue", color=TEXT, fontsize=11, pad=10)
        plt.tight_layout()
        st.pyplot(f6); plt.close(f6)

    with col2:
        # Category breakdown — active vs dead stock
        cat_stats = run("""
            SELECT b.category,
                   SUM(CASE WHEN p.purchase_id IS NOT NULL THEN 1 ELSE 0 END) AS sold,
                   SUM(CASE WHEN p.purchase_id IS NULL     THEN 1 ELSE 0 END) AS never_sold
            FROM   books b
            LEFT   JOIN purchases p ON b.book_id = p.book_id
            GROUP  BY b.category, b.book_id
        """)
        cat_agg = cat_stats.groupby("category").agg(
            sold=("sold","sum"), never_sold=("never_sold","sum")
        ).reset_index()
        # simplify: count distinct books per status
        cat_counts = run("""
            SELECT b.category,
                   COUNT(DISTINCT b.book_id)                                           AS total_books,
                   COUNT(DISTINCT CASE WHEN p.purchase_id IS NOT NULL THEN b.book_id END) AS sold_books,
                   COUNT(DISTINCT CASE WHEN p.purchase_id IS NULL     THEN b.book_id END) AS unsold_books
            FROM   books b
            LEFT   JOIN purchases p ON b.book_id = p.book_id
            GROUP  BY b.category ORDER BY total_books DESC
        """)
        SQL_CAT = """
SELECT b.category,
       COUNT(DISTINCT b.book_id)  AS total_books,
       COUNT(DISTINCT CASE WHEN p.purchase_id IS NOT NULL
                           THEN b.book_id END) AS sold_books,
       COUNT(DISTINCT CASE WHEN p.purchase_id IS NULL
                           THEN b.book_id END) AS unsold_books
FROM   books b
LEFT   JOIN purchases p ON b.book_id = p.book_id
GROUP  BY b.category;"""

        f7, ax7 = fig(7, 5)
        x = range(len(cat_counts))
        w = 0.35
        ax7.bar([i - w/2 for i in x], cat_counts["sold_books"],   width=w,
                label="Sold", color=C2, edgecolor="none", zorder=3)
        ax7.bar([i + w/2 for i in x], cat_counts["unsold_books"], width=w,
                label="Never Sold", color=C4, edgecolor="none", zorder=3, alpha=0.85)
        ax7.set_xticks(list(x))
        ax7.set_xticklabels(cat_counts["category"], color=MUTED, fontsize=9)
        ax7.tick_params(axis="y", colors=MUTED)
        ax7.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        ax7.legend(facecolor=CARD, labelcolor=TEXT, fontsize=9)
        ax7.set_title("Books Sold vs Never Sold by Category", color=TEXT, fontsize=11, pad=10)
        plt.tight_layout()
        st.pyplot(f7); plt.close(f7)
        sql_box(SQL_CAT)

    st.markdown("---")

    # ── Price vs Revenue scatter ──────────────────────────────────────────────
    st.subheader("💹 Price vs Revenue — Every Book")
    f8, ax8 = fig(12, 4)
    for cat, grp in catalog.groupby("category"):
        color = CAT_PAL.get(cat, MUTED)
        sold   = grp[grp["total_revenue"] > 0]
        unsold = grp[grp["total_revenue"] == 0]
        ax8.scatter(sold["price"], sold["total_revenue"], color=color,
                    s=sold["times_purchased"]*30+40, alpha=0.8, label=cat, zorder=3)
        ax8.scatter(unsold["price"], unsold["total_revenue"], color=C4,
                    s=60, marker="x", linewidths=2, zorder=4)
    ax8.axhline(0, color=GRID, lw=1)
    ax8.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax8.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax8.tick_params(colors=MUTED)
    ax8.set_xlabel("List Price", color=MUTED, fontsize=9)
    ax8.set_ylabel("Total Revenue Earned", color=MUTED, fontsize=9)
    legend_els = [Patch(color=c, label=cat) for cat, c in CAT_PAL.items()]
    legend_els.append(Line2D([0],[0], marker="x", color=C4, lw=0, markersize=8,
                              markeredgewidth=2, label="Never Sold"))
    ax8.legend(handles=legend_els, facecolor=CARD, labelcolor=TEXT, fontsize=9)
    ax8.set_title("Price vs Revenue  (bubble size = times purchased,  ✕ = never sold)",
                  color=TEXT, fontsize=11, pad=10)
    plt.tight_layout()
    st.pyplot(f8); plt.close(f8)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 · REVENUE ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════

elif page.startswith("💰"):
    st.title("💰 Revenue Analytics")
    st.caption("Deep-dive into revenue trends, seasonality, and what's driving the numbers.")

    # ── Cumulative revenue ────────────────────────────────────────────────────
    st.subheader("📈 Cumulative Revenue — All Time")

    cumulative = run("""
        SELECT purchase_date,
               ROUND(SUM(total_amount),2)                                  AS daily_rev,
               ROUND(SUM(SUM(total_amount)) OVER (ORDER BY purchase_date),2) AS cumulative
        FROM   purchases
        GROUP  BY purchase_date
        ORDER  BY purchase_date
    """)
    SQL_CUMUL = """
SELECT purchase_date,
       ROUND(SUM(total_amount), 2)                                   AS daily_rev,
       ROUND(SUM(SUM(total_amount)) OVER (ORDER BY purchase_date), 2) AS cumulative
FROM   purchases
GROUP  BY purchase_date
ORDER  BY purchase_date;"""

    f9, ax9 = fig(12, 4)
    dates = pd.to_datetime(cumulative["purchase_date"])
    ax9.fill_between(dates, cumulative["cumulative"], alpha=0.25, color=C1)
    ax9.plot(dates, cumulative["cumulative"], color=C1, lw=2.5, label="Cumulative Revenue")
    ax9.bar(dates, cumulative["daily_rev"], color=C2, alpha=0.6, width=1.5, label="Daily Revenue")
    ax9.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax9.tick_params(axis="x", colors=MUTED, rotation=30)
    ax9.tick_params(axis="y", colors=MUTED)
    final = cumulative["cumulative"].iloc[-1]
    ax9.annotate(f"  ${final:,.2f}", xy=(dates.iloc[-1], final),
                 color=C1, fontsize=10, fontweight="bold")
    ax9.legend(facecolor=CARD, labelcolor=TEXT, fontsize=9, loc="upper left")
    ax9.set_title("Cumulative Revenue  (window function: SUM OVER ORDER BY date)",
                  color=TEXT, fontsize=11, pad=10)
    plt.tight_layout()
    st.pyplot(f9); plt.close(f9)
    sql_box(SQL_CUMUL, "Window function: running total with SUM OVER ORDER BY")

    st.markdown("---")

    # ── Fall vs Spring + Required vs Optional ─────────────────────────────────
    st.subheader("📊 Revenue Breakdown")
    col1, col2 = st.columns(2)

    sem_detail = run("""
        SELECT c.semester,
               ROUND(SUM(p.total_amount),2)      AS revenue,
               COUNT(*)                           AS purchases,
               COUNT(DISTINCT p.student_id)       AS students,
               ROUND(AVG(p.total_amount),2)       AS avg_order
        FROM   purchases p
        JOIN   courses c ON p.course_id = c.course_id
        GROUP  BY c.semester
        ORDER  BY c.semester
    """)
    SQL_SEM = """
SELECT c.semester,
       ROUND(SUM(p.total_amount),2) AS revenue,
       COUNT(*)                     AS purchases,
       COUNT(DISTINCT p.student_id) AS students,
       ROUND(AVG(p.total_amount),2) AS avg_order
FROM   purchases p
JOIN   courses c ON p.course_id = c.course_id
GROUP  BY c.semester ORDER BY c.semester;"""

    with col1:
        f10, ax10 = fig(6, 4)
        sem_colors = [C1, C2]
        bars10 = ax10.bar(sem_detail["semester"], sem_detail["revenue"],
                          color=sem_colors, edgecolor="none", zorder=3)
        for b in bars10:
            ax10.text(b.get_x()+b.get_width()/2, b.get_height()+30,
                      f"${b.get_height():,.0f}", ha="center", color=TEXT, fontsize=10, fontweight="bold")
        ax10.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax10.tick_params(colors=MUTED)
        ax10.set_title("Revenue: Fall vs Spring", color=TEXT, fontsize=11, pad=10)
        plt.tight_layout()
        st.pyplot(f10); plt.close(f10)
        st.dataframe(sem_detail, use_container_width=True, hide_index=True)
        sql_box(SQL_SEM)

    req_opt = run("""
        SELECT CASE WHEN cb.required THEN 'Required' ELSE 'Optional' END AS book_type,
               COUNT(*)                        AS purchases,
               ROUND(SUM(p.total_amount),2)    AS revenue,
               ROUND(AVG(p.total_amount),2)    AS avg_price
        FROM   purchases p
        JOIN   course_books cb ON p.book_id=cb.book_id AND p.course_id=cb.course_id
        GROUP  BY cb.required
        ORDER  BY revenue DESC
    """)
    SQL_REQ = """
SELECT CASE WHEN cb.required THEN 'Required' ELSE 'Optional' END AS book_type,
       COUNT(*)                     AS purchases,
       ROUND(SUM(p.total_amount),2) AS revenue,
       ROUND(AVG(p.total_amount),2) AS avg_price
FROM   purchases p
JOIN   course_books cb ON p.book_id  = cb.book_id
                      AND p.course_id = cb.course_id
GROUP  BY cb.required ORDER BY revenue DESC;"""

    with col2:
        f11, (ax11a, ax11b) = plt.subplots(1, 2, figsize=(6, 4))
        f11.patch.set_facecolor(BG)
        pie_colors = [C1, C3]
        ax11a.pie(req_opt["purchases"], labels=req_opt["book_type"],
                  colors=pie_colors, autopct="%1.0f%%", startangle=90,
                  textprops={"color": TEXT, "fontsize": 9})
        ax11a.set_title("Purchases", color=TEXT, fontsize=9)
        ax11b.pie(req_opt["revenue"], labels=req_opt["book_type"],
                  colors=pie_colors, autopct="%1.0f%%", startangle=90,
                  textprops={"color": TEXT, "fontsize": 9})
        ax11b.set_title("Revenue", color=TEXT, fontsize=9)
        f11.patch.set_facecolor(BG)
        f11.suptitle("Required vs Optional — Purchases & Revenue", color=TEXT, fontsize=10)
        plt.tight_layout()
        st.pyplot(f11); plt.close(f11)
        st.dataframe(req_opt, use_container_width=True, hide_index=True)
        sql_box(SQL_REQ)

    st.markdown("---")

    # ── Revenue per student (window) ──────────────────────────────────────────
    st.subheader("🎯 Revenue per Student vs Major Average")

    per_student = run("""
        SELECT s.name, s.major,
               ROUND(SUM(p.total_amount),2)                          AS student_total,
               ROUND(AVG(SUM(p.total_amount)) OVER (PARTITION BY s.major),2) AS major_avg,
               ROUND(SUM(p.total_amount)
                   - AVG(SUM(p.total_amount)) OVER (PARTITION BY s.major),2) AS vs_avg
        FROM   purchases p
        JOIN   students s ON p.student_id = s.student_id
        GROUP  BY s.name, s.major
        ORDER  BY s.major, student_total DESC
    """)
    SQL_PER_STUDENT = """
SELECT s.name, s.major,
       ROUND(SUM(p.total_amount),2)                                AS student_total,
       ROUND(AVG(SUM(p.total_amount)) OVER (PARTITION BY s.major),2) AS major_avg,
       ROUND(SUM(p.total_amount)
           - AVG(SUM(p.total_amount)) OVER (PARTITION BY s.major),2) AS vs_avg
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.name, s.major
ORDER  BY s.major, student_total DESC;"""

    f12, ax12 = fig(12, 4)
    bar_cols12 = ["#10b981" if v >= 0 else "#ef4444" for v in per_student["vs_avg"]]
    ax12.bar(range(len(per_student)), per_student["student_total"],
             color=bar_cols12, edgecolor="none", zorder=3)
    # Major avg lines
    for major, grp in per_student.groupby("major", sort=False):
        idxs = [list(per_student.index).index(i) for i in grp.index]
        avg_val = grp["major_avg"].iloc[0]
        ax12.hlines(avg_val, min(idxs)-0.4, max(idxs)+0.4, colors=C3, lw=2, ls="--")
        ax12.text(max(idxs)+0.5, avg_val, f"${avg_val:,.0f}", color=C3, fontsize=7.5, va="center")
    ax12.set_xticks(range(len(per_student)))
    ax12.set_xticklabels(
        [f"{n.split()[0]}" for n in per_student["name"]], color=MUTED, fontsize=8, rotation=30
    )
    ax12.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax12.tick_params(axis="y", colors=MUTED)
    legend_els = [Patch(color=C2, label="Above major avg"),
                  Patch(color=C4, label="Below major avg"),
                  Line2D([0],[0], color=C3, lw=2, ls="--", label="Major average")]
    ax12.legend(handles=legend_els, facecolor=CARD, labelcolor=TEXT, fontsize=8, loc="upper right")
    ax12.set_title("Student Spend vs Their Major Average  (AVG OVER PARTITION BY major)",
                   color=TEXT, fontsize=11, pad=10)
    plt.tight_layout()
    st.pyplot(f12); plt.close(f12)
    st.dataframe(per_student, use_container_width=True, hide_index=True)
    sql_box(SQL_PER_STUDENT, "Window function: AVG OVER PARTITION BY — each student vs their major's average")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 · MANAGER ACTIONS  (read-write)
# ══════════════════════════════════════════════════════════════════════════════

elif page.startswith("✏️"):
    st.title("✏️ Manager Actions")
    st.caption("Record new purchases, register new students. Every write shows the exact SQL executed.")

    tab1, tab2, tab3 = st.tabs(["🛒 Record a Purchase", "🎓 Register a Student", "🔄 Recent Activity"])

    # ── Tab 1: New purchase ───────────────────────────────────────────────────
    with tab1:
        st.subheader("Record a New Purchase")
        st.markdown("Select the student and book, choose an optional course, and the system "
                    "computes `total_amount` from the catalog price — locking it at today's value.")

        students_df = run("SELECT student_id, name FROM students ORDER BY name")
        books_df    = run("SELECT book_id, title, price FROM books ORDER BY title")
        courses_df  = run("SELECT course_id, course_name FROM courses ORDER BY course_name")

        col1, col2 = st.columns(2)
        with col1:
            s_opts = {r["name"]: r["student_id"] for _, r in students_df.iterrows()}
            sel_s  = st.selectbox("Student", list(s_opts.keys()))
            sid    = s_opts[sel_s]

            b_opts = {r["title"]: (r["book_id"], r["price"]) for _, r in books_df.iterrows()}
            sel_b  = st.selectbox("Book", list(b_opts.keys()))
            bid, bprice = b_opts[sel_b]

        with col2:
            c_opts = {"(none — personal purchase)": None}
            c_opts.update({r["course_name"]: r["course_id"] for _, r in courses_df.iterrows()})
            sel_c  = st.selectbox("Course (optional)", list(c_opts.keys()))
            cid    = c_opts[sel_c]

            pdate = st.date_input("Purchase date", value=datetime.date.today())
            qty   = st.number_input("Quantity", min_value=1, max_value=10, value=1)

        total = round(bprice * qty, 2)
        st.info(f"**Total amount:** {qty} × ${bprice:.2f} = **${total:.2f}**")

        new_pid = next_id("purchases", "purchase_id")
        cid_sql = "NULL" if cid is None else str(cid)
        insert_sql = (
            f"INSERT INTO purchases\n"
            f"    (purchase_id, student_id, book_id, course_id,\n"
            f"     purchase_date, quantity, total_amount)\n"
            f"VALUES ({new_pid}, {sid}, {bid}, {cid_sql},\n"
            f"        '{pdate}', {qty}, {total});"
        )
        st.code(insert_sql, language="sql")

        if st.button("▶ Record Purchase", type="primary"):
            try:
                run_write(insert_sql.rstrip(";"))
                alert_green(f"Purchase #{new_pid} recorded — <strong>{sel_s}</strong> bought "
                            f"<em>{sel_b}</em> for <strong>${total:.2f}</strong>.")
                st.balloons()
            except Exception as e:
                alert_red(f"Insert failed: {e}")

    # ── Tab 2: New student ────────────────────────────────────────────────────
    with tab2:
        st.subheader("Register a New Student")

        col1, col2 = st.columns(2)
        with col1:
            new_name  = st.text_input("Full name", placeholder="e.g. Sofia Reyes")
            new_email = st.text_input("SCU email", placeholder="e.g. sreyes@scu.edu")
            new_major = st.selectbox("Major", [
                "Computer Science", "Electrical Engineering",
                "Business Analytics", "English Literature",
                "Mechanical Engineering", "Other"])
        with col2:
            new_year = st.selectbox("Year", [1,2,3,4],
                                    format_func=lambda x: {1:"Freshman",2:"Sophomore",
                                                            3:"Junior",4:"Senior"}[x])
            new_gpa  = st.slider("GPA", 0.0, 4.0, 3.5, 0.01)

        new_sid = next_id("students", "student_id")
        reg_sql = (
            f"INSERT INTO students\n"
            f"    (student_id, name, email, major, year, gpa)\n"
            f"VALUES ({new_sid}, '{new_name}', '{new_email}',\n"
            f"        '{new_major}', {new_year}, {new_gpa});"
        )
        st.code(reg_sql, language="sql")

        if st.button("▶ Register Student", type="primary"):
            if not new_name.strip():
                alert_red("Please enter a name.")
            elif "@" not in new_email:
                alert_red("Please enter a valid SCU email address.")
            else:
                try:
                    run_write(reg_sql.rstrip(";"))
                    alert_green(f"Student <strong>{new_name}</strong> registered "
                                f"with ID {new_sid}.")
                    st.balloons()
                except Exception as e:
                    alert_red(f"Registration failed: {e}")

    # ── Tab 3: Recent activity ────────────────────────────────────────────────
    with tab3:
        st.subheader("Recent Purchases")
        recent = run("""
            SELECT p.purchase_id,
                   s.name          AS student,
                   b.title         AS book,
                   c.course_name   AS course,
                   p.purchase_date,
                   p.quantity,
                   p.total_amount
            FROM   purchases p
            JOIN   students s ON p.student_id = s.student_id
            JOIN   books    b ON p.book_id    = b.book_id
            LEFT   JOIN courses c ON p.course_id = c.course_id
            ORDER  BY p.purchase_id DESC
            LIMIT  25
        """)
        SQL_RECENT = """
SELECT p.purchase_id, s.name AS student, b.title AS book,
       c.course_name AS course, p.purchase_date,
       p.quantity, p.total_amount
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
JOIN   books    b ON p.book_id    = b.book_id
LEFT   JOIN courses c ON p.course_id = c.course_id
ORDER  BY p.purchase_id DESC
LIMIT  25;"""
        st.dataframe(recent, use_container_width=True, hide_index=True,
                     column_config={
                         "total_amount": st.column_config.NumberColumn("Amount", format="$%.2f")
                     })
        sql_box(SQL_RECENT)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 · SQL PLAYGROUND
# ══════════════════════════════════════════════════════════════════════════════

elif page.startswith("🔬"):
    st.title("🔬 SQL Playground")
    st.caption(
        "Write any SELECT query against the bookstore database. "
        "When your result has a text column and a numeric column, "
        "the Playground will offer to chart it for you."
    )

    # ── Schema quick-reference ────────────────────────────────────────────────
    with st.expander("📋 Schema quick-reference — tables & columns"):
        schema_cols = st.columns(5)
        schema_info = {
            "students":     ["student_id (PK)", "name", "email", "major", "year", "gpa"],
            "courses":      ["course_id (PK)", "course_name", "department", "credits", "semester", "instructor"],
            "books":        ["book_id (PK)", "title", "author", "isbn", "price", "category", "publisher"],
            "course_books": ["course_id (FK)", "book_id (FK)", "required", "edition"],
            "purchases":    ["purchase_id (PK)", "student_id (FK)", "book_id (FK)", "course_id (FK)", "purchase_date", "quantity", "total_amount"],
        }
        for col, (tbl, cols) in zip(schema_cols, schema_info.items()):
            col.markdown(f"**`{tbl}`**")
            for c in cols:
                col.caption(c)

    # ── Example query library ─────────────────────────────────────────────────
    EXAMPLES = {
        "— pick an example —": "",
        "Revenue by department": """\
SELECT c.department,
       ROUND(SUM(p.total_amount), 2) AS revenue,
       COUNT(*)                       AS purchases
FROM   purchases p
JOIN   courses c ON p.course_id = c.course_id
GROUP  BY c.department
ORDER  BY revenue DESC;""",
        "Top 10 books by revenue": """\
SELECT b.title, b.category,
       COUNT(*)                        AS times_sold,
       ROUND(SUM(p.total_amount), 2)   AS revenue
FROM   purchases p
JOIN   books b ON p.book_id = b.book_id
GROUP  BY b.title, b.category
ORDER  BY revenue DESC
LIMIT  10;""",
        "Spend by student (ranked)": """\
SELECT ROW_NUMBER() OVER (ORDER BY SUM(p.total_amount) DESC) AS rank,
       s.name, s.major,
       ROUND(SUM(p.total_amount), 2) AS total_spent
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.name, s.major
ORDER  BY total_spent DESC;""",
        "Books never sold (anti-join)": """\
SELECT b.title, b.category, b.price, b.author
FROM   books b
LEFT   JOIN purchases p ON b.book_id = p.book_id
WHERE  p.purchase_id IS NULL
ORDER  BY b.category, b.price DESC;""",
        "Students never purchased (anti-join)": """\
SELECT s.name, s.major, s.year, s.gpa
FROM   students s
LEFT   JOIN purchases p ON s.student_id = p.student_id
WHERE  p.purchase_id IS NULL
ORDER  BY s.name;""",
        "Monthly revenue trend": """\
SELECT strftime(purchase_date, '%Y-%m') AS month,
       ROUND(SUM(total_amount), 2)       AS revenue,
       COUNT(*)                           AS purchases
FROM   purchases
GROUP  BY month
ORDER  BY month;""",
        "Required vs optional revenue": """\
SELECT CASE WHEN cb.required THEN 'Required' ELSE 'Optional' END AS book_type,
       COUNT(*)                        AS purchases,
       ROUND(SUM(p.total_amount), 2)   AS revenue
FROM   purchases p
JOIN   course_books cb
       ON p.book_id = cb.book_id AND p.course_id = cb.course_id
GROUP  BY cb.required
ORDER  BY revenue DESC;""",
        "Average book price by category": """\
SELECT category,
       COUNT(*)               AS num_books,
       ROUND(AVG(price), 2)   AS avg_price,
       ROUND(MIN(price), 2)   AS min_price,
       ROUND(MAX(price), 2)   AS max_price
FROM   books
GROUP  BY category
ORDER  BY avg_price DESC;""",
        "Spend by academic year": """\
SELECT CASE year WHEN 1 THEN 'Freshman'  WHEN 2 THEN 'Sophomore'
                 WHEN 3 THEN 'Junior'    ELSE 'Senior' END AS year,
       COUNT(*)                        AS purchases,
       ROUND(SUM(p.total_amount), 2)   AS total_spent,
       ROUND(AVG(p.total_amount), 2)   AS avg_per_purchase
FROM   purchases p
JOIN   students s ON p.student_id = s.student_id
GROUP  BY s.year, year
ORDER  BY s.year;""",
        "Cumulative revenue by date": """\
SELECT purchase_date,
       ROUND(SUM(total_amount), 2)                                    AS daily_rev,
       ROUND(SUM(SUM(total_amount)) OVER (ORDER BY purchase_date), 2) AS cumulative
FROM   purchases
GROUP  BY purchase_date
ORDER  BY purchase_date;""",
    }

    chosen_example = st.selectbox("📂 Load an example query", list(EXAMPLES.keys()))
    default_sql = EXAMPLES[chosen_example]

    # ── SQL editor ────────────────────────────────────────────────────────────
    user_sql = st.text_area(
        "Write your SQL here  (SELECT only — no data modification)",
        value=default_sql,
        height=180,
        placeholder="SELECT * FROM books LIMIT 10;",
    )

    col_run, col_clear = st.columns([1, 5])
    run_btn   = col_run.button("▶ Run Query", type="primary")
    clear_btn = col_clear.button("🗑 Clear results")

    if clear_btn:
        st.session_state.pop("pg_result", None)
        st.session_state.pop("pg_sql",    None)

    # ── Execute query and cache result in session_state ───────────────────────
    if run_btn and user_sql.strip():
        first_word = user_sql.strip().split()[0].upper()
        if first_word not in ("SELECT", "WITH", "EXPLAIN"):
            st.error("❌ Only SELECT (and WITH / EXPLAIN) queries are allowed in the Playground.")
        else:
            try:
                st.session_state["pg_result"] = run(user_sql.rstrip(";"))
                st.session_state["pg_sql"]    = user_sql
            except Exception as e:
                st.error(f"❌ Query error: {e}")
                st.session_state.pop("pg_result", None)
    elif run_btn:
        st.warning("Please enter a SQL query first.")

    # ── Render results (persists across reruns from widget changes) ───────────
    if "pg_result" in st.session_state:
        result_df = st.session_state["pg_result"]
        st.markdown("---")

        st.subheader(f"📋 Results — {len(result_df)} rows × {len(result_df.columns)} columns")
        st.dataframe(result_df, use_container_width=True, hide_index=True)

        num_cols = result_df.select_dtypes(include="number").columns.tolist()
        cat_cols = result_df.select_dtypes(exclude="number").columns.tolist()

        if len(num_cols) >= 1 and len(result_df) > 1:
            st.markdown("---")
            st.subheader("📊 Visualise Results")

            ctrl1, ctrl2, ctrl3, ctrl4 = st.columns(4)
            chart_type = ctrl1.selectbox(
                "Chart type",
                ["Bar Chart", "Horizontal Bar", "Pie Chart",
                 "Line Chart", "Area Chart", "Scatter Plot"],
                key="pg_chart_type",
            )
            label_col = ctrl2.selectbox(
                "Label / X-axis column",
                cat_cols + num_cols,
                index=0,
                key="pg_label_col",
            )
            value_col = ctrl3.selectbox(
                "Value / Y-axis column",
                num_cols,
                index=0,
                key="pg_value_col",
            )
            palette = ctrl4.selectbox(
                "Colour palette",
                ["Indigo", "Emerald", "Amber", "Multi-colour"],
                key="pg_palette",
            )

            PAL_MAP = {
                "Indigo":       [C1],
                "Emerald":      [C2],
                "Amber":        [C3],
                "Multi-colour": [C1, C2, C3, C5, C6, C4],
            }
            chosen_pal = PAL_MAP[palette]

            def get_colors(n):
                p = chosen_pal
                return [p[i % len(p)] for i in range(n)]

            labels       = result_df[label_col].astype(str).tolist()
            values       = result_df[value_col].tolist()
            n            = len(labels)
            colors       = get_colors(n)
            short_labels = [lb[:22]+"…" if len(lb) > 22 else lb for lb in labels]

            f_play, ax_play = fig(12, max(4, n * 0.38 if chart_type == "Horizontal Bar" else 4))

            if chart_type == "Bar Chart":
                bars_p = ax_play.bar(short_labels, values, color=colors,
                                     edgecolor="none", zorder=3)
                ax_play.set_xticklabels(short_labels, rotation=35, ha="right",
                                        color=MUTED, fontsize=8)
                ax_play.tick_params(axis="y", colors=MUTED)
                for b in bars_p:
                    v = b.get_height()
                    ax_play.text(b.get_x()+b.get_width()/2, v,
                                 f"{v:,.2f}" if isinstance(v, float) else str(v),
                                 ha="center", va="bottom", color=TEXT, fontsize=8)

            elif chart_type == "Horizontal Bar":
                hbars_p = ax_play.barh(short_labels[::-1], values[::-1],
                                       color=colors[::-1], edgecolor="none", zorder=3)
                ax_play.tick_params(axis="y", colors=MUTED, labelsize=8)
                ax_play.tick_params(axis="x", colors=MUTED)
                ax_play.grid(axis="x", color=GRID, lw=0.5, alpha=0.6)
                ax_play.grid(axis="y", visible=False)
                for b in hbars_p:
                    v = b.get_width()
                    ax_play.text(v, b.get_y()+b.get_height()/2,
                                 f"  {v:,.2f}" if isinstance(v, float) else f"  {v}",
                                 va="center", color=TEXT, fontsize=8)

            elif chart_type == "Pie Chart":
                # Pie slices always need distinct colours regardless of palette
                PIE_COLORS = [C1, C2, C3, C5, C6, C4, "#a78bfa", "#34d399",
                              "#fcd34d", "#f87171", "#60a5fa", "#f472b6"]
                pie_colors = [PIE_COLORS[i % len(PIE_COLORS)] for i in range(n)]
                ax_play.axis("off")
                ax_play.pie(
                    values, labels=short_labels, colors=pie_colors,
                    autopct="%1.1f%%", startangle=140,
                    textprops={"color": TEXT, "fontsize": 9},
                    wedgeprops={"edgecolor": BG, "linewidth": 1.5},
                )

            elif chart_type == "Line Chart":
                ax_play.plot(short_labels, values, color=colors[0],
                             lw=2.5, marker="o", markersize=5, zorder=3)
                ax_play.fill_between(range(n), values, alpha=0.12, color=colors[0])
                ax_play.set_xticks(range(n))
                ax_play.set_xticklabels(short_labels, rotation=35, ha="right",
                                        color=MUTED, fontsize=8)
                ax_play.tick_params(axis="y", colors=MUTED)
                for i, v in enumerate(values):
                    ax_play.text(i, v, f" {v:,.1f}", va="bottom", color=TEXT, fontsize=7.5)

            elif chart_type == "Area Chart":
                ax_play.fill_between(range(n), values, alpha=0.35, color=colors[0])
                ax_play.plot(range(n), values, color=colors[0], lw=2.5, zorder=3)
                ax_play.set_xticks(range(n))
                ax_play.set_xticklabels(short_labels, rotation=35, ha="right",
                                        color=MUTED, fontsize=8)
                ax_play.tick_params(axis="y", colors=MUTED)

            elif chart_type == "Scatter Plot":
                second_num = [c for c in num_cols if c != value_col]
                if second_num:
                    y2_col  = ctrl4.selectbox("Y-axis (scatter)", second_num, key="pg_y2")
                    y2_vals = result_df[y2_col].tolist()
                    y_label = y2_col
                else:
                    y2_vals = list(range(n))
                    y_label = "index"
                ax_play.scatter(values, y2_vals, color=colors[0], s=80, alpha=0.85, zorder=3)
                ax_play.set_xlabel(value_col, color=MUTED, fontsize=9)
                ax_play.set_ylabel(y_label, color=MUTED, fontsize=9)
                ax_play.tick_params(colors=MUTED)
                ax_play.grid(axis="both", color=GRID, lw=0.5, alpha=0.6)

            if chart_type not in ("Pie Chart", "Scatter Plot"):
                try:
                    ax_play.yaxis.set_major_formatter(
                        mticker.FuncFormatter(lambda v, _: f"{v:,.0f}")
                    )
                except Exception:
                    pass

            ax_play.set_title(f"{value_col}  by  {label_col}",
                              color=TEXT, fontsize=11, pad=10)
            plt.tight_layout()
            st.pyplot(f_play)
            plt.close(f_play)

        elif len(result_df) == 1:
            st.info("Single-row result — no chart needed.")
        else:
            st.info("No numeric column detected — chart not available for this result.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "SCU Bookstore Intelligence Platform · "
    "OMIS-105 · Santa Clara University · Leavey School of Business · "
    "Powered by DuckDB + Streamlit"
)
