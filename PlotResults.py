import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta

def plot_signals(data, signals):
    """
    Plot stock price and buy/sell signals for the last 3 months.
    """
    # Filter data for the last 3 months
    last_date = data.index.max()
    start_date = last_date - timedelta(days=90)  # Approx. 3 months
    data_filtered = data.loc[start_date:]
    signals_filtered = signals.loc[start_date:]

    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(data_filtered['Close'], label='Close Price', alpha=0.7, color='blue')

    # Plot Buy Signals
    plt.plot(signals_filtered.loc[signals_filtered['Action'] == 'Buy'].index,
             data_filtered['Close'][signals_filtered['Action'] == 'Buy'],
             '^', markersize=10, color='g', lw=0, label='Buy Signal')

    # Plot Sell Signals
    plt.plot(signals_filtered.loc[signals_filtered['Action'] == 'Sell'].index,
             data_filtered['Close'][signals_filtered['Action'] == 'Sell'],
             'v', markersize=10, color='r', lw=0, label='Sell Signal')

    # Improve Date Formatting
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))  # Major ticks every week
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()  # Auto-rotate date labels

    # Title and Grid
    plt.title('Stock Price with Buy/Sell Signals (Last 3 Months)', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(alpha=0.3)

    plt.legend()
    plt.tight_layout()
    plt.show()
