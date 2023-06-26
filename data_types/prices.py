from dataclasses import dataclass
from datetime import datetime


@dataclass
class DailyTokenPrice:
    """Token pricing (min, max, first, last) for a specific day"""

    token: str
    quote_day: datetime
    first_price: float
    last_price: float
    daily_minimum_price: float
    daily_maximum_price: float
    rolling_minimum_price: float
    rolling_maximum_price: float
    rolling_volatility: float
