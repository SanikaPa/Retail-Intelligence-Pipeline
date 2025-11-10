import pandas as pd
import os

# -------------------------------
# Paths
# -------------------------------
processed_file = "../data/processed/transformed_sales_data.csv"
curated_folder = "../data/curated/"
os.makedirs(curated_folder, exist_ok=True)

# -------------------------------
# Load processed data
# -------------------------------
df = pd.read_csv(processed_file)

# -------------------------------
# 1. Customer-level summary
# -------------------------------
customer_summary = df.groupby('CUSTOMERNAME').agg(
    LifetimeValue=('TOTALREVENUE', 'sum'),
    AvgOrderValue=('TOTALREVENUE', 'mean'),
    TotalOrders=('ORDERNUMBER', 'nunique'),
    OrderFrequency=('OrderFrequency', 'mean')
).reset_index()

customer_summary.to_csv(os.path.join(curated_folder, "customer_summary.csv"), index=False)

# -------------------------------
# 2. Product-level summary
# -------------------------------
product_summary = df.groupby('PRODUCTLINE').agg(
    TotalRevenue=('TOTALREVENUE', 'sum'),
    TotalQuantity=('QUANTITYORDERED', 'sum'),
    AvgPrice=('PRICEEACH', 'mean')
).reset_index()

product_summary.to_csv(os.path.join(curated_folder, "product_summary.csv"), index=False)

# -------------------------------
# 3. Monthly summary
# -------------------------------
monthly_summary = df.groupby(['YEAR', 'MONTH']).agg(
    MonthlyRevenue=('TOTALREVENUE', 'sum'),
    MonthlyOrders=('ORDERNUMBER', 'nunique')
).reset_index()

monthly_summary.to_csv(os.path.join(curated_folder, "monthly_summary.csv"), index=False)

# -------------------------------
# 4. Country/Region summary
# -------------------------------
country_summary = df.groupby('COUNTRY').agg(
    TotalRevenue=('TOTALREVENUE', 'sum'),
    TotalOrders=('ORDERNUMBER', 'nunique')
).reset_index()

country_summary.to_csv(os.path.join(curated_folder, "country_summary.csv"), index=False)

print("All curated summary tables saved in:", curated_folder)
