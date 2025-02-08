from enums.StockTickerType import InvestType

WEIGHT_MAPPING_HIGH_RISK = {
    InvestType.SHORT.value: {
        'MA_Signal': 0.35,
        'RSI_Signal': 0.25,
        'MACD_Signal': 0.10,  # Increased to catch micro-trends more effectively
        'Reversal_Signal': 0.30  # Reduced slightly to prevent excessive false signals
    },
    InvestType.MID.value: {
        'MA_Signal': 0.50,
        'RSI_Signal': 0.30,
        'MACD_Signal': 0.15,  # Slightly higher to improve trend shift detection
        'Reversal_Signal': 0.05  # Lowered to avoid overreacting to minor pullbacks
    },
    InvestType.LONG.value: {
        'MA_Signal': 0.50,
        'RSI_Signal': 0.15,  # Increased RSI slightly to help confirm trends earlier
        'MACD_Signal': 0.35,  # Reduced a bit to balance RSI
        'Reversal_Signal': 0.00  # Completely removed since reversals are irrelevant in long-term
    }
}


WEIGHT_MAPPING_LOW_RISK = {
    InvestType.SHORT.value: {
        'MA_Signal': 0.50,
        'RSI_Signal': 0.35,  # Slightly reduced to balance
        'MACD_Signal': 0.05,  # Small weight added to still consider trend confirmation
        'Reversal_Signal': 0.10
    },
    InvestType.MID.value: {
        'MA_Signal': 0.50,
        'RSI_Signal': 0.35,  # Reduced slightly to avoid overreliance
        'MACD_Signal': 0.10,  # Increased to improve trend shift confirmation
        'Reversal_Signal': 0.05
    },
    InvestType.LONG.value: {
        'MA_Signal': 0.50,
        'RSI_Signal': 0.25,  # Increased to help detect divergences earlier
        'MACD_Signal': 0.20,
        'Reversal_Signal': 0.05  # Small addition in case of unexpected major reversals
    }
}
