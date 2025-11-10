import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/processed/transformed_sales_data.csv")

def load_df():
    return pd.read_csv(DATA_PATH)

def test_file_exists():
    assert os.path.exists(DATA_PATH), f"transformed.csv not found at {DATA_PATH}"

def test_required_columns():
    df = load_df()
    required = ['ORDERNUMBER','ORDERDATE','CUSTOMERNAME','PRODUCTLINE','QUANTITYORDERED','PRICEEACH','SALES']
    missing = [c for c in required if c not in df.columns]
    assert not missing, f"Missing required columns: {missing}"

def test_no_negative_sales():
    df = load_df()
    assert (df['SALES'] >= 0).all(), "Negative SALES values present"

def test_orderdate_parsable():
    df = load_df()
    # try to parse ORDERDATE
    parsed = pd.to_datetime(df['ORDERDATE'], errors='coerce')
    assert parsed.notna().all(), "Some ORDERDATE values are not parseable"