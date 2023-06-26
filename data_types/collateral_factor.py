from dataclasses import dataclass
from datetime import datetime


@dataclass
class CollateralFactorStats:
    """Token pricing (min, max, first, last) for a specific day"""

    token: str
    min_datetime: datetime
    max_datetime: datetime
    averageCollateralFactor: float
    latestCollateralFactor: float
    minCollateralFactor: float
    maxCollateralFactor: float
    p10CollateralFactor: float
    p50CollateralFactor: float
    p80CollateralFactor: float
