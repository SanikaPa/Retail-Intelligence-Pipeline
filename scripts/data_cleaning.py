import pandas as pd
import numpy as np
import os

# -------------------------------
# Set base paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
CLEAN_DIR = os.path.join(BASE_DIR, "data", "clean")
os.makedirs(CLEAN_DIR, exist_ok=True)

def clean_sales_data(raw_file_path):
    """
    Reads raw sales CSV, performs cleaning, and saves cleaned data to /data/clean.
    """
    try:
        data = pd.read_csv(raw_file_path, encoding='latin1')
    except Exception as e:
        print("Error reading CSV:", e)
        return None

    print("Initial shape:", data.shape)

    # Fill missing numeric values with median
    numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())

    # Fill missing categorical values
    categorical_cols = data.select_dtypes(include='object').columns
    for col in categorical_cols:
        if col == "ADDRESSLINE2":
            data[col] = data[col].fillna("")
        elif col == "STATE":
            data[col] = data[col].fillna("Unknown")
        elif col == "TERRITORY":
            data[col] = data[col].fillna(data[col].mode()[0])
        else:
            data[col] = data[col].fillna(data[col].mode()[0])

    # Remove duplicates
    data = data.drop_duplicates()

    # Fix ORDERDATE type
    if 'ORDERDATE' in data.columns:
        data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'], errors='coerce')
        data = data[data['ORDERDATE'].notna()]

    # Convert numeric columns
    cols_to_numeric = ['ORDERNUMBER', 'QUANTITYORDERED', 'PRICEEACH', 'ORDERLINENUMBER', 'SALES', 'MSRP']
    for col in cols_to_numeric:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')

    # Clean text
    for col in categorical_cols:
        data[col] = data[col].astype(str).str.strip().str.title()

    if 'COUNTRY' in data.columns:
        data['COUNTRY'] = data['COUNTRY'].str.upper()

    # Remove negative numbers
    for col in ['QUANTITYORDERED', 'PRICEEACH', 'SALES']:
        if col in data.columns:
            data = data[data[col] >= 0]

    # Clean phone numbers
    if 'PHONE' in data.columns:
        data['PHONE'] = data['PHONE'].astype(str).str.replace(r'\D', '', regex=True)

    # Feature engineering
    if 'QUANTITYORDERED' in data.columns and 'PRICEEACH' in data.columns:
        data['SALES'] = data['QUANTITYORDERED'] * data['PRICEEACH']

    if 'ORDERDATE' in data.columns:
        data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'], errors='coerce')

        data['DAY'] = data['ORDERDATE'].dt.day
        data['MONTH'] = data['ORDERDATE'].dt.month
        data['YEAR'] = data['ORDERDATE'].dt.year

    if 'DEALSIZE' in data.columns:
        size_map = {'Small': 1, 'Medium': 2, 'Large': 3}
        data['DEALSIZE_NUM'] = data['DEALSIZE'].map(size_map)

    # Save cleaned data
    clean_path = os.path.join(CLEAN_DIR, "cleaned_sales_data.csv")
    data.to_csv(clean_path, index=False)
    print(f"✅ Cleaned data saved to: {clean_path}")
    return data

if __name__ == "__main__":
    raw_path = os.path.join(RAW_DIR, "sales_data.csv")
    clean_sales_data(raw_path)