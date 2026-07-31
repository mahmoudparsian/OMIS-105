"""
plots.py — Helpers for the DuckDB Intro Lab
============================================
Students: you don't need to read this file.
Just call the functions from the notebook!

  Table display:
    run(sql, title, con)               <- execute SQL and show a styled table
    show_table(df, title)              <- display any DataFrame as a styled table

  Charts:
    plot_revenue_by_category(revenue_df)
    plot_monthly_trend(monthly_df)
    plot_customer_tiers(tier_df)
    plot_employee_analytics(dept_df, con)
    plot_movie_dashboard(genre_df, con)
    plot_customer_leaderboard(top_customers)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from IPython.display import display, HTML
import duckdb as _duckdb

# ── Colour constants (used by both table and chart helpers) ───────────────────
TEXT = '#e8eaf6'

# ── Colour palette ────────────────────────────────────────────────────────────
DARK_BG  = '#0f1117'
CARD_BG  = '#1a1d2e'
GOLD     = '#FFD700'
PALETTE  = ['#FFD700','#61dafb','#50fa7b','#bd93f9','#ff79c6','#ff5555','#8be9fd','#f1fa8c']


# ── Table display helpers ─────────────────────────────────────────────────────

def show_table(df, title=None, max_rows=30):
    """Render a DataFrame as a dark-themed HTML table with row numbers."""
    df_show = df.head(max_rows).copy()
    title_html = ''
    if title:
        title_html = (
            f'<div style="background:linear-gradient(135deg,#FFD700,#FFA500);'
            f'color:#0f1117;font-weight:800;font-size:1.05em;'
            f'padding:10px 20px;border-radius:10px 10px 0 0;">&#128202; {title}</div>'
        )
    headers = (
        '<th style="background:#12151f;color:#FFD700;padding:10px 16px;font-weight:700;'
        'border-bottom:2px solid #FFD700;font-size:0.82em;text-align:center;">#</th>'
    )
    for col in df_show.columns:
        headers += (
            f'<th style="background:#12151f;color:#FFD700;padding:10px 16px;'
            f'font-weight:700;border-bottom:2px solid #FFD700;font-size:0.82em;">{col}</th>'
        )
    rows_html = ''
    for i, (_, row) in enumerate(df_show.iterrows()):
        bg = '#1a1d2e' if i % 2 == 0 else '#1e2340'
        cells_html = (
            f'<td style="background:{bg};color:#6272a4;padding:9px 16px;'
            f'border-bottom:1px solid #2d3148;font-size:0.82em;'
            f'text-align:center;font-family:monospace;">{i + 1}</td>'
        )
        for val in row:
            if isinstance(val, (int, float, np.integer, np.floating)):
                col_c = '#bd93f9'
                fmt = f'{val:,.2f}' if isinstance(val, (float, np.floating)) else f'{val:,}'
            else:
                col_c = TEXT
                fmt = str(val)
            cells_html += (
                f'<td style="background:{bg};color:{col_c};padding:9px 16px;'
                f'border-bottom:1px solid #2d3148;font-size:0.88em;'
                f'font-family:Consolas,monospace;">{fmt}</td>'
            )
        rows_html += f'<tr>{cells_html}</tr>'
    total = len(df)
    shown = len(df_show)
    fn = (f'Showing {shown} of {total} rows' if total > shown
          else f'{total} row{"s" if total != 1 else ""}')
    footer = (
        f'<tr><td colspan="{len(df_show.columns) + 1}" style="background:#12151f;'
        f'color:#6272a4;font-size:0.78em;padding:6px 16px;text-align:right;'
        f'font-style:italic;">{fn}</td></tr>'
    )
    html = (
        f'<div style="margin:16px 0;border-radius:12px;overflow:hidden;'
        f'box-shadow:0 6px 24px rgba(0,0,0,0.5);border:1px solid #2d3148;">'
        f'{title_html}<div style="overflow-x:auto;">'
        f'<table style="border-collapse:collapse;width:100%;margin:0;">'
        f'<thead><tr>{headers}</tr></thead>'
        f'<tbody>{rows_html}{footer}</tbody></table></div></div>'
    )
    display(HTML(html))


def run(sql, title=None, con=None):
    """Execute a SQL string and display the result as a styled table.

    Returns the result as a pandas DataFrame so you can keep working with it.

    Examples
    --------
    run("SELECT * FROM customers", con=con)
    df = run("SELECT category, COUNT(*) FROM products GROUP BY 1", con=con)
    """
    df = (con or _duckdb).sql(sql).df()
    show_table(df, title=title)
    return df


# ── Chart style ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': DARK_BG, 'axes.facecolor': CARD_BG,
    'axes.edgecolor': '#2d3148', 'axes.labelcolor': TEXT,
    'axes.titlecolor': GOLD, 'axes.titlesize': 15, 'axes.titleweight': 'bold',
    'axes.labelsize': 12, 'xtick.color': TEXT, 'ytick.color': TEXT,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'text.color': TEXT,
    'grid.color': '#2d3148', 'grid.linestyle': '--', 'grid.alpha': 0.6,
    'legend.facecolor': CARD_BG, 'legend.edgecolor': '#2d3148',
})


def plot_revenue_by_category(df):
    """Chart 1 — Revenue bar + units-sold pie, grouped by product category.

    Expected columns: category, total_revenue, units_sold
    """
    cats   = df['category']
    revs   = df['total_revenue']
    units  = df['units_sold']
    colors = PALETTE[:len(cats)]

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
    fig.patch.set_facecolor(DARK_BG)

    # Left: horizontal bar — revenue
    ax = axes[0]
    bars = ax.barh(cats, revs, color=colors, edgecolor='none', height=0.6)
    ax.set_xlabel('Total Revenue ($)')
    ax.set_title('Revenue by Category', pad=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.4)
    ax.set_axisbelow(True)
    for bar, val in zip(bars, revs):
        ax.text(bar.get_width() + max(revs) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f'${val:,.0f}', va='center', color=GOLD, fontsize=9, fontweight='bold')

    # Right: pie — units sold
    ax2 = axes[1]
    wedges, texts, autotexts = ax2.pie(
        units, labels=cats, colors=colors, autopct='%1.1f%%', startangle=140,
        pctdistance=0.75, wedgeprops={'edgecolor': DARK_BG, 'linewidth': 2})
    for at in autotexts:
        at.set_color(DARK_BG)
        at.set_fontweight('bold')
    for t in texts:
        t.set_color(TEXT)
    ax2.set_title('Units Sold by Category', pad=12)

    plt.suptitle('E-Commerce Sales Breakdown', color=GOLD,
                 fontsize=16, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.show()
    print('Insight: Electronics dominate revenue — high unit price drives totals despite fewer units sold!')


def plot_monthly_trend(df):
    """Chart 2 — Monthly revenue line + order count bars (dual-axis).

    Expected columns: month, revenue, num_orders
    """
    months   = df['month']
    revenues = df['revenue']
    orders_n = df['num_orders']
    x        = range(len(months))

    fig, ax1 = plt.subplots(figsize=(12, 5.5))
    fig.patch.set_facecolor(DARK_BG)

    ax1.fill_between(x, revenues, alpha=0.18, color=GOLD)
    ax1.plot(x, revenues, color=GOLD, linewidth=2.5, marker='o',
             markersize=8, markerfacecolor=DARK_BG,
             markeredgecolor=GOLD, markeredgewidth=2)
    ax1.set_ylabel('Monthly Revenue ($)', color=GOLD)
    ax1.tick_params(axis='y', colors=GOLD)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
    ax1.set_xticks(x)
    ax1.set_xticklabels(months)
    ax1.grid(True, alpha=0.3)
    ax1.set_axisbelow(True)
    for xi, yi in zip(x, revenues):
        ax1.annotate(f'${yi:,.0f}', (xi, yi), textcoords='offset points',
                     xytext=(0, 12), ha='center', color=GOLD, fontsize=9, fontweight='bold')

    ax2 = ax1.twinx()
    ax2.bar(x, orders_n, alpha=0.35, color='#61dafb', width=0.4)
    ax2.set_ylabel('Number of Orders', color='#61dafb')
    ax2.tick_params(axis='y', colors='#61dafb')
    ax2.set_ylim(0, max(orders_n) * 2.5)
    ax2.spines['right'].set_color('#61dafb')

    legend_items = [
        Line2D([0], [0], color=GOLD, linewidth=2.5, marker='o', label='Revenue ($)'),
        plt.Rectangle((0, 0), 1, 1, color='#61dafb', alpha=0.5, label='Order Count'),
    ]
    ax1.legend(handles=legend_items, loc='upper left')
    ax1.set_title('Monthly Revenue & Order Volume 2024',
                  color=GOLD, fontsize=15, fontweight='bold', pad=14)
    plt.tight_layout()
    plt.show()


def plot_customer_tiers(df):
    """Chart 3 — Three-panel bar chart comparing customer tier metrics.

    Expected columns: tier, total_spent, avg_order_value, revenue_per_customer
    """
    tier_palette = {
        'Platinum': '#bd93f9', 'Gold': '#FFD700',
        'Silver': '#8be9fd',   'Bronze': '#ff9966',
    }
    colors  = [tier_palette.get(t, PALETTE[i]) for i, t in enumerate(df['tier'])]
    metrics = [
        ('total_spent',          'Total Revenue ($)',        'Revenue by Customer Tier'),
        ('avg_order_value',      'Avg Order Value ($)',       'Avg Order Value by Tier'),
        ('revenue_per_customer', 'Revenue per Customer ($)',  'Revenue per Customer'),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    fig.patch.set_facecolor(DARK_BG)

    for ax, (col, ylabel, ttl) in zip(axes, metrics):
        vals = df[col]
        bars = ax.bar(df['tier'], vals, color=colors, edgecolor='none', width=0.55)
        ax.set_title(ttl, pad=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
        ax.grid(axis='y', alpha=0.35)
        ax.set_axisbelow(True)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(vals) * 0.02,
                    f'${val:,.0f}', ha='center', va='bottom',
                    fontsize=9, color=GOLD, fontweight='bold')

    plt.suptitle('Customer Tier Performance', color=GOLD,
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()
    print('Insight: Platinum customers spend 3x more per order than Bronze!')


def plot_employee_analytics(dept_df, con):
    """Chart 4 — Salary range bars + rating-vs-experience bubble chart.

    dept_df expected columns: department, avg_salary, min_salary, max_salary
    con: active DuckDB connection (used to fetch individual employee rows)
    """
    depts        = dept_df['department']
    avg_s        = dept_df['avg_salary']
    min_s        = dept_df['min_salary']
    max_s        = dept_df['max_salary']
    dept_colors  = PALETTE[:len(depts)]
    x            = range(len(depts))
    dept_color_map = dict(zip(depts, dept_colors))

    emp_df = con.execute(
        'SELECT department, years_exp, rating, salary FROM employees'
    ).df()

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor(DARK_BG)

    # Left: salary bars with min/max whiskers
    ax = axes[0]
    bars = ax.bar(x, avg_s, color=dept_colors, edgecolor='none', width=0.6)
    ax.errorbar(x, avg_s, yerr=[avg_s - min_s, max_s - avg_s],
                fmt='none', color='white', capsize=6, capthick=2, linewidth=2)
    ax.set_xticks(x)
    ax.set_xticklabels(depts, rotation=20, ha='right')
    ax.set_ylabel('Salary ($)')
    ax.set_title('Avg Salary by Dept (whiskers = min/max)', pad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v/1000:.0f}k'))
    ax.grid(axis='y', alpha=0.35)
    ax.set_axisbelow(True)
    for bar, val in zip(bars, avg_s):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3000,
                f'${val/1000:.0f}k', ha='center', va='bottom',
                color=GOLD, fontweight='bold', fontsize=9)

    # Right: rating vs experience bubble
    ax2 = axes[1]
    for dept, grp in emp_df.groupby('department'):
        ax2.scatter(grp['years_exp'], grp['rating'],
                    color=dept_color_map.get(dept, 'gray'),
                    s=grp['salary'] / 700, alpha=0.85, label=dept,
                    edgecolors='white', linewidths=0.5)
    ax2.set_xlabel('Years of Experience')
    ax2.set_ylabel('Performance Rating')
    ax2.set_title('Rating vs Experience (bubble size = salary)', pad=10)
    ax2.legend(loc='lower right', fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.suptitle('Employee Analytics Dashboard', color=GOLD,
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()


def plot_movie_dashboard(genre_df, con):
    """Chart 5 — Four-panel movie analytics dashboard.

    genre_df expected columns: genre, total_box_office_m, avg_rating
    con: active DuckDB connection (used to fetch individual movie rows)
    """
    genres          = genre_df['genre']
    genre_colors    = ['#ff79c6', '#50fa7b', '#FFD700', '#61dafb']
    genre_color_map = dict(zip(genres, genre_colors))

    movie_df = con.execute(
        'SELECT title, genre, year, rating, box_office_m, runtime_min FROM movies'
    ).df()

    fig, axes = plt.subplots(2, 2, figsize=(15, 11))
    fig.patch.set_facecolor(DARK_BG)
    axes = axes.flatten()

    # Panel 1: total box office
    ax = axes[0]
    bars = ax.bar(genres, genre_df['total_box_office_m'],
                  color=genre_colors, width=0.55)
    ax.set_title('Total Box Office by Genre ($M)')
    ax.set_ylabel('Revenue ($M)')
    ax.grid(axis='y', alpha=0.35)
    ax.set_axisbelow(True)
    for bar, val in zip(bars, genre_df['total_box_office_m']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                f'${val:.0f}M', ha='center', color=GOLD,
                fontweight='bold', fontsize=10)

    # Panel 2: avg rating horizontal bars
    ax2 = axes[1]
    bars2 = ax2.barh(genres, genre_df['avg_rating'],
                     color=genre_colors, height=0.5)
    ax2.set_title('Average Audience Rating')
    ax2.set_xlabel('Rating (out of 10)')
    ax2.set_xlim(0, 10)
    ax2.grid(axis='x', alpha=0.35)
    ax2.set_axisbelow(True)
    for bar, val in zip(bars2, genre_df['avg_rating']):
        ax2.text(val + 0.1, bar.get_y() + bar.get_height() / 2,
                 f'{val:.1f}', va='center', color=GOLD,
                 fontweight='bold', fontsize=10)

    # Panel 3: rating vs box office scatter (bubble = runtime)
    ax3 = axes[2]
    for genre, grp in movie_df.groupby('genre'):
        ax3.scatter(grp['rating'], grp['box_office_m'],
                    color=genre_color_map.get(genre, 'gray'),
                    s=grp['runtime_min'] * 1.2, alpha=0.8, label=genre,
                    edgecolors='white', linewidths=0.7)
    ax3.set_xlabel('Audience Rating')
    ax3.set_ylabel('Box Office ($M)')
    ax3.set_title('Rating vs Box Office (bubble size = runtime)')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)

    # Panel 4: stacked bar — movies per year by genre
    ax4 = axes[3]
    pivot  = movie_df.groupby(['year', 'genre']).size().unstack(fill_value=0)
    bottom = np.zeros(len(pivot.index))
    for i, genre in enumerate(pivot.columns):
        vals  = pivot[genre].values
        bars4 = ax4.bar(pivot.index, vals, bottom=bottom,
                        color=genre_color_map.get(genre, PALETTE[i]),
                        label=genre, edgecolor=DARK_BG, linewidth=0.8)
        for bar, val, bot in zip(bars4, vals, bottom):
            if val > 0:
                ax4.text(bar.get_x() + bar.get_width() / 2, bot + val / 2,
                         str(val), ha='center', va='center',
                         color='#0f1117', fontweight='bold', fontsize=11)
        bottom += vals
    ax4.set_title('Movies per Year by Genre')
    ax4.set_ylabel('Number of Movies')
    ax4.set_xticks(pivot.index)
    ax4.legend(fontsize=9, loc='upper right')
    ax4.grid(axis='y', alpha=0.35)
    ax4.set_axisbelow(True)
    ax4.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    plt.suptitle('Movie Database Analytics', color=GOLD,
                 fontsize=18, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.show()


def plot_customer_leaderboard(df):
    """Chart 6 — Horizontal bar leaderboard of customers by total spend.

    Expected columns: name, tier, total_spent
    """
    tier_pal   = {
        'Platinum': '#bd93f9', 'Gold': '#FFD700',
        'Silver':   '#8be9fd', 'Bronze': '#ff9966',
    }
    bar_colors = [tier_pal.get(t, PALETTE[0]) for t in df['tier']]
    names = df['name']
    spent = df['total_spent']

    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor(DARK_BG)

    bars = ax.barh(names[::-1], spent[::-1],
                   color=bar_colors[::-1], edgecolor='none', height=0.65)
    for bar, val, tier in zip(bars, spent[::-1], df['tier'][::-1]):
        ax.text(bar.get_width() + max(spent) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f'${val:,.0f}', va='center', color=GOLD,
                fontweight='bold', fontsize=10)
        ax.text(bar.get_width() * 0.03,
                bar.get_y() + bar.get_height() / 2,
                tier, va='center', color='#0f1117',
                fontweight='bold', fontsize=8.5)

    ax.set_xlabel('Total Amount Spent ($)')
    ax.set_title('Customer Spend Leaderboard — GROUP BY + ORDER BY',
                 color=GOLD, fontsize=15, fontweight='bold', pad=14)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
    ax.grid(axis='x', alpha=0.35)
    ax.set_axisbelow(True)
    legend_patches = [Patch(color=c, label=t) for t, c in tier_pal.items()]
    ax.legend(handles=legend_patches, title='Tier', loc='lower right', fontsize=10)
    plt.tight_layout()
    plt.show()
