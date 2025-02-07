import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta
from StockTicketType import InvestType;

def plot_signals(data, signals,investType,ticker):

    last_date = data.index.max()

    if(investType == InvestType.SHORT.value):
        start_date = last_date - timedelta(days=7)  # Approx. 1 week
    elif(investType == InvestType.MID.value):
        start_date = last_date - timedelta(days=60)  # Approx. 2 months
    elif(investType == InvestType.LONG.value):
        start_date = last_date - timedelta(days=90)  # Approx. 3 months

    data_filtered = data.loc[start_date:]
    signals_filtered = signals.loc[start_date:]

    plt.figure(figsize=(14, 7))
    plt.plot(data_filtered['Close'], label='Close Price', alpha=0.7, color='blue')

    buy_signals = signals_filtered[signals_filtered['Action'] == 'Buy']
    plt.scatter(buy_signals.index, data_filtered.loc[buy_signals.index, 'Close'],
                marker='^', color='g', s=100, label='Buy Signal', alpha=1.0)

    sell_signals = signals_filtered[signals_filtered['Action'] == 'Sell']
    plt.scatter(sell_signals.index, data_filtered.loc[sell_signals.index, 'Close'],
                marker='v', color='r', s=100, label='Sell Signal', alpha=1.0)

    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))  # Major ticks every week
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()  # Auto-rotate date labels

    plt.title(f'Stock Price with Buy/Sell Signals for {ticker.upper()} ({investType.capitalize()} Investment)',
              fontsize=18, fontweight='bold')
    plt.xlabel('Date', fontsize=15, fontweight='bold')
    plt.ylabel('Price', fontsize=15, fontweight='bold')
    plt.grid(True, which='both', linestyle='--', alpha=0.3)

    plt.legend()
    plt.tight_layout()
    plt.show()
