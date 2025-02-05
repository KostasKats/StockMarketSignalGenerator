import yfinance as yf
import pandas as pd
import ta

def fetch_stock_data(ticker, period='6mo', interval='1d'):
    """
    Fetch historical stock data.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    return data

def calculate_indicators(data):
    """
    Calculate technical indicators.
    """
    # Moving Averages
    data['MA_50'] = ta.trend.sma_indicator(data['Close'], window=50)
    data['MA_200'] = ta.trend.sma_indicator(data['Close'], window=200)

    # RSI
    data['RSI'] = ta.momentum.rsi(data['Close'], window=14)

    # MACD
    macd = ta.trend.MACD(data['Close'])
    data['MACD'] = macd.macd()
    data['MACD_Signal'] = macd.macd_signal()

    return data

def generate_signals(data):
    """
    Generate buy/sell signals based on indicators.
    """
    signals = pd.DataFrame(index=data.index)
    signals['Price'] = data['Close']

    # Initialize MA Signal column with 0 (hold)
    signals['MA_Signal'] = 0

    # Buy Condition: Price < MA_50 - threshold (percentage below MA50)
    signals.loc[data['Close'] < data['MA_50'] * (1 - 0.02), 'MA_Signal'] = 1  # Buy

    # Sell Condition: Price > MA_50 + threshold (percentage above MA50)
    signals.loc[data['Close'] > data['MA_50'] * (1 + 0.02), 'MA_Signal'] = -1  # Sell

    signals['RSI_Signal'] = 0
    signals.loc[data['RSI'] < 40, 'RSI_Signal'] = 1  # Buy
    signals.loc[data['RSI'] > 65, 'RSI_Signal'] = -1  # Sell

    signals['MACD_Signal'] = 0
    signals.loc[data['MACD'] > data['MACD_Signal'], 'MACD_Signal'] = 1  # Buy
    signals.loc[data['MACD'] < data['MACD_Signal'], 'MACD_Signal'] = -1  # Sell

    signals['Action'] = 'Hold'  # Default action

    # Weighted decision making
    buy_condition = (
        (signals['MA_Signal'] == 1).astype(int) * 0.4 +
        (signals['RSI_Signal'] == 1).astype(int) * 0.3 +
        (signals['MACD_Signal'] == 1).astype(int) * 0.3
    ) >= 0.5

    sell_condition = (
        (signals['MA_Signal'] == -1).astype(int) * 0.4 +
        (signals['RSI_Signal'] == -1).astype(int) * 0.3 +
        (signals['MACD_Signal'] == -1).astype(int) * 0.3
    ) >= 0.5

    # Assign actions
    signals.loc[buy_condition, 'Action'] = 'Buy'
    signals.loc[sell_condition, 'Action'] = 'Sell'

    return signals

# Example usage
ticker = 'AAPL'
data = fetch_stock_data(ticker)
data = calculate_indicators(data)
signals = generate_signals(data)

print(signals.tail())


def main(ticker):
    # Fetch data
    data = fetch_stock_data(ticker)

    # Calculate indicators
    data = calculate_indicators(data)

    # Generate signals
    signals = generate_signals(data)

    # Plot signals
    plot.plot_signals(data, signals)

    # Print latest signal
    latest_signal = signals.iloc[-1]['Action']
    print(f"Latest Signal for {ticker}: {latest_signal}")

if __name__ == "__main__":
    main('NVDA')