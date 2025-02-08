import pandas as pd
import ta
import numpy as np
from enums import RiskType, WeightMapping
import PlotResults as plot
import pytz
from enums.StockTicketType import InvestType
import yfinance as yf
from enums.RiskType import RiskType


def fetch_stock_data(ticker, investType):
    timeframes = {
        InvestType.SHORT.value: ('14d', '30m'),  # 🔹 Using 14 days instead of 1 month for better accuracy
        InvestType.MID.value: ('3mo', '1d'),
        InvestType.LONG.value: ('8mo', '1d')
    }

    period, interval = timeframes.get(investType, ('3mo', '1d'))  # Default to mid-term

    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval, prepost=True)  # 🔹 Include pre/post-market data

    return data


def calculate_indicators(data, investType):
    ma_windows = {
        InvestType.SHORT.value: 10,
        InvestType.MID.value: 50,
        InvestType.LONG.value: 200
    }
    window = ma_windows.get(investType, 50)  # Default to midterm MA

    data['MA'] = ta.trend.sma_indicator(data['Close'], window=window)
    data['RSI'] = ta.momentum.rsi(data['Close'], window=14)

    macd = ta.trend.MACD(data['Close'])
    data['MACD'] = macd.macd()
    data['MACD_Signal'] = macd.macd_signal()

    return data

def create_low_risk_indexes(data):
    signals = pd.DataFrame(index=data.index)
    signals['Price'] = data['Close']

    signals['MA_Signal'] = np.where(data['Close'] < data['MA'] * 0.90, 1,
                                    np.where(data['Close'] > data['MA'] * 1.05, -1, 0))

    signals['RSI_Signal'] = np.where(data['RSI'] < 38, 1,
                                     np.where(data['RSI'] > 67, -1, 0))

    signals['MACD_Signal'] = np.where(data['MACD'] > data['MACD_Signal'], 1,
                                      np.where(data['MACD'] < data['MACD_Signal'], -1, 0))

    price_change = data['Close'].pct_change()
    signals['Reversal_Signal'] = np.where(price_change < -0.05, 1,  # Lower volatility tolerance
                                          np.where(price_change > 0.10, -1, 0))

    return signals


def create_high_risk_indexes(data):
    signals = pd.DataFrame(index=data.index)
    signals['Price'] = data['Close']

    signals['MA_Signal'] = np.where(data['Close'] < data['MA'] * 0.95, 1,
                                    np.where(data['Close'] > data['MA'] * 1.2, -1, 0))

    signals['RSI_Signal'] = np.where(data['RSI'] < 45, 1,
                                     np.where(data['RSI'] > 70, -1, 0))

    signals['MACD_Signal'] = np.where(data['MACD'] > data['MACD_Signal'], 1,
                                      np.where(data['MACD'] < data['MACD_Signal'], -1, 0))

    price_change = data['Close'].pct_change()
    signals['Reversal_Signal'] = np.where(price_change < -0.10, 1,  # Higher volatility tolerance
                                          np.where(price_change > 0.20, -1, 0))

    return signals


def generate_signals(data, investType, riskType):
    signals = pd.DataFrame(index=data.index)
    signals['Price'] = data['Close']


    if(riskType == RiskType.LOW_RISK.value):
        weights = WeightMapping.WEIGHT_MAPPING_LOW_RISK.get(investType, None)
        signals = create_low_risk_indexes(data)
    elif(riskType == RiskType.HIGH_RISK.value):
        weights = WeightMapping.WEIGHT_MAPPING_HIGH_RISK.get(investType, None)
        signals = create_high_risk_indexes(data)

    if weights is None or len(weights) == 0:
        raise ValueError(f"Error: No weight mapping found for investType '{investType}'")

    buy_score = (signals[['MA_Signal', 'RSI_Signal', 'MACD_Signal', 'Reversal_Signal']] == 1) @ np.array(list(weights.values()))
    sell_score = (signals[['MA_Signal', 'RSI_Signal', 'MACD_Signal', 'Reversal_Signal']] == -1) @ np.array(list(weights.values()))

    signals.loc[buy_score >= 0.5, 'Action'] = 'Buy'
    signals.loc[sell_score >= 0.5, 'Action'] = 'Sell'

    return signals


def createSignals(ticker,investType, riskType):
    data = fetch_stock_data(ticker,investType)
    print(ticker)
    data = calculate_indicators(data,investType)
    signals = generate_signals(data,investType,riskType)

    athens_tz = pytz.timezone('Europe/Athens')
    signals = signals.tz_convert(athens_tz)

    print_signals(signals)

    plot.plot_signals(data, signals,investType,ticker)

    latest_signal = signals.iloc[-1]['Action']
    print(f"Latest Signal for {ticker}: {latest_signal}")

def print_signals(signals):
    columns_to_display = ['Price', 'MA_Signal', 'RSI_Signal', 'MACD_Signal', 'Reversal_Signal', 'Action']

    available_columns = [col for col in columns_to_display if col in signals.columns]

    print(signals[available_columns].tail(5))  # Show the last 10 entries


if __name__ == "__main__":
    # UiInitializer.create_ui()
    createSignals('AAPL', InvestType.MID.value, RiskType.HIGH_RISK.value)