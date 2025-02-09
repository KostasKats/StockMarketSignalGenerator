# Stock Trading Signal Generator

📈 Stock Trading Signal Generator – Algorithmic Strategies for Smarter Trading

This repository is designed to generate high-precision stock trading signals using Python and technical analysis. <br> It integrates moving averages (MA), RSI, MACD, and reversal signals to identify buy and sell opportunities across different investment strategies (short-term, mid-term, and long-term).

🔹 Key Features:

✅ Dynamic Indicator Weighting – Different weight distributions for BUY and SELL signals to enhance accuracy.<br>
✅ Risk-Based Strategies – Supports both low-risk (conservative) and high-risk (aggressive) trading styles.<br>
✅ Trend-Optimized MACD Signals – MACD is emphasized in mid-term strategies for stronger trend confirmation.<br>
✅ Intelligent Signal Filtering – Avoids false signals by using momentum-based validation.<br>
✅ Fully Customizable – Adjust indicator weights, risk profiles, and trading styles to fit different market conditions.<br>

🚀 Optimized for traders and quants who want automated, data-driven trading strategies!

## Technologies Used
- **Python**: Core programming language.
- **pandas**: Data manipulation and analysis.
- **numpy**: Numerical computations.
- **matplotlib**: Data visualization.
- **yfinance**: Market data retrieval.

## Installation
```bash
# Clone the repository
git clone https://github.com/KostasKats/StockMarketSignalGenerator.git
cd [your-repo-name](https://github.com/KostasKats/StockMarketSignalGenerator)

# Install dependencies
pip install -r requirements.txt
```

## Usage
```python
import pandas as pd
import yfinance as yf

# Example: Create Market Signals
    monitor_stocks(InvestType.MID.value, Region.US.value, RiskType.LOW_RISK.value)

```

## Contributing
Contributions, feedback, and suggestions are welcome to enhance the project's functionality and accuracy. Feel free to open issues or submit pull requests.

## License
This project is licensed under the [MIT License](LICENSE).
