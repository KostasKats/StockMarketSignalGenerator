import matplotlib.pyplot as plt

def plot_signals(data, signals):
    """
    Plot stock price and buy/sell signals.
    """
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)

    # Plot Buy Signals
    plt.plot(signals.loc[signals['Action'] == 'Buy'].index,
             data['Close'][signals['Action'] == 'Buy'],
             '^', markersize=10, color='g', lw=0, label='Buy')

    # Plot Sell Signals
    plt.plot(signals.loc[signals['Action'] == 'Sell'].index,
             data['Close'][signals['Action'] == 'Sell'],
             'v', markersize=10, color='r', lw=0, label='Sell')

    plt.title('Stock Price with Buy/Sell Signals')
    plt.legend()
    plt.show()