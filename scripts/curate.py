import pandas as pd
import os

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_FILE = os.path.join(BASE_DIR, "data", "processed", "transformed_sales_data.csv")
CURATED_DIR = os.path.join(BASE_DIR, "data", "curated")
os.makedirs(CURATED_DIR, exist_ok=True)

df = pd.read_csv(PROCESSED_FILE)

# -------------------------------
# 1. Customer-level summary
# -------------------------------
customer_summary = df.groupby('CUSTOMERNAME').agg(
    LifetimeValue=('TOTALREVENUE', 'sum'),
    AvgOrderValue=('TOTALREVENUE', 'mean'),
    TotalOrders=('ORDERNUMBER', 'nunique'),
    OrderFrequency=('OrderFrequency', 'mean')
).reset_index()
customer_summary.to_csv(os.path.join(CURATED_DIR, "customer_summary.csv"), index=False)

# -------------------------------
# 2. Product-level summary
# -------------------------------
product_summary = df.groupby('PRODUCTLINE').agg(
    TotalRevenue=('TOTALREVENUE', 'sum'),
    TotalQuantity=('QUANTITYORDERED', 'sum'),
    AvgPrice=('PRICEEACH', 'mean')
).reset_index()
product_summary.to_csv(os.path.join(CURATED_DIR, "product_summary.csv"), index=False)

# -------------------------------
# 3. Monthly summary
# -------------------------------
monthly_summary = df.groupby(['YEAR', 'MONTH']).agg(
    MonthlyRevenue=('TOTALREVENUE', 'sum'),
    MonthlyOrders=('ORDERNUMBER', 'nunique')
).reset_index()
monthly_summary.to_csv(os.path.join(CURATED_DIR, "monthly_summary.csv"), index=False)

# -------------------------------
# 4. Country summary
# -------------------------------
country_summary = df.groupby('COUNTRY').agg(
    TotalRevenue=('TOTALREVENUE', 'sum'),
    TotalOrders=('ORDERNUMBER', 'nunique')
).reset_index()
country_summary.to_csv(os.path.join(CURATED_DIR, "country_summary.csv"), index=False)

print(f"✅ All curated summary tables saved in: {CURATED_DIR}")
