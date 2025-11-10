import pandas as pd
import numpy as np
import os

def clean_sales_data(raw_file_path, clean_folder="../data/clean/"):
    """
    Reads raw sales CSV, performs professional data cleaning,
    and saves cleaned data to a new CSV in the clean folder.

    Parameters:
    - raw_file_path: path to raw CSV
    - clean_folder: folder to save cleaned CSV (default: ../data/clean/)

    Returns:
    - Cleaned pandas DataFrame
    """
    # -------------------------------
    # 1. Load CSV safely
    # -------------------------------
    try:
        data = pd.read_csv(raw_file_path, encoding='latin1')
    except Exception as e:
        print("Error reading CSV:", e)
        return None

    print("Initial shape:", data.shape)

    # -------------------------------
    # 2. Handle missing values
    # -------------------------------
    # Numeric columns: fill missing with median
    numeric_cols = data.select_dtypes(include=['int64','float64']).columns
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())

    # Categorical columns: fill missing appropriately
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

    # -------------------------------
    # 3. Remove duplicates
    # -------------------------------
    data = data.drop_duplicates()

    # -------------------------------
    # 4. Fix data types
    # -------------------------------
    if 'ORDERDATE' in data.columns:
        data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'], errors='coerce')
        data = data[data['ORDERDATE'].notna()]  # drop rows with invalid dates

    cols_to_numeric = ['ORDERNUMBER', 'QUANTITYORDERED', 'PRICEEACH', 'ORDERLINENUMBER', 'SALES', 'MSRP']
    for col in cols_to_numeric:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')

    # -------------------------------
    # 5. Clean categorical text
    # -------------------------------
    for col in categorical_cols:
        data[col] = data[col].astype(str).str.strip()
        data[col] = data[col].str.title()

    if 'COUNTRY' in data.columns:
        data['COUNTRY'] = data['COUNTRY'].str.upper()

    # -------------------------------
    # 6. Clean numeric inconsistencies
    # -------------------------------
    for col in ['QUANTITYORDERED', 'PRICEEACH', 'SALES']:
        if col in data.columns:
            data = data[data[col] >= 0]

    # -------------------------------
    # 7. Clean phone numbers
    # -------------------------------
    if 'PHONE' in data.columns:
        data['PHONE'] = data['PHONE'].astype(str).str.replace(r'\D', '', regex=True)

    # -------------------------------
    # 8. Feature Engineering
    # -------------------------------
    if 'QUANTITYORDERED' in data.columns and 'PRICEEACH' in data.columns:
        data['SALES'] = data['QUANTITYORDERED'] * data['PRICEEACH']

    if 'ORDERDATE' in data.columns and pd.api.types.is_datetime64_any_dtype(data['ORDERDATE']):
        data['DAY'] = data['ORDERDATE'].dt.day
        data['MONTH'] = data['ORDERDATE'].dt.month
        data['YEAR'] = data['ORDERDATE'].dt.year
    else:
        print("Warning: ORDERDATE column is not datetime. Skipping date extraction.")

    if 'DEALSIZE' in data.columns:
        size_map = {'Small': 1, 'Medium': 2, 'Large': 3}
        data['DEALSIZE_NUM'] = data['DEALSIZE'].map(size_map)

    # -------------------------------
    # 9. Save cleaned data
    # -------------------------------
    os.makedirs(clean_folder, exist_ok=True)
    clean_file_path = os.path.join(clean_folder, "cleaned_sales_data.csv")
    data.to_csv(clean_file_path, index=False)
    print(f"Cleaned data saved to: {clean_file_path}")

    # -------------------------------
    # 10. Final checks
    # -------------------------------
    print("\nCleaned data info:")
    print(data.info())
    print("\nMissing values after cleaning:")
    print(data.isnull().sum())
    print("\nSample data:")
    print(data.head())

    return data

# -------------------------------
# Example usage when running script directly
# -------------------------------
if __name__ == "__main__":
    raw_path = "../data/raw/sales_data.csv"
    clean_sales_data(raw_path)
