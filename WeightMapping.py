from StockTicketType import InvestType


WEIGHT_MAPPING = {
    InvestType.SHORT.value: {
        'MA_Signal': 0.35,  # Slightly reduced to favor reversals
        'RSI_Signal': 0.25,  # Lower weight since RSI can lag in short-term moves
        'MACD_Signal': 0.05,  # Small weight to catch micro-trends
        'Reversal_Signal': 0.35  # Higher weight since reversals matter most in short-term trading
    },
    InvestType.MID.value: {
        'MA_Signal': 0.50,  # MA still key but slightly reduced
        'RSI_Signal': 0.30,  # Balanced RSI contribution
        'MACD_Signal': 0.10,  # Increased to better confirm trend shifts
        'Reversal_Signal': 0.10  # Lower, as midterm trades rely less on reversals
    },
    InvestType.LONG.value: {
        'MA_Signal': 0.50,  # MA remains the highest weight for trend following
        'RSI_Signal': 0.10,  # RSI remains low as it can be misleading for long-term
        'MACD_Signal': 0.39,  # Increased to confirm major trend shifts
        'Reversal_Signal': 0.01  # Minimal impact of reversals in long-term investing
    }
}
