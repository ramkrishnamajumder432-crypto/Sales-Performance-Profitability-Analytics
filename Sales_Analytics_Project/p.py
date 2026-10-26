
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

INPUT_FILE = DATA_DIR / "processed_data.csv"
OUTPUT_DIR.mkdir(exist_ok=True)

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        "processed_data.csv not found. Run clean_data.py first."
    )

df = pd.read_csv(INPUT_FILE, parse_dates=["invoicedate"])

# Ensure numeric fields are valid
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unitprice"] = pd.to_numeric(df["unitprice"], errors="coerce")

df = df.dropna(subset=["invoicedate", "revenue"])

# -----------------------------------
# 1. OVERALL SALES KPIs
# -----------------------------------
total_revenue = df["revenue"].sum()
total_orders = df["invoiceno"].nunique()
total_customers = df["customerid"].nunique()
total_products = df["stockcode"].nunique()
average_order_value = (
    total_revenue / total_orders if total_orders else 0
)

kpis = pd.DataFrame({
    "Metric": [
        "Total positive sales revenue",
        "Unique invoices",
        "Unique identified customers",
        "Unique products",
        "Average revenue per invoice"
    ],
    "Value": [
        round(total_revenue, 2),
        total_orders,
        total_customers,
        total_products,
        round(average_order_value, 2)
    ]
})

kpis.to_csv(OUTPUT_DIR / "sales_kpis.csv", index=False)

# -----------------------------------
# 2. MONTHLY SALES TREND
# -----------------------------------
df["year_month"] = df["invoicedate"].dt.to_period("M").astype(str)

monthly = df.groupby("year_month", as_index=False).agg(
    revenue=("revenue", "sum"),
    orders=("invoiceno", "nunique"),
    quantity_sold=("quantity", "sum")
)

monthly["previous_month_revenue"] = monthly["revenue"].shift(1)
monthly["mom_growth_pct"] = (
    (monthly["revenue"] / monthly["previous_month_revenue"] - 1) * 100
).replace([np.inf, -np.inf], np.nan)

monthly.to_csv(OUTPUT_DIR / "monthly_sales.csv", index=False)

# -----------------------------------
# 3. TOP PRODUCTS BY REVENUE
# -----------------------------------
products = df.groupby(
    ["stockcode", "description"], dropna=False, as_index=False
).agg(
    revenue=("revenue", "sum"),
    quantity_sold=("quantity", "sum"),
    orders=("invoiceno", "nunique")
)

products = products.sort_values("revenue", ascending=False)
products.head(20).to_csv(
    OUTPUT_DIR / "top_products.csv", index=False
)

# -----------------------------------
# 4. COUNTRY PERFORMANCE
# -----------------------------------
countries = df.groupby("country", as_index=False).agg(
    revenue=("revenue", "sum"),
    orders=("invoiceno", "nunique"),
    customers=("customerid", "nunique"),
    quantity_sold=("quantity", "sum")
)

countries["revenue_share_pct"] = (
    countries["revenue"] / total_revenue * 100
)

countries = countries.sort_values("revenue", ascending=False)
countries.to_csv(OUTPUT_DIR / "country_performance.csv", index=False)

# -----------------------------------
# 5. CUSTOMER REVENUE CONCENTRATION
# -----------------------------------
identified = df.dropna(subset=["customerid"]).copy()

customer_sales = identified.groupby(
    "customerid", as_index=False
).agg(
    revenue=("revenue", "sum"),
    orders=("invoiceno", "nunique")
)

customer_sales = customer_sales.sort_values(
    "revenue", ascending=False
).reset_index(drop=True)

customer_sales["revenue_share_pct"] = (
    customer_sales["revenue"] /
    customer_sales["revenue"].sum() * 100
)

customer_sales["cumulative_revenue_share_pct"] = (
    customer_sales["revenue_share_pct"].cumsum()
)

top_10_count = max(1, int(np.ceil(len(customer_sales) * 0.10)))

top_10_customer_share = (
    customer_sales.head(top_10_count)["revenue"].sum()
    / customer_sales["revenue"].sum() * 100
    if len(customer_sales) else 0
)

customer_sales.head(100).to_csv(
    OUTPUT_DIR / "top_customers.csv", index=False
)

# -----------------------------------
# 6. REPEAT PURCHASE BEHAVIOUR
# -----------------------------------
# Count distinct invoices per identified customer.
repeat_summary = pd.DataFrame({
    "Metric": [
        "Identified customers",
        "Customers with more than one invoice",
        "Repeat customer percentage"
    ],
    "Value": [
        len(customer_sales),
        int((customer_sales["orders"] > 1).sum()),
        round(
            (customer_sales["orders"] > 1).mean() * 100, 2
        ) if len(customer_sales) else 0
    ]
})

repeat_summary.to_csv(
    OUTPUT_DIR / "repeat_purchase_summary.csv", index=False
)

# -----------------------------------
# 7. PRINT IMPORTANT RESULTS
# -----------------------------------
print("\n========== SALES KPIs ==========")
print(kpis.to_string(index=False))

print("\n========== TOP 5 MONTHS ==========")
print(monthly.nlargest(5, "revenue").to_string(index=False))

print("\n========== TOP 10 PRODUCTS ==========")
print(products.head(10).to_string(index=False))

print("\n========== TOP 10 COUNTRIES ==========")
print(countries.head(10).to_string(index=False))

print("\n========== CUSTOMER CONCENTRATION ==========")
print(f"Top 10% of identified customers contribute "
      f"{top_10_customer_share:.2f}% of identified-customer revenue.")

print("\n========== REPEAT PURCHASES ==========")
print(repeat_summary.to_string(index=False))

print("\nAnalysis complete. Results saved in:", OUTPUT_DIR)
