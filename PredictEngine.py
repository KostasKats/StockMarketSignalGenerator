import yfinance as yf
import pandas as pd
import ta
import PlotResults as plot
import pytz

def fetch_stock_data(ticker, period='6mo', interval='1d'):

    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    return data

def calculate_indicators(data):

    data['MA_50'] = ta.trend.sma_indicator(data['Close'], window=50)
    data['MA_200'] = ta.trend.sma_indicator(data['Close'], window=200)

    data['RSI'] = ta.momentum.rsi(data['Close'], window=14)

    macd = ta.trend.MACD(data['Close'])
    data['MACD'] = macd.macd()
    data['MACD_Signal'] = macd.macd_signal()

    return data

def generate_signals(data):
    """
    Generate buy/sell signals based on indicators, including weighted reversal detection.
    """
    signals = pd.DataFrame(index=data.index)
    signals['Price'] = data['Close']

    # Moving Average (MA) Signal
    signals['MA_Signal'] = 0
    signals.loc[data['Close'] < data['MA_50'] * (1 - 0.02), 'MA_Signal'] = 1  # Buy
    signals.loc[data['Close'] > data['MA_50'] * (1 + 0.02), 'MA_Signal'] = -1  # Sell

    # RSI Signal
    signals['RSI_Signal'] = 0
    signals.loc[data['RSI'] < 40, 'RSI_Signal'] = 1  # Buy
    signals.loc[data['RSI'] > 60, 'RSI_Signal'] = -1  # Sell

    # MACD Signal
    signals['MACD_Signal'] = 0
    signals.loc[data['MACD'] > data['MACD_Signal'], 'MACD_Signal'] = 1  # Buy
    signals.loc[data['MACD'] < data['MACD_Signal'], 'MACD_Signal'] = -1  # Sell

    # Reversal Signal (based on sharp price changes)
    signals['Reversal_Signal'] = 0
    price_change = data['Close'].pct_change()  # Percentage change

    # ✅ Strong Buy if price drops > 5% (indicating a potential rebound opportunity)
    signals.loc[price_change < -0.05, 'Reversal_Signal'] = 1

    # ✅ Strong Sell if price increases > 4% (indicating a potential overbought condition)
    signals.loc[price_change > 0.04, 'Reversal_Signal'] = -1

    # Default action
    signals['Action'] = 'Hold'

    # Weighted decision-making
    buy_condition = (
                            (signals['MA_Signal'] == 1).astype(int) * 0.50 +
                            (signals['RSI_Signal'] == 1).astype(int) * 0.20 +
                            (signals['MACD_Signal'] == 1).astype(int) * 0.10 +
                            (signals['Reversal_Signal'] == 1).astype(int) * 0.20
                    ) >= 0.5

    sell_condition = (
                             (signals['MA_Signal'] == -1).astype(int) * 0.50 +
                             (signals['RSI_Signal'] == -1).astype(int) * 0.20 +
                             (signals['MACD_Signal'] == -1).astype(int) * 0.10 +
                             (signals['Reversal_Signal'] == -1).astype(int) * 0.20
                     ) >= 0.5

    # Assign actions
    signals.loc[buy_condition, 'Action'] = 'Buy'
    signals.loc[sell_condition, 'Action'] = 'Sell'

    return signals



def main(ticker):
    # Example usage
    data = fetch_stock_data(ticker)
    data = calculate_indicators(data)
    signals = generate_signals(data)

    # Assuming signals is a pandas DataFrame with timezone-aware datetime
    athens_tz = pytz.timezone('Europe/Athens')
    # Directly convert to Athens timezone if it's already timezone-aware
    signals = signals.tz_convert(athens_tz)

    print(signals.tail())

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