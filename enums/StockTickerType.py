from enum import Enum


class StockTickerType(Enum):
    OPEN = "Open"
    CLOSE = "Close"
    HIGH = "High"
    LOW = "Low"
    VOLUME = "Volume"

class InvestType(Enum):
    SHORT = "short"
    MID = "mid"
    LONG = "long"
