import os
import pandas as pd
import pytest

# Get project root (2 levels up from test file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROCESSED_FILE = os.path.join(PROJECT_ROOT, "data", "processed", "transformed_sales_data.csv")

# Test if file exists
def test_file_exists():
    assert os.path.exists(PROCESSED_FILE), f"{PROCESSED_FILE} not found"

# Test if required columns exist
def test_required_columns():
    df = pd.read_csv(PROCESSED_FILE)
    required_columns = ['ORDERNUMBER', 'QUANTITYORDERED', 'PRICEEACH', 'ORDERDATE', 'PRODUCTLINE']
    for col in required_columns:
        assert col in df.columns, f"Column {col} not found in {PROCESSED_FILE}"

# Test if there are no negative sales
def test_no_negative_sales():
    df = pd.read_csv(PROCESSED_FILE)
    assert (df['QUANTITYORDERED'] >= 0).all(), "Negative quantity found"
    assert (df['PRICEEACH'] >= 0).all(), "Negative price found"

# Test if ORDERDATE can be parsed as datetime
def test_orderdate_parsable():
    df = pd.read_csv(PROCESSED_FILE)
    try:
        pd.to_datetime(df['ORDERDATE'])
    except Exception as e:
        pytest.fail(f"ORDERDATE column cannot be parsed as datetime: {e}")
