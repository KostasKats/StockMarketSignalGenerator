from enums.InvestType import InvestType


WEIGHT_MAPPING_HIGH_RISK_BUY = {
    InvestType.SHORT.value: {
        'MA_Signal': 0.30,
        'RSI_Signal': 0.30,
        'MACD_Signal': 0.15,  # MACD is useful in strong uptrends
        'Reversal_Signal': 0.25
    },
    InvestType.MID.value: {
        'MA_Signal': 0.50,
        'RSI_Signal': 0.25,
        'MACD_Signal': 0.20,
        'Reversal_Signal': 0.05
    },
    InvestType.LONG.value: {
        'MA_Signal': 0.55,
        'RSI_Signal': 0.20,
        'MACD_Signal': 0.20,
        'Reversal_Signal': 0.05
    }
}

WEIGHT_MAPPING_HIGH_RISK_SELL = {
    InvestType.SHORT.value: {
        'MA_Signal': 0.25,  # Slightly lower since price might still be above MA
        'RSI_Signal': 0.20,  # RSI has a smaller role in exits
        'MACD_Signal': 0.30,  # Increased weight for trend reversals
        'Reversal_Signal': 0.25  # Important in fast reversals
    },
    InvestType.MID.value: {
        'MA_Signal': 0.40,  # Reduced compared to buy since sell-offs can happen below MA
        'RSI_Signal': 0.20,
        'MACD_Signal': 0.30,  # More weight since MACD detects weakening momentum
        'Reversal_Signal': 0.10  # Higher than buy to catch trend shifts early
    },
    InvestType.LONG.value: {
        'MA_Signal': 0.50,
        'RSI_Signal': 0.15,
        'MACD_Signal': 0.30,  # Important in exits to confirm trend change
        'Reversal_Signal': 0.05
    }
}

WEIGHT_MAPPING_LOW_RISK_BUY = {
    InvestType.SHORT.value: {
        'MA_Signal': 0.50,
        'RSI_Signal': 0.30,
        'MACD_Signal': 0.05,
        'Reversal_Signal': 0.15
    },
    InvestType.MID.value: {
        'MA_Signal': 0.55,
        'RSI_Signal': 0.30,
        'MACD_Signal': 0.10,
        'Reversal_Signal': 0.05
    },
    InvestType.LONG.value: {
        'MA_Signal': 0.60,
        'RSI_Signal': 0.25,
        'MACD_Signal': 0.10,
        'Reversal_Signal': 0.05
    }
}

WEIGHT_MAPPING_LOW_RISK_SELL = {
    InvestType.SHORT.value: {
        'MA_Signal': 0.45,  # Slightly reduced since price might be above MA
        'RSI_Signal': 0.25,  # RSI plays a lesser role in exits
        'MACD_Signal': 0.15,  # Increased since trend confirmation is key
        'Reversal_Signal': 0.15
    },
    InvestType.MID.value: {
        'MA_Signal': 0.50,
        'RSI_Signal': 0.25,
        'MACD_Signal': 0.15,
        'Reversal_Signal': 0.10
    },
    InvestType.LONG.value: {
        'MA_Signal': 0.55,
        'RSI_Signal': 0.20,
        'MACD_Signal': 0.15,
        'Reversal_Signal': 0.10
    }
}

