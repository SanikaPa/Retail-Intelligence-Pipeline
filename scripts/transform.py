import pandas as pd
import os

# -------------------------------
# Set base directory (repo root)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input & output paths
clean_path = os.path.join(BASE_DIR, 'data', 'clean', 'cleaned_sales_data.csv')
processed_folder = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(processed_folder, exist_ok=True)
processed_file_path = os.path.join(processed_folder, "transformed_sales_data.csv")

# -------------------------------
# Load cleaned data
# -------------------------------
df = pd.read_csv(clean_path)
print("Initial shape:", df.shape)

# -------------------------------
# Ensure TOTALREVENUE column exists
# -------------------------------
if 'SALES' not in df.columns:
    df['SALES'] = df['QUANTITYORDERED'] * df['PRICEEACH']

df['TOTALREVENUE'] = df['SALES']

# -------------------------------
# Ensure ORDERDATE is datetime and extract DAY, MONTH, YEAR
# -------------------------------
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')
df = df[df['ORDERDATE'].notna()]  # remove invalid dates

df['DAY'] = df['ORDERDATE'].dt.day
df['MONTH'] = df['ORDERDATE'].dt.month
df['YEAR'] = df['ORDERDATE'].dt.year

# -------------------------------
# Feature Engineering
# -------------------------------

# 1. Customer-level metrics
cust_summary = df.groupby('CUSTOMERNAME').agg(
    LifetimeValue=('TOTALREVENUE', 'sum'),
    AvgOrderValue=('TOTALREVENUE', 'mean'),
    TotalOrders=('ORDERNUMBER', 'nunique')
).reset_index()

# 2. Product-level trends
prod_summary = df.groupby(['PRODUCTLINE', 'DAY', 'MONTH', 'YEAR']).agg(
    DailyProductSales=('QUANTITYORDERED', 'sum'),
    DailyRevenue=('TOTALREVENUE', 'sum')
).reset_index()

# 3. Geographical performance
country_summary = df.groupby('COUNTRY').agg(
    TotalRevenue=('TOTALREVENUE', 'sum'),
    TotalOrders=('ORDERNUMBER', 'nunique')
).reset_index()

# 4. Time-based summaries
monthly_summary = df.groupby(['YEAR', 'MONTH']).agg(
    MonthlyRevenue=('TOTALREVENUE', 'sum'),
    MonthlyOrders=('ORDERNUMBER', 'nunique')
).reset_index()

# 5. Additional Feature Engineering
# Days since last order per customer
last_order = df.groupby('CUSTOMERNAME')['ORDERDATE'].transform('max')
df['DaysSinceLastOrder'] = (last_order - df['ORDERDATE']).dt.days

# Order frequency per month per customer
df['OrderMonth'] = df['ORDERDATE'].dt.to_period('M')
order_freq = df.groupby(['CUSTOMERNAME', 'OrderMonth']).size().groupby('CUSTOMERNAME').mean().reset_index(name='OrderFrequency')

# Merge features back to main df
df = df.merge(cust_summary, on='CUSTOMERNAME', how='left')
df = df.merge(order_freq, on='CUSTOMERNAME', how='left')

# -------------------------------
# Save transformed dataset
# -------------------------------
df.to_csv(processed_file_path, index=False)
print(f"Transformed data saved to: {processed_file_path}")
print("Transformed data shape:", df.shape)
print(df.head())
