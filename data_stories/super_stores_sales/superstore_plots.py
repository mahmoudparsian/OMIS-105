"""
superstore_plots.py
-------------------
All plotting functions for the Superstore Sales DuckDB notebook.
Each function takes a pandas DataFrame (query result) and renders a chart.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")
sns.set_style("whitegrid")

# ── internal counter ──────────────────────────────────────────────
_plot_counter = 0

def _next_title(text: str) -> str:
    global _plot_counter
    _plot_counter += 1
    return f"{_plot_counter}. {text}"

def reset_counter():
    global _plot_counter
    _plot_counter = 0


# ── Category / Sub-Category ──────────────────────────────────────

def plot_category_sales_profit(df):
    """Bar charts: category-wise sales and profit side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.barplot(x="category", y="total_sales", data=df, ax=axes[0])
    axes[0].set_title(_next_title("Category-Wise Total Sales"))
    axes[0].set_ylabel("Total Sales")

    sns.barplot(x="category", y="total_profit", data=df, ax=axes[1])
    axes[1].set_title(_next_title("Category-Wise Profit"))
    axes[1].set_ylabel("Total Profit")
    plt.tight_layout()
    plt.show()


def plot_top_subcategories(df, n=10):
    """Horizontal bars: top N sub-categories by sales and by profit."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    top_sales = df.sort_values("total_sales", ascending=False).head(n)
    sns.barplot(x="total_sales", y="sub_category", data=top_sales, ax=axes[0])
    axes[0].set_title(_next_title(f"Top {n} Sub-Categories by Sales"))

    top_profit = df.sort_values("total_profit", ascending=False).head(n)
    sns.barplot(x="total_profit", y="sub_category", data=top_profit, ax=axes[1])
    axes[1].set_title(_next_title(f"Top {n} Sub-Categories by Profit"))
    plt.tight_layout()
    plt.show()


def plot_loss_subcategories(df):
    """Horizontal bars: sub-categories with negative profit."""
    loss = df[df["total_profit"] < 0].sort_values("total_profit")
    if loss.empty:
        print("No loss-making sub-categories found.")
        return
    sns.barplot(x="total_profit", y="sub_category", data=loss, palette="Reds_r")
    plt.title(_next_title("Loss-Making Sub-Categories"))
    plt.xlabel("Total Profit (Loss)")
    plt.tight_layout()
    plt.show()


# ── Regional ─────────────────────────────────────────────────────

def plot_region_sales_profit(df):
    """Side-by-side bar charts for regional sales and profit."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.barplot(x="region", y="total_sales", data=df, ax=axes[0])
    axes[0].set_title(_next_title("Regional Sales"))
    sns.barplot(x="region", y="total_profit", data=df, ax=axes[1])
    axes[1].set_title(_next_title("Regional Profit"))
    plt.tight_layout()
    plt.show()


def plot_top_cities(df):
    """Horizontal bar: top cities by sales."""
    sns.barplot(x="total_sales", y="city", data=df)
    plt.title(_next_title("Top 10 Cities by Sales"))
    plt.xlabel("Total Sales")
    plt.tight_layout()
    plt.show()


def plot_top_cities_profit(df):
    """Horizontal bar: top cities by profit."""
    sns.barplot(x="total_profit", y="city", data=df)
    plt.title(_next_title("Top 10 Cities by Profit"))
    plt.xlabel("Total Profit")
    plt.tight_layout()
    plt.show()


# ── Segment & Shipping ──────────────────────────────────────────

def plot_segment_sales_profit(df):
    """Grouped bar: segment-wise sales & profit."""
    melted = df.melt(id_vars="segment", value_vars=["total_sales", "total_profit"],
                     var_name="Metric", value_name="Value")
    sns.barplot(data=melted, x="segment", y="Value", hue="Metric")
    plt.title(_next_title("Segment-Wise Sales & Profit"))
    plt.ylabel("Total Value")
    plt.tight_layout()
    plt.show()


def plot_shipmode_sales_profit(df):
    """Side-by-side horizontal bars: ship mode sales and profit."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.barplot(x="total_sales", y="ship_mode", data=df, ax=axes[0])
    axes[0].set_title(_next_title("Sales by Ship Mode"))
    sns.barplot(x="total_profit", y="ship_mode", data=df, ax=axes[1])
    axes[1].set_title(_next_title("Profit by Ship Mode"))
    plt.tight_layout()
    plt.show()


# ── Time Series ──────────────────────────────────────────────────

def plot_monthly_trend(df):
    """Line chart: monthly sales trend."""
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df["month"], df["total_sales"], marker="o", markersize=3)
    ax.set_title(_next_title("Monthly Sales Trend"))
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales")
    ticks = ax.get_xticks()
    ax.set_xticks(ticks[::6])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_seasonality(df):
    """Bar chart: total sales by calendar month."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    labels = months[: len(df)]
    plt.bar(labels, df["total_sales"])
    plt.title(_next_title("Seasonality — Total Sales by Month"))
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.show()


def plot_quarterly_growth(df):
    """Bar chart: quarter-over-quarter sales with growth % annotation."""
    labels = [f"{int(r.yr)}-Q{int(r.qtr)}" for r in df.itertuples()]
    fig, ax = plt.subplots(figsize=(14, 5))
    bars = ax.bar(labels, df["total_sales"])
    ax.set_title(_next_title("Quarter-over-Quarter Sales"))
    ax.set_ylabel("Total Sales")
    plt.xticks(rotation=45)
    # annotate growth %
    for i, (bar, growth) in enumerate(zip(bars, df["growth_pct"])):
        if growth is not None and str(growth) != "None":
            color = "green" if float(growth) >= 0 else "red"
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    f"{growth}%", ha="center", va="bottom", fontsize=7, color=color)
    plt.tight_layout()
    plt.show()


# ── Relationships / Scatter ──────────────────────────────────────

def plot_quantity_vs_sales(df, sample_n=2000):
    """Scatter: Quantity vs Sales colored by Segment."""
    sample = df.sample(min(sample_n, len(df)), random_state=42)
    sns.scatterplot(data=sample, x="quantity", y="sales", hue="segment", alpha=0.6)
    plt.title(_next_title("Quantity vs Sales by Segment"))
    plt.tight_layout()
    plt.show()


def plot_sales_vs_profit(df, sample_n=2000):
    """Scatter: Sales vs Profit colored by Segment."""
    sample = df.sample(min(sample_n, len(df)), random_state=42)
    sns.scatterplot(data=sample, x="sales", y="profit", hue="segment", alpha=0.6)
    plt.axhline(0, color="red", linestyle="--", linewidth=0.8)
    plt.title(_next_title("Sales vs Profit by Segment"))
    plt.tight_layout()
    plt.show()


def plot_correlation_heatmap(df):
    """Heatmap of numeric correlations."""
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
    plt.title(_next_title("Correlation Heatmap"))
    plt.tight_layout()
    plt.show()


def plot_discount_vs_profit(df):
    """Bar: average profit at each discount level."""
    fig, ax = plt.subplots()
    ax.bar(df["discount_level"].astype(str), df["avg_profit"])
    ax.axhline(0, color="red", linestyle="--", linewidth=0.8)
    ax.set_title(_next_title("Average Profit by Discount Level"))
    ax.set_xlabel("discount")
    ax.set_ylabel("Avg Profit")
    plt.tight_layout()
    plt.show()


# ── State-level ──────────────────────────────────────────────────

def plot_top_states_profit(df, n=15):
    """Horizontal bar: top N states by profit."""
    top = df.sort_values("total_profit", ascending=False).head(n)
    colors = ["green" if p >= 0 else "red" for p in top["total_profit"]]
    plt.barh(top["state_province"], top["total_profit"], color=colors)
    plt.xlabel("Total Profit")
    plt.title(_next_title(f"Top {n} States by Profit"))
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def plot_yearly_performance(df):
    """Grouped bar: yearly sales and profit."""
    melted = df.melt(id_vars="order_year", value_vars=["total_sales", "total_profit"],
                     var_name="Metric", value_name="Value")
    sns.barplot(data=melted, x="order_year", y="Value", hue="Metric")
    plt.title(_next_title("Yearly Sales & Profit"))
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.show()
