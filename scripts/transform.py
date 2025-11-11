import pandas as pd
import os

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_PATH = os.path.join(BASE_DIR, "data", "clean", "cleaned_sales_data.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)
PROCESSED_FILE = os.path.join(PROCESSED_DIR, "transformed_sales_data.csv")

# -------------------------------
# Load data
# -------------------------------
df = pd.read_csv(CLEAN_PATH)
print("Initial shape:", df.shape)

# -------------------------------
# Basic transformations
# -------------------------------
if 'SALES' not in df.columns:
    df['SALES'] = df['QUANTITYORDERED'] * df['PRICEEACH']
df['TOTALREVENUE'] = df['SALES']

df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')
df = df[df['ORDERDATE'].notna()]
df['DAY'] = df['ORDERDATE'].dt.day
df['MONTH'] = df['ORDERDATE'].dt.month
df['YEAR'] = df['ORDERDATE'].dt.year

# -------------------------------
# Feature engineering
# -------------------------------
cust_summary = df.groupby('CUSTOMERNAME').agg(
    LifetimeValue=('TOTALREVENUE', 'sum'),
    AvgOrderValue=('TOTALREVENUE', 'mean'),
    TotalOrders=('ORDERNUMBER', 'nunique')
).reset_index()

last_order = df.groupby('CUSTOMERNAME')['ORDERDATE'].transform('max')
df['DaysSinceLastOrder'] = (last_order - df['ORDERDATE']).dt.days

df['OrderMonth'] = df['ORDERDATE'].dt.to_period('M')
order_freq = df.groupby(['CUSTOMERNAME', 'OrderMonth']).size().groupby('CUSTOMERNAME').mean().reset_index(name='OrderFrequency')

df = df.merge(cust_summary, on='CUSTOMERNAME', how='left')
df = df.merge(order_freq, on='CUSTOMERNAME', how='left')

# -------------------------------
# Save transformed dataset
# -------------------------------
df.to_csv(PROCESSED_FILE, index=False)
print(f"✅ Transformed data saved to: {PROCESSED_FILE}")
