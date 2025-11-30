# sales_charts.py
# Creates sample sales data, aggregates, saves charts & a short summary.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import datetime as dt

OUTPUT_DIR = Path("sales_charts_output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Create sample dataset (one year daily for 2024) - replace this block to load your CSV
np.random.seed(42)
start = pd.Timestamp("2024-01-01")
end = pd.Timestamp("2024-12-31")
dates = pd.date_range(start, end, freq="D")
categories = ["Electronics", "Clothing", "Home", "Books"]
rows = []
for d in dates:
    for cat in categories:
        base = {"Electronics": 200, "Clothing": 100, "Home": 150, "Books": 50}[cat]
        month_factor = 1 + (0.25 if d.month in (11,12) else 0.0)
        noise = np.random.normal(loc=0.0, scale=base * 0.18)
        sales = max(0, base * month_factor + noise)
        units = max(1, int(sales / max(1, base * 0.5)))
        rows.append({"date": d, "category": cat, "sales": round(sales, 2), "units": units})

df = pd.DataFrame(rows)
csv_path = OUTPUT_DIR / "sample_sales.csv"
df.to_csv(csv_path, index=False)

# Aggregations
df["date"] = pd.to_datetime(df["date"])
daily = df.groupby("date", as_index=False)["sales"].sum()
monthly = df.set_index("date").groupby(pd.Grouper(freq="M"))["sales"].sum().reset_index()
monthly["month_start"] = monthly["date"].dt.to_period("M").dt.to_timestamp()
quarterly = df.set_index("date").groupby(pd.Grouper(freq="Q"))["sales"].sum().reset_index()
by_category = df.groupby("category", as_index=False)["sales"].sum().sort_values("sales", ascending=False)

# Plot helpers
def save_line_chart(x, y, title, fname, xlabel="Date", ylabel="Sales", date_rotation=0):
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(x, y, marker="", linewidth=1.5)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if np.issubdtype(x.dtype, np.datetime64):
        locator = mdates.AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
        for tick in ax.get_xticklabels():
            tick.set_rotation(date_rotation)
            tick.set_ha("right")
    ax.grid(axis="y", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    path = OUTPUT_DIR / fname
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path

def save_bar_chart(categories, values, title, fname, xlabel="Category", ylabel="Total Sales"):
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(categories, values)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    path = OUTPUT_DIR / fname
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path

def save_pie_chart(labels, sizes, title, fname):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.set_title(title, fontsize=14)
    ax.axis("equal")
    plt.tight_layout()
    path = OUTPUT_DIR / fname
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path

# Save charts
daily_path = save_line_chart(daily["date"], daily["sales"], "Daily Total Sales (2024)", "daily_sales.png", date_rotation=30)
monthly_path = save_line_chart(monthly["month_start"], monthly["sales"], "Monthly Total Sales (2024)", "monthly_sales.png")
quarterly_path = save_line_chart(quarterly["date"], quarterly["sales"], "Quarterly Total Sales (2024)", "quarterly_sales.png")
bar_path = save_bar_chart(by_category["category"], by_category["sales"], "Total Sales by Category (2024)", "category_bar.png")
pie_path = save_pie_chart(by_category["category"], by_category["sales"], "Category Sales Share (2024)", "category_pie.png")

# Summary
total_sales = df["sales"].sum()
top_cat = by_category.iloc[0]["category"]
top_cat_sales = by_category.iloc[0]["sales"]
best_month = monthly.loc[monthly["sales"].idxmax(), "month_start"].strftime("%B %Y")
best_month_sales = monthly["sales"].max()

summary_text = f"""Sales Charts Demo - Summary
Generated: {dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC

Total sales: {total_sales:,.2f}
Top category: {top_cat} ({top_cat_sales:,.2f})
Best month: {best_month} ({best_month_sales:,.2f})

Files in: {OUTPUT_DIR}
- {daily_path.name}
- {monthly_path.name}
- {quarterly_path.name}
- {bar_path.name}
- {pie_path.name}
- {csv_path.name}
"""
with open(OUTPUT_DIR / "summary.txt", "w") as f:
    f.write(summary_text)

print("Generated files in:", OUTPUT_DIR)
