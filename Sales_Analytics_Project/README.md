# Sales Performance & Profitability Analytics

## Project Overview

This project analyzes online retail transactions to understand sales
performance, product contribution, customer value, and geographic sales
patterns. It uses Python and Pandas for data preparation and analysis,
with Google Looker Studio for interactive visualization.

> **Important:** The available transaction data supports revenue
> analysis, not true profit analysis, because product costs and
> operating expenses are not provided. Here, `revenue` means
> `quantity × unit price` for valid positive-sales records.

## Business Objectives

-   Track sales revenue over time.
-   Identify products contributing the most revenue.
-   Compare revenue across countries.
-   Identify high-value customers where customer IDs are available.
-   Recommend actions for sales, marketing, and inventory planning.

## Tools

Python, Pandas, NumPy, OpenPyXL, Google Sheets, Google Looker Studio,
Git, and GitHub.

## Project Structure

``` text
Sales-Performance-Profitability-Analytics/
├── data/
│   ├── Online Retail.xlsx
│   └── processed_data.csv
├── outputs/
│   ├── sales_kpis.csv
│   ├── monthly_sales.csv
│   ├── top_products.csv
│   ├── country_performance.csv
│   ├── top_customers.csv
│   └── repeat_purchase_summary.csv
├── clean_data.py
├── sales_analysis.py
├── requirements.txt
├── README.md
└── .gitignore
```

Adjust the filenames above to match your actual project. Consider
keeping the original and processed datasets out of GitHub if they are
large or their redistribution terms do not permit sharing.

## Dataset

**Source:** UCI Machine Learning Repository --- Online Retail\
https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains online retail transactions, including invoice
numbers, products, quantities, invoice dates, unit prices, customer IDs,
and countries. Confirm exact row counts and missing-value totals from
your local source and data-quality report.

## Methodology

1.  Load and inspect the dataset.
2.  Standardize column names and convert dates and numeric fields to
    appropriate types.
3.  Identify and remove exact duplicate rows.
4.  Identify cancellation invoices and non-positive quantities or
    prices.
5.  Prepare a positive-sales dataset for revenue analysis while
    retaining the original source separately.
6.  Calculate `revenue = quantity × unit price` and derive monthly date
    fields.
7.  Export cleaned data and analysis summaries.
8.  Build charts and KPI scorecards in Looker Studio.

## Dashboard

**Looker Studio URL:** \[Add your shareable dashboard link here\]

Planned charts: - Monthly sales revenue trend - Top 10 products by
revenue - Revenue by country - Top 10 customers by revenue

Suggested KPI scorecards include total revenue, total orders, unique
identified customers, and average order value.

**Average Order Value (AOV):**
`SUM(revenue) / COUNT_DISTINCT(invoiceno)`

## Key Findings

Add at least five findings supported by actual values from your
generated CSV outputs. For each finding, include evidence, business
relevance, impact, and a recommendation. Do not present unverified
assumptions as results.

## Recommendations

Validate these potential recommendations against your findings: 1.
Develop retention campaigns for high-value and repeat customers. 2.
Improve inventory planning for products with consistently high revenue
or demand. 3. Compare country-level performance to prioritize
established markets and investigate growth opportunities.

## Limitations

-   Product costs, operating expenses, marketing costs, and full return
    costs are not provided, so true profit and product profitability
    cannot be calculated.
-   Missing customer IDs limit customer-level analysis.
-   Cancellations, returns, missing values, and duplicates may affect
    results; document cleaning decisions.
-   Positive-sales analysis should not be interpreted as net revenue
    after returns unless returns are analyzed separately.

## Run Locally (Ubuntu/Linux)

``` bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Place the source workbook at `data/Online Retail.xlsx` if that is the
path expected by your script, then run:

``` bash
python clean_data.py
python sales_analysis.py
```

Adjust paths and filenames if your scripts differ. Verify that output
files are generated before connecting the cleaned data to Google Sheets
and Looker Studio.

## AI Usage Disclosure

AI assistance was used to help plan the project structure, explain
analysis steps, and draft documentation. The author should validate data
processing, calculations, dashboard metrics, and final interpretations
against the actual dataset. Review AI-generated suggestions before
submitting the project.

## Author

**Ramkrishna Majumder**

## Data Use

Refer to the dataset provider's terms and cite the UCI source. Do not
redistribute the source data unless its terms permit it. Add a license
for your own code only if you have selected appropriate terms.
