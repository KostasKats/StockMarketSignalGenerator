import yfinance as yf
import logging
import time
from PredictEngine import calculate_indicators,generate_signals
from enums import TopCompanies
from enums.StockTicketType import InvestType
from colorama import Fore, Style, init
from enums.Regions import Region
from enums.RiskType import RiskType


init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def fetch_stock_data(ticker, investType):
    timeframes = {
        'SHORT': ('1d', '5m'),  # Fetching 1-day data with 5-minute intervals for real-time
        'MID': ('3mo', '1d'),
        'LONG': ('8mo', '1d')
    }

    period, interval = timeframes.get(investType, ('3mo', '1d'))  # Default to mid-term

    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval, prepost=True)  # Include pre/post-market data

    return data


def monitor_stocks(investType,region):
    while True:
        logging.info("-" * 50)
        logging.info("-" * 50)

        companies = ""

        if(region == Region.US.value):
            companies = TopCompanies.TOP_US_TECH_COMPANIES
        elif(region == Region.GR.value):
            companies = TopCompanies.TOP_GR_COMPANIES
        else:
            logging.ERROR("Unknown region");

        for ticker in companies:
            data = fetch_stock_data(ticker, investType)
            data = calculate_indicators(data, investType)
            signals = generate_signals(data, investType, RiskType.LOW_RISK.value)

            latest_signal = signals.iloc[-1]['Action']
            if latest_signal in ['Buy', 'Sell']:
                notify(latest_signal, ticker, data,region)

        time.sleep(300)


def notify(signal, ticker, data, region):
    # Extract latest data
    latest_price = data.iloc[-1]['Close']
    moving_avg = data.iloc[-1]['MA']
    rsi = data.iloc[-1]['RSI']

    signal_color = Fore.GREEN if signal == 'Buy' else Fore.RED
    signal_text = f"{signal_color}{signal: <4}{Style.RESET_ALL}"

    if region == Region.US.value:
        ticker_text = f"{Fore.BLUE}{ticker: <4}{Style.RESET_ALL}"
        price_text = f"{Fore.BLACK}Price:{Style.RESET_ALL}"
        ma_text = f"{Fore.BLACK}MA:{Style.RESET_ALL}"
        price_width = 7
        ma_width = 7
    elif region == Region.GR.value:
        ticker_text = f"{Fore.BLUE}{ticker: <8}{Style.RESET_ALL}"
        price_text = f"{Fore.BLACK}Price:{Style.RESET_ALL}"
        ma_text = f"{Fore.BLACK}MA:{Style.RESET_ALL}"
        price_width = 5
        ma_width = 5

    rsi_text = f"{Fore.BLACK}RSI:{Style.RESET_ALL}"

    message = (
        f"{Fore.BLACK}{Style.RESET_ALL} | {signal_text} | {ticker_text} | "
        f"{price_text} {Fore.BLACK}{latest_price: <{price_width}.2f}{Style.RESET_ALL} "
        f"| {ma_text} {Fore.BLACK}{moving_avg: <{ma_width}.2f}{Style.RESET_ALL} "
        f"| {rsi_text} {Fore.BLACK}{rsi:5.2f}{Style.RESET_ALL} "
    )
    logging.info(message)


if __name__ == "__main__":
    monitor_stocks(InvestType.MID.value, Region.GR.value, RiskType.HIGH_RISK.value)
