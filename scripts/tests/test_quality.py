import pandas as pd
import os

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'transformed_sales_data.csv')

# -------------------------------
# Helper function
# -------------------------------
def load_df():
    return pd.read_csv(DATA_PATH)

# -------------------------------
# Tests
# -------------------------------
def test_file_exists():
    """Check if transformed CSV exists"""
    assert os.path.exists(DATA_PATH), f"transformed_sales_data.csv not found at {DATA_PATH}"

def test_required_columns():
    """Check required columns exist"""
    df = load_df()
    required = [
        'ORDERNUMBER',
        'ORDERDATE',
        'CUSTOMERNAME',
        'PRODUCTLINE',
        'QUANTITYORDERED',
        'PRICEEACH',
        'SALES',
        'TOTALREVENUE'
    ]
    missing = [c for c in required if c not in df.columns]
    assert not missing, f"Missing required columns: {missing}"

def test_no_negative_sales():
    """Check SALES values are non-negative"""
    df = load_df()
    assert (df['SALES'] >= 0).all(), "Negative SALES values present"

def test_orderdate_parsable():
    """Check ORDERDATE can be parsed as datetime"""
    df = load_df()
    parsed = pd.to_datetime(df['ORDERDATE'], errors='coerce')
    assert parsed.notna().all(), "Some ORDERDATE values are not parseable"
