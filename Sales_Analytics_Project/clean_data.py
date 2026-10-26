from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INPUT_FILE = "Online Retail.xlsx"
OUTPUT_FILE = DATA_DIR / "processed_data.csv"
QUALITY_FILE = DATA_DIR / "data_quality_report.csv"



df = pd.read_excel(INPUT_FILE)
original_rows, original_columns = df.shape

# Standardize column names
df.columns = (
    df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
)

required = {
    "invoiceno", "stockcode", "description", "quantity",
    "invoicedate", "unitprice", "customerid", "country"
}
missing_columns = required - set(df.columns)
if missing_columns:
    raise ValueError(f"Required columns missing: {missing_columns}")

initial_missing = df.isna().sum()
initial_duplicates = int(df.duplicated().sum())

df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")
for col in ["quantity", "unitprice", "customerid"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

invalid_dates = int(df["invoicedate"].isna().sum())
invalid_quantity = int(df["quantity"].isna().sum())
invalid_price = int(df["unitprice"].isna().sum())

df = df.drop_duplicates().copy()
duplicates_removed = original_rows - len(df)

cancelled_invoice = (
    df["invoiceno"].astype("string").str.strip().str.upper()
    .str.startswith("C", na=False)
)
negative_quantity = df["quantity"].lt(0).fillna(False)

sales = df.loc[
    ~cancelled_invoice
    & df["quantity"].gt(0)
    & df["unitprice"].gt(0)
    & df["invoicedate"].notna()
    & df["quantity"].notna()
    & df["unitprice"].notna()
].copy()

sales["description"] = sales["description"].astype("string").str.strip()
sales["country"] = sales["country"].astype("string").str.strip()
sales["revenue"] = sales["quantity"] * sales["unitprice"]
sales["year_month"] = sales["invoicedate"].dt.to_period("M").astype("string")
sales["year"] = sales["invoicedate"].dt.year
sales["month"] = sales["invoicedate"].dt.month

quality_report = pd.DataFrame([
    {"metric": "Original rows", "count": original_rows},
    {"metric": "Original columns", "count": original_columns},
    {"metric": "Missing customer IDs before cleaning",
     "count": int(initial_missing.get("customerid", 0))},
    {"metric": "Missing descriptions before cleaning",
     "count": int(initial_missing.get("description", 0))},
    {"metric": "Exact duplicate rows found", "count": initial_duplicates},
    {"metric": "Exact duplicate rows removed", "count": duplicates_removed},
    {"metric": "Invalid invoice dates", "count": invalid_dates},
    {"metric": "Missing/non-numeric quantity values", "count": invalid_quantity},
    {"metric": "Missing/non-numeric unit price values", "count": invalid_price},
    {"metric": "Cancellation invoice rows identified",
     "count": int(cancelled_invoice.sum())},
    {"metric": "Negative quantity rows identified",
     "count": int(negative_quantity.sum())},
    {"metric": "Processed sales rows", "count": len(sales)},
    {"metric": "Processed rows with missing customer IDs",
     "count": int(sales["customerid"].isna().sum())},
    {"metric": "Processed rows with missing descriptions",
     "count": int(sales["description"].isna().sum())},
    {"metric": "Total positive sales revenue", "count": round(sales["revenue"].sum(), 2)},
])

DATA_DIR.mkdir(parents=True, exist_ok=True)
sales.to_csv(OUTPUT_FILE, index=False)
quality_report.to_csv(QUALITY_FILE, index=False)

print(f"Original shape: {original_rows} rows x {original_columns} columns")
print(f"Duplicates removed: {duplicates_removed}")
print(f"Processed shape: {sales.shape}")
print(f"Positive sales revenue: {sales['revenue'].sum():,.2f}")
print(f"Saved: {OUTPUT_FILE}")
print(f"Saved: {QUALITY_FILE}")
