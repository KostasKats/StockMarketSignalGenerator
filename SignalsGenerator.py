import pandas as pd
import ta
import numpy as np
from enums import RiskType
import enums.WeightMapping as weights
from plot import PlotResults as plot
import pytz
from enums.InvestType import InvestType
import yfinance as yf
from enums.RiskType import RiskType


def fetch_stock_data(ticker, investType):
    timeframes = {
        InvestType.SHORT.value: ('14d', '30m'),
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

    THRESHOLD_MA_BUY = 0.90
    THRESHOLD_MA_SELL = 1.05

    bullish_trend = (data['Close'] > data['MA']) & (data['RSI'] > 50) & (data['MACD'] > 0)

    signals['MA_Signal'] = np.where(data['Close'] < data['MA'] * THRESHOLD_MA_BUY, 1,
                                    np.where(data['Close'] > data['MA'] * THRESHOLD_MA_SELL, -1, 0))

    signals['RSI_Signal'] = np.where(data['RSI'] < 38, 1,
                                     np.where(data['RSI'] > 67, -1, 0))

    # Use macd mostly to catch bullish trends
    signals['MACD_Signal'] = np.where((data['MACD'] > data['MACD_Signal']) & bullish_trend, 1,
                                      np.where((data['MACD'] < data['MACD_Signal']), -1, 0))

    price_change = data['Close'].pct_change()
    signals['Reversal_Signal'] = np.where(price_change < -0.05, 1,  # Lower volatility tolerance
                                          np.where(price_change > 0.10, -1, 0))

    return signals


def create_high_risk_indexes(data):
    signals = pd.DataFrame(index=data.index)
    signals['Price'] = data['Close']

    THRESHOLD_MA_BUY = 0.95
    THRESHOLD_MA_SELL = 1.2

    bullish_trend = (data['Close'] > data['MA']) & (data['RSI'] > 50) & (data['MACD'] > 0)

    signals['MA_Signal'] = np.where(data['Close'] < data['MA'] * THRESHOLD_MA_BUY, 1,
                                    np.where(data['Close'] > data['MA'] * THRESHOLD_MA_SELL, -1, 0))

    signals['RSI_Signal'] = np.where(data['RSI'] < 45, 1,
                                     np.where(data['RSI'] > 70, -1, 0))

    signals['MACD_Signal'] = np.where((data['MACD'] > data['MACD_Signal']) & bullish_trend, 1,
                                      np.where((data['MACD'] < data['MACD_Signal']), -1, 0))

    price_change = data['Close'].pct_change()
    signals['Reversal_Signal'] = np.where(price_change < -0.10, 1,  # Higher volatility tolerance
                                          np.where(price_change > 0.20, -1, 0))

    return signals


def generate_signals(data, investType, riskType):
    signals = pd.DataFrame(index=data.index)
    signals['Price'] = data['Close']

    # Select the right risk mapping and compute signals
    if riskType == RiskType.LOW_RISK.value:
        buy_weights = weights.WEIGHT_MAPPING_LOW_RISK_BUY.get(investType, None)
        sell_weights = weights.WEIGHT_MAPPING_LOW_RISK_SELL.get(investType, None)
        signals = create_low_risk_indexes(data)
    elif riskType == RiskType.HIGH_RISK.value:
        buy_weights = weights.WEIGHT_MAPPING_HIGH_RISK_BUY.get(investType, None)
        sell_weights = weights.WEIGHT_MAPPING_HIGH_RISK_SELL.get(investType, None)
        signals = create_high_risk_indexes(data)

    if buy_weights is None or sell_weights is None:
        raise ValueError(f"Error: No weight mapping found for investType '{investType}'")

    # 1️⃣ Create raw BUY/SELL signals BEFORE applying weights
    signals['Buy_Signal'] = (signals['MA_Signal'] == 1) | (signals['RSI_Signal'] == 1) | (signals['MACD_Signal'] == 1) | (signals['Reversal_Signal'] == 1)
    signals['Sell_Signal'] = (signals['MA_Signal'] == -1) | (signals['RSI_Signal'] == -1) | (signals['MACD_Signal'] == -1) | (signals['Reversal_Signal'] == -1)

    # 2️⃣ Apply separate weights for BUY and SELL signals
    buy_score = (signals[['MA_Signal', 'RSI_Signal', 'MACD_Signal', 'Reversal_Signal']] == 1) @ np.array(list(buy_weights.values()))
    sell_score = (signals[['MA_Signal', 'RSI_Signal', 'MACD_Signal', 'Reversal_Signal']] == -1) @ np.array(list(sell_weights.values()))

    # 3️⃣ Assign final BUY or SELL action based on weighted scores
    signals['Action'] = 'Hold'  # Default action
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

    print(signals[available_columns].tail(5))


if __name__ == "__main__":
    # UiInitializer.create_ui()
    createSignals('AMD', InvestType.MID.value, RiskType.LOW_RISK.value)