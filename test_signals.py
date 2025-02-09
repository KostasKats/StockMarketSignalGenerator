import pytest
from datetime import datetime, timedelta
from SignalsGenerator import fetch_stock_data, calculate_indicators  # Import your functions

# 📌 Use a Fixed Date Range to Ensure Consistency
TEST_TICKER = "AAPL"  # Change this to any stock you want to test
START_DATE = datetime.today() - timedelta(days=90)  # Test with the last 3 months of data
INVEST_TYPE = "MID"  # Test midterm strategy (you can change this)


# ✅ Load Historical Data for Testing
@pytest.fixture
def historical_data():
    """Fetch historical stock data for testing."""
    data = fetch_stock_data(TEST_TICKER, INVEST_TYPE)
    assert not data.empty, "Error: No data returned from Yahoo Finance"
    return data


# ✅ Test Moving Averages, RSI, MACD, and Reversal Calculation
def test_calculate_indicators(historical_data):
    data = calculate_indicators(historical_data, INVEST_TYPE)

    assert 'MA' in data.columns, "Error: Moving Average (MA) not calculated"
    assert 'RSI' in data.columns, "Error: RSI not calculated"
    assert 'MACD' in data.columns, "Error: MACD not calculated"
    assert 'MACD_Signal' in data.columns, "Error: MACD Signal not calculated"

    # Check that indicators contain valid values
    assert data['MA'].notnull().sum() > 0, "Error: MA contains NaN values"
    assert data['RSI'].notnull().sum() > 0, "Error: RSI contains NaN values"
    assert data['MACD'].notnull().sum() > 0, "Error: MACD contains NaN values"




